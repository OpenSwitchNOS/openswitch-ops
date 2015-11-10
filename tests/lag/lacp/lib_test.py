# (C) Copyright 2015 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import pytest
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *
import re
import pexpect
import random
import time
from math import ceil
from math import floor
from datetime import timedelta


def expecting(expectHndl, command):
    '''
    Wraps the process of sending a command to a device CLI and expecting
    an output as long as the CLI always has a '#' character on the prompt

    Args:
        expectHndl (object): pexpect handler
        command (str): Command to be sent through pexpect handler

    Returns:
        bool: True if received prompt, False if timeouts after 20 seconds
    '''
    expectHndl.sendline(command)
    if expectHndl.expect(['#', pexpect.TIMEOUT], timeout=20) != 0:
        LogOutput(
            'error',
            'Timeout while waiting for output of command: %s' % command)
        return False
    return True


def switchTcpdumpInterfaces(deviceObj):
    '''
    Obtains the equivalent names of active interfaces for use with tcpdump

    Mainly used by lagVerifyTrafficFlow

    Args:
        deviceObj (Switch): Switch with active interfaces

    Returns:
        bool, dict: True and dictionary of with keys being the real interfaces
            of switch and the values what tcpdump understands. True and None
            otherwise
    '''

    expectHndl = deviceObj.expectHndl
    res = {}
    if not expecting(expectHndl, 'tcpdump -D'):
        return False, None
    for result in re.findall(r'(\d+)[.](\d+)', expectHndl.before):
        res[result[1]] = result[0]
    return True, res


def deviceStartWiresharkCap(device, deviceLink, filter=None):
    '''
    Initiates a tcpdump capture on a device link on the background
    The capture output is sent to a temporal file

    Mainly used by lagVerifyTrafficFlow

    Args:
        device (Device): Device on which a capture is started
        deviceLink (str): Interface on device to start capture
            Note this is the interface name tcpdump understands
            See switchTcpdumpInterfaces function for more information
        filter (str, optional): Filter for tcpdump to use

    Returns:
        int: Returns process ID of capture on device.
            None if not able to get it
    '''
    expectHndl = device.expectHndl
    command = 'tcpdump -i %s' % deviceLink
    if filter:
        command += ' %s' % filter
    command += ' 1>/tmp/cap%s.test 2>&1 &' % deviceLink
    expecting(expectHndl, command)
    res = re.search(r'\[\d+\] (\d+)', expectHndl.before)
    if res:
        return int(res.group(1))
    else:
        return None


def deviceStopWiresharkCap(device,
                           processId,
                           deviceLink,
                           filter=None,
                           filteresSwitch=None):
    '''
    Stops tcpdump capture on device and reads obtained information
    from temporal file

    Mainly used by lagVerifyTrafficFlow

    Args:
        device (Device): Device on which a capture was started
        processId (int): Process number of capture on device's system
        deviceLink (str): Interface on device in whcih capture was started
            Note this is the interface name tcpdump understands
            See switchTcpdumpInterfaces function for more information
        filter (str, optional): Filter expression to look for desired packets
            in capture
        filteresSwitch (str, optional): Second filter expression

    Returns:
        dict: Dictionary with parsed information
            filtered (int): Number of filtered packets if a filter was
                defined in deviceStartWiresharkCap
            total (int): Total number of packets capture
            filtered_matches (int, optional): Number of packets matching
                filter argument
            filtered_matches2 (int, optional): Number of packets matching
                filteresSwitch argument
            raw (str): Raw output obtained from capture
    '''
    expectHndl = device.expectHndl
    expecting(expectHndl, 'kill %d' % int(processId))
    time.sleep(1)
    for i in xrange(0, 2):
        expecting(expectHndl, '')
    expecting(expectHndl, 'cat /tmp/cap%s.test' % deviceLink)
    res = {}

    try:
        match = re.search(
            r'(\d+) packets received by filter', expectHndl.before)
        if match:
            res['filtered'] = match.group(1)
        else:
            res['filtered'] = 0
        match = re.search(r'(\d+) packets captured', expectHndl.before)
        if match:
            res['total'] = match.group(1)
        else:
            res['total'] = 0
        if filter:
            match = re.findall(filter, expectHndl.before)
            if match:
                res['filtered_matches'] = len(match)
            else:
                res['filtered_matches'] = 0
        if filteresSwitch:
            match = re.findall(filteresSwitch, expectHndl.before)
            if match:
                res['filtered_matches2'] = len(match)
            else:
                res['filtered_matches2'] = 0
        res['raw'] = expectHndl.before
    except Exception as e:
        LogOutput('error',
                  'Error while deciphering packets ' +
                  'obtained by Wireshark for device %s' %
                  str(device.device))
        LogOutput('error', 'Exception:\n%s' % e)
        return None
    return res


def devicesGetActiveMacAddresses(devices):
    '''
    Creates a list with all the MAC addresses used by all devices in
    the links of interest

    Mainly used by lagVerifyTrafficFlow

    Args:
        devices (list[dict]): Dictionary of information of interes for
            each device

    Returns:
        list[str]: List of MAC address on all devices' links of interest
    '''
    macList = []
    linkTypes = ['wrkston_link', 'lag_links']
    for device in devices:
        expectHndl = device['obj'].expectHndl
        expecting(expectHndl, 'ifconfig')
        for linkType in linkTypes:
            for link in device[linkType]:
                try:
                    macList.append(
                        re.search(r'%s.*?(\w{2}'
                                  % device[linkType][link] +
                                  r':\w{2}:\w{2}' +
                                  r':\w{2}:\w{2}:\w{2})',
                                  expectHndl.before).group(1).upper())
                except AttributeError:
                    return None
    macList.append('00:00:00:00:00:00')
    macList.append('FF:FF:FF:FF:FF:FF')
    return macList


def deviceObtainActiveMacAddresses(device, links):
    '''
    Creates a list with all the MAC addresses used by a devices in
    the links of interest

    Since the device can either be a switch or a workstation, it is
    up to the user of this function to handle device contexts correctly

    Args:
        device (object): Device to which the MAC addresses will be obtained
        links (list[str]): List of links as defined in topology (ie: lnk01)
            that belong to the device

    Returns:
        list[str]: List of MAC address on all devices' links of interest
    '''
    macList = []
    expectHndl = device.expectHndl
    expecting(expectHndl, 'ifconfig')
    for link in links:
        try:
            macList.append(
                re.search(r'%s.*?(\w{2}'
                          % device.linkPortMapping[link] +
                          r':\w{2}:\w{2}' +
                          r':\w{2}:\w{2}:\w{2})',
                          expectHndl.before).group(1).upper())
        except AttributeError:
            return None
    return macList


def generateMacAddress(macList):
    '''
    Generates a new MAC address to use and verifies it is not in use

    Mainly used by lagVerifyTrafficFlow

    Args:
        macList (list[str]): MAC address list with used MAC addresses

    Returns:
        str: New MAC address not already in use
    '''
    random.seed()
    while True:
        mac = '%X:%X:%X:%X:%X:%X' % (random.randint(0, 255),
                                     random.randint(0, 255),
                                     random.randint(0, 255),
                                     random.randint(0, 255),
                                     random.randint(0, 255),
                                     random.randint(0, 255))
        if mac not in macList:
            macList.append(mac)
            return mac


def generateIPAddress(ipAddrList, prefix):
    '''
    Generates a new IP address to use and verifies it is not in use

    Mainly used by lagVerifyTrafficFlow

    Args:
        ipAddrList (list[str]): List of IP addresses already employed
        prefix: First 3 octets of IP address range to use

    Returns:
        str: IP address not already in use
    '''
    random.seed()
    while True:
        if len(ipAddrList) == 256:
            return None
        ipAddr = '%s.%d' % (prefix, random.randint(0, 255))
        if ipAddr not in ipAddrList:
            ipAddrList.append(ipAddr)
            return ipAddr


def lagBroadcastTrafficTest(wrkstonSrc,
                            wrkstonDst,
                            dut01,
                            dut02,
                            randomUnusedIPAddress):
    '''
    Tests if LAG is able to correctly handle broadcast packets

    Note: Internally, captures are only done on the switch receiving
        the broadcast messages, this is by design and not an oversight

    Mainly used by lagVerifyTrafficFlow

    Args:
        wrkstonSrc (dict): Information of workstation that will generate
            broadcast frames
        wrkstonDst (dict): Information of workstation that will receive
            broadcast frames
        dut01 (dict): Information of switch that is connected to
            wrkstonSrc
        dut02 (dict): Information of switch that is connected to
            wrkstonDst
        randomUnusedIPAddress (str): IP address not in use but in the
            same range as those used by workstations so the source can
            generate ARP broadcast messages

    Returns:
        bool: True if the test passed, False if not
    '''
    procsSwitches = []
    procsWrkstons = []
    resSwitches = []
    resWrkstons = []
    linksWithTraffic = []
    errTolerance = 0.1
    minValue = 0
    maxValue = 0
    LogOutput('info', 'Initiate traffic captures on switch %s links...' %
              dut02['obj'].device)
    for link in dut02['lag_links']:
        try:
            procSwitch = deviceStartWiresharkCap(
                dut02['obj'],
                dut02['tcpdump_links'][dut02['lag_links'][link]],
                'arp')
            time.sleep(2)
            if not (procSwitch):
                raise RuntimeError('Unable to start capture on device')
            procsSwitches.append(procSwitch)
        except KeyError as e:
            LogOutput('error', 'One interface of device is not active')
            return False
        except Exception as e:
            LogOutput(
                'error', 'Error while starting traffic capture on' +
                ' switches to measure broadcast traffic')
            LogOutput('debug', 'Exception information:\n%s' % e)
            return False
    for wrkston in [wrkstonSrc, wrkstonDst]:
        LogOutput('info', 'Initiate traffic capture on workstation %s' %
                  wrkston['obj'].device)
        procWrkston = deviceStartWiresharkCap(
            wrkston['obj'], wrkston['wrkston_link'].values()[0], 'arp')
        time.sleep(2)
        if not (procWrkston):
            raise RuntimeError('Unable to start capture on device')
        procsWrkstons.append(procWrkston)
    LogOutput('info', 'Transmit broadcast traffic')
    wrkstonSrc['obj'].Ping(ipAddr=randomUnusedIPAddress)
    time.sleep(2)
    LogOutput('info', 'Stop traffic captures on switch %s links...' %
              dut02['obj'].device)
    for procSwitch, link in zip(procsSwitches, dut01['lag_links'].keys()):
        resSwitches.append(deviceStopWiresharkCap(dut02['obj'],
                                                  procSwitch,
                                                  dut02['tcpdump_links']
                                                  [dut02['lag_links'][link]],
                                                  'who-has %s tell %s' %
                                                  (randomUnusedIPAddress,
                                                   wrkstonSrc['wrkston_ip'])))
    for procWrkston, wrkston in zip(procsWrkstons, [wrkstonSrc, wrkstonDst]):
        LogOutput('info', 'Stop traffic capture on ' +
                  'workstation %s...' % wrkston['obj'].device)
        resWrkstons.append(deviceStopWiresharkCap(wrkston['obj'],
                                                  procWrkston,
                                                  wrkston['wrkston_link'].
                                                  values()[0],
                                                  'who-has %s tell %s' %
                                                  (randomUnusedIPAddress,
                                                   wrkstonSrc['wrkston_ip'])))
    LogOutput('info', 'Analyzing results...')
    # obtain numbers of max/min allowed values
    minValue = int(floor(float(resWrkstons[0]['filtered_matches']) *
                         (1 - errTolerance)))
    maxValue = int(ceil(float(resWrkstons[0]['filtered_matches']) *
                        (1 + errTolerance)))
    # begin comparisons
    for resSwitch, link in zip(resSwitches, dut01['lag_links'].keys()):
        if resSwitch['filtered_matches'] > 0:
            linksWithTraffic.append(link)
            if resSwitch['filtered_matches'] < minValue:
                LogOutput('error',
                          'Less traffic than expected was seen on' +
                          ' LAG link: Expected: At least %d - ' % minValue +
                          'Actual: %d' % resSwitch['filtered_matches'])
                LogOutput('error', 'Interface on device %s is %s' %
                          (dut01['obj'].device,
                           dut01['lag_links'][link]))
                LogOutput('error', 'Interface on device %s is %s' %
                          (dut02['obj'].device,
                           dut02['lag_links'][link]))
                return False
            if resSwitch['filtered_matches'] > maxValue:
                LogOutput('error',
                          'More traffic than expected was seen on LAG' +
                          ' link: Expected: At most %d - ' % maxValue +
                          'Actual: %d' % resSwitch['filtered_matches'])
                LogOutput('error', 'Interface on device %s is %s' %
                          (dut01['obj'].device,
                           dut01['lag_links'][link]))
                LogOutput('error', 'Interface on device %s is %s' %
                          (dut02['obj'].device,
                           dut02['lag_links'][link]))
                return False

    if resWrkstons[1]['filtered_matches'] < minValue:
        LogOutput(
            'error',
            'Less traffic than expected was received after client' +
            ' broadcast transmission on another workstation')
        LogOutput('error', 'Expected: At least %s - Actual: %d' %
                  (minValue, resWrkstons[1]['filtered_matches']))
        return False
    if resWrkstons[1]['filtered_matches'] > maxValue:
        LogOutput(
            'error',
            'More traffic than expected was received after client' +
            ' broadcast transmission on another workstation')
        LogOutput('error', 'Expected: At most %d - Actual: %d' %
                  (maxValue, resWrkstons[1]['filtered_matches']))
        return False

    if len(linksWithTraffic) < 1:
        LogOutput('error', 'No traffic traversed the switches')
        return False
    if len(linksWithTraffic) > 1:
        LogOutput(
            'error', 'More than 1 interface carried broadcast traffic')
        for dut in [dut01, dut02]:
            LogOutput('error', 'Device %s' % dut['obj'])
            for i in linksWithTraffic:
                LogOutput('error', 'Interface %s' % i)
        return False
    LogOutput('info', 'Broadcast traffic handled as expected')
    return True


def swtichGetIntoVtyshOrSwns(device, enter=True):
    '''
    Normalizes device prompt so it can be handled by standard framework
    functions or enters switch bash context

    Mainly used by lagVerifyTrafficFlow

    Args:
        device (dict): Information of device
        enter (bool, optional): Controls whether the function attempts
            to normalize the device prompt or get to switch bash context

    Returns:
        bool: True if managed to get into VTYSH or into switch bash
            context, False otherwise
    '''

    expectHndl = device.expectHndl

    if enter:
        if not expecting(expectHndl, 'exit'):
            LogOutput(
                'error', 'Could not return to VTYSH on device %s' %
                device.device)
            return False
        if not expecting(expectHndl, 'vtysh'):
            LogOutput(
                'error', 'Could not return to VTYSH on device %s' %
                device.device)
            device.deviceContext = 'linux'
            return False
    else:
        if device.deviceContext != 'vtyShell':
            retStruct = device.VtyshShell(enter=True)
            if retStruct.returnCode() != 0:
                LogOutput('error', 'Could not enter vtysh on device %s' %
                          device.device)
                return False
        if not expecting(expectHndl, 'exit'):
            LogOutput('error', 'Could not exit vtysh context on device' +
                      ' %s' % device.device)
            return False
        if not expecting(expectHndl, 'ip netns exec swns bash'):
            LogOutput('error', 'Could not enter switch bash context on' +
                      ' device %s' % device.device)
            device.deviceContext = 'linux'
            return False
    return True


def interfaceGetCounters(device, interface):
    '''
    Obtains packet counters of interface on device

    Mainly used by lagVerifyTrafficFlow

    Args:
        device (dict): Information of device
        interface (str): Interface from which to get information

    Returns:
        dict: Dictionary with interface counters
            input_packets (int): Number of packets entering interface
            output_packets (int): Number of packets exiting interface
            input_bytes (int): Number of bytes entering interface
            output_bytes (int): Number of bytes exiting interface
    '''
    expectHndl = device['obj'].expectHndl
    if not expecting(expectHndl, 'show interface %s' % interface):
        return None
    res = {}
    input = re.search(r'(\d+) input packets\s+(\d+) bytes',
                      expectHndl.before)
    res['input_packets'] = int(input.group(1))
    res['input_bytes'] = int(input.group(2))
    output = re.search(r'(\d+) output packets\s+(\d+) bytes',
                       expectHndl.before)
    res['output_packets'] = int(output.group(1))
    res['output_bytes'] = int(output.group(2))
    return res


def workstationChangeInfo(device, macAddr, ipAddr):
    '''
    Changes a workstation MAC address and IP address

    Mainly used by lagVerifyTrafficFlow

    Args:
        device (dict): Information or workstation
        macAddr (str): MAC address to replace current one in workstation
        ipAddr (str): IP address to replace current one in workstation

    Returns:
        None
    '''
    expectHndl = device['obj'].expectHndl
    expecting(expectHndl, 'ifconfig %s' %
              device['wrkston_link'].values()[0])
    match = re.search(
        r'Bcast:(\d+[.]\d+[.]\d+[.]\d+).*Mask:(\d+[.]\d+[.]\d+[.]\d+)',
        expectHndl.before)
    bcast = match.group(1)
    mask = match.group(2)
    expecting(expectHndl, 'ifconfig %s down' %
              device['wrkston_link'].values()[0])
    expecting(expectHndl, 'ifconfig %s hw ether %s' %
              (device['wrkston_link'].values()[0], macAddr))
    expecting(expectHndl, 'ifconfig %s up' %
              device['wrkston_link'].values()[0])
    expecting(expectHndl, 'ifconfig %s down' %
              device['wrkston_link'].values()[0])
    expecting(expectHndl, 'ifconfig  %s %s netmask %s broadcast %s' %
              (device['wrkston_link'].values()[0], ipAddr, mask, bcast))
    expecting(expectHndl, 'ifconfig %s up' %
              device['wrkston_link'].values()[0])
    device['wrkston_ip'] = ipAddr


def switchGetInterfaceCounters(device):
    '''
    Obtains the interface counters for all LAG links in a device

    Mainly used by lagVerifyTrafficFlow

    Args:
        device (dict): Device information

    Returns:
        list[dict]: List of interface counters for all device's LAG links
    '''
    res = []
    for interface in device['lag_links'].values():
        res.append(interfaceGetCounters(device, interface))
    return res


def switchAnalyzeInterfaceCounters(countersDut01,
                                   countersDut02,
                                   countersDut01After,
                                   countersDut02After,
                                   offset=None):
    '''
    Analyzes interface counters obtained from 2 switches at different
    times and calculates statistics based on packets transferred

    Mainly used by lagVerifyTrafficFlow

    Args:
        countersDut01 (list[dict]): Counters of switch 1 on moment 1
        countersDut02 (list[dict]): Counters of switch 2 on moment 1
        countersDut01After (list[dict]): Counters of switch 1 on moment 2
        countersDut02After (list[dict]): Counters of switch 2 on moment 2
        offset (list[int], optional): List of offset values to adjust
            interface traffic to account for idle traffic like that from
            LACP protocol

    Returns:
            list[dict]: List of dictionaries with the information of the
                analysis performed
                    net_traffic01 (int): Net traffic that traversed
                        interface on switch 1. Positive values indicate more
                        output than input
                    net_traffic02 (int): Net traffic that traversed
                        interface on switch 2. Positive values indicate more
                        output than input
                    traffic_mismatch (bool): If there is too much difference
                        between what 1 switch reports comprared to the other
                        in terms of total traffic transmitted either downlink
                        or uplink
                    uplink_traffic (int): Uplink packets minus offset. Minimum
                        value is 0
                    downlink_traffic (int): Downlink packets minus offset.
                        Minimum value is 0
                    excess_traffic (bool): If too many packets are transmitted
                        uplink
                    low_traffic (bool): If too few packets are transmitted
                        uplink
    '''
    difCounters01 = []
    difCounters02 = []
    res = []
    typesOfCounters = ['input_packets', 'output_packets']
    for i, typeOfCounter in enumerate(typesOfCounters):
        for k in xrange(0, len(countersDut01)):
            if i == 0:
                difCounters01.append({})
                difCounters02.append({})
            difCounters01[k][typeOfCounter] = countersDut01After[
                k][typeOfCounter] - countersDut01[k][typeOfCounter]
            difCounters02[k][typeOfCounter] = countersDut02After[
                k][typeOfCounter] - countersDut02[k][typeOfCounter]
    for dif1, dif2, i in zip(difCounters01,
                             difCounters02,
                             xrange(0, len(difCounters01))):
        dictionary = {}
        dictionary['net_traffic01'] = dif1[
            'output_packets'] - dif1['input_packets']
        dictionary['net_traffic02'] = dif2[
            'output_packets'] - dif2['input_packets']
        dictionary['traffic_mismatch'] = abs(
            abs(dictionary['net_traffic01']) -
            abs(dictionary['net_traffic02'])) > 2
        traffic = dif1['output_packets']
        if offset:
            traffic -= offset[i]
        if traffic < 0:
            traffic = 0
        dictionary['uplink_traffic'] = traffic
        traffic = dif1['input_packets']
        if offset:
            traffic -= offset[i]
        if traffic < 0:
            traffic = 0
        dictionary['downlink_traffic'] = traffic
        dictionary['active_link'] = dictionary[
            'uplink_traffic'] > 4 or dictionary['downlink_traffic'] > 4
        dictionary['excess_traffic'] = dictionary[
            'uplink_traffic'] > 15 or dictionary['downlink_traffic'] > 15
        dictionary['low_traffic'] = (dictionary['uplink_traffic'] < 8
                                     and dictionary['uplink_traffic'] >
                                     4)or (
            dictionary['downlink_traffic'] < 8 and
            dictionary['downlink_traffic'] > 4)
        res.append(dictionary)
    return res


def switchAnalyzeInterfaceCountersBytes(countersDut01,
                                        countersDut02,
                                        countersDut01After,
                                        countersDut02After,
                                        offset=None, minTrafficBytes=125000.0,
                                        maxTrafficBytes=1250000.0,
                                        errTolerance=0.1):
    '''
    Analyzes interface counters obtained from 2 switches at different
    times and calculates statistics based on bytes transferred

    Mainly used by lagVerifyTrafficFlow

    Args:
        countersDut01 (list[dict]): Counters of switch 1 on moment 1
        countersDut02 (list[dict]): Counters of switch 2 on moment 1
        countersDut01After (list[dict]): Counters of switch 1 on moment 2
        countersDut02After (list[dict]): Counters of switch 2 on moment 2
        offset (list[int], optional): List of offset values to adjust
            interface traffic to account for idle traffic like that from
            LACP protocol

    Returns:
            list[dict]: List of dictionaries with the information of the
                analysis performed
                    net_traffic01 (int): Net traffic that traversed
                        interface on switch 1. Positive values indicate more
                        output than input
                    net_traffic02 (int): Net traffic that traversed
                        interface on switch 2. Positive values indicate more
                        output than input
                    traffic_mismatch (bool): If there is too much difference
                        between what 1 switch reports comprared to the other
                        in terms of total traffic transmitted either downlink
                        or uplink
                    uplink_traffic (int): Uplink bytes minus offset. Minimum
                        value is 0
                    downlink_traffic (int): Downlink bytes minus offset.
                        Minimum value is 0
                    excess_traffic (bool): If too many bytes are transmitted
                        uplink
                    low_traffic (bool): If too few bytes are transmitted
                        uplink
    '''
    difCounters01 = []
    difCounters02 = []
    res = []
    typesOfCounters = ['input_bytes', 'output_bytes']
    for i, typeOfCounter in enumerate(typesOfCounters):
        for k in xrange(0, len(countersDut01)):
            if i == 0:
                difCounters01.append({})
                difCounters02.append({})
            difCounters01[k][typeOfCounter] = countersDut01After[
                k][typeOfCounter] - countersDut01[k][typeOfCounter]
            difCounters02[k][typeOfCounter] = countersDut02After[
                k][typeOfCounter] - countersDut02[k][typeOfCounter]
    for dif1, dif2, i in zip(difCounters01,
                             difCounters02,
                             xrange(0, len(difCounters01))):
        dictionary = {}
        dictionary['net_traffic01'] = (dif1['output_bytes'] -
                                       dif1['input_bytes'])
        dictionary['net_traffic02'] = (dif2['output_bytes'] -
                                       dif2['input_bytes'])
        dictionary['traffic_mismatch'] = abs(
            abs(dictionary['net_traffic01']) -
            abs(dictionary['net_traffic02'])) > int(minTrafficBytes *
                                                    (1 + errTolerance))
        traffic = dif1['output_bytes']
        if offset:
            traffic -= offset[i]
        if traffic < 0:
            traffic = 0
        dictionary['uplink_traffic'] = traffic
        traffic = dif1['input_bytes']
        if offset:
            traffic -= offset[i]
        if traffic < 0:
            traffic = 0
        dictionary['downlink_traffic'] = traffic
        dictionary['active_link'] = (dictionary['uplink_traffic'] >
                                     int(minTrafficBytes *
                                         (1 - errTolerance)) or
                                     dictionary['downlink_traffic'] >
                                     int(minTrafficBytes * (1 -
                                                            errTolerance)))
        dictionary['excess_traffic'] = (dictionary['uplink_traffic'] >
                                        int(maxTrafficBytes *
                                            (1 + errTolerance)) or
                                        dictionary['downlink_traffic'] >
                                        int(maxTrafficBytes *
                                            (1 + errTolerance)))
        dictionary['low_traffic'] = ((dictionary['uplink_traffic'] <
                                      int(maxTrafficBytes *
                                          (1 - errTolerance)) and
                                      dictionary['uplink_traffic'] >
                                      int(minTrafficBytes *
                                          (1 - errTolerance))) or
                                     (dictionary['downlink_traffic'] <
                                      int(maxTrafficBytes *
                                          (1 - errTolerance)) and
                                      dictionary['downlink_traffic'] >
                                      int(minTrafficBytes *
                                          (1 - errTolerance))))
        res.append(dictionary)
    return res


def lagUnicastTrafficTest(wrkstonSrc,
                          wrkstonDst,
                          dut01,
                          dut02,
                          macList,
                          ipAddrList,
                          ipPrefix):
    '''
    Tests the LAG is able to transmit Unicast traffic employing each
    active link with different types of traffic

    Each traffic transmission test sends 10 seconds worth of traffic at
    1 Mbps

    Since the device counters don't update immediatly, the function waits
    the 10 seconds of the test plus some more time. By default the full
    waiting time is 20 seconds

    Used mainly by lagVerifyTrafficFlow

    Args:
        wrkstonSrc (dict): Information of workstation that will generate
            unicast packets
        wrkstonDst (dict): Information of workstation that will receive
            unicast packets
        dut01 (dict): Information of switch that is connected to
            wrkstonSrc
        dut02 (dict): Information of switch that is connected to
            wrkstonDst
        macList (list[str]): List of MAC addresses already in use to
            generate new MAC address for wrkstonDst to use
        ipAddrList (list[str]): List of IP addresses already in use to
            generate new IP address for wrkstonDst to use

    Returns:
        bool: True if test passed, False otherwise
    '''
    linksUsed = []
    expectedUsedLinks = dut01['lag_links'].keys()
    offset = []
    error = False
    trafficTransmit = 1250000.0
    minTrafficTransmit = trafficTransmit * 0.1
    errTolerance = 0.1
    maxTrafficReceived = int(ceil(trafficTransmit * (1 + errTolerance)))
    minTrafficReceived = int(floor(trafficTransmit * (1 - errTolerance)))
    timeToWait = 20
    # idle setup values
    LogOutput('info', 'Obtain setup idle traffic behavior...')
    values11 = switchGetInterfaceCounters(dut01)
    values21 = switchGetInterfaceCounters(dut02)
    time.sleep(timeToWait)
    values12 = switchGetInterfaceCounters(dut01)
    values22 = switchGetInterfaceCounters(dut02)
    analysis = switchAnalyzeInterfaceCountersBytes(
        values11, values21, values12, values22)
    for res in analysis:
        if res['traffic_mismatch']:
            LogOutput(
                'error',
                'Error obtaining idle values in setup Verify there are' +
                ' no external sources of traffic present')
            return False
        offset.append(res['uplink_traffic'])
    while len(linksUsed) < len(expectedUsedLinks):
        LogOutput('info', 'Modifying setup to start traffic ' +
                  'transmission...')
        macAddr = generateMacAddress(macList)
        ipAddr = generateIPAddress(ipAddrList, ipPrefix)
        if not ipAddr:
            LogOutput(
                'error',
                'Could not get traffic to use all LAG interfaces')
            return False
        workstationChangeInfo(wrkstonDst, macAddr, ipAddr)
        values11 = switchGetInterfaceCounters(dut01)
        values21 = switchGetInterfaceCounters(dut02)

        # Traffic transmission
        LogOutput('info', 'Starting traffic transmission...')
        LogOutput('info', 'Starting iperf server on device %s...' %
                  wrkstonDst['obj'].device)
        retStruct = hostIperfServerStart(deviceObj=wrkstonDst['obj'],
                                         protocol='UDP')
        if retStruct.returnCode() != 0:
            LogOutput('error', 'Could not start iperf server on ' +
                      'device %s' % wrkstonDst['obj'].device)
            return False
        time.sleep(2)
        LogOutput('info', 'Starting iperf client on device %s...' %
                  wrkstonSrc['obj'].device)
        retStruct = hostIperfClientStart(deviceObj=wrkstonSrc['obj'],
                                         protocol='UDP',
                                         serverIP=wrkstonDst['wrkston_ip'],
                                         time=10)
        if retStruct.returnCode() != 0:
            LogOutput('error', 'Could not start iperf client on ' +
                      'device %s' % wrkstonDst['obj'].device)
            error = True
        if not error:
            time.sleep(timeToWait)
            LogOutput('info', 'Stopping iperf client on device %s...' %
                      wrkstonSrc['obj'].device)
            retStructClient = hostIperfClientStop(
                deviceObj=wrkstonSrc['obj'])
            if retStructClient.returnCode() != 0:
                LogOutput('error', 'Could not stop iperf client on ' +
                          'device %s' % wrkstonDst['obj'].device)

                error = True
        LogOutput('info', 'Stopping iperf server on device %s...' %
                  wrkstonDst['obj'].device)
        retStruct = hostIperfServerStop(deviceObj=wrkstonDst['obj'])
        if retStruct.returnCode() != 0 or error:
            if retStruct.returnCode() != 0:
                LogOutput('error', 'Could not stop iperf server on ' +
                          'device %s' % wrkstonDst['obj'].device)
            return False
        if error:
            return False

        LogOutput('info', 'Analyzing results...')

        '''
        If everything is correct, the iperf client should have the
        Server report (traffic received by iperf server as reported by it)
        '''

        trafficReceived = re.findall(r'Server Report:.*(\d+[.]\d+) ' +
                                     r'MBytes ', retStructClient.buffer(),
                                     flags=re.DOTALL)
        if len(trafficReceived) != 1:
            LogOutput('error', 'Error in communication between iperf ' +
                      'client and host')
            LogOutput('error', 'Iperf client could not obtain traffic ' +
                      'report from server')
            return False
        trafficReceived = int(float(trafficReceived[0]) * 1000000)
        if trafficReceived > maxTrafficReceived:
            LogOutput('error', 'Traffic received by server is more ' +
                      'than expected')
            LogOutput('error', 'Expected: At most %d bytes' %
                      maxTrafficReceived)
            LogOutput('error', 'Actual: %d bytes' % trafficReceived)
            return False
        if trafficReceived < minTrafficReceived:
            LogOutput('error', 'Traffic received by server is less ' +
                      'than expected')
            LogOutput('error', 'Expected: At least %d bytes' %
                      minTrafficReceived)
            LogOutput('error', 'Actual: %d bytes' % trafficReceived)
            return False

        values12 = switchGetInterfaceCounters(dut01)
        values22 = switchGetInterfaceCounters(dut02)
        analysis = switchAnalyzeInterfaceCountersBytes(
            values11, values21, values12, values22, offset)
        linksWithTraffic = []
        for i, res in enumerate(analysis):
            if res['traffic_mismatch']:
                LogOutput('error',
                          'The counters of both sides of a LAG are ' +
                          'not displaying the same values: %s' %
                          dut01['lag_links'].keys()[i])
                return False
            if res['active_link']:
                LogOutput('info', 'Link %s was used to transmit traffic' %
                          dut01['lag_links'].keys()[i])
                if res['uplink_traffic'] > int(minTrafficTransmit *
                                               (1 - errTolerance)):
                    linksWithTraffic.append(dut01['lag_links'].keys()[i])
                if res['excess_traffic']:
                    LogOutput(
                        'error',
                        'Detected excess traffic on a link: %s' %
                        dut01['lag_links'].keys()[i])
                    LogOutput(
                        'error',
                        'Uplink expected: Max of %d bytes - Uplink ' %
                        maxTrafficReceived +
                        'detected: %d bytes' % res['uplink_traffic'])
                    LogOutput(
                        'error',
                        'Downlink expected: Max of %d bytes - ' %
                        int(trafficTransmit * (1 + errTolerance)) +
                        'Downlink detected: %d packets' %
                        res['downlink_traffic'])
                    return False
                if res['low_traffic']:
                    LogOutput('error',
                              'Detected lower than expected traffic ' +
                              'on a link: %s' %
                              dut01['lag_links'].keys()[i])
                    LogOutput(
                        'error',
                        'From the values below, one is above %d and ' %
                        minTrafficTransmit +
                        'below %d' % minTrafficReceived)
                    LogOutput(
                        'error', 'Uplink detected: %d packets' %
                        res['uplink_traffic'])
                    LogOutput(
                        'error', 'Downlink detected: %d packets' %
                        res['downlink_traffic'])
                    return False

        if len(linksWithTraffic) < 1:
            LogOutput('error', 'No traffic traversed the switches')
            return False
        if len(linksWithTraffic) > 1:
            LogOutput(
                'error', 'More than 1 interface carried unicast traffic')
            for dut in [dut01, dut02]:
                LogOutput('debug', 'Device %s' % dut['obj'])
                for i in linksWithTraffic:
                    LogOutput('debug', 'Interface %s' % i)
            return False
        if linksWithTraffic[0] not in linksUsed:
            LogOutput('info', 'Link %s was used to transmit ' %
                      linksWithTraffic[0] + 'traffic')
            linksUsed.append(linksWithTraffic[0])
            if len(linksUsed) == len(expectedUsedLinks):
                break
        else:
            LogOutput('info', 'Link %s was used again to transmit ' %
                      linksWithTraffic[0] + 'traffic')
        LogOutput('info', 'Finished analysis successfully')
    LogOutput('info', 'Unicast test finished successfully')
    return True


def lagUnicastTrafficTestVirtual(wrkstonSrc,
                                 wrkstonDst,
                                 dut01,
                                 dut02,
                                 macList,
                                 ipAddrList,
                                 ipPrefix):
    '''
    Tests the LAG is able to transmit Unicast traffic employing each
    active link with different types of traffic on virtual devices

    Each traffic transmission test sends 10 seconds worth of traffic at
    1 Mbps

    The function waits by default 14 seconds instead of 10 just to give
    a better chance for iperf and tcpdump to wrap on all virtual devices

    Used mainly by lagVerifyTrafficFlow

    Args:
        wrkstonSrc (dict): Information of workstation that will generate
            unicast packets
        wrkstonDst (dict): Information of workstation that will receive
            unicast packets
        dut01 (dict): Information of switch that is connected to
            wrkstonSrc
        dut02 (dict): Information of switch that is connected to
            wrkstonDst
        macList (list[str]): List of MAC addresses already in use to
            generate new MAC address for wrkstonDst to use
        ipAddrList (list[str]): List of IP addresses already in use to
            generate new IP address for wrkstonDst to use

    Returns:
        bool: True if test passed, False otherwise
    '''

    procsSwitches = []
    procWrkstonDst = 0
    resSwitches = []
    res3 = None
    linksUsed = []
    error = False
    trafficTransmit = 1250000.0
    # iperf transmits 1470 bytes per packet
    packets = 894
    errTolerance = 0.1
    timeToWait = 14
    maxTrafficReceived = int(ceil(trafficTransmit * (1 + errTolerance)))
    minTrafficReceived = int(floor(trafficTransmit * (1 - errTolerance)))
    maxPackets = int(ceil(packets * (1 + errTolerance)))
    minPackets = int(floor(packets * (1 - errTolerance)))

    expectedUsedLinks = dut01['lag_links'].keys()

    while len(linksUsed) < len(expectedUsedLinks):
        procsSwitches = []
        procWrkstonDst = 0
        resSwitches = []
        res3 = None
        LogOutput('info', 'Modifying setup to start traffic ' +
                  'transmission...')
        macAddr = generateMacAddress(macList)
        ipAddr = generateIPAddress(ipAddrList, ipPrefix)
        if not ipAddr:
            LogOutput(
                'error',
                'Could not get traffic to use all LAG interfaces')
            return False
        # Start traffic capture
        workstationChangeInfo(wrkstonSrc, macAddr, ipAddr)
        LogOutput('info', 'Initiate traffic captures on switch %s links...' %
                  dut02['obj'].device)
        for link in dut02['lag_links']:
            try:
                procSwitch = deviceStartWiresharkCap(
                    dut02['obj'],
                    dut02['tcpdump_links'][dut02['lag_links'][link]],
                    '-n src %s and dst %s' % (wrkstonSrc['wrkston_ip'],
                                              wrkstonDst['wrkston_ip']))
                time.sleep(2)
                if not (procSwitch):
                    raise RuntimeError('Unable to start capture on device')
                procsSwitches.append(procSwitch)
            except KeyError as e:
                LogOutput('error', 'One interface of device is not active')
                return False
            except Exception as e:
                LogOutput(
                    'error', 'Error while starting traffic capture on' +
                    ' switches to measure unicast traffic')
                LogOutput('debug', 'Exception information:\n%s' % e)
                return False
        LogOutput('info', 'Initiate traffic capture on destination ' +
                  'workstation %s...' % wrkstonDst['obj'].device)
        procWrkstonDst = deviceStartWiresharkCap(
            wrkstonDst['obj'], wrkstonDst['wrkston_link'].values()[0],
            '-n src %s and dst %s' % (wrkstonSrc['wrkston_ip'],
                                      wrkstonDst['wrkston_ip']))
        time.sleep(2)

        # Traffic transmission
        LogOutput('info', 'Starting traffic transmission...')
        LogOutput('info', 'Starting iperf server on device %s...' %
                  wrkstonDst['obj'].device)
        retStruct = hostIperfServerStart(deviceObj=wrkstonDst['obj'],
                                         protocol='UDP')
        if retStruct.returnCode() != 0:
            LogOutput('error', 'Could not start iperf server on ' +
                      'device %s' % wrkstonDst['obj'].device)
            return False
        time.sleep(2)
        LogOutput('info', 'Starting iperf client on device %s...' %
                  wrkstonSrc['obj'].device)
        retStruct = hostIperfClientStart(deviceObj=wrkstonSrc['obj'],
                                         protocol='UDP',
                                         serverIP=wrkstonDst['wrkston_ip'],
                                         time=10)
        if retStruct.returnCode() != 0:
            LogOutput('error', 'Could not start iperf client on ' +
                      'device %s' % wrkstonDst['obj'].device)
            error = True
        if not error:
            time.sleep(timeToWait)
            LogOutput('info', 'Stopping iperf client on device %s...' %
                      wrkstonSrc['obj'].device)
            retStructClient = hostIperfClientStop(
                deviceObj=wrkstonSrc['obj'])
            if retStructClient.returnCode() != 0:
                LogOutput('error', 'Could not stop iperf client on ' +
                          'device %s' % wrkstonDst['obj'].device)

                error = True
        LogOutput('info', 'Stopping iperf server on device %s...' %
                  wrkstonDst['obj'].device)
        retStruct = hostIperfServerStop(deviceObj=wrkstonDst['obj'])
        if retStruct.returnCode() != 0 or error:
            if retStruct.returnCode() != 0:
                LogOutput('error', 'Could not stop iperf server on ' +
                          'device %s' % wrkstonDst['obj'].device)
            return False
        if error:
            return False

        # Stop traffic capture
        time.sleep(2)
        LogOutput('info', 'Stop traffic captures on switch %s links...' %
                  dut02['obj'].device)
        for procSwitch, link in zip(procsSwitches, dut01['lag_links'].keys()):
            resSwitches.append(deviceStopWiresharkCap(dut02['obj'],
                                                      procSwitch,
                                                      dut02['tcpdump_links']
                                                      [dut02['lag_links']
                                                          [link]],
                                                      ' > %s' %
                                                      wrkstonDst
                                                      ['wrkston_ip']))
        LogOutput('info', 'Stop traffic capture on destination ' +
                  'workstation %s...' % wrkstonDst['obj'].device)
        res3 = deviceStopWiresharkCap(wrkstonDst['obj'],
                                      procWrkstonDst,
                                      wrkstonDst['wrkston_link'].values()[0],
                                      ' > %s' % wrkstonDst['wrkston_ip'])

        LogOutput('info', 'Analyzing results...')

        trafficReceived = re.findall(r'Server Report:.*(\d+[.]\d+) ' +
                                     r'MBytes ', retStructClient.buffer(),
                                     flags=re.DOTALL)
        if len(trafficReceived) != 1:
            LogOutput('error', 'Error in communication between iperf ' +
                      'client and host')
            LogOutput('error', 'Iperf client could not obtain traffic ' +
                      'report from server')
            return False
        trafficReceived = int(float(trafficReceived[0]) * 1000000)
        if trafficReceived > maxTrafficReceived:
            LogOutput('error', 'Traffic received by server is more ' +
                      'than expected')
            LogOutput('error', 'Expected: At most %d bytes' %
                      maxTrafficReceived)
            LogOutput('error', 'Actual: %d bytes' % trafficReceived)
            return False
        if trafficReceived < minTrafficReceived:
            LogOutput('error', 'Traffic received by server is less ' +
                      'than expected')
            LogOutput('error', 'Expected: At least %d bytes' %
                      minTrafficReceived)
            LogOutput('error', 'Actual: %d bytes' % trafficReceived)
            return False

        linksWithTraffic = []
        for resSwitch, link in zip(resSwitches, dut01['lag_links'].keys()):
            if resSwitch['filtered_matches'] > 0:
                linksWithTraffic.append(link)
                if resSwitch['filtered_matches'] < minPackets:
                    LogOutput('error',
                              'Less traffic than expected was seen on' +
                              ' LAG link: Expected packets: %d - ' % packets +
                              'Actual packets: %d' %
                              resSwitch['filtered_matches'])
                    LogOutput('error', 'Expected: At least 10')
                    LogOutput('error', 'Interface on device %s is %s' %
                              (dut01['obj'].device,
                               dut01['lag_links'][link]))
                    LogOutput('error', 'Interface on device %s is %s' %
                              (dut02['obj'].device,
                               dut02['lag_links'][link]))
                    return False
                if resSwitch['filtered_matches'] > maxPackets:
                    LogOutput('error',
                              'More traffic than expected was seen on LAG' +
                              ' link: Expected packets: %d - ' % packets +
                              'Actual packets: %d' %
                              resSwitch['filtered_matches'])
                    LogOutput('error', 'Interface on device %s is %s' %
                              (dut01['obj'].device,
                               dut01['lag_links'][link]))
                    LogOutput('error', 'Interface on device %s is %s' %
                              (dut02['obj'].device,
                               dut02['lag_links'][link]))
                    return False

        if res3['filtered_matches'] < minPackets:
            LogOutput(
                'error',
                'Less traffic than expected was received after client' +
                ' broadcast transmission on another workstation')
            LogOutput('error', 'Expected packets: %d - Actual packets: %d' %
                      (packets, res3['filtered_matches']))
            return False
        if res3['filtered_matches'] > maxPackets:
            LogOutput(
                'error',
                'More traffic than expected was received after client' +
                ' broadcast transmission on another workstation')
            LogOutput('error', 'Expected packets: 894 - Actual packets: %d' %
                      (packets, res3['filtered_matches']))
            return False

        if len(linksWithTraffic) < 1:
            LogOutput('error', 'No traffic traversed the switches')
            return False
        if len(linksWithTraffic) > 1:
            LogOutput(
                'error', 'More than 1 interface carried unicast traffic')
            for dut in [dut01, dut02]:
                LogOutput('debug', 'Device %s' % dut['obj'])
                for i in linksWithTraffic:
                    LogOutput('debug', 'Interface %s' % i)
            return False
        if linksWithTraffic[0] not in linksUsed:
            LogOutput('info', 'Link %s was used to transmit ' %
                      linksWithTraffic[0] + 'traffic')
            linksUsed.append(linksWithTraffic[0])
            if len(linksUsed) == len(expectedUsedLinks):
                break
        else:
            LogOutput('info', 'Link %s was used again to transmit ' %
                      linksWithTraffic[0] + 'traffic')
        LogOutput('info', 'Finished analysis successfully')
    LogOutput('info', 'Unicast test finished successfully')
    return True


def workstationsChangeToNormal(workstations):
    '''
    Changes workstations information back to standard values

    Used mainly by lagVerifyTrafficFlow

    Args:
        workstations (list[dict]): List of workstation

    Returns:
        None
    '''
    for workstation in workstations:
        workstationChangeInfo(workstation,
                              workstation['original_macaddr'],
                              workstation['original_ip'])


def lagVerifyTrafficFlow(dut01,
                         dut02,
                         wrkston01,
                         wrkston02,
                         wrkston01IP,
                         wrkston02IP,
                         lagLinks,
                         wrkston01Link,
                         wrkston02Link,
                         ipPrefix,
                         ipAddrList=None,
                         macList=None):
    '''
    Tests LAG traffic behaviors with broadcast and Unicast packets
    The function assumes the topology is comprised of 2 switches connected
    through a LAG and these devices serve to connect 2 workstation each
    located in one switch port

    Args:
        dut01 (PHost,VSwitch): One of the switches
        dut02 (PSwitch,VSwitch): One of the switches
        wrkston01 (Host): Workstation connected to dut01
        wrkston02 (Host): Workstation connected to dut02
        wrkston01IP (str): IP address of wrkston01
        wrkston02IP (str): IP address of wrkston02
        lagLinks (list[str]): List of symbolic links that are part of a LAG
            The names should be the same as those in topoDict ina test case
        wrkston01Link (str): Link as per in topoDict that denotes the link
            between wrkston01 and dut01
        wrkston02Link (str): Link as per in topoDict that denotes the link
            between wrkston02 and dut02
        ipPrefix (str): Prefix for IP addresses used in workstations
            The function only will work correctly if 3 octets from the IP
            addresses are passed as prefix. Ex: 140.1.1
        ipAddrList (list[str], optional): List of IP addresses that will not
            be used by the function. Please note the function will modify
            the list
        macList ](list[str], optional): List of MAC addresses that will not
            be used by the function. Please note the function will modify
            the list. The MAC address numbers must be upper case and the
            octets separated by ":". Eg: 45:16:C8:BC:56:00

    Returns:
        bool: True if configuration matches, False otherwise
    '''

    dut01Info = {
        'obj': dut01,
        'lag_links': {link_name:
                      dut01.linkPortMapping
                      [link_name] for link_name in lagLinks},
        'wrkston_link': {wrkston01Link: dut01.linkPortMapping[wrkston01Link]}
    }

    dut02Info = {
        'obj': dut02,
        'lag_links': {link_name: dut02.linkPortMapping
                      [link_name] for link_name in lagLinks},
        'wrkston_link': {wrkston02Link: dut02.linkPortMapping[wrkston02Link]}
    }
    wrkston01Info = {
        'obj': wrkston01,
        'wrkston_link': {wrkston01Link:
                         wrkston01.linkPortMapping[wrkston01Link]},
        'wrkston_ip': wrkston01IP, 'original_ip': wrkston01IP,
        'lag_links': {}
    }
    wrkston01Info['original_macaddr'] = devicesGetActiveMacAddresses(
        [wrkston01Info])[0]
    wrkston02Info = {
        'obj': wrkston02,
        'wrkston_link': {wrkston02Link:
                         wrkston02.linkPortMapping[wrkston02Link]},
        'wrkston_ip': wrkston02IP, 'original_ip': wrkston02IP,
        'lag_links': {}
    }
    wrkston02Info['original_macaddr'] = devicesGetActiveMacAddresses(
        [wrkston02Info])[0]

    wrkstons = [wrkston01Info, wrkston02Info]
    duts = [dut01Info, dut02Info]
    randomUnusedIP = None
    # Modify unicast test if switches are virtual or physical
    unicastTest = None
    virtualTest = True
    if dut01.__class__.__name__ != 'VSwitch':
        unicastTest = lagUnicastTrafficTest
        virtualTest = False
    else:
        unicastTest = lagUnicastTrafficTestVirtual
        virtualTest = True

    LogOutput(
        'debug',
        'Translating interfaces names to perform tcpdump ' +
        'captures on switches')
    for i, dut in enumerate(duts):
        if not swtichGetIntoVtyshOrSwns(dut['obj'], enter=False):
            z = i - 1
            if z >= 0:
                for k in xrange(0, z):
                    swtichGetIntoVtyshOrSwns(duts[k]['obj'])
            return False
        res = switchTcpdumpInterfaces(dut['obj'])
        if not res[0]:
            LogOutput('error', 'Error while obtaining interfaces ' +
                      'information for tcpdump')
            for device in duts:
                swtichGetIntoVtyshOrSwns(device['obj'])
            return False
        dut['tcpdump_links'] = res[1]
    if not macList:
        macList = devicesGetActiveMacAddresses(
            [dut01Info, dut02Info, wrkston01Info, wrkston02Info])
    if not ipAddrList:
        ipAddrList = [wrkston01Info['wrkston_ip'], wrkston02Info[
            'wrkston_ip'], '%s.0' % ipPrefix, '%s.255' % ipPrefix]
    if not (macList or ipAddrList):
        LogOutput(
            'error',
            'Could not obtain information to begin testing flow of ' +
            'traffic inside the LAG')
        return False
    randomUnusedIP = generateIPAddress(ipAddrList, ipPrefix)

    if not virtualTest:
        for i, dut in enumerate(duts):
            if not swtichGetIntoVtyshOrSwns(dut['obj']):
                z = i + 1
                if z < len(duts):
                    for k in xrange(z, len(duts)):
                        swtichGetIntoVtyshOrSwns(duts[k]['obj'])
                return False
    for wrkston, otherWrkston, dut, otherDut in zip(wrkstons,
                                                    reversed(wrkstons),
                                                    duts, reversed(duts)):
        if not virtualTest:
            for i, device in enumerate(duts):
                if not swtichGetIntoVtyshOrSwns(device['obj'], enter=False):
                    z = i - 1
                    if z >= 0:
                        for k in xrange(0, z):
                            swtichGetIntoVtyshOrSwns(duts[k]['obj'])
                    workstationsChangeToNormal(wrkstons)
                    return False
        LogOutput('info', 'Generate broadcast traffic from workstation %s' %
                  str(wrkston['obj'].device))
        if not lagBroadcastTrafficTest(wrkston,
                                       otherWrkston,
                                       dut,
                                       otherDut,
                                       randomUnusedIP):
            for device in duts:
                expecting(device['obj'].expectHndl, 'exit')
                device['obj'].deviceContext = 'linux'
            workstationsChangeToNormal(wrkstons)
            return False
        if not virtualTest:
            for device in duts:
                if not swtichGetIntoVtyshOrSwns(device['obj']):
                    z = i + 1
                    if z < len(duts):
                        for k in xrange(z, len(duts)):
                            swtichGetIntoVtyshOrSwns(duts[k]['obj'])
                    workstationsChangeToNormal(wrkstons)
                    return False
        LogOutput('info', 'Generate unicast traffic from workstation %s' %
                  str(wrkston['obj'].device))
        if not unicastTest(wrkston01Info,
                           wrkston02Info,
                           dut01Info,
                           dut02Info,
                           macList,
                           ipAddrList,
                           ipPrefix):
            for device in duts:
                device['obj'].VtyshShell(enter=False)
            workstationsChangeToNormal(wrkstons)
            return False

    LogOutput('info', 'Normalizing environment after tests...')
    if virtualTest:
        for i, device in enumerate(duts):
            if not swtichGetIntoVtyshOrSwns(device['obj']):
                z = i + 1
                if z < len(duts):
                    for k in xrange(z, len(duts)):
                        swtichGetIntoVtyshOrSwns(duts[k]['obj'])
                workstationsChangeToNormal(wrkstons)
                return False

    for dut in duts:
        retStruct = dut['obj'].VtyshShell(enter=False)
        if retStruct.returnCode() != 0:
            return False
    workstationsChangeToNormal(wrkstons)
    return True


def lagCheckOwnership(dut, lagId, interfaces, dutCheckNumberMatch=True):
    '''
    Verifies if a group of interfaces are part of a LAG. Optionally the
    function also verify if there are more or less links in the LAG than
    passed as argument

    Args:
        dut (object): Device to test
        lagId (str): Name of LAG as in OVS. Eg: lag1
        interfaces (list[str]): List of interfaces part of the LAG
        dutCheckNumberMatch (bool, optional): When True, the function
            verifies if the number of interfaces is exactly as reported
            by OVS before proceeding to verify if the interfaces themselves
            are indeed part of the LAG. Otherwise the function only verifies
            if the interfaces are part of the LAG

    Returns:
        bool: True if all the interfaces are part of the LAG, False otherwise

    '''
    if not expecting(dut.expectHndl, 'ovs-vsctl get port %s' % lagId +
                     ' interfaces'):
        LogOutput('error', 'Could not get the interfaces in %s' %
                  str(lagIg) + ' on device %s' % dut.device)
        return False

    if re.search(r'no row "%s"' % lagId, dut.expectHndl.before):
        LogOutput('error', '%s does not exist' % lagId)
        return False

    lagUuidInterfaces = re.search(r'\[(.*)\]',
                                  dut.expectHndl.before).group(1)
    lagUuidInterfaces = lagUuidInterfaces.split(', ')

    if (dutCheckNumberMatch and len(lagUuidInterfaces) != len(interfaces)
            and lagUuidInterfaces[0] != ''):
        LogOutput('error', 'The number of interfaces in %s on ' % lagId +
                  'device %s is different from the number of interfaces to' %
                  dut.device + ' evaluate')
        LogOutput('error', 'Expected interfaces: %d' % len(lagUuidInterfaces))
        LogOutput('error', 'Interfaces to evaluate: %d' % len(interfaces))
        return False

    for interface in interfaces:
        if not expecting(dut.expectHndl, 'ovs-vsctl get interface %s' %
                         interface + ' _uuid'):
            LogOutput('error', 'Could not obtain interface %s' % interface +
                      ' information on device %s' % dut.device)
            return False
        interfaceUuid = re.search(
            r'(([a-z0-9]+-?){5})\r', dut.expectHndl.before).group(1)
        if interfaceUuid not in lagUuidInterfaces:
            LogOutput('error', 'Interface %s is not present' % interface +
                      ' on %s on device %s' % (lagId, dut.device))
            return False
    LogOutput('debug', '%d interfaces have been ' % len(interfaces) +
              'accounted for in %s as expected' % lagId)
    return True


def lagCheckLACPStatus(dut01, interfaceLag):

    # Recover LACP information from OVS from specific LAG

    # Variables
    overallBuffer = []
    bufferString = ""
    command = ""
    returnCode = 0

    if dut01 is None:
        LogOutput('error', "Need to pass switch dut01 to this routine")
        returnCls = returnStruct(returnCode=1)
        return returnCls

    # Get into vtyshelll
    returnStructure = dut01.VtyshShell(enter=True)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        LogOutput('error', "Failed to get vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=1, buffer=bufferString)
        return returnCls

    ###########################################################################
    # Exit vtysh context and validate buffer with information
    ###########################################################################

    value = expecting(dut01.expectHndl, 'exit')
    dut01.deviceContext = 'linux'
    overallBuffer.append(dut01.expectHndl.before)
    if not value:
        LogOutput('error', 'Unable to exit vtysh context')
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=1, buffer=bufferString)
        return returnCls

    command = "ovs-vsctl list port " + str(interfaceLag)
    LogOutput('info', "Show LACP status " + command)
    returnDevInt = dut01.DeviceInteract(command=command)
    retCode = returnDevInt['returnCode']
    overallBuffer.append(returnDevInt['buffer'])

    if retCode != 0:
        LogOutput('error', "Failed to get information ." + command)

    ###########################################################################
    # Analyze obtained information
    ###########################################################################

    for curLine in overallBuffer:
        bufferString += str(curLine)
    lacpStatus = dict()
    lacpElements = re.search(
        r'lacp_status\s*:\s*{bond_speed="(\d*)",\s*bond_status=' +
        '(\w*)(,\s*bond_status_reason=".*")?}', bufferString)

    lacpStatus['bond_speed'] = lacpElements.group(1)
    lacpStatus['bond_status'] = lacpElements.group(2)
    if lacpElements.group(3):
        lacpStatus['bond_reason'] = re.search(
            r'="(.*)"', lacpElements.group(3)).group(1)
    else:
        lacpStatus['bond_reason'] = None

    return lacpStatus


def lagCheckLACPInterfaceStatus(dut01, interface):

    # Recover vlan information from running config from specific VLAN
    # Variables
    overallBuffer = []
    bufferString = ""
    command = ""
    returnCode = 0

    if dut01 is None:
        LogOutput('error', "Need to pass switch dut01 to this routine")
        returnCls = returnStruct(returnCode=1)
        return returnCls

    # Get into vtyshelll
    returnStructure = dut01.VtyshShell(enter=True)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        LogOutput('error', "Failed to get vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=1, buffer=bufferString)
        return returnCls

    ###########################################################################
    # Exit vtysh and obtain information
    ###########################################################################
    value = expecting(dut01.expectHndl, 'exit')
    dut01.deviceContext = 'linux'
    overallBuffer.append(dut01.expectHndl.before)
    if not value:
        LogOutput('error', 'Unable to exit vtysh context')
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=1, buffer=bufferString)
        return returnCls

    command = "ovs-vsctl list interface " + str(interface)
    LogOutput('info', "Show LACP status in interface" + command)
    returnDevInt = dut01.DeviceInteract(command=command)
    retCode = returnDevInt['returnCode']
    overallBuffer.append(returnDevInt['buffer'])

    if retCode != 0:
        LogOutput('error', "Failed to get information ." + command)

    ###########################################################################
    # Validate buffer with information
    ###########################################################################

    for curLine in overallBuffer:
        bufferString += str(curLine)

    lacpInterfaceStatus = dict()
    lacpInterfaceElements = re.search(
        r'lacp_current\s*:\s(.*?)\r', bufferString)

    lacpInterfaceStatus['lacp_current'] = lacpInterfaceElements.group(1)

    lacpInterfaceElements = re.search(
        r'actor_key="(\d*)"\s*', bufferString)
    lacpInterfaceStatus['actor_key'] = lacpInterfaceElements.group(1)

    lacpInterfaceElements = re.search(
        r'actor_port_id="(\d*,\d*)"', bufferString)
    lacpInterfaceStatus['actor_port_id'] = lacpInterfaceElements.group(1)

    lacpInterfaceElements = re.search(
        r'actor_state="Activ:(\d*),TmOut:(\d*),Aggr:(\d*),Sync:(\d*),' +
        'Col:(\d*),Dist:(\d*),Def:(\d*),Exp:(\d*)"', bufferString)

    actorFlags = dict()
    actorFlags['Activ'] = lacpInterfaceElements.group(1)
    actorFlags['TmOut'] = lacpInterfaceElements.group(2)
    actorFlags['Aggr'] = lacpInterfaceElements.group(3)
    actorFlags['Sync'] = lacpInterfaceElements.group(4)
    actorFlags['Col'] = lacpInterfaceElements.group(5)
    actorFlags['Dist'] = lacpInterfaceElements.group(6)
    actorFlags['Def'] = lacpInterfaceElements.group(7)
    actorFlags['Exp'] = lacpInterfaceElements.group(8)

    lacpInterfaceStatus['actor_state'] = actorFlags

    lacpInterfaceElements = re.search(
        r'actor_system_id="(\d*,.{2}:.{2}:.{2}:.{2}:.{2}:.{2})"', bufferString)
    lacpInterfaceStatus['actor_system_id'] = lacpInterfaceElements.group(1)

    lacpInterfaceElements = re.search(
        r'partner_key="(\d*)"\s*', bufferString)
    lacpInterfaceStatus['partner_key'] = lacpInterfaceElements.group(1)

    lacpInterfaceElements = re.search(
        r'partner_port_id="(\d*,\d*)"', bufferString)
    lacpInterfaceStatus['partner_port_id'] = lacpInterfaceElements.group(1)

    lacpInterfaceElements = re.search(
        r'partner_state="Activ:(\d*),TmOut:(\d*),Aggr:(\d*),Sync:(\d*),' +
        'Col:(\d*),Dist:(\d*),Def:(\d*),Exp:(\d*)"', bufferString)

    partnerFlags = dict()
    partnerFlags['Activ'] = lacpInterfaceElements.group(1)
    partnerFlags['TmOut'] = lacpInterfaceElements.group(2)
    partnerFlags['Aggr'] = lacpInterfaceElements.group(3)
    partnerFlags['Sync'] = lacpInterfaceElements.group(4)
    partnerFlags['Col'] = lacpInterfaceElements.group(5)
    partnerFlags['Dist'] = lacpInterfaceElements.group(6)
    partnerFlags['Def'] = lacpInterfaceElements.group(7)
    partnerFlags['Exp'] = lacpInterfaceElements.group(8)

    lacpInterfaceStatus['partner_state'] = partnerFlags

    lacpInterfaceElements = re.search(
        r'partner_system_id="(\d*,.{2}:.{2}:.{2}:.{2}:.{2}:.{2})"',
        bufferString)
    lacpInterfaceStatus['partner_system_id'] = lacpInterfaceElements.group(1)

    return lacpInterfaceStatus


# Verify LACP status & flagging


def lagVerifyLACPStatusAndFlags(dut01,
                                dut02,
                                lacpActive,
                                lagLinks,
                                lag01,
                                lag02,
                                status='ok',
                                dut01Flags={'Activ': '1',
                                            'TmOut': '1',
                                            'Aggr': '1',
                                            'Sync': '1',
                                            'Col': '1',
                                            'Dist': '1',
                                            'Def': '0',
                                            'Exp': '0'},
                                dut02Flags={'Activ': '1',
                                            'TmOut': '1',
                                            'Aggr': '1',
                                            'Sync': '1',
                                            'Col': '1',
                                            'Dist': '1',
                                            'Def': '0',
                                            'Exp': '0'},
                                dut01LnksKeys=None, dut02LnksKeys=None,
                                dut01PortIds=None, dut02PortIds=None,
                                dut01LnkPriorities=None,
                                dut02LnkPriorities=None,
                                dut01LACPCurrentVals=None,
                                dut02LACPCurrentVals=None,
                                dut01LnkCheckNumberMatch=True,
                                dut02LnkCheckNumberMatch=True):
    '''
    Validates the LACP configuration is established on both ends of a LAG

    Args:
        dut01 (object): First member of LAG
        dut02 (object): Second member of LAG
        lacpActive (bool): Flag indicating if LAG is using LACP or not
        lagLinks (list[str]): List of links in the topology which are part
            of the LAG
        lag01 (str): Name of LAG in first switch
        lag02 (str): Name of LAG in second switch
        status (str, optional): Expected status of LAG in both switches
            Default: ok
        dut01Flags (ditc[str]): Dictionary containing the LACP flags which
            are expected the first switch to be advertising to its partner
        dut02Flags (ditc[str]): Dictionary containing the LACP flags which
            are expected the second switch to be advertising to its partner
        dut01LnksKeys (list[str]): List of keys the ports members of a LAG
            are expected to have. There should be 1 per port in LAG. If a
            value in the list is None, the key 1 is utilized
            Default: None
        dut02LnksKeys (list[str], optional): List of keys the ports members
            of a LAG are expected to have. There should be 1 per port in
            LAG. If a value in the list is None, the key 1 is utilized
            Default: None
        dut01PortIds (list[str], optional): List of port IDs used by the ports
            members of the LAG. There should be 1 per port in LAG. If a value
            in the list is None, it is not checked
            Default: None
        dut02PortIds (list[str], optional): List of port IDs used by the ports
            members of the LAG. There should be 1 per port in LAG. If a value
            in the list is None, it is not checked
            Default: None
        dut01LnkPriorities (list[str], optional): List of port priorities used
            by members of LAG. There should be 1 per port in LAG. If a value
            in the list is None, the priority by default is 1
            Default: None
        dut01LnkPriorities (list[str], optional): List of port priorities used
            by members of LAG. There should be 1 per port in LAG. If a value
            in the list is None, the priority by default is 1
            Default: None
        dut01LACPCurrentVals (list[str], optional): List of current status of
            LACP on each interface. There should be 1 per port in LAG. If a
            value in the list is None, the default value is true
            Default: None
        dut02LACPCurrentVals (list[str], optional): List of current status of
            LACP on each interface. There should be 1 per port in LAG. If a
            value in the list is None, the default value is true
            Default: None
        dut01LnkCheckNumberMatch (bool, optional): If True, the function will
            check if the number of links inserted into the function for dut01
            is the total number configured on the LAG. Otherwise, the function
            will only check if the links passed are part of the LAG
        dut02LnkCheckNumberMatch (bool, optional): If True, the function will
            check if the number of links inserted into the function for dut02
            is the total number configured on the LAG. Otherwise, the function
            will only check if the links passed are part of the LAG

        Returns:
            bool: True if information matches, False otherwise
    '''
    # variable initialization
    dut01LACPStatus = {}
    dut02LACPStatus = {}
    dut01LACPInterfacesStatus = []
    dut02LACPInterfacesStatus = []
    duts = [{'dut': dut01, 'lag': lag01, 'lacp_status': dut01LACPStatus,
             'lacp_interfaces': dut01LACPInterfacesStatus,
             'flags': dut01Flags, 'keys': dut01LnksKeys, 'ids': dut01PortIds,
             'priorities': dut01LnkPriorities,
             'lacp_currents': dut01LACPCurrentVals,
             'check_lnk_numbers': dut01LnkCheckNumberMatch},
            {'dut': dut02, 'lag': lag02, 'lacp_status': dut02LACPStatus,
             'lacp_interfaces': dut02LACPInterfacesStatus,
             'flags': dut02Flags, 'keys': dut02LnksKeys, 'ids': dut02PortIds,
             'priorities': dut02LnkPriorities,
             'lacp_currents': dut02LACPCurrentVals,
             'check_lnk_numbers': dut02LnkCheckNumberMatch}]

    '''
    Attempt to retrieve LACP information
    It should fail when LACP is disabled and succeed otherwise
    '''

    LogOutput('info', 'Verify ownership of LAGs on interfaces')
    for dut in duts:
        LogOutput('info', 'Device: %s....' % dut['dut'].device)
        interfaces = [dut['dut'].linkPortMapping[interface] for interface
                      in lagLinks]
        if not lagCheckOwnership(dut['dut'], dut['lag'], interfaces,
                                 dutCheckNumberMatch=dut['check_lnk_numbers']):
            return False
    LogOutput('info', 'All member interfaces correctly accounted')
    LogOutput(
        'info', 'Attempt to retrieve LACP information for all switches ' +
        'interfaces')
    for dut in duts:
        LogOutput('info', 'Device: %s....' % dut['dut'].device)
        try:
            dut['lacp_status'] = lagCheckLACPStatus(dut['dut'], dut['lag'])
            if not lacpActive:
                LogOutput('error', 'LACP status information detected on ' +
                          'device %s with LACP disabled' % dut['dut'].device)
                return False
        except AttributeError as e:
            # Validation in case the LAG has no interfaces yet
            if len(lagLinks) == 0:
                dut['lacp_status'] = None
                LogOutput('debug', 'No links are present yes on %s and it ' %
                          dut['lag'] + 'is not possible to get its ' +
                          'information even if it is dynamic or static')
                continue
            # Normal validation
            if lacpActive:
                LogOutput('error', 'Could not verify LACP status for LAG' +
                          ' %s in device %s' %
                          (dut['lag'], dut['dut'].device))
                LogOutput('debug', 'Exception: %s' % str(e))
                return False
        for lagLink in lagLinks:
            try:
                stat = lagCheckLACPInterfaceStatus(dut['dut'],
                                                   dut['dut'].linkPortMapping
                                                   [lagLink])
                if not lacpActive:
                    LogOutput('error', 'Obtained LACP status on interface ' +
                              '%s from device %s when LACP is disabled' %
                              (dut['dut'].linkPortMapping[lagLink],
                               dut['dut'].device))
                    return False
                dut['lacp_interfaces'].append(stat)
            except AttributeError as e:
                if lacpActive:
                    LogOutput('error', 'Could not verify LACP interface ' +
                              'status for LAG %s interface %s in device %s' %
                              (dut['lag'],
                               dut['dut'].linkPortMapping[lagLink],
                               dut['dut'].device))
                    LogOutput('debug', 'Exception: %s' % str(e))
                    return False

# If LACP is not active and we got here, there is nothing else to do
    if not lacpActive:
        LogOutput('info', 'No LACP information obtained as expected from' +
                  ' static LAGs')
        return True

# Validate LACP is up and information is consistent between partners

    LogOutput('info', 'Analyze obtained LACP information')
    for i, dut in enumerate(duts, 0):
        LogOutput('info', 'Device: %s....' % dut['dut'].device)
        # Validate LAG LACP status
        if dut['lacp_status'] and dut['lacp_status']['bond_status'] != status:
            LogOutput('error', 'Unexpected LACP status for device ' +
                      '%s: %s' % (dut['dut'].device,
                                  dut['lacp_status']['bond_status']))
            LogOutput('error', 'Expected: %s' % status)
            return False
# If there are no interfaces on LAG, there is nothing to gain
# past this point
        if len(lagLinks) == 0:
            continue
        if i == 0:
            otherDut = duts[1]
        else:
            otherDut = duts[0]

# Get current system-id
        retStruct = lagpGlobalSystemShow(deviceObj=dut['dut'])
        if retStruct.returnCode() != 0:
            LogOutput('error', 'Could not obtain system-id for ' +
                      'verification on device %s' % dut['dut'].device)
            return False

        expectedSystemId = retStruct.valueGet()
        expectedSystemId['System-id'] = expectedSystemId['System-id'].lower()

        # Validate LACP information

        for k, (ints1, ints2) in enumerate(zip(dut['lacp_interfaces'],
                                               otherDut['lacp_interfaces']),
                                           0):
            # Validate system id locally
            id = re.search(
                r'\d+,(([0-9a-fA-F]{1,2}:?){6})',
                ints1['actor_system_id']).group(1)
            if (id != expectedSystemId['System-id']):
                LogOutput('error', 'System-id of device does not match ' +
                          'expected value')
                LogOutput('error', 'Expected: %s' %
                          expectedSystemId['System-id'])
                LogOutput('error', 'Actual: %s' % ints1['actor_system_id'])
                return False

            # Validate system id is correctly sent
            id2 = re.search(
                r'\d+,(([0-9a-fA-F]{1,2}:?){6})',
                ints2['partner_system_id']).group(1)
            if id != id2:
                LogOutput('error', 'Actor system-id does not match value sent')
                LogOutput('error', 'Device: %s' % dut['dut'].device)
                LogOutput('error', 'System-id: %s' % id)
                LogOutput('error', 'System-id sent: %s' % id2)
                return False

            # Validate system priority locally
            id = re.search(
                r'(\d+),([0-9a-fA-F]{1,2}:?){6}',
                ints1['actor_system_id']).group(1)
            if (id != str(expectedSystemId['System-priority'])):
                LogOutput('error', 'System-priority of device does not ' +
                          'match expected value')
                LogOutput('error', 'Expected: %s' %
                          str(expectedSystemId['System-priority']))
                LogOutput('error', 'Actual: %s' % ints1['actor_system_id'])
                return False

            # Validate system priority is correctly sent
            id2 = re.search(
                r'(\d+),([0-9a-fA-F]{1,2}:?){6}',
                ints2['partner_system_id']).group(1)
            if id != id2:
                LogOutput(
                    'error', 'Actor system-priority does not match ' +
                    'value sent')
                LogOutput('error', 'Device: %s' % dut['dut'].device)
                LogOutput('error', 'System-priority: %s' % id)
                LogOutput('error', 'System-priority sent: %s' % id2)
                return False

            # Validate locally the port-id

            id = re.search(r'\d+,(\d+)', ints1['actor_port_id']).group(1)
            if dut['ids'] and dut['ids'][k]:
                expected = dut['ids'][k]
            else:
                expected = id

            if expected != id:
                LogOutput('error', 'Actor port id on device ' +
                          '%s does not match expected' %
                          dut['dut'].device)
                LogOutput('error', 'Expected: %s' % expected)
                LogOutput('error', 'Actual: %s' % id)
                return False

            # Validate the port-id is passed to other device
            id2 = re.search(r'\d+,(\d+)', ints2['partner_port_id']).group(1)
            if id != id2:
                LogOutput('error', 'Actor port-id does not match value sent')
                LogOutput('error', 'Device: %s' % dut['dut'].device)
                LogOutput('error', 'Port-id: %s' % id)
                LogOutput('error', 'Port-id sent: %s' % id2)
                return False

            # Validate locally the port priority
            if dut['priorities'] and dut['priorities'][k]:
                expected = dut['priorities'][k]
            else:
                expected = 1

            priority = re.search(r'(\d+),\d+',
                                 ints1['actor_port_id']).group(1)
            if str(expected) != priority:
                LogOutput('error', 'Actor port priority on device ' +
                          '%s does not match expected' % dut['dut'].device)
                LogOutput('error', 'Expected: %s' % expected)
                LogOutput('error', 'Actual: %s' % priority)
                return False

            # Validate the port-priority is passed to other device
            priority2 = re.search(
                r'(\d+),\d+', ints2['partner_port_id']).group(1)
            if priority != priority2:
                LogOutput('error', 'Actor port-priority does not match ' +
                          'value sent')
                LogOutput('error', 'Device: %s' % dut['dut'].device)
                LogOutput('error', 'Port-priority: %s' % priority)
                LogOutput('error', 'Port-priority sent: %s' % priority2)
                return False

            # Validate locally the key
            if dut['keys'] and dut['keys'][k]:
                expected = dut['keys'][k]
            else:
                expected = 1

            if str(expected) != ints1['actor_key']:
                LogOutput('error', 'Actor key on device ' +
                          '%s does not match expected' % dut['dut'].device)
                LogOutput('error', 'Expected: %s' % expected)
                LogOutput('error', 'Actual: %s' % ints1['actor_key'])
                return False

            # Validate the key is passed to other device
            if ints1['actor_key'] != ints2['partner_key']:
                LogOutput('error', 'Actor key does not match ' +
                          'value sent')
                LogOutput('error', 'Device: %s' % dut['dut'].device)
                LogOutput('error', 'Key: %s' % ints1['actor_key'])
                LogOutput('error', 'Key sent: %s' % ints2['partner_key'])
                return False

            # Validate locally the lacp_current flag
            if dut['lacp_currents'] and dut['lacp_currents'][k]:
                expected = dut['lacp_currents'][k]
            else:
                expected = 'true'

            if expected != ints1['lacp_current']:
                LogOutput('error', 'Actor lacp_current flag on device ' +
                          '%s does not match expected' % dut['dut'].device)
                LogOutput('error', 'Expected: %s' % expected)
                LogOutput('error', 'Actual: %s' % ints1['lacp_current'])
                return False

            # Validate LACP interface status flags
            for key in ints1['actor_state']:
                if ints1['actor_state'][key] != dut['flags'][key]:
                    LogOutput('error', 'Unexpected LACP flag information')
                    LogOutput('error', 'Flag: %s' % key)
                    LogOutput('error', 'Device: %s' % dut['dut'].device)
                    LogOutput('error', 'Local status: %s' %
                              ints1['actor_state'][key])
                    LogOutput('error', 'Expected local status: %s' %
                              dut['flags'][key])
                    return False
                if ints1['actor_state'][key] != ints2['partner_state'][key]:
                    LogOutput('error', 'Difference in LACP information ' +
                              'betweeen partners')
                    LogOutput('error', 'Flag: %s' % key)
                    LogOutput('error', 'Device: %s' % dut['dut'].device)
                    LogOutput('error', 'Partner device: %s' %
                              otherDut['dut'].device)
                    LogOutput('error', 'Local status: %s' %
                              ints1['actor_state'][key])
                    LogOutput('error', 'Partner status: %s' %
                              ints2['partner_state'][key])
                    return False
    LogOutput('info', 'Finished analyzing LACP information with no ' +
              'unexpected results')
    return True


def lagVerifyConfig(
        deviceObj,
        lagId,
        interfaces=[],
        lacpMode='off',
        fallbackFlag=False,
        hashType='l3-src-dst',
        lacpFastFlag=False):
    '''
    Parse a LAG for configuration settings

    Args:
        deviceObj (PSwitch,VSwitch): Device from which configuration is
            verified
        lagId (str): LAG identifier
        interfaces (list[str], optional): A list of interfaces to
            verify if present (default: empty list)
        lacpMode (str, optional): LACP mode (default: off)
        fallbackFlag (bool, optional): Status of fallback flag
            (default: False)
        hashType (str, optional): Hashing algorithm employed
            (default: l3-src-dst)
        lacpFastFlag (bool, optional): Flag indicating if LAG uses fast
            heartbeat (detault: False)

    Returns:
        bool: True if configuration matches, False otherwise
    '''
    if not deviceObj or not lagId:
        LogOutput('error', "The device and LAG ID must be specified")
        return False
    LogOutput('debug', "Verifying LAG %s configuration..." % str(lagId))
    # Working code, comenting until LACP heartbeat rate is fixed on CLI
#     retStruct = lacpAggregatesShow(deviceObj=deviceObj, lagId=lagId)
#     if retStruct.returnCode() != 0:
#         return False
#     baseLag = {
#         "interfaces": interfaces,
#         "lacpMode": lacpMode,
#         "fallbackFlag": fallbackFlag,
#         "hashType": hashType,
#         "lacpFastFlag": lacpFastFlag}
#     for key in baseLag:
#         LogOutput('debug', "Verifying attribute %s..." % key)
#         if isinstance(baseLag[key], list):
#             for i in baseLag[key]:
#                 if i not in retStruct.valueGet(key=lagId)[key]:
#                     LogOutput(
#                         'error',
#                         "Interface %s was not found in LAG %s" %
#                         (str(i), str(lagId)))
#                     return False
#             continue
#         if baseLag[key] != retStruct.valueGet(key=lagId)[key]:
#             LogOutput(
#                 'error',
#                 "Failure verifying LAG %s configuration " % str(lagId) +
#                 "configuration on attribute %s" % key)
#             LogOutput(
#                 'error',
#                 "Found: %s - Expected: %s" %
#                 (str(retStruct.valueGet(key=lagId)[key]), str(baseLag[key])))
#             return False
#         LogOutput('debug', "Passed")

    '''
    Start of temporary code to verify LAG configuration
    '''

    baseLag = {
        "interfaces": interfaces,
        "lacpMode": lacpMode,
        "fallbackFlag": fallbackFlag,
        "hashType": hashType,
        "lacpFastFlag": lacpFastFlag}
    otherConfigAttributes = {'lacp-fallback-ab': {'attr': 'fallbackFlag',
                                                  'value': False,
                                                  'meanings': {'true': True,
                                                               'false': False}
                                                  },
                             'bond_mode': {'attr': 'hashType', 'value':
                                           'l3-src-dst', 'meanings': None},
                             'lacp-time': {'attr': 'lacpFastFlag', 'value':
                                           True, 'meanings': {'fast': True,
                                                              'slow': False}}}

    # Get into vtyshelll
    returnStructure = deviceObj.VtyshShell(enter=True)
    returnCode = returnStructure.returnCode()
    if returnCode != 0:
        LogOutput('error', "Failed to get vtysh prompt")
        return False
    value = expecting(deviceObj.expectHndl, 'exit')
    deviceObj.deviceContext = 'linux'
    if not value:
        LogOutput('error', 'Unable to exit vtysh context')
        return False
    # Get information
    command = 'ovs-vsctl list port lag%s' % str(lagId)
    if not expecting(deviceObj.expectHndl, command):
        LogOutput('error', 'Unable to retrieve LAG %s information' %
                  str(lagId))
        return False

    # Name
    res = re.findall(r'name\s+?: "(lag%s+?)"' % str(lagId),
                     deviceObj.expectHndl.before)
    if len(res) == 0:
        LogOutput('error', 'Could not retrieve LAG %s information' %
                  str(lagId))
        return False
    # lacpMode
    res = re.findall(r'lacp\s+?: (active|passive|off|\[\])',
                     deviceObj.expectHndl.before)
    if len(res) == 0:
        LogOutput('error', 'Could not retrieve LACP mode')
        return False
    if res[0] == '[]':
        res[0] = 'off'
    if res[0] != baseLag['lacpMode']:
        LogOutput(
            'error',
            "Failure verifying LAG %s configuration " % str(lagId) +
            "configuration on attribute lacpMode")
        LogOutput(
            'error', "Found: %s - Expected: %s" %
            (res[0], baseLag['lacpMode']))
        return False

# Other attributes except interfaces
    res = re.findall(r'other_config\s+: {(.*?)}', deviceObj.expectHndl.before)
    if len(res) == 0:
        LogOutput('error', 'Could not retrieve fallback, hash and rate')
        return False
    if res[0] != '':
        text = re.sub(r'"', '', res[0])
        textList = text.split(', ')
        for element in textList:
            values = element.split('=')
            if otherConfigAttributes[values[0]]['meanings']:
                otherConfigAttributes[values[0]]['value'] =\
                    otherConfigAttributes[values[0]]['meanings'][values[1]]
            else:
                otherConfigAttributes[values[0]]['value'] = values[1]
    for key in otherConfigAttributes:
        if baseLag[otherConfigAttributes[key]['attr']] !=\
                otherConfigAttributes[key]['value']:
            LogOutput(
                'error',
                "Failure verifying LAG %s configuration " % str(lagId) +
                "configuration on attribute %s" %
                otherConfigAttributes[key]['attr'])
            LogOutput(
                'error', "Found: %s - Expected: %s" %
                (otherConfigAttributes[key]['value'],
                 str(baseLag[otherConfigAttributes[key]['attr']])))
            return False
# Interfaces
    if not lagCheckOwnership(deviceObj, 'lag%s' % str(lagId), interfaces):
        return False

    '''
    End of temporary code
    '''

    LogOutput(
        'info',
        "Verification of LAG %s configuration passed" % str(lagId))
    return True

# Parses the output of "show run" and verify that the config is empty.
# Returns True if the configuration is empty, False otherwise


def validateEmptyConfig(devices):
    for dev in devices:
        output = showRun(deviceObj=dev).buffer()
        ret_expression = re.search(
            r'Current configuration:\s*!\s*!\s*!\s*(.*)\s*exit',
            output,
            re.DOTALL
        )
        if ret_expression.group(1) != "":
            return False
    return True

# Reboots switch


def switchReboot(deviceObj):
    if not validateEmptyConfig([deviceObj]):
        # Reboot switch
        LogOutput('info', "Reboot switch " + deviceObj.device)
        deviceObj.Reboot()
    if not validateEmptyConfig([deviceObj]):
        return False
    return True


def interfaceEnableRouting(deviceObj, int, enable):
    # Enable/disable routing on interfaces so VLANs can be configured
    overallBuffer = []
    returnStructure = deviceObj.VtyshShell(enter=True)
    overallBuffer.append(returnStructure.buffer())
    returnCode = returnStructure.returnCode()
    if returnCode != 0:
        LogOutput('error', "Failed to get vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls

    # Get into config context
    returnStructure = deviceObj.ConfigVtyShell(enter=True)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        LogOutput('error', "Failed to get vtysh config prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls
    # enter interface
    command = "interface %s\r" % str(int)
    returnDevInt = deviceObj.DeviceInteract(command=command)
    retCode = returnDevInt['returnCode']
    overallBuffer.append(returnDevInt['buffer'])
    if retCode != 0:
        LogOutput('error', "Failed to configure interface " +
                  str(int) + " on device " + deviceObj.device)
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
        return returnCls
    else:
        LogOutput('debug', "Entered interface " +
                  str(int) + " on device " + deviceObj.device)
    if enable:
        # configure interface
        command = "routing"
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to enable routing on interface " +
                      str(int) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput('info', "Enabled routing on interface " +
                      str(int) + " on device " + deviceObj.device)
    else:
        # configure interface
        command = "no routing"
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to disable routing on interface " +
                      str(int) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput('info', "Disabled routing on interface " +
                      str(int) + " on device " + deviceObj.device)
        # exit
    command = "exit"
    returnDevInt = deviceObj.DeviceInteract(command=command)
    retCode = returnDevInt['returnCode']
    overallBuffer.append(returnDevInt['buffer'])
    if retCode != 0:
        LogOutput('error', "Failed to exit configure interface " +
                  str(int) + " on device " + deviceObj.device)
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
        return returnCls
    else:
        LogOutput('debug', "Exited configure interface " +
                  str(int) + " on device " + deviceObj.device)
    # Get out of config context
    returnStructure = deviceObj.ConfigVtyShell(enter=False)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        LogOutput('error', "Failed to exit vtysh config prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls
    # Get out of vtysh
    returnStructure = deviceObj.VtyshShell(enter=False)
    overallBuffer.append(returnStructure.buffer())
    returnCode = returnStructure.returnCode()
    if returnCode != 0:
        LogOutput('error', "Failed to exit vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls
    # Return
    bufferString = ""
    for curLine in overallBuffer:
        bufferString += str(curLine)
    returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
    return returnCls

# Enable/disable interface on DUT


def interfaceGetStatus(dev, interface):
    # Gets the status of a switch interface
    output = showInterface(deviceObj=dev, interface=interface).buffer()
    ret_expression = re.search(
        r'Interface [\d-]+? is (down|up)',
        output
    )
    if ret_expression.group(1) == "up":
        LogOutput('info',"Interface %s is up" % str(interface))
        return True
    LogOutput('info',"Interface %s is down" % str(interface))
    return False


def switchEnableInterface(deviceObj, int, enable):
    # Enables/disables a switch interface and verifies if correctly configured
    if enable:
        retStruct = InterfaceEnable(
            deviceObj=deviceObj, enable=enable, interface=int)
        if not retStruct.returnCode() == 0:
            LogOutput(
                'error', "Failed to enable " + deviceObj.device +
                " interface " + int)
            return False
        else:
            LogOutput(
                'info', "Enabled " + deviceObj.device + " interface " + int)
    else:
        retStruct = InterfaceEnable(
            deviceObj=deviceObj, enable=enable, interface=int)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed to disable " + deviceObj.device +
                " interface " + int)
            return False
        else:
            LogOutput(
                'info', "Disabled " + deviceObj.device + " interface " + int)

    return True


def lagAddInterfaces(deviceObj, lagId, intArray):
    # Adds interfaces to LAG
    overallBuffer = []
    returnStructure = deviceObj.VtyshShell(enter=True)
    overallBuffer.append(returnStructure.buffer())
    returnCode = returnStructure.returnCode()
    if returnCode != 0:
        LogOutput('error', "Failed to get vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls

    # Get into config context
    returnStructure = deviceObj.ConfigVtyShell(enter=True)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        LogOutput('error', "Failed to get vtysh config prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls

    # Add interfaces
    for i in intArray:
        command = "interface %s\r" % str(i)
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to configure interface " +
                      str(i) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput(
                'debug', "Entered interface " + str(i) + " on device " +
                deviceObj.device)

        command = "lag %s" % str(lagId)
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to add interface " + str(i) +
                      " to LAG" + str(lagId) + " on device " +
                      deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode,
                                     buffer=bufferString)
            return returnCls
        else:
            LogOutput('info', "Added interface " + str(i) +
                      " to LAG" + str(lagId) + " on device " +
                      deviceObj.device)

        command = "exit"
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to exit configuration of interface " +
                      str(i) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput('debug', "Exited configuration of interface " +
                      str(i) + " on device " + deviceObj.device)

    # Get out of config context
    returnStructure = deviceObj.ConfigVtyShell(enter=False)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        LogOutput('error', "Failed to exit vtysh config prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls
    # Exit vtysh
    returnStructure = deviceObj.VtyshShell(enter=False)
    overallBuffer.append(returnStructure.buffer())
    returnCode = returnStructure.returnCode()
    if returnCode != 0:
        LogOutput('error', "Failed to exit vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls
    bufferString = ""
    for curLine in overallBuffer:
        bufferString += str(curLine)
    returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
    return returnCls


def lagCreate(deviceObj, lagId, configure, intArray, mode):
    # Creates LAG and adds interfaces
    if configure:
        retStruct = lagCreation(
            deviceObj=deviceObj, lagId=str(lagId), configFlag=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to create LAG1 on " + deviceObj.device)
            return False
        else:
            LogOutput(
                'info', "Created LAG" + str(lagId) + " on " +
                deviceObj.device)
        retStruct = lagAddInterfaces(deviceObj, lagId, intArray)
        if retStruct.returnCode() != 0:
            return False
        if mode != 'off':
            retStruct = lagMode(
                lagId=str(lagId), deviceObj=deviceObj, lacpMode=mode)
            if retStruct.returnCode() != 0:
                return False
        if not lagVerifyConfig(deviceObj, lagId, intArray, mode):
            LogOutput('error',
                      'Failed to create a LAG with intended configuration')
            return False

    else:
        retStruct = lagCreation(
            deviceObj=deviceObj, lagId=str(lagId), configFlag=False)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to delete LAG1 on " + deviceObj.device)
            return False
        else:
            LogOutput(
                'info', "Deleted LAG" + str(lagId) + " on " + deviceObj.device)
        retStruct = lacpAggregatesShow(deviceObj=deviceObj)
        if len(retStruct.dataKeys()) != 0:
            if retStruct.valueGet(key=str(lagId)) is not None:
                LogOutput(
                    'error', "The LAG was not deleted from configuration")
                return False
    return True

# Add VLAN to interface


def vlanVerifyPorts(dut, vlanID, port):
    # Verify if port is part of a VLAN
    assigned = False
    helper = re.search('lag ', port)
    if helper:
        port = port.replace(' ', '')
    returnCLS = ShowVlan(deviceObj=dut)
    output = returnCLS.buffer()
    output = re.search(r'\r\n(%d .+?)\r' % vlanID, output)
    if not output:
        LogOutput('error', 'Could not find VLAN %d to which ' % vlanID +
                  'ports could be assigned')
        return False
    output = output.group(1)
    helper = ''
    helperList = []
    count = 0
    foundLetter = False
    for i in xrange(len(output) - 1, 0, -1):
        if not foundLetter:
            if output[i] != ' ':
                foundLetter = True
                continue
        else:
            if output[i] == ' ':
                count += 1
                if count > 1:
                    helper = output[i + 2:]
                    helperList = helper.split(', ')
                    break
            else:
                count = 0
    if port in helperList:
        assigned = True
        LogOutput('info', 'Found interface %s in VLAN %d' %
                  (port, vlanID))
    else:
        LogOutput('error', 'Could not find interface %s in VLAN %d' %
                  (port, vlanID))
    return assigned


def vlanAddInterface(deviceObj, vlanId, enable, int):
    # Verify a port has been assigned to a vlan

    if enable:
        retStruct = interfaceEnableRouting(deviceObj, int, False)
        if retStruct.returnCode() != 0:
            return False
        retStruct = AddPortToVlan(deviceObj=deviceObj, vlanId=vlanId,
                                  interface=int, access=True)
        if not (retStruct.returnCode() == 0 and
                vlanVerifyPorts(deviceObj, vlanId, int)):
            LogOutput(
                'error', "Failed to add VLAN " + str(vlanId) +
                " to interface " + int)
            return False
        else:
            LogOutput('info', "Added VLAN " + str(vlanId) +
                      " to interface " + int)
    else:
        retStruct = AddPortToVlan(deviceObj=deviceObj, vlanId=vlanId,
                                  interface=int, config=False, access=True)

        if not (retStruct.returnCode() == 0 and
                not vlanVerifyPorts(deviceObj, vlanId, int)):
            LogOutput(
                'error', "Failed to delete VLAN " + str(vlanId) +
                " to interface " + int)
            return False
        else:
            LogOutput('info', "Delete VLAN " + str(vlanId) +
                      " to interface " + int)
        retStruct = interfaceEnableRouting(deviceObj, int, True)
        if retStruct.returnCode() != 0:
            return False
    return True


def vlanVerify(dut, pVlan):
    ''' Verify a vlan exist on VLAN table.

    Args:
         dut (obj) : device under test
         pVlan (str) : vlan name to verify

    '''
    LogOutput('info', "Validating VLAN")
    cont = 0
    devRetStruct = ShowVlan(deviceObj=dut)
    returnData = devRetStruct.buffer()
    vlans = re.findall('[vV][lL][aA][nN]([0-9]+)\s', returnData)
    for vlan in vlans:
        if vlan == str(pVlan):
            cont = cont + 1
    if cont == 1:
        return 0
    else:
        return 1


def vlanConfigure(deviceObj, vlanId, enable):
    # Configure/delete VLAN on switch

    if enable:
        LogOutput('debug', "Configuring VLAN " + str(vlanId) +
                  " on device " + deviceObj.device)
        retStruct = AddVlan(deviceObj=deviceObj, vlanId=vlanId)
        if retStruct.returnCode() != 0 or vlanVerify(deviceObj, vlanId) != 0:
            LogOutput('error', "Failed to create VLAN " +
                      str(vlanId) + " on device " + deviceObj.device)
            return False
        else:
            LogOutput(
                'info', "Created VLAN " + str(vlanId) + " on device " +
                deviceObj.device)
        retStruct = VlanStatus(deviceObj=deviceObj, vlanId=vlanId,
                               status=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to enable VLAN " +
                      str(vlanId) + " on device " + deviceObj.device)
            return False
        else:
            LogOutput(
                'info', "Enabled VLAN " + str(vlanId) + " on device " +
                deviceObj.device)
    else:
        LogOutput('debug', "Deleting VLAN " + str(vlanId) +
                  " on device " + deviceObj.device)
        retStruct = AddVlan(deviceObj=deviceObj, vlanId=vlanId,
                            config=False)
        if retStruct.returnCode() != 0 or vlanVerify(deviceObj, vlanId) != 1:
            LogOutput('error', "Failed to delete VLAN " +
                      str(vlanId) + " on device " + deviceObj.device)
            return False
        else:
            LogOutput(
                'info', "Deleted VLAN " + str(vlanId) + " on device " +
                deviceObj.device)
    return True


def workstationConfigure(deviceObj, int, ipAddr, netMask, broadcast, enable):
    # Configure/unconfigure the IP address of a workstation
    if enable:
        retStruct = deviceObj.NetworkConfig(ipAddr=ipAddr,
                                            netMask=netMask,
                                            broadcast=broadcast,
                                            interface=int, configFlag=True)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed to configure IP on workstation " +
                deviceObj.device)
            return False
        cmdOut = deviceObj.cmd("ifconfig " + int)
        LogOutput('info', "Ifconfig info for workstation " +
                  deviceObj.device + ":\n" + cmdOut)
    else:
        retStruct = deviceObj.NetworkConfig(ipAddr=ipAddr,
                                            netMask=netMask,
                                            broadcast=broadcast,
                                            interface=int, configFlag=False)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed to unconfigure IP on workstation " +
                deviceObj.device)
            return False
        cmdOut = deviceObj.cmd("ifconfig " + int)
        LogOutput('info', "Ifconfig info for workstation " +
                  deviceObj.device + ":\n" + cmdOut)
    return True


def workstationsPing(deviceObj1, deviceObj2, ipAddr, success):
    # Ping between workstations
    LogOutput('info', "Pinging between workstation " +
              deviceObj1.device + " and workstation " + deviceObj2.device)
    if success:
        LogOutput('info', 'Ping expected to succeed: Yes')
    else:
        LogOutput('info', 'Ping expected to succeed: No')
    retStruct = deviceObj1.Ping(ipAddr=ipAddr)
    if success:
        if retStruct.returnCode() != 0:
            LogOutput('error', 'Failure!: Failed to ping from workstation %s' %
                      deviceObj1.device + ' to workstation %s' %
                      deviceObj2.device)
            LogOutput('debug', "Debug information:\n%s" %
                      str(retStruct.retValueString()))
            return False
        else:
            LogOutput('info', 'Success!: Ping was successful')
            LogOutput('debug', "IPv4 Ping from workstation 1 to workstation 2 \
            return JSON:\n" +
                      str(retStruct.retValueString()))
            packet_loss = retStruct.valueGet(key='packet_loss')
            packets_sent = retStruct.valueGet(key='packets_transmitted')
            packets_received = retStruct.valueGet(key='packets_received')
            LogOutput('debug', "Packets Sent:\t" + str(packets_sent))
            LogOutput('debug', "Packets Recv:\t" + str(packets_received))
            LogOutput('debug', "Packet Loss %:\t" + str(packet_loss))
            LogOutput('debug', "Passed ping test between workstation " +
                      deviceObj1.device + " and workstation " +
                      deviceObj2.device)
    else:
        if retStruct.returnCode() != 0:
            LogOutput('info', 'Success!: Failed to ping workstation %s ' %
                      deviceObj2.device + 'from workstation %s as expected' %
                      deviceObj1.device)
            LogOutput(
                'debug', "Debug information:\n%s" %
                str(retStruct.retValueString()))
        else:
            LogOutput('error', 'Failure!: Ping was successful')
            LogOutput('debug', "Debug information:\n" +
                      str(retStruct.retValueString()))
            packet_loss = retStruct.valueGet(key='packet_loss')
            packets_sent = retStruct.valueGet(key='packets_transmitted')
            packets_received = retStruct.valueGet(key='packets_received')
            LogOutput('debug', "Packets Sent:\t" + str(packets_sent))
            LogOutput('debug', "Packets Recv:\t" + str(packets_received))
            LogOutput('debug', "Packet Loss %:\t" + str(packet_loss))
            return False
    return True


def lagAddInterface(deviceObj, lagId, int, config):
    # Adds/removes interfaces from LAG
    if config:
        LogOutput('info', "Adding interface " + str(int) +
                  " to LAG" + lagId + " on device " + deviceObj.device)
    else:
        LogOutput('info', "Removing interface " + str(int) +
                  " to LAG" + lagId + " on device " + deviceObj.device)
    returnStruct = InterfaceLagIdConfig(
        deviceObj=deviceObj, interface=int, lagId=lagId, enable=config)
    if returnStruct.returnCode() != 0:
        if config:
            LogOutput('error', 'Failed to add interface to LAG')
        else:
            LogOutput('error', 'Failed to remove interface from LAG')
        return False
    return True


def lagVerifyNumber(dutObj, expectedNumber):
    '''
    Verifies the number of LAGs in a switch is the same as expected

    Params:
        dutObj (object): Switch reference
        expectedNumber (int): Number of expected LAGs in configuration

    Returns:
        bool: True if the number of LAGs is as expected, False otherwise
    '''
    LogOutput('info', 'Verifying number of LAGs in device %s...' %
              dutObj.device)
    retStruct = lacpAggregatesShow(deviceObj=dutObj)
    if retStruct.returnCode() != 0:
        LogOutput('error', 'Could not obtain information on number of LAGs')
        return False
    if len(retStruct.valueGet().keys()) != expectedNumber:
        LogOutput('error', 'Different number of LAGs in config')
        LogOutput('error', 'Expected: %d - Actual: %d' %
                  (expectedNumber, len(retStruct.valueGet().keys())))
        return False
    LogOutput('info', 'As expected')
    return True


def lagChangeLACPRate(deviceObj, lagId, lacpFastFlag=False, config=True):
    '''
    Changes LACP rate of LAG directly on OVS

    Args:
        deviceObj (object): Device on which change is made
        lagId (str): Number of LAG in configuration, this change
            is to make it similar to library function once
            pending defect is fixed
        lacpFastFlag (bool, optional): True indicates the rate will
            be set to fast, False is for slow
        config (bool, optional): True indicates lacp-rate will be configured,
            False is for wiping lacp-rate from OVS

    Returns:
        bool: True if successful, False otherwise
    '''

    # Variable declaration
    lacpRate = {'lacp-time': 'lacp-time',
                'values': {True: 'fast', False: 'slow'}}

    # If deviceObj or lagId are not defined, return error
    if not deviceObj or not lagId:
        LogOutput('error', "The device and LAG ID must be specified")
        return False
    LogOutput('debug', "Verifying LAG %s configuration..." % str(lagId))

    # Get into vtyshelll
    returnStructure = deviceObj.VtyshShell(enter=True)
    returnCode = returnStructure.returnCode()
    if returnCode != 0:
        LogOutput('error', "Failed to get vtysh prompt")
        return False
    # Get into linux context
    value = expecting(deviceObj.expectHndl, 'exit')
    deviceObj.deviceContext = 'linux'
    if not value:
        LogOutput('error', 'Unable to exit vtysh context')
        return False

    # Get current LAG information
    command = 'ovs-vsctl get port lag%s other_config' % str(lagId)
    if not expecting(deviceObj.expectHndl, command):
        LogOutput('error', 'Unable to retrieve LAG %s information' %
                  str(lagId))
        return False
    # If LAG is not present, return error
    if re.search(r'no row "lag%s"' % str(lagId), deviceObj.expectHndl.before):
        LogOutput('error', 'LAG %s does not exist' % str(lagId))
        return False

    # Separate information
    res = re.findall(r'[{ ](.+?=.+?)[},]',
                     deviceObj.expectHndl.before)

    # Look for pre-existing LACP rate
    for i, value in enumerate(res, 0):
        if (len(re.findall(lacpRate['lacp-time'], value) > 0)):
            if config:
                text = value.split('=')
                text[1] = lacpRate['values'][lacpFastFlag]
                text = '='.join(text)
                res[i] = text
            else:
                res.remove(value)
            break
    if config:
        # If no pre-existing information exists, fill it
        if len(res) == 0:
            res.append('='.join([lacpRate['lacp-time'],
                                 lacpRate['values'][lacpFastFlag]]))

    command = ('ovs-vsctl set port lag%s other_config={%s}' %
               (str(lagId), ', '.join(res)))
    if not expecting(deviceObj.expectHndl, command):
        LogOutput('error', 'Unable to configure LAG %s' % str(lagId))
        return False
    return True


def lacpCaptureFormat(capText):
    '''
    Format output of tcpdump capture into usable information
    The text that matches is the output from: tcpdump -i <INTERFACE> -v -e
    when observing LACP messages

    Args:
        capText (str): Text which is to be formatted

    Returns:
        list[dict(str)]: Dictionary with LACP information for each packet
            None if it cannot format the data
    '''
    def flagParse(flagText):
        retDict = {'Activ': '0', 'TmOut': '0', 'Aggr': '0', 'Sync': '0',
                   'Col': '0', 'Dist': '0', 'Def': '0', 'Exp': '0'}
        parseDict = {'Activ': 'Activ', 'Time': 'TmOut', 'Aggr': 'Aggr',
                     'Sync': 'Sync', 'Col': 'Col', 'Dist': 'Dist',
                     'Def': 'Def', 'Exp': 'Exp'}
        for key in parseDict.keys():
            if re.search(key, flagText):
                retDict[parseDict[key]] = '1'
        return retDict
    finalResult = None
    hoursSum = [0, 0]
    if capText is None:
        LogOutput('error', 'To format LACP capture please use a no None ' +
                  'type object')
        return None

    formatExpr = (r'(\d+?):(\d+?):(\d+?)[.](\d{6}) ([0-9a-z]{2}:[0-9a-z]{2}' +
                  r':[0-9a-z]{2}:[0-9a-z]{2}:[0-9a-z]{2}:[0-9a-z]{2}).*?([0' +
                  r'-9a-z]{2}:[0-9a-z]{2}:[0-9a-z]{2}:[0-9a-z]{2}:[0-9a-z]{' +
                  r'2}:[0-9a-z]{2}).*?LACP.*?Actor.*?System ([0-9a-z]{2}:[0' +
                  r'-9a-z]{2}:[0-9a-z]{2}:[0-9a-z]{2}:[0-9a-z]{2}:[0-9a-z]{' +
                  r'2}).*?System Priority (\d+?), Key (\d+?), Port (\d+?), ' +
                  r'Port Priority (\d+?)\s.*?Flags \[(.*?)\].*?Partner.*?Sy' +
                  r'stem ([0-9a-z]{2}:[0-9a-z]{2}:[0-9a-z]{2}:[0-9a-z]{2}:[' +
                  r'0-9a-z]{2}:[0-9a-z]{2}).*?System Priority (\d+?), Key (' +
                  r'\d+?), Port (\d+?), Port Priority (\d+?)\s.*?Flags \[(.' +
                  r'*?)\]')

    formatRes = re.findall(formatExpr, str(capText), re.DOTALL)
    if len(formatRes) == 0:
        LogOutput('error', 'Could not format LACP capture information')
        return None
    finalResult = []
    for res in formatRes:
        base = 0
        resDict = {'general_info': {}, 'actor_info': {}, 'partner_info': {}}
        if hoursSum[0] > int(res[0]):
            hoursSum[1] += 1
        hoursSum[0] = int(res[0])
        resDict['general_info']['time'] = timedelta(days=hoursSum[1],
                                                    hours=int(res[0]),
                                                    minutes=int(res[1]),
                                                    seconds=int(res[2]),
                                                    microseconds=int(res[3]))
        resDict['general_info']['src_mac'] = res[4]
        resDict['general_info']['dst_mac'] = res[5]
        base = 6
        for devInfo in [resDict['actor_info'], resDict['partner_info']]:
            devInfo['system_id'] = res[base]
            devInfo['system_priority'] = res[base+1]
            devInfo['key'] = res[base+2]
            devInfo['port_id'] = res[base+3]
            devInfo['port_priority'] = res[base+4]
            devInfo['flags'] = flagParse(res[base+5])
            base += 6
        finalResult.append(resDict)
    return finalResult

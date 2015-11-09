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
##########################################################################
# Description: Verify the functionality of creating LAGs with unsupported IDs.
#
# Author:      Juan Pablo Jimenez
#
# Topology:                           |DUT|-------|Switch|
#                                     |   |-------|      |
#                                        |            |
#                                        |            |
#                                  |workStation|   |workStation|
#
#
# Success Criteria:  PASS -> DUT should reject all invalid parameters
#                            #
#                    FAILED -> If DUT accepts invalid parameters
#
##########################################################################
import pytest
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *
import re
import pexpect
import random
import time

topoDict = {"topoExecution": 3000,
            "topoDevices": "dut01 dut02 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut01:dut02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut02:wrkston02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation,\
                            wrkston01:docker-image: openswitch/ubuntutest,\
                            wrkston02:docker-image: openswitch/ubuntutest"}


def showRun(**kwargs):
    """
    Library function to get the running configuration from the device.

    :param deviceObj : Device object
    :type  deviceObj : object
    :return: returnStruct Object
            buffer

    :returnType: object
    """
    deviceObj = kwargs.get('deviceObj', None)

    overallBuffer = []
    bufferString = ""

# If Device object is not passed, we need to error out
    if deviceObj is None:
        opstestfw.LogOutput(
            'error', "Need to pass switch deviceObj to this routine")
        returnCls = returnStruct(returnCode=1)
        return returnCls

# Get into vtyshelll
    returnStructure = deviceObj.VtyshShell(enter=True)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        opstestfw.LogOutput('error', "Failed to get vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=1, buffer=bufferString)
        return returnCls

##########################################################################
# Send Command
##########################################################################
    command = "show running-config"
    opstestfw.LogOutput('debug', "Sending: " + command)
    returnDevInt = deviceObj.DeviceInteract(command=command)
    retCode = returnDevInt['returnCode']
    overallBuffer.append(returnDevInt['buffer'])

    if retCode != 0:
        opstestfw.LogOutput('error', "Failed to get information ." + command)

###########################################################################
# Get out of the Shell
###########################################################################
    returnStructure = deviceObj.VtyshShell(enter=False)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        opstestfw.LogOutput('error', "Failed to exit vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=1, buffer=bufferString)
        return returnCls

###########################################################################
# Exit for context and validate buffer with information
###########################################################################
    for curLine in overallBuffer:
        bufferString += str(curLine)

    returnCls = opstestfw.returnStruct(returnCode=0, buffer=bufferString)
    return returnCls


def showInterface(**kwargs):
    """
    Library function to get specific interface information from the device.

    :param deviceObj : Device object
    :type  deviceObj : object
    :param interface : interface number context (optional)
    :type  interface : integer
    :return: returnStruct Object
            buffer

    :returnType: object
    """
    deviceObj = kwargs.get('deviceObj', None)
    interface = kwargs.get('interface', None)

    overallBuffer = []
    bufferString = ""

# If Device object is not passed, we need to error out
    if deviceObj is None:
        opstestfw.LogOutput(
            'error', "Need to pass switch deviceObj to this routine")
        returnCls = returnStruct(returnCode=1)
        return returnCls

# Get into vtyshelll
    returnStructure = deviceObj.VtyshShell(enter=True)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        opstestfw.LogOutput('error', "Failed to get vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=1, buffer=bufferString)
        return returnCls

##########################################################################
# Send Command
##########################################################################
    if interface is None:
        command = "show interface"
    else:
        command = "show interface " + str(interface)

    opstestfw.LogOutput('debug', "Sending: " + command)
    returnDevInt = deviceObj.DeviceInteract(command=command)
    retCode = returnDevInt['returnCode']
    overallBuffer.append(returnDevInt['buffer'])

    if retCode != 0:
        opstestfw.LogOutput('error', "Failed to get information ." + command)

###########################################################################
# Get out of the Shell
###########################################################################
    returnStructure = deviceObj.VtyshShell(enter=False)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        opstestfw.LogOutput('error', "Failed to exit vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=1, buffer=bufferString)
        return returnCls

###########################################################################
# Exit for context and validate buffer with information
###########################################################################
    for curLine in overallBuffer:
        bufferString += str(curLine)

    returnCls = opstestfw.returnStruct(returnCode=0, buffer=bufferString)
    return returnCls


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


def check_lag_ownership(dut, lagId, interfaces):
    if not expecting(dut.expectHndl, 'ovs-vsctl get port %s' % lagId +
                     ' interfaces'):
        LogOutput('error', 'Could not get the interfaces in %s' %
                  str(lagIg) + ' on device %s' % dut.device)
        return False

    lagUuidInterfaces = re.search(r'\[(.*)\]',
                                  dut.expectHndl.before).group(1)
    lagUuidInterfaces = lagUuidInterfaces.split(', ')

    if len(lagUuidInterfaces) != len(interfaces):
        LogOutput('error', 'The number of interfaces in %s on ' % lagId +
                  'device %s is different from the number of interfaces to' +
                  ' evaluate')
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
        LogOutput('info', '%d interfaces have been ' % len(interfaces) +
                  'accounted for in %s as expected' % lagId)
    return True


def check_lacp_status(dut01, interfaceLag):

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


def check_lacp_interface_status(dut01, interface):

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


def verifyLACPStatusAndFlags(dut01,
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
                             dut02LACPCurrentVals=None):
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
             'flags': dut01Flags, 'keys': dut01LnksKeys, 'ids': dut01LnksKeys,
             'priorities': dut01LnkPriorities,
             'lacp_currents': dut01LACPCurrentVals},
            {'dut': dut02, 'lag': lag02, 'lacp_status': dut02LACPStatus,
             'lacp_interfaces': dut02LACPInterfacesStatus,
             'flags': dut02Flags, 'keys': dut02LnksKeys, 'ids': dut02LnksKeys,
             'priorities': dut02LnkPriorities,
             'lacp_currents': dut02LACPCurrentVals}]

    '''
    Attempt to retrieve LACP information
    It should fail when LACP is disabled and succeed otherwise
    '''

    LogOutput('info', 'Verify ownership of LAGs on interfaces')
    for dut in duts:
        LogOutput('info', 'Device: %s....' % dut['dut'].device)
        interfaces = [dut['dut'].linkPortMapping[interface] for interface
                      in lagLinks]
        if not check_lag_ownership(dut['dut'], dut['lag'], interfaces):
            return False

    LogOutput(
        'info', 'Attempt to retrieve LACP information for all switches ' +
        'interfaces')
    for dut in duts:
        LogOutput('info', 'Device: %s....' % dut['dut'].device)
        try:
            dut['lacp_status'] = check_lacp_status(dut['dut'], dut['lag'])
            if not lacpActive:
                LogOutput('error', 'LACP status information detected on ' +
                          'device %s with LACP disabled' % dut['dut'].device)
                return False
        except AttributeError as e:
            if lacpActive:
                LogOutput('error', 'Could not verify LACP status for LAG' +
                          ' %s in device %s. Exception: %s' %
                          (dut['lag'], dut['dut'].device, str(e)))
                return False
        for lagLink in lagLinks:
            try:
                stat = check_lacp_interface_status(dut['dut'],
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
                  'static LAGs')
        return True

    # Validate LACP is up and information is consistent between partners

    LogOutput('info', 'Analyze obtained LACP information')
    for i, dut in enumerate(duts, 0):
        LogOutput('info', 'Device: %s....' % dut['dut'].device)
        # Validate LAG LACP status
        if not dut['lacp_status']['bond_status'] == status:
            LogOutput('error', 'Unexpected LACP status for device ' +
                      '%s: %s' % (dut['dut'].device,
                                  dut['lacp_status']['bond_status']))
            LogOutput('error', 'Expected: %s' % status)
            return False
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

        expectedSystemId = retStruct.data
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
                    LogOutput('error', 'Flag: %s', key)
                    LogOutput('error', 'Device: %s' % dut['dut'].device)
                    LogOutput('error', 'Local status: %s' %
                              ints1['actor_state'][key])
                    LogOutput('error', 'Expected local status: %s' %
                              dut['flags'][key])
                    return False
                if ints1['actor_state'][key] != ints2['partner_state'][key]:
                    LogOutput('error', 'Difference in LACP information ' +
                              'betweeen partners')
                    LogOutput('error', 'Flag: %s', key)
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


def verifyLAGTrafficFlow(dut01,
                         dut02,
                         wrkston01,
                         wrkston02,
                         wrkston01IP,
                         wrkston02IP,
                         lagLinks,
                         wrkston01Link,
                         wrkston02Link,
                         ipPrefix):
    '''
    Tests LAG traffic behaviors with broadcast and Unicast packets
    The function assumes the topology is comprised of 2 switches connected
    through a LAG and these devices serve to connect 2 workstation each
    located in one switch port

    WARNING: The IP address of both workstations may change after executing
    this function

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

    Returns:
        bool: True if configuration matches, False otherwise
    '''

    def tcpdumpInterfaces(dut):
        '''
        Obtains the equivalent names of active interfaces for use with tcpdump

        Args:
            dut (Switch): Switch with active interfaces

        Returns:
            None
        '''
        expectHndl = dut['obj'].expectHndl
        # obtain port number in TCPDUMP
        # enter switch context
        retStruct = dut['obj'].VtyshShell(enter=True)
        if retStruct.returnCode() != 0:
            return False
        if not expecting(expectHndl, 'exit'):
            return False
        # retrieve interface number for correct tcpdump call
        if not expecting(expectHndl, 'ip netns exec swns bash'):
            return False
        if not expecting(expectHndl, 'tcpdump -D'):
            return False
        dut['tcpdump_links'] = {}
        for result in re.findall(r'(\d+)[.](\d+)', expectHndl.before):
            dut['tcpdump_links'][result[1]] = result[0]
        return True

    def startWiresharkCap(device, deviceLink, filter=None):
        '''
        Initiates a tcpdump capture on a device link on the background
        The capture output is sent to a temporal file

        Args:
            device (Device): Device on which a capture is started
            deviceLink (str): Interface on device to start capture
                Note this is the interface name tcpdump understands
                See tcpdumpInterfaces function for more information
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

    def stopWiresharkCap(device,
                         processId,
                         deviceLink,
                         filter,
                         filter2=None):
        '''
        Stops tcpdump capture on device and reads obtained information
        from temporal file

        Args:
            device (Device): Device on which a capture was started
            processId (int): Process number of capture on device's system
            deviceLink (str): Interface on device in whcih capture was started
                Note this is the interface name tcpdump understands
                See tcpdumpInterfaces function for more information
            filter (str): Filter expression to look for desired packets in
                capture
            filter2 (str, optional): Second filter expression

        Returns:
            dict: Dictionary with parsed information
                filtered (int): Number of filtered packets if a filter was
                    defined in startWiresharkCap
                total (int): Total number of packets capture
                filtered_matches (int): Number of packets matching filter
                    argument
                filtered_matches2 (int, optional): Number of packets matching
                    filter2 argument
        '''
        expectHndl = device.expectHndl
        expecting(expectHndl, 'kill %d' % processId)
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
            match = re.findall(filter, expectHndl.before)
            if match:
                res['filtered_matches'] = len(match)
            else:
                res['filtered_matches'] = 0
            if filter2:
                match = re.findall(filter2, expectHndl.before)
                if match:
                    res['filtered_matches2'] = len(match)
                else:
                    res['filtered_matches2'] = 0
        except Exception as e:
            LogOutput('error',
                      'Error while deciphering packets ' +
                      'obtained by Wireshark for device %s' %
                      str(device.device))
            LogOutput('error', 'Exception:\n%s' % e)
            return None
        return res

    def obtainMacAddresses(devices):
        '''
        Creates a list with all the MAC addresses used by all devices in
        the links of interest

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

    def generateMacAddress(macList):
        '''
        Generates a new MAC address to use and verifies it is not in use

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

        Args:
            ipAddrList (list[str]): List of IP addresses already employed
            prefix: First 3 octets of IP address range to use

        Returns:
            str: IP address not already in use
        '''
        random.seed()
        while True:
            if len(ipAddrList) == 255:
                return None
            ipAddr = '%s.%d' % (prefix, random.randint(0, 255))
            if ipAddr not in ipAddrList:
                ipAddrList.append(ipAddr)
                return ipAddr

    def broadcastTrafficTest(wrkstonSrc,
                             wrkstonDst,
                             dut01,
                             dut02,
                             randomUnusedIPAddress):
        '''
        Tests if LAG is able to correctly handle broadcast packets

        Note: Internally, captures are only done on the switch receiving
            the broadcast messages, this is by design and not an oversight

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
        procs2 = []
        proc3 = 0
        res2 = []
        res3 = None
        linksWithTraffic = []
        LogOutput('info', 'Initiate traffic captures on switch %s links...' %
                  dut02['obj'].device)
        for link in dut02['lag_links']:
            try:
                proc2 = startWiresharkCap(
                    dut02['obj'],
                    dut02['tcpdump_links'][dut02['lag_links'][link]],
                    'arp')
                if not (proc2):
                    raise RuntimeError('Unable to start capture on device')
                procs2.append(proc2)
            except KeyError as e:
                LogOutput('error', 'One interface of device is not active')
                return False
            except Exception as e:
                LogOutput(
                    'error', 'Error while starting traffic capture on' +
                    ' switches to measure broadcast traffic')
                LogOutput('error', 'Exception information:\n%s' % e)
                return False
        LogOutput('info', 'Initiate traffic capture on destination ' +
                  'workstation %s...' % wrkstonDst['obj'].device)
        proc3 = startWiresharkCap(
            wrkstonDst['obj'], wrkstonDst['wrkston_link'].values()[0], 'arp')
        LogOutput('info', 'Transmit broadcast traffic')
        wrkstonSrc['obj'].Ping(ipAddr=randomUnusedIPAddress)
        time.sleep(2)
        LogOutput('info', 'Stop traffic captures on switch %s links...' %
                  dut02['obj'].device)
        for proc2, link in zip(procs2, dut01['lag_links'].keys()):
            res2.append(stopWiresharkCap(dut02['obj'],
                                         proc2,
                                         dut02['tcpdump_links'][dut02
                                                                ['lag_links']
                                                                [link]],
                                         'who-has %s tell %s' %
                                         (randomUnusedIPAddress,
                                          wrkstonSrc['wrkston_ip'])))
        LogOutput('info', 'Stop traffic capture on destination ' +
                  'workstation %s...' % wrkstonDst['obj'].device)
        if proc3:
            res3 = stopWiresharkCap(wrkstonDst['obj'],
                                    proc3,
                                    wrkstonDst['wrkston_link'].values()[0],
                                    'who-has %s tell %s' %
                                    (randomUnusedIPAddress,
                                     wrkstonSrc['wrkston_ip']))
        LogOutput('info', 'Analyzing results...')
        for r2, link in zip(res2, dut01['lag_links'].keys()):
            if r2['filtered_matches'] > 0:
                linksWithTraffic.append(link)
                if r2['filtered_matches'] < 10:
                    LogOutput('error',
                              'Less traffic than expected was seen on' +
                              ' LAG link: Expected: At least 10 - ' +
                              'Actual: %d' % r2['filtered_matches'])
                    LogOutput('error', 'Expected: At least 10')
                    LogOutput('error', 'Interface on device %s is %s' %
                              (dut01['obj'].device,
                               dut01['lag_links'][link]))
                    LogOutput('error', 'Interface on device %s is %s' %
                              (dut02['obj'].device,
                               dut02['lag_links'][link]))
                    return False
                if r2['filtered_matches'] > 12:
                    LogOutput('error',
                              'More traffic than expected was seen on LAG' +
                              ' link: %d' % r2['filtered_matches'])
                    LogOutput('error', 'Interface on device %s is %s' %
                              (dut01['obj'].device,
                               dut01['lag_links'][link]))
                    LogOutput('error', 'Interface on device %s is %s' %
                              (dut02['obj'].device,
                               dut02['lag_links'][link]))
                    return False

        if res3:
            if res3['filtered_matches'] < 10:
                LogOutput(
                    'error',
                    'Less traffic than expected was received after client' +
                    ' broadcast transmission on another workstation')
                LogOutput('error', 'Expected: At least 10 - Actual: %d' %
                          res3['filtered_matches'])
                return False
            if res3['filtered_matches'] > 12:
                LogOutput(
                    'error',
                    'More traffic than expected was received after client' +
                    ' broadcast transmission on another workstation')
                LogOutput('error', 'Expected: At most 12 - Actual: %d' %
                          res3['filtered_matches'])
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

    def getIntoVtysh(device):
        '''
        Normalizes device prompt so it can be handled by standard framework
        functions

        Args:
            device (dict): Information of device

        Returns:
            bool: True if managed to get into VTYSH, False otherwise
        '''
        expectHndl = device.expectHndl
        if not expecting(expectHndl, 'exit'):
            LogOutput(
                'error', 'Could not return to VTYSH on device %s' %
                device.device)
            return False
        if not expecting(expectHndl, 'vtysh'):
            LogOutput(
                'error', 'Could not return to VTYSH on device %s' %
                device.device)
            return False
        return True

    def getInterfaceCounters(device, interface):
        '''
        Obtains packet counters of interface on device

        Args:
            device (dict): Information of device
            interface (str): Interface from which to get information

        Returns:
            dict: Dictionary with interface counters
                input (int)
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

    def changeWorkstationInfo(device, macAddr, ipAddr):
        '''
        Changes a workstation MAC address and IP address

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

    def getDeviceCounters(device):
        '''
        Obtains the interface counters for all LAG links in a device

        Args:
            device (dict): Device information

        Returns:
            list[dict]: List of interface counters for all device's LAG links
        '''
        res = []
        for interface in device['lag_links'].values():
            res.append(getInterfaceCounters(device, interface))
        return res

    def analyzeCounters(countersDut01,
                        countersDut02,
                        countersDut01After,
                        countersDut02After,
                        offset=None):
        '''
        Analyzes interface counters obtained from 2 switches at different
        times and calculates statistics based on packets transferred

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

    def analyzeCountersBytes(countersDut01,
                             countersDut02,
                             countersDut01After,
                             countersDut02After,
                             offset=None, minTrafficBytes=125000.0,
                             maxTrafficBytes=1250000.0, errTolerance=0.1):
        '''
        Analyzes interface counters obtained from 2 switches at different
        times and calculates statistics based on bytes transferred

        Args:
            countersDut01 (list[dict]): Counters of switch 1 on moment 1
            countersDut02 (list[dict]): Counters of switch 2 on moment 1
            countersDut01After (list[dict]): Counters of switch 1 on moment 2
            countersDut02After (list[dict]): Counters of switch 2 on moment 2
            offset (list[int], optional): List of offset values to adjust
                interface traffic to account for idle traffic like that from
                LACP protocol
            minTrafficBytes (float, optional): Number of bytes expected at the
                very least to be transmitted on a port to consider it active.
                Considered to be 10%of traffic expected. The analysis expects
                an active port to be this value minus tolerance.
                Default: 125000.0
            maxTrafficBytes (float, optional): Number of bytes expected to be
                transmitted at most on a single port. If value is higher than
                it plus error tolerance, the flag for excess traffic is turned
                on on resulting analysis. Default: 1250000.0
            errTolerance (float, optional): Error tolerance for traffic
                values. Default: 0.1

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

    def unicastTrafficTest(wrkstonSrc,
                           wrkstonDst,
                           dut01,
                           dut02,
                           macList,
                           ipAddrList):
        '''
        Tests the LAG is able to transmit Unicast traffic employing each
        active link with different types of traffic

        Each traffic transmission test sends 10 seconds worth of traffic at
        1 Mbps

        Since the device counters don't update immediatly, the function waits
        the 10 seconds of the test plus some more time. By default the full
        waiting time is 20 seconds

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
        timeToWait = 20
        # idle setup values
        LogOutput('info', 'Obtain setup idle traffic behavior...')
        values11 = getDeviceCounters(dut01)
        values21 = getDeviceCounters(dut02)
        time.sleep(timeToWait)
        values12 = getDeviceCounters(dut01)
        values22 = getDeviceCounters(dut02)
        analysis = analyzeCountersBytes(values11, values21, values12, values22)
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
            changeWorkstationInfo(wrkstonDst, macAddr, ipAddr)
            values11 = getDeviceCounters(dut01)
            values21 = getDeviceCounters(dut02)

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
            LogOutput('info', 'Starting iperf client on device %s...' %
                      wrkstonSrc['obj'].device)
            retStruct = hostIperfClientStart(deviceObj=wrkstonSrc['obj'],
                                             protocol='UDP', serverIP=ipAddr,
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
            if trafficReceived != trafficTransmit:
                LogOutput('error', 'Traffic received by server is different ' +
                          'than expected')
                LogOutput('error', 'Expected: %d bytes' % trafficTransmit)
                LogOutput('error', 'Actual: %d bytes' % trafficReceived)
                return False

            values12 = getDeviceCounters(dut01)
            values22 = getDeviceCounters(dut02)
            analysis = analyzeCountersBytes(
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
                            int(trafficTransmit * (1 + errTolerance)) +
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
                            int(minTrafficTransmit * (1 - errTolerance)) +
                            'below %d' % int(trafficTransmit *
                                             (1 - errTolerance)))
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
                linksUsed.append(linksWithTraffic[0])
                if len(linksUsed) == len(expectedUsedLinks):
                    break
            else:
                LogOutput('info', 'Link %s was used again to transmit ' %
                          linksWithTraffic[0] + 'traffic')
            LogOutput('info', 'Finished analysis successfully')
        LogOutput('info', 'Unicast test finished successfully')
        return True

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
        'wrkston_ip': wrkston01IP,
        'lag_links': {}
    }
    wrkston02Info = {
        'obj': wrkston02,
        'wrkston_link': {wrkston02Link:
                         wrkston02.linkPortMapping[wrkston02Link]},
        'wrkston_ip': wrkston02IP,
        'lag_links': {}
    }

    LogOutput(
        'debug',
        'Translating interfaces names to perform tcpdump ' +
        'captures on switches')
    if not tcpdumpInterfaces(dut01Info):
        LogOutput('error', 'Error while obtaining interfaces information' +
                  'for tcpdump')
        return False
    if not tcpdumpInterfaces(dut02Info):
        LogOutput('error', 'Error while obtaining interfaces information' +
                  'for tcpdump')
        return False
    macList = obtainMacAddresses(
        [dut01Info, dut02Info, wrkston01Info, wrkston02Info])
    ipAddrList = [wrkston01Info['wrkston_ip'], wrkston02Info[
        'wrkston_ip'], '%s.0' % ipPrefix, '%s.255' % ipPrefix]
    if not (macList or ipAddrList):
        LogOutput(
            'error',
            'Could not obtain information to begin testing flow of ' +
            'traffic inside the LAG')
        return False
    LogOutput('info', 'Generate broadcast traffic from workstation %s' %
              str(wrkston01Info['obj'].device))
    if not broadcastTrafficTest(wrkston01Info,
                                wrkston02Info,
                                dut01Info,
                                dut02Info,
                                generateIPAddress(ipAddrList, ipPrefix)):
        print('before_test', dut01.expectHndl.before + dut01.expectHndl.after)
        expecting(dut01.expectHndl, 'exit')
        print('after_test', dut01.expectHndl.before + dut01.expectHndl.after)
        expecting(dut02.expectHndl, 'exit')
        dut01.deviceContext = 'linux'
        dut02.deviceContext = 'linux'
        return False
    LogOutput('info', 'Generate broadcast traffic from workstation %s' %
              str(wrkston02Info['obj'].device))
    if not broadcastTrafficTest(wrkston02Info,
                                wrkston01Info,
                                dut02Info,
                                dut01Info,
                                generateIPAddress(ipAddrList, ipPrefix)):
        expecting(dut01.expectHndl, 'exit')
        expecting(dut02.expectHndl, 'exit')
        dut01.deviceContext = 'linux'
        dut02.deviceContext = 'linux'
        return False
    if not getIntoVtysh(dut01):
        return False
    if not getIntoVtysh(dut02):
        return False
    LogOutput('info', 'Generate unicast traffic from workstation %s' %
              str(wrkston01Info['obj'].device))
    if not unicastTrafficTest(wrkston01Info,
                              wrkston02Info,
                              dut01Info,
                              dut02Info,
                              macList,
                              ipAddrList):
        dut01.VtyshShell(enter=False)
        dut02.VtyshShell(enter=False)
        return False
    LogOutput('info', 'Generate unicast traffic from workstation %s' %
              str(wrkston02Info['obj'].device))
    if not unicastTrafficTest(wrkston02Info,
                              wrkston01Info,
                              dut02Info,
                              dut01Info,
                              macList,
                              ipAddrList):
        dut01.VtyshShell(enter=False)
        dut02.VtyshShell(enter=False)
        return False
    retStruct = dut01Info['obj'].VtyshShell(enter=False)
    if retStruct.returnCode() != 0:
        return False
    retStruct = dut02Info['obj'].VtyshShell(enter=False)
    if retStruct.returnCode() != 0:
        return False
    return True


# Adds interfaces to LAG

def verifyLAGConfig(
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
    retStruct = lacpAggregatesShow(deviceObj=deviceObj, lagId=lagId)
    if retStruct.returnCode() != 0:
        return False
    baseLag = {
        "interfaces": interfaces,
        "lacpMode": lacpMode,
        "fallbackFlag": fallbackFlag,
        "hashType": hashType,
        "lacpFastFlag": lacpFastFlag}
    for key in baseLag:
        LogOutput('debug', "Verifying attribute %s..." % key)
        if isinstance(baseLag[key], list):
            for i in baseLag[key]:
                if i not in retStruct.valueGet(key=lagId)[key]:
                    LogOutput(
                        'error',
                        "Interface %s was not found in LAG %s" %
                        (str(i), str(lagId)))
                    return False
            continue
        if baseLag[key] != retStruct.valueGet(key=lagId)[key]:
            LogOutput(
                'error',
                "Failure verifying LAG %s configuration " % str(lagId) +
                "configuration on attribute %s" % key)
            LogOutput(
                'error',
                "Found: %s - Expected: %s" %
                (str(retStruct.valueGet(key=lagId)[key]), str(baseLag[key])))
            return False
        LogOutput('debug', "Passed")
    LogOutput(
        'debug',
        "Verification LAG %s configuration passed" % str(lagId))
    return True

# Parses the output of "show run" and verify that the config is empty.
# Returns True if the configuration is empty, False otherwise


def val_empty_config(devices):
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


def switch_reboot(deviceObj):
    if not val_empty_config([deviceObj]):
        # Reboot switch
        LogOutput('info', "Reboot switch " + deviceObj.device)
        deviceObj.Reboot()
    if not val_empty_config([deviceObj]):
        return False
    return True

# Adds interfaces to LAG


def addInterfacesToLAG(deviceObj, lagId, intArray):
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

# Enable/disable routing on interfaces so VLANs can be configured


def enableInterfaceRouting(deviceObj, int, enable):
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
            LogOutput('info', "Enabledrouting on interface " +
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


def enableDutInterface(deviceObj, int, enable):
    def get_int_status(dev, interface):
        output = showInterface(deviceObj=dev, interface=interface).buffer()
        ret_expression = re.search(
            r'Interface \d is (down|up)',
            output
        )
        if ret_expression.group(1) == "up":
            return True
        return False

    if enable:
        retStruct = InterfaceEnable(
            deviceObj=deviceObj, enable=enable, interface=int)
        if not (retStruct.returnCode() == 0 and get_int_status(deviceObj,
                                                               int)):
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
        if retStruct.returnCode() != 0 or get_int_status(deviceObj, int):
            LogOutput(
                'error', "Failed to disable " + deviceObj.device +
                " interface " + int)
            return False
        else:
            LogOutput(
                'info', "Disabled " + deviceObj.device + " interface " + int)

    return True

# Create/delete a LAG and add interfaces


def createLAG(deviceObj, lagId, configure, intArray, mode):
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
        retStruct = addInterfacesToLAG(deviceObj, lagId, intArray)
        if retStruct.returnCode() != 0:
            return False
        if mode != 'off':
            retStruct = lagMode(
                lagId=str(lagId), deviceObj=deviceObj, lacpMode=mode)
            if retStruct.returnCode() != 0:
                return False
        if not verifyLAGConfig(deviceObj, lagId, intArray, mode):
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


def addInterfaceVLAN(deviceObj, vlanId, enable, int):
    # Verify a port has been assigned to a vlan

    def verifyVlanPorts(dut, vlanID, port):
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

    if enable:
        retStruct = enableInterfaceRouting(deviceObj, int, False)
        if retStruct.returnCode() != 0:
            return False
        retStruct = AddPortToVlan(deviceObj=deviceObj, vlanId=vlanId,
                                  interface=int, access=True)
        if not (retStruct.returnCode() == 0 and
                verifyVlanPorts(deviceObj, vlanId, int)):
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
                not verifyVlanPorts(deviceObj, vlanId, int)):
            LogOutput(
                'error', "Failed to delete VLAN " + str(vlanId) +
                " to interface " + int)
            return False
        else:
            LogOutput('info', "Delete VLAN " + str(vlanId) +
                      " to interface " + int)
        retStruct = enableInterfaceRouting(deviceObj, int, True)
        if retStruct.returnCode() != 0:
            return False
    return True

# Configure/delete VLAN on switch


def configureVLAN(deviceObj, vlanId, enable):
    ''' Verify a vlan exist on vlan table.

        Args:
             dut (obj) : device under test
             pVlan (str) : vlan name to verify

     '''

    def verifyVlan(dut, pVlan):
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

    if enable:
        LogOutput('debug', "Configuring VLAN " + str(vlanId) +
                  " on device " + deviceObj.device)
        retStruct = AddVlan(deviceObj=deviceObj, vlanId=vlanId)
        if retStruct.returnCode() != 0 or verifyVlan(deviceObj, vlanId) != 0:
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
        if retStruct.returnCode() != 0 or verifyVlan(deviceObj, vlanId) != 1:
            LogOutput('error', "Failed to delete VLAN " +
                      str(vlanId) + " on device " + deviceObj.device)
            return False
        else:
            LogOutput(
                'info', "Deleted VLAN " + str(vlanId) + " on device " +
                deviceObj.device)
    return True

# Configure/unconfigure the IP address of a workstation


def configureWorkstation(deviceObj, int, ipAddr, netMask, broadcast, enable):
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

# Ping between workstation


def pingBetweenWorkstations(deviceObj1, deviceObj2, ipAddr, success):
    LogOutput('info', "Pinging between workstation " +
              deviceObj1.device + " and workstation " + deviceObj2.device)
    if success:
        retStruct = deviceObj1.Ping(ipAddr=ipAddr)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to ping from workstation " +
                      deviceObj1.device + ":\n" +
                      str(retStruct.retValueString()))
            return False
        else:
            LogOutput('info', "IPv4 Ping from workstation 1 to workstation 2 \
            return JSON:\n" +
                      str(retStruct.retValueString()))
            packet_loss = retStruct.valueGet(key='packet_loss')
            packets_sent = retStruct.valueGet(key='packets_transmitted')
            packets_received = retStruct.valueGet(key='packets_received')
            LogOutput('info', "Packets Sent:\t" + str(packets_sent))
            LogOutput('info', "Packets Recv:\t" + str(packets_received))
            LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
            LogOutput('info', "Passed ping test between workstation " +
                      deviceObj1.device + " and workstation " +
                      deviceObj2.device)
    else:
        retStruct = deviceObj1.Ping(ipAddr=ipAddr)
        if retStruct.returnCode() != 0:
            LogOutput(
                'debug', "Failed to ping workstation2 as expected:\n" +
                str(retStruct.retValueString()))
            LogOutput('info',
                      "Passed negative ping test between workstation " +
                      deviceObj1.device + " and workstation " +
                      deviceObj2.device)
        else:
            LogOutput('error', "IPv4 Ping from workstation 1 to workstation \
            2 return JSON:\n" +
                      str(retStruct.retValueString()))
            packet_loss = retStruct.valueGet(key='packet_loss')
            packets_sent = retStruct.valueGet(key='packets_transmitted')
            packets_received = retStruct.valueGet(key='packets_received')
            LogOutput('error', "Packets Sent:\t" + str(packets_sent))
            LogOutput('error', "Packets Recv:\t" + str(packets_received))
            LogOutput('error', "Packet Loss %:\t" + str(packet_loss))
            return False
    return True


def createLAGNegative(deviceObj, lagId, configure=True):
    '''
    Configures a LAG with invalid ID to verify if DUT rejects the parameter

    Args:
        deviceObj (PSwitch,VSwitch): Device from which configuration is
            verified
        lagId (str): LAG identifier
        configure(bool): Configure option, set by default to True
    '''
    if configure:
        retStruct = lagCreation(
            deviceObj=deviceObj, lagId=str(lagId), configFlag=True)
        if retStruct.returnCode() != 0:
            LogOutput(
                'info', "LAG " + str(lagId) + " not created on "
                + deviceObj.device)
            return True
        else:
            LogOutput(
                'error', "Created LAG" + str(lagId) + " on " +
                deviceObj.device)
            return False


def verifyLAGnumbers(deviceObj, number_id=1):
    '''
    Verifies the number of LAGs configured in the device

    Args:
        deviceObj (PSwitch,VSwitch): Device from which configuration is
            verified
        number_id (int): Number of expected IDs configured in the device
    '''
    if not deviceObj:
        LogOutput('error', "The device  must be specified")
        return False
    LogOutput('debug', "Verifying LAG configuration...")
    retStruct = lacpAggregatesShow(deviceObj=deviceObj)

    if retStruct.returnCode() != 0:
        return False
    if len(retStruct.valueGet().keys()) == number_id:
        LogOutput(
            'info', "LAGs configured in the device %s: %s"
            % (deviceObj.device, str(len(retStruct.valueGet().keys()))))
        return True
    else:
        LogOutput('error', "LAGs configured in the device did not match")
        return False

# Clean up devices


def clean_up_devices(dut01Obj, dut02Obj, wrkston01Obj, wrkston02Obj):
    LogOutput('info', "\n############################################")
    LogOutput('info', "Device Cleanup - rolling back config")
    LogOutput('info', "############################################")
    finalResult = []

    LogOutput('info', "Unconfigure workstations")
    LogOutput('info', "Unconfiguring workstation 1")
    finalResult.append(configureWorkstation(
        wrkston01Obj,
        wrkston01Obj.linkPortMapping['lnk01'], "140.1.1.10",
        "255.255.255.0", "140.1.1.255", False))
    LogOutput('info', "Unconfiguring workstation 2")
    finalResult.append(configureWorkstation(
        wrkston02Obj,
        wrkston02Obj.linkPortMapping['lnk04'], "140.1.1.11",
        "255.255.255.0", "140.1.1.255", False))

    LogOutput('info', "Delete LAGs on DUTs")
    finalResult.append(createLAG(dut01Obj, '1', False, [], None))
    finalResult.append(createLAG(dut02Obj, '1', False, [], None))

    LogOutput('info', "Disable interfaces on DUTs")
    LogOutput('info', "Configuring switch dut01")
    finalResult.append(
        enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk01'],
                           False))
    finalResult.append(
        enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk02'],
                           False))
    finalResult.append(
        enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk03'],
                           False))

    LogOutput('info', "Configuring switch dut02")
    finalResult.append(
        enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'],
                           False))
    finalResult.append(
        enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03'],
                           False))
    finalResult.append(
        enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk04'],
                           False))

    LogOutput('info', "Remove VLAN from DUTs")
    finalResult.append(configureVLAN(dut01Obj, 900, False))
    finalResult.append(configureVLAN(dut02Obj, 900, False))

    for i in finalResult:
        if not i:
            LogOutput('error', 'Errors were detected while cleaning ' +
                      'devices')
            return
    LogOutput('info', "Cleaned up devices")


class Test_ft_framework_basics:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_ft_framework_basics.testObj = testEnviron(topoDict=topoDict)
        Test_ft_framework_basics.topoObj =\
            Test_ft_framework_basics.testObj.topoObjGet()

    def teardown_class(cls):
        # clean devices
        clean_up_devices(
            cls.topoObj.deviceObjGet(device="dut01"),
            cls.topoObj.deviceObjGet(device="dut02"),
            cls.topoObj.deviceObjGet(device="wrkston01"),
            cls.topoObj.deviceObjGet(device="wrkston02"))
        # Terminate all nodes
        Test_ft_framework_basics.topoObj.terminate_nodes()

    def test_reboot_switch(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Reboot the switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        devRebootRetStruct = switch_reboot(dut01Obj)
        if not devRebootRetStruct:
            LogOutput('error', "Failed to reboot and clean Switch 1")
            assert(devRebootRetStruct.returnCode() == 0)
        else:
            LogOutput('info', "Passed Switch 1 Reboot piece")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        devRebootRetStruct = switch_reboot(dut02Obj)
        if not devRebootRetStruct:
            LogOutput('error', "Failed to reboot and clean Switch 2")
            assert(devRebootRetStruct.returnCode() == 0)
        else:
            LogOutput('info', "Passed Switch 2 Reboot piece")

    def test_enableDUTsInterfaces(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Enable switches interfaces")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        LogOutput('info', "Configuring switch dut01")
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk01'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk02'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk03'],
                               True))

        LogOutput('info', "Configuring switch dut02")
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk04'],
                               True))

    def test_createLAGs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Create LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(createLAG(dut01Obj, '1', True, [dut01Obj.linkPortMapping[
            'lnk02'], dut01Obj.linkPortMapping['lnk03']], 'off'))
        assert(createLAG(dut02Obj, '1', True, [dut02Obj.linkPortMapping[
            'lnk02'], dut02Obj.linkPortMapping['lnk03']], 'off'))

    def test_configureVLANs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Configure VLANs on switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        # Switch 1
        LogOutput('info', "Configure VLAN on dut01")
        assert(configureVLAN(dut01Obj, 900, True))
        assert(
            addInterfaceVLAN(dut01Obj, 900, True,
                             dut01Obj.linkPortMapping['lnk01']))
        assert(addInterfaceVLAN(dut01Obj, 900, True, 'lag 1'))
        # Switch 2
        LogOutput('info', "Configure VLAN on dut02")
        assert(configureVLAN(dut02Obj, 900, True))
        assert(
            addInterfaceVLAN(dut02Obj, 900, True,
                             dut02Obj.linkPortMapping['lnk04']))
        assert(addInterfaceVLAN(dut02Obj, 900, True, 'lag 1'))

    def test_lagConfiguration_1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAG configuration was successfully applied")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(verifyLACPStatusAndFlags(dut01Obj, dut02Obj, False,
                                        ['lnk02', 'lnk03'], 'lag1', 'lag1'))

    def test_configureWorkstations_1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Configure workstations")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        LogOutput('info', "Configuring workstation 1")
        assert(configureWorkstation(
            wrkston01Obj,
            wrkston01Obj.linkPortMapping[
                'lnk01'], "140.1.1.10", "255.255.255.0", "140.1.1.255", True))
        LogOutput('info', "Configuring workstation 2")
        assert(configureWorkstation(
            wrkston02Obj,
            wrkston02Obj.linkPortMapping[
                'lnk04'], "140.1.1.11", "255.255.255.0", "140.1.1.255", True))

    def test_lagTraffic_1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAG traffic")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(verifyLAGTrafficFlow(dut01Obj, dut02Obj, wrkston01Obj,
                                    wrkston02Obj, '140.1.1.10',
                                    '140.1.1.11', ['lnk02', 'lnk03'],
                                    'lnk01', 'lnk04', '140.1.1'))

# Negative Testing

    def test_createLAGs_Negative(self):
        # Configure ivalid LAGs in the DUT
        LogOutput('info', "\n############################################")
        LogOutput(
            'info', "Configure a new LAG with invalid IDs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        duts = [dut01Obj, dut02Obj]

        for dutObj in duts:
            assert(createLAGNegative(dutObj, '-1'))
            assert(createLAGNegative(dutObj, '0'))
            assert(createLAGNegative(dutObj, '2001'))
            assert(createLAGNegative(dutObj, 'abc'))
            assert(createLAGNegative(dutObj, '@$%+abc'))

    def test_verify_lag_config(self):
        # Verify if LAG1 config is not modified
        LogOutput('info', "\n############################################")
        LogOutput(
            'info', "Verify LAG 1 config stability")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        duts = [dut01Obj, dut02Obj]

        for dutObj in duts:
            LogOutput('info', "Verifying LAG config on " + dutObj.device)
            assert(verifyLAGConfig(dutObj, '1', [dutObj.linkPortMapping[
                'lnk02'], dutObj.linkPortMapping['lnk03']]))

    def test_verify_lag_number(self):
        # Verify is only one LAG is configured
        LogOutput('info', "\n############################################")
        LogOutput(
            'info', "Verify number of LAGs configured")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        duts = [dut01Obj, dut02Obj]

        for dutObj in duts:
            LogOutput('info', "Verifying number of LAGs on " + dutObj.device)
            assert(verifyLAGnumbers(dutObj))

    def test_lagConfiguration_2(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAG configuration was not modified")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(verifyLACPStatusAndFlags(dut01Obj, dut02Obj, False,
                                        ['lnk02', 'lnk03'], 'lag1', 'lag1'))

    def test_configureWorkstations_2(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Configure workstations")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        LogOutput('info', "Configuring workstation 1")
        assert(configureWorkstation(
            wrkston01Obj,
            wrkston01Obj.linkPortMapping[
                'lnk01'], "140.1.1.10", "255.255.255.0", "140.1.1.255", True))
        LogOutput('info', "Configuring workstation 2")
        assert(configureWorkstation(
            wrkston02Obj,
            wrkston02Obj.linkPortMapping[
                'lnk04'], "140.1.1.11", "255.255.255.0", "140.1.1.255", True))

    def test_ping_2(self):
        # Test ping between Workstations
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test ping between workstations")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        assert(pingBetweenWorkstations(
            wrkston01Obj, wrkston02Obj, '140.1.1.11', True))

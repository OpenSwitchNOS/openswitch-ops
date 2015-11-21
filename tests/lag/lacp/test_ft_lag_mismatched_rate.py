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
###############################################################################
# Name:        test_lag_lacp_ft_mismatched_rate.py
#
# Description:  Verify the behavior of a DUT with a slow rate, when it doesn't 
#               receive LACP PDU 
#
# Author:      Oscar Alas
#
# Topology:  |Host| ----- |Switch| ---------------------- |Switch| ----- |Host|
#                                   (Dynamic LAG - 2 links)
#
# Success Criteria:  PASS -> Lag LACP rate returns to the original config
#
#                    FAILED -> If Lag LACP rate does not return to the original
#                              configuration 
#
###############################################################################

import pytest
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *
from lib_test import lagVerifyTrafficFlow
from lib_test import lagVerifyLACPStatusAndFlags
from lib_test import lagVerifyConfig
from lib_test import switchEnableInterface
from lib_test import lagCreate
from lib_test import vlanAddInterface
from lib_test import vlanConfigure
from lib_test import workstationConfigure
from lib_test import switchReboot
from lib_test import lagVerifyNumber
from lib_test import workstationsPing
from lib_test import interfaceEnableRouting

from lib_test import lagChangeLACPRate
from lib_test import lacpCaptureFormat
from lib_test import swtichGetIntoVtyshOrSwns
from lib_test import switchTcpdumpInterfaces
from lib_test import deviceStartWiresharkCap
from lib_test import deviceStopWiresharkCap
from lib_test import deviceObtainActiveMacAddresses
from time import sleep
from audioop import avg

topoDict = {"topoExecution": 3000,
            "topoTarget": "dut01 dut02",
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


def trafficCaptureStart(deviceObj, interfaces):
    tcpdumpInts = None
    macInts = None
    procs = None
    if not swtichGetIntoVtyshOrSwns(deviceObj, enter=False):
        LogOutput('error', 'Could not enter into linux switching context')
        return None, None, None
    res = switchTcpdumpInterfaces(deviceObj)
    if not res[0]:
        swtichGetIntoVtyshOrSwns(deviceObj)
        LogOutput('Could not obtain information on the interfaces for ' +
                  'tcpdump on device %s' % deviceObj.device)
        return None, None, None
    tcpdumpInts = res[1]
    macInts = deviceObtainActiveMacAddresses(deviceObj, interfaces)
    procs = []
    for interface, macAddr in zip(interfaces, macInts):
        procs.append(deviceStartWiresharkCap(deviceObj,
                                             tcpdumpInts[interface],
                                             '-v -e ether src %s' %
                                             macAddr.lower()))
    if None in procs:
        swtichGetIntoVtyshOrSwns(deviceObj)
        LogOutput('error', 'Could not start traffic captures on device %s' %
                  deviceObj.device)
        return None, None, None
    return procs, tcpdumpInts, macInts


def trafficCaptureStop(deviceObj, interfaces, tcpdumpInts, processesIds):
    LogOutput('info', 'Obtaining results...')
    res = []
    for proc, interface in zip(processesIds, interfaces):
        res.append(deviceStopWiresharkCap(deviceObj, proc, 
                                          tcpdumpInts[interface]))
    if None in res:
        swtichGetIntoVtyshOrSwns(deviceObj)
        LogOutput('error', 'Could not stop traffic captures on device %s' %
                  deviceObj.device)
        return None
    if not swtichGetIntoVtyshOrSwns(deviceObj):
        LogOutput('error', 'Could not return to normal device context')
        return None
    return res


def lagCheckFinish(dut01Obj, dut02Obj, activeFlag1, fastFlag1, fastFlag2,
                   lagId2):
    interfaces = dut01Obj.linkPortMapping['lnk02']
    tcpdumpInts = None
    macInts = None
    procs = None
    waitTime = 0
    heartbeat = 0
    if activeFlag1:
        heartbeat = 1
        if fastFlag1:
            if fastFlag2:
                waitTime = 10
            else:
                waitTime = 120
        else:
            if fastFlag2:
                waitTime = 10
            else:
                waitTime = 120
    else:
        heartbeat = 30
        if fastFlag1:
            if fastFlag2:
                waitTime = 10
            else:
                waitTime = 120
        else:
            if fastFlag2:
                waitTime = 10
            else:
                waitTime = 120
    trafficCaptureStart(dut01Obj, interfaces)
    if not (procs and tcpdumpInts and macInts):
        return False
    retStruct = lagMode(lagId=str(lagId2), deviceObj=dut02Obj, lacpMode='off')
    if retStruct.returnCode() != 0:
        LogOutput('error', 'Could not change LACP mode to off' +
                  ' on device %s' % dut02Obj.device)
        return False
    LogOutput('info', 'Waiting %d seconds...' % waitTime)
    sleep(waitTime)
    res = trafficCaptureStop(dut01Obj, interfaces, tcpdumpInts, procs)
    if not res:
        return False
    LogOutput('info', 'Analyzing results...')
    for interface, formattedResult in zip(interfaces,
                                          (lacpCaptureFormat(val)
                                           for val in res)):
        if not formattedResult:
            return False
        filteredListSrc = [element for element in formattedResult if\
                        formattedResult['src_mac'] ==\
                        macInts[interfaces.index(interface)]]
        filteredListDst = [element for element in formattedResult if\
                        formattedResult['dst_mac'] ==\
                        macInts[interfaces.index(interface)]]
        expired = []
        defaulted = []
        current = []
        expired.append({'count': 0, 'last': -1, 'first': -1})
        expired.append({'count': 0, 'last': -1, 'first': -1})
        defaulted.append({'count': 0, 'last': -1, 'first': -1})
        defaulted.append({'count': 0, 'last': -1, 'first': -1})
        current.append({'count': 0, 'last': -1, 'first': -1})
        current.append({'count': 0, 'last': -1, 'first': -1})
        for list, ex, de, cu in zip([filteredListSrc, filteredListDst],
                                    expired, defaulted, current):
            for i, val in enumerate(list):
                if val['flags']['actor_info']['Exp'] == '1':
                    ex['count'] += 1
                    ex['last'] = i
                    if ex['first'] == -1:
                        ex['first'] = i
                if val['flags']['actor_info']['Def'] == '1':
                    de['count'] += 1
                    de['last'] = i
                    if de['first'] == -1:
                        de['first'] = i
                if ((val['flags']['actor_info']['Exp'] == '0') and
                    (val['flags']['actor_info']['Exp'] == '0')):
                    cu['count'] += 1
                    cu['last'] = i
                    if cu['first'] == -1:
                        cu['first'] = i
        if ((expired[1]['count'] != 0) or (defaulted[1]['count'] != 0)):
            LogOutput('error', 'Device %s kept sending LACP messages' %
                      dut02Obj)
            return False
        '''
        Missing validations:
        No active message from other switch is older than any of expired messages
        Time difference between first expired heartbeat and the heartbeats before timeout have
            to be at least 3 times the current timeout value
        Duration of expired heartbeats has to be at most 4 seconds and there cannot be a more than 1 per second
        Frequency of packets before expired has to be what the other switch had configured
        Expired messages are older than current messages
        '''
        if activeFlag1:
            if (defaulted[0]['first'] == -1):
                LogOutput('error','No defaulted messages were sent from ' +
                          'device %s' % dut01Obj.device)
                return False
            if (defaulted[0]['first'] == defaulted[0]['last']):
                LogOutput('error','Only 1 defaulted message was sent from ' +
                          'device %s' % dut01Obj.device)
                return False
            '''
            Missing validations:
            Defaulted rate is consisted with configured rate
            Defaulted messages are older than current and expired messages
            '''
        else:
            if (defaulted[0]['first'] != -1):
                LogOutput('error','Observed messages in default state from ' +
                          'device %s when it is set to passive' %
                          dut01Info['obj'].device)
                return False
        
    


def lagLACPCheckStart(dut01Obj, dut02Obj, activeFlag1, activeFlag2,
                      fastFlag1, fastFlag2, lagId1, lagId2):
    tcpdumpInts = None
    macInts = None
    procs = None
    waitTime = 0
    heartbeat = 0
    mode = ''
    dut01Info = {'obj': dut01Obj, 'active_flag': activeFlag1,
                 'fast_flag': fastFlag1, 'id': str(lagId1)}
    dut02Info = {'obj': dut02Obj, 'active_flag': activeFlag2,
                 'fast_flag': fastFlag2, 'id': str(lagId1)}
    if ((dut01Info['active_flag'] == dut02Info['active_flag'])
        and not dut01Info['active_flag']):
        LogOutput('error', 'Both devices are set on passive')
        return False
    if dut01Info['active_flag']:
        if dut02Info['fast_flag']:
            waitTime = 10
        else:
            waitTime = 70
    else:
        if dut02Info['fast_flag']:
            waitTime = 10
        else:
            waitTime = 100
    if dut02Info['fast_flag']:
        heartbeat = 1
    else:
        heartbeat = 30
    LogOutput('info', 'Starting traffic captures on devices')
    trafficCaptureStart(dut01Obj, interfaces)
    if not (procs and tcpdumpInts and macInts):
        return False
    if dut01Info['active_flag']:
        mode = 'active'
    else:
        mode = 'passive'
    retStruct = lagMode(lagId=str(lagId1), deviceObj=dut01Info['obj'],
                        lacpMode=mode)
    if retStruct.returnCode() != 0:
        LogOutput('error', 'Could not change LACP mode to %s' % mode +
                  ' on device %s' % dut01Info['obj'].device)
        return False
    LogOutput('info', 'Waiting %d seconds...' % waitTime)
    sleep(waitTime)
    res = trafficCaptureStop(dut01Obj, interfaces, tcpdumpInts, procs)
    if not res:
        return False
    LogOutput('info', 'Analyzing results...')
    for interface, formattedResult in zip(interfaces,
                                          (lacpCaptureFormat(val)
                                           for val in res)):
        if not formattedResult:
            return False
        filteredListSrc = [element for element in formattedResult if\
                        formattedResult['src_mac'] ==\
                        macInts[interfaces.index(interface)]]
        filteredListDst = [element for element in formattedResult if\
                        formattedResult['dst_mac'] ==\
                        macInts[interfaces.index(interface)]]
        expired = []
        defaulted = []
        current = []
        expired.append({'count': 0, 'last': -1, 'first': -1})
        expired.append({'count': 0, 'last': -1, 'first': -1})
        defaulted.append({'count': 0, 'last': -1, 'first': -1})
        defaulted.append({'count': 0, 'last': -1, 'first': -1})
        current.append({'count': 0, 'last': -1, 'first': -1})
        current.append({'count': 0, 'last': -1, 'first': -1})
        for list, ex, de, cu in zip([filteredListSrc, filteredListDst],
                                    expired, defaulted, current):
            for i, val in enumerate(list):
                if val['flags']['actor_info']['Exp'] == '1':
                    ex['count'] += 1
                    ex['last'] = i
                    if ex['first'] == -1:
                        ex['first'] = i
                if val['flags']['actor_info']['Def'] == '1':
                    de['count'] += 1
                    de['last'] = i
                    if de['first'] == -1:
                        de['first'] = i
                if ((val['flags']['actor_info']['Exp'] == '0') and
                    (val['flags']['actor_info']['Exp'] == '0')):
                    cu['count'] += 1
                    cu['last'] = i
                    if cu['first'] == -1:
                        cu['first'] = i
        if expired[0]['first'] != -1:
            LogOutput('error', 'Observed the expired flag on a LACP ' +
                      'message from device %s' % dut01Info['obj'].device)
            return False
        if (defaulted[0]['last'] != -1) and (defaulted[0]['last'] ==\
                                             expired[0]['last']):
            LogOutput('error', 'Observed the expired and default flag on ' +
                      'same LACP message from device %s' %
                      dut01Info['obj'].device)
            return False
        if current[0]['last'] != (len(filteredListSrc) - 1):
            LogOutput('error', 'Could not detect that link established ' +
                      'after capture finished on device %s' %
                      dut01Info['obj'].device)
            return False
        if dut01Info['active_flag']:
            if defaulted['first'] != -1:
                t = (filteredListDst[current[1]\
                                     ['first']]['general_info']['time'] -
                     filteredListSrc[defaulted[0]\
                                     ['first']]['general_info']['time'])
                if not (t.seconds > 0 and t.seconds < 2):
                    LogOutput('error', 'Device %s took 2 seconds or more to ' %
                              dut02Info['obj'].device +
                              'answer LACP message for the first time')
                    return False    
        else:
            if current[0]['first'] != 0:
                LogOutput('error','First message transmitted by passive ' +
                          'device %s was not when link was established' %
                          dut01Info['obj'].device)
            if (defaulted[0]['first'] != -1):
                LogOutput('error','Observed messages in default state from ' +
                          'device %s when it is set to passive' %
                          dut01Info['obj'].device)
                return False
        t = (filteredListSrc[current[0]['first']]['general_info']['time'] -
             filteredListDst[defaulted[1]['last']]['general_info']['time'])
        if not (t.seconds > 0 and t.seconds < 2):
            LogOutput('error', 'Device %s took 2 seconds or more to ' %
                      dut01Info['obj'].device +
                      'answer LACP message for the first time')
            return False
        if len(filteredListSrc) == current[0]['first']:
            LogOutput('error','Only 1 heartbeat was sent from device %s' %
                      dut01Info['obj'] + 'since establishing connection')
            return False
        t = (filteredListSrc[current[0]['first']+1]['general_info']['time'] -
             filteredListSrc[current[0]['first']]['general_info']['time'])
        if t < (heartbeat - 1):
            LogOutput('error', 'LACP hearbteat average rate is too slow ' +
                      'on interface %s' % interface)
            LogOutput('error', 'Expected: %d - Found: %.2f' %
                      (heartbeat, t))
            return False
        if t > (heartbeat + 1):
            LogOutput('error', 'LACP hearbteat average rate is too fast ' +
                      'on interface %s' % interface)
            LogOutput('error', 'Expected: %d - Found: %.2f' %
                      (heartbeat, t))
            return False

def lagLACPTimeCheckAverage(deviceObj, interfaces, fastHeartbeat):
    heartbeat = 0
    waitTime = 0
    tcpdumpInts = None
    macInts = None
    procs = None
    if fastHeartbeat:
        heartbeat = 1
        waitTime = 3
    else:
        heartbeat = 30
        waitTime = 90
    LogOutput('info', 'Verifying LACP rate behavior for device %s...' %
              deviceObj.device)
    procs, tcpdumpInts, macInts =\
    trafficCaptureStart(deviceObj, interfaces)
    if not (procs and tcpdumpInts and macInts):
        return False
    LogOutput('info', 'Waiting %d seconds to let LACP traffic flow...' %
              waitTime)
    sleep(waitTime)
    res = trafficCaptureStop(deviceObj, interfaces, tcpdumpInts, procs)
    if not res:
        return False
    LogOutput('info', 'Analyzing results...')
    for interface, formattedResult in zip(interfaces,
                                          (lacpCaptureFormat(val)
                                           for val in res)):
        if not formattedResult:
            return False
        filteredList = [element for element in formattedResult if\
                        formattedResult['src_mac'] ==\
                        macInts[interfaces.index(interface)]]
        if len(filteredList) < 2:
            LogOutput('error', 'Less than 2 LACP messages observed coming ' +
                      'from interface %s' % interface)
            return False
        avg = 0
        for i in xrange(0, len(filteredList) - 1):
            t = filteredList[i+1]['time'] - filteredList[i]['time']
            avg += t.seconds
        avg /= (len(filteredList) - 1)
        if avg < (heartbeat - 1):
            LogOutput('error', 'LACP hearbteat average rate is too slow ' +
                      'on interface %s' % interface)
            LogOutput('error', 'Expected: %d - Found: %.2f' %
                      (heartbeat, avg))
            return False
        if avg > (heartbeat + 1):
            LogOutput('error', 'LACP hearbteat average rate is too fast ' +

                      'on interface %s' % interface)
            LogOutput('error', 'Expected: %d - Found: %.2f' %
                      (heartbeat, avg))
            return False
    LogOutput('info', 'LACP heartbeat rate is as expected')
    return True


def clean_up_devices(dut01Obj, dut02Obj, wrkston01Obj, wrkston02Obj):
    # Clean up devices
    LogOutput('info', "\n############################################")
    LogOutput('info', "Device Cleanup - rolling back config")
    LogOutput('info', "############################################")
    finalResult = []
    dut01 = {'obj': dut01Obj, 'links': ['lnk01', 'lnk02', 'lnk03'],
             'wrkston_links': ['lnk01']}
    dut02 = {'obj': dut02Obj, 'links': ['lnk02', 'lnk03', 'lnk04'],
             'wrkston_links': ['lnk04']}

    LogOutput('info', "Unconfigure workstations")
    LogOutput('info', "Unconfiguring workstation 1")
    finalResult.append(workstationConfigure(
        wrkston01Obj,
        wrkston01Obj.linkPortMapping['lnk01'], "140.1.1.10",
        "255.255.255.0", "140.1.1.255", False))
    LogOutput('info', "Unconfiguring workstation 2")
    finalResult.append(workstationConfigure(
        wrkston02Obj,
        wrkston02Obj.linkPortMapping['lnk04'], "140.1.1.11",
        "255.255.255.0", "140.1.1.255", False))

    LogOutput('info', "Enable routing on DUTs workstations links")
    for dut in [dut01, dut02]:
        LogOutput('info', "Configuring switch %s" % dut['obj'].device)
        for link in dut['wrkston_links']:
            finalResult.append(interfaceEnableRouting(dut['obj'],
                                                      dut['obj'].
                                                      linkPortMapping[link],
                                                      True))

    LogOutput('info', "Disable interfaces on DUTs")
    for dut in [dut01, dut02]:
        LogOutput('info', "Configuring switch %s" % dut['obj'].device)
        for link in dut['links']:
            finalResult.append(switchEnableInterface(dut['obj'],
                                                     dut['obj'].
                                                     linkPortMapping[link],
                                                     False))

    LogOutput('info', "Delete LAGs on DUTs")
    finalResult.append(lagCreate(dut01Obj, '1', False, [], 'off'))
    finalResult.append(lagCreate(dut02Obj, '1', False, [], 'off'))

    LogOutput('info', "Remove VLAN from DUTs")
    finalResult.append(vlanConfigure(dut01Obj, 900, False))
    finalResult.append(vlanConfigure(dut02Obj, 900, False))

    for i in finalResult:
        if not i:
            LogOutput('error', "Errors were detected while cleaning \
                    devices")
            return
    LogOutput('info', "Cleaned up devices")


class Test_ft_delete_low_number_of_members:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_ft_delete_low_number_of_members.\
            testObj = testEnviron(topoDict=topoDict)
        Test_ft_delete_low_number_of_members.topoObj =\
            Test_ft_delete_low_number_of_members.testObj.topoObjGet()

    def teardown_class(cls):
        # clean devices
        clean_up_devices(
            cls.topoObj.deviceObjGet(device="dut01"),
            cls.topoObj.deviceObjGet(device="dut02"),
            cls.topoObj.deviceObjGet(device="wrkston01"),
            cls.topoObj.deviceObjGet(device="wrkston02"))
        # Terminate all nodes
        Test_ft_delete_low_number_of_members.topoObj.\
            terminate_nodes()

    def test_rebootSwitches(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Reboot the switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        devRebootRetStruct = switchReboot(dut01Obj)
        if not devRebootRetStruct:
            LogOutput('error', "Failed to reboot and clean Switch 1")
            assert(devRebootRetStruct)
        else:
            LogOutput('info', "Passed Switch 1 Reboot piece")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        devRebootRetStruct = switchReboot(dut02Obj)
        if not devRebootRetStruct:
            LogOutput('error', "Failed to reboot and clean Switch 2")
            assert(devRebootRetStruct)
        else:
            LogOutput('info', "Passed Switch 2 Reboot piece")

    def test_enableDUTsInterfaces(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Enable switches interfaces")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut01 = {'obj': dut01Obj, 'links': ['lnk01', 'lnk02', 'lnk03']}
        dut02 = {'obj': dut02Obj, 'links': ['lnk02', 'lnk03', 'lnk04']}
        for dut in [dut01, dut02]:
            LogOutput('info', "Configuring switch %s" % dut['obj'].device)
            for link in dut['links']:
                assert(switchEnableInterface(dut['obj'],
                                             dut['obj'].linkPortMapping[link],
                                             True))

    def test_createLAGs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Create LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        links = ['lnk02', 'lnk03']
        for dut, mode in zip([dut01Obj, dut02Obj], ['active', 'passive']):
            assert(lagCreate(dut, '1', True, [
                dut.linkPortMapping[link] for link in links], mode))
            assert(lagVerifyNumber(dut, 1))
    
    def test_changeLACPRate(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Change LACP timeouts to slow on devices")
        LogOutput('info', "############################################")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        links = ['lnk02', 'lnk03']
        assert(lagChangeLACPRate(dut02Obj, '1', lacpFastFlag=True, config=True))
        time.sleep(4)
        #set up sleep in 3 sec due the lacp rate has been changed to fast, 
        #otherwise it should take at least 40 sec(when it is changed to slow)
        assert(lagVerifyConfig(dut02Obj, [dut02Obj.linkPortMapping[link]\
                                          for link in links], '1',
                                lacpFastFlag=True, lacpMode=active)) 
        """for dut, mode in zip([dut01Obj, dut02Obj], ['active', 'passive']):
            assert(lagChangeLACPRate(dut, '1', lacpFastFlag=False))
            assert(lagVerifyConfig(dut01Obj, [dut.linkPortMapping[link]\
                                              for link in links], '1',
                                   lacpFastFlag=False, lacpMode=mode))"""

    def test_configureVLANs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Configure VLANs on switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut01 = {'obj': dut01Obj, 'links': ['lag 1',
                                            dut01Obj.
                                            linkPortMapping['lnk01']]}
        dut02 = {'obj': dut02Obj, 'links': ['lag 1',
                                            dut02Obj.
                                            linkPortMapping['lnk04']]}
        for dut in [dut01, dut02]:
            LogOutput('info', 'Configure VLAN on %s' % dut['obj'].device)
            assert(vlanConfigure(dut['obj'], 900, True))
            for link in dut['links']:
                assert(vlanAddInterface(dut['obj'], 900, True, link))

    def test_configureWorkstations(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Configure workstations")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        LogOutput('info', "Configuring workstation 1")
        assert(workstationConfigure(
            wrkston01Obj,
            wrkston01Obj.linkPortMapping[
                'lnk01'], "140.1.1.10", "255.255.255.0", "140.1.1.255", True))
        LogOutput('info', "Configuring workstation 2")
        assert(workstationConfigure(
            wrkston02Obj,
            wrkston02Obj.linkPortMapping[
                'lnk04'], "140.1.1.11", "255.255.255.0", "140.1.1.255", True))

    def test_LAGdisableLACPonDUT02(self):
        LogOutput('info', "\n###############################################")
        LogOutput('info', "Capture traffic on dut01 and disable lacp on dut02")
        LogOutput('info', "###############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagCheckFinish(dut01Obj, dut02Obj, True, False, True, '1'))

    def test_LAGFormation1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAGs are correctly formed and pass traffic")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        flags1 = {'Activ': '1', 'TmOut': '0', 'Aggr': '1', 'Sync': '1',
                  'Col': '1', 'Dist': '1', 'Def': '0', 'Exp': '0'}
        flags2 = {'Activ': '0', 'TmOut': '0', 'Aggr': '1', 'Sync': '1',
                  'Col': '1', 'Dist': '1', 'Def': '0', 'Exp': '0'}
        assert(lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                           ['lnk02', 'lnk03'], 'lag1', 'lag1',
                                           dut01Flags=flags1,
                                           dut02Flags=flags2))
        assert(lagVerifyTrafficFlow(dut01Obj, dut02Obj, wrkston01Obj,
                                    wrkston02Obj, '140.1.1.10',
                                    '140.1.1.11', ['lnk02', 'lnk03'], 'lnk01',
                                    'lnk04', '140.1.1'))

    def test_LACPTiming1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Verify timing of LACP messages")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        for dut in [dut01Obj, dut02Obj]:
            assert(lagLACPTimeCheckAverage(dut, [dut.linkPortMapping[link] for\
                                            link in ['lnk02', 'lnk03']],
                                      False))

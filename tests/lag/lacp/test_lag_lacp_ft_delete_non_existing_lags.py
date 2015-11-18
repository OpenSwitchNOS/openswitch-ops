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
# Name:        test_lag_lacp_ft_delete_non_existing_lags.py
#
# Description: Tests that a previously configured dynamic Link Aggregation does
#              not stop forwarding traffic when attempting to delete several
#              non-existent Link Aggregations with different names that may not
#              be supported
#
# Author:      Jose Hernandez
#
# Topology:  |Host| ----- |Switch| ---------------------- |Switch| ----- |Host|
#                                   (Dynamic LAG - 2 links)
#
# Success Criteria:  PASS -> Non-existent LAGs cannot be deleted and they
#                            don't affect the functioning LAG
#
#                    FAILED -> Functioning LAG configuration is changed or any
#                              of the non-existing LAGs don't produce errors
#                              when attempting to delete them
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
from lib_test import interfaceEnableRouting
from lib_test import interfaceGetStatus

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


def lagDeleteNegative(
        deviceObj, lagId, goodLagId, goodLagMode, goodLagInterfaces,
        goodLagHash, goodLagFallback, goodLagFastFlag):
    '''
    Function to try and delete a non-existent LAG. It assumes there is only
    1 other LAG and then matches the information present in DUT to verify it
    wasn't modified
    '''
    retStruct = lagCreation(
        deviceObj=deviceObj, lagId=str(lagId), configFlag=False)
    if retStruct.returnCode() != 0:
        LogOutput('info', "Failed to delete LAG " + str(lagId) +
                  " as expected on " + deviceObj.device)
    else:
        LogOutput('error', "Deleted LAG " + str(lagId) +
                  " unexpectedly on " + deviceObj.device)
        return False
    if not lagVerifyNumber(deviceObj, 1):
        return False
    if not lagVerifyConfig(deviceObj, goodLagId, interfaces=goodLagInterfaces,
                           lacpMode=goodLagMode, fallbackFlag=goodLagFallback,
                           hashType=goodLagHash, lacpFastFlag=goodLagFastFlag):
        return False
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
        wrkston01Obj, wrkston01Obj.linkPortMapping['lnk01'],
        "140.1.1.10", "255.255.255.0", "140.1.1.255", False))
    LogOutput('info', "Unconfiguring workstation 2")
    finalResult.append(workstationConfigure(
        wrkston02Obj, wrkston02Obj.linkPortMapping['lnk04'],
        "140.1.1.11", "255.255.255.0", "140.1.1.255", False))

    LogOutput('info', "Delete LAGs on DUTs")
    finalResult.append(lagCreate(dut01Obj, '1', False, [], 'off'))
    finalResult.append(lagCreate(dut02Obj, '1', False, [], 'off'))

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

    LogOutput('info', "Remove VLAN from DUTs")
    finalResult.append(vlanConfigure(dut01Obj, 900, False))
    finalResult.append(vlanConfigure(dut02Obj, 900, False))

    for i in finalResult:
        if not i:
            LogOutput('error', "Errors were detected while cleaning \
                    devices")
            return
    LogOutput('info', "Cleaned up devices")


class Test_ft_delete_non_existing_lags:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_ft_delete_non_existing_lags.testObj =\
            testEnviron(topoDict=topoDict)
        Test_ft_delete_non_existing_lags.topoObj =\
            Test_ft_delete_non_existing_lags.testObj.topoObjGet()

    def teardown_class(cls):
        # clean up devices
        clean_up_devices(
            cls.topoObj.deviceObjGet(device="dut01"),
            cls.topoObj.deviceObjGet(device="dut02"),
            cls.topoObj.deviceObjGet(device="wrkston01"),
            cls.topoObj.deviceObjGet(device="wrkston02"))
        # Terminate all nodes
        Test_ft_delete_non_existing_lags.topoObj.terminate_nodes()

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
        assert(lagCreate(dut01Obj, '1', True, [
            dut01Obj.linkPortMapping['lnk02'],
            dut01Obj.linkPortMapping['lnk03']], 'active'))
        assert(lagCreate(dut02Obj, '1', True, [
            dut02Obj.linkPortMapping['lnk02'],
            dut02Obj.linkPortMapping['lnk03']], 'passive'))
        assert(lagVerifyNumber(dut01Obj, 1))
        assert(lagVerifyNumber(dut02Obj, 1))

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

    def test_verifyInterfaces(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Verify switches interfaces are up")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut01 = {'obj': dut01Obj, 'links': ['lnk01', 'lnk02', 'lnk03']}
        dut02 = {'obj': dut02Obj, 'links': ['lnk02', 'lnk03', 'lnk04']}
        for dut in [dut01, dut02]:
            LogOutput('info', 'Device %s' % dut['obj'].device)
            for link in dut['links']:
                assert(interfaceGetStatus(dut['obj'],
                                          dut['obj'].linkPortMapping[link]))

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

    def test_LAGFormation1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAGs are correctly formed and pass traffic")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        assert(lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                           ['lnk02', 'lnk03'], 'lag1', 'lag1',
                                           dut02Flags={'Activ': '0',
                                                       'TmOut': '0',
                                                       'Aggr': '1',
                                                       'Sync': '1',
                                                       'Col': '1',
                                                       'Dist': '1',
                                                       'Def': '0',
                                                       'Exp': '0'}))
        assert(lagVerifyTrafficFlow(dut01Obj, dut02Obj, wrkston01Obj,
                                    wrkston02Obj, '140.1.1.10',
                                    '140.1.1.11', ['lnk02', 'lnk03'], 'lnk01',
                                    'lnk04', '140.1.1'))

    def test_deleteLAGs1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Delete non-existent LAGs on both DUTs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        for dut, mode in zip([dut01Obj, dut02Obj], ['active', 'passive']):
            LogOutput('info', 'Attemtpt to delete LAGs on %s' % dut.device)
            LogOutput('info', 'With ID XX')
            assert(lagDeleteNegative(dut, 'XX', '1', mode, [
                dut.linkPortMapping['lnk02'],
                dut.linkPortMapping['lnk03']], 'l3-src-dst', False,
                False))
            LogOutput('info', 'With ID 0')
            assert(lagDeleteNegative(dut, '0', '1', mode, [
                dut.linkPortMapping['lnk02'],
                dut.linkPortMapping['lnk03']], 'l3-src-dst', False,
                False))
            LogOutput('info', 'With ID -1')
            assert(lagDeleteNegative(dut, '-1', '1', mode, [
                dut.linkPortMapping['lnk02'],
                dut.linkPortMapping['lnk03']], 'l3-src-dst', False,
                False))
            LogOutput('info', 'With ID 2000')
            assert(lagDeleteNegative(dut, '2000', '1', mode, [
                dut.linkPortMapping['lnk02'],
                dut.linkPortMapping['lnk03']], 'l3-src-dst', False,
                False))
            LogOutput('info', 'With ID 2001')
            assert(lagDeleteNegative(dut, '2001', '1', mode, [
                dut.linkPortMapping['lnk02'],
                dut.linkPortMapping['lnk03']], 'l3-src-dst', False,
                False))
            LogOutput('info', 'With ID @%&$#()')
            assert(lagDeleteNegative(dut, '@%&$#()', '1', mode, [
                dut.linkPortMapping['lnk02'],
                dut.linkPortMapping['lnk03']], 'l3-src-dst', False,
                False))
            LogOutput('info', 'With ID 60000')
            assert(lagDeleteNegative(dut, '60000', '1', mode, [
                dut.linkPortMapping['lnk02'],
                dut.linkPortMapping['lnk03']], 'l3-src-dst', False,
                False))
            LogOutput('info', 'With ID 600')
            assert(lagDeleteNegative(dut, '600', '1', mode, [
                dut.linkPortMapping['lnk02'],
                dut.linkPortMapping['lnk03']], 'l3-src-dst', False,
                False))
            LogOutput('info', 'With ID 2')
            assert(lagDeleteNegative(dut, '2', '1', mode, [
                dut.linkPortMapping['lnk02'],
                dut.linkPortMapping['lnk03']], 'l3-src-dst', False,
                False))
            LogOutput('info', 'With ID 01')
            assert(lagDeleteNegative(dut, '01', '1', mode, [
                dut.linkPortMapping['lnk02'],
                dut.linkPortMapping['lnk03']], 'l3-src-dst', False,
                False))

    def test_LAGFormation2(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAGs are correctly formed and pass traffic")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        assert(lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                           ['lnk02', 'lnk03'], 'lag1', 'lag1',
                                           dut02Flags={'Activ': '0',
                                                       'TmOut': '0',
                                                       'Aggr': '1',
                                                       'Sync': '1',
                                                       'Col': '1',
                                                       'Dist': '1',
                                                       'Def': '0',
                                                       'Exp': '0'}))
        assert(lagVerifyTrafficFlow(dut01Obj, dut02Obj, wrkston01Obj,
                                    wrkston02Obj, '140.1.1.10',
                                    '140.1.1.11', ['lnk02', 'lnk03'], 'lnk01',
                                    'lnk04', '140.1.1'))

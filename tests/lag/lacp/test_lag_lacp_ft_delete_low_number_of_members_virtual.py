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
# Name:        test_lag_lacp_ft_delete_low_number_of_members.py
#
# Description: Tests that a previously configured dynamic Link Aggregation of
#              2, 1 or 0 members can be deleted
#
# Author:      Jose Hernandez
#
# Topology:  |Host| ----- |Switch| ---------------------- |Switch| ----- |Host|
#                                   (Dynamic LAG - 2 links)
#
# Success Criteria:  PASS -> LAGs are deleted when having 2, 1 or 0 members
#
#                    FAILED -> LAGs cannot be deleted in any of the scenarios
#                              mentioned in the pass criteria
#
###############################################################################

import pytest
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *
from lib_test import lagVerifyTrafficFlow
from lib_test import lagVerifyLACPStatusAndFlags
from lib_test import switchEnableInterface
from lib_test import lagCreate
from lib_test import vlanAddInterface
from lib_test import vlanConfigure
from lib_test import workstationConfigure
from lib_test import switchReboot
from lib_test import lagVerifyNumber
from lib_test import workstationsPing
from lib_test import interfaceEnableRouting
from lib_test import interfaceGetStatus

topoDict = {"topoExecution": 3000,
            "topoType": "virtual",
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

    LogOutput('info', "Delete LAGs on DUTs if present")
    finalResult.append(not lagCreate(dut01Obj, '1', False, [], 'off'))
    finalResult.append(not lagCreate(dut02Obj, '1', False, [], 'off'))

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
                                    'lnk04', '140.1.1.0'))

    def test_deleteLAGs1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Delete LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagCreate(dut01Obj, '1', False, [], 'off'))
        assert(lagCreate(dut02Obj, '1', False, [], 'off'))
        assert(lagVerifyNumber(dut01Obj, 0))
        assert(lagVerifyNumber(dut02Obj, 0))

    def test_LAGFormation2(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAGs are not working anymore")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        flagsPassive = {'Activ': '0', 'TmOut': '0', 'Aggr': '1', 'Sync': '1',
                        'Col': '1', 'Dist': '1', 'Def': '0', 'Exp': '0'}
        assert(not lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                               ['lnk02',
                                                   'lnk03'], 'lag1', 'lag1',
                                               dut02Flags=flagsPassive))
        assert(not lagVerifyLACPStatusAndFlags(dut02Obj, dut01Obj, True,
                                               ['lnk02',
                                                   'lnk03'], 'lag1', 'lag1',
                                               dut01Flags=flagsPassive))
        assert(
            workstationsPing(wrkston01Obj, wrkston02Obj, '140.1.1.11', False))

    def test_createLAG1Interface(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Create LAGs with just 1 interface")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(
            lagCreate(dut01Obj, '1', True, [
                dut01Obj.linkPortMapping['lnk02']], 'active'))
        assert(
            lagCreate(dut02Obj, '1', True, [
                dut02Obj.linkPortMapping['lnk02']], 'passive'))
        assert(lagVerifyNumber(dut01Obj, 1))
        assert(lagVerifyNumber(dut02Obj, 1))

    def test_addVLANsToLAGs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Add VLAN configuration to newly created LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(vlanAddInterface(dut01Obj, 900, True, 'lag 1'))
        assert(vlanAddInterface(dut02Obj, 900, True, 'lag 1'))

    def test_LAGFormation3(self):
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
                                    'lnk04', '140.1.1.0'))

    def test_deleteLAGs2(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Delete LAGs from DUTs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagCreate(dut01Obj, '1', False, [], 'off'))
        assert(lagCreate(dut02Obj, '1', False, [], 'off'))
        assert(lagVerifyNumber(dut01Obj, 0))
        assert(lagVerifyNumber(dut02Obj, 0))

    def test_LAGFormation4(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAGs are not working anymore")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        flagsPassive = {'Activ': '0', 'TmOut': '0', 'Aggr': '1', 'Sync': '1',
                        'Col': '1', 'Dist': '1', 'Def': '0', 'Exp': '0'}
        assert(not lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                               ['lnk02',
                                                   'lnk03'], 'lag1', 'lag1',
                                               dut02Flags=flagsPassive))
        assert(not lagVerifyLACPStatusAndFlags(dut02Obj, dut01Obj, True,
                                               ['lnk02',
                                                   'lnk03'], 'lag1', 'lag1',
                                               dut01Flags=flagsPassive))
        assert(
            workstationsPing(wrkston01Obj, wrkston02Obj, '140.1.1.11', False))

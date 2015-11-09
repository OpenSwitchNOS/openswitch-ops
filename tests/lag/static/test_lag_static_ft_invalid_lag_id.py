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


# Clean up devices


def clean_up_devices(dut01Obj, dut02Obj, wrkston01Obj, wrkston02Obj):
    # Clean up devices
    LogOutput('info', "\n############################################")
    LogOutput('info', "Device Cleanup - rolling back config")
    LogOutput('info', "############################################")
    finalResult = []
    dut01 = {'obj': dut01Obj, 'links': ['lnk01', 'lnk02', 'lnk03']}
    dut02 = {'obj': dut02Obj, 'links': ['lnk02', 'lnk03', 'lnk04']}

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

    LogOutput('info', "Delete LAGs on DUTs")
    finalResult.append(lagCreate(dut01Obj, '1', False, [], None))
    finalResult.append(lagCreate(dut02Obj, '1', False, [], None))

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

    def test_rebootSwitches(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Reboot the switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        devRebootRetStruct = switchReboot(dut01Obj)
        if not devRebootRetStruct:
            LogOutput('error', "Failed to reboot and clean Switch 1")
            assert(devRebootRetStruct.returnCode() == 0)
        else:
            LogOutput('info', "Passed Switch 1 Reboot piece")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        devRebootRetStruct = switchReboot(dut02Obj)
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
        dut01 = {'obj': dut01Obj, 'links': ['lnk01', 'lnk02', 'lnk03']}
        dut02 = {'obj': dut02Obj, 'links': ['lnk02', 'lnk03', 'lnk04']}
        for dut in [dut01, dut02]:
            LogOutput('info', "Configuring switch %s" % dut['obj'].device)
            for link in dut['links']:
                assert(switchEnableInterface(
                    dut['obj'], dut['obj'].linkPortMapping[link], True))

    def test_createLAGs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Create LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagCreate(dut01Obj, '1', True, [dut01Obj.linkPortMapping[
            'lnk02'], dut01Obj.linkPortMapping['lnk03']], 'off'))
        assert(lagCreate(dut02Obj, '1', True, [dut02Obj.linkPortMapping[
            'lnk02'], dut02Obj.linkPortMapping['lnk03']], 'off'))
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

    def test_lagConfiguration_1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAG configuration was successfully applied")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, False,
                                           ['lnk02', 'lnk03'], 'lag1', 'lag1'))

    def test_configureWorkstations_1(self):
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

    def test_lagTraffic_1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAG traffic")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagVerifyTrafficFlow(dut01Obj, dut02Obj, wrkston01Obj,
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
            assert(lagVerifyConfig(dutObj, '1', [dutObj.linkPortMapping[
                'lnk02'], dutObj.linkPortMapping['lnk03']]))

    def test_verify_lag_number(self):
        # Verify is only one LAG is configured
        LogOutput('info', "\n############################################")
        LogOutput(
            'info', "Verify number of LAGs configured")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        lagVerifyNumber(dut01Obj, 1)
        lagVerifyNumber(dut02Obj, 1)

    def test_lagConfiguration_2(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAG configuration was successfully applied")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, False,
                                           ['lnk02', 'lnk03'], 'lag1', 'lag1'))

    def test_ping_2(self):
        # Test ping between Workstations
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test ping between workstations")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        assert(workstationsPing(
            wrkston01Obj, wrkston02Obj, '140.1.1.11', True))

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
# Name:        Test_lag_dynamic_ft_interfaces_on_other_LAG
#
# Objective:   To verify the interface is moved when it is part
#                of a dynamic LAG and is added to another LAG
#
# Author:      Pablo Araya M.
#
# Topology:    2 switches, 2 workstations
#
##########################################################################

import pytest
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *
from lib_test import lagVerifyTrafficFlow
from lib_test import lagVerifyLACPStatusAndFlags
from lib_test import switchReboot
from lib_test import lagCreate
from lib_test import vlanAddInterface
from lib_test import vlanConfigure
from lib_test import workstationConfigure
from lib_test import switchEnableInterface

topoDict = {"topoExecution": 3000,
            "topoDevices": "dut01 dut02 wrkston01 wrkston02",
            "topoTarget": "dut01 dut02",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut01:dut02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut02:wrkston02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation"}


def clean_up_devices(dut01Obj, dut02Obj, wrkston01Obj, wrkston02Obj):
    LogOutput('info', "\n############################################")
    LogOutput('info', "Device Cleanup - rolling back config")
    LogOutput('info', "############################################")
    finalResult = []

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

    LogOutput('info', "\nCLEANUP - Reboot the switches")
    devRebootRetStruct = switchReboot(dut01Obj)
    if not devRebootRetStruct:
        LogOutput('error', "Failed to reboot Switch 1")
        finalResult.append(devRebootRetStruct)
    else:
        LogOutput('info', "Passed Switch 1 Reboot piece")
    devRebootRetStruct = switchReboot(dut02Obj)
    if not devRebootRetStruct:
        LogOutput('error', "Failed to reboot Switch 2")
        finalResult.append(devRebootRetStruct)
    else:
        LogOutput('info', "Passed Switch 2 Reboot piece")

    for i in finalResult:
        if not i:
            LogOutput('error', 'Errors were detected while cleaning ' +
                      'devices')
            return
    LogOutput('info', "Cleaned up devices")


class Test_lag_dynamic_ft_interfaces_on_other_LAG:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_lag_dynamic_ft_interfaces_on_other_LAG.testObj = testEnviron(
            topoDict=topoDict)
        Test_lag_dynamic_ft_interfaces_on_other_LAG.topoObj =\
            Test_lag_dynamic_ft_interfaces_on_other_LAG.testObj.topoObjGet()

    def teardown_class(cls):
        # clean devices
        clean_up_devices(
            cls.topoObj.deviceObjGet(device="dut01"),
            cls.topoObj.deviceObjGet(device="dut02"),
            cls.topoObj.deviceObjGet(device="wrkston01"),
            cls.topoObj.deviceObjGet(device="wrkston02"))
        # Terminate all nodes
        Test_lag_dynamic_ft_interfaces_on_other_LAG.topoObj.terminate_nodes()

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
        LogOutput('info', "Configuring switch dut01")
        assert(
            switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk01'],
                                  True))
        assert(
            switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk02'],
                                  True))
        assert(
            switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk03'],
                                  True))

        LogOutput('info', "Configuring switch dut02")
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'],
                                  True))
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03'],
                                  True))
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk04'],
                                  True))

    def test_configureLAG(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Create LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        lagId = "1"

        assert(lagCreate(dut01Obj, lagId, True, [dut01Obj.linkPortMapping[
            'lnk02'], dut01Obj.linkPortMapping['lnk03']], 'active'))
        assert(lagCreate(dut02Obj, lagId, True, [dut02Obj.linkPortMapping[
            'lnk02'], dut02Obj.linkPortMapping['lnk03']], 'active'))

    def test_configureVLAN(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Configure VLANs on switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        vlanId = 900

        LogOutput('info', "Configure VLAN on dut01")
        assert(vlanConfigure(dut01Obj, vlanId, True))
        assert(
            vlanAddInterface(dut01Obj, vlanId, True,
                             dut01Obj.linkPortMapping['lnk01']))
        assert(vlanAddInterface(dut01Obj, vlanId, True, 'lag 1'))
        # Switch 2
        LogOutput('info', "Configure VLAN on dut02")
        assert(vlanConfigure(dut02Obj, vlanId, True))
        assert(
            vlanAddInterface(dut02Obj, vlanId, True,
                             dut02Obj.linkPortMapping['lnk04']))
        assert(vlanAddInterface(dut02Obj, vlanId, True, 'lag 1'))

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

    def test_verifyLacpConfiguration(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAG configuration was successfully applied")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                           ['lnk02', 'lnk03'], 'lag1', 'lag1'))

    def test_verifyLagTraffic(self):
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

    def test_moveLAG(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Move LAGs to LAG 2")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        lagId = "2"

        assert(lagCreate(dut01Obj, lagId, True, [
               dut01Obj.linkPortMapping['lnk02'],
               dut01Obj.linkPortMapping['lnk03']], 'active'))
        assert(lagCreate(dut02Obj, lagId, True, [dut02Obj.linkPortMapping[
               'lnk02'], dut02Obj.linkPortMapping['lnk03']], 'active'))

    def test_configureVLAN2(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Configure VLANs on switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        vlanId = 902

        LogOutput('info', "Configure VLAN on dut01")
        assert(vlanConfigure(dut01Obj, vlanId, True))
        assert(
            vlanAddInterface(dut01Obj, vlanId, True,
                             dut01Obj.linkPortMapping['lnk01']))
        assert(vlanAddInterface(dut01Obj, vlanId, True, 'lag 1'))
        # Switch 2
        LogOutput('info', "Configure VLAN on dut02")
        assert(vlanConfigure(dut02Obj, vlanId, True))
        assert(
            vlanAddInterface(dut02Obj, vlanId, True,
                             dut02Obj.linkPortMapping['lnk04']))
        assert(vlanAddInterface(dut02Obj, vlanId, True, 'lag 1'))

    def test_verifyLagTraffic2(self):
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

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
# Description: To verify a dynamic LAG  of 8 links can be formed between 2
#              devices and verify a 9 link can be added
#
# Author:      Pablo Araya
#
# Topology:               |Switch|------|WorkStation|
#                           |||x3
#                           |||x3
#                           |||x3
#     |WorkStation|-------|Switch|
#
# Success Criteria:  PASS ->   8 links lag can be created and work correctly
#
#                    FAILED -> If lag can t be created correctly or 9 link
#                              is created
#
##########################################################################

from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *
from lib_test import *

topoDict = {"topoExecution": 3000,
            "topoType": "virtual",
            "topoDevices": "dut01 dut02 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut01:dut02,\
                          lnk03:dut01:dut02,\
                          lnk05:dut01:dut02,\
                          lnk06:dut01:dut02,\
                          lnk07:dut01:dut02,\
                          lnk08:dut01:dut02,\
                          lnk09:dut01:dut02,\
                          lnk10:dut01:dut02,\
                          lnk11:dut01:dut02,\
                          lnk04:dut02:wrkston02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation,\
                            wrkston01:docker-image: openswitch/ubuntutest,\
                            wrkston02:docker-image: openswitch/ubuntutest"}


def clean_up_devices(dut01Obj, dut02Obj, wrkston01Obj, wrkston02Obj):
    LogOutput('info', "\n############################################")
    LogOutput('info', "Device Cleanup - rolling back config")
    LogOutput('info', "############################################")
    finalResult = []

    '''LogOutput('info', "Unconfigure workstations")
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
    finalResult.append(lagCreate(dut02Obj, '1', False, [], None))'''

    LogOutput('info', "Disable interfaces on DUTs")
    LogOutput('info', "Configuring switch dut01")
    finalResult.append(
        switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk01'],
                              False))
    finalResult.append(
        switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk02'],
                              False))
    finalResult.append(
        switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk03'],
                              False))
    finalResult.append(
        switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk05'],
                              False))
    finalResult.append(
        switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk06'],
                              False))
    finalResult.append(
        switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk07'],
                              False))
    finalResult.append(
        switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk08'],
                              False))
    finalResult.append(
        switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk09'],
                              False))
    finalResult.append(
        switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk10'],
                              False))
    finalResult.append(
        switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk11'],
                              False))

    LogOutput('info', "Configuring switch dut02")
    finalResult.append(
        switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'],
                              False))
    finalResult.append(
        switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03'],
                              False))
    finalResult.append(
        switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk05'],
                              False))
    finalResult.append(
        switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk06'],
                              False))
    finalResult.append(
        switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk07'],
                              False))
    finalResult.append(
        switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk08'],
                              False))
    finalResult.append(
        switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk09'],
                              False))
    finalResult.append(
        switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk10'],
                              False))
    finalResult.append(
        switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk11'],
                              False))
    finalResult.append(
        switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk04'],
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


class Test_ft_lag_8_9_members:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_ft_lag_8_9_members.testObj = testEnviron(topoDict=topoDict)
        Test_ft_lag_8_9_members.topoObj =\
            Test_ft_lag_8_9_members.testObj.topoObjGet()

    def teardown_class(cls):
        # clean devices
        clean_up_devices(
            cls.topoObj.deviceObjGet(device="dut01"),
            cls.topoObj.deviceObjGet(device="dut02"),
            cls.topoObj.deviceObjGet(device="wrkston01"),
            cls.topoObj.deviceObjGet(device="wrkston02"))
        # Terminate all nodes
        Test_ft_lag_8_9_members.topoObj.terminate_nodes()

    def test_reboot_switch(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 1- Reboot the switches")
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
        LogOutput('info', "Step 2- Enable switches interfaces")
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
        assert(
            switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk05'],
                                  True))
        assert(
            switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk06'],
                                  True))
        assert(
            switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk07'],
                                  True))
        assert(
            switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk08'],
                                  True))
        assert(
            switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk09'],
                                  True))
        assert(
            switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk10'],
                                  True))
        assert(
            switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk11'],
                                  True))

        LogOutput('info', "Configuring switch dut02")
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'],
                                  True))
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03'],
                                  True))
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk05'],
                                  True))
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk06'],
                                  True))
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk07'],
                                  True))
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk08'],
                                  True))
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk09'],
                                  True))
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk10'],
                                  True))
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk11'],
                                  True))
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk04'],
                                  True))

    def test_createLAGs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 3- Create LAG")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagCreate(dut01Obj, '1', True, [dut01Obj.linkPortMapping[
            'lnk02'], dut01Obj.linkPortMapping['lnk03'],
            dut01Obj.linkPortMapping['lnk05'],
            dut01Obj.linkPortMapping['lnk06'],
            dut01Obj.linkPortMapping['lnk07'],
            dut01Obj.linkPortMapping['lnk08'],
            dut01Obj.linkPortMapping['lnk09'],
            dut01Obj.linkPortMapping['lnk10']], 'active'))
        assert(lagCreate(dut02Obj, '1', True, [dut02Obj.linkPortMapping[
            'lnk02'], dut02Obj.linkPortMapping['lnk03'],
            dut02Obj.linkPortMapping['lnk05'],
            dut02Obj.linkPortMapping['lnk06'],
            dut02Obj.linkPortMapping['lnk07'],
            dut02Obj.linkPortMapping['lnk08'],
            dut02Obj.linkPortMapping['lnk09'],
            dut02Obj.linkPortMapping['lnk10']], 'active'))

    def test_configureVLANs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 4- Configure VLANs on switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        # Switch 1
        LogOutput('info', "Configure VLAN on dut01")
        assert(vlanConfigure(dut01Obj, 900, True))
        assert(
            vlanAddInterface(dut01Obj, 900, True,
                             dut01Obj.linkPortMapping['lnk01']))
        assert(vlanAddInterface(dut01Obj, 900, True, 'lag 1'))
        # Switch 2
        LogOutput('info', "Configure VLAN on dut02")
        assert(vlanConfigure(dut02Obj, 900, True))
        assert(
            vlanAddInterface(dut02Obj, 900, True,
                             dut02Obj.linkPortMapping['lnk04']))
        assert(vlanAddInterface(dut02Obj, 900, True, 'lag 1'))

    def test_configureWorkstations(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 5- Configure workstations")
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

    def test_lagConfiguration(self):
        LogOutput('info', "\n############################################")
        LogOutput(
            'info', "Step 6- Test LAG configuration was successfully applied")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                           ['lnk02', 'lnk03',
                                            'lnk05', 'lnk06',
                                            'lnk07', 'lnk08',
                                            'lnk09', 'lnk10'],
                                           'lag1', 'lag1'))

    def test_lagTraffic(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 7- Test LAG traffic")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagVerifyTrafficFlow(dut01Obj, dut02Obj, wrkston01Obj,
                                    wrkston02Obj, '140.1.1.10',
                                    '140.1.1.11', ['lnk02', 'lnk03',
                                                   'lnk05', 'lnk06',
                                                   'lnk07', 'lnk08',
                                                   'lnk09', 'lnk10'],
                                    'lnk01', 'lnk04', '140.1.1'))

    def test_try9Links(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 8- Try to create 9 links LAG")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagCreate(dut01Obj, '1', True, [dut01Obj.linkPortMapping[
            'lnk11']], 'off') is False)
        assert(lagCreate(dut02Obj, '1', True, [dut02Obj.linkPortMapping[
            'lnk11']], 'off') is False)
        LogOutput('info', "Lag with 9 links not created as expected")

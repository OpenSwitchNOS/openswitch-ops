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
# Name:        Test_lag_static_ft_supported_and_unsupported_names
#
# Objective:   Check LAG can be created with supported names and can not
#              be created with unsupported ones.
#
# Author:      Pablo Araya M.
#
# Topology:
#              Client 1 <-> OpenSwitch_1
#                                ||  LAG
#              Client 2 <-> OpenSwitch_2
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
from lib_test import lagAddInterface
from lib_test import lagVerifyNumber

topoDict = {"topoExecution": 3000,
            "topoDevices": "dut01 dut02 wrkston01 wrkston02",
            "topoType": "virtual",
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

    dutList = [dut01Obj, dut02Obj]
    for switch in dutList:
        LogOutput('info', "CLEANUP - Rebooting switch: " + switch.device)
        if switchReboot(switch) != 0:
            LogOutput('error', "Failed to reboot Switch")
            finalResult.append(True)
        else:
            LogOutput('info', "Passed Switch 1 Reboot piece")

    for i in finalResult:
        if not i:
            LogOutput('error', 'Errors were detected while cleaning ' +
                      'devices')
            return
    LogOutput('info', "Cleaned up devices")


class Test_lag_static_ft_supported_and_unsupported_names:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_lag_static_ft_supported_and_unsupported_names.testObj = testEnviron(
            topoDict=topoDict)
        Test_lag_static_ft_supported_and_unsupported_names.topoObj =\
            Test_lag_static_ft_supported_and_unsupported_names.testObj.topoObjGet()

    def teardown_class(cls):
        # clean devices
        clean_up_devices(
            cls.topoObj.deviceObjGet(device="dut01"),
            cls.topoObj.deviceObjGet(device="dut02"),
            cls.topoObj.deviceObjGet(device="wrkston01"),
            cls.topoObj.deviceObjGet(device="wrkston02"))
        # Terminate all nodes
        Test_lag_static_ft_supported_and_unsupported_names.topoObj.terminate_nodes()

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
                assert(switchEnableInterface(dut['obj'],
                                             dut['obj'].linkPortMapping[link],
                                             True))

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

    def test_lagConfiguration(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAG configuration was successfully applied")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                           ['lnk02', 'lnk03'], 'lag1', 'lag1'))

    def test_lagTraffic(self):
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
                                    'lnk01', 'lnk04', '140.1.1.0'))

    def test_createExtraLAGs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Create LAGs with supported and unsupported name")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        listNames = [["18", False],
                     ["2000", False],
                     ["theLag01", True],
                     ["0", True],
                     ["-1", True],
                     ["2001", True]]

        for lagTouple in listNames:
            lagName = lagTouple[0]
            expectedFailure = lagTouple[1]

            if expectedFailure:
                assert(not lagCreate(dut01Obj, lagName, True,
                                     [dut01Obj.linkPortMapping['lnk02'],
                                      dut01Obj.linkPortMapping['lnk03']],
                                     'off'))
                assert(not lagCreate(dut02Obj, lagName, True,
                                     [dut01Obj.linkPortMapping['lnk02'],
                                      dut01Obj.linkPortMapping['lnk03']],
                                     'off'))
            else:
                assert(lagCreate(dut01Obj, lagName, True,
                                 [dut01Obj.linkPortMapping['lnk02'],
                                  dut01Obj.linkPortMapping['lnk03']],
                                 'off'))
                assert(lagCreate(dut02Obj, lagName, True,
                                 [dut01Obj.linkPortMapping['lnk02'],
                                  dut01Obj.linkPortMapping['lnk03']],
                                 'off'))

    def test_lagTrafficAgain(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAG traffic on working LAG again")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagVerifyTrafficFlow(dut01Obj, dut02Obj, wrkston01Obj,
                                    wrkston02Obj, '140.1.1.10',
                                    '140.1.1.11', ['lnk02', 'lnk03'],
                                    'lnk01', 'lnk04', '140.1.1.0'))


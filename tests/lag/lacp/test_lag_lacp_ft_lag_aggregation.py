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
# Name:        Test_lag_lacp_ft_lag_aggregation
#
# Objective:   To verify DUT will not activate certain links in a LAG if it
#              detects a different aggregation key from another switch.
#
# Author:      Pablo Araya M.
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
            "topoDevices": "dut01 dut02 dut03 wrkston01 wrkston02 \
                            wrkston03",
            "topoTarget": "dut01 dut02 dut03 dut04",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut01:dut02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut02:wrkston02,\
                          lnk05:dut01:dut03,\
                          lnk06:dut01:dut03,\
                          lnk07:dut03:wrkston03",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation,\
                            wrkston03:system-category:workstation"}


def clean_up_devices(dut01Obj, dut02Obj, dut03Obj,
                     wrkston01Obj, wrkston02Obj, wrkston03Obj):
    LogOutput('info', "\n############################################")
    LogOutput('info', "Device Cleanup - rolling back config")
    LogOutput('info', "############################################")
    finalResult = []

    dutList = [dut01Obj, dut02Obj, dut03Obj]
    wrkstonList = [[wrkston01Obj, "lnk01", "140.1.1.10"],
                   [wrkston02Obj, "lnk04", "140.1.1.11"],
                   [wrkston03Obj, "lnk07", "140.1.1.12"]]

    for switch in dutList:
        LogOutput('info', "CLEANUP - Rebooting switch: " + switch.device)
        if switchReboot(switch) != 0:
            LogOutput('error', "Failed to reboot Switch")
            finalResult.append(True)
        else:
            LogOutput('info', "Passed Switch 1 Reboot piece")

    for toupleWrskton in wrkstonList:
        wrkston = toupleWrskton[0]
        lnk = toupleWrskton[1]
        ip = toupleWrskton[2]
        LogOutput('info', "CLEANUP - Configuring workstation " +
                  wrkston.device + " using link " + lnk + " and IP " + ip)
        finalResult.append(workstationConfigure(wrkston,
                                                wrkston.linkPortMapping[lnk], 
                                                ip, "255.255.255.0", 
                                                "140.1.1.255", True))

    for i in finalResult:
        if not i:
            LogOutput('error', 'Errors were detected while cleaning ' +
                      'devices')
            return
    LogOutput('info', "Cleaned up devices")


class Test_lag_lacp_ft_lag_aggregation:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_lag_lacp_ft_lag_aggregation.testObj = testEnviron(
            topoDict=topoDict)
        Test_lag_lacp_ft_lag_aggregation.topoObj =\
            Test_lag_lacp_ft_lag_aggregation.testObj.topoObjGet()

    def teardown_class(cls):
        # clean devices
        clean_up_devices(
            cls.topoObj.deviceObjGet(device="dut01"),
            cls.topoObj.deviceObjGet(device="dut02"),
            cls.topoObj.deviceObjGet(device="dut03"),
            cls.topoObj.deviceObjGet(device="wrkston01"),
            cls.topoObj.deviceObjGet(device="wrkston02"),
            cls.topoObj.deviceObjGet(device="wrkston03"))
        # Terminate all nodes
        Test_lag_lacp_ft_lag_aggregation.topoObj.terminate_nodes()

    def test_enableDUTsInterfaces(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Enable switches interfaces")
        LogOutput('info', "############################################")

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        dutList = [[dut01Obj, ["lnk01", "lnk02", "lnk03", "lnk05",
                               "lnk06"]],
                   [dut02Obj, ["lnk02", "lnk03", "lnk04"]],
                   [dut03Obj, ["lnk05", "lnk06", "lnk07"]]]

        for dutElement in dutList:
            dutObj = dutElement[0]
            lnkList = dutElement[1]
            for lnk in lnkList:
                LogOutput('info', "Turning on link " +
                          dutObj.linkPortMapping[lnk] +
                          " in switch " + dutObj.device)
                assert(
                    switchEnableInterface(dutObj,
                                          dutObj.linkPortMapping[lnk], True))

    def test_createLAGs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Create LAGs")
        LogOutput('info', "############################################")

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")

        lagList = [[dut01Obj, "1", ["lnk02", "lnk03", "lnk05", "lnk06"]],
                   [dut02Obj, "1", ["lnk02", "lnk03"]],
                   [dut03Obj, "1", ["lnk05", "lnk06"]]]

        dynamic = "active"
        for lagElement in lagList:
            dutObj = lagElement[0]
            lagId = lagElement[1]
            lnkList = lagElement[2]

            assert(lagCreate(dutObj, lagId, True,
                             [dutObj.linkPortMapping[lnk] for lnk in lnkList],
                             dynamic))

    def test_configureVLANs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Configure VLANs on switches")
        LogOutput('info', "############################################")

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        vlanConfigList = [[dut01Obj, "lag 1", "lnk01"],
                          [dut02Obj, "lag 1", "lnk04"],
                          [dut03Obj, "lag 1", "lnk07"]]
        vlanId = 900

        for vlanElement in vlanConfigList:
            dutObj = vlanElement[0]
            lagId = vlanElement[1]
            interface = vlanElement[2]

            LogOutput(
                'info', "Configure VLAN " + str(vlanId)
                + " on switch " + dutObj.device)
            assert(vlanConfigure(dutObj, vlanId, True))
            if interface != "":
                assert(
                    vlanAddInterface(dutObj, vlanId, True,
                                     dutObj.linkPortMapping[interface]))
            assert(vlanAddInterface(dutObj, vlanId, True, lagId))

    def test_configureWorkstations(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Configure workstations")
        LogOutput('info', "############################################")

        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        wrkston03Obj = self.topoObj.deviceObjGet(device="wrkston03")

        wrkstonList = [[wrkston01Obj, "lnk01", "140.1.1.10"],
                       [wrkston02Obj, "lnk04", "140.1.1.11"],
                       [wrkston03Obj, "lnk07", "140.1.1.12"]]

        for wrkstonItem in wrkstonList:
            wrkston = wrkstonItem[0]
            lnk = wrkstonItem[1]
            ip = wrkstonItem[2]
            LogOutput('info', "Configuring workstation " +
                      wrkston.device + " using link " + lnk + " and IP " + ip)
            assert(workstationConfigure(wrkston, wrkston.linkPortMapping[
                   lnk], ip, "255.255.255.0", "140.1.1.255", True))

    def test_lagConfiguration(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAG configuration was successfully applied")
        LogOutput('info', "############################################")

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        wrkston03Obj = self.topoObj.deviceObjGet(device="wrkston03")
        testList = [[dut01Obj, dut02Obj, wrkston01Obj, wrkston02Obj,
                     "140.1.1.10", "140.1.1.11", ["lnk02", "lnk03"],
                     "lnk01", "lnk04", '140.1.1'],
                    [dut01Obj, dut03Obj, wrkston01Obj, wrkston03Obj,
                     "140.1.1.10", "140.1.1.12", ["lnk05", "lnk06"],
                     "lnk01", "lnk07", '140.1.1']]
        lagList = [[dut02Obj, "lag1", ["lnk02", "lnk03"]],
                   [dut03Obj, "lag1", ["lnk05", "lnk06"]]]
        resultList = [False, False]

        LogOutput('info', "First part: Verify LACP status and Flags")
        for index, lagElement in enumerate(lagList):
            dut = lagElement[0]
            lagName = lagElement[1]
            interfaces = lagElement[2]
            LogOutput('info', "Test LAg configuration between " +
                      dut01Obj.device + " and " + dut.device +
                      " for lag name " + lagName)
            resultList[index] = lagVerifyLACPStatusAndFlags(
                dut01Obj, dut, True, interfaces, lagName, lagName,
                dut01LnkCheckNumberMatch=False)

            if resultList[index]:
                LogOutput('info', "Positive result")
            else:
                LogOutput('info', "Negative result")

        LogOutput('info', "Second part: Verify Traffic")
        for index, testItem in enumerate(testList):
            dut1 = testItem[0]
            dut2 = testItem[1]
            wrkston1 = testItem[2]
            wrkston2 = testItem[3]
            ip1 = testItem[4]
            ip2 = testItem[5]
            lagLinks = testItem[6]
            wrkston1Lnk = testItem[7]
            wrkston2Lnk = testItem[8]
            ipPrefix = testItem[9]
            expectedResult = resultList[index]

            LogOutput('info', "Test LAG traffic from " +
                      wrkston1.device + " to " + wrkston2.device)
            result = lagVerifyTrafficFlow(dut1, dut2, wrkston1, wrkston2, ip1,
                                          ip2, lagLinks, wrkston1Lnk,
                                          wrkston2Lnk, ipPrefix)

            if result:
                LogOutput(
                    'info', "Positive result, expected: " + 
                    str(expectedResult))
            else:
                LogOutput(
                    'info', "Negative result, expected: " + 
                    str(expectedResult))

            assert(expectedResult == result)

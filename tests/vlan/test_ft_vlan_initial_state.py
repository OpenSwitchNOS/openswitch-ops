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
# Name:        InitialVlanState.py
#
# Description: Verify the initial state of vlans when they are created
#
# Author:      Roy Ibarra
#
# Topology:      |Switch|
#
# Success Criteria:  PASS -> Vlan 30 is created and shows up with
#                            a status of down in the 'show vlan' output
#
#                    FAILED -> Vlan status is other than down
#
##########################################################################

import pytest
from opstestfw import *
from opstestfw import testEnviron
from opstestfw.switch.CLI import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01",
            "topoDevices": "dut01",
            "topoFilters": "dut01:system-category:switch"}


def deviceCleanup(dut01Obj):
    LogOutput('info', "\n############################################")
    LogOutput('info', "Device Cleanup - rolling back config")
    LogOutput('info', "############################################")
    finalResult = []
    LogOutput('info', "Remove VLAN from DUTs")
    finalResult.append(unconfigureVLAN(dut01Obj, 30))
    for i in finalResult:
        if not i:
            LogOutput('error', "Errors were detected while cleaning devices")
            return
    LogOutput('info', "Cleaned up devices")
    switchReboot(dut01Obj)


def switchReboot(dut01Obj):
    returnCode = 0
    LogOutput('info', "############################################")
    LogOutput('info', "CLEANUP: Reboot the switch")
    LogOutput('info', "############################################")
    rebootRetStruct = dut01Obj.Reboot()
    rebootRetStruct = returnStruct(returnCode=0)
    if rebootRetStruct.returnCode() != 0:
        LogOutput('error', "Switch Reboot failed")
        returnCode = 1
    else:
        LogOutput('info', "Passed Switch Reboot piece")
        # Global cleanup return structure
        cleanupRetStruct = returnStruct(returnCode=returnCode)
        return cleanupRetStruct


# Delete VLAN on switch


def unconfigureVLAN(deviceObj, vlanId):
    LogOutput('debug', "Deleting VLAN " + str(vlanId) +
              " on device " + deviceObj.device)
    retStruct = AddVlan(deviceObj=deviceObj, vlanId=vlanId,
                        config=False)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to delete VLAN " +
                  str(vlanId) + " on device " + deviceObj.device)
        return False
    else:
        LogOutput('info', "Deleted VLAN " + str(vlanId) + " on device " +
                  deviceObj.device)
    return True


class Test_InitialVlanStateTC:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_InitialVlanStateTC.testObj = testEnviron(topoDict=topoDict)
        Test_InitialVlanStateTC.topoObj = \
            Test_InitialVlanStateTC.testObj.topoObjGet()
        Test_InitialVlanStateTC.dut01Obj = \
            Test_InitialVlanStateTC.topoObj.deviceObjGet(
                device="dut01")

    def teardown_class(cls):
        # Terminate all nodes
        deviceCleanup(cls.dut01Obj)
        Test_InitialVlanStateTC.topoObj.terminate_nodes()

    def test_vlan_add(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 1- Create Vlan")
        LogOutput('info', "############################################")

        devRetStruct = AddVlan(deviceObj=self.dut01Obj, vlanId=30)
        if devRetStruct.returnCode() != 0:
            LogOutput('info', "Failed to add Vlan with ID 30")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan with ID 30 added to the switch")

    def test_check_vlan_status(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 2- Check Vlan status")
        LogOutput('info', "############################################")
        returnCLS = ShowVlan(deviceObj=self.dut01Obj)
        # Get the list containing the output of 'show vlan'. Each position in
        # the list is a dictionary that corresponds to a row of the 'show vlan'
        showVlanOutput = returnCLS.valueGet()
        if len(showVlanOutput) == 0 or \
                len(showVlanOutput) > 1:
            LogOutput(
                'error', "Zero or more than one vlan \
                have been created on the switch")
            assert 1 != 1
        else:
            myDict = showVlanOutput[0]
            if myDict['Status'] != "down":
                LogOutput(
                    'error', "Step failed. Vlan status is other than down")
                assert myDict['Status'] == "down"
            else:
                LogOutput(
                    'info', "Passed - Vlan with ID 30 has a status of down")

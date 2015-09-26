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
# Name:        VlanNoPortMember.py
#
# Description: Create three different vlans and set admin state 'up' for one
#            of them. Verify the state is admin_down for two vlans and
#            no_member_port for one of them.
#
# Author:      Roy Ibarra
#
# Topology:      |Switch|
#
# Success Criteria:  PASS -> Vlan 30,40 and 50 are created. Only one vlan
#                    shows up with a status and reason of down and
#                    no_member_port as per the 'show vlan' output.
#
#                    FAILED -> Vlan status or reason is other than down
#                              and no_member_port.
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


class Test_VlanNoMemberPortTC:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_VlanNoMemberPortTC.testObj = testEnviron(topoDict=topoDict)
        Test_VlanNoMemberPortTC.topoObj = \
            Test_VlanNoMemberPortTC.testObj.topoObjGet()
        Test_VlanNoMemberPortTC.dut01Obj = \
            Test_VlanNoMemberPortTC.topoObj.deviceObjGet(device="dut01")

    def teardown_class(cls):
        # Terminate all nodes
        deviceCleanup(cls.dut01Obj)
        Test_VlanNoMemberPortTC.topoObj.terminate_nodes()

    def test_vlan_add(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 1- Create Vlan 30, 40 and 50")
        LogOutput('info', "############################################")

        devRetStruct = AddVlan(deviceObj=self.dut01Obj, vlanId=30)
        if devRetStruct.returnCode() != 0:
            LogOutput('info', "Failed to add Vlan with ID 30")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan with ID 30 added to the switch")

        devRetStruct = AddVlan(deviceObj=self.dut01Obj, vlanId=40)
        if devRetStruct.returnCode() != 0:
            LogOutput('info', "Failed to add Vlan with ID 40")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan with ID 40 added to the switch")

        devRetStruct = AddVlan(deviceObj=self.dut01Obj, vlanId=50)
        if devRetStruct.returnCode() != 0:
            LogOutput('info', "Failed to add Vlan with ID 50")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan with ID 50 added to the switch")

    def test_vlan_state(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 2- Set vlan 50 to admin state up")
        LogOutput('info', "############################################")
        # Add port 1 in mode access
        devRetStruct = VlanStatus(
            deviceObj=self.dut01Obj, vlanId=50, status=True)
        if devRetStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed when entering the command 'no shutdown'")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan 50 was configured \
            with the 'no shutdown' command")

    def test_check_vlan_status(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 3- Check Vlan status")
        LogOutput('info', "############################################")
        returnCLS = ShowVlan(deviceObj=self.dut01Obj)
        # Get the list containing the output of 'show vlan'. Each position in
        # the list is a dictionary that corresponds to a row of the 'show vlan'
        showVlanOutput = returnCLS.valueGet()
        if len(showVlanOutput) == 0 or len(showVlanOutput) > 3:
            LogOutput(
                'error', "Zero or more than 3 vlans \
                have been created on the switch")
            assert 1 != 1
        else:
            for myDictionary in showVlanOutput:
                if myDictionary['VLAN'] == "30" and \
                        (myDictionary['Status'] != "down" or
                         myDictionary['Reason'] != "admin_down"):
                    LogOutput(
                        'error', "Step failed. Vlan 30 status or reason \
                        value is other than down and admin_down")
                    assert 1 != 1
                if myDictionary['VLAN'] == "40" and \
                        (myDictionary['Status'] != "down" or
                         myDictionary['Reason'] != "admin_down"):
                    LogOutput(
                        'error', "Step failed. Vlan 40 status or reason value\
                         is other than down and admin_down")
                    assert 1 != 1
                if myDictionary['VLAN'] == "50" and \
                        (myDictionary['Status'] != "down" or
                         myDictionary['Reason'] != "no_member_port"):
                    LogOutput(
                        'error', "Step failed. Vlan 50 status or reason value\
                         is other than down and no_member_port")
                    assert 1 != 1

            LogOutput(
                'info', "Passed - All vlans have the correct \
                Status and Reason values")

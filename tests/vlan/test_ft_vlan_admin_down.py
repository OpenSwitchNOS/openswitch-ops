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
# Name:        VlanAdminDown.py
#
# Description: Verify the state of a vlan is admin_down if ports have
#     been assigned to the respective vlan but vlan has not been set to up.
#
# Author:      Roy Ibarra
#
# Topology:      |Switch|
#
# Success Criteria:  PASS -> Vlan 30 is created with ports assigned to it and
#           shows up with a status of admin_down as per the 'show vlan' output
#
#                    FAILED -> Vlan status or reason is other than admin_down
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

    LogOutput('info', "Disable interface on DUT")
    finalResult.append(disableDutInterface(dut01Obj, "1"))
    LogOutput('info', "Remove VLAN from DUTs")
    finalResult.append(unconfigureVLAN(dut01Obj, 30))
    finalResult.append(unconfigureVLAN(dut01Obj, 40))
    finalResult.append(unconfigureVLAN(dut01Obj, 50))
    for i in finalResult:
        if not i:
            LogOutput('error', "Errors were detected while cleaning devices")
            return
    LogOutput('info', "Cleaned up devices")
    switchReboot(dut01Obj)


def disableDutInterface(deviceObj, int):
    retStruct = InterfaceEnable(deviceObj=deviceObj,
                                enable=False, interface=int)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to disable " + deviceObj.device +
                  " interface " + int)
        return False
    else:
        LogOutput('info', "Disabled "
                  + deviceObj.device + " interface " + int)
    return True


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


def verifyVlanPorts(dut, vlanID, port):
    assigned = False
    returnCLS = ShowVlan(deviceObj=dut)
    showVlanOutput = returnCLS.valueGet()
    for myDictionary in showVlanOutput:
        if myDictionary['VLAN'] == vlanID and \
                port in myDictionary['Ports']:
            assigned = True
            return assigned
    return assigned

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


class Test_VlanAdminDownTC:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_VlanAdminDownTC.testObj = testEnviron(topoDict=topoDict)
        Test_VlanAdminDownTC.topoObj = \
            Test_VlanAdminDownTC.testObj.topoObjGet()
        Test_VlanAdminDownTC.dut01Obj = \
            Test_VlanAdminDownTC.topoObj.deviceObjGet(device="dut01")

    def teardown_class(cls):
        # Terminate all nodes
        deviceCleanup(cls.dut01Obj)
        Test_VlanAdminDownTC.topoObj.terminate_nodes()

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

        # Verify vlans were created
        returnCLS = ShowVlan(deviceObj=self.dut01Obj)
        showVlanOutput = returnCLS.valueGet()
        if len(showVlanOutput) == 0 or len(showVlanOutput) > 3:
            LogOutput('error', "Zero or more than 3 VLAN "
                      + "have been created on DUT01")
            assert 1 != 1
        else:
            for myDictionary in showVlanOutput:
                if myDictionary['VLAN'] not in ["30", "40", "50"]:
                    LogOutput('error', "Step failed. Vlan "
                              + myDictionary['VLAN']
                              + " does not exist in the VLAN table on DUT01")
                    assert 1 != 1
            LogOutput('info', "Passed - All vlans exist "
                      + "in the VLAN table on DUT01")

    def test_vlan_ports(self):
        LogOutput('info', "############################################")
        LogOutput(
            'info', "Step 2- Assign ports 1 and 2 to vlan 30 as access ports")
        LogOutput('info', "############################################")
        # Add port 1 in mode access
        devRetStruct = AddPortToVlan(
            deviceObj=self.dut01Obj, vlanId=30, interface=1,
            access=True, allowed=False, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput(
                'info', "Failed to configure port 1 as access port on vlan 30")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput(
                'info', "Passed - Port 1 was configure " +
                "with mode access on vlan 30")
        # Add port 2 in mode access
        devRetStruct = AddPortToVlan(
            deviceObj=self.dut01Obj, vlanId=30, interface=2,
            access=True, allowed=False, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput(
                'info', "Failed to configure port 2 " +
                "as access port on vlan 30")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput(
                'info', "Passed - Port 2 was configure " +
                "with mode access on vlan 30")

        # verify ports are assigned to the respective vlan
        if verifyVlanPorts(self.dut01Obj, "30", "1"):
            LogOutput('info', "Passed - Added port 1 to vlan 30")
        else:
            LogOutput('error', "Failed to add port 1 to vlan 30")
            assert(False)
        if verifyVlanPorts(self.dut01Obj, "30", "2"):
            LogOutput('info', "Passed - Added port 2 to vlan 30")
        else:
            LogOutput('error', "Failed to add port 2 to vlan 30")
            assert(False)

    def test_set_interfaces_up(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 3- Set interfaces to UP state")
        LogOutput('info', "############################################")
        devRetStruct = InterfaceEnable(deviceObj=self.dut01Obj,
                                       enable=True, interface="1")
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to set interface 1 to UP\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "DUT01 interface 1 set to up\n")

        devRetStruct = InterfaceEnable(deviceObj=self.dut01Obj,
                                       enable=True, interface="2")
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to set interface 2 to up")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "DUT01 interface 2 set to up\n")

    def test_check_vlan_status(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 4- Check Vlan status")
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
                if myDictionary['VLAN'] not in ["30", "40", "50"] \
                        or myDictionary['Status'] != "down" \
                        or myDictionary['Reason'] != "admin_down":
                    LogOutput(
                        'error', "Step failed. Vlan status or " +
                        "reason value is other than down")
                    assert 1 != 1
            LogOutput(
                'info', "Passed - All vlans have the " +
                " correct Status and Reason values")

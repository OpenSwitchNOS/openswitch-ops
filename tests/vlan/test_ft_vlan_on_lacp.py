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
# Name:        test_vlan_on_LACP.py
#
# Description: Verify that a switch (port aggregation) trunk's ability to have
#              multiple VLAN's on it with all VLAN's tagged. Port Aggregation
#              methods shall include the following: LACP.
#              Tagged ports on all Vlan's for link between switches.
#              Untagged between clients on each switch
#
# Author:      Roy Ibarra
#
# Topology:   |2 wrkstons|----|Switch|==(LACP/Trunk)=|Switch|----|2 wrkstons|
#
# Success Criteria:  PASS -> Connectivity exists in all Vlans in the system.
#
#                    Failed -> Connectivity Failed.
#
##########################################################################

import pytest
from opstestfw import *
from opstestfw import testEnviron
from opstestfw.switch.CLI import *

# Topology definition
topoDict = {"topoExecution": 3000,
            "topoDevices": "dut01 dut02 wrkston01 wrkston02 \
            " + "wrkston03 wrkston04",
            "topoLinks": "lnk01:dut01:wrkston01,lnk02:dut01:wrkston02,\
            " + " lnk03:dut01:dut02,lnk04:dut01:dut02,lnk05:dut02:wrkston03,\
            " + "lnk06:dut02:wrkston04",
            "topoFilters": "dut01:system-category:switch,\
            " + "dut02:system-category:switch,\
            " + "wrkston01:system-category:workstation,\
            " + "wrkston02:system-category:workstation,\
            " + "wrkston03:system-category:workstation,\
            " + "wrkston04:system-category:workstation"}

# Clean up devices


def clean_up_devices(dut01Obj, dut02Obj, wrkston01Obj, wrkston02Obj,
                     wrkston03Obj, wrkston04Obj):
    LogOutput('info', "\n############################################")
    LogOutput('info', "Device Cleanup - rolling back config")
    LogOutput('info', "############################################")
    finalResult = []

    LogOutput('info', "Unconfigure workstations")
    LogOutput('info', "Unconfiguring workstation 1")
    finalResult.append(unConfigureWorkstation(
        wrkston01Obj,
        wrkston01Obj.linkPortMapping['lnk01'], "192.168.30.10",
        "255.255.255.0", "192.168.30.255"))
    LogOutput('info', "Unconfiguring workstation 2")
    finalResult.append(unConfigureWorkstation(
        wrkston02Obj,
        wrkston02Obj.linkPortMapping['lnk02'], "192.168.40.10",
        "255.255.255.0", "192.168.40.255"))
    LogOutput('info', "Unconfiguring workstation 3")
    finalResult.append(unConfigureWorkstation(
        wrkston03Obj,
        wrkston03Obj.linkPortMapping['lnk05'], "192.168.30.11",
        "255.255.255.0", "192.168.30.255"))
    LogOutput('info', "Unconfiguring workstation 4")
    finalResult.append(unConfigureWorkstation(
        wrkston04Obj,
        wrkston04Obj.linkPortMapping['lnk06'], "192.168.40.11",
        "255.255.255.0", "192.168.40.255"))

    LogOutput('info', "Delete LAGs on DUTs")
    finalResult.append(deleteLAG(dut01Obj, '100', [], 'off'))
    finalResult.append(deleteLAG(dut02Obj, '100', [], 'off'))

    LogOutput('info', "Disable interfaces on DUTs")
    LogOutput('info', "Configuring switch dut01")
    finalResult.append(
        disableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk01']))
    finalResult.append(
        disableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk02']))
    finalResult.append(
        disableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk03']))
    finalResult.append(
        disableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk04']))

    LogOutput('info', "Configuring switch dut02")
    finalResult.append(
        disableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03']))
    finalResult.append(
        disableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk04']))
    finalResult.append(
        disableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk05']))
    finalResult.append(
        disableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk06']))
    LogOutput('info', "Remove VLAN from DUTs")
    finalResult.append(unconfigureVLAN(dut01Obj, 30))
    finalResult.append(unconfigureVLAN(dut01Obj, 40))
    finalResult.append(unconfigureVLAN(dut01Obj, 50))
    finalResult.append(unconfigureVLAN(dut02Obj, 30))
    finalResult.append(unconfigureVLAN(dut02Obj, 40))
    finalResult.append(unconfigureVLAN(dut02Obj, 50))

    for i in finalResult:
        if not i:
            LogOutput('error', "Errors were detected while cleaning \
                    devices")
            return
    LogOutput('info', "Cleaned up devices")


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

# Unconfigure the IP address of a workstation


def unConfigureWorkstation(deviceObj, int, ipAddr, netMask, broadcast):
    retStruct = deviceObj.NetworkConfig(ipAddr=ipAddr,
                                        netMask=netMask,
                                        broadcast=broadcast,
                                        interface=int, configFlag=False)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to unconfigure IP on workstation " +
                  deviceObj.device)
        return False
    cmdOut = deviceObj.cmd("ifconfig " + int)
    LogOutput('info', "Ifconfig info for workstation " +
              deviceObj.device + ":\n" + cmdOut)
    return True

# Delete LAG interface


def deleteLAG(deviceObj, lagId, intArray, mode):
    retStruct = lagCreation(deviceObj=deviceObj,
                            lagId=str(lagId), configFlag=False)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to delete LAG1 on " + deviceObj.device)
        return False
    else:
        LogOutput('info', "Deleted LAG" +
                  str(lagId) + " on " + deviceObj.device)
        retStruct = lacpAggregatesShow(deviceObj=deviceObj)
        if len(retStruct.dataKeys()) != 0:
            if retStruct.valueGet(key=str(lagId)) is not None:
                LogOutput('error',
                          "The LAG was not deleted from configuration")
                return False
    return True

# Disable interface on DUT


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

# Verify a port has been assigned to a vlan


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


class Test_VlanOnLACP:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_VlanOnLACP.testObj = testEnviron(topoDict=topoDict)
        Test_VlanOnLACP.topoObj = Test_VlanOnLACP.testObj.topoObjGet()
        Test_VlanOnLACP.dut01Obj = Test_VlanOnLACP.topoObj.deviceObjGet(
            device="dut01")
        Test_VlanOnLACP.dut02Obj = Test_VlanOnLACP.topoObj.deviceObjGet(
            device="dut02")
        Test_VlanOnLACP.wrkston01Obj = Test_VlanOnLACP.topoObj.deviceObjGet(
            device="wrkston01")
        Test_VlanOnLACP.wrkston02Obj = Test_VlanOnLACP.topoObj.deviceObjGet(
            device="wrkston02")
        Test_VlanOnLACP.wrkston03Obj = Test_VlanOnLACP.topoObj.deviceObjGet(
            device="wrkston03")
        Test_VlanOnLACP.wrkston04Obj = Test_VlanOnLACP.topoObj.deviceObjGet(
            device="wrkston04")

    def teardown_class(cls):
        # clean devices
        '''clean_up_devices(
            cls.topoObj.deviceObjGet(device="dut01"),
            cls.topoObj.deviceObjGet(device="dut02"),
            cls.topoObj.deviceObjGet(device="wrkston01"),
            cls.topoObj.deviceObjGet(device="wrkston02"),
            cls.topoObj.deviceObjGet(device="wrkston03"),
            cls.topoObj.deviceObjGet(device="wrkston04"),)'''
        # Terminate all nodes
        Test_VlanOnLACP.topoObj.terminate_nodes()

    def test_initialize_clients(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 1- Configure workstations")
        LogOutput('info', "############################################")

        LogOutput('info', "\nConfiguring Host A IP Address")
        devRetStruct = self.wrkston01Obj.NetworkConfig(
            ipAddr="192.168.30.10",
            netMask="255.255.255.0",
            broadcast="192.168.30.255",
            interface=self.wrkston01Obj.linkPortMapping['lnk01'],
            config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Host A: cannot set IP Address\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Host A has been configured"
                      + " with an IP Address")

        LogOutput('info', "\nConfiguring Host B IP Address")
        devRetStruct = self.wrkston02Obj.NetworkConfig(
            ipAddr="192.168.40.10",
            netMask="255.255.255.0",
            broadcast="192.168.40.255",
            interface=self.wrkston02Obj.linkPortMapping['lnk02'],
            config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Host B: cannot set IP Address\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Host B has been configured"
                      + "  with an IP Address")

        LogOutput('info', "\nConfiguring Host C IP Address")
        devRetStruct = self.wrkston03Obj.NetworkConfig(
            ipAddr="192.168.30.11",
            netMask="255.255.255.0",
            broadcast="192.168.30.255",
            interface=self.wrkston03Obj.linkPortMapping['lnk05'],
            config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Host C: cannot set IP Address\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Host C has been configured"
                      + " with an IP Address")

        LogOutput('info', "\nConfiguring Host D IP Address")
        devRetStruct = self.wrkston04Obj.NetworkConfig(
            ipAddr="192.168.40.11",
            netMask="255.255.255.0",
            broadcast="192.168.40.255",
            interface=self.wrkston04Obj.linkPortMapping['lnk06'],
            config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Host D: cannot set IP Address\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Host D has been configured"
                      + " with an IP Address")

    def test_vlan_add_Dut01(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 2- Create Vlan 30, 40 and 50 on DUT01")
        LogOutput('info', "############################################")

        devRetStruct = AddVlan(deviceObj=self.dut01Obj, vlanId=30)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to add Vlan with ID 30 on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan with ID 30 added to DUT01")

        devRetStruct = AddVlan(deviceObj=self.dut01Obj, vlanId=40)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to add Vlan with ID 40 on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan with ID 40 added to DUT01")

        devRetStruct = AddVlan(deviceObj=self.dut01Obj, vlanId=50)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to add Vlan with ID 50 on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan with ID 50 added to DUT01")

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
                    LogOutput('error', "Step failed. Vlan " + myDictionary['VLAN']
                              + " does not exist in the VLAN table on DUT01")
                    assert 1 != 1
            LogOutput('info', "Passed - All vlans exist "
                      + "in the VLAN table on DUT01")

    def test_vlan_add_Dut02(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 3- Create Vlan 30, 40 and 50 on DUT02")
        LogOutput('info', "############################################")

        devRetStruct = AddVlan(deviceObj=self.dut02Obj, vlanId=30)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to add Vlan with ID 30 on DUT02")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan with ID 30 added to DUT02")

        devRetStruct = AddVlan(deviceObj=self.dut02Obj, vlanId=40)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to add Vlan with ID 40 on DUT02")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan with ID 40 added to DUT02")

        devRetStruct = AddVlan(deviceObj=self.dut02Obj, vlanId=50)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to add Vlan with ID 50 on DUT02")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan with ID 50 added to DUT02")

         # Verify vlans were created
        returnCLS = ShowVlan(deviceObj=self.dut02Obj)
        showVlanOutput = returnCLS.valueGet()
        if len(showVlanOutput) == 0 or len(showVlanOutput) > 3:
            LogOutput('error', "Zero or more than 3 VLAN "
                      + "have been created on DUT02")
            assert 1 != 1
        else:
            for myDictionary in showVlanOutput:
                if myDictionary['VLAN'] not in ["30", "40", "50"]:
                    LogOutput('error', "Step failed. Vlan " + myDictionary['VLAN']
                              + " does not exist in the VLAN table on DUT02")
                    assert 1 != 1
            LogOutput('info', "Passed - All vlans exist "
                      + "in the VLAN table on DUT02")

    def test_vlan_state_Dut01(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 4- Set all vlans on DUT01 to admin state up")
        LogOutput('info', "############################################")
        # Vlan 30
        devRetStruct = VlanStatus(
            deviceObj=self.dut01Obj, vlanId=30, status=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed when entering the command"
                      + " 'no shutdown for vlan 30'")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan 30 was configured"
                      + " with the 'no shutdown' command")
        # Vlan 40
        devRetStruct = VlanStatus(
            deviceObj=self.dut01Obj, vlanId=40, status=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed when entering the command"
                      + " 'no shutdown for vlan 40'")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan 40 was configured with"
                      + " the 'no shutdown' command")
        # Vlan 50
        devRetStruct = VlanStatus(
            deviceObj=self.dut01Obj, vlanId=50, status=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed when entering the command"
                      + " 'no shutdown for vlan 50'")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan 50 was configured with"
                      + " the 'no shutdown' command")

    def test_vlan_state_Dut02(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 5- Set all vlans on DUT02 to admin state up")
        LogOutput('info', "############################################")
        # Vlan 30
        devRetStruct = VlanStatus(
            deviceObj=self.dut02Obj, vlanId=30, status=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed when entering the command"
                      + " 'no shutdown' for vlan 30")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan 30 was configured"
                      + " with the 'no shutdown' command")
        # Vlan 40
        devRetStruct = VlanStatus(
            deviceObj=self.dut02Obj, vlanId=40, status=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed when entering the command"
                      + " 'no shutdown for vlan 40'")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan 40 was configured"
                      + " with the 'no shutdown' command")
        # Vlan 50
        devRetStruct = VlanStatus(
            deviceObj=self.dut02Obj, vlanId=50, status=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed when entering the command"
                      + " 'no shutdown for vlan 50'")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan 50 was configured with"
                      + " the 'no shutdown' command")

    def test_vlan_ports_Dut01(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 6- Assign one port to vlan 30 & 40"
                  + " as access ports on DUT01")
        LogOutput('info', "############################################")
        # Add one port in mode access
        interface1 = self.dut01Obj.linkPortMapping['lnk01']
        devRetStruct = AddPortToVlan(deviceObj=self.dut01Obj, vlanId=30,
                                     interface=interface1, access=True,
                                     allowed=False, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure port "
                      + str(interface1) + " as access port on vlan 30")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Port "
                      + str(interface1)
                      + " was configured with mode access on vlan 30")
        # Add a second port in mode access
        interface2 = self.dut01Obj.linkPortMapping['lnk02']
        devRetStruct = AddPortToVlan(deviceObj=self.dut01Obj, vlanId=40,
                                     interface=interface2, access=True,
                                     allowed=False, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure port "
                      + str(interface2) + " as access port on vlan 40")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Port " + str(interface2)
                      + " was configured with mode access on vlan 40")

        # Verify vlan state
        returnCLS = ShowVlan(deviceObj=self.dut01Obj)
        showVlanOutput = returnCLS.valueGet()
        for myDictionary in showVlanOutput:
            if myDictionary['VLAN'] == "50" \
                and (myDictionary['Status'] != "down"
                     or myDictionary['Reason'] != "no_member_port"):
                LogOutput('error', "Step failed. Vlan 50 has a Status or "
                          + "Reason value is other than down"
                          + " and no_member_port")
                assert 1 != 1
            elif myDictionary['VLAN'] in ["30", "40"] \
                and (myDictionary['Status'] != "up"
                     or myDictionary['Reason'] != "ok"):
                LogOutput('error', "Step failed. Vlan 30 or 40 has an"
                          + " incorrect Status or Reason value")
                assert 1 != 1
        LogOutput('info', "Passed - All vlans have the "
                  + "correct Status and Reason values")

        # verify ports are assigned to the respective vlan
        if verifyVlanPorts(self.dut01Obj, "30", interface1):
            LogOutput(
                'info', "Passed added port " + interface1 + " to vlan 30")
        else:
            LogOutput(
                'error', "Failed to add port " + interface1 + " to vlan 30")
            assert(False)
        if verifyVlanPorts(self.dut01Obj, "40", interface2):
            LogOutput(
                'info', "Passed added port " + interface2 + " to vlan 40")
        else:
            LogOutput(
                'error', "Failed to add port " + interface2 + " to vlan 40")
            assert(False)

    def test_vlan_ports_Dut02(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 7- Assign one port to vlan 30 & 40"
                  + " as access ports on DUT02")
        LogOutput('info', "############################################")
        # Add one port in mode access
        interface1 = self.dut02Obj.linkPortMapping['lnk05']
        devRetStruct = AddPortToVlan(deviceObj=self.dut02Obj, vlanId=30,
                                     interface=interface1, access=True,
                                     allowed=False, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure port "
                      + str(interface1) + " as access port on vlan 30")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Port "
                      + str(interface1)
                      + " was configured with mode access on vlan 30")
        # Add a second port in mode access
        interface2 = self.dut02Obj.linkPortMapping['lnk06']
        devRetStruct = AddPortToVlan(deviceObj=self.dut02Obj, vlanId=40,
                                     interface=interface2, access=True,
                                     allowed=False, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure port "
                      + str(interface2) + " as access port on vlan 40")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Port " + str(interface2)
                      + " was configured with mode access on vlan 40")

        # Verify vlan state
        returnCLS = ShowVlan(deviceObj=self.dut02Obj)
        showVlanOutput = returnCLS.valueGet()
        for myDictionary in showVlanOutput:
            if myDictionary['VLAN'] == "50" \
                and (myDictionary['Status'] != "down"
                     or myDictionary['Reason'] != "no_member_port"):
                LogOutput('error', "Step failed. Vlan 50 has a Status or "
                          + "Reason value is other than down"
                          + " and no_member_port")
                assert 1 != 1
            elif myDictionary['VLAN'] in ["30", "40"] \
                and (myDictionary['Status'] != "up"
                     or myDictionary['Reason'] != "ok"):
                LogOutput('error', "Step failed. Vlan 30 or 40 has an"
                          + " incorrect Status or Reason value")
                assert 1 != 1

        LogOutput('info', "Passed - All vlans have the "
                  + "correct Status and Reason values")

        # verify ports are assigned to the respective vlan
        if verifyVlanPorts(self.dut02Obj, "30", interface1):
            LogOutput(
                'info', "Passed added port " + interface1 + " to vlan 30")
        else:
            LogOutput(
                'error', "Failed to add port " + interface1 + " to vlan 30")
            assert(False)
        if verifyVlanPorts(self.dut02Obj, "40", interface2):
            LogOutput(
                'info', "Passed added port " + interface2 + " to vlan 40")
        else:
            LogOutput(
                'error', "Failed to add port " + interface2 + " to vlan 40")
            assert(False)

    def test_create_LAG(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 8- Create LAG on DUT01 and DUT02")
        LogOutput('info', "############################################")
        # Configure LAG on DUT01
        devRetStruct = lagCreation(
            deviceObj=self.dut01Obj, lagId=100, configFlag=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure LAG interface on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - LAG 100 was configured on DUT01")
        # Configure LAG on DUT02
        devRetStruct = lagCreation(
            deviceObj=self.dut02Obj, lagId=100, configFlag=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure LAG interface on DUT02")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - LAG 100 was configured on DUT02")

    def test_assign_ports_to_LAG(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 9- Assign two ports to LAG on each DUT")
        LogOutput('info', "############################################")
        # Assign first port to LAG on DUT01
        interface = self.dut01Obj.linkPortMapping['lnk03']
        devRetStruct = InterfaceLagIdConfig(
            deviceObj=self.dut01Obj, interface=interface, lagId=100)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to add port " +
                      str(interface) + " to LAG interface on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Port " + str(interface) +
                      " added to LAG interface on DUT01")
        # Assign second port to LAG on DUT01
        interface = self.dut01Obj.linkPortMapping['lnk04']
        devRetStruct = InterfaceLagIdConfig(
            deviceObj=self.dut01Obj, interface=interface, lagId=100)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to add port " +
                      str(interface) + " to LAG interface on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Port " + str(interface) +
                      " added to LAG interface on DUT01")
        # Assign first port to LAG on DUT02
        interface = self.dut02Obj.linkPortMapping['lnk03']
        devRetStruct = InterfaceLagIdConfig(
            deviceObj=self.dut02Obj, interface=interface, lagId=100)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to add port " +
                      str(interface) + " to LAG interface on DUT02")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Port " + str(interface) +
                      " added to LAG interface on DUT02")
        # Assign second Port to LAG on DUT02
        interface = self.dut02Obj.linkPortMapping['lnk04']
        devRetStruct = InterfaceLagIdConfig(
            deviceObj=self.dut02Obj, interface=interface, lagId=100)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to add port " +
                      str(interface) + " to LAG interface on DUT02")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Port " + str(interface) +
                      " added to LAG interface on DUT02")

    def test_configure_LACP(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 10- Configure LACP on DUT01 and DUT02")
        LogOutput('info', "############################################")
        # Configure LACP on DUT01
        devRetStruct = lagMode(
            deviceObj=self.dut01Obj, lagId=100, lacpMode="off")
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure LACP on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - LACP was configured on DUT01")
        # Configure LACP on DUT02
        devRetStruct = lagMode(
            deviceObj=self.dut02Obj, lagId=100, lacpMode="off")
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure LACP on DUT02")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - LACP was configured on DUT02")

    def test_vlan_trunk_Dut01(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 11- Add VLANs to the list of allowed"
                  + " VLANs on interface LAG trunk port on DUT01")
        LogOutput('info', "############################################")
        # Adding vlan 30 to the allow list in trunk link
        devRetStruct = AddPortToVlan(deviceObj=self.dut01Obj, vlanId=30,
                                     interface="lag 100", access=False,
                                     allowed=True, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure the allowed"
                      + " VLAN 30 in trunk link interface"
                      + " LAG 100 on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - VLAN 30 allowed in trunk"
                      + " link interface LAG 100 on DUT01")
        # Adding vlan 40 to the allow list in trunk link
        devRetStruct = AddPortToVlan(deviceObj=self.dut01Obj, vlanId=40,
                                     interface="lag 100", access=False,
                                     allowed=True, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure the allowed"
                      + " VLAN 40 in trunk link interface"
                      + " LAG 100 on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - VLAN 40 allowed in trunk link"
                      + " interface LAG 100 on DUT01")
        # Adding vlan 50 to the allow list in trunk link
        devRetStruct = AddPortToVlan(deviceObj=self.dut01Obj, vlanId=50,
                                     interface="lag 100", access=False,
                                     allowed=True, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure the allowed"
                      + " VLAN 50 in trunk link interface"
                      + " LAG 100 on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - VLAN 50 allowed in trunk link"
                      + " interface LAG 100 on DUT01")

         # Verify ports have been assigned to vlans
        interface1 = self.dut01Obj.linkPortMapping['lnk01']
        interface2 = self.dut01Obj.linkPortMapping['lnk02']
        returnCLS = ShowVlan(deviceObj=self.dut01Obj)
        showVlanOutput = returnCLS.valueGet()
        for myDictionary in showVlanOutput:
            if myDictionary['VLAN'] == "30" and \
                (interface1 not in myDictionary['Ports']
                 or "lag100" not in myDictionary['Ports']):
                LogOutput('error', "Step failed. Vlan 30 doesn't have"
                          + " the correct ports assigned")
                assert 1 != 1
            elif myDictionary['VLAN'] == "40" and \
                (interface2 not in myDictionary['Ports']
                 or "lag100" not in myDictionary['Ports']):
                LogOutput('error', "Step failed. Vlan 40 doesn't have"
                          + " the correct ports assigned")
                assert 1 != 1

        LogOutput('info', "Passed - All vlans have the "
                  + "correct ports assigned")

    def test_vlan_trunk_Dut02(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 12- Add VLANs to the list of allowed"
                  + " VLANs on interface LAG trunk port on DUT02")
        LogOutput('info', "############################################")
        # Adding vlan 30 to the allow list in trunk link
        devRetStruct = AddPortToVlan(deviceObj=self.dut02Obj, vlanId=30,
                                     interface="lag 100", access=False,
                                     allowed=True, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure the allowed"
                      + " VLAN 30 in trunk link interface"
                      + " LAG 100 on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - VLAN 30 allowed in trunk"
                      + " link interface LAG 100 on DUT01")
        # Adding vlan 40 to the allow list in trunk link
        devRetStruct = AddPortToVlan(deviceObj=self.dut02Obj, vlanId=40,
                                     interface="lag 100", access=False,
                                     allowed=True, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure the allowed"
                      + " VLAN 40 in trunk link interface"
                      + " LAG 100 on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - VLAN 40 allowed in trunk link"
                      + " interface LAG 100 on DUT01")
        # Adding vlan 50 to the allow list in trunk link
        devRetStruct = AddPortToVlan(deviceObj=self.dut02Obj, vlanId=50,
                                     interface="lag 100", access=False,
                                     allowed=True, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure the allowed"
                      + " VLAN 50 in trunk link interface"
                      + " LAG 100 on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput(
                'info', "Passed - VLAN 50 allowed in trunk link"
                + " interface LAG 100 on DUT01")

         # Verify ports have been assigned to vlans
        interface1 = self.dut02Obj.linkPortMapping['lnk05']
        interface2 = self.dut02Obj.linkPortMapping['lnk06']
        returnCLS = ShowVlan(deviceObj=self.dut02Obj)
        showVlanOutput = returnCLS.valueGet()
        for myDictionary in showVlanOutput:
            if myDictionary['VLAN'] == "30" and \
                (interface1 not in myDictionary['Ports']
                 or "lag100" not in myDictionary['Ports']):
                LogOutput('error', "Step failed. Vlan 30 doesn't have"
                          + " the correct ports assigned")
                assert 1 != 1
            elif myDictionary['VLAN'] == "40" and \
                (interface2 not in myDictionary['Ports']
                 or "lag100" not in myDictionary['Ports']):
                LogOutput('error', "Step failed. Vlan 40 doesn't have"
                          + " the correct ports assigned")
                assert 1 != 1

        LogOutput('info', "Passed - All vlans have the "
                  + "correct ports assigned")

    def test_set_interfaces_up(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 13- Bring interfaces"
                  + " to UP state on both DUTs")
        LogOutput('info', "############################################")
        interface = self.dut01Obj.linkPortMapping['lnk01']
        devRetStruct = InterfaceEnable(deviceObj=self.dut01Obj,
                                       enable=True, interface=interface)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to bring interface " +
                      str(interface) + " to UP on DUT01\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "DUT01 interface "
                      + str(interface) + " is up\n")

        interface = self.dut01Obj.linkPortMapping['lnk02']
        devRetStruct = InterfaceEnable(
            deviceObj=self.dut01Obj, enable=True, interface=interface)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to bring interface " +
                      str(interface) + " to UP on DUT01\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "DUT01 interface "
                      + str(interface) + " is up\n")

        interface = self.dut01Obj.linkPortMapping['lnk03']
        devRetStruct = InterfaceEnable(
            deviceObj=self.dut01Obj, enable=True, interface=interface)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to bring interface " +
                      str(interface) + " to UP on DUT01\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "DUT01 interface "
                      + str(interface) + " is up\n")

        interface = self.dut01Obj.linkPortMapping['lnk04']
        devRetStruct = InterfaceEnable(
            deviceObj=self.dut01Obj, enable=True, interface=interface)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to bring interface " +
                      str(interface) + " to UP on DUT01\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "DUT01 interface "
                      + str(interface) + " is up\n")

        interface = self.dut02Obj.linkPortMapping['lnk03']
        devRetStruct = InterfaceEnable(
            deviceObj=self.dut02Obj, enable=True, interface=interface)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to bring interface " +
                      str(interface) + " to UP on DUT02\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "DUT02 interface "
                      + str(interface) + " is up\n")

        interface = self.dut02Obj.linkPortMapping['lnk04']
        devRetStruct = InterfaceEnable(
            deviceObj=self.dut02Obj, enable=True, interface=interface)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to bring interface " +
                      str(interface) + " to UP on DUT02\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "DUT02 interface "
                      + str(interface) + " is up\n")

        interface = self.dut02Obj.linkPortMapping['lnk05']
        devRetStruct = InterfaceEnable(
            deviceObj=self.dut02Obj, enable=True, interface=interface)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to bring interface " +
                      str(interface) + " to UP on DUT02\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "DUT02 interface "
                      + str(interface) + " is up\n")

        interface = self.dut02Obj.linkPortMapping['lnk06']
        devRetStruct = InterfaceEnable(
            deviceObj=self.dut02Obj, enable=True, interface=interface)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to bring interface " +
                      str(interface) + " to UP on DUT02\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "DUT02 interface "
                      + str(interface) + " is up\n")

    def test_ping_hosts(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 14- Verify ping between hosts")
        LogOutput('info', "############################################\n")
        LogOutput('info', "Ping between clients in vlan 30\n")
        devRetStruct = self.wrkston01Obj.Ping(ipAddr="192.168.30.11")
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Ping failed...\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Ping to 192.168.30.11... \n")
            packet_loss = devRetStruct.valueGet(key='packet_loss')
        if packet_loss != 0:
            LogOutput('error', "Packet Loss > 0%, lost " + str(packet_loss))
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Success is 100%...\n")

        LogOutput('info', "Ping between clients in vlan 40")
        devRetStruct = self.wrkston02Obj.Ping(ipAddr="192.168.40.11")
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Ping failed...\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Ping to 192.168.40.11... \n")
            packet_loss = devRetStruct.valueGet(key='packet_loss')
        if packet_loss != 0:
            LogOutput('error', "Packet Loss > 0%, lost " + str(packet_loss))
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Success is 100%...\n")

        LogOutput('info', "Ping between clients in different vlans")
        devRetStruct = self.wrkston01Obj.Ping(ipAddr="192.168.40.11")
        if devRetStruct.returnCode() == 0:
            LogOutput('error', "Client in vlan 30 shouldn't reach \
            " + " client in vlan 40...\n")
            assert devRetStruct.returnCode() != 0
        else:
            LogOutput('info', "Passed - Ping between clients"
                      + "  in different vlans not allowed\n")

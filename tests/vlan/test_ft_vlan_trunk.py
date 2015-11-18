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
# Name:        test_vlan_trunk.py
#
# Description: Verify trunk link can carry multiple vlan traffic.
#              A trunk link is used to connect switches and it
#              should be able to carry traffic from multiple VLANs.
#
# Author:      Roy Ibarra
#
# Topology:   |2 wrkstons |----|Switch|==(trunk)==|Switch|----|2 wrkstons|
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
            " + " lnk03:dut01:dut02,lnk04:dut02:wrkston03,\
            " + "lnk05:dut02:wrkston04",
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
        wrkston03Obj.linkPortMapping['lnk04'], "192.168.30.11",
        "255.255.255.0", "192.168.30.255"))
    LogOutput('info', "Unconfiguring workstation 4")
    finalResult.append(unConfigureWorkstation(
        wrkston04Obj,
        wrkston04Obj.linkPortMapping['lnk05'], "192.168.40.11",
        "255.255.255.0", "192.168.40.255"))

    LogOutput('info', "Delete ports configuration on dut01")
    finalResult.append(clearPortConfig(
        dut01Obj, 30, dut01Obj.linkPortMapping['lnk01'], True, False, False, False))
    finalResult.append(clearPortConfig(
        dut01Obj, 40, dut01Obj.linkPortMapping['lnk02'], True, False, False, False))
    LogOutput('info', "Delete trunk port configuration on dut01")
    finalResult.append(clearPortConfig(
        dut01Obj, 30, dut01Obj.linkPortMapping['lnk03'], False, True, False, False))
    finalResult.append(clearPortConfig(
        dut01Obj, 40, dut01Obj.linkPortMapping['lnk03'], False, True, False, False))
    finalResult.append(clearPortConfig(
        dut01Obj, 50, dut01Obj.linkPortMapping['lnk03'], False, True, False, False))
    LogOutput('info', "Delete ports configuration on dut02")
    finalResult.append(clearPortConfig(
        dut02Obj, 30, dut02Obj.linkPortMapping['lnk04'], True, False, False, False))
    finalResult.append(clearPortConfig(
        dut02Obj, 40, dut02Obj.linkPortMapping['lnk05'], True, False, False, False))
    LogOutput('info', "Delete trunk port configuration on dut02")
    finalResult.append(clearPortConfig(
        dut02Obj, 30, dut02Obj.linkPortMapping['lnk03'], False, True, False, False))
    finalResult.append(clearPortConfig(
        dut02Obj, 40, dut02Obj.linkPortMapping['lnk03'], False, True, False, False))
    finalResult.append(clearPortConfig(
        dut02Obj, 50, dut02Obj.linkPortMapping['lnk03'], False, True, False, False))

    LogOutput('info', "Disabling interfaces on dut01")
    finalResult.append(
        disableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk01']))
    finalResult.append(
        disableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk02']))
    finalResult.append(
        disableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk03']))

    LogOutput('info', "Disabling interfaces on dut02")
    finalResult.append(
        disableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03']))
    finalResult.append(
        disableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk04']))
    finalResult.append(
        disableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk05']))

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

# Erase port configuration


def clearPortConfig(deviceObj, vlanID, interface, access, allowed, tag, config):
    devRetStruct = AddPortToVlan(deviceObj=deviceObj, vlanId=vlanID,
                                 interface=interface, access=access,
                                 allowed=allowed, tag=tag, config=config)
    if devRetStruct.returnCode() != 0:
        LogOutput('error', "Failed to delete port "
                  + str(interface) + " of vlan configuration")
        return False
    else:
        LogOutput('info', "Deleted port "
                  + str(interface)
                  + " of vlan configuration")
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

# Verify a given list of vlan IDs exist in the vlan table


def verifyVlans(deviceObj, vlansList):
    returnCLS = ShowVlan(deviceObj=deviceObj)
    showVlanOutput = returnCLS.valueGet()
    result = True
    for vlanID in vlansList:
        foundVlan = False
        for myDictionary in showVlanOutput:
            if vlanID == myDictionary['VLAN']:
                LogOutput('info', "Vlan " + myDictionary['VLAN'] + " found"
                          + " in the VLAN table")
                foundVlan = True
                break
        if not foundVlan:
            result = False
            LogOutput('error', "Step failed. Vlan " + myDictionary['VLAN']
                      + " does not exist in the VLAN table")
    return result

# Verify the status value of a vlan is correct


def verifyVlanStatus(status, vlanID, data):
    returnData = data.valueGet(key=None)
    for dictionary in returnData:
        if dictionary['VLAN'] == vlanID and \
                dictionary['Status'] == status:
            return 1
    return 0

# Verify the reason value of a vlan is correct


def verifyVlanReason(reason, vlanID, data):
    returnData = data.valueGet(key=None)
    for dictionary in returnData:
        if dictionary['VLAN'] == vlanID and \
                dictionary['Reason'] == reason:
            return 1
    return 0


def verifyVlanPorts(vlanID, port, data):
    assigned = False
    showVlanOutput = data.valueGet()
    for myDictionary in showVlanOutput:
        if myDictionary['VLAN'] == vlanID and \
                port in myDictionary['Ports']:
            assigned = True
            return assigned
    return assigned


class Test_vlan_trunk:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_vlan_trunk.testObj = testEnviron(topoDict=topoDict)
        Test_vlan_trunk.topoObj = Test_vlan_trunk.testObj.topoObjGet()
        Test_vlan_trunk.dut01Obj = Test_vlan_trunk.topoObj.deviceObjGet(
            device="dut01")
        Test_vlan_trunk.dut02Obj = Test_vlan_trunk.topoObj.deviceObjGet(
            device="dut02")
        Test_vlan_trunk.wrkston01Obj = Test_vlan_trunk.topoObj.deviceObjGet(
            device="wrkston01")
        Test_vlan_trunk.wrkston02Obj = Test_vlan_trunk.topoObj.deviceObjGet(
            device="wrkston02")
        Test_vlan_trunk.wrkston03Obj = Test_vlan_trunk.topoObj.deviceObjGet(
            device="wrkston03")
        Test_vlan_trunk.wrkston04Obj = Test_vlan_trunk.topoObj.deviceObjGet(
            device="wrkston04")

    def teardown_class(cls):
        # clean devices
        clean_up_devices(
            cls.topoObj.deviceObjGet(device="dut01"),
            cls.topoObj.deviceObjGet(device="dut02"),
            cls.topoObj.deviceObjGet(device="wrkston01"),
            cls.topoObj.deviceObjGet(device="wrkston02"),
            cls.topoObj.deviceObjGet(device="wrkston03"),
            cls.topoObj.deviceObjGet(device="wrkston04"),)
        # Terminate all nodes
        Test_vlan_trunk.topoObj.terminate_nodes()

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
            interface=self.wrkston03Obj.linkPortMapping['lnk04'],
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
            interface=self.wrkston04Obj.linkPortMapping['lnk05'],
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
        if verifyVlans(self.dut01Obj, ["30", "40", "50"]):
            LogOutput('info', "Passed - All vlans created successfully")
        else:
            LogOutput('error', "Failed- Not all vlans exist in the" +
                      " vlan table on DUT01")
            assert(False)

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
        if verifyVlans(self.dut02Obj, ["30", "40", "50"]):
            LogOutput('info', "Passed - All vlans created successfully")
        else:
            LogOutput('error', "Failed- Not all vlans exist in the" +
                      " vlan table on DUT02")
            assert(False)

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
        interface = self.dut01Obj.linkPortMapping['lnk01']
        devRetStruct = AddPortToVlan(deviceObj=self.dut01Obj, vlanId=30,
                                     interface=interface, access=True,
                                     allowed=False, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure port "
                      + str(interface) + " as access port on vlan 30")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Port "
                      + str(interface)
                      + " was configure with mode access on vlan 30")
        # Add a second port in mode access
        interface = self.dut01Obj.linkPortMapping['lnk02']
        devRetStruct = AddPortToVlan(deviceObj=self.dut01Obj, vlanId=40,
                                     interface=interface, access=True,
                                     allowed=False, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure port "
                      + str(interface) + " as access port on vlan 40")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Port " + str(interface)
                      + " was configure with mode access on vlan 40")

    def test_check_vlan_status_Dut01(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 7- Check vlans have the correct status/reason"
                  + " and ports assigned on DUT01")
        LogOutput('info', "############################################")
        data = ShowVlan(deviceObj=self.dut01Obj)

        # Check status value from show vlan output
        if verifyVlanStatus(status="up", vlanID="30", data=data) != 1:
            LogOutput('error', "Vlan 30 has a status other than up")
            assert(False)
        elif verifyVlanStatus(status="up", vlanID="40", data=data) != 1:
            LogOutput('error', "Vlan 40 has a status other than up")
            assert(False)
        elif verifyVlanStatus(status="down", vlanID="50", data=data) != 1:
            LogOutput('error', "Vlan 50 has a status other than down")
            assert(False)
        else:
            LogOutput('info',
                      "Passed- Vlan 30 & 40 are UP and vlan 50 is down")

        # Check Reason value from show vlan output

        if verifyVlanReason(reason="ok", vlanID="30", data=data) != 1:
            LogOutput('error', "Vlan 30 has a reason value other than up")
            assert(False)
        elif verifyVlanReason(reason="ok", vlanID="40", data=data) != 1:
            LogOutput('error', "Vlan 40 has a reason value other than up")
            assert(False)
        elif verifyVlanReason(reason="no_member_port",
                              vlanID="50", data=data) != 1:
            LogOutput('error',
                      "Vlan 50 has a reason value other than no_member_port")
            assert(False)
        else:
            LogOutput('info',
                      "Passed- Vlan 30 & 40 with reason value of UP" +
                      " and vlan 50 with reason value of no_member_port")

        # Check ports are assigned to the correct vlan
        port = self.dut01Obj.linkPortMapping['lnk01']
        if verifyVlanPorts("30", port, data):
            LogOutput('info', "Port " + port + " assigned to vlan 30")
        else:
            LogOutput('error', "Port" + port
                      + " has not been assigned to vlan 30")
            assert(False)
        port = self.dut01Obj.linkPortMapping['lnk02']
        if verifyVlanPorts("40", port, data):
            LogOutput('info', "Port " + port + " assigned to vlan 40")
        else:
            LogOutput('error', "Port" + port
                      + " has not been assigned to vlan 40")
            assert(False)

    def test_vlan_ports_Dut02(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 8- Assign one port to"
                  + " vlan 30 & 40 as access ports on DUT02")
        LogOutput('info', "############################################")
        # Add one port in mode access
        interface = self.dut02Obj.linkPortMapping['lnk04']
        devRetStruct = AddPortToVlan(deviceObj=self.dut02Obj, vlanId=30,
                                     interface=interface, access=True,
                                     allowed=False, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure port "
                      + str(interface) + " as access port on vlan 30")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Port "
                      + str(interface)
                      + " was configure with mode access on vlan 30")
        # Add a second port in mode access
        interface = self.dut02Obj.linkPortMapping['lnk05']
        devRetStruct = AddPortToVlan(deviceObj=self.dut02Obj, vlanId=40,
                                     interface=interface, access=True,
                                     allowed=False, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure port "
                      + str(interface) + " as access port on vlan 40")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Port " + str(interface)
                      + " was configure with mode access on vlan 40")

    def test_check_vlan_status_Dut02(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 9- Check vlans have the correct status/reason "
                  + " and ports assigned on DUT02")
        LogOutput('info', "############################################")
        data = ShowVlan(deviceObj=self.dut02Obj)

        # Check status value from show vlan output
        if verifyVlanStatus(status="up", vlanID="30", data=data) != 1:
            LogOutput('error', "Vlan 30 has a status other than up")
            assert(False)
        elif verifyVlanStatus(status="up", vlanID="40", data=data) != 1:
            LogOutput('error', "Vlan 40 has a status other than up")
            assert(False)
        elif verifyVlanStatus(status="down", vlanID="50", data=data) != 1:
            LogOutput('error', "Vlan 50 has a status other than down")
            assert(False)
        else:
            LogOutput('info',
                      "Passed- Vlan 30 & 40 are UP and vlan 50 is down")

        # Check Reason value from show vlan output

        if verifyVlanReason(reason="ok", vlanID="30", data=data) != 1:
            LogOutput('error', "Vlan 30 has a reason value other than up")
            assert(False)
        elif verifyVlanReason(reason="ok", vlanID="40", data=data) != 1:
            LogOutput('error', "Vlan 40 has a reason value other than up")
            assert(False)
        elif verifyVlanReason(reason="no_member_port",
                              vlanID="50", data=data) != 1:
            LogOutput('error',
                      "Vlan 50 has a reason value other than no_member_port")
            assert(False)
        else:
            LogOutput('info',
                      "Passed- Vlan 30 & 40 with reason value of UP" +
                      " and vlan 50 with reason value of no_member_port")

        # Check ports are assigned to the correct vlan
        port = self.dut02Obj.linkPortMapping['lnk04']
        if verifyVlanPorts("30", port, data):
            LogOutput('info', "Port " + port + " assigned to vlan 30")
        else:
            LogOutput('error', "Port" + port
                      + " has not been assigned to vlan 30")
            assert(False)
        port = self.dut02Obj.linkPortMapping['lnk05']
        if verifyVlanPorts("40", port, data):
            LogOutput('info', "Port " + port + " assigned to vlan 40")
        else:
            LogOutput('error', "Port" + port
                      + " has not been assigned to vlan 40")
            assert(False)

    def test_vlan_trunk_Dut01(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 8- Add VLANs to the list of allowed"
                  + " VLANs in a trunk port on DUT01")
        LogOutput('info', "############################################")
        # Adding vlan 30 to the allow list in trunk link
        port1 = self.dut01Obj.linkPortMapping['lnk03']
        devRetStruct = AddPortToVlan(deviceObj=self.dut01Obj, vlanId=30,
                                     interface=port1, access=False,
                                     allowed=True, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure the allowed"
                      + " VLAN 30 in trunk port on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - VLAN 30 allowed in trunk"
                      + " port on DUT01")
        # Adding vlan 40 to the allow list in trunk link
        devRetStruct = AddPortToVlan(deviceObj=self.dut01Obj, vlanId=40,
                                     interface=port1, access=False,
                                     allowed=True, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure the allowed"
                      + " VLAN 40 in trunk port on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - VLAN 40 allowed in trunk"
                      + " port on DUT01")
        # Adding vlan 50 to the allow list in trunk link
        devRetStruct = AddPortToVlan(deviceObj=self.dut01Obj, vlanId=50,
                                     interface=port1, access=False,
                                     allowed=True, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure the allowed"
                      + " VLAN 50 in trunk port on DUT01")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - VLAN 50 allowed in trunk"
                      + "  port on DUT01")

        # Check ports are assigned to the correct vlan
        data = ShowVlan(deviceObj=self.dut01Obj)
        if verifyVlanPorts("30", port1, data):
            LogOutput('info', "Port " + port1 +
                      " assigned to vlan 30 as trunk")
        else:
            LogOutput('error', "Port" + port1
                      + " has not been assigned to vlan 30 as trunk")
            assert(False)

        if verifyVlanPorts("40", port1, data):
            LogOutput('info', "Port " + port1 +
                      " assigned to vlan 40 as trunk")
        else:
            LogOutput('error', "Port" + port1
                      + " has not been assigned to vlan 40 as trunk")
            assert(False)
        if verifyVlanPorts("50", port1, data):
            LogOutput('info', "Port " + port1 +
                      " assigned to vlan 50 as trunk")
        else:
            LogOutput('error', "Port" + port1
                      + " has not been assigned to vlan 50 as trunk")

    def test_vlan_trunk_Dut02(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 9- Add VLANs to the list of allowed"
                  + " VLANs in a trunk port on DUT02")
        LogOutput('info', "############################################")
        # Adding vlan 30 to the allow list in trunk link
        port1 = self.dut02Obj.linkPortMapping['lnk03']
        devRetStruct = AddPortToVlan(deviceObj=self.dut02Obj, vlanId=30,
                                     interface=port1, access=False,
                                     allowed=True, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure the allowed"
                      + " VLAN 30 in trunk port on DUT02")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - VLAN 30 allowed in trunk"
                      + " port on DUT02")
        # Adding vlan 40 to the allow list in trunk link
        devRetStruct = AddPortToVlan(deviceObj=self.dut02Obj, vlanId=40,
                                     interface=port1, access=False,
                                     allowed=True, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure the allowed"
                      + " VLAN 40 in trunk port on DUT02")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - VLAN 40 allowed in trunk"
                      + " port on DUT02")
        # Adding vlan 50 to the allow list in trunk link
        devRetStruct = AddPortToVlan(deviceObj=self.dut02Obj, vlanId=50,
                                     interface=port1, access=False,
                                     allowed=True, tag=False, config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure the allowed"
                      + " VLAN 50 in trunk port on DUT02")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - VLAN 50 allowed in trunk"
                      + "  port on DUT02")

        # Check ports are assigned to the correct vlan
        data = ShowVlan(deviceObj=self.dut02Obj)
        if verifyVlanPorts("30", port1, data):
            LogOutput('info', "Port " + port1 +
                      " assigned to vlan 30 as trunk")
        else:
            LogOutput('error', "Port" + port1
                      + " has not been assigned to vlan 30 as trunk")
            assert(False)

        if verifyVlanPorts("40", port1, data):
            LogOutput('info', "Port " + port1 +
                      " assigned to vlan 40 as trunk")
        else:
            LogOutput('error', "Port" + port1
                      + " has not been assigned to vlan 40 as trunk")
            assert(False)
        if verifyVlanPorts("50", port1, data):
            LogOutput('info', "Port " + port1 +
                      " assigned to vlan 50 as trunk")
        else:
            LogOutput('error', "Port" + port1
                      + " has not been assigned to vlan 50 as trunk")

    def test_set_interfaces_up(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 10- Bring interfaces"
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

    def test_ping_hosts(self):
        LogOutput('info', "############################################")
        LogOutput('info', "step 11- Verify ping between hosts")
        LogOutput('info', "############################################\n")
        LogOutput('info', "ping between clients in vlan 30\n")
        devRetStruct = self.wrkston01Obj.Ping(ipAddr="192.168.30.11")
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "ping failed...\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "ping to 192.168.30.11... \n")
            packet_loss = devRetStruct.valueGet(key='packet_loss')
        if packet_loss != 0:
            LogOutput('error', "packet loss > 0%, lost " + str(packet_loss))
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "success is 100%...\n")

        LogOutput('info', "ping between clients in vlan 40")
        devRetStruct = self.wrkston02Obj.Ping(ipAddr="192.168.40.11")
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "ping failed...\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "ping to 192.168.40.11... \n")
            packet_loss = devRetStruct.valueGet(key='packet_loss')
        if packet_loss != 0:
            LogOutput('error', "packet loss > 0%, lost " + str(packet_loss))
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "success is 100%...\n")

        LogOutput('info', "ping from client in vlan 30 to client in vlan 40")
        devRetStruct = self.wrkston01Obj.Ping(ipAddr="192.168.40.11")
        if devRetStruct.returnCode() == 0:
            LogOutput('error', "client in vlan 30 shouldn't reach \
            " + " client in vlan 40...\n")
            assert devRetStruct.returnCode() != 0
        else:
            LogOutput('info', "passed - ping between clients is successful\n")

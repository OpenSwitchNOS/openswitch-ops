# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import opstestfw.host.PacketCapture
from opstestfw import testEnviron
from opstestfw import LogOutput
from opstestfw import Sleep
from opstestfw.switch.CLI import *

# Topology definition
# Topology : TwoDUT's , One workstation
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01",
            "topoDevices": "dut01 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,lnk02:dut01:wrkston02",
            "topoFilters": "dut01:system-category:switch, \
                 wrkston01:system-category:workstation, \
                 wrkston01:docker-image:host/freeradius-ubuntu, \
                 wrkston02:system-category:workstation, \
                 wrkston02:docker-image:host/freeradius-ubuntu"}


def lldp_vlan_access(**kwargs):
    device1 = kwargs.get('device1', None)
    host = kwargs.get('device2', None)

    LogOutput('info', "\nTest 1 : Access Vlan\n\n")
    # Configuring no routing on interface
    # Entering VTYSH terminal
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    LogOutput('info', "Configuring VLAN 10")
    returnStructure = device1.DeviceInteract(command="vlan 10")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to enter interface context for vlan"

    returnStructure = device1.DeviceInteract(command="no shutdown")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to perform no shut"

    returnStructure = device1.DeviceInteract(command="exit")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to exit"

    LogOutput('info', "Configuring VLAN 20")
    returnStructure = device1.DeviceInteract(command="vlan 20")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to enter interface context for vlan"

    returnStructure = device1.DeviceInteract(command="no shutdown")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to perform no shut"

    returnStructure = device1.DeviceInteract(command="exit")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to exit"

    LogOutput('info', "Configuring VLAN 30")
    returnStructure = device1.DeviceInteract(command="vlan 30")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to enter interface context for vlan"

    returnStructure = device1.DeviceInteract(command="no shutdown")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to perform no shut"

    returnStructure = device1.DeviceInteract(command="exit")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to exit"

    LogOutput('info', "Configuring VLAN 40")
    returnStructure = device1.DeviceInteract(command="vlan 40")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to enter interface context for vlan"

    returnStructure = device1.DeviceInteract(command="no shutdown")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to perform no shut"

    returnStructure = device1.DeviceInteract(command="exit")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to exit"

    # Entering interface
    LogOutput('info', "Switch 1 interface is : " +
              str(device1.linkPortMapping['lnk01']))
    devIntRetStruct = device1.DeviceInteract(
        command="interface " + str(device1.linkPortMapping['lnk01']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter interface"

    returnStructure = device1.DeviceInteract(command="no shutdown")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to no shutdown"

    devIntRetStruct = device1.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to disable routing"

    # Exiting interface
    devIntRetStruct = device1.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to exit interface"

    # Exiting Config terminal
    retStruct = device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Exiting VTYSH terminal
    retStruct = device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Configuring lldp on SW1
    LogOutput('info', "\n\n\nConfig lldp on SW1")
    retStruct = LldpConfig(deviceObj=device1, enable=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to configure LLDP on SW1"

    AddPortToVlan(deviceObj=device1, vlanId=10,
                  interface=device1.linkPortMapping['lnk01'], access=True)

    # Enabling interface 1 SW1
    LogOutput('info', "Enabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True,
                                interface=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to enabling interafce on SW1"

    # Printing captured packets
    CaptureObj = opstestfw.host.PacketCapture(
        host.device, host.linkPortMapping['lnk01'], "Capture.log")
    retStruct = CaptureObj.StartCapture(connection=host)
    Sleep(seconds=40, message="Waiting for LLDP packets to be captured")
    myretStruct = CaptureObj.ParseCapture(host)
    if myretStruct.returnCode() == 0:
        print myretStruct.dataKeys()
        PacketDict = dict()
        PacketDict = myretStruct.valueGet(key='LLDPFrames')
        print PacketDict
        # Details of the first frame
        print "#######"
        assert (str(PacketDict[1]["VlanNameTLV"][0]) == "vlan10" and
                str(PacketDict[1]["PortVLanID"]) == "10 (0x000A)"), \
            "\n**Case Failed**\n"
        LogOutput('info', "\n**Case Passed**\n")
    else:
        LogOutput("error", "Failed to capture packets on workstation**")
        assert(False)


def lldp_vlan_trunk(**kwargs):
    device1 = kwargs.get('device1', None)
    host = kwargs.get('device2', None)

    # Configuring no routing on interface
    # Entering VTYSH terminal
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    LogOutput('info', "Configuring VLAN 10")
    returnStructure = device1.DeviceInteract(command="vlan 10")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to enter interface context for vlan"

    returnStructure = device1.DeviceInteract(command="no shutdown")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to perform no shut"

    returnStructure = device1.DeviceInteract(command="exit")
    retCode = returnStructure.get('returnCode')
    assert retCode == 0, "Failed to exit interface"

    LogOutput('info', "Configuring VLAN 20")
    returnStructure = device1.DeviceInteract(command="vlan 20")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to enter interface context for vlan"

    returnStructure = device1.DeviceInteract(command="no shutdown")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to perform no shut"

    returnStructure = device1.DeviceInteract(command="exit")
    retCode = returnStructure.get('returnCode')
    assert retCode == 0, "Failed to exit interface"

    LogOutput('info', "Configuring VLAN 30")
    returnStructure = device1.DeviceInteract(command="vlan 30")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to enter interface context for vlan"

    returnStructure = device1.DeviceInteract(command="no shutdown")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to perform no shut"

    returnStructure = device1.DeviceInteract(command="exit")
    retCode = returnStructure.get('returnCode')
    assert retCode == 0, "Failed to exit interface"

    LogOutput('info', "Configuring VLAN 40")
    returnStructure = device1.DeviceInteract(command="vlan 40")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to enter interface context for vlan"

    returnStructure = device1.DeviceInteract(command="no shutdown")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to perform no shut"

    returnStructure = device1.DeviceInteract(command="exit")
    retCode = returnStructure.get('returnCode')
    assert retCode == 0, "Failed to exit interface"

    # Entering interface
    LogOutput('info', "Switch 1 interface is : " +
              str(device1.linkPortMapping['lnk02']))
    devIntRetStruct = device1.DeviceInteract(
        command="interface " + str(device1.linkPortMapping['lnk02']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter interface"

    returnStructure = device1.DeviceInteract(command="no shutdown")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to perform no shut"

    devIntRetStruct = device1.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to disable routing"

    # Exiting interface
    devIntRetStruct = device1.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to exit interface"

    # Exiting Config terminal
    retStruct = device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Exiting VTYSH terminal
    retStruct = device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Configuring lldp on SW1
    LogOutput('info', "\n\n\nConfig lldp on SW1")
    retStruct = LldpConfig(deviceObj=device1, enable=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to configure LLDP on SW1"

    AddPortToVlan(deviceObj=device1, vlanId=10,
                  interface=device1.linkPortMapping['lnk02'])
    AddPortToVlan(deviceObj=device1, vlanId=20,
                  interface=device1.linkPortMapping['lnk02'], allowed=True)
    AddPortToVlan(deviceObj=device1, vlanId=30,
                  interface=device1.linkPortMapping['lnk02'], allowed=True)
    AddPortToVlan(deviceObj=device1, vlanId=40,
                  interface=device1.linkPortMapping['lnk02'], allowed=True)

    # Enabling interface 1 SW1
    LogOutput('info', "Enabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True,
                                interface=device1.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to enabling interafce on SW1"

    CaptureObj = opstestfw.host.PacketCapture(
        host.device, host.linkPortMapping['lnk02'], "Capture.log")
    retStruct = CaptureObj.StartCapture(connection=host)
    Sleep(seconds=40, message="Waiting for LLDP packets to be captured")
    myretStruct = CaptureObj.ParseCapture(host)
    if myretStruct.returnCode() == 0:
        print myretStruct.dataKeys()
        PacketDict = dict()
        PacketDict = myretStruct.valueGet(key='LLDPFrames')
        print PacketDict
        # Details of the first frame
        assert (str(PacketDict[1]["VlanNameTLV"][0]) == "vlan10" and
                str(PacketDict[1]["VlanNameTLV"][1]) == "vlan20" and
                str(PacketDict[1]["VlanNameTLV"][2]) == "vlan30" and
                str(PacketDict[1]["VlanNameTLV"][3]) == "vlan40" and
                str(PacketDict[1]["PortVLanID"]) == "10 (0x000A)"), \
            "\n**Case Failed**\n"
        LogOutput('info', "\n**Case Passed**\n")
    else:
        LogOutput("error", "Failed to capture packets on workstation**")
        assert(False)


@pytest.mark.timeout(700)
class Test_lldp_vlan:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_lldp_vlan.testObj = testEnviron(topoDict=topoDict)
        # Get topology object
        Test_lldp_vlan.topoObj = Test_lldp_vlan.testObj.topoObjGet()

    def teardown_class(cls):
        Test_lldp_vlan.topoObj.terminate_nodes()

    def test_lldp_vlan_access(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        lldp_vlan_access(device1=dut01Obj, device2=wrkston01Obj)
        LogOutput('info', "\nTest 2 : Trunk Vlan\n\n")

    def test_lldp_vlan_trunk(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        lldp_vlan_trunk(device1=dut01Obj, device2=wrkston02Obj)

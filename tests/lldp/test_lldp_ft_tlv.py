#!/usr/bin/env python
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

import pytest
import re
from  opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02",
            "topoLinks": "lnk01:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,dut02:system-category:switch"}
def lldp_tlv(**kwargs):
    device1 = kwargs.get('device1',None)
    device2 = kwargs.get('device2',None)

    #Setting tx time to 5 sec on SW1 and SW2
    #Entering vtysh SW1
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to enter vtysh prompt"

    #Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode= retStruct.returnCode()
    assert retCode==0, "Failed to enter config terminal"

    #Setting tx time to 5 seconds on SW1
    LogOutput('info', "\nConfiguring transmit time of 5 sec on SW1")
    devIntRetStruct = device1.DeviceInteract(command="lldp timer 5")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to set transmit time"

    #Entering vtysh SW2
    retStruct = device2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to get vtysh prompt"

    #Entering config terminal SW2
    devIntRetStruct = device2.ConfigVtyShell(enter=True)
    retCode = devIntRetStruct.returnCode()
    assert retCode==0, "\nFailed to enter config mode"

    #Setting tx time to 5 seconds on SW2
    LogOutput('info', "\nConfiguring transmit time of 5 sec on SW2")
    devIntRetStruct = device2.DeviceInteract(command="lldp timer 5")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "\nFailed to configure transmit time"

    #Exiting Config terminal SW1
    retStruct= device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to come out of config terminal"

    #Exiting Config terminal SW2
    retStruct=device2.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to come out of config terminal"

    #Exiting vtysh terminal SW1
    retStruct=device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to exit vtysh prompt"

    #Exiting vtysh terminal SW2
    retStruct=device2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to exit vtysh prompt"


    #Configuring lldp on SW1
    LogOutput('info', "\n\n\nConfig lldp on SW1")
    retStruct = LldpConfig(deviceObj=device1, enable=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to configure LLDP on SW1"

    #Enabling interface 1 SW1
    LogOutput('info', "Enabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True, interface=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW1"

    #Configuring lldp on SW2
    LogOutput('info', "\n\n\nConfig lldp on SW2")
    retStruct = LldpConfig(deviceObj=device2, enable=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Configure lldp on SW2"

    #Enabling interface 1 SW2
    LogOutput('info', "Enabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True, interface=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enable interface on SW2"


    #Waiting for neighbour to advertise
    Sleep(seconds=25, message="\nWaiting")

    #Parsing neighbour info for SW1
    LogOutput('info', "\nShowing Lldp neighbourship on SW1")
    retStruct = ShowLldpNeighborInfo(deviceObj=device1, port=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to show neighbour info"

    LogOutput('info', "CLI_Switch1")
    retStruct.printValueString()
    lnk01PrtStats = retStruct.valueGet(key='portStats')
    assert int((lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())==1, "Case Failed, No Neighbor present for SW1"
    assert (lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_chassisName'])!="(null)", "Case Failed, Neighbor Chassis-Name is not present"
    assert (lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_chassisDescription'])!="(null)\r", "Case Failed, Neighbor Chassis-Description is not present"
    assert (lnk01PrtStats[device1.linkPortMapping['lnk01']]['Chassis_Capabilities_Available'])=="Bridge, Router\r", "Case Failed, Neighbor Chassis-Capabilities is not available"
    if (lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']):
       LogOutput('info',"\nCase Passed, Neighborship established by SW1")
       LogOutput('info', "\nNeighbor Chassis-Name :" + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_chassisName']))
       LogOutput('info', "\nNeighbor Chassis-Description :" + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_chassisDescription']))
       LogOutput('info',"\nChassie Capabilities available : "+str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Chassis_Capabilities_Available']))
       LogOutput('info', "\nChassis Capabilities Enabled : "+str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Chassis_Capabilities_Enabled']))

    #Parsing neighbour info for SW2
    LogOutput('info', "\nShowing Lldp neighborship on SW2")
    retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk01'])

    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to show neighour info"

    LogOutput('info', "CLI_Switch2")
    retStruct.printValueString()
    lnk01PrtStats = retStruct.valueGet(key='portStats')
    assert int((lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())==1, "Case Failed, No Neighbor present for SW1"
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_chassisName'])!="(null)", "Case Failed, Neighbor Chassis-Name is not present"
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_chassisDescription'])!="(null)\r", "Case Failed, Neighbor Chassis-Description is not present"
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Available'])=="Bridge, Router\r", "Case Failed, Neighbor Chassis-Capabilities is not available"
    if (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']):
       LogOutput('info',"\nCase Passed, Neighborship established by SW2")
       LogOutput('info', "\nNeighbor Chassis-Name :" + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_chassisName']))
       LogOutput('info', "\nNeighbor Chassis-Description :" + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_chassisDescription']))
       LogOutput('info',"\nChassie Capablities available : "+ str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Available']))
       LogOutput('info', "\nChassis Capabilities Enabled : "+ str( lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Enabled']))

    #Disabling chassie name for neighbor
    #Entering vtysh SW1
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to enter vtysh prompt"

    #Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode= retStruct.returnCode()
    assert retCode==0, "Failed to enter config terminal"

    #Disabling system-name on SW1
    LogOutput('info', "\nDisabling system-name for SW1")
    devIntRetStruct = device1.DeviceInteract(command="no lldp select-tlv system-name")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to set no lldp select-tlv system-name"

    #Checking SW2 to see if system-name is removed
    LogOutput('info', "\n\nCase 1:System-Name Disabled")
    retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to show neighbor info"


    LogOutput('info', "CLI_Switch2")
    lnk01PrtStats = retStruct.valueGet(key='portStats')
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_chassisName'])=="(null)", "Case Failed, Neighbor Chassis-Name is present"
    LogOutput('info', "#Case Passed,No neighbor Chassis-Name present#")

    #Enabling System-Name
    LogOutput('info', "\nEnabling System-Name for SW1")
    devIntRetStruct = device1.DeviceInteract(command="lldp select-tlv system-name")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to set lldp select-tlv system-name"

    #Checking SW2 to see if system-name is reset
    LogOutput('info', "\n\nCase 2 :System-Name Enabled")

    retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to show neighbor info"


    LogOutput('info', "CLI_Switch2")
    lnk01PrtStats = retStruct.valueGet(key='portStats')
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_chassisName'])!="(null)", "Case Failed, Neighbor Chassis-Name is not present"
    LogOutput('info', "#Case Passed,Neighbor Chassis-Name is present#")

    #Disabling Neighbor Chassis-Description
    LogOutput('info', "\nDisabling System-Description for SW1")
    devIntRetStruct = device1.DeviceInteract(command="no lldp select-tlv system-description")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to set no lldp select-tlv system-description"

    #Checking SW2 to see if system-description is removed

    LogOutput('info', "\n\nCase 3: System-Description Disabled")

    retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to show neighbor info"


    LogOutput('info', "CLI_Switch2")
    lnk01PrtStats = retStruct.valueGet(key='portStats')
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_chassisDescription'])=="(null)\r", "Case Failed, Neighbor Chassis-Description is present"
    LogOutput('info', "#Case Passed,No neighbor Chassis-Description present#")

    #Enabling System-Description
    LogOutput('info', "\nEnabling System-description for SW1")
    devIntRetStruct = device1.DeviceInteract(command="lldp select-tlv system-description")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to set lldp select-tlv system-description"

   #Checking SW2 to see if system-name is reset

    LogOutput('info', "\n\nCase 4: System-Description Enabled")

    retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to show neighbor info"


    LogOutput('info', "CLI_Switch2")

    lnk01PrtStats = retStruct.valueGet(key='portStats')
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_chassisDescription'])!="(null)\r", "Case Failed, Neighbor Chassis-Description is not present"
    LogOutput('info', "#Case Passed,Neighbor Chassis-Description is present#")

    #Disabling System-Capabilities
    LogOutput('info', "\nDisabling Neighor Chassis-Capabilities for SW1")
    devIntRetStruct = device1.DeviceInteract(command="no lldp select-tlv system-capabilities")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to set no lldp select-tlv system-capabilities"

    #Checking SW2 to see if system-description is removed

    LogOutput('info', "\n\nCase 5: System-Capabilities disabled")

    retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to show neighbor info"


    LogOutput('info', "CLI_Switch2")
    lnk01PrtStats = retStruct.valueGet(key='portStats')
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Available'])=="", "Case Failed, Neighbor Chassis-Capabilities is available"
    LogOutput('info', "#Case Passed,No neighbor Chassis-capablities available#")
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Enabled'])=="", "Case Failed, Neighbor Chassis-Capabilities is enabled"
    LogOutput('info', "#Case Passed,No neighbor Chassis-capablities enabled#")

    #System-Capabilities Enabled
    LogOutput('info', "\nEnabling Neighbor Chassis-Capabilities for SW1")
    devIntRetStruct = device1.DeviceInteract(command="lldp select-tlv system-capabilities")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to set lldp select-tlv system-capabilities"

   #Checking SW2 to see if system-name is reset

    LogOutput('info', "\n\nCase 6: System-Capabilities enabled")

    retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to show neighbor info"


    LogOutput('info', "CLI_Switch2")
    lnk01PrtStats = retStruct.valueGet(key='portStats')
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Available'])=="Bridge, Router\r", "Case Failed, Neighbor Chassis-Capabilities is not available"
    LogOutput('info', "#Case Passed,Neighbor Chassis-capablities available#")
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Enabled'])=="Bridge, Router\r", "Case Failed, Neighbor Chassis-Capabilities is not enabled"
    LogOutput('info', "#Case Passed,Neighbor Chassis-capablities enabled#")


    retStruct= device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to come out of config terminal"

    retStruct=device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to exit vtysh prompt"


class Test_lldp_configuration:
    def setup_class (cls):
        # Test object will parse command line and formulate the env
        Test_lldp_configuration.testObj = testEnviron(topoDict=topoDict)
        #    Get topology object
        Test_lldp_configuration.topoObj = Test_lldp_configuration.testObj.topoObjGet()

    def teardown_class (cls):
        Test_lldp_configuration.topoObj.terminate_nodes()

    def test_lldp_tlv(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        retValue = lldp_tlv(device1=dut01Obj, device2=dut02Obj)

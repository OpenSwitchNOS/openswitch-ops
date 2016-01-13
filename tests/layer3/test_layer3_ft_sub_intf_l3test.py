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
            "topoTarget": "dut01 ",
            "topoDevices": "dut01 wrkston01 ",
            "topoLinks": "lnk01:dut01:wrkston01",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation"}

def sub_interface(**kwargs):
    device1 = kwargs.get('device1',None)
    wrkstn1 = kwargs.get('device2',None)

    LogOutput('info',"## Positive l3 reachability test with admin state up ")

    retStruct = InterfaceEnable(deviceObj=device1, enable=True,
                                interface="1.1")

    retStruct = InterfaceIpConfig(deviceObj=device1,
                                  interface=device1.linkPortMapping['lnk01'],
                                  routing=True, config=True)

    if retStruct.returnCode() != 0:
        LogOutput('error',"Failed to enable interface")
        assert(False)

    retStruct = InterfaceIpConfig(deviceObj=device1,
                                  interface="1.1",
                                  addr="192.168.1.1", mask=24, config=True)

    if retStruct.returnCode() != 0:
        LogOutput('error',"Failed to configure interface Ip address ")
        assert(False)

    retStruct = Dot1qEncapsulation(deviceObj=device1,subInterface="1.1", dot1q=True, vlan=100)
    if retStruct.returnCode() != 0:
        LogOutput('error',"Failed to enable interface")
        assert(False)
    rcommand="ip link add link "+ wrkstn1.linkPortMapping['lnk01']+ " name eth1.100 type vlan id 100"
    #retCmdout=wrkstn1.DeviceInteract(command="ip link add link eth0 name eth0.100 type vlan id 100")
    retCmdout=wrkstn1.DeviceInteract(command="ip link add link "+ wrkstn1.linkPortMapping['lnk01']+ " name eth1.100 type vlan id 100")
    # configure Ip on the host
    retStructObj = wrkstn1.NetworkConfig(ipAddr="192.168.1.2",
		   netMask="255.255.255.0", broadcast="192.168.1.255",
		   interface="eth1.100", config=True)
    if retStructObj.returnCode() != 0:
        LogOutput('error', "Failed to configure IP on workstation")
        assert(False)

    retStruct = wrkstn1.Ping(ipAddr="192.168.1.1", packetCoung=10)
    retCode = retStruct.returnCode()
    assert retCode ==0, "failed to ping switch"

    LogOutput('info', "IPv4 Ping from workstation 1 to dut01 return JSON:\n" + str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key='packet_loss')
    packets_sent = retStruct.valueGet(key='packets_transmitted')
    packets_received = retStruct.valueGet(key='packets_received')
    LogOutput('info', "Packets Sent:\t"+ str(packets_sent))
    LogOutput('info', "Packets Recv:\t"+ str(packets_received))
    LogOutput('info', "Packet Loss %:\t"+str(packet_loss))

    LogOutput('info',"## Negative l3 reachability test with admin state down ")
    retStruct = InterfaceEnable(deviceObj=device1, enable=False,
                                interface="1.1")

    retStruct = wrkstn1.Ping(ipAddr="192.168.1.1", packetCoung=10)
    retCode = retStruct.returnCode()
    assert retCode ==0, "failed to ping switch"

    LogOutput('info', "IPv4 Ping from workstation 1 to dut01 return JSON:\n" + str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key='packet_loss')
    packets_sent = retStruct.valueGet(key='packets_transmitted')
    packets_received = retStruct.valueGet(key='packets_received')
    LogOutput('info', "Packets Sent:\t"+ str(packets_sent))
    LogOutput('info', "Packets Recv:\t"+ str(packets_received))
    LogOutput('info', "Packet Loss %:\t"+str(packet_loss))

    LogOutput('info', "shutting down interface 1.1")
    LogOutput('info', "checking ping after shutting down interface 1.1")

    retStruct = wrkstn1.Ping(ipAddr="192.168.1.1", packetCoung=10)
    retCode = retStruct.returnCode()
    assert retCode ==0, "failed to ping switch"

    LogOutput('info', "IPv4 Ping from workstation 1 to dut01 return JSON:\n" + str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key='packet_loss')
    packets_sent = retStruct.valueGet(key='packets_transmitted')
    packets_received = retStruct.valueGet(key='packets_received')
    LogOutput('info', "Packets Sent:\t"+ str(packets_sent))
    LogOutput('info', "Packets Recv:\t"+ str(packets_received))
    LogOutput('info', "Packet Loss %:\t"+str(packet_loss))


def deviceCleanup(**kwargs):
    device1 = kwargs.get('device1',None)
    wrkstn1 = kwargs.get('device2',None)

    LogOutput('info',"Device Cleanup")

    retStruct = InterfaceEnable(deviceObj=device1, enable=False,
                                interface="1.1")

    if retStruct.returnCode() != 0:
        LogOutput('error',"Failed to enable interface")
        assert(False)

    retStruct = InterfaceIpConfig(deviceObj=device1,
                                  interface="1.1",
                                  addr="192.168.1.1", mask=24, config=False)

    if retStruct.returnCode() != 0:
        LogOutput('error',"Failed to configure interface Ip address ")
        assert(False)

    retStruct = Dot1qEncapsulation(deviceObj=device1,subInterface="1.1", dot1q=False, vlan=100)
    if retStruct.returnCode() != 0:
        LogOutput('error',"Failed to enable interface")
        assert(False)

    # configure Ip on the host
    retStructObj = wrkstn1.NetworkConfig(ipAddr="192.168.1.2",
                   netMask="255.255.255.0",broadcast="192.168.1.255",
		   interface="eth1.100", config=False)
    if retStructObj.returnCode() != 0:
        LogOutput('error', "Failed to configure IP on workstation")
        assert(False)

class Test_subInt:
    def setup_class (cls):
        # Test object will parse command line and formulate the env
        Test_subInt.testObj = testEnviron(topoDict=topoDict)
        #    Get topology object
        Test_subInt.topoObj = Test_subInt.testObj.topoObjGet()

    #def teardown_class (cls):
        #Test_subInt.topoObj.terminate_nodes()

    def test_l3_route(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkston1Obj = self.topoObj.deviceObjGet(device="wrkston01")
        retValue = sub_interface(device1=dut01Obj,device2=wrkston1Obj)

    def test_deviceClanup(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkston1Obj = self.topoObj.deviceObjGet(device="wrkston01")
        retValue = deviceCleanup(device1=dut01Obj,device2=wrkston1Obj)

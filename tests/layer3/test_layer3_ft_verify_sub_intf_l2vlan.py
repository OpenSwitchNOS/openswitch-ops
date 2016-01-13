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
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 ",
            "topoDevices": "dut01 wrkston01 wrkston02 wrkston03",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut01:wrkston02,\
                          lnk03:dut01:wrkston03",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation,\
                            wrkston03:system-category:workstation"}


def l3_route(**kwargs):

    device1 = kwargs.get('device1', None)
    wrkstn1 = kwargs.get('device2', None)
    wrkstn2 = kwargs.get('device3', None)
    wrkstn3 = kwargs.get('device4', None)

    retStruct = InterfaceEnable(deviceObj=device1, enable=True,
                                interface="1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True,
                                interface="1.10")

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    retStruct = InterfaceEnable(deviceObj=device1, enable=True,
                                interface=device1.linkPortMapping['lnk02'])

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to configure interface IP address")
        assert(False)

    retStruct = InterfaceEnable(deviceObj=device1, enable=True,
                                interface=device1.linkPortMapping['lnk03'])

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    devVlanRetStruct1 = AddVlan(deviceObj=device1,
                                vlanId=10,
                                config=True)

    if devVlanRetStruct1.returnCode() != 0:
        LogOutput('error',
                  "Failed to add vlan")
        assert(False)
    else:
        LogOutput('info', "Passed Adding Vlan")

    devIntRetStruct1 = AddPortToVlan(deviceObj=device1,
                                     vlanId=10,
                                     interface=device1.
                                     linkPortMapping['lnk02'],
                                     access=True,
                                     config=True)

    devIntRetStruct2 = AddPortToVlan(deviceObj=device1,
                                     vlanId=10,
                                     interface=device1.
                                     linkPortMapping['lnk03'],
                                     access=True,
                                     config=True)

    if devIntRetStruct1.returnCode() != 0 \
       or devIntRetStruct2.returnCode() != 0:
        LogOutput('error',
                  "Failed to add vlan to port")
        assert(False)
    else:
        LogOutput('info', "Passed Adding Vlan to port")

    # configure Ip on the host
    retStructObj = wrkstn2.NetworkConfig(ipAddr="192.168.1.2",
                                         netMask="255.255.255.0",
                                         broadcast="192.168.1.255",
                                         interface=wrkstn2.
                                         linkPortMapping['lnk02'], config=True)

    if retStructObj.returnCode() != 0:
        LogOutput('error', "Failed to configure IP on workstation")

    retStructObj = wrkstn3.NetworkConfig(ipAddr="192.168.1.3",
                                         netMask="255.255.255.0",
                                         broadcast="192.168.1.255",
                                         interface=wrkstn3.
                                         linkPortMapping['lnk03'], config=True)
    if retStructObj.returnCode() != 0:
        LogOutput('error', "Failed to configure IP on workstation")
    LogOutput('info', "Pinging between workstation1 and dworkstation3")

    retStruct = wrkstn2.Ping(ipAddr="192.168.1.3", packetCoung=10)
    retCode = retStruct.returnCode()
    assert retCode == 0, "failed to ping Host3"

    LogOutput('info', "ping workstation 2 to workstation 3 return \
                       JSON:\n" + str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key='packet_loss')
    packets_sent = retStruct.valueGet(key='packets_transmitted')
    packets_received = retStruct.valueGet(key='packets_received')
    LogOutput('info', "Packets Sent:\t" + str(packets_sent))
    LogOutput('info', "Packets Recv:\t" + str(packets_received))
    LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
    assert packets_received == packets_sent, "failed to ping Host3"


def test_2(**kwargs):
    switch1 = kwargs.get('device1', None)
    wrkstn1 = kwargs.get('device2', None)

    LogOutput('info', "test 2")

    retStruct = InterfaceIpConfig(deviceObj=device1,
                                  interface="1.10",
                                  addr="192.168.1.4", mask=24, config=True)

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    retStruct = Dot1qEncapsulation(deviceObj=device1, subInterface="1.10",
                                   dot1q=True, vlan=10, enable=True)

    # configure Ip on the host
    retStructObj = wrkstn1.NetworkConfig(ipAddr="192.168.1.1",
                                         netMask="255.255.255.0",
                                         broadcast="192.168.1.255",
                                         interface=wrkstn1.
                                         linkPortMapping['lnk01'], config=True)

    if retStructObj.returnCode() != 0:
        LogOutput('error', "Failed to configure IP on workstation")

    retStruct = wrkstn1.Ping(ipAddr="192.168.1.4", packetCoung=10)
    retCode = retStruct.returnCode()
    assert retCode == 0, "failed to ping switch"

    LogOutput('info', "IPv4 Ping from workstation 1 to switch 1 return \
                       JSON:\n" + str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key='packet_loss')
    packets_sent = retStruct.valueGet(key='packets_transmitted')
    packets_received = retStruct.valueGet(key='packets_received')
    LogOutput('info', "Packets Sent:\t" + str(packets_sent))
    LogOutput('info', "Packets Recv:\t" + str(packets_received))
    LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
    assert packets_received == packets_sent, "failed to ping switch"

# changing Vlan and verifying ping
    retStruct = Dot1qEncapsulation(deviceObj=device1, subInterface="1.10",
                                   dot1q=True, vlan=20, enable=True)

    retStruct = wrkstn1.Ping(ipAddr="192.168.1.4", packetCoung=10)
    retCode = retStruct.returnCode()
    if retCode == 0:
        LogOutput('info', "failed to ping switch")
    LogOutput('info', "IPv4 Ping from workstation 1 to dut01 return JSON:\n" +
              str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key='packet_loss')
    packets_sent = retStruct.valueGet(key='packets_transmitted')
    packets_received = retStruct.valueGet(key='packets_received')
    LogOutput('info', "Packets Sent:\t" + str(packets_sent))
    LogOutput('info', "Packets Recv:\t" + str(packets_received))
    LogOutput('info', "Packet Loss %:\t" + str(packet_loss))

    if retStruct.returnCode() != 0:
        LogOutput('info', "Failed to ping loopback.\
                  Negative test case passed")

    devIntRetStruct1 = AddPortToVlan(deviceObj=device1,
                                     vlanId=20,
                                     interface=device1.
                                     linkPortMapping['lnk02'],
                                     access=True,
                                     config=True)

    retStruct = wrkstn2.Ping(ipAddr="192.168.1.4", packetCoung=10)
    retCode = retStruct.returnCode()
    assert retCode == 0, "failed to ping switch1"

    LogOutput('info', "ping workstation 2 to switch return \
                       JSON:\n" + str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key='packet_loss')
    packets_sent = retStruct.valueGet(key='packets_transmitted')
    packets_received = retStruct.valueGet(key='packets_received')
    LogOutput('info', "Packets Sent:\t" + str(packets_sent))
    LogOutput('info', "Packets Recv:\t" + str(packets_received))
    LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
    assert packets_received == packets_sent, "failed to ping switch1"


def test_3(**kwargs):

    device1 = kwargs.get('device1', None)
    wrkstn1 = kwargs.get('device2', None)

    LogOutput('info', "Delete vlan and ping the switch")
    devVlanRetStruct1 = AddVlan(deviceObj=device1,
                                vlanId=10,
                                config=False)

    if devVlanRetStruct1.returnCode() != 0:
        LogOutput('error',
                  "Failed to delete vlan")
        assert(False)
    else:
        LogOutput('info', "Passed deleting Vlan")

    retStruct = wrkstn1.Ping(ipAddr="192.168.1.4", packetCoung=10)
    retCode = retStruct.returnCode()
    assert retCode == 0, "failed to ping switch"

    LogOutput('info', "IPv4 Ping from workstation1 to switch 1 return \
                       JSON:\n" + str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key='packet_loss')
    packets_sent = retStruct.valueGet(key='packets_transmitted')
    packets_received = retStruct.valueGet(key='packets_received')
    LogOutput('info', "Packets Sent:\t" + str(packets_sent))
    LogOutput('info', "Packets Recv:\t" + str(packets_received))
    assert packets_received == packets_sent, "failed to ping switch"


class Test_subInt:

    def setup_class(cls):

        # Test object will parse command line and formulate the env
        Test_subInt.testObj = testEnviron(topoDict=topoDict)
        #    Get topology object
        Test_subInt.topoObj = Test_subInt.testObj.topoObjGet()

    def teardown_class(cls):
        Test_subInt.topoObj.terminate_nodes()

    def test_l3_route(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston1Obj = self.topoObj.deviceObjGet(device="wrkston02")
        wrkston2Obj = self.topoObj.deviceObjGet(device="wrkston03")
        retValue = l3_route(device1=dut01Obj, device2=dut02Obj,
                            device3=wrkston1Obj, device4=wrkston2Obj)

    '''def test_test_2(self):
        LogOutput('info', "configuration")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="wrkston01")
        retValue = test_2(device1=dut01Obj, device2=dut02Obj)

    def test_test_3(self):
        LogOutput('info', "Reverting the configuration")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="wrkston01")
        retValue = test_3(device1=dut01Obj, device2=dut02Obj)'''

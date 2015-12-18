#!/usr/bin/env python

# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
#
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
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch.OVS import *

#
# The purpose of this test is to test
# functionality of ping Ip-App
#
# For this test, we need below topology
#
# S1 [interface 1]<--->[interface 1] S2
# S2 [interface 2]<--->[interface 2] S3

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02 dut03",
            "topoDevices": "dut01 dut02 dut03",
            "topoLinks": "lnk01:dut01:dut02,lnk02:dut02:dut03",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch"}


def configure(**kwargs):
    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)

    #Enabling interface 1 SW1
    LogOutput('info', "Enabling interface1 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=True,
                                interface=switch1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interafce1 on SW1"

    #Enabling interface 1 SW2
    LogOutput('info', "Enabling interface1 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True,
                                interface=switch2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface1 on SW2"

    #Enabling interface 2 SW2
    LogOutput('info', "Enabling interface2 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True,
                                interface=switch2.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface2 on SW2"

    #Enabling interface 2 SW3
    LogOutput('info', "Enabling interface2 on SW3")
    retStruct = InterfaceEnable(deviceObj=switch3, enable=True,
                                interface=switch3.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface2 on SW3"

    #Entering interface for link 1 SW1, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr="10.0.30.1", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Entering interface for link 1 SW1, giving an IPv6 address
    LogOutput('info', "Configuring IPv6 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr="1030::1", mask=120,
                                  ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address"

    #Entering interface for link 1 SW2, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk01'],
                                  addr="10.0.30.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Entering interface for link 1 SW2, giving an IPv6 address
    LogOutput('info', "Configuring IPv6 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk01'],
                                  addr="1030::2", mask=120, ipv6flag=True,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address"

    #Entering interface for link 2 SW2, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 2 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk02'],
                                  addr="10.0.40.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Entering interface for link 2 SW2, giving an IPv6 address
    LogOutput('info', "Configuring IPv6 address on link 2 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk02'],
                                  addr="2030::2", mask=120, ipv6flag=True,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address"

    #Entering interface for link 2 SW3, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 2 SW3")
    retStruct = InterfaceIpConfig(deviceObj=switch3,
                                  interface=switch3.linkPortMapping['lnk02'],
                                  addr="10.0.40.1", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Entering interface for link 2 SW3, giving an IPv6 address
    LogOutput('info', "Configuring IPv6 address on link 2 SW3")
    retStruct = InterfaceIpConfig(deviceObj=switch3,
                                  interface=switch3.linkPortMapping['lnk02'],
                                  addr="2030::1", mask=120, ipv6flag=True,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address"

    LogOutput('info', "Configuring switch 1 and 2 static ipv4 routes")
    retStruct = IpRouteConfig(deviceObj=switch1, route="10.0.40.0", mask=24,
                              nexthop="10.0.30.2", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure ipv4 address route"

    LogOutput('info', "Configuring switch 3 and 2 static ipv4 routes")
    retStruct = IpRouteConfig(deviceObj=switch3, route="10.0.30.0", mask=24,
                              nexthop="10.0.40.2", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure ipv4 address route"

    #Entering vtysh SW1
    retStruct = switch1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    #Entering vtysh SW2
    retStruct = switch2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    #Entering vtysh SW3
    retStruct = switch3.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    LogOutput('info', "Configuring switch 1 static ipv6 routes")
    devIntRetStruct = switch1.DeviceInteract(command="conf t")
    devIntRetStruct = switch1.DeviceInteract(command="ipv6"
                                             " route 2030::/120 1030::2")
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure ipv6 address route"

    devIntRetStruct = switch1.DeviceInteract(command="exit")

    LogOutput('info', "Configuring switch 3 static ipv6 routes")
    devIntRetStruct = switch3.DeviceInteract(command="conf t")
    devIntRetStruct = switch3.DeviceInteract(command="ipv6"
                                             " route 1030::/120 2030::2")
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure ipv6 address route"

    devIntRetStruct = switch3.DeviceInteract(command="exit")

    devIntRetStruct = switch1.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)
    devIntRetStruct = switch2.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)
    devIntRetStruct = switch3.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)


def ping_basic(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)

    #Ping IPv4-address from switch1 to switch2
    LogOutput('info', "Test ping IPv4-address from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="ping 10.0.30.2")
    retCode = devIntRetStruct.get('returnCode')

    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch1 to switch2"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 10.0.30.2 (10.0.30.2): 100 data bytes' in retBuffer, "Ping"
    " from switch1 to switch2 failed"

    #Ping IPv4-address from switch2 to switch1
    LogOutput('info', "Test ping IPv4-address from switch2 to switch1")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.0.30.1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch2 to switch1"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 10.0.30.1 (10.0.30.1): 100 data bytes' in retBuffer, "Ping"
    " from switch2 to switch1 failed"


def ping_with_options(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)

    #Ping IPv4-address from switch1 to switch2 with the data-fill parameter
    LogOutput('info', "Test ping IPv4-address from switch1 to switch2"
              " with the data-fill parameter")
    devIntRetStruct = switch1.DeviceInteract(command="ping 10.0.30.2"
                                             " data-fill dee")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch1 to switch2 with the data-fill parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 10.0.30.2 (10.0.30.2): 100 data bytes' in retBuffer, "Ping"
    " IPv4-address from switch1 to switch2 with the data-fill parameter failed"

    #Ping IPv4-address from switch1 to switch2 with the datagram-size parameter
    LogOutput('info', "Test ping IPv4-address from switch1 to switch2"
              " with the datagram-size parameter ")
    devIntRetStruct = switch1.DeviceInteract(command="ping 10.0.30.2"
                                             " datagram-size 200")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch1 to switch2 with the datagram-size parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 10.0.30.2 (10.0.30.2): 200 data bytes' in retBuffer, "Ping"
    " IPv4-address from switch1 to switch2"
    " with the datagram-size parameter failed"

    #Ping IPv4-address from switch1 to switch2 with the interval parameter
    LogOutput('info', "Test ping IPv4-address from switch1 to switch2"
              " with the interval parameter")
    devIntRetStruct = switch1.DeviceInteract(command="ping 10.0.30.2"
                                             " interval 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch1 to switch2 with the interval parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 10.0.30.2 (10.0.30.2): 100 data bytes' in retBuffer, "Ping"
    " IPv4-address from switch1 to switch2 with the interval parameter failed"

    #Ping IPv4-address with the repetition parameter from switch1 to switch2
    LogOutput('info', "Test ping IPv4-address from switch1 to switch2"
              " with the repetition parameter")
    devIntRetStruct = switch1.DeviceInteract(command="ping 10.0.30.2"
                                             " repetitions 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch1 to switch2 with the repetition parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 10.0.30.2 (10.0.30.2): 100 data bytes' in retBuffer, "Ping"
    " IPv4-address from switch1 to switch2"
    " with the repetition parameter failed"

    #Ping IPv4-address with the timeout parameter from switch1 to switch2
    LogOutput('info', "Test ping IPv4-address from switch1 to switch2"
              " with the timeout parameter")
    devIntRetStruct = switch1.DeviceInteract(command="ping 10.0.30.2"
                                             " timeout 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch1 to switch2 with the timeout parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 10.0.30.2 (10.0.30.2): 100 data bytes' in retBuffer, "Ping"
    " IPv4-address from switch1 to switch2 with the timeout parameter failed"

    #Ping IPv4-address with the TOS parameter from switch1 to switch2
    LogOutput('info', "Test ping IPv4-address from switch1 to switch2"
              " with the TOS parameter")
    devIntRetStruct = switch1.DeviceInteract(command="ping 10.0.30.2"
                                             " tos 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch1 to switch2 with the TOS parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 10.0.30.2 (10.0.30.2): 100 data bytes' in retBuffer, "Ping"
    " IPv4-address from switch1 to switch2 with the TOS parameter failed"


def ping_extended_options(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)

    #Ping IPv4-address with the ip-option record-route
    LogOutput('info', "Test ping IPv4-address from switch1 to switch2"
              " with the ip-option record-route")
    devIntRetStruct = switch1.DeviceInteract(command="ping 10.0.30.2"
                                             " ip-option record-route")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch1 to switch2 with the ip-option record-route"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'RR:' in retBuffer, "Ping from switch1"
    " to switch2 with the ip-option record-route failed"

    #Ping IPv4-address with the ip-option include-timestamp
    LogOutput('info', "Test ping IPv4-address from switch1 to switch2"
              " with the ip-option include-timestamp")
    devIntRetStruct = switch1.DeviceInteract(command="ping 10.0.30.2"
                                             " ip-option include-timestamp")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch1 to switch2 with the ip-option include-timestamp"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'TS:' in retBuffer, "Ping from switch1 to switch2"
    " with the ip-option include-timestamp failed"

    #Ping IPv4-address with the ip-option include-timestamp-and-address
    LogOutput('info', "Test ping IPv4-address from switch1 to switch2"
              " with the ip-option include-timestamp-and-address")
    devIntRetStruct = switch1.DeviceInteract(command="ping 10.0.30.2"
                                             " ip-option "
                                             "include-timestamp-and-address")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch1 to switch2 with the ip-option include-timestamp-and-address"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'TS:' in retBuffer, "Ping from"
    " switch1 to switch2 with the ip-option"
    " include-timestamp-and-address failed"


def ping6_basic(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)

    #Ping6 from switch1 to switch2
    LogOutput('info', "Test ping6 IPv6-address from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="ping6 1030::2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping6 IPv6-address"
    " from switch1 to switch2"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 1030::2 (1030::2): 100 data bytes' in retBuffer, "Ping6"
    "from switch1 to switch2 failed"

    #Ping6 from switch2 to switch1
    LogOutput('info', "Test ping6 IPv6-address from switch2 to switch1")
    devIntRetStruct = switch2.DeviceInteract(command="ping6 1030::1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping6 IPv6-address"
    " from switch2 to switch1"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 1030::1 (1030::1): 100 data bytes' in retBuffer, "Ping6"
    " from switch2 to switch1 passed"


def ping6_with_options(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)

    #Ping6 from switch2 to switch1 with the data-fill parameter
    LogOutput('info', "Test ping6 IPv6-address from switch2 to switch1"
              " with the data-fill parameter")
    devIntRetStruct = switch2.DeviceInteract(command="ping6 1030::1"
                                             " data-fill dee")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping6 IPv6-address"
    " with the data-fill parameter from switch2 to switch1"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 1030::1 (1030::1): 100 data bytes' in retBuffer, "Ping6"
    " from switch2 to switch1 with the data-fill parameter failed"

    #Ping6 from switch2 to switch1 with the datagram-size parameter
    LogOutput('info', "Test ping6 IPv6-address from switch2 to switch1"
              " with the datagram-size parameter")
    devIntRetStruct = switch2.DeviceInteract(command="ping6 1030::1"
                                             " datagram-size 200")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping6 IPv6-address"
    " from switch2 to switch1 with the datagram-size parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 1030::1 (1030::1): 200 data bytes' in retBuffer, "Ping6"
    " from switch2 to switch1 with the datagram-size parameter failed"

    #Ping6 from switch2 to switch1 with the interval parameter
    LogOutput('info', "Test ping6 IPv6-address from switch2 to switch1"
              " with the interval parameter")
    devIntRetStruct = switch2.DeviceInteract(command="ping6 1030::1"
                                             " interval 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping6 IPv6-address"
    " from switch2 to switch1 with the interval parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 1030::1 (1030::1): 100 data bytes' in retBuffer, "Ping6"
    " from switch2 to switch1 with the interval parameter failed"

    #Ping6 from switch2 to switch1 with the repetition parameter
    LogOutput('info', "Test ping6 IPv6-address from switch2 to switch1"
              " with the repetitions parameter")
    devIntRetStruct = switch2.DeviceInteract(command="ping6 1030::1"
                                             " repetitions 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping6 IPv6-address"
    " from switch2 to switch1 with the repetition parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 1030::1 (1030::1): 100 data bytes' in retBuffer, "Ping6"
    " from switch2 to switch1 with the repetition parameter failed"


def ping_multihop_test(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)

    #Ping IPv4-address from switch1 to switch3
    LogOutput('info', "Test ping with multihop IPv4 and IPv6 address")
    LogOutput('info', "Test ping IPv4-address from switch1 to switch3")
    devIntRetStruct = switch1.DeviceInteract(command="ping 10.0.40.1")
    retCode = devIntRetStruct.get('returnCode')

    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch1 to switch3"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 10.0.40.1 (10.0.40.1): 100 data bytes' in retBuffer, "Ping"
    " from switch1 to switch3 failed"

    #Ping IPv6-address from switch1 to switch3
    LogOutput('info', "Test ping IPv6-address from switch3 to switch1")
    devIntRetStruct = switch3.DeviceInteract(command="ping6 1030::1")
    retCode = devIntRetStruct.get('returnCode')

    assert retCode == 0, "Failed to ping IPv6-address"
    " from switch3 to switch1"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 1030::1 (1030::1): 100 data bytes' in retBuffer, "Ping6"
    " from switch3 to switch1 failed"


def exit_vtysh_shell(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)

    retStruct = switch1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    retStruct = switch2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    retStruct = switch3.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"


class Test_ping:

    def setup_class(cls):
        # Test objaect will parse command line and formulate the env
        Test_ping.testObj = testEnviron(topoDict=topoDict,
                                        defSwitchContext="vtyShell")
        # Get ping topology object
        Test_ping.pingTopoObj = Test_ping.testObj.topoObjGet()

    def teardown_class(cls):

        Test_ping.pingTopoObj.terminate_nodes()

    def test_ping_full(self):

        # Get Device objects
        dut01Obj = self.pingTopoObj.deviceObjGet(device="dut01")
        dut02Obj = self.pingTopoObj.deviceObjGet(device="dut02")
        dut03Obj = self.pingTopoObj.deviceObjGet(device="dut03")
        configure(switch1=dut01Obj, switch2=dut02Obj, switch3=dut03Obj)

        LogOutput('info', "### Basic ping tests ###")
        ping_basic(switch1=dut01Obj, switch2=dut02Obj, switch3=dut03Obj)

        LogOutput('info', "\n### Ping with options tests ###")
        ping_with_options(switch1=dut01Obj, switch2=dut02Obj, switch3=dut03Obj)

        LogOutput('info', "\n### Ping with extended options tests ###")
        ping_extended_options(switch1=dut01Obj,
                              switch2=dut02Obj, switch3=dut03Obj)

        LogOutput('info', "\n### Basic ping6 tests ###")
        ping6_basic(switch1=dut01Obj,
                    switch2=dut02Obj, switch3=dut03Obj)

        LogOutput('info', "\n### Ping6 test with options ###")
        ping6_with_options(switch1=dut01Obj,
                           switch2=dut02Obj, switch3=dut03Obj)

        LogOutput('info', "\n### Ping multihop test ###")
        ping_multihop_test(switch1=dut01Obj,
                           switch2=dut02Obj, switch3=dut03Obj)

        exit_vtysh_shell(switch1=dut01Obj, switch2=dut02Obj, switch3=dut03Obj)

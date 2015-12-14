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

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02",
            "topoLinks": "lnk01:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch"}


def traceroute(**kwargs):
    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    # systemctl stop zebra
    # /usr/sbin/zebra --detach --pidfile -vSYSLOG:DBG

    # Enabling interface 1 SW1
    LogOutput('info', "Enabling interface1 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=True,
                                interface=switch1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interafce on SW1"
        # caseReturnCode = 1

    # Enabling interface 1 SW1
    LogOutput('info', "Enabling interface1 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True,
                                interface=switch2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interafce on SW1"
        # caseReturnCode = 1

    # Entering interface for link 1 SW1, giving an ip address
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr="10.0.30.1", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an ipv4 address"
        # caseReturnCode = 1

    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr="1030::1", mask=120,
                                  ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an ipv6 address"
        # caseReturnCode = 1

    # Entering interface for link 1 SW2, giving an ping ip address
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk01'],
                                  addr="10.0.30.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an ipv4 address"
        # caseReturnCode = 1

    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk01'],
                                  addr="1030::2", mask=120, ipv6flag=True,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an ipv6 address"
        # caseReturnCode = 1
    #Entering vtysh SW1

    retStruct = switch1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    LogOutput('info', "Test traceroute ip-address from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute 10.0.30.2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute ip-address \
from switch1 to switch2"

    LogOutput('info', "Test traceroute Host from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute switch2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute Host from switch1 to switch2"

    LogOutput('info', "Test traceroute ip-address maxttl \
from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
10.0.30.2 maxttl 30")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute ip-address maxttl \
from switch1 to switch2"

    LogOutput('info', "Test traceroute Host maxttl from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
switch2 maxttl 30")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute Host maxttl \
from switch1 to switch2"

    LogOutput('info', "Test traceroute ip-address minttl \
from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
10.0.30.2 minttl 1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute ip-address minttl \
from switch1 to switch2"

    LogOutput('info', "Test traceroute Host minttl from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
switch2 minttl 1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute Host minttl from \
switch1 to switch2"

    LogOutput('info', "Test traceroute ip-address Dstport from \
switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute 10.0.30.2 \
dstport 33434")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute ip-address Dstport \
from switch1 to switch2"

    LogOutput('info', "Test traceroute Host Dstport from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
switch2 dstport 33434")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute Host Dstport \
from switch1 to switch2"

    LogOutput('info', "Test traceroute ip-address timeout \
from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute 10.0.30.2 \
timeout 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute ip-address timeout \
from switch1 to switch2"

    LogOutput('info', "Test traceroute Host timeout from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
switch2 timeout 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute Host timeout \
from switch1 to switch2"

    LogOutput('info', "Test traceroute ip-address probes \
from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute 10.0.30.2 \
probes 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute ip-address probes \
from switch1 to switch2"

    LogOutput('info', "Test traceroute Host probes from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
switch2 probes 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute Host probes \
from switch1 to switch2"

    LogOutput('info', "Test traceroute ip-address ip-option loosesource route \
from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute 10.0.30.2 \
ip-option loosesourceroute 10.0.30.9")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute ip-address ip-option \
loosesource route from switch1 to switch2"

    LogOutput('info', "Test traceroute Host ip-option loosesource route \
from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute switch2 \
ip-option loosesourceroute 10.0.30.9")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute Host ip-option \
loosesource route from switch1 to switch2"

    LogOutput('info', "Test traceroute6 ip-address from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 1030::2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 ip-address \
from switch1 to switch2"

    LogOutput('info', "Test traceroute6 Host from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 switch1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 Host from switch1 to switch2"

    LogOutput('info', "Test traceroute6 ip-address maxttl \
from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
1030::2 maxttl 30")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 ip-address maxttl \
from switch1 to switch2"

    LogOutput('info', "Test traceroute6 Host maxttl from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
switch1 maxttl 30")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 Host maxttl \
from switch1 to switch2"

    LogOutput('info', "Test traceroute6 ip-address Dstport \
from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
1030::2 dstport 33434")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 ip-address Dstport \
from switch1 to switch2"

    LogOutput('info', "Test traceroute6 Host Dstport from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
switch1 dstport 33434")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 Host Dstport \
from switch1 to switch2"

    LogOutput('info', "Test traceroute6 ip-address timeout \
from switch1 to swith2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
1030::2 timeout 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 ip-address timeout \
from switch1 to switch2"

    LogOutput('info', "Test traceroute6 Host timeout from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
switch1 timeout 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 Host timeout \
from switch1 to switch2"

    LogOutput('info', "Test traceroute6 ip-address probes \
from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
1030::2 probes 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 ip-address probes \
from switch1 to switch2"

    LogOutput('info', "Test traceroute6 Host probes from switch1 to switch2")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
switch1 probes 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 Host probes \
from switch1 to switch2"

    #Entering vtysh SW2

    retStruct = switch2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    LogOutput('info', "Test traceroute ip-address from switch2 to switch1")
    devIntRetStruct = switch2.DeviceInteract(command="traceroute 10.0.30.1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute ip-address \
from switch2 to switch1"

    LogOutput('info', "Test traceroute Host from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute switch1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute Host from switch2 to switch1"

    LogOutput('info', "Test traceroute ip-address maxttl \
from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
10.0.30.1 maxttl 30")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute ip-address maxttl \
from switch2 to switch1"

    LogOutput('info', "Test traceroute Host maxttl from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
switch1 maxttl 30")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute Host maxttl \
from switch2 to switch1"

    LogOutput('info', "Test traceroute ip-address minttl \
from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
10.0.30.1 minttl 1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute ip-address minttl \
from switch2 to switch1"

    LogOutput('info', "Test traceroute Host minttl from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
switch1 minttl 1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute Host minttl \
from switch2 to switch1"

    LogOutput('info', "Test traceroute ip-address Dstport \
from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
10.0.30.1 dstport 33434")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute ip-address Dstport \
from switch2 to switch1"

    LogOutput('info', "Test traceroute Host Dstport from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
switch1 dstport 33434")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute Host Dstport \
from switch2 to switch1"

    LogOutput('info', "Test traceroute ip-address timeout \
from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
10.0.30.1 timeout 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute ip-address timeout \
from switch2 to switch1"

    LogOutput('info', "Test traceroute Host timeout from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
switch1 timeout 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute Host timeout \
from switch2 to switch1"

    LogOutput('info', "Test traceroute ip-address probes \
from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
10.0.30.1 probes 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute ip-address probes \
from switch2 to switch1"

    LogOutput('info', "Test traceroute Host probes from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
switch1 probes 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute Host probes \
from switch2 to switch1"

    LogOutput('info', "Test traceroute ip-address ip-option \
loosesource route from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute \
10.0.30.1 ip-option loosesourceroute 10.0.30.9")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute ip-address \
ip-option loosesource route from switch2 to switch1"

    LogOutput('info', "Test traceroute Host ip-option loosesource route \
from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute switch1 \
ip-option loosesourceroute 10.0.30.9")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute Host ip-option \
loosesource route from switch2 to switch1"

    LogOutput('info', "Test traceroute6 ip-address from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 1030::2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 ip-address \
from switch2 to switch1"

    LogOutput('info', "Test traceroute6 Host from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 switch2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 Host from switch2 to switch1"

    LogOutput('info', "Test traceroute6 ip-address maxttl \
from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
1030::2 maxttl 30")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 ip-address maxttl \
from switch2 to switch1"

    LogOutput('info', "Test traceroute6 Host maxttl from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
switch2 maxttl 30")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 Host maxttl \
from switch2 to switch1"

    LogOutput('info', "Test traceroute6 ip-address Dstport \
from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
1030::2 dstport 33434")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 ip-address Dstport \
from switch2 to switch1"

    LogOutput('info', "Test traceroute6 Host Dstport from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
switch2 dstport 33434")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 Host Dstport \
from switch2 to switch1"

    LogOutput('info', "Test traceroute6 ip-address timeout \
from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
1030::1 timeout 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 ip-address timeout \
from switch2 to switch1"

    LogOutput('info', "Test traceroute6 Host timeout from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
switch2 timeout 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 Host timeout \
from switch2 to switch1"

    LogOutput('info', "Test traceroute6 ip-address probes \
from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
1030::1 probes 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 ip-address probes \
from switch2 to switch1"

    LogOutput('info', "Test traceroute6 Host probes from switch2 to switch1")
    devIntRetStruct = switch1.DeviceInteract(command="traceroute6 \
switch2 probes 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 Host probes \
from switch2 to switch1"

    retStruct = switch1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    retStruct = switch2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"


class Test_traceroute:

    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_traceroute.testObj = testEnviron(topoDict=topoDict,
                                              defSwitchContext="vtyShell")
        # Get topology object
        Test_traceroute.topoObj = Test_traceroute.testObj.topoObjGet()

    def teardown_class(cls):

        Test_traceroute.topoObj.terminate_nodes()

    def test_traceroute(self):

        # GEt Device objects
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        retValue = traceroute(switch1=dut01Obj, switch2=dut02Obj)
        if retValue != 0:
            assert "Test failed"
        else:
            LogOutput('info', "\n### Test passed ###\n")

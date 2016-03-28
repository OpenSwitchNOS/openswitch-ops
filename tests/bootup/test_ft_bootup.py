#!/usr/bin/env python

# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
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
from platform_err_msgs import *

#
# The purpose of this test is to test
# functionality of ping Ip-App
#
# For this test, we need below topology
#
# +---------+            +----------+          +-----------+
# |         |            |          |          |           |
# |         |            |          |          |           |
# | Host1   +------------+ Switch1  +----------+ Switch2   |
# |         |            |          |          |           |
# |         |            |          |          |           |
# +---------+            +----------+          +-----------+
#


# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02 wrkston01",
            "topoLinks": "lnk01:wrkston01:dut01,lnk02:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation"}

hw_daemons = ['ops-switchd', 'ops-sysd', 'ops-pmd', 'ops-tempd', 'ops-powerd', 'ops-ledd', 'ops-fand']

def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))

def configure(**kwargs):
    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    host1 = kwargs.get('host1', None)

    #Host1 configuration
    LogOutput('info', "Configuring host1 with IPv4 address")
    retStruct = host1.NetworkConfig(ipAddr="10.0.30.1",
                                    netMask="255.255.255.0",
                                    broadcast="10.0.30.255",
                                    interface=host1.linkPortMapping['lnk01'],
                                    config=True)
    if retStruct.returnCode() != 0:
        assert "Failed to configure IPv4 address on Host1"

    #Enabling interface 1 SW1
    LogOutput('info', "Enabling interface1 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=True,
                                interface=switch1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface1 on SW1"

    #Enabling interface 2 SW1
    LogOutput('info', "Enabling interface2 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=True,
                                interface=switch1.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface2 on SW1"

    #Entering interface for link 1 SW1, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr="10.0.30.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Entering interface for link 2 SW1, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 2 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk02'],
                                  addr="10.0.10.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Enabling interface 2 SW2
    LogOutput('info', "Enabling interface2 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True,
                                interface=switch2.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface2 on SW2"

    #Entering interface for link 2 SW2, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk02'],
                                  addr="10.0.10.3", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Configuring static routes
    LogOutput('info', "Configuring static IPv4 route on host1")
    retStruct = host1.IPRoutesConfig(config=True,
                                     destNetwork="10.0.10.0",
                                     netMask=24, gateway="10.0.30.2")
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure static IPv4 route on host1"

    LogOutput('info', "Configuring static IPv4 route on switch2")
    retStruct = IpRouteConfig(deviceObj=switch2, route="10.0.30.0", mask=24,
                              nexthop="10.0.10.2", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure static IPv4 route on switch2"

    #Entering vtysh SW1
    retStruct = switch1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    #Entering vtysh SW2
    retStruct = switch2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    devIntRetStruct = switch1.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)
    devIntRetStruct = switch2.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)

    cmdOut = host1.cmd("netstat -rn")
    LogOutput('info', "IPv4 Route table for workstation 1:\n" + str(cmdOut))


def check_bootup(**kwargs):
    switch2 = kwargs.get('switch2', None)
    cmdOut = switch2.cmd('exit')

    cmdOut = switch2.cmd('ps -e')
    LogOutput('info', "\nList of platform processes running on SW2:\n")

    for daemon in hw_daemons:
        if daemon in str(cmdOut):
            LogOutput('info', "%s daemon is running" %(daemon))
        else:
            assert False, LogOutput('info', "%s daemon is not running" %(daemon))

    cmdOut = switch2.cmd('vtysh')


def check_segfault(**kwargs):
    switch2 = kwargs.get('switch2', None)
    cmdOut = switch2.cmd('exit')
    cmdOut = switch2.cmd('cp /var/log/messages /messages')

    LogOutput('info', "Test to find error messages in log file while bootup")
    for err in msgs:
        shCmd = 'cat /messages | grep "' + err + '"'
        cmdOut = switch2.cmd(shCmd)
	lst = cmdOut.split('\n')
	lst.pop(0)
        for item in lst:
	    if err in item:
		print item
                assert False, LogOutput('info', "There is an error while system bootup")

    cmdOut = switch2.cmd('vtysh')


def ping_basic(**kwargs):

    host1 = kwargs.get('host1', None)
    switch2 = kwargs.get('switch2', None)

    #Ping IPv4-address from switch2 to host1
    LogOutput('info', "Test ping IPv4-address from switch2 to host1")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.0.30.1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch2 to host1"

    retBuffer = devIntRetStruct.get('buffer')
    assert '0% packet loss' in retBuffer, "Ping"
    " from switch2 to host1 failed"


def ping_network_unreachable(**kwargs):

    switch2 = kwargs.get('switch2', None)

    #Ping network unreachable case
    LogOutput('info', "Test ping network unreachable case")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.11.1.1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'Network is unreachable' in retBuffer, "Failure"
    " case test is unsuccessful"


def ping_destination_unreachable(**kwargs):

    switch2 = kwargs.get('switch2', None)

    #Ping destination unreachable case
    LogOutput('info', "Test ping destination host unreachable case")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.0.10.5")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'Destination Host Unreachable' in retBuffer, "Failure"
    " case test is unsuccessful"


def ping_unknown_host(**kwargs):

    switch2 = kwargs.get('switch2', None)

    #Ping unknown host
    LogOutput('info', "Test ping unknown host case")
    devIntRetStruct = switch2.DeviceInteract(command="ping asdfrgqweewwe")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping hostname"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'unknown host' in retBuffer, "Failure"
    " case test is unsuccessful"


def cleanup(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    host1 = kwargs.get('host1', None)

    retStruct = switch1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    LogOutput('info', "\nPerforming cleanup")
    LogOutput('info', "unconfiguring static ipv4 route on host1")
    retStruct = host1.IPRoutesConfig(config=False,
                                     destNetwork="10.0.10.0",
                                     netMask=24, gateway="10.0.30.2")
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to unconfigure static ipv4 route on host1"

    LogOutput('info', "Unconfiguring host1 with IPv4 address")
    retStruct = host1.NetworkConfig(ipAddr="10.0.30.1",
                                    netMask="255.255.255.0",
                                    broadcast="10.0.30.255",
                                    interface=host1.linkPortMapping['lnk01'],
                                    config=False)
    if retStruct.returnCode() != 0:
        assert "Failed to unconfigure IPv4 address on Host1"

    #SW1
    LogOutput('info', "Unconfiguring IPv4 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr="10.0.30.2", mask=24, config=False)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to unconfigure an IPv4 address"

    LogOutput('info', "Unconfiguring IPv4 address on link 2 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk02'],
                                  addr="10.0.10.2", mask=24, config=False)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to unconfigure an ipv4 address"

    LogOutput('info', "Disabling interface1 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=False,
                                interface=switch1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to disable interface1 on SW1"

    LogOutput('info', "Disabling interface2 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=False,
                                interface=switch1.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to disable interface2 on SW1"

    #SW2
    LogOutput('info', "Unconfiguring IPv4 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk02'],
                                  addr="10.0.10.3", mask=24, config=False)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to unconfigure an IPv4 address"

    #Unconfiguring static routes
    retStruct = IpRouteConfig(deviceObj=switch2, route="10.0.30.0", mask=24,
                              nexthop="10.0.10.2", config=False)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to unconfigure static ipv4 route on switch2"

    LogOutput('info', "Disabling interface2 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=False,
                                interface=switch2.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to disable interface2 on SW2"

    retStruct = switch2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"



class Test_bootup:

    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_bootup.testObj = testEnviron(topoDict=topoDict,
                                        defSwitchContext="vtyShell")
        # Get ping topology object
        Test_bootup.bootupTopoObj = Test_bootup.testObj.topoObjGet()

    def teardown_class(cls):

        Test_bootup.bootupTopoObj.terminate_nodes()

    def test_ping_full(self):

        # Get Device objects
        dut01Obj = self.bootupTopoObj.deviceObjGet(device="dut01")
        dut02Obj = self.bootupTopoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.bootupTopoObj.deviceObjGet(device="wrkston01")
        configure(switch1=dut01Obj, switch2=dut02Obj, host1=wrkston01Obj)

        LogOutput('info', "\n### Checking hardware daemons initialization ###")
        check_bootup(host1=wrkston01Obj, switch1=dut01Obj, switch2=dut02Obj)

        LogOutput('info', "\n### Checking for segmentation fault in log messages ###")
        check_segfault(host1=wrkston01Obj, switch1=dut01Obj, switch2=dut02Obj)

        LogOutput('info', "\n### Basic ping tests ###")
        ping_basic(host1=wrkston01Obj, switch1=dut01Obj, switch2=dut02Obj)

        LogOutput('info', "\n### Ping failure test cases ###")
        ping_network_unreachable(switch2=dut02Obj)
        ping_destination_unreachable(switch2=dut02Obj)
        ping_unknown_host(switch2=dut02Obj)

        cleanup(switch1=dut01Obj, switch2=dut02Obj, host1=wrkston01Obj)

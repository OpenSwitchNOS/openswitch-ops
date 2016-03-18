#!/usr/bin/python

# (c) Copyright 2015-2016 Hewlett Packard Enterprise Development LP
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
            "topoType" : "virtual",
            "topoTarget": "dut01",
            "topoDevices": "dut01 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,lnk02:dut01:wrkston02",
            "topoFilters": "dut01:system-category:switch,wrkston01:system-category:workstation,wrkston02:system-category:workstation"}

PING_BYTES = 128
PING_CNT = 10

def verify_stats(switch, command):
    # Retry loop around tx and rx stats.
    for iteration in range(0, 5):
        pass_cases = 0
        returnStructure = switch.DeviceInteract(command="show ip interface 1")
        buf = returnStructure.get('buffer')
        rx = dict()
        tx = dict()
        rxTokens = re.findall(r'RX\s*\r\n\s*ucast:\s*(\d*)\s*packets,\s*(\d*)\s*bytes\s*\r\n\s*', buf)
        txTokens = re.findall(r'RX\s*\r\n\s*ucast:\s*(\d*)\s*packets,\s*(\d*)\s*bytes\s*\r\n\s*', buf)
        if rxTokens:
            rx['packets'] = rxTokens[0][0]
            rx['bytes'] = rxTokens[0][1]
        if txTokens:
            tx['packets'] = txTokens[0][0]
            tx['bytes'] = txTokens[0][1]
        if int(rx['packets']) < PING_CNT:
            LogOutput('info', "Retrying statistic - waiting for rx_packets to update")
            Sleep(seconds=5, message="\nWaiting")
            continue
        pass_cases = pass_cases + 1
        if int(tx['packets']) < PING_CNT:
            LogOutput('info', "Retrying statistic - waiting for tx_packets to update")
            Sleep(seconds=5, message="\nWaiting")
            continue
        if int(rx['bytes']) < (PING_CNT * PING_BYTES):
            LogOutput('info', "Retrying statistic - waiting for rx_bytes to update")
            Sleep(seconds=5, message="\nWaiting")
            continue
        pass_cases = pass_cases + 1
        if int(tx['bytes']) < (PING_CNT * PING_BYTES):
            LogOutput('info', "Retrying statistic - waiting for tx_bytes to update")
            Sleep(seconds=5, message="\nWaiting")
            continue
        pass_cases = pass_cases + 1
        if pass_cases == 4:
            break

    # Verify RX_packets
    assert int(rx['packets']) >= PING_CNT, "rx_packets wrong."
    # Verify TX_packets
    assert int(tx['packets']) >= PING_CNT, "tx_packets wrong."
    # Verify RX_packets
    assert int(rx['bytes']) >= (PING_CNT * PING_BYTES), "rx_bytes wrong."
    # Verify RX_packets
    assert int(tx['bytes']) >= (PING_CNT * PING_BYTES), "tx_bytes wrong."

def l3_fp_stats_test(**kwargs):

    switch = kwargs.get('switch', None)
    host1 = kwargs.get('host1', None)
    host2 = kwargs.get('host2', None)

    #Enabling interfaces on switch

    LogOutput('info', "Enabling interface1 on switch")
    retStruct = InterfaceEnable(deviceObj=switch, enable=True, interface=switch.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to enable interafce on switch1"

    LogOutput('info', "Enabling interface2 on switch")
    retStruct = InterfaceEnable(deviceObj=switch, enable=True, interface=switch.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to enable interface on switch1"

    interface1=int(switch.linkPortMapping['lnk01'])

    interface2=int(switch.linkPortMapping['lnk02'])

    returnStructure = switch.VtyshShell(enter=True)
    returnCode = returnStructure.returnCode()
    assert returnCode == 0, "Failed to get vtysh config prompt"

    returnStructure = switch.ConfigVtyShell(enter=True)

    LogOutput('info', "Configuring L3 on interface 1")
    returnStructure = switch.DeviceInteract(command="interface 1")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to enter interface context for interface 1"
    returnStructure = switch.DeviceInteract(command="no shutdown")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to perform no shut on interface 1"
    returnStructure = switch.DeviceInteract(command="ip address 2.2.2.1/24")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to configure ip address for interface 1"
    returnStructure = switch.DeviceInteract(command="ipv6 address 1000::1/120")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to configure ipv6 address for interface 1"

    returnStructure = switch.DeviceInteract(command="exit")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to exit interface"

    LogOutput('info', "Configuring L3 on interface 2")
    returnStructure = switch.DeviceInteract(command="interface 2")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to enter interface context for interface 1"
    returnStructure = switch.DeviceInteract(command="no shutdown")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to perform no shut on interface 1"
    returnStructure = switch.DeviceInteract(command="ip address 3.3.3.1/24")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to configure ip address for interface 1"

    returnStructure = switch.DeviceInteract(command="ipv6 address 2000::1/120")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to configure ip address for interface 1"


    returnStructure = switch.DeviceInteract(command="end")
    retCode = returnStructure['returnCode']
    assert retCode == 0, "Failed to exit vtysh config"

    returnStructure = switch.VtyshShell(enter=False)
    returnCode = returnStructure.returnCode()
    assert returnCode == 0, "Failed to exit vtysh prompt"

    #Configure host 1

    LogOutput('info', "\n\n\nConfiguring host 1 ipv4")
    retStruct = host1.NetworkConfig(ipAddr="2.2.2.2", netMask="255.255.255.0", interface=host1.linkPortMapping['lnk01'], broadcast="2.2.2.255", config=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to configure an ipv4 address"

    retStruct = host1.IPRoutesConfig(config=True, destNetwork="3.3.3.0", netMask=24, gateway="2.2.2.1")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    LogOutput('info', "\n\n\nConfiguring host 1 ipv6")
    retStruct = host1.Network6Config(ipAddr="1000::10", netMask=120, interface=host1.linkPortMapping['lnk01'], broadcast="1000::0", config=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to configure an ipv6 address"

    retStruct = host1.IPRoutesConfig(config=True, destNetwork="::", netMask=120, gateway="1000::1", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    #Configure host 2

    LogOutput('info', "\n\n\nConfiguring host 2 ipv4")
    retStruct = host2.NetworkConfig(ipAddr="3.3.3.2", netMask="255.255.255.0", interface=host2.linkPortMapping['lnk02'], broadcast="3.3.3.255", config=True )
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to configure an ipv4 address"

    retStruct = host2.IPRoutesConfig(config=True, destNetwork="2.2.2.0", netMask=24, gateway="3.3.3.1")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    LogOutput('info', "\n\n\nConfiguring host 2 ipv6")
    retStruct = host2.Network6Config(ipAddr="2000::10", netMask=120, interface=host2.linkPortMapping['lnk02'], broadcast="2000::0", config=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to configure an ipv6 address"

    retStruct = host2.IPRoutesConfig(config=True, destNetwork="::", netMask=120, gateway="2000::1", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    #Ping From Host1 to Host 2
    retStruct = host1.Ping(ipAddr="3.3.3.2", packetCount=10)
    retCode = retStruct.returnCode()
    assert retCode == 0, "\n##### Failed to do IPv4 ping 10 packets, Case Failed #####"
    LogOutput('info', "\n##### Ping 10 packets Passed, Case Passed #####\n\n")

    retStruct = host1.Ping(ipAddr="2000::10", packetCount=10, ipv6Flag=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "\n##### Failed to do IPv6 ping, Case Failed #####"
    LogOutput('info', "\n##### Ping Passed, Case Passed #####\n\n")


    returnStructure = switch.VtyshShell(enter=True)
    returnStructure = switch.ConfigVtyShell(enter=True)
    returnStructure = switch.DeviceInteract(command="end")

    verify_stats(switch, "show ip interface 1")
    verify_stats(switch, "show ipv6 interface 1")
    verify_stats(switch, "show ip interface 2")
    verify_stats(switch, "show ip interface 2")


class Test_l3_fp_stasts_ct:

    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_l3_fp_stasts_ct.testObj = testEnviron(topoDict=topoDict)
        # Get topology object
        Test_l3_fp_stasts_ct.topoObj = Test_l3_fp_stasts_ct.testObj.topoObjGet()

    def teardown_class(cls):
        Test_l3_fp_stasts_ct.topoObj.terminate_nodes()

    def test_l3_fp_stats(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        l3_fp_stats_test(switch=dut01Obj, host1=wrkston01Obj, host2=wrkston02Obj)
        LogOutput('info', "\n### Test Passed ###\n")

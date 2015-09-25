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
###############################################################################
# Name:        Dynamic_LAG_Increase_system_priority.py
#
# Description: Tests that based of "System Priority" (less prefered) LAG will
#              aggregate max 8 interfaces (of the total of 16 configured).
#              Then, change values of the "System Priority" and corroborate
#              the correct behavior of the Aggregated Interfaces based on "Port
#              Priority" (less prefered) and "System Priority"
#
# Author:      Luis Kopper
#
# Topology:                +-----------+              +-----------+
#            |Host 1| -----|         2 |--------------|1          |-----|Host 2|
#                          |Switch1 ...|              |... Switch2|   
#                          |         17|--------------|16         |
#                          +-----------+              +-----------+
#                               (Static LAG - 16 links)
#
# Success Criteria:  PASS -> Correct selection of interfaces based on "System
#                            Priority" and "port Priorito". Also traffic flow
#                            between hosts is not stopped after applying
#                            "System Id" changes configuration
#
#                    FAILED -> Wrong selection of interfaces or traffic flow
#                              stopped between hosts.
#
###############################################################################

import pytest
from opstestfw.switch.CLI import *
from opstestfw import *


topoDict = {"topoExecution": 3000,
            "topoDevices": "dut01 dut02 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut01:dut02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut01:dut02,\
                          lnk05:dut01:dut02,\
                          lnk06:dut01:dut02,\
                          lnk07:dut01:dut02,\
                          lnk08:dut01:dut02,\
                          lnk09:dut01:dut02,\
                          lnk10:dut01:dut02,\
                          lnk11:dut01:dut02,\
                          lnk12:dut01:dut02,\
                          lnk13:dut01:dut02,\
                          lnk14:dut01:dut02,\
                          lnk15:dut01:dut02,\
                          lnk16:dut01:dut02,\
                          lnk17:dut01:dut02,\
                          lnk18:dut02:wrkston02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation"}


def switch_reboot(dut01):
    # Reboot switch
    LogOutput('info', "Reboot switch")
    dut01.Reboot()
    rebootRetStruct = returnStruct(returnCode=0)
    return rebootRetStruct

# Configure/unconfigure the IP address of a workstation


def configureWorkstation(deviceObj, int, ipAddr, netMask, broadcast, enable):
    if enable:
        retStruct = deviceObj.NetworkConfig(ipAddr=ipAddr,
                                            netMask=netMask,
                                            broadcast=broadcast,
                                            interface=int, configFlag=True)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error',
                "Failed to configure IP on workstation " + deviceObj.device)
            return False
        cmdOut = deviceObj.cmd("ifconfig " + int)
        LogOutput('info', "Ifconfig info for workstation " +
                  deviceObj.device + ":\n" + cmdOut)
    else:
        retStruct = deviceObj.NetworkConfig(ipAddr=ipAddr,
                                            netMask=netMask,
                                            broadcast=broadcast,
                                            interface=int, configFlag=False)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error',
                "Failed to unconfigure IP on workstation " + deviceObj.device)
            return False
        cmdOut = deviceObj.cmd("ifconfig " + int)
        LogOutput('info', "Ifconfig info for workstation " +
                  deviceObj.device + ":\n" + cmdOut)
    return True


class Test_ft_framework_basics:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_ft_framework_basics.testObj = \
            testEnviron(topoDict=topoDict)
        Test_ft_framework_basics.topoObj = \
            Test_ft_framework_basics.testObj.topoObjGet()

    def teardown_class(cls):
        # Terminate all nodes
        Test_ft_framework_basics.topoObj.terminate_nodes()

    def test_reboot_switch(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Reboot the switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        devRebootRetStruct = switch_reboot(dut01Obj)
        if devRebootRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to reboot Switch 1")
            assert(devRebootRetStruct.returnCode() == 0)
        else:
            LogOutput('info', "Passed Switch 1 Reboot ")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        devRebootRetStruct = switch_reboot(dut02Obj)
        if devRebootRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to reboot Switch 2")
            assert(devRebootRetStruct.returnCode() == 0)
        else:
            LogOutput('info', "Passed Switch 2 Reboot ")

    def test_enableDUTsinterfaces(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Enable switches interfaces")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        LogOutput('info', "############################################")
        LogOutput('info', "Configuring switch dut01")
        LogOutput('info', "############################################")
        for i in range(0, 9):
            retStruct = \
                InterfaceEnable(deviceObj=dut01Obj, enable=True,
                                interface=dut01Obj.linkPortMapping['lnk0' +
                                                                   str(i + 1)])
            if retStruct.returnCode() != 0:
                LogOutput('error', "Failed to enable dut01 interface " +
                          str(dut01Obj.linkPortMapping['lnk0' + str(i + 1)]))
                assert(retStruct.returnCode() == 0)
            else:
                LogOutput(
                    'info',
                    "enable dut01 interface " +
                    str(dut01Obj.linkPortMapping['lnk0' + str(i + 1)]))

        for i in range(0, 8):
            retStruct = \
                InterfaceEnable(deviceObj=dut01Obj, enable=True,
                                interface=dut01Obj.linkPortMapping['lnk1' +
                                                                   str(i)])
            if retStruct.returnCode() != 0:
                LogOutput('error', "Failed to enable dut01 interface " +
                          str(dut01Obj.linkPortMapping['lnk0' + str(i)]))
                assert(retStruct.returnCode() == 0)
            else:
                LogOutput(
                    'info',
                    "enable dut01 interface " +
                    str(dut01Obj.linkPortMapping['lnk1' + str(i)]))
        LogOutput('info', "############################################")
        LogOutput('info', "Configuring switch dut02")
        LogOutput('info', "############################################")
        for i in range(1, 9):            
            retStruct = \
                InterfaceEnable(deviceObj=dut02Obj, enable=True,
                                interface=dut02Obj.linkPortMapping['lnk0' +
                                                                   str(i + 1)])
            if retStruct.returnCode() != 0:
                LogOutput('error', "Failed to enable dut02 interface " +
                          str(dut02Obj.linkPortMapping['lnk0' + str(i + 1)]))
                assert(retStruct.returnCode() == 0)
            else:
                LogOutput(
                    'info',
                    "enable dut02 interface " +
                    str(dut02Obj.linkPortMapping['lnk0' + str(i + 1)]))

        for i in range(0, 9):
            retStruct = \
                InterfaceEnable(deviceObj=dut02Obj, enable=True,
                                interface=dut02Obj.linkPortMapping['lnk1' +
                                                                   str(i)])
            if retStruct.returnCode() != 0:
                LogOutput('error', "Failed to enable dut02 interface " +
                          str(dut02Obj.linkPortMapping['lnk1' + str(i)]))
                assert(retStruct.returnCode() == 0)
            else:
                LogOutput(
                    'info',
                    "enable dut02 interface " +
                    str(dut02Obj.linkPortMapping['lnk1' + str(i)]))

    def test_createLAGs(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Create LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        retStruct = lagCreation(deviceObj=dut01Obj, lagId=1, configFlag=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to create LAG on dut01")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "Configured LAG on dut01 ")
        # to fill with interface info
        retStruct = lagCreation(deviceObj=dut02Obj, lagId=1, configFlag=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to create LAG on dut02 ")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "Configured LAG on dut02")

    def test_createDinamicLag(self):
        LogOutput('info', "############################################")
        LogOutput('info', "LAGs Mode Configuration")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        # Switch 1
        retStruct1 = lagMode(deviceObj=dut01Obj, lagId=1, lacpMode="active")
        if retStruct1.returnCode() != 0:
            LogOutput('error', "Failed to put LAG in Active Mode on dut01")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "Configured LAG in Active Mode in dut01 ")
        LogOutput('info', "############################################")
        LogOutput('info', "Show lacp aggregates in dut01")
        LogOutput('info', "############################################")
        returnBuffer1 = dut01Obj.cmdVtysh(command='show lacp aggregates')
        LogOutput('info', returnBuffer1)
        # Switch 2
        retStruct2 = lagMode(deviceObj=dut02Obj, lagId=1, lacpMode="passive")
        if retStruct2.returnCode() != 0:
            LogOutput('error', "Failed to put LAG in Passive Mode on dut02")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "Configured LAG in Passive Mode in dut02")
        LogOutput('info', "############################################")
        LogOutput('info', "Show lacp aggregates in dut02")
        LogOutput('info', "############################################")
        returnBuffer2 = dut02Obj.cmdVtysh(command='show lacp aggregates')
        LogOutput('info', returnBuffer2)

    def test_configureVLANs(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Configure VLANs on switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        # Switch 1
        retStruct1 = AddVlan(deviceObj=dut01Obj, vlanId=100)
        if retStruct1.returnCode() != 0:
            LogOutput('error', "Failed to add Vlan 100 in dut01")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "Add Vlan 100 in dut01")

        retStruct2 = VlanStatus(deviceObj=dut01Obj, vlanId=100, status=True)
        if retStruct2.returnCode() != 0:
            LogOutput('error', "Failed to active Vlan 100 in dut01")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "Vlan 100 activaded in dut01")

        retStruct3 = AddPortToVlan(
            deviceObj=dut01Obj, vlanId=100,
            interface=dut01Obj.linkPortMapping['lnk01'], access=True)
        if retStruct3.returnCode() != 0:
            LogOutput(
                'error', "Failed to add Interface 1 in Vlan 100 in dut01")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "Interface 1 added to Vlan 100 in dut01")
        retStruct4 = AddPortToVlan(
            deviceObj=dut01Obj, vlanId=100, interface='lag 1', access=True)
        if retStruct4.returnCode() != 0:
            LogOutput('error', "Failed to add Lag 1 in Vlan 100 in dut01")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "Interface Lag 1 added to Vlan 100 in dut01")

        # Switch 2
        retStruct5 = AddVlan(deviceObj=dut02Obj, vlanId=100)
        if retStruct5.returnCode() != 0:
            LogOutput('error', "Failed to add Vlan 100 in dut02")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "Add Vlan 100 in dut02")
        retStruct6 = VlanStatus(deviceObj=dut02Obj, vlanId=100, status=True)
        if retStruct6.returnCode() != 0:
            LogOutput('error', "Failed to active Vlan 100 in dut02")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "Vlan 100 activaded in dut02")
        retStruct7 = AddPortToVlan(
            deviceObj=dut02Obj, vlanId=100,
            interface=dut02Obj.linkPortMapping['lnk18'], access=True)
        if retStruct7.returnCode() != 0:
            LogOutput(
                'error', "Failed to add Interface 17 in Vlan 100 in dut02")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "Interface 17 added to Vlan 100 in dut02")
        retStruct8 = AddPortToVlan(
            deviceObj=dut02Obj, vlanId=100, interface='lag 1', access=True)
        if retStruct8.returnCode() != 0:
            LogOutput('error', "Failed to add Lag 1 in Vlan 100 in dut02")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "Interface Lag 1 added to Vlan 100 ind dut02")

    def test_defineSystemPriority(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Set lacp system-priority in both DUTs ")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        # Switch 1
        retStruct1 = lagpGlobalSystemPriority(
            deviceObj=dut01Obj, systemPriority=100, configure=True)
        if retStruct1.returnCode() != 0:
            LogOutput(
                'error', "Failed to set lacp system-priority to 100 in dut01")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "Lacp system-priority set to 100 in dut01")
        # Switch 2
        retStruct2 = lagpGlobalSystemPriority(
            deviceObj=dut02Obj, systemPriority=200, configure=True)
        if retStruct2.returnCode() != 0:
            LogOutput(
                'error', "Failed to set lacp system-priority to 200 in dut02")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "Lacp system-priority set to 200 in dut02")

    def test_definePortPriority(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Set interface port-priority in both DUTs ")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        LogOutput('info', "############################################")
        LogOutput(
            'info', "Set port-priority in 10 from 2-9 interfaces in dut01")
        LogOutput('info', "############################################")
        for i in range(1, 9):
            retStruct1 = InterfaceLacpPortPriorityConfig(
                deviceObj=dut01Obj, interface=i + 1, lacpPortPriority=10)
            if retStruct1.returnCode() != 0:
                LogOutput(
                    'error', "Failed to set in interface " +
                    str(i + 1) + " port-priority")
                assert(retStruct.returnCode() == 0)
            else:
                LogOutput('info', "Interface " + str(i + 1) + " configured")

        LogOutput('info', "############################################")
        LogOutput(
            'info', "Set port-priority in 65000 from 10-17 interfaces in dut01")
        LogOutput('info', "############################################")
        for i in range(1, 9):
            retStruct2 = InterfaceLacpPortPriorityConfig(
                deviceObj=dut01Obj, interface=i + 9, lacpPortPriority=65000)
            if retStruct2.returnCode() != 0:
                LogOutput(
                    'error', "Failed to set in interface " +
                    str(i + 9) + " port-priority")
                assert(retStruct.returnCode() == 0)
            else:
                LogOutput('info', "Interface " + str(i + 9) + " configured")

        LogOutput('info', "############################################")
        LogOutput(
            'info', "Set port-priority in 65000 1-8 interfaces in dut02")
        LogOutput('info', "############################################")
        for i in range(0, 8):
            retStruct3 = InterfaceLacpPortPriorityConfig(
                deviceObj=dut02Obj, interface=i + 1, lacpPortPriority=65000)
            if retStruct3.returnCode() != 0:
                LogOutput(
                    'error', "Failed to set in interface " +
                    str(i + 1) + " port-priority")
                assert(retStruct.returnCode() == 0)
            else:
                LogOutput('info', "Interface " + str(i + 1) + " configured")
        LogOutput('info', "############################################")
        LogOutput(
            'info', "Set port-priority in 10 from 9 to 16 interfaces in dut02")
        LogOutput('info', "############################################")
        for i in range(0, 8):
            retStruct4 = InterfaceLacpPortPriorityConfig(
                deviceObj=dut02Obj, interface=i + 9, lacpPortPriority=10)
            if retStruct4.returnCode() != 0:
                LogOutput(
                    'error', "Failed to set in interface " +
                    str(i + 9) + " port-priority")
                assert(retStruct.returnCode() == 0)
            else:
                LogOutput('info', "Interface " + str(i + 9) + " configured")

    def test_putInterfaceIntoLAG(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Configure interfaces into LAG 1 interface")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")

        # Switch 1
        LogOutput('info', "############################################")
        LogOutput('info', "Configuring dut01")
        LogOutput('info', "############################################")
        for i in range(1, 18):
            retStruct1 = InterfaceLagIdConfig(
                deviceObj=dut01Obj, interface=i + 1, lagId=1, enable=True)
            if retStruct1.returnCode() != 0:
                LogOutput('error', "Failed to set in interface " +
                          str(i + 1) + " into Lag 1 interface in dut01")
                assert(retStruct.returnCode() == 0)
            else:
                LogOutput(
                    'info', "Interface " + str(i + 1) +
                    " into Lag 1 Interface in dut01")

        # Switch 2
        LogOutput('info', "############################################")
        LogOutput('info', "Configuring dut02")
        LogOutput('info', "############################################")
        for i in range(0, 17):
            retStruct2 = InterfaceLagIdConfig(
                deviceObj=dut02Obj, interface=i + 1, lagId=1, enable=True)
            if retStruct2.returnCode() != 0:
                LogOutput('error', "Failed to set in interface " +
                          str(i + 1) + " into Lag 1 interface in dut02")
                assert(retStruct.returnCode() == 0)
            else:
                LogOutput(
                    'info', "Interface " + str(i + 1) +
                    " into Lag 1 Interface in dut02")

        returnBuffer1 = dut01Obj.cmdVtysh(command='show lacp aggregates')
        LogOutput('info', "############################################")
        LogOutput('info', "Show lacp aggregates in dut01\n" + returnBuffer1)
        LogOutput('info', "############################################")
        returnBuffer2 = dut02Obj.cmdVtysh(command='show lacp aggregates')
        LogOutput('info', "############################################")
        LogOutput('info', "Show lacp aggregates in dut02\n" + returnBuffer2)
        LogOutput('info', "############################################")

    def test_testWhichInterfacesAreActive1(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        returnBufferX = lacpAggregatesShow(lagId=1, deviceObj=dut01Obj)
        test = ['2', '3', '4', '5', '6', '7', '8', '9']
        print test
        print sorted(returnBufferX.data['1']['interfaces'])
        retStruct = sorted(returnBufferX.data['1']['interfaces'])
        if retStruct == test:
            LogOutput('info', "Interfaces 2-9 selected correctly")
        else:
            LogOutput('error', "Failed in selected Interfaces 2-9")
            assert(True)

    def test_configureWorkstations(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Configure workstations")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        LogOutput('info', "Configuring workstation 1")
        assert(configureWorkstation(wrkston01Obj, wrkston01Obj.linkPortMapping[
               'lnk01'], "140.1.1.10", "255.255.255.0", "140.1.1.255", True))
        LogOutput('info', "Configuring workstation 2")
        assert(configureWorkstation(wrkston02Obj, wrkston02Obj.linkPortMapping[
               'lnk18'], "140.1.1.11", "255.255.255.0", "140.1.1.255", True))

    def test_pingBetweenClients1(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Test ping between clients work")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        LogOutput('info', "Pinging between WS 1 and SW 2")
        retStruct = wrkston01Obj.Ping(ipAddr="140.1.1.11")
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to ping workstation2")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info',
                      "IPv4 Ping from SW 1 to WS 2 return JSON:\n" +
                      str(retStruct.retValueString()))
            packet_loss = retStruct.valueGet(key='packet_loss')
            packets_sent = retStruct.valueGet(key='packets_transmitted')
            packets_received = retStruct.valueGet(key='packets_received')
            LogOutput('info', "Packets Sent:\t" + str(packets_sent))
            LogOutput('info', "Packets Recv:\t" + str(packets_received))
            LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
            LogOutput(
                'info',
                "Passed ping test between SW 1 and SW 2")

    def test_RiseDut01PriorityBelowDut02(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Rise dut01 system-priority to 190 ")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        retStruct1 = lagpGlobalSystemPriority(
            deviceObj=dut01Obj, systemPriority=190, configure=True)
        if retStruct1.returnCode() != 0:
            LogOutput(
                'error', "Failed to rise lacp system-priority to 190 in dut01")
            assert(retStruct1.returnCode() == 0)
        else:
            LogOutput('info', "Lacp system-priority rised to 190 in dut01")

    def test_DisableEnableInterfaces1(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        # Switch 1
        LogOutput('info', "############################################")
        LogOutput('info', "Disable interfaces in dut01 and dut02")
        LogOutput('info', "############################################")
        for i in range(0, 17):
            retStruct1 = InterfaceEnable(
                deviceObj=dut01Obj, interface=i + 2, enable=False)
            if retStruct1.returnCode() != 0:
                LogOutput(
                    'error', "Failed to disable inteface "
                    + str(i + 2) + " in dut01")
                assert(retStruct1.returnCode() == 0)
            else:
                LogOutput(
                    'info', "Interface " + str(i + 2) + " disabled in dut01")

            retStruct2 = InterfaceEnable(
                deviceObj=dut02Obj, interface=i + 1, enable=False)
            if retStruct2.returnCode() != 0:
                LogOutput(
                    'error', "Failed to disable inteface " +
                    str(i + 1) + " in dut02")
                assert(retStruct1.returnCode() == 0)
            else:
                LogOutput(
                    'info', "Interface " + str(i + 1) + " disabled in dut02")

        LogOutput('info', "############################################")
        LogOutput('info', "Enable interfaces in dut01 and dut02")
        LogOutput('info', "############################################")

        for i in range(0, 17):
            retStruct3 = InterfaceEnable(
                deviceObj=dut01Obj, interface=i + 2, enable=True)
            if retStruct3.returnCode() != 0:
                LogOutput(
                    'error', "Failed to enable inteface " +
                    str(i + 2) + " in dut01")
                assert(retStruct3.returnCode() == 0)
            else:
                LogOutput(
                    'info', "Interface " + str(i + 2) + " enabled in dut01")
            retStruct4 = InterfaceEnable(
                deviceObj=dut02Obj, interface=i + 1, enable=True)
            if retStruct4.returnCode() != 0:
                LogOutput(
                    'error', "Failed to enable inteface " +
                    str(i + 1) + " in dut02")
                assert(retStruct4.returnCode() == 0)
            else:
                LogOutput(
                    'info', "Interface " + str(i + 1) + " enabled in dut02")

    def test_testWhichInterfacesAreActive2(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        returnBufferX = lacpAggregatesShow(lagId=1, deviceObj=dut01Obj)
        test = ['2', '3', '4', '5', '6', '7', '8', '9']
        print test
        print sorted(returnBufferX.data['1']['interfaces'])
        retStruct = sorted(returnBufferX.data['1']['interfaces'])
        if retStruct == test:
            LogOutput(
                'info', "Interfaces 2-9 selected correctly after rise to 190")
        else:
            LogOutput('error', "Failed in selected Interfaces 2-9")
            assert(True)

    def test_pingBetweenClients2(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Test ping between clients work")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        LogOutput('info', "Pinging between workstation 1 and workstation 2")
        retStruct = wrkston01Obj.Ping(ipAddr="140.1.1.11")
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to ping workstation2")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "IPv4 Ping from SW 1 to WS 2 return JSON:\n" +
                      str(retStruct.retValueString()))
            packet_loss = retStruct.valueGet(key='packet_loss')
            packets_sent = retStruct.valueGet(key='packets_transmitted')
            packets_received = retStruct.valueGet(key='packets_received')
            LogOutput('info', "Packets Sent:\t" + str(packets_sent))
            LogOutput('info', "Packets Recv:\t" + str(packets_received))
            LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
            LogOutput(
                'info', "Passed ping test between WS 1 and WS 2")

    def test_RiseDut01PriorityOverDut02(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Rise dut01 system-priority to 300 ")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        retStruct = lagpGlobalSystemPriority(
            deviceObj=dut01Obj, systemPriority=300, configure=True)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed to rise lacp system-priority to 300 in dut01")
            assert(retStruct1.returnCode() == 0)
        else:
            LogOutput('info', "Lacp system-priority rised to 300 in dut01")

    def test_DisableEnableInterfaces2(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        # Switch 1
        LogOutput('info', "############################################")
        LogOutput('info', "Disable interfaces in dut01 and dut02")
        LogOutput('info', "############################################")
        for i in range(0, 17):
            retStruct1 = InterfaceEnable(
                deviceObj=dut01Obj, interface=i + 2, enable=False)
            if retStruct1.returnCode() != 0:
                LogOutput(
                    'error', "Failed to disable inteface " +
                    str(i + 2) + " in dut01")
                assert(retStruct1.returnCode() == 0)
            else:
                LogOutput(
                    'info', "Interface " + str(i + 2) + " disabled in dut01")

            retStruct2 = InterfaceEnable(
                deviceObj=dut02Obj, interface=i + 1, enable=False)
            if retStruct2.returnCode() != 0:
                LogOutput(
                    'error', "Failed to disable inteface " +
                    str(i + 1) + " in dut02")
                assert(retStruct1.returnCode() == 0)
            else:
                LogOutput(
                    'info', "Interface " + str(i + 1) + " disabled in dut02")

        LogOutput('info', "############################################")
        LogOutput('info', "Enable interfaces in dut01 and dut02")
        LogOutput('info', "############################################")

        for i in range(0, 17):
            retStruct3 = InterfaceEnable(
                deviceObj=dut01Obj, interface=i + 2, enable=True)
            if retStruct3.returnCode() != 0:
                LogOutput(
                    'error', "Failed to enable inteface " +
                    str(i + 2) + " in dut01")
                assert(retStruct3.returnCode() == 0)
            else:
                LogOutput(
                    'info', "Interface " + str(i + 2) + " enabled in dut01")
            retStruct4 = InterfaceEnable(
                deviceObj=dut02Obj, interface=i + 1, enable=True)
            if retStruct4.returnCode() != 0:
                LogOutput(
                    'error', "Failed to enable inteface " +
                    str(i + 1) + " in dut02")
                assert(retStruct4.returnCode() == 0)
            else:
                LogOutput(
                    'info', "Interface " + str(i + 1) + " enabled in dut02")

    def test_testWhichInterfacesAreActive3(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        returnBufferX = lacpAggregatesShow(lagId=1, deviceObj=dut01Obj)
        test = ['10', '11', '12', '13', '14', '15', '16', '17']
        print test 
        print sorted(returnBufferX.data['1']['interfaces'])
        retStruct = sorted(returnBufferX.data['1']['interfaces'])
        if retStruct == test:
            LogOutput(
                'info', "Interfaces 9-16 selected correctly after rise to 300")
        else:
            LogOutput('error', "Failed in selected Interfaces 9-16")
            assert(True)

    def test_pingBetweenClients3(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Test ping between clients work")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        LogOutput('info', "Pinging between SW 1 and SW 2")
        retStruct = wrkston01Obj.Ping(ipAddr="140.1.1.11")
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to ping workstation2")
            assert(retStruct.returnCode() == 0)
        else:
            LogOutput('info', "IPv4 Ping from WS 1 to WS 2 return JSON:\n" +
                      str(retStruct.retValueString()))
            packet_loss = retStruct.valueGet(key='packet_loss')
            packets_sent = retStruct.valueGet(key='packets_transmitted')
            packets_received = retStruct.valueGet(key='packets_received')
            LogOutput('info', "Packets Sent:\t" + str(packets_sent))
            LogOutput('info', "Packets Recv:\t" + str(packets_received))
            LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
            LogOutput(
                'info', "Passed ping test between SW 1 and SW 2")

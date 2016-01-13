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
#                                   TOPOLOGY
#  ---------------------------------------------------------------------------
#       ___                ____                  ____                  ____
#      |ws1| vlan access  |    |                |    |  vlan access   |    |
#      |___|------------->|    |   vlan trunk   |    |--------------->|    |
#                         |  S |--------------->|  S |                |  S |
#                         |  W |   vlan trunk   |  W |                |  W |
#       ___  vlan access  |    |--------------->|    |                |    |
#      |ws2|------------->|  1 |       Lag      |  2 |--------------->|  3 |
#      |___|              |____|                |____|  vlan access   |____|
#
#  ---------------------------------------------------------------------------

import pytest
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *
import math

topoDict = {"topoExecution": 1500,
            "topoTarget" : "dut01 dut02 dut03\
                            wrkston01 wrkston02",
            "topoDevices": "dut01 dut02 dut03\
                            wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut01:wrkston02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut01:dut02,\
                          lnk05:dut02:dut03,\
                          lnk06:dut02:dut03",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation"}


def switch_reboot(dut01):
    # Reboot switch
    LogOutput('info', "Reboot switch")
    dut01.Reboot()
    rebootRetStruct = returnStruct(returnCode=0)
    return rebootRetStruct


def clean_up(dut01, dut02, dut03, wrkston01, wrkston02):

    listDut = [dut01, dut02, dut03]
    for currentDut in listDut:
        devRebootRetStruct = switch_reboot(currentDut)
        if devRebootRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to reboot Switch")
            assert(False)
    else:
        LogOutput('info', "Passed Switch Reboot ")


class Test_ft_LAG_static_L2_VLAN_Hashing_Flow_Distribution:

    listDut = None
    listWrkston = None
    dut01Obj = None
    dut02Obj = None
    dut03Obj = None
    wrkston01Obj = None
    wrkston02Obj = None
    l2IpDevice = None
    l2IpWrkston = None
    l2IpNetwork = None
    l2IpNetmask = None
    marginError = None

    def setup_class(cls):

        # Create Topology object and connect to devices
        Test_ft_LAG_static_L2_VLAN_Hashing_Flow_Distribution.testObj \
            = testEnviron(topoDict=topoDict)
        Test_ft_LAG_static_L2_VLAN_Hashing_Flow_Distribution.topoObj = \
            Test_ft_LAG_static_L2_VLAN_Hashing_Flow_Distribution. \
            testObj.topoObjGet()

        # Global definition
        global listDut
        global listWrkston
        global dut01Obj
        global dut02Obj
        global dut03Obj
        global wrkston01Obj
        global wrkston02Obj
        global l2IpDevice
        global l2IpWrkston
        global l2IpNetwork
        global l2IpNetmask
        global marginError

        # Var initiation
        l2IpWrkston = ["10.2.2.100", "10.3.3.100"]
        l2IpDevice = ["10.2.2.1", "10.3.3.1"]
        l2IpNetwork = ["10.2.2.255", "10.3.3.255"]
        l2IpNetmask = "255.255.255.0"
        marginError = 0.20
        dut01Obj = cls.topoObj.deviceObjGet(device="dut01")
        dut02Obj = cls.topoObj.deviceObjGet(device="dut02")
        dut03Obj = cls.topoObj.deviceObjGet(device="dut03")

        wrkston01Obj = cls.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = cls.topoObj.deviceObjGet(device="wrkston02")

        listDut = [dut01Obj, dut02Obj, dut03Obj]
        listWrkston = [wrkston01Obj, wrkston02Obj]

    def teardown_class(cls):
        # Terminate all nodes
        clean_up(dut01Obj,
                 dut02Obj,
                 dut03Obj,
                 wrkston01Obj,
                 wrkston02Obj)
        Test_ft_LAG_static_L2_VLAN_Hashing_Flow_Distribution.topoObj. \
            terminate_nodes()

    ##########################################################################
    # Step 1 - Reboot Switch
    ##########################################################################

    def test_reboot_switches(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 1 - Reboot the switches")
        LogOutput('info', "###############################################")

        for currentDut in listDut:
            devRebootRetStruct = switch_reboot(currentDut)
            if devRebootRetStruct.returnCode() != 0:
                LogOutput('error', "Failed to reboot Switch")
                assert(False)
            else:
                LogOutput('info', "Passed Switch Reboot ")

    ##########################################################################
    # Step 2 - Configure Switch 1
    ##########################################################################

    def test_configure_first_switch(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 2 - Configure Switch 1")
        LogOutput('info', "###############################################")

        # Entering vtysh prompt
        retStruct = dut01Obj.VtyshShell(enter=True)
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to enter vtysh prompt"

        # Entering config terminal SW1
        retStruct = dut01Obj.ConfigVtyShell(enter=True)
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to enter config terminal"

        # Adding vlan 500
        devIntRetStruct = dut01Obj.DeviceInteract(command="vlan 500")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add vlan 500"

        # Enabling vlan 500
        devIntRetStruct = dut01Obj.DeviceInteract(command="no shutdown")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enable vlan 500"

        # Adding vlan 600
        devIntRetStruct = dut01Obj.DeviceInteract(command="vlan 600")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add vlan 600"

        # Enabling vlan 600
        devIntRetStruct = dut01Obj.DeviceInteract(command="no shutdown")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enable vlan 600"

        # Entering interface
        LogOutput('info', "Switch 1 interface is :"
                  + str(dut01Obj.linkPortMapping['lnk01']))
        devIntRetStruct =\
            dut01Obj.DeviceInteract(command="interface "
                                   + str(dut01Obj.linkPortMapping['lnk01']))
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enter interface"

        # Enabling interface
        devIntRetStruct = dut01Obj.DeviceInteract(command="no shutdown")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enable interface"

        # Disabling routing
        devIntRetStruct = dut01Obj.DeviceInteract(command="no routing")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to disable routing"

        # Adding access vlan to the interface
        devIntRetStruct = dut01Obj.DeviceInteract(command="vlan access 600")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add vlan 600 to interface"

        # Entering interface
        LogOutput('info', "Switch 1 interface is :"
                  + str(dut01Obj.linkPortMapping['lnk02']))
        devIntRetStruct =\
            dut01Obj.DeviceInteract(command="interface "
                                   + str(dut01Obj.linkPortMapping['lnk02']))
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enter interface"

        # Enabling interface
        devIntRetStruct = dut01Obj.DeviceInteract(command="no shutdown")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enable interface"

        # Disabling routing
        devIntRetStruct = dut01Obj.DeviceInteract(command="no routing")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to disable routing"

        # Adding access vlan to the interface
        devIntRetStruct = dut01Obj.DeviceInteract(command="vlan access 500")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add vlan 500 to interface"

        # Adding lag interface
        devIntRetStruct = dut01Obj.DeviceInteract(command="interface lag 150")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add lag interface"

        # Disabling routing
        devIntRetStruct = dut01Obj.DeviceInteract(command="no routing")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to disable routing"

        # Adding trunk vlan to lag interface
        devIntRetStruct = dut01Obj.DeviceInteract(command="vlan trunk allowed 500")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add vlan trunk 500 to lag interface"

        # Adding trunk vlan to lag interface
        devIntRetStruct = dut01Obj.DeviceInteract(command="vlan trunk allowed 600")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add vlan trunk 600 to lag interface"

        # Entering interface
        LogOutput('info', "Switch 1 interface is :"
                  + str(dut01Obj.linkPortMapping['lnk03']))
        devIntRetStruct =\
            dut01Obj.DeviceInteract(command="interface "
                                   + str(dut01Obj.linkPortMapping['lnk03']))
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enter interface"

        # Adding lag to interface
        devIntRetStruct = dut01Obj.DeviceInteract(command="lag 150")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add lag to the interface"

        # Enabling interface
        devIntRetStruct = dut01Obj.DeviceInteract(command="no shutdown")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enable interface"

        # Entering interface
        LogOutput('info', "Switch 1 interface is :"
                  + str(dut01Obj.linkPortMapping['lnk04']))
        devIntRetStruct =\
            dut01Obj.DeviceInteract(command="interface "
                                   + str(dut01Obj.linkPortMapping['lnk04']))
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enter interface"

        # Adding lag to interface
        devIntRetStruct = dut01Obj.DeviceInteract(command="lag 150")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add lag to the interface"

        # Enabling interface
        devIntRetStruct = dut01Obj.DeviceInteract(command="no shutdown")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enable interface"

        # Exiting interface
        devIntRetStruct = dut01Obj.DeviceInteract(command="exit")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to exit interface"

        # Exiting terminal
        retStruct = dut01Obj.ConfigVtyShell(enter=False)
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to come out of config terminal"

        # Exiting vtysh prompt
        retStruct = dut01Obj.VtyshShell(enter=False)
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to exit vtysh prompt"

    ##########################################################################
    # Step 3 - Configure Switch 2
    ##########################################################################

    def test_configure_second_switch(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 3 - Configure Switch 2")
        LogOutput('info', "###############################################")

        # Entering vtysh prompt
        retStruct = dut02Obj.VtyshShell(enter=True)
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to enter vtysh prompt"

        # Entering config terminal SW1
        retStruct = dut02Obj.ConfigVtyShell(enter=True)
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to enter config terminal"

        # Adding vlan 500
        devIntRetStruct = dut02Obj.DeviceInteract(command="vlan 500")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add vlan 500"

        # Enabling vlan 500
        devIntRetStruct = dut02Obj.DeviceInteract(command="no shutdown")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enable vlan 500"

        # Adding vlan 600
        devIntRetStruct = dut02Obj.DeviceInteract(command="vlan 600")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add vlan 600"

        # Enabling vlan 600
        devIntRetStruct = dut02Obj.DeviceInteract(command="no shutdown")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enable vlan 600"

        # Entering interface
        LogOutput('info', "Switch 2 interface is :"
                  + str(dut02Obj.linkPortMapping['lnk05']))
        devIntRetStruct =\
            dut02Obj.DeviceInteract(command="interface "
                                   + str(dut02Obj.linkPortMapping['lnk05']))
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enter interface"

        # Enabling interface
        devIntRetStruct = dut02Obj.DeviceInteract(command="no shutdown")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enable interface"

        # Disabling routing
        devIntRetStruct = dut02Obj.DeviceInteract(command="no routing")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to disable routing"

        # Adding access vlan to the interface
        devIntRetStruct = dut02Obj.DeviceInteract(command="vlan access 600")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add vlan 600 to interface"

        # Entering interface
        LogOutput('info', "Switch 2 interface is :"
                  + str(dut02Obj.linkPortMapping['lnk06']))
        devIntRetStruct =\
            dut02Obj.DeviceInteract(command="interface "
                                   + str(dut02Obj.linkPortMapping['lnk06']))
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enter interface"

        # Enabling interface
        devIntRetStruct = dut02Obj.DeviceInteract(command="no shutdown")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enable interface"

        # Disabling routing
        devIntRetStruct = dut02Obj.DeviceInteract(command="no routing")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to disable routing"

        # Adding access vlan to the interface
        devIntRetStruct = dut02Obj.DeviceInteract(command="vlan access 500")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add vlan 500 to interface"

        # Adding lag interface
        devIntRetStruct = dut02Obj.DeviceInteract(command="interface lag 150")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add lag interface"

        # Disabling routing
        devIntRetStruct = dut02Obj.DeviceInteract(command="no routing")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to disable routing"

        # Adding trunk vlan to lag interface
        devIntRetStruct = dut02Obj.DeviceInteract(command="vlan trunk allowed 500")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add vlan trunk 500 to lag interface"

        # Adding trunk vlan to lag interface
        devIntRetStruct = dut02Obj.DeviceInteract(command="vlan trunk allowed 600")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add vlan trunk 600 to lag interface"

        # Entering interface
        LogOutput('info', "Switch 2 interface is :"
                  + str(dut02Obj.linkPortMapping['lnk03']))
        devIntRetStruct =\
            dut02Obj.DeviceInteract(command="interface "
                                   + str(dut02Obj.linkPortMapping['lnk03']))
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enter interface"

        # Adding lag to interface
        devIntRetStruct = dut02Obj.DeviceInteract(command="lag 150")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add lag to the interface"

        # Enabling interface
        devIntRetStruct = dut02Obj.DeviceInteract(command="no shutdown")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enable interface"

        # Entering interface
        LogOutput('info', "Switch 2 interface is :"
                  + str(dut02Obj.linkPortMapping['lnk04']))
        devIntRetStruct =\
            dut02Obj.DeviceInteract(command="interface "
                                   + str(dut02Obj.linkPortMapping['lnk04']))
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enter interface"

        # Adding lag to interface
        devIntRetStruct = dut02Obj.DeviceInteract(command="lag 150")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to add lag to the interface"

        # Enabling interface
        devIntRetStruct = dut02Obj.DeviceInteract(command="no shutdown")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enable interface"

        # Exiting interface
        devIntRetStruct = dut02Obj.DeviceInteract(command="exit")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to exit interface"

        # Exiting terminal
        retStruct = dut02Obj.ConfigVtyShell(enter=False)
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to come out of config terminal"

        # Exiting vtysh prompt
        retStruct = dut02Obj.VtyshShell(enter=False)
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to exit vtysh prompt"

    ##########################################################################
    # Step 4 - Configure switch 3 ip address
    ##########################################################################

    def test_configured_switch_ip_address(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 4 - Configure Switch 3 ip address")
        LogOutput('info', "###############################################")

        index = 0

        dut03Interface01 = dut03Obj.linkPortMapping['lnk05']
        dut03Interface02 = dut03Obj.linkPortMapping['lnk06']

        listDut03Interface = [dut03Interface01,
                              dut03Interface02]

        for currentInterface in listDut03Interface:
            retStruct = InterfaceIpConfig(deviceObj=dut03Obj,
                                          interface=currentInterface,
                                          addr=l2IpDevice[index],
                                          mask=24,
                                          config=True)

            if retStruct.returnCode() != 0:
                LogOutput('error', "Failed to configured  IP on interface")
                assert(False)
            else:
                LogOutput('info', "Successfully configured IP on Interface")
            index += 1

    ##########################################################################
    # Step 5 - Configure Workstation
    ##########################################################################

    def test_configure_workstations(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 4 - Configure Workstations")
        LogOutput('info', "###############################################")

        # Client Side

        retStruct = wrkston01Obj.NetworkConfig(
            ipAddr=l2IpWrkston[0],
            netMask=l2IpNetmask,
            broadcast=l2IpNetwork[0],
            interface=wrkston01Obj.linkPortMapping['lnk01'],
            config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configured Client station")
            assert(False)
        LogOutput('info', "Complete workstation configuration")

        retStruct = wrkston02Obj.NetworkConfig(
            ipAddr=l2IpWrkston[1],
            netMask=l2IpNetmask,
            broadcast=l2IpNetwork[1],
            interface=wrkston02Obj.linkPortMapping['lnk02'],
            config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configured Client station")
            assert(False)
        LogOutput('info', "Complete workstation configuration")


    ##########################################################################
    # Step 6 - Enable Switch 3 ports
    ##########################################################################

    def test_enable_switch_interfaces(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 6 - Enable switch 3 interfaces")
        LogOutput('info', "###############################################")

        switch3Interface1 = dut03Obj.linkPortMapping['lnk05']
        switch3Interface2 = dut03Obj.linkPortMapping['lnk06']

        listSwitchInterfacesDut3 = [
            switch3Interface1,
            switch3Interface2]

        # Enable ports from switch 3
        for currentInterface in listSwitchInterfacesDut3:
            retStruct = InterfaceEnable(
                deviceObj=dut03Obj,
                enable=True,
                interface=currentInterface)

            if retStruct.returnCode() != 0:
                LogOutput('error', "Failed to enable port on switch")
                assert(False)

    ##########################################################################
    # Step 7 - Send and validated traffic
    ##########################################################################

    def test_send_validated_traffic(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 7 - Send and validated traffic")
        LogOutput('info', "###############################################")

        packetsCounter = 25

        # Check ports for delta

        interfaceLag1 = dut01Obj.linkPortMapping['lnk03']
        interfaceLag2 = dut01Obj.linkPortMapping['lnk04']

        retTxIntStruct1 = InterfaceStatisticsShow(
            deviceObj=dut01Obj,
            interface=interfaceLag1)
        retTxIntStruct2 = InterfaceStatisticsShow(
            deviceObj=dut01Obj,
            interface=interfaceLag2)

        if retTxIntStruct1.returnCode() != 0 \
                or retTxIntStruct2.returnCode() != 0:
            LogOutput('error', "Can show interface information")
            assert(False)

        tx1Delta = retTxIntStruct1.valueGet(key='TX')
        tx1Delta = tx1Delta['outputPackets']

        tx2Delta = retTxIntStruct2.valueGet(key='TX')
        tx2Delta = tx2Delta['outputPackets']

        LogOutput('info', "Delta values for the interfaces are :")
        LogOutput('info', "Interface clean is : " + str(tx1Delta))
        LogOutput('info', "Interface clean is : " + str(tx2Delta))

        # Ping from the first device
        retStructValid = wrkston01Obj.Ping(ipAddr=l2IpDevice[0],
                                           packetCount=packetsCounter,
                                           packetSize=1024)

        if retStructValid.returnCode() != 0:
            LogOutput('error',
                      "Failed to ping from workstation 1 to device1")
            assert(False)

        retTxIntStruct1 = InterfaceStatisticsShow(
            deviceObj=dut01Obj,
            interface=interfaceLag1)
        retTxIntStruct2 = InterfaceStatisticsShow(
            deviceObj=dut01Obj,
            interface=interfaceLag2)

        if retTxIntStruct1.returnCode() != 0 \
                or retTxIntStruct2.returnCode() != 0:
            LogOutput('error', "Can show interface information")
            assert(False)

        tx1First = retTxIntStruct1.valueGet(key='TX')
        tx1First = tx1First['outputPackets']

        tx2First = retTxIntStruct2.valueGet(key='TX')
        tx2First = tx2First['outputPackets']

        LogOutput('info', "Values fot the first ping :")
        LogOutput('info', "Interface clean is : " + str(tx1First))
        LogOutput('info', "Interface clean is : " + str(tx2First))

        # Ping from the second device
        retStructValid = wrkston02Obj.Ping(ipAddr=l2IpDevice[1],
                                           packetCount=packetsCounter,
                                           packetSize=1024)

        if retStructValid.returnCode() != 0:
            LogOutput('error',
                      "Failed to ping from workstation 2 to device2")
            assert(False)

        retTxIntStruct1 = InterfaceStatisticsShow(
            deviceObj=dut01Obj,
            interface=interfaceLag1)
        retTxIntStruct2 = InterfaceStatisticsShow(
            deviceObj=dut01Obj,
            interface=interfaceLag2)

        if retTxIntStruct1.returnCode() != 0 \
                or retTxIntStruct2.returnCode() != 0:
            LogOutput('error', "Can show interface information")
            assert(False)

        tx1Second = retTxIntStruct1.valueGet(key='TX')
        tx1Second = tx1Second['outputPackets']

        tx2Second = retTxIntStruct2.valueGet(key='TX')
        tx2Second = tx2Second['outputPackets']

        LogOutput('info', "Values fot the firts ping :")
        LogOutput('info', "Interface clean is : " + str(tx1Second))
        LogOutput('info', "Interface clean is : " + str(tx2Second))

        # Operations to see if traffic was distributed
        raw1Tx = (int(tx1First) - int(tx1Delta)) - \
            (int(tx2First) - int(tx2Delta))
        raw2Tx = (int(tx2Second) - int(tx2First)) - \
            (int(tx1Second) - int(tx1First))

        lowBandError = packetsCounter - \
            math.floor(float(packetsCounter) * marginError)
        highBandError = packetsCounter + \
            math.ceil(float(packetsCounter) * marginError)

        if lowBandError > raw2Tx or  raw2Tx > highBandError \
                or lowBandError > raw1Tx or raw1Tx > highBandError:
            LogOutput('error', "Traffic not was evenly distributed ")
            assert(False)
        else:
            LogOutput('info', "Traffic in ports was evenly distributed")

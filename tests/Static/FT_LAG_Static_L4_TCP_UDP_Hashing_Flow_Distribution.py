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
import pytest
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *
import math

topoDict = {"topoExecution": 1500,
            "topoTarget" : "dut01 dut02\
                            wrkston01 wrkston02",
            "topoDevices": "dut01 dut02\
                            wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut01:dut02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut02:wrkston02",
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


def clean_up(dut01, dut02, wrkston01, wrkston02):

    listDut = [dut01, dut02]
    for currentDut in listDut:
        devRebootRetStruct = switch_reboot(currentDut)
        if devRebootRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to reboot Switch")
            assert(False)
    else:
        LogOutput('info', "Passed Switch Reboot ")


class Test_ft_LAG_static_L4_TCP_UDP_Hashing_Flow_Distribution:

    listDut = None
    listWrkston = None
    dut01Obj = None
    dut02Obj = None
    wrkston01Obj = None
    wrkston02Obj = None
    lagId = None
    l2IpAddress = None
    l2IpNetwork = None
    l2IpNetmask = None
    vlanLagId = None
    marginError = None

    def setup_class(cls):

        # Create Topology object and connect to devices
        Test_ft_LAG_static_L4_TCP_UDP_Hashing_Flow_Distribution.testObj \
            = testEnviron(topoDict=topoDict)
        Test_ft_LAG_static_L4_TCP_UDP_Hashing_Flow_Distribution.topoObj = \
            Test_ft_LAG_static_L4_TCP_UDP_Hashing_Flow_Distribution. \
            testObj.topoObjGet()

        # Global definition
        global listDut
        global listWrkston
        global dut01Obj
        global dut02Obj
        global wrkston01Obj
        global wrkston02Obj
        global lagId
        global l2IpAddress
        global l2IpNetwork
        global l2IpNetmask
        global vlanLagId
        global marginError

        # Var initiation
        lagId = 150
        l2IpAddress = ["10.2.2.5", "10.2.2.7"]
        l2IpNetwork = "10.2.2.255"
        l2IpNetmask = "255.255.255.0"
        vlanLagId = 800
        marginError = 0.15
        dut01Obj = cls.topoObj.deviceObjGet(device="dut01")
        dut02Obj = cls.topoObj.deviceObjGet(device="dut02")

        wrkston01Obj = cls.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = cls.topoObj.deviceObjGet(device="wrkston02")

        listDut = [dut01Obj, dut02Obj]
        listWrkston = [wrkston01Obj, wrkston02Obj]

    def teardown_class(cls):
        # Terminate all nodes
        clean_up(dut01Obj,
                 dut02Obj,
                 wrkston01Obj,
                 wrkston02Obj)
        Test_ft_LAG_static_L4_TCP_UDP_Hashing_Flow_Distribution.topoObj. \
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
    # Step 2 - Configured Lag
    ##########################################################################

    def test_configure_lag(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 2 - Configure lag in the switch")
        LogOutput('info', "###############################################")

        listSemiDut = [dut01Obj, dut02Obj]

        for currentDut in listSemiDut:
            devLagRetStruct = lagCreation(
                deviceObj=currentDut,
                lagId=lagId,
                configFlag=True)

            if devLagRetStruct.returnCode() != 0:
                LogOutput('error', "Failed to configured lag in the switchs")
                assert(False)
            else:
                LogOutput('info', "Passed lag configured ")

    ##########################################################################
    # Step 3 - Configured vlan
    ##########################################################################

    def test_configure_vlan(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 3 - Configure vlan  in the switch")
        LogOutput('info', "###############################################")

        listSemiDut = [dut01Obj, dut02Obj]

        # Create Vlan
        for currentDut in listSemiDut:
            devLagRetStruct1 = AddVlan(
                deviceObj=currentDut,
                vlanId=vlanLagId,
                config=True)

            if devLagRetStruct1.returnCode() != 0:
                LogOutput('error', "Failed to create vlan in the switchs")
                assert(False)
            else:
                LogOutput('info', "Vlan created")

        # Enable Vlan
        for currentDut in listSemiDut:
            devLagRetStruct1 = VlanStatus(
                deviceObj=currentDut,
                vlanId=vlanLagId,
                status=True)

            if devLagRetStruct1.returnCode() != 0:
                LogOutput('error', "Failed to create vlan in the switchs")
                assert(False)
            else:
                LogOutput('info', "Vlan enabled")

    ##########################################################################
    # Step 4 - Add ports to vlan
    ##########################################################################

    def test_interface_vlan(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 4 - Add ports to vlan")
        LogOutput('info', "###############################################")

        dut01Interface01 = dut01Obj.linkPortMapping['lnk01']
        dut01Interface02 = "lag " + str(lagId)

        listDut01Interface = [dut01Interface01, dut01Interface02]

        dut02Interface01 = dut02Obj.linkPortMapping['lnk04']
        dut02Interface02 = "lag " + str(lagId)

        listDut02Interface = [dut02Interface01, dut02Interface02]

        # Configured Vlan for device 1
        for currentInterface in listDut01Interface:
            devIntLagRetStruct = AddPortToVlan(
                deviceObj=dut01Obj,
                vlanId=vlanLagId,
                interface=currentInterface,
                access=True,
                config=True)

            if devIntLagRetStruct.returnCode() != 0:
                LogOutput('error',
                          "Failed to configured vlan in the interface")
                assert(False)
            else:
                LogOutput('info', "Passed interface vlan configured")

        # Configured Vlan for device 2
        for currentInterface in listDut02Interface:
            devIntLagRetStruct = AddPortToVlan(
                deviceObj=dut02Obj,
                vlanId=vlanLagId,
                interface=currentInterface,
                access=True,
                config=True)

            if devIntLagRetStruct.returnCode() != 0:
                LogOutput('error',
                          "Failed to configured vlan in the interface")
                assert(False)
            else:
                LogOutput('info', "Passed interface vlan configured")

    ##########################################################################
    # Step 5 - Add ports to lag
    ##########################################################################

    def test_configure_interface_lag(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 5 - Configure lag id in the interface")
        LogOutput('info', "###############################################")

        dut01Interface01 = dut01Obj.linkPortMapping['lnk02']
        dut01Interface02 = dut01Obj.linkPortMapping['lnk03']

        dut02Interface01 = dut02Obj.linkPortMapping['lnk02']
        dut02Interface02 = dut02Obj.linkPortMapping['lnk03']

        listInterfacesDut1 = [dut01Interface01, dut01Interface02]
        listInterfacesDut2 = [dut02Interface01, dut02Interface02]

        for interfaceDut in listInterfacesDut1:
            devIntLagRetStruct = InterfaceLagIdConfig(
                deviceObj=dut01Obj,
                interface=interfaceDut,
                lagId=lagId,
                enable=True)
            if devIntLagRetStruct.returnCode() != 0:
                LogOutput('error', "Failed to configured interface lag id")
                assert(False)
            else:
                LogOutput('info', "Passed interface lag id configured ")

        for interfaceDut in listInterfacesDut2:
            devIntLagRetStruct = InterfaceLagIdConfig(
                deviceObj=dut02Obj,
                interface=interfaceDut,
                lagId=lagId,
                enable=True)
            if devIntLagRetStruct.returnCode() != 0:
                LogOutput('error', "Failed to configured interface lag id")
                assert(False)
            else:
                LogOutput('info', "Passed interface lag id configured ")

    ##########################################################################
    # Step 6 - Configure Workstation
    ##########################################################################

    def test_configure_workstations(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 6 - Configure Workstations")
        LogOutput('info', "###############################################")

        # Client Side
        indexIpAddrWrk = 0

        #Configuring workstation 1
        retStruct = wrkston01Obj.NetworkConfig(
            ipAddr=l2IpAddress[indexIpAddrWrk],
            netMask=l2IpNetmask,
            broadcast=l2IpNetwork,
            interface=wrkston01Obj.linkPortMapping['lnk01'],
            config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configured Client 1 station")
            assert(False)
        LogOutput('info', "Complete workstation 1 configuration")

        #Configuring workstation 2
        retStruct = wrkston02Obj.NetworkConfig(
            ipAddr=l2IpAddress[indexIpAddrWrk + 1],
            netMask=l2IpNetmask,
            broadcast=l2IpNetwork,
            interface=wrkston02Obj.linkPortMapping['lnk04'],
            config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configured Client 2 station")
            assert(False)
        LogOutput('info', "Complete workstation 2 configuration")


    #########################################################################
    # Step 7 - Enable switch ports
    ##########################################################################

    def test_enable_switch_interfaces(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 7 - Enable all the switchs interfaces")
        LogOutput('info', "###############################################")

        switch1Interface1 = dut01Obj.linkPortMapping['lnk01']
        switch1Interface2 = dut01Obj.linkPortMapping['lnk02']
        switch1Interface3 = dut01Obj.linkPortMapping['lnk03']

        listSwitchInterfacesDut1 = [
            switch1Interface1,
            switch1Interface2,
            switch1Interface3]

        switch2Interface1 = dut02Obj.linkPortMapping['lnk02']
        switch2Interface2 = dut02Obj.linkPortMapping['lnk03']
        switch2Interface3 = dut02Obj.linkPortMapping['lnk04']

        listSwitchInterfacesDut2 = [
            switch2Interface1,
            switch2Interface2,
            switch2Interface3]

        # Enable ports from switch 1
        for currentInterface in listSwitchInterfacesDut1:
            retStruct = InterfaceEnable(
                deviceObj=dut01Obj,
                enable=True,
                interface=currentInterface)

            if retStruct.returnCode() != 0:
                LogOutput('error', "Failed to enable port on switch")
                assert(False)
        # Enable ports from switch 2
        for currentInterface in listSwitchInterfacesDut2:
            retStruct = InterfaceEnable(
                deviceObj=dut02Obj,
                enable=True,
                interface=currentInterface)

            if retStruct.returnCode() != 0:
                LogOutput('error', "Failed to enable port on switch")
                assert(False)

    ##########################################################################
    # Step 8 - Send and validated traffic
    ##########################################################################

    def test_send_validated_traffic(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 8 - Send and validated traffic")
        LogOutput('info', "###############################################")

        # Check ports for delta

        interfaceLag1 = dut01Obj.linkPortMapping['lnk02']
        interfaceLag2 = dut01Obj.linkPortMapping['lnk03']

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

        # Send UDP packets
        for index in range(0,10):
            retStructValid = hostIperfServerStart(deviceObj=wrkston02Obj,
                                               protocol="UDP",
                                               port=5001)

            if retStructValid.returnCode() != 0:
                LogOutput('error',
                          "Failed to receive UDP packets on workstation 2")
                assert(False)
            else:
                LogOutput('info', "iperf server configured")

            retStructValid = hostIperfClientStart(deviceObj=wrkston01Obj,
                                               serverIP=l2IpAddress[1],
                                               time=100,
                                               protocol="UDP",
                                               port=5001)

            if retStructValid.returnCode() != 0:
                LogOutput('error',
                          "Failed to send UDP packets from workstation 1")
                assert(False)
            else:
                LogOutput('info', "iperf client configured")

            retStructValid = hostIperfClientStop(deviceObj=wrkston01Obj)

            if retStructValid.returnCode() != 0:
                LogOutput('error', "Failed to stop iperf on workstation 1")
                assert(False)
            else:
                LogOutput('info', "iperf client stopped")

            retStructValid = hostIperfServerStop(deviceObj=wrkston02Obj)

            if retStructValid.returnCode() != 0:
                LogOutput('error', "Failed to stop iperf on workstation2")
                assert(False)
            else:
                LogOutput('info', "iperf server stopped")

        sleep(10)

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

        tx1Firts = retTxIntStruct1.valueGet(key='TX')
        tx1Firts = tx1Firts['outputPackets']

        tx2Firts = retTxIntStruct2.valueGet(key='TX')
        tx2Firts = tx2Firts['outputPackets']

        LogOutput('info', "Values fot the firts ping :")
        LogOutput('info', "Interface clean is : " + str(tx1Firts))
        LogOutput('info', "Interface clean is : " + str(tx2Firts))


        # Operations to see if traffic was distributed
        raw1Tx = (int(tx1Firts) - int(tx1Delta))
        raw2Tx = (int(tx2Firts) - int(tx2Delta))

        if raw2Tx and  raw1Tx > 0:
            LogOutput('info', "Traffic in ports was distributed ")
        else:
            LogOutput('error', "Traffic not was distributed")
            assert(False)

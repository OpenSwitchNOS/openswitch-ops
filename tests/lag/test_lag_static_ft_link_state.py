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
# Name:        test_lag_static_ft_link_state.py
#
# Description: Tests that states in the lacp are correct transmitted correctly
#
# Author:      Randall Loaiza
#
# Topology:  |Host| ----- |Switch| ---------------------- |Switch| ----- |Host|
#                                   (Static LAG - 2 links)
#
# Success Criteria:  PASS -> No information on LACP transmitted
#
#                    FAILED -> LACP informatio transmitted
#
###############################################################################
import pytest
import re
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *

topoDict = {"topoExecution": 2500,
            "topoTarget": "dut01 dut02",
            "topoDevices":
                "dut01 dut02 wrkston01 wrkston02 wrkston03 wrkston04",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut01:wrkston02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut01:dut02,\
                          lnk05:dut02:wrkston03,\
                          lnk06:dut02:wrkston04",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston01:docker-image: openswitch/ubuntutest,\
                            wrkston02:system-category:workstation,\
                            wrkston02:docker-image: openswitch/ubuntutest,\
                            wrkston03:system-category:workstation,\
                            wrkston03:docker-image: openswitch/ubuntutest,\
                            wrkston04:system-category:workstation,\
                            wrkston04:docker-image: openswitch/ubuntutest"}


def switch_reboot(dut01):
    # Reboot switch
    LogOutput('info', "Reboot switch")
    dut01.Reboot()
    rebootRetStruct = returnStruct(returnCode=0)
    return rebootRetStruct


def vlanVerify(dut, pVlan):
    ''' Verify a vlan exist on VLAN table.

    Args:
         dut (obj) : device under test
         pVlan (str) : vlan name to verify

    '''

    LogOutput('info', "Validating VLAN")
    cont = 0
    devRetStruct = ShowVlan(deviceObj=dut)
    returnData = devRetStruct.buffer()
    vlans = re.findall('[vV][lL][aA][nN]([0-9]+)\s', returnData)
    for vlan in vlans:
        if vlan == str(pVlan):
            cont = cont + 1
    if cont == 1:
        return True
    else:
        return False


def vlanVerifyPorts(dut, vlanID, port):
    # Verify if port is part of a VLAN
    assigned = False
    helper = re.search('lag ', port)
    if helper:
        port = port.replace(' ', '')
    returnCLS = ShowVlan(deviceObj=dut)
    output = returnCLS.buffer()
    output = re.search(r'\r\n(%d .+?)\r' % vlanID, output)
    if not output:
        LogOutput('error', 'Could not find VLAN %d to which ' % vlanID +
                  'ports could be assigned')
        return False
    output = output.group(1)
    helper = ''
    helperList = []
    count = 0
    foundLetter = False
    for i in xrange(len(output) - 1, 0, -1):
        if not foundLetter:
            if output[i] != ' ':
                foundLetter = True
                continue
        else:
            if output[i] == ' ':
                count += 1
                if count > 1:
                    helper = output[i + 2:]
                    helperList = helper.split(', ')
                    break
            else:
                count = 0
    if port in helperList:
        assigned = True
        LogOutput('info', 'Found interface %s in VLAN %d' %
                  (port, vlanID))
    else:
        LogOutput('error', 'Could not find interface %s in VLAN %d' %
                  (port, vlanID))
    return assigned


def check_lacp_status(dut01, interfaceLag):
    # Recover vlan information from running config from specific VLAN
    # Variables
    overallBuffer = []
    bufferString = ""
    command = ""

    if dut01 is None:
        LogOutput('error', "Need to pass switch dut01 to this routine")
        returnCls = returnStruct(returnCode=1)
        return returnCls

    command = "ovs-vsctl list port " + str(interfaceLag)
    LogOutput('info', "Show LACP status " + command)
    returnDevInt = dut01.DeviceInteract(command=command)
    retCode = returnDevInt['returnCode']
    overallBuffer.append(returnDevInt['buffer'])

    if retCode != 0:
        LogOutput('error', "Failed to get information ." + command)

    ###########################################################################
    # Exit for context and validet buffer with information
    ###########################################################################

    for curLine in overallBuffer:
        bufferString += str(curLine)

    lacpStatus = dict()
    lacpElements = dict()
    regEx = 'lacp_status\s*:\s*{bond_speed="(\d*)"\s*,\s*bond_status=(\w*)\s*}'
    lacpElements = re.findall(regEx, bufferString)

    if lacpElements:
        lacpStatus['bond_speed'] = lacpElements[0][0]
        lacpStatus['bond_status'] = lacpElements[0][1]
    else:
        assert(False)

    lacpElements = re.findall(
        r'lacp\s+?: (active|passive|off|\[\])',
        bufferString)
    if lacpElements:
        lacpStatus['bond_mode'] = lacpElements[0]
    else:
        assert(False)
    return lacpStatus



    # Recover vlan information from running config from specific VLAN
    # Variables
    overallBuffer = []
    bufferString = ""
    command = ""

    if dut01 is None:
        LogOutput('error', "Need to pass switch dut01 to this routine")
        returnCls = returnStruct(returnCode=1)
        return returnCls

    command = "ovs-vsctl list interface " + str(interface)
    LogOutput('info', "Show LACP status in interface " + command)
    returnDevInt = dut01.DeviceInteract(command=command)
    retCode = returnDevInt['returnCode']
    overallBuffer.append(returnDevInt['buffer'])

    if retCode != 0:
        LogOutput('error', "Failed to get information ." + command)

    ###########################################################################
    # Exit for context and validet buffer with information
    ###########################################################################

    for curLine in overallBuffer:
        bufferString += str(curLine)

    lacpInterfaceStatus = dict()
    lacpInterfaceElements = re.findall(
        'lacp_current\s*:\s(true|false|\[\])\s*', bufferString)

    lacpInterfaceStatus['lacp_current'] = lacpInterfaceElements[0].strip()

    lacpInterfaceElements = re.findall(
        'actor_key="(\d*)"\s*', bufferString)
    lacpInterfaceStatus['actor_key'] = lacpInterfaceElements[0]

    lacpInterfaceElements = re.findall(
        'actor_port_id="(\d*,\d*)"', bufferString)
    lacpInterfaceStatus['actor_port_id'] = lacpInterfaceElements[0]

    stateRegEx = r'actor_state="Activ:(\d*),TmOut:(\d*),Aggr:(\d*),' + \
        r'Sync:(\d*),Col:(\d*),Dist:(\d*),Def:(\d*),Exp:(\d*)"'

    lacpInterfaceElements = re.findall(stateRegEx, bufferString)
    actorFlags = dict()

    if lacpInterfaceElements:
        actorFlags['Activ'] = lacpInterfaceElements[0][0]
        actorFlags['TmOut'] = lacpInterfaceElements[0][1]
        actorFlags['Aggr'] = lacpInterfaceElements[0][2]
        actorFlags['Sync'] = lacpInterfaceElements[0][3]
        actorFlags['Col'] = lacpInterfaceElements[0][4]
        actorFlags['Dist'] = lacpInterfaceElements[0][5]
        actorFlags['Def'] = lacpInterfaceElements[0][6]
        actorFlags['Exp'] = lacpInterfaceElements[0][7]

    lacpInterfaceStatus['actor_state'] = actorFlags

    lacpInterfaceElements = re.findall(
        'actor_system_id="(\d*,.{2}:.{2}:.{2}:.{2}:.{2}:.{2})"', bufferString)
    lacpInterfaceStatus['actor_system_id'] = lacpInterfaceElements[0]

    lacpInterfaceElements = re.findall(
        'partner_key="(\d*)"\s*', bufferString)
    lacpInterfaceStatus['partner_key'] = lacpInterfaceElements[0]

    lacpInterfaceElements = re.findall(
        'partner_port_id="(\d*,\d*)"', bufferString)
    lacpInterfaceStatus['partner_port_id'] = lacpInterfaceElements[0]

    stateRegEx = r'partner_state="Activ:(\d*),TmOut:(\d*),Aggr:(\d*),' + \
        r'Sync:(\d*),Col:(\d*),Dist:(\d*),Def:(\d*),Exp:(\d*)"'

    lacpInterfaceElements = re.findall(stateRegEx, bufferString)

    partnerFlags = dict()
    if lacpInterfaceElements:
        partnerFlags['Activ'] = lacpInterfaceElements[0][0]
        partnerFlags['TmOut'] = lacpInterfaceElements[0][1]
        partnerFlags['Aggr'] = lacpInterfaceElements[0][2]
        partnerFlags['Sync'] = lacpInterfaceElements[0][3]
        partnerFlags['Col'] = lacpInterfaceElements[0][4]
        partnerFlags['Dist'] = lacpInterfaceElements[0][5]
        partnerFlags['Def'] = lacpInterfaceElements[0][6]
        partnerFlags['Exp'] = lacpInterfaceElements[0][7]

    lacpInterfaceStatus['partner_state'] = partnerFlags

    lacpInterfaceElements = re.findall(
        'partner_system_id="(\d*,.{2}:.{2}:.{2}:.{2}:.{2}:.{2})"',
        bufferString
    )
    if lacpInterfaceElements:
        lacpInterfaceStatus['partner_system_id'] = lacpInterfaceElements[0]

    return lacpInterfaceStatus


def interfaceGetStatus(dev, interface):
    # Gets the status of a switch interface
    output = showInterface(deviceObj=dev, interface=interface).buffer()
    ret_expression = re.search(
        r'Interface [\d-]+? is (down|up)',
        output
    )
    if ret_expression.group(1) == "up":
        return True
    return False


def clean_up(
    dut01,
    dut02,
    wrkston01,
    wrkston02,
    wrkston03,
    wrkston04,
    l2IpAddress,
    l2IpNetmask,
    l2IpNetwork,
    vlanL2Id
):

    listDut = [dut01, dut02]
    for currentDut in listDut:
        devRebootRetStruct = switch_reboot(currentDut)
        if devRebootRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to reboot Switch")
            assert(False)
    else:
        LogOutput('info', "Passed Switch Reboot ")
    # WORKSTATION UNCONFIG

    wrkston01Obj.NetworkConfig(
        ipAddr=l2IpAddress[0],
        netMask=l2IpNetmask,
        broadcast=l2IpNetwork,
        interface=wrkston01Obj.linkPortMapping['lnk01'],
        config=False)

    wrkston02Obj.NetworkConfig(
        ipAddr=l2IpAddress[1],
        netMask=l2IpNetmask,
        broadcast=l2IpNetwork,
        interface=wrkston02Obj.linkPortMapping['lnk02'],
        config=False)

    wrkston03Obj.NetworkConfig(
        ipAddr=l2IpAddress[2],
        netMask=l2IpNetmask,
        broadcast=l2IpNetwork,
        interface=wrkston03Obj.linkPortMapping['lnk05'],
        config=False)

    wrkston04Obj.NetworkConfig(
        ipAddr=l2IpAddress[3],
        netMask=l2IpNetmask,
        broadcast=l2IpNetwork,
        interface=wrkston04Obj.linkPortMapping['lnk06'],
        config=False)

    lagCreation(
        deviceObj=dut01Obj,
        lagId=lagId,
        configFlag=False)
    lagCreation(
        deviceObj=dut02Obj,
        lagId=lagId,
        configFlag=False)

    for currentVlan in vlanL2Id:
        VlanStatus(
            deviceObj=dut01Obj,
            vlanId=currentVlan,
            status=False)
        VlanStatus(
            deviceObj=dut02Obj,
            vlanId=currentVlan,
            status=False)


class test_lag_static_ft_link_state:

    listDut = None
    dut01Obj = None
    dut02Obj = None
    wrkston01Obj = None
    wrkston02Obj = None
    wrkston03Obj = None
    wrkston04Obj = None
    lagId = None
    l2IpAddress = None
    l2IpGateway = None
    l2IpNetwork = None
    l2IpNetmask = None
    vlanL2Id = None

    def setup_class(cls):

        # Create Topology object and connect to devices
        test_lag_static_ft_link_state.testObj = testEnviron(
            topoDict=topoDict)
        test_lag_static_ft_link_state.topoObj = \
            test_lag_static_ft_link_state.testObj.topoObjGet()

        # Global definition
        global listDut
        global dut01Obj
        global dut02Obj
        global wrkston01Obj
        global wrkston02Obj
        global wrkston03Obj
        global wrkston04Obj
        global lagId
        global l2IpAddress
        global l2IpGateway
        global l2IpNetwork
        global l2IpNetmask
        global vlanL2Id

        # Var initiation
        lagId = 1
        l2IpAddress = ["10.2.2.100", "10.2.2.101", "10.2.2.102", "10.2.2.103"]
        l2IpGateway = "10.2.2.1"
        l2IpNetwork = "10.2.2.255"
        l2IpNetmask = "255.255.255.0"
        vlanL2Id = [900, 950]
        dut01Obj = cls.topoObj.deviceObjGet(device="dut01")
        dut02Obj = cls.topoObj.deviceObjGet(device="dut02")

        wrkston01Obj = cls.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = cls.topoObj.deviceObjGet(device="wrkston02")
        wrkston03Obj = cls.topoObj.deviceObjGet(device="wrkston03")
        wrkston04Obj = cls.topoObj.deviceObjGet(device="wrkston04")

        listDut = [dut01Obj, dut02Obj]

    def teardown_class(cls):
        # Terminate all nodes
        clean_up(dut01Obj,
                 dut02Obj,
                 wrkston01Obj,
                 wrkston02Obj,
                 wrkston03Obj,
                 wrkston04Obj,
                 l2IpAddress,
                 l2IpNetmask,
                 l2IpNetwork,
                 vlanL2Id)

        test_lag_static_ft_link_state.topoObj.terminate_nodes()

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

        LogOutput('info', "######Validated status of the switches#######")
        for currentDut in listDut:
            devRunRetStruc = showRun(deviceObj=currentDut).buffer()
            isEmptyConfig = re.search(r':\s*!\s*!\s*!\s*(.*)\s*exit',
                                      devRunRetStruc, re.DOTALL)
            isEmptyConfig = isEmptyConfig.group(1)
            print devRunRetStruc
            if isEmptyConfig != "":
                LogOutput(
                    'error', "DUT doesn't clean configuration after reboot")
                assert(False)
            else:
                LogOutput('info', "Passed DUT are clean after reboot")

    ##########################################################################
    # Step 2 - Enable switch ports
    ##########################################################################

    def test_enable_switch_interfaces(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 2 - Enable all the switchs interfaces")
        LogOutput('info', "###############################################")

        switchInterface1 = dut01Obj.linkPortMapping['lnk01']
        switchInterface2 = dut01Obj.linkPortMapping['lnk02']
        switchInterface3 = dut01Obj.linkPortMapping['lnk03']
        switchInterface4 = dut01Obj.linkPortMapping['lnk04']

        listSwitchInterfacesDut1 = [
            switchInterface1,
            switchInterface2,
            switchInterface3,
            switchInterface4]

        switchInterface1 = dut02Obj.linkPortMapping['lnk03']
        switchInterface2 = dut02Obj.linkPortMapping['lnk04']
        switchInterface3 = dut02Obj.linkPortMapping['lnk05']
        switchInterface4 = dut02Obj.linkPortMapping['lnk06']

        listSwitchInterfacesDut2 = [
            switchInterface1,
            switchInterface2,
            switchInterface3,
            switchInterface4]

        # Enable ports from switch 1
        for currentInterface in listSwitchInterfacesDut1:
            retStruct = InterfaceEnable(
                deviceObj=dut01Obj,
                enable=True,
                interface=currentInterface)

            if retStruct.returnCode() != 0:
                LogOutput('error', "Failed to enable port on switch")
                assert(False)
            LogOutput('info', "Interface enabled %s " % currentInterface)
        # Enable ports from switch 2
        for currentInterface in listSwitchInterfacesDut2:
            retStruct = InterfaceEnable(
                deviceObj=dut02Obj,
                enable=True,
                interface=currentInterface)

            if retStruct.returnCode() != 0:
                LogOutput('error', "Failed to enable port on switch")
                assert(False)
            LogOutput('info', "Interface enabled %s " % currentInterface)

    ##########################################################################
    # Step 3 - Configured Lag
    ##########################################################################

    def test_configure_lag(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 3 - Configure lag in the switch")
        LogOutput('info', "###############################################")

        devLagRetStruct1 = lagCreation(
            deviceObj=dut01Obj,
            lagId=lagId,
            configFlag=True)
        devLagRetStruct2 = lagCreation(
            deviceObj=dut02Obj,
            lagId=lagId,
            configFlag=True)

        if devLagRetStruct1.returnCode() != 0 \
                or devLagRetStruct2.returnCode() != 0:
                    LogOutput(
                        'error', "Failed to configured lag in the switchs")
                    assert(False)
        else:
            LogOutput('info', "Passed lag configured ")

    ##########################################################################
    # Step 4 - Add ports to lag
    ##########################################################################

    def test_configure_interface_lag(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 4 - Configure lag id in the interface")
        LogOutput('info', "###############################################")

        dut01Interface01 = dut01Obj.linkPortMapping['lnk03']
        dut01Interface02 = dut01Obj.linkPortMapping['lnk04']

        dut02Interface01 = dut02Obj.linkPortMapping['lnk03']
        dut02Interface02 = dut02Obj.linkPortMapping['lnk04']

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
    # Step 5 - Enable dynamic Lag
    ##########################################################################

    def test_enable_dynamic_lag(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 5 - Enable dynamic Lag ")
        LogOutput('info', "###############################################")

        devLagDinRetStruct1 = lagMode(
            deviceObj=dut01Obj,
            lagId=lagId,
            lacpMode="active")

        devLagDinRetStruct2 = lagMode(
            deviceObj=dut02Obj,
            lagId=lagId,
            lacpMode="active")
        if devLagDinRetStruct1.returnCode() != 0 \
                or devLagDinRetStruct2.returnCode() != 0:
            LogOutput('error', "Failed to enable dynamic lag")
            assert(False)
        else:
            LogOutput('info', "Enable dynamic lag")

        LogOutput('info', "####Validated status of the created LACP#######")

        interfaceLagName = "lag" + str(lagId)
        lacpDUT01Info = check_lacp_status(dut01Obj, interfaceLagName)
        lacpDUT02Info = check_lacp_status(dut02Obj, interfaceLagName)

        # FIXME validate LACP type
        if lacpDUT01Info['bond_status'] != "ok" and \
                lacpDUT02Info['bond_status'] != "ok" and \
                lacpDUT02Info['bond_mode'] != "active" and \
                lacpDUT01Info['bond_mode'] != "active":
            LogOutput('error', "Lacp not stablished")
            assert(false)
        else:
            LogOutput('info', "LACP connected in Active mode")

        # Information from partner has to be equal

        LogOutput('info', "#######Checking status of lag#######")
        DUT1Int1 = dut01Obj.linkPortMapping['lnk03']
        DUT1Int2 = dut01Obj.linkPortMapping['lnk04']
        lacpDUT01Int1 = check_lacp_interface_status(dut01Obj, DUT1Int1)
        lacpDUT01Int2 = check_lacp_interface_status(dut01Obj, DUT1Int2)

        DUT2Int1 = dut02Obj.linkPortMapping['lnk03']
        DUT2Int2 = dut02Obj.linkPortMapping['lnk04']
        lacpDUT02Int1 = check_lacp_interface_status(dut02Obj, DUT2Int1)
        lacpDUT02Int2 = check_lacp_interface_status(dut02Obj, DUT2Int2)
        if lacpDUT01Int1['lacp_current'] != "true" and \
                lacpDUT01Int2['lacp_current'] != "true" and \
                lacpDUT02Int1['lacp_current'] != "true" and \
                lacpDUT02Int2['lacp_current'] != "true":
            LogOutput('error', "Lacp are not established")
            assert(False)
        else:
            LogOutput('info', "All interface enable lacp")
        LogOutput('info', "Check if link communicated ")
        if lacpDUT01Int1['actor_system_id'] != \
                lacpDUT02Int1['partner_system_id'] and \
                lacpDUT01Int1['actor_port_id'] != \
                lacpDUT02Int1['partner_port_id']:
            LogOutput('error', "Lacp misconfigured")
            assert(False)
        else:
            LogOutput('info', "Communication established in the interfaces")

    ##########################################################################
    # Step 6 - Configured vlan
    ##########################################################################

    def test_configure_vlan(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 6 -Configure vlan  in the switch")
        LogOutput('info', "###############################################")

        for currentVlan in vlanL2Id:
            devLagRetStruct1 = AddVlan(
                deviceObj=dut01Obj,
                vlanId=currentVlan,
                config=True)

            devLagRetStruct2 = AddVlan(
                deviceObj=dut02Obj,
                vlanId=currentVlan,
                config=True)

            if devLagRetStruct1.returnCode() != 0 \
                    or devLagRetStruct2.returnCode() != 0:
                LogOutput('error', "Failed to create vlan in the switchs")
                assert(False)
            else:
                LogOutput('info', "Vlan created")

        for currentVlan in vlanL2Id:
            devLagRetStruct1 = VlanStatus(
                deviceObj=dut01Obj,
                vlanId=currentVlan,
                status=True)
            devLagRetStruct2 = VlanStatus(
                deviceObj=dut02Obj,
                vlanId=currentVlan,
                status=True)

            if devLagRetStruct1.returnCode() != 0 \
                    or devLagRetStruct2.returnCode() != 0:
                LogOutput('error', "Failed to enable the vlan in the switchs")
                assert(False)
            else:
                LogOutput('info', "Passed vlan enable ")

        LogOutput('info', "#######Checking VLAN creation#######")

        for currentDUT in listDut:
            for currentVLAN in vlanL2Id:
                if vlanVerify(currentDUT, currentVLAN):
                    LogOutput(
                        'info',
                        "Vlan %s configured in %s" %
                        (currentVLAN, currentDUT))
                else:
                    LogOutput(
                        'error',
                        "Vlan %s isn't configured in %s" %
                        (currentVLAN, currentDUT))
                    assert(False)

    ##########################################################################
    # Step 7 - Add ports to vlan
    ##########################################################################

    def test_interface_vlan(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 7 - Configure vlan in  the interface")
        LogOutput('info', "###############################################")

        dut01Interface01 = dut01Obj.linkPortMapping['lnk01']
        dut01Interface02 = dut01Obj.linkPortMapping['lnk02']
        dut01Interface03 = "lag " + str(lagId)

        dut02Interface01 = dut02Obj.linkPortMapping['lnk05']
        dut02Interface02 = dut02Obj.linkPortMapping['lnk06']
        dut02Interface03 = "lag " + str(lagId)

        switchInterface1 = dut01Obj.linkPortMapping['lnk01']
        switchInterface2 = dut01Obj.linkPortMapping['lnk02']
        switchInterface3 = dut01Obj.linkPortMapping['lnk03']
        switchInterface4 = dut01Obj.linkPortMapping['lnk04']

        listSwitchInterfacesDut1 = [
            switchInterface1,
            switchInterface2,
            switchInterface3,
            switchInterface4]

        switchInterface1 = dut02Obj.linkPortMapping['lnk03']
        switchInterface2 = dut02Obj.linkPortMapping['lnk04']
        switchInterface3 = dut02Obj.linkPortMapping['lnk05']
        switchInterface4 = dut02Obj.linkPortMapping['lnk06']

        listSwitchInterfacesDut2 = [
            switchInterface1,
            switchInterface2,
            switchInterface3,
            switchInterface4]

        # Configured Vlan for device 1
        devIntLagRetStruct1 = AddPortToVlan(
            deviceObj=dut01Obj,
            vlanId=vlanL2Id[0],
            interface=dut01Interface01,
            access=True,
            config=True)

        devIntLagRetStruct2 = AddPortToVlan(
            deviceObj=dut01Obj,
            vlanId=vlanL2Id[1],
            interface=dut01Interface02,
            access=True,
            config=True)

        if devIntLagRetStruct1.returnCode() != 0 \
                or devIntLagRetStruct2.returnCode() != 0:
            LogOutput('error',
                      "Failed to configured vlan in the interface")
            assert(False)
        else:
            LogOutput('info', "Passed interface vlan configured")

        # Configured Vlan for device 2
        devIntLagRetStruct1 = AddPortToVlan(
            deviceObj=dut02Obj,
            vlanId=vlanL2Id[0],
            interface=dut02Interface01,
            access=True,
            config=True)

        devIntLagRetStruct2 = AddPortToVlan(
            deviceObj=dut02Obj,
            vlanId=vlanL2Id[1],
            interface=dut02Interface02,
            access=True,
            config=True)

        if devIntLagRetStruct1.returnCode() != 0 \
                or devIntLagRetStruct2.returnCode() != 0:
            LogOutput('error',
                      "Failed to configured vlan in the interface")
            assert(False)
        else:
            LogOutput('info', "Passed interface vlan configured")

        for currentVlan in vlanL2Id:
            devIntLagRetStruct1 = AddPortToVlan(
                deviceObj=dut01Obj,
                vlanId=currentVlan,
                interface=dut01Interface03,
                allowed=True,
                config=True)

            devIntLagRetStruct2 = AddPortToVlan(
                deviceObj=dut02Obj,
                vlanId=currentVlan,
                interface=dut02Interface03,
                allowed=True,
                config=True)

            if devIntLagRetStruct1.returnCode() != 0 \
                    or devIntLagRetStruct2.returnCode() != 0:
                LogOutput('error',
                          "Failed to configured vlan in the Lag")
                assert(False)
            else:
                LogOutput('info', "Passed Lag vlan configured")

        LogOutput('info', "######Validated status of the interfaces#######")

        for currentInterface in listSwitchInterfacesDut1:
            if interfaceGetStatus(dut01Obj, currentInterface):
                LogOutput('info', "Interface UP")
            else:
                LogOutput('info', "Interface down")

        for currentInterface in listSwitchInterfacesDut2:
            if interfaceGetStatus(dut01Obj, currentInterface):
                LogOutput('info', "Interface UP")
            else:
                LogOutput('info', "Interface down")

        LogOutput('info', "All ports in switches are enable")

        LogOutput('info', "######Validated vlan interfaces#######")

        for currentDUT in listDut:
            for currentVlan in vlanL2Id:
                if vlanVerifyPorts(currentDUT, currentVlan, dut01Interface03):
                    LogOutput(
                        'info', "Interface %s with vlan %s" %
                        (dut01Interface01, currentVlan))
                else:
                    LogOutput(
                        'error', "Interface %s is not conf vlan %s" %
                        (dut01Interface01, currentVlan))
                    assert(False)
        if vlanVerifyPorts(dut01Obj, vlanL2Id[0], dut01Interface01):
            LogOutput(
                'info', "Interface %s with vlan %s" %
                (dut01Interface01, currentVlan))
        else:
            LogOutput(
                'error', "Interface %s is not conf vlan %s" %
                (dut01Interface01, currentVlan))
            assert(False)
        if vlanVerifyPorts(dut01Obj, vlanL2Id[1], dut01Interface02):
            LogOutput(
                'info', "Interface %s with vlan %s" %
                (dut01Interface01, currentVlan))
        else:
            LogOutput(
                'error', "Interface %s is not conf vlan %s" %
                (dut01Interface01, currentVlan))
            assert(False)
        if vlanVerifyPorts(dut02Obj, vlanL2Id[0], dut02Interface01):
            LogOutput(
                'info', "Interface %s with vlan %s" %
                (dut01Interface01, currentVlan))
        else:
            LogOutput(
                'error', "Interface %s is not conf vlan %s" %
                (dut01Interface01, currentVlan))
            assert(False)
        if vlanVerifyPorts(dut02Obj, vlanL2Id[1], dut02Interface02):
            LogOutput(
                'info', "Interface %s with vlan %s" %
                (dut01Interface01, currentVlan))
        else:
            LogOutput(
                'error', "Interface %s is not conf vlan %s" %
                (dut01Interface01, currentVlan))
            assert(False)

    ##########################################################################
    # Step 8 - Configure Workstation
    ##########################################################################

    def test_configure_workstations(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 8 - Configure Workstations")
        LogOutput('info', "###############################################")

        # Client Side
        retStruct = wrkston01Obj.NetworkConfig(
            ipAddr=l2IpAddress[0],
            netMask=l2IpNetmask,
            broadcast=l2IpNetwork,
            interface=wrkston01Obj.linkPortMapping['lnk01'],
            config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configured Client station")
            assert(False)

        # Server side
        retStruct = wrkston02Obj.NetworkConfig(
            ipAddr=l2IpAddress[1],
            netMask=l2IpNetmask,
            broadcast=l2IpNetwork,
            interface=wrkston02Obj.linkPortMapping['lnk02'],
            config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configured Client station")
            assert(False)

        retStruct = wrkston03Obj.NetworkConfig(
            ipAddr=l2IpAddress[2],
            netMask=l2IpNetmask,
            broadcast=l2IpNetwork,
            interface=wrkston03Obj.linkPortMapping['lnk05'],
            config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configured Client station")
            assert(False)

        retStruct = wrkston04Obj.NetworkConfig(
            ipAddr=l2IpAddress[3],
            netMask=l2IpNetmask,
            broadcast=l2IpNetwork,
            interface=wrkston04Obj.linkPortMapping['lnk06'],
            config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configured Client station")
            assert(False)

        LogOutput('info', "Complete workstation configuration")

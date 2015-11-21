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
##########################################################################
# Description: Verify a switch port ability to handle tagged frames
#              received on an access port.
#
# Author:      Jose Pablo Araya
#
# Topology:       |workStation|-------|Switch|-------|workStation|
#
# Success Criteria:  PASS -> Vlan forward traffic correctly and drop it
#                            if necessary
#
#                    FAILED -> Vlan is not forwarding traffic propertly
#
###########################################################################

import pytest
import re
from opstestfw.switch.CLI import *
from opstestfw import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01",
            "topoDevices": "dut01 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,lnk02:dut01:wrkston02",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation"}

# verifyPing success or failure


def verifyPing(dut, pIp, condition="not forwarded"):
    value = "100% "
    if condition != "not forwarded":
        value = "0% "
    command = 'ping -c 5 ' + pIp + "\n"
    dut.expectHndl.send(command)
    time.sleep(10)
    dut.expectHndl.expect('#')
    result = re.findall(r'(\d*%\s\w*\s\w*)', dut.expectHndl.before)
    if result[0] != value + "packet loss":
        LogOutput('error', "Error while checking traffic")
        return False
    else:
        LogOutput('info', "Result: " + dut.expectHndl.before)
        LogOutput('info',
                  "Passed traffic {condition} as \
                   expected".format(condition=condition))
    return True

# Configure an interface as trunk port


def configureInterface(dut, pInterface, pVlanId,
                       pMask, pPhysicalIp, pLogicalIp):
    LogOutput('info', "Configure interface: " + str(pInterface))
    # Enable physical interface
    command = "ifconfig " + pInterface + ' up' + "\n"
    dut.expectHndl.send(command)
    dut.expectHndl.expect('#')
    # Create logical interface
    command = "ip link add link " + pInterface + " name " + \
        'eth' + '.' + pVlanId + ' type vlan id ' + pVlanId + "\n"
    dut.expectHndl.send(command)
    dut.expectHndl.expect('#')
    # Enable logical interface
    command = 'ifconfig ' + 'eth' + '.' + pVlanId + ' ' + \
        pLogicalIp + ' netmask ' + pMask + ' up' + "\n"
    dut.expectHndl.send(command)
    dut.expectHndl.expect('#')


# Unconfigure an interface as trunk port

def unconfigureInterface(dut, pInterface, pVlanId):
    LogOutput('info', "Unconfigure interface: " + str(pInterface))
    # Delete logical interface
    command = "ip link delete link " + pInterface + " name " + \
        'eth' + '.' + pVlanId + ' dev ' + 'eth.' + pVlanId + "\n"
    dut.expectHndl.send(command)
    dut.expectHndl.expect('#')
    # Delete physical interface ip address
    command = "ip addr flush dev " + pInterface + "\n"
    dut.expectHndl.send(command)
    dut.expectHndl.expect('#')


# Verify if a vlan is configured or not


def verifyVlan(dut, pVlan, pQuantity=0):
    LogOutput('info', "Validating vlan")
    cont = 0
    devRetStruct = ShowVlan(deviceObj=dut)
    returnData = devRetStruct.buffer()
    vlans = re.findall('VLAN[0-9]*', returnData)
    for vlan in vlans:
        if vlan == "VLAN" + str(pVlan):
            cont = cont + 1
    if cont == pQuantity:
        return 0
    else:
        return 1

# Configure vlans


def configureVlans(dut, vlans, configure=True):
    status = "adding"
    if configure is False:
        status = "delete"
    for vlan in vlans:
        if AddVlan(deviceObj=dut, vlanId=vlan,
                   config=configure).returnCode() != 0:
            LogOutput(
                'error',
                "Failed to {status} {vlan}".format(vlan=vlan, status=status))
            return False
        else:
            LogOutput(
                'info',
                "Passed {status} {vlan} ".format(vlan=vlan, status=status))
    return True


# Verify vlans


def verifyVlans(dut, vlans, existent=0):
    for vlan in vlans:
        if verifyVlan(dut, vlan, existent) != 0:
            LogOutput('error',
                      "Failed to validate vlan {pVlan} configuration"
                      .format(pVlan=str(vlan)))
            return False
        else:
            LogOutput(
                'info', "Passed validating vlan {vlan} ".format(vlan=vlan))
    return True


# To assign ports to vlans in Trunk Allowed


def portsAssign(dut, ports, vlans, access=False, allowed=True,
                tag=True, config=True):
    state = "configure"
    if config is False:
        state = "unconfigure"
    for port, vlan in zip(ports, vlans):
        returnStr = AddPortToVlan(
            deviceObj=dut, vlanId=vlan,
            interface=port, access=access,
            allowed=allowed, tag=tag, config=config)
        if returnStr.returnCode() != 0:
            LogOutput('error',
                      "Failed to {state} port {port} in vlan {vlan} ".format(
                          port=port, vlan=vlan, state=state))
            return False
        else:
            LogOutput('info',
                      "Passed {state} port {port} in vlan {vlan} ".format(
                          port=port, vlan=vlan, state=state))
    return True


# To verify ports assigned


def verifyPorts(dut, ports, vlans):
    for port, vlan in zip(ports, vlans):
        if verifyVlanPorts(dut, vlan, port) != 0:
            LogOutput('error', "Failed to verify port {pPort}".format(
                pPort=port))
            return False
        else:
            LogOutput('info', "Passed verifying port {pPort}".format(
                pPort=port))
    return True


# To enable interfaces


def enableInterfaces(dut, interfaces, pEnable):
    status = "enable"
    if pEnable is False:
        status = "disable"
    for interface in interfaces:
        returnStr = InterfaceEnable(
            deviceObj=dut,
            interface=interface, enable=pEnable,)
        if returnStr.returnCode() != 0:
            LogOutput('error',
                      "Failed to {status} interface {pInterface}".format(
                          pInterface=interface, status=status))
            return False
        else:
            LogOutput('info',
                      "Passed {status} interface {pInterface}".format(
                          pInterface=interface, status=status))
    return True


# To enable vlans

def enableVlans(dut, vlans):
    for vlan in vlans:
        if VlanStatus(deviceObj=dut, vlanId=vlan,
                      status=True).returnCode() != 0:
            LogOutput(
                'error', "Failed to enable vlan {vlan}".format(vlan=vlan))
            return False
        else:
            LogOutput('info', "Passed enabling vlan {vlan}".format(vlan=vlan))
    return True


# Verify a port has been assigned to a vlan


def verifyVlanPorts(dut, vlanID, port):
    assigned = False
    returnCLS = ShowVlan(deviceObj=dut)
    showVlanOutput = returnCLS.valueGet()
    for myDictionary in showVlanOutput:
        if myDictionary['VLAN'] == vlanID and \
                port in myDictionary['Ports']:
            assigned = True
            return assigned
    return assigned

# Configure workStations


def workStationConfig(wrk2, pConfig=True):
    if wrk2.NetworkConfig(
            interface=wrk2.linkPortMapping['lnk02'],
            ipAddr="10.1.1.6", netMask="255.255.255.0",
            broadcast="10.1.1.255", config=pConfig).returnCode() != 0:
        return False
    return True


def cleanUp(dut, wrk1, wrk2):
    LogOutput('info', "\n############################################")
    LogOutput('info', "CleanUp")
    LogOutput('info', "############################################")
    LogOutput('info', "CleanUp - Disable interfaces")
    interfaces = (dut.linkPortMapping['lnk01'],
                  dut.linkPortMapping['lnk02'])
    assert(enableInterfaces(dut, interfaces, False))
    LogOutput('info', "CleanUp - Delete vlan")
    vlans = list([4])
    assert(configureVlans(dut, vlans, False))
    LogOutput('info', "\nCleanUp - Unconfiguring workstations")
    unconfigureInterface(wrk1, wrk1.linkPortMapping['lnk01'], '4')
    unconfigureInterface(wrk2, wrk2.linkPortMapping['lnk02'], '4')
    LogOutput('info', "\nCleanUp - Reboot the Switch")
    devRebootRetStruct = dut.Reboot()
    devRebootRetStruct = returnStruct(returnCode=0)
    if devRebootRetStruct.returnCode() != 0:
        LogOutput('error', "Failed to reboot Switch")
        finalResult.append(devRebootRetStruct.returnCode())
    else:
        LogOutput('info', "Passed Switch Reboot piece")


class Test_ft_vlan_tagged_frames_trunk_port:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_ft_vlan_tagged_frames_trunk_port.testObj = \
            testEnviron(
                topoDict=topoDict)
        Test_ft_vlan_tagged_frames_trunk_port.topoObj = \
            Test_ft_vlan_tagged_frames_trunk_port.testObj.topoObjGet()
        Test_ft_vlan_tagged_frames_trunk_port.dut01Obj = \
            Test_ft_vlan_tagged_frames_trunk_port.topoObj.deviceObjGet(
                device="dut01")
        Test_ft_vlan_tagged_frames_trunk_port.wrkston01 = \
            Test_ft_vlan_tagged_frames_trunk_port.topoObj.deviceObjGet(
                device="wrkston01")
        Test_ft_vlan_tagged_frames_trunk_port.wrkston02 = \
            Test_ft_vlan_tagged_frames_trunk_port.topoObj.deviceObjGet(
                device="wrkston02")

    def teardown_class(cls):
        # Terminate all nodes
        cleanUp(cls.dut01Obj, cls.wrkston01, cls.wrkston02)
        Test_ft_vlan_tagged_frames_trunk_port.topoObj.terminate_nodes()

    def test_add_vlans(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 1- Adding vlan")
        LogOutput('info', "############################################")
        vlans = list([4])
        assert(configureVlans(self.dut01Obj, vlans))

    def test_enable_vlan(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 2- Enable vlan")
        LogOutput('info', "############################################")
        vlans = list([4])
        assert(enableVlans(self.dut01Obj, vlans))

    def test_verifyConfVlans(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 3- Verify vlan was configured ")
        LogOutput('info', "############################################")
        vlans = list([4])
        assert(verifyVlans(self.dut01Obj, vlans, 1))

    def test_addPort_vlans(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 4- Add ports to vlan")
        LogOutput('info', "############################################")
        vlans = (4, 4)
        interfaces = (self.dut01Obj.linkPortMapping['lnk01'],
                      self.dut01Obj.linkPortMapping['lnk02'])
        assert(portsAssign(self.dut01Obj, interfaces, vlans))

    def test_enable_interfaces(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 5- Enable interfaces as trunk allowed")
        LogOutput('info', "############################################")
        interfaces = (self.dut01Obj.linkPortMapping['lnk01'],
                      self.dut01Obj.linkPortMapping['lnk02'])
        assert(enableInterfaces(self.dut01Obj, interfaces, True))

    def test_added_ports(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 6- Verify ports assign correctly")
        LogOutput('info', "############################################")
        vlans = (4, 4)
        interfaces = (self.dut01Obj.linkPortMapping['lnk01'],
                      self.dut01Obj.linkPortMapping['lnk02'])
        assert(verifyPorts(self.dut01Obj, interfaces, vlans))

    def test_sendTraffic(self):
        LogOutput('info', "\n############################################")
        LogOutput(
            'info', "Step 7- Send signal and verify it works")
        LogOutput('info', "############################################")
        configureInterface(self.wrkston01, self.wrkston01.linkPortMapping[
                           'lnk01'], '4', '255.255.255.0',
                           '10.1.1.5', '10.1.1.2')
        configureInterface(self.wrkston02, self.wrkston02.linkPortMapping[
                           'lnk02'], '4', '255.255.255.0', '10.1.1.6',
                           '10.1.1.3')
        assert(verifyPing(self.wrkston01, '10.1.1.3', "forwarded"))
        assert(verifyPing(self.wrkston02, '10.1.1.2', "forwarded"))

    def test_changePort_vlans(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 8- Change ports as access mode")
        LogOutput('info', "############################################")
        vlans = (4, 4)
        interfaces = (self.dut01Obj.linkPortMapping['lnk01'],
                      self.dut01Obj.linkPortMapping['lnk02'])
        LogOutput('info', "Unconfiguring trunk allowed ports")
        assert(portsAssign(self.dut01Obj, interfaces, vlans, False, True,
                           True, False))
        LogOutput('info', "Configuring access mode ports")
        assert(portsAssign(self.dut01Obj, interfaces, vlans, True, False,
                           False, True))

    def test_sendTraffic2(self):
        LogOutput('info', "\n############################################")
        LogOutput(
            'info', "Step 9- Send signal and verify is not forwarded")
        LogOutput('info', "############################################")
        assert(verifyPing(self.wrkston01, '10.1.1.3', "not forwarded"))
        assert(verifyPing(self.wrkston02, '10.1.1.2', "not forwarded"))

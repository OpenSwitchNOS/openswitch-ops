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
# Description: Verify the functionality of deleting an existent and non
#              existent VLAN with ports/no ports configured within the VLAN
#
# Author:      Jose Pablo Araya
#
# Topology:       |workStation|-------|Switch|-------|workStation|
#
# Success Criteria:  PASS -> Vlans is correctly delete it with ports
#                            member and no ports
#
#                    FAILED -> If vlan is not correctly deleted
#
##########################################################################

import pytest
import re
from opstestfw.switch.CLI import *
from opstestfw import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01",
            "topoDevices": "dut01 wrkston01 wrkston02 wrkston03",
            "topoLinks": "lnk01:dut01:wrkston01,lnk02:dut01:wrkston02,\
                          lnk03:dut01:wrkston03",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation,\
                            wrkston03:system-category:workstation,\
                            wrkston01:docker-image: openswitch/ubuntutest,\
                            wrkston02:docker-image: openswitch/ubuntutest,\
                            wrkston03:docker-image: openswitch/ubuntutest"}


# Send broadcast traffic through nmap signal tool


def capture(deviceObj, interface, number=1):
    LogOutput('info', "Sending nmap signal")
    command = 'nmap -sP 10.1.1.1-254' + "\n"
    deviceObj.expectHndl.send(command)
    time.sleep(5)
    deviceObj.expectHndl.expect('#')
    result = re.findall('\(\d*\s\w*\s\w*\)', deviceObj.expectHndl.before)
    hostsNumber = re.findall('\d?', result[0])
    if hostsNumber[1] != number:
        LogOutput('error', "Error sending nmap signal")
        return False
    else:
        LogOutput('info', "nmap signal sent successfully")
        return True

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
            LogOutput('info', "Passed validating vlan {vlan} ".format(vlan=vlan))
    return True

# To assign ports to vlans


def portsAssign(dut, ports, vlans):
    for port, vlan in zip(ports, vlans):
        returnStr = AddPortToVlan(
            deviceObj=dut, vlanId=vlan,
            interface=port, access=True,
            allowed=False, tag=False, config=True)
        if returnStr.returnCode() != 0:
            LogOutput('error',
                      "Failed to add port {port} to vlan {vlan} ".format(
                          port=port, vlan=vlan))
            return False
        else:
            LogOutput('info',
                      "Passed adding port {port} to vlan {vlan} ".format(
                          port=port, vlan=vlan))
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

# Configure workStations


def workStationConfig(wrk1, wrk2, wrk3, pConfig=True):
    if wrk1.NetworkConfig(
            interface=wrk1.linkPortMapping['lnk01'],
            ipAddr="10.1.1.5", netMask="255.255.255.0",
            broadcast="10.1.1.255", config=pConfig).returnCode() != 0:
        return False

    if wrk2.NetworkConfig(
            interface=wrk2.linkPortMapping['lnk02'],
            ipAddr="10.1.1.6", netMask="255.255.255.0",
            broadcast="10.1.1.255", config=pConfig).returnCode() != 0:
        return False

    if wrk3.NetworkConfig(
            interface=wrk3.linkPortMapping['lnk03'],
            ipAddr="10.1.1.7", netMask="255.255.255.0",
            broadcast="10.1.1.255", config=pConfig).returnCode() != 0:
        return False
    return True


def cleanUp(dut, wrk1, wrk2, wrk3):
    LogOutput('info', "\n############################################")
    LogOutput('info', "CleanUp")
    LogOutput('info', "############################################")
    LogOutput('info', "CleanUp - Disable interfaces")
    interfaces = (dut.linkPortMapping['lnk01'],
                  dut.linkPortMapping['lnk02'],
                  dut.linkPortMapping['lnk03'])
    assert(enableInterfaces(dut, interfaces, False))
    LogOutput('info', "CleanUp - Delete vlans")
    vlans = (5, 6, 7)
    assert(configureVlans(dut, vlans, False))
    LogOutput('info', "\nCleanUp - Unconfiguring workstations")
    assert(workStationConfig(wrk1, wrk2, wrk3, False))
    LogOutput('info', "\nCleanUp - Reboot the Switch")
    devRebootRetStruct = dut.Reboot()
    devRebootRetStruct = returnStruct(returnCode=0)
    if devRebootRetStruct.returnCode() != 0:
        LogOutput('error', "Failed to reboot Switch")
        finalResult.append(devRebootRetStruct.returnCode())
    else:
        LogOutput('info', "Passed Switch Reboot piece")


class Test_vlan_state_removed_from_middle_of_table:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_vlan_state_removed_from_middle_of_table.testObj = testEnviron(
            topoDict=topoDict)
        Test_vlan_state_removed_from_middle_of_table.topoObj = \
            Test_vlan_state_removed_from_middle_of_table.testObj.topoObjGet()
        Test_vlan_state_removed_from_middle_of_table.dut01Obj = \
            Test_vlan_state_removed_from_middle_of_table.topoObj.deviceObjGet(
                device="dut01")
        Test_vlan_state_removed_from_middle_of_table.wrkston01 = \
            Test_vlan_state_removed_from_middle_of_table.topoObj.deviceObjGet(
                device="wrkston01")
        Test_vlan_state_removed_from_middle_of_table.wrkston02 = \
            Test_vlan_state_removed_from_middle_of_table.topoObj.deviceObjGet(
                device="wrkston02")
        Test_vlan_state_removed_from_middle_of_table.wrkston03 = \
            Test_vlan_state_removed_from_middle_of_table.topoObj.deviceObjGet(
                device="wrkston03")

    def teardown_class(cls):
        # Terminate all nodes
        cleanUp(cls.dut01Obj, cls.wrkston01, cls.wrkston02, cls.wrkston03)
        Test_vlan_state_removed_from_middle_of_table.topoObj.terminate_nodes()

    def test_add_vlans(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 1- Adding vlans")
        LogOutput('info', "############################################")
        vlans = (2, 3, 4, 5, 6, 7)
        assert(configureVlans(self.dut01Obj, vlans))

    def test_verifyConfVlans(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 2- Verify vlans were configured ")
        LogOutput('info', "############################################")
        vlans = (2, 3, 4, 5, 6, 7)
        assert(verifyVlans(self.dut01Obj, vlans, 1))

    def test_addPort_vlans(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 3- Add ports to vlans")
        LogOutput('info', "############################################")
        vlans = (2, 3, 4)
        interfaces = (self.dut01Obj.linkPortMapping['lnk01'],
                      self.dut01Obj.linkPortMapping['lnk02'],
                      self.dut01Obj.linkPortMapping['lnk03'])
        assert(portsAssign(self.dut01Obj, interfaces, vlans))

    def test_enable_interfaces(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 4- Enable interfaces")
        LogOutput('info', "############################################")
        interfaces = (self.dut01Obj.linkPortMapping['lnk01'],
                      self.dut01Obj.linkPortMapping['lnk02'],
                      self.dut01Obj.linkPortMapping['lnk03'])
        assert(enableInterfaces(self.dut01Obj, interfaces, True))

    def test_added_ports(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 5- Verify ports assign correctly")
        LogOutput('info', "############################################")
        vlans = (2, 3, 4)
        interfaces = (self.dut01Obj.linkPortMapping['lnk01'],
                      self.dut01Obj.linkPortMapping['lnk02'],
                      self.dut01Obj.linkPortMapping['lnk03'])
        assert(verifyPorts(self.dut01Obj, interfaces, vlans))

    def test_configureWorkStons(self):
        LogOutput(
            'info', "\n##################################################")
        LogOutput('info', "Step 6- Configure workstations")
        LogOutput(
            'info', "##################################################")
        assert(
            workStationConfig(self.wrkston01, self.wrkston02, self.wrkston03))

    def test_sendTraffic(self):
        LogOutput(
            'info', "\n#################################################")
        LogOutput('info', "Step 7- Send traffic")
        LogOutput(
            'info', "##################################################")
        assert(capture(deviceObj=self.wrkston01,
                       interface=self.wrkston01.linkPortMapping['lnk01'],
                       number='1'))

    def test_move_vlan_ports(self):
        LogOutput(
            'info', "\n#################################################")
        LogOutput(
            'info', "Step 8- Move ports from vlan to another")
        LogOutput(
            'info', "#################################################")
        vlans = (5, 6, 7)
        interfaces = (self.dut01Obj.linkPortMapping['lnk01'],
                      self.dut01Obj.linkPortMapping['lnk02'],
                      self.dut01Obj.linkPortMapping['lnk03'])
        assert(portsAssign(self.dut01Obj, interfaces, vlans))

    def test_moved_ports(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 9- Verify ports re-assigned correctly")
        LogOutput('info', "############################################")
        vlans = (5, 6, 7)
        interfaces = (self.dut01Obj.linkPortMapping['lnk01'],
                      self.dut01Obj.linkPortMapping['lnk02'],
                      self.dut01Obj.linkPortMapping['lnk03'])
        assert(verifyPorts(self.dut01Obj, interfaces, vlans))

    def test_delete_firt_vlans(self):
        LogOutput(
            'info', "\n##################################################")
        LogOutput('info', "Step 10- Delete first vlans")
        LogOutput(
            'info', "###################################################")
        vlans = (2, 3, 4)
        assert(configureVlans(self.dut01Obj, vlans, False))

    def test_verifyDeletedVlans(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Step 11- Verify vlans were deleted ")
        LogOutput('info', "############################################")
        vlans = (2, 3, 4)
        assert(verifyVlans(self.dut01Obj, vlans))

    def test_sendTraffic2(self):
        LogOutput(
            'info', "\n#################################################")
        LogOutput(
            'info', "Step 12- Send traffic and verifying is not forwarded")
        LogOutput(
            'info', "#################################################")
        assert(capture(deviceObj=self.wrkston01,
                       interface=self.wrkston01.linkPortMapping['lnk01'],
                       number='1'))

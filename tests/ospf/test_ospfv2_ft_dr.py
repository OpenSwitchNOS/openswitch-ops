#!/usr/bin/python

# (c) Copyright 2016 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
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
import re
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *
from opstestfw.switch.CLI.InterfaceIpConfig import InterfaceIpConfig
from opsvsiutils.vtyshutils import *

dict = {}

'''
TOPOLOGY
+---------------+             +---------------+
|               |   Area1     |               |
| Switch 1     1+-------------+1  Switch 2    +
|               |             |               |
|               |             |               |
+---------------+             +---------------+

Switch 1 Configuration
IP ADDR is 10.10.10.1
Router Id is 1.1.1.1


Switch 2 Configuration
IP ADDR is 10.10.10.2
Router Id is 2.2.2.2

'''

OSPF_DUT_OBJ = 'dut_obj'
OSPF_ROUTER_KEY = 'router_id'
OSPF_IP_ADDR_KEY = 'ip'
OSPF_IP_MASK_KEY = "mask"
OSPF_NETWORK_KEY = "network"
OSPF_LINK_KEY = 'lnk'
OSPF_AREA_KEY = "area"  # Single quotes double quotes all same.

VTYSH_CR = '\r\n'
ADJACENCY_MAX_WAIT_TIME = 100
OSPF_DEAD_TIMER = 40


# Topology definition
topoDict = {"topoExecution": 5000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02",
            "topoLinks": "lnk01:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch"}


def enterConfigShell(dut01):
    retStruct = dut01.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    retStruct = dut01.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    return True


# If the context is not present already then it will be created
def enterRouterContext(dut01):
    if (enterConfigShell(dut01) is False):
        return False

    devIntReturn = dut01.DeviceInteract(command="router ospf")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter OSPF context"

    return True


def delete_router_id(dut, router_id):
    if (enterRouterContext(dut) is False):
        return False

    LogOutput('info', "deleting OSPF router ID " + router_id)
    devIntReturn = dut.DeviceInteract(command="no router-id ")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set router-id failed"

    return True


def enterInterfaceContext(dut01, interface, enable):
    if (enterConfigShell(dut01) is False):
        return False

    cmd = "interface " + str(interface)
    devIntReturn = dut01.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter Interface context"

    if (enable is True):
        dut01.DeviceInteract(command="no shutdown")
        dut01.DeviceInteract(command="no routing")

    return True


def exitContext(dut01):
    devIntReturn = dut01.DeviceInteract(command="exit")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to exit current context"

    retStruct = dut01.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit config terminal"

    retStruct = dut01.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    return True


def deleteRouterInstanceTest(dut01):
    if (enterConfigShell(dut01) is False):
        return False

    devIntReturn = dut01.DeviceInteract(command="no router ospf")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to delete OSPF context failed"

    return True


def configure_router_id(dut, router_id):
    if (enterRouterContext(dut) is False):
        return False

    LogOutput('info', "Configuring OSPF router ID " + router_id)
    devIntReturn = dut.DeviceInteract(command="router-id " + router_id)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set router-id failed"

    return True


def configure_network_area(dut01, network, area):
    if (enterRouterContext(dut01) is False):
        return False

    cmd = "network " + network + " area " + area
    devIntReturn = dut01.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set network area id failed"

    return True


# Test case to verify that the neighbors are discovered
def verify_ospf_adjacency(dut01, dut02_router_id, print_nbrs=False):
        neighbors = SwitchVtyshUtils.vtysh_cmd(dut01, "show ip ospf neighbor")

        if print_nbrs:
            info("%s\n" % neighbors)

        nbrs = neighbors.split(VTYSH_CR)

        for nbr in nbrs:
            if dut02_router_id in nbr:
                return True

        return False


def verify_neighbour(dut02, dut01_router_id, print_nbrs=True):
        neighbors = SwitchVtyshUtils.vtysh_cmd(dut02, "show ip ospf neighbor")

        if print_nbrs:
            info("%s\n" % neighbors)

        nbrs = neighbors.split(VTYSH_CR)

        for nbr in nbrs:
            if dut01_router_id in nbr:
                return False

        return True


def verify_dr_bdr_selection(dut01Obj, state):

    neighbors = SwitchVtyshUtils.vtysh_cmd(dut01Obj, "show ip ospf neighbor")

    nbrs = neighbors.split(VTYSH_CR)

    for nbr in nbrs:
        if state in nbr:
            return True

    return False


def getDeadInterval():
    return OSPF_DEAD_TIMER


def wait_for_dead_timer_expiry(dut02, dut01_router_id, condition=True,
                               print_nbrs=True):

        for i in range(getDeadInterval()):
            not_found = verify_neighbour(dut02, dut01_router_id, print_nbrs)

            if not_found == condition:
                if condition:
                    result = "Adjacency not formed with " + dut01_router_id
                else:
                    result = "Adjacency formed with " + dut01_router_id

                LogOutput('info', result)
                return not_found

        sleep(1)

        info("### Condition not met after %s seconds ###\n" %
             OSPF_DEAD_TIMER)
        return not_found


def wait_for_adjacency(dut01, dut02_router_id, condition=True,
                       print_nbrs=False):
        for i in range(ADJACENCY_MAX_WAIT_TIME):
            found = verify_ospf_adjacency(dut01, dut02_router_id, print_nbrs)

            if found == condition:
                if condition:
                    result = "Adjacency formed with " + dut02_router_id
                else:
                    result = "Adjacency not formed with " + dut02_router_id

                LogOutput('info', result)
                return found

            sleep(1)

        info("### Condition not met after %s seconds ###\n" %
             ADJACENCY_MAX_WAIT_TIME)

        return found


def configure(dict):
    '''
     - Configures the IP address in SW1 and SW2
     - Creates router ospf instances
     - Configures the router id
     - Configures the network range and area
    '''

    # - Enable the link.
    # - Set IP for the switches.
    # Enabling interface

    if "OSPF_DUT_OBJ" in dict:
        switch = dict["OSPF_DUT_OBJ"]
        print switch
    if (not switch):
        assert "No Object to configure"

    if "OSPF_LINK_KEY" in dict:
        link = dict["OSPF_LINK_KEY"]
        LogOutput('info', "Enabling interface1 on %s" % switch)
        interface_value = switch.linkPortMapping[str(link)]
        retStruct = InterfaceEnable(deviceObj=switch,
                                    enable=True,
                                    interface=interface_value)
        retCode = retStruct.returnCode()
        if retCode != 0:
            assert "Unable to enable interface"

    # Assigning an IPv4 address on interface
    if "OSPF_IP_ADDR_KEY" and "OSPF_IP_MASK_KEY" in dict:
        ipAddr = dict["OSPF_IP_ADDR_KEY"]
        ipMask = dict["OSPF_IP_MASK_KEY"]
        interface_value = switch.linkPortMapping[str(link)]
        LogOutput('info', "Configuring IPv4 address on link 1 SW1")
        retStruct = InterfaceIpConfig(deviceObj=switch,
                                      interface=interface_value,
                                      addr=ipAddr, mask=ipMask,
                                      config=True)
        retCode = retStruct.returnCode()
        if retCode != 0:
            assert "Failed to configure an IPv4 address on interface "

    '''
    For all the switches
    - Create the instance.
    - Configure network range and area id.
    - Configure the router Id.
    '''
    if "OSPF_ROUTER_KEY" in dict:
        routerId = dict["OSPF_ROUTER_KEY"]
        result = configure_router_id(switch, routerId)
        assert result is True, "OSPF router id set failed"

    if "OSPF_NETWORK_KEY" and "OSPF_AREA_KEY" in dict:
        network = dict["OSPF_NETWORK_KEY"]
        area = dict["OSPF_AREA_KEY"]
        result = configure_network_area(switch, network, area)
        assert result is True, "OSPF network creation failed"

    exitContext(switch)  # In config context


class Test_ospf_configuration:

    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_ospf_configuration.testObj = testEnviron(topoDict=topoDict)
        #    Get topology object
        Test_ospf_configuration.topoObj = \
            Test_ospf_configuration.testObj.topoObjGet()

    def teardown_class(cls):
        Test_ospf_configuration.topoObj.terminate_nodes()

    # [1.04] - Verifying that the router id configured
    # in router context is selected
    def test_nbr_discovery(self):

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict = {"OSPF_DUT_OBJ": dut01Obj, "OSPF_ROUTER_KEY": "1.1.1.1",
                "OSPF_IP_ADDR_KEY": "10.10.10.1", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.1/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1", }
        configure(dict)

        dict = {}

        dict = {"OSPF_DUT_OBJ": dut02Obj, "OSPF_ROUTER_KEY": "2.2.2.2",
                "OSPF_IP_ADDR_KEY": "10.10.10.2", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.2/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1"}
        configure(dict)

        LogOutput('info', "Wait for adjacency to form")
        wait_for_adjacency(dut01Obj, "2.2.2.2")
        wait_for_adjacency(dut02Obj, "1.1.1.1")

    # [2.02] - Test case to verify that the neighbors are discovered
    def test_nbr_discovery(self):
        print "Test case to verify that the neighbors are discovered"
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict = {"OSPF_DUT_OBJ": dut01Obj, "OSPF_ROUTER_KEY": "1.1.1.1",
                "OSPF_IP_ADDR_KEY": "10.10.10.1", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.1/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1", }
        configure(dict)

        dict = {}

        dict = {"OSPF_DUT_OBJ": dut02Obj, "OSPF_ROUTER_KEY": "2.2.2.2",
                "OSPF_IP_ADDR_KEY": "10.10.10.2", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.2/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1"}
        configure(dict)

        LogOutput('info', "Wait for adjacency to form")
        wait_for_adjacency(dut01Obj, "2.2.2.2")
        wait_for_adjacency(dut02Obj, "1.1.1.1")

    # [2.03]Test case to verify that neighbor information
    # is updated when ospfv2 is disabled in one of the switches
    def test_nbr_ospf_disabled(self):

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict = {"OSPF_DUT_OBJ": dut01Obj, "OSPF_ROUTER_KEY": "1.1.1.1",
                "OSPF_IP_ADDR_KEY": "10.10.10.1", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.1/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1", }
        configure(dict)

        dict = {}

        dict = {"OSPF_DUT_OBJ": dut02Obj, "OSPF_ROUTER_KEY": "2.2.2.2",
                "OSPF_IP_ADDR_KEY": "10.10.10.2", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.2/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1"}
        configure(dict)
        LogOutput('info', "Wait for adjacency to form")
        wait_for_adjacency(dut01Obj, "2.2.2.2")
        wait_for_adjacency(dut02Obj, "1.1.1.1")

        deleteRouterInstanceTest(dut01Obj)
        wait_for_dead_timer_expiry(dut02Obj, "1.1.1.1")

    # [1.05] - Verifying that the dynamic router id is
    #  selected when instance level router id is removed
    def test_remove_global_rtr_id(self):

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict = {"OSPF_DUT_OBJ": dut01Obj, "OSPF_ROUTER_KEY": "1.1.1.1",
                "OSPF_IP_ADDR_KEY": "10.10.10.1", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.1/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1", }
        configure(dict)

        dict = {}

        dict = {"OSPF_DUT_OBJ": dut02Obj, "OSPF_ROUTER_KEY": "2.2.2.2",
                "OSPF_IP_ADDR_KEY": "10.10.10.2", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.2/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1"}
        configure(dict)

        result = delete_router_id(dut01Obj, "1.1.1.1")
        assert result is True, "no OSPF router id set failed"

        wait_for_adjacency(dut02Obj, "10.10.10.1")

    # [1.01] Verifying that the dynamic router id is selected
    def test_dynamic_router_id(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dict = {"OSPF_DUT_OBJ": dut01Obj,
                "OSPF_IP_ADDR_KEY": "10.10.10.1", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.1/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1", }
        configure(dict)
        dict = {}
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict = {"OSPF_DUT_OBJ": dut02Obj,
                "OSPF_IP_ADDR_KEY": "10.10.10.2", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.2/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1"}
        configure(dict)
        wait_for_adjacency(dut01Obj, "10.10.10.2")
        wait_for_adjacency(dut02Obj, "10.10.10.1")

    # [2.04] -Test case to verify that neighbor information
    # is updated when one of the neighbor goes down
    def test_neighbor_down(self):

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")

        dict = {"OSPF_DUT_OBJ": dut01Obj, "OSPF_ROUTER_KEY": "1.1.1.1",
                "OSPF_IP_ADDR_KEY": "10.10.10.1", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.1/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1", }
        OSPF_ROUTER_ID_DUT1 = dict["OSPF_ROUTER_KEY"]

        configure(dict)

        dict = {}

        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict = {"OSPF_DUT_OBJ": dut02Obj, "OSPF_ROUTER_KEY": "2.2.2.2",
                "OSPF_IP_ADDR_KEY": "10.10.10.2", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.2/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1"}
        OSPF_ROUTER_ID_DUT2 = dict["OSPF_ROUTER_KEY"]
        configure(dict)

        wait_for_adjacency(dut01Obj, "2.2.2.2")
        wait_for_adjacency(dut02Obj, "1.1.1.1")

        LogOutput('info', "Disable interface1 on %s" % switch)
        interface_value = dut02Obj.linkPortMapping["lnk01"]
        retStruct = InterfaceEnable(deviceObj=dut02Obj, enable=False,
                                    interface=interface_value)
        retCode = retStruct.returnCode()
        if retCode != 0:
            assert "Unable to disable interface"

        wait_for_dead_timer_expiry(dut02Obj, "1.1.1.1")

    # [3.01] :Test case to verify that the DR and BDR is selected
    def test_dr_bdr_selection(self):

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")

        dict = {"OSPF_DUT_OBJ": dut01Obj, "OSPF_ROUTER_KEY": "1.1.1.1",
                "OSPF_IP_ADDR_KEY": "10.10.10.1", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.1/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1", }
        OSPF_ROUTER_ID_DUT1 = dict["OSPF_ROUTER_KEY"]

        configure(dict)

        dict = {}

        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict = {"OSPF_DUT_OBJ": dut02Obj, "OSPF_ROUTER_KEY": "2.2.2.2",
                "OSPF_IP_ADDR_KEY": "10.10.10.2", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.2/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1"}
        OSPF_ROUTER_ID_DUT2 = dict["OSPF_ROUTER_KEY"]
        configure(dict)

        LogOutput('info', "Wait for adjacency to form")
        wait_for_adjacency(dut01Obj, "2.2.2.2")
        wait_for_adjacency(dut02Obj, "1.1.1.1")

        verify_dr_bdr_selection(dut01Obj, "Full/DR")
        verify_dr_bdr_selection(dut01Obj, "Full/Backup")

    # [3.04] :Test case to verify that the DR election is
    # triggered when router ids are changed.
    def test_dr_bdr_election(self):

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")

        dict = {"OSPF_DUT_OBJ": dut01Obj, "OSPF_ROUTER_KEY": "1.1.1.1",
                "OSPF_IP_ADDR_KEY": "10.10.10.1", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.1/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1", }
        OSPF_ROUTER_ID_DUT1 = dict["OSPF_ROUTER_KEY"]

        configure(dict)

        dict = {}

        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict = {"OSPF_DUT_OBJ": dut02Obj, "OSPF_ROUTER_KEY": "2.2.2.2",
                "OSPF_IP_ADDR_KEY": "10.10.10.2", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.2/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1"}
        OSPF_ROUTER_ID_DUT2 = dict["OSPF_ROUTER_KEY"]
        configure(dict)

        LogOutput('info', "Wait for adjacency to form")
        wait_for_adjacency(dut01Obj, "2.2.2.2")
        wait_for_adjacency(dut02Obj, "1.1.1.1")

        verify_dr_bdr_selection(dut01Obj, "Full/DR")
        verify_dr_bdr_selection(dut01Obj, "Full/Backup")
        dict = {"OSPF_DUT_OBJ": dut01Obj, "OSPF_ROUTER_KEY": "5.5.5.5",
                "OSPF_IP_ADDR_KEY": "10.10.10.1", "OSPF_IP_MASK_KEY": "24",
                "OSPF_NETWORK_KEY": "10.10.10.1/24", "OSPF_LINK_KEY": "lnk01",
                "OSPF_AREA_KEY": "1", }
        OSPF_ROUTER_ID_DUT1 = dict["OSPF_ROUTER_KEY"]

        configure(dict)

        dict = {}

        wait_for_adjacency(dut01Obj, "2.2.2.2")
        wait_for_adjacency(dut02Obj,  "5.5.5.5")

        verify_dr_bdr_selection(dut01Obj, "Full/DR")
        verify_dr_bdr_selection(dut01Obj, "Full/Backup")

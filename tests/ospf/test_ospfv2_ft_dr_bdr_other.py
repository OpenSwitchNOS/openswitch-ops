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


from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *
from opstestfw.switch.CLI.InterfaceIpConfig import InterfaceIpConfig
from opsvsiutils.vtyshutils import *

dict = {}

'''
TOPOLOGY 1
        (L2 Switch)
      _____dut04_______
     |       |         |
   dut01   dut02    dut03
'''

OSPF_DUT_OBJ = 'dut_obj'
OSPF_ROUTER_KEY = 'router_id'
OSPF_IP_ADDR_KEY = 'ip'
OSPF_IP_MASK_KEY = "mask"
OSPF_NETWORK_KEY = "network"
OSPF_LINK_KEY = 'lnk'
OSPF_AREA_KEY = "area"


VTYSH_CR = '\r\n'

topoDict = {"topoExecution": 5000,
            "topoTarget": "dut01 dut02 dut03 dut04",
            "topoDevices": "dut01 dut02 dut03 dut04",
            "topoLinks": "lnk01:dut01:dut04, lnk01:dut02:dut04,\
                          lnk01:dut03:dut04",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch,\
                            dut04:system-category:switch"}


dict01 = {OSPF_ROUTER_KEY: "1.1.1.1",
          OSPF_IP_ADDR_KEY: "10.10.10.1", OSPF_IP_MASK_KEY: "24",
          OSPF_NETWORK_KEY: "10.10.10.1/24", OSPF_LINK_KEY: "lnk01",
          OSPF_AREA_KEY: "0", }


dict02 = {OSPF_ROUTER_KEY: "2.2.2.2",
          OSPF_IP_ADDR_KEY: "10.10.10.2", OSPF_IP_MASK_KEY: "24",
          OSPF_NETWORK_KEY: "10.10.10.2/24", OSPF_LINK_KEY: "lnk01",
          OSPF_AREA_KEY: "0", }

dict03 = {OSPF_ROUTER_KEY: "3.3.3.3",
          OSPF_IP_ADDR_KEY: "10.10.10.3", OSPF_IP_MASK_KEY: "24",
          OSPF_NETWORK_KEY: "10.10.10.3/24", OSPF_LINK_KEY: "lnk01",
          OSPF_AREA_KEY: "0", }


# Function to enter into config mode
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


# Function to delete router id
def delete_router_id(dut, router_id):
    if (enterRouterContext(dut) is False):
        return False

    LogOutput('info', "deleting OSPF router ID " + router_id)
    devIntReturn = dut.DeviceInteract(command="no router-id ")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set router-id failed"

    return True


# Function to enter into interface context
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


# Function to exit from context
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


# Function to delete router instance
def deleteRouterInstanceTest(dut01):
    if (enterConfigShell(dut01) is False):
        return False

    devIntReturn = dut01.DeviceInteract(command="no router ospf")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to delete OSPF context failed"

    return True


# Function to configure router id
def configure_router_id(dut, router_id):
    if (enterRouterContext(dut) is False):
        return False

    LogOutput('info', "Configuring OSPF router ID " + router_id)
    devIntReturn = dut.DeviceInteract(command="router-id " + router_id)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set router-id failed"

    return True


# Function to configure network area for OSPF
def configure_network_area(dut01, network, area):
    if (enterRouterContext(dut01) is False):
        return False

    cmd = "network " + network + " area " + area
    devIntReturn = dut01.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set network area id failed"

    return True


# Function to get ospf states
def verify_ospf_states(dut02):
    LogOutput('info', "fetching states of the router")
    ospf_interface = SwitchVtyshUtils.vtysh_cmd(dut02, "show ip\
                                                ospf interface")
    matchObj = re.search(r'State\s<.*>', ospf_interface)
    split_list = re.split(r'\s+', matchObj.group())
    if "Backup>" in split_list:
        return "DRBackup"
    elif "Other>" in split_list:
        return "DROther"
    elif "<DR>" in split_list:
        return "DR"


# Test case to verify that the neighbors are discovered
def verify_ospf_adjacency(dut01, dut02_router_id, print_nbrs=False):
    neighbors = SwitchVtyshUtils.vtysh_cmd(dut01, "show ip ospf neighbor")

    if print_nbrs:
        info("%s\n" % neighbors)

    nbrs = neighbors.split(VTYSH_CR)
    nbr_id = dut02_router_id + " "
    for nbr in nbrs:
        if nbr_id in nbr:
            return True

    return False


# Function to get the dead interval and hello timer value
def getTimers(dut02, timer_type):
    ospf_interface = SwitchVtyshUtils.vtysh_cmd(dut02, "show\
                                                        ip ospf interface")

    if "Dead" in timer_type:
        matchObj = re.search(r'Dead\s\d+', ospf_interface)
    elif "Hello" in timer_type:
        matchObj = re.search(r'Hello\s\d+', ospf_interface)

    timers = re.split(r'\s+', matchObj.group())
    timer = timers[1]
    return timer


# Function to wait for adjacency establishment
def wait_for_adjacency(dut01, dut02_router_id, condition=True,
                       print_nbrs=False):
    hello_time = getTimers(dut01, "Hello")
    wait_time = int(hello_time) + 30
    for i in range(wait_time):
        found = verify_ospf_adjacency(dut01, dut02_router_id, print_nbrs)
        if found == condition:
            result = "Adjacency formed with " + dut02_router_id
            LogOutput('info', result)
            return found

        sleep(1)

    info("### Condition not met after %s seconds ###\n" %
         wait_time)

    return found


# Function to configure OSPF
def configure(dict):

    # - Configures the IP address
    # - Creates router ospf instances
    # - Configures the router id
    # - Configures the network range and area

    # - Enable the link.
    # - Set IP for the switches.
    # Enabling interface

    if OSPF_DUT_OBJ in dict:
        switch = dict[OSPF_DUT_OBJ]
    if (not switch):
        assert "No Object to configure"

    if OSPF_LINK_KEY in dict:
        link = dict[OSPF_LINK_KEY]
        info_str = "Enabling " + link + " on " + str(switch)
        LogOutput('info', info_str)
        interface_value = switch.linkPortMapping[str(link)]
        retStruct = InterfaceEnable(deviceObj=switch,
                                    enable=True,
                                    interface=interface_value)
        retCode = retStruct.returnCode()
        if retCode != 0:
            assert_msg = "Unable to enable " + interface_value
            " on " + str(switch)
            assert assert_msg

        # Assigning an IPv4 address on interface
        if OSPF_IP_ADDR_KEY and OSPF_IP_MASK_KEY in dict:
            ipAddr = dict[OSPF_IP_ADDR_KEY]
            ipMask = dict[OSPF_IP_MASK_KEY]
            interface_value = switch.linkPortMapping[str(link)]
            info_str = str(link) + " of " + str(switch)
            LogOutput('info', "Configuring ip adddress on " + info_str)
            retStruct = InterfaceIpConfig(deviceObj=switch,
                                          interface=interface_value,
                                          addr=ipAddr, mask=ipMask,
                                          config=True)
            retCode = retStruct.returnCode()
            if retCode != 0:
                assert "Failed to configure an IPv4 address on interface "

    if (not link):
        return

    # For all the switches
    # - Create the instance.
    # - Configure the router Id.
    # - Configure network area.

    if OSPF_ROUTER_KEY in dict:
        routerId = dict[OSPF_ROUTER_KEY]
        result = configure_router_id(switch, routerId)
        assert result is True, "OSPF router id set failed"

    if OSPF_NETWORK_KEY and OSPF_AREA_KEY in dict:
        network = dict[OSPF_NETWORK_KEY]
        area = dict[OSPF_AREA_KEY]
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

    def test_dr_bdr_selection(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        dut04Obj = self.topoObj.deviceObjGet(device="dut04")
        dict01[OSPF_DUT_OBJ] = dut01Obj
        dict02[OSPF_DUT_OBJ] = dut02Obj
        dict03[OSPF_DUT_OBJ] = dut03Obj
        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        configure(dict01)

        OSPF_ROUTER_ID_DUT2 = dict02[OSPF_ROUTER_KEY]
        configure(dict02)

        OSPF_ROUTER_ID_DUT3 = dict03[OSPF_ROUTER_KEY]
        configure(dict03)

        enterInterfaceContext(dut04Obj, 1, True)
        enterInterfaceContext(dut04Obj, 2, True)
        enterInterfaceContext(dut04Obj, 3, True)
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2, True, True)
        assert retVal is True, "OSPF adjacency not formed"
        sleep(30)
        state = verify_ospf_states(dut01Obj)
        if (state == "DRBackup"):
            LogOutput('info', "Switch in DRBackup state")
        else:
            LogOutput('info', "Switch not in correct state")

        state = verify_ospf_states(dut02Obj)
        if (state == "DR"):
            LogOutput('info', "Switch in DR  state")
        else:
            LogOutput('info', "Switch not in correct state")

        state = verify_ospf_states(dut03Obj)
        if (state == "DROther"):
            LogOutput('info', "Switch in DROther state")
        else:
            LogOutput('info', "Switch not in correct state")

        #changing router-id of dut01 to verify DR/BRR/DROther election
        #Right now states are not updated as per RFC
        dict01[OSPF_ROUTER_KEY] = "5.5.5.5"
        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        configure(dict01)
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2, True, True)
        assert retVal is True, "OSPF adjacency not formed"

        state = verify_ospf_states(dut01Obj)
        if (state == "DR"):
            LogOutput('info', "Switch in DR state")
        else:
            LogOutput('info', "Switch not in correct state")

        state = verify_ospf_states(dut02Obj)
        if (state == "DROther"):
            LogOutput('info', "Switch in DROther state")
        else:
            LogOutput('info', "Switch not in correct state")

        state = verify_ospf_states(dut03Obj)
        if (state == "DRBackup"):
            LogOutput('info', "Switch in DRBackup  state")
        else:
            LogOutput('info', "Switch not in correct state")

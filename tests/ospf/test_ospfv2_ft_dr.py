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
OSPF_AREA_KEY = "area"


VTYSH_CR = '\r\n'
ADJACENCY_MAX_WAIT_TIME = 100
OSPF_DEAD_TIMER = 40


# Topology definition
topoDict = {"topoExecution": 5000,
            "topoTarget": "dut01 dut02 dut03",
            "topoDevices": "dut01 dut02 dut03",
            "topoLinks": "lnk01:dut01:dut02, lnk02:dut02:dut03",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch"}

dict01 = {OSPF_ROUTER_KEY: "1.1.1.1",
          OSPF_IP_ADDR_KEY: "10.10.10.1", OSPF_IP_MASK_KEY: "24",
          OSPF_NETWORK_KEY: "10.10.10.1/24", OSPF_LINK_KEY: "lnk01",
          OSPF_AREA_KEY: "1", }


dict02 = {OSPF_ROUTER_KEY: "2.2.2.2",
          OSPF_IP_ADDR_KEY: "10.10.10.2", OSPF_IP_MASK_KEY: "24",
          OSPF_NETWORK_KEY: "10.10.10.2/24", OSPF_LINK_KEY: "lnk01",
          OSPF_AREA_KEY: "1", }

dict03 = {OSPF_ROUTER_KEY: "3.3.3.3",
          OSPF_IP_ADDR_KEY: "10.10.10.3", OSPF_IP_MASK_KEY: "24",
          OSPF_NETWORK_KEY: "10.10.10.3/24", OSPF_LINK_KEY: "lnk01",
          OSPF_AREA_KEY: "1", }


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


def getTcpdump(switch_id):
    LogOutput('info', "Capturing packets through tcpdump")

    devIntReturn = switch_id.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter the bash shell"

    devIntReturn = switch_id.DeviceInteract(command="ip netns exec swns bash")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to execute command"

    fo = open("tcpdump.txt", "wb+")

    devIntReturn = switch_id.DeviceInteract(command="timeout 50 tcpdump -i2\
                                            -v -XX ip proto 89")
    assert retCode == 0, "Failed to get tcpdump"
    fo.write(devIntReturn['buffer'])

    fo.seek(0, 0)
    str = fo.read()
    fo.close()
    return str


# Function to fetch neighbor-id from tcpdump
def get_nbor_id_frm_dump(switch_id):
    str = getTcpdump(switch_id)
    regex = r'10.10.10.2 >.*Neighbor List:.*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    matchObj = re.search(regex, str, re.S)
    split_list = re.split(r'\s+', matchObj.group())
    index = split_list.index("List:")
    return split_list[index+1]


# Function to count number of router-id instance
def get_packet_count(switch_id):
    str = getTcpdump(switch_id)
    reg_ex = r'switch\s>.*Router-ID\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    matchObj = re.search(reg_ex, str, re.S)
    split_list = re.split(r'\s+', matchObj.group())
    count = split_list.count("Router-ID")
    return count


# Function to get Router-id of switch
def get_router_id(switch_id):
    LogOutput('info', "fetching router-id from show ip ospf")
    ospf_interface = SwitchVtyshUtils.vtysh_cmd(switch_id, "show ip ospf")
    matchObj = re.search(r'Router\sID:\s\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
                         ospf_interface)
    split_list = re.split(r'\s+', matchObj.group())
    router_id = split_list[2]
    return router_id


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

    # [1.01] Verifying that the dynamic router id is selected
    def test_dynamic_router_id(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dict = {OSPF_DUT_OBJ: dut01Obj,
                OSPF_IP_ADDR_KEY: "10.10.10.1", OSPF_IP_MASK_KEY: "24",
                OSPF_NETWORK_KEY: "10.10.10.1/24", OSPF_LINK_KEY: "lnk01",
                OSPF_AREA_KEY: "1", }
        configure(dict)
        OSPF_ROUTER_ID_DUT1 = "10.10.10.1"
        OSPF_ROUTER_ID_DUT2 = "10.10.10.2"
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict = {OSPF_DUT_OBJ: dut02Obj,
                OSPF_IP_ADDR_KEY: "10.10.10.2", OSPF_IP_MASK_KEY: "24",
                OSPF_NETWORK_KEY: "10.10.10.2/24", OSPF_LINK_KEY: "lnk01",
                OSPF_AREA_KEY: "1"}
        configure(dict)
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2)
        assert retVal is True, "OSPF adjacency not formed"
        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1)
        assert retVal is True, "OSPF adjacency not formed"
        router_id = get_router_id(dut01Obj)
        if OSPF_ROUTER_ID_DUT1 in router_id:
            LogOutput('info', "Router-id is verfied for switch")
        else:
            LogOutput('info', "Dynamic Router-id selection failed")

    # [1.04] - Verifying that the router id configured
    # in router context is selected
    def test_verify_router_id(self):

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict01[OSPF_DUT_OBJ] = dut01Obj
        dict02[OSPF_DUT_OBJ] = dut02Obj

        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        configure(dict01)

        OSPF_ROUTER_ID_DUT2 = dict02[OSPF_ROUTER_KEY]
        configure(dict02)

        LogOutput('info', "Wait for adjacency to form")
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2)
        assert retVal is True, "OSPF adjacency not formed"
        retval = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1)
        assert retVal is True, "OSPF adjacency not formed"
        router_id = get_router_id(dut01Obj)
        if OSPF_ROUTER_ID_DUT1 in router_id:
            LogOutput('info', "Router-id is verfied for switch")
        else:
            LogOutput('info', "Router-id verification failed")

    # [2.01] - Test case to verify that the
    #  hello packets are exchanged periodically
    def test_verify_hello_packets(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict01[OSPF_DUT_OBJ] = dut01Obj
        dict02[OSPF_DUT_OBJ] = dut02Obj

        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        configure(dict01)

        OSPF_ROUTER_ID_DUT2 = dict02[OSPF_ROUTER_KEY]
        configure(dict02)

        LogOutput('info', "Wait for adjacency to form")
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2, True, True)
        assert retVal is True, "OSPF adjacency not formed"
        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1, True, True)
        assert retVal is True, "OSPF adjacency not formed"

        neighbor_id = get_nbor_id_frm_dump(dut01Obj)
        if (neighbor_id == OSPF_ROUTER_ID_DUT1):
            LogOutput('info', "Router-id found in hello packet")
        else:
            LogOutput('info', "Router-id not seen in hello packet")

        count = get_packet_count(dut01Obj)
        if (count > 4):
            LogOutput('info', "Hello packets exchanged periodically")
        else:
            LogOutput('info', "Hello packets are not exchanged")

    # [2.02] - Test case to verify that the neighbors are discovered
    # When pkt capture is in place we have to check the router id in the packet
    # configuring area id as ipv4 address
    def test_nbr_discovery(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict01[OSPF_DUT_OBJ] = dut01Obj
        dict02[OSPF_DUT_OBJ] = dut02Obj

        dict01[OSPF_AREA_KEY] = "1.2.3.4"
        configure(dict01)

        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]

        dict02[OSPF_AREA_KEY] = "1.2.3.4"
        configure(dict02)

        OSPF_ROUTER_ID_DUT2 = dict02[OSPF_ROUTER_KEY]

        LogOutput('info', "Wait for adjacency to form")
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2, True, True)
        assert retVal is True, "OSPF adjacency not formed"
        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1, True, True)
        assert retVal is True, "OSPF adjacency not formed"

        sleep(30)
        state = verify_ospf_states(dut01Obj)
        if (state == "DRBackup"):
            LogOutput('info', "Switch in DR state")
        else:
            LogOutput('info', "Switch not in correct state")

        state = verify_ospf_states(dut02Obj)
        if (state == "DR"):
            LogOutput('info', "Switch in DRBackup state")
        else:
            LogOutput('info', "Switch not in correct state")

        neighbor_id = get_nbor_id_frm_dump(dut01Obj)
        if (neighbor_id == OSPF_ROUTER_ID_DUT1):
            LogOutput('info', "Router-id found in neighbor list")
        else:
            LogOutput('info', "Router-id not found in neighbor list")

    # [2.03]Test case to verify that neighbor information
    # is updated when ospfv2 is disabled in one of the switches
    def test_nbr_ospf_disabled(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict01[OSPF_DUT_OBJ] = dut01Obj
        dict02[OSPF_DUT_OBJ] = dut02Obj

        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        configure(dict01)

        OSPF_ROUTER_ID_DUT2 = dict02[OSPF_ROUTER_KEY]
        configure(dict02)
        LogOutput('info', "Wait for adjacency to form")
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2)
        assert retVal is True, "OSPF adjacency not  formed"
        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1)
        assert retVal is True, "OSPF adjacency not formed"

        deleteRouterInstanceTest(dut01Obj)
        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT2, False)
        assert retVal is False, "Failed to torn OSPF adjacency"

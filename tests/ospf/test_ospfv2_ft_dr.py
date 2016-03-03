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
+------+             +------+             +---------+             +--------+
|      |   Area1     |      |   Area1     |         |   Area1     |        |
| SW1 1+------------+1 SW2 2+-------------+1  SW3  2+-------------+1  SW4  +
|      |             |      |             |         |             |        |
|      |             |      |             |         |             |        |
+------+             +------+             +---------+             +--------+

Switch 1 Configuration
IP ADDR is 10.10.10.1
Router Id is 1.1.1.1


Switch 2 Configuration
interface 1
IP ADDR is 10.10.10.2
Router Id is 2.2.2.2
interface 2
IP ADDR is 20.10.10.1


Switch 3 Configuration
IP ADDR is 20.10.10.2
Router Id is 3.3.3.3
interface 2
IP ADDR is 30.10.10.1

Switch 4 Configuration
IP ADDR is 30.10.10.2
Router Id is 4.4.4.4

TOPOLOGY 2
        (L2 Switch)
      _____dut04_______
     |       |         |
   dut01   dut02    dut03


Switch 1 Configuration
IP ADDR is 10.10.10.1
Router Id is 1.1.1.1


Switch 2 Configuration
IP ADDR is 10.10.10.2
Router Id is 2.2.2.2


Switch 3 Configuration
IP ADDR is 10.10.10.3
Router Id is 3.3.3.3

'''

OSPF_DUT_OBJ = 'dut_obj'
OSPF_ROUTER_KEY = 'router_id'
OSPF_IP_ADDR_KEY = 'ip'
OSPF_IP_MASK_KEY = "mask"
OSPF_NETWORK_KEY = "network"
OSPF_LINK_KEY = 'lnk'
OSPF_AREA_KEY = "area"

VTYSH_CR = '\r\n'
OSPF_DEAD_TIMER = 40


# Topology definition
# Topology 1
topoDict = {"topoExecution": 5000,
            "topoType": "virtual",
            "topoTarget": "dut01 dut02 dut03 dut04",
            "topoDevices": "dut01 dut02 dut03 dut04",
            "topoLinks": "lnk01:dut01:dut02, lnk02:dut02:dut03,\
                          lnk03:dut03:dut04",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch,\
                            dut04:system-category:switch"}

# Topology 2
topoDict1 = {"topoExecution": 5001,
             "topoType": "virtual",
             "topoTarget": "dut01 dut02 dut03 dut04",
             "topoDevices": "dut01 dut02 dut03 dut04",
             "topoLinks": "lnk01:dut01:dut04, lnk01:dut02:dut04,\
                          lnk01:dut03:dut04",
             "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch,\
                            dut04:system-category:switch"}

# Topology 1 configs
dict01 = {OSPF_ROUTER_KEY: "1.1.1.1",
          OSPF_IP_ADDR_KEY: "10.10.10.1", OSPF_IP_MASK_KEY: "24",
          OSPF_NETWORK_KEY: "10.10.10.1/24", OSPF_LINK_KEY: "lnk01",
          OSPF_AREA_KEY: "1", }


dict02 = {OSPF_ROUTER_KEY: "2.2.2.2",
          OSPF_IP_ADDR_KEY: "10.10.10.2", OSPF_IP_MASK_KEY: "24",
          OSPF_NETWORK_KEY: "10.10.10.2/24", OSPF_LINK_KEY: "lnk01",
          OSPF_AREA_KEY: "1", }

dict02_2 = {OSPF_IP_ADDR_KEY: "20.10.10.1", OSPF_IP_MASK_KEY: "24",
            OSPF_NETWORK_KEY: "20.10.10.1/24", OSPF_LINK_KEY: "lnk02",
            OSPF_AREA_KEY: "1", }

dict03 = {OSPF_ROUTER_KEY: "3.3.3.3",
          OSPF_IP_ADDR_KEY: "20.10.10.2", OSPF_IP_MASK_KEY: "24",
          OSPF_NETWORK_KEY: "20.10.10.2/24", OSPF_LINK_KEY: "lnk02",
          OSPF_AREA_KEY: "1", }

dict03_2 = {OSPF_IP_ADDR_KEY: "30.10.10.1", OSPF_IP_MASK_KEY: "24",
            OSPF_NETWORK_KEY: "30.10.10.1/24", OSPF_LINK_KEY: "lnk03",
            OSPF_AREA_KEY: "1", }

dict04 = {OSPF_ROUTER_KEY: "4.4.4.4",
          OSPF_IP_ADDR_KEY: "30.10.10.2", OSPF_IP_MASK_KEY: "24",
          OSPF_NETWORK_KEY: "30.10.10.2/24", OSPF_LINK_KEY: "lnk03",
          OSPF_AREA_KEY: "1", }

# Topology 2 configs
dict1_01 = {OSPF_ROUTER_KEY: "1.1.1.1",
            OSPF_IP_ADDR_KEY: "10.10.10.1", OSPF_IP_MASK_KEY: "24",
            OSPF_NETWORK_KEY: "10.10.10.1/24", OSPF_LINK_KEY: "lnk01",
            OSPF_AREA_KEY: "0", }


dict1_02 = {OSPF_ROUTER_KEY: "2.2.2.2",
            OSPF_IP_ADDR_KEY: "10.10.10.2", OSPF_IP_MASK_KEY: "24",
            OSPF_NETWORK_KEY: "10.10.10.2/24", OSPF_LINK_KEY: "lnk01",
            OSPF_AREA_KEY: "0", }

dict1_03 = {OSPF_ROUTER_KEY: "3.3.3.3",
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
    exitContext(dut)

    return True


# Function to configure network area for OSPF
def configure_network_area(dut01, network, area):
    if (enterRouterContext(dut01) is False):
        return False

    cmd = "network " + network + " area " + area
    devIntReturn = dut01.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set network area id failed"
    exitContext(dut01)

    return True


def getTcpdump(switch_id):
    LogOutput('info', "Capturing packets through tcpdump")

    devIntReturn = switch_id.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter the bash shell"

    devIntReturn = switch_id.DeviceInteract(command="ip netns exec swns bash")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to execute command"

    devIntReturn = switch_id.DeviceInteract(command="timeout 50 tcpdump -i2\
                                            -v -XX ip proto 89")
    assert retCode == 0, "Failed to get tcpdump"
    return devIntReturn['buffer']


# Function will return neighbor list from tcpdump
def get_nbor_id_frm_dump(switch_id, ip, dump_str):
    regex = ip + r' >.*Neighbor List:.*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    matchObj = re.search(regex, dump_str, re.S)
    if matchObj:
        split_list = re.split(r'\s+', matchObj.group())
        index = split_list.index("List:")
        return split_list[index+1]
    else:
        return False


# Function to count number of router-id instance
def get_packet_count(switch_id, dump_str):
    reg_ex = r'switch\s>.*Router-ID\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    matchObj = re.search(reg_ex, dump_str, re.S)
    if matchObj:
        split_list = re.split(r'\s+', matchObj.group())
        count = split_list.count("Router-ID")
    else:
        count = 0

    return count


# Function to get Router-id of switch
def get_router_id(switch_id):
    LogOutput('info', "fetching router-id from show ip ospf")
    ospf_interface = SwitchVtyshUtils.vtysh_cmd(switch_id, "show ip ospf")
    matchObj = re.search(r'Router\sID:\s\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
                         ospf_interface)
    if matchObj:
        split_list = re.split(r'\s+', matchObj.group())
        router_id = split_list[2]
        return router_id

    return False


# Function to get ospf states
def verify_ospf_states(dut):
    LogOutput('info', "fetching states of the router")
    retVal = wait_for_2way_state(dut)
    if retVal:
        ospf_interface = SwitchVtyshUtils.vtysh_cmd(dut, "show ip\
                                                    ospf interface")
        matchObj = re.search(r'State\s<.*>', ospf_interface)
        if matchObj:
            split_list = re.split(r'\s+', matchObj.group())
            if "Backup>" in split_list:
                return "DRBackup"
            elif "Other>" in split_list:
                return "DROther"
            elif "<DR>" in split_list:
                return "DR"

    return False


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

    if matchObj:
        timers = re.split(r'\s+', matchObj.group())
        timer = timers[1]
    else:
        timer = 0

    return timer


# Function to wait until 2-Way or greater state
def wait_for_2way_state(dut):

    hello_time = getTimers(dut, "Hello")
    wait_time = int(hello_time) + 10
    for i in range(wait_time):
        down_state = verify_ospf_adjacency(dut, "Down")
        init_state = verify_ospf_adjacency(dut, "Init")
        if (down_state or init_state):
            sleep(1)
        else:
            return True

    info("### Condition not met after %s seconds ###\n" %
         wait_time)
    return False


# Function to wait for adjacency establishment
def wait_for_adjacency(dut01, dut02_router_id, condition=True,
                       print_nbrs=False):
    hello_time = getTimers(dut01, "Hello")
    wait_time = int(hello_time) + 30
    for i in range(wait_time):
        found = verify_ospf_adjacency(dut01, dut02_router_id, print_nbrs)
        if found == condition:
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
        info_str = "configuring network " + network + " for area " + area
        LogOutput('info', info_str)
        result = configure_network_area(switch, network, area)
        assert result is True, "OSPF network creation failed"


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
        LogOutput('info', "******[1.01] Verifying that dynamic router "
                  "ID is selected*****")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")

        dict = {OSPF_DUT_OBJ: dut01Obj,
                OSPF_IP_ADDR_KEY: "10.10.10.1", OSPF_IP_MASK_KEY: "24",
                OSPF_NETWORK_KEY: "10.10.10.1/24", OSPF_LINK_KEY: "lnk01",
                OSPF_AREA_KEY: "1", }

        LogOutput('info', "The global router ID is not configured")
        LogOutput('info', "The router ID is not configured in router"
                  " ospf context")
        LogOutput('info', "Step 1 - Configure switch1 and switch2")

        configure(dict)
        OSPF_ROUTER_ID_DUT1 = "10.10.10.1"
        OSPF_ROUTER_ID_DUT2 = "10.10.10.2"
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict = {OSPF_DUT_OBJ: dut02Obj,
                OSPF_IP_ADDR_KEY: "10.10.10.2", OSPF_IP_MASK_KEY: "24",
                OSPF_NETWORK_KEY: "10.10.10.2/24", OSPF_LINK_KEY: "lnk01",
                OSPF_AREA_KEY: "1"}
        configure(dict)

        LogOutput('info', "Step 2 - Waiting for adjacency")
        LogOutput('info', "Step 3 - Verifying Router ID using show ip ospf"
                  " neighbor command")

        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1)
        if retVal:
            LogOutput('info', "Adjacency formed in SW2 with SW1 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT1)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT1

        LogOutput('info', "Step 4 - verify hello packets are exchanged")
        dump_str = getTcpdump(dut01Obj)
        count = get_packet_count(dut01Obj, dump_str)
        if (count > 1):
            LogOutput('info', "Hello packets exchanged periodically")
        else:
            LogOutput('info', "Hello packets are not exchanged")
            assert False, "Failed to exchange hello packets"

        LogOutput('info', "******[1.01] Passed *****")

    # [1.04] - Verifying that the router id configured
    # in router context is selected
    def test_router_id_in_router_context_selected(self):
        LogOutput('info', "*****[1.04] Verifying that the router id configured"
                  "in router context is selected******")

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dict_01 = {OSPF_DUT_OBJ: dut01Obj, OSPF_ROUTER_KEY: "1.1.1.1", }
        dict_02 = {OSPF_DUT_OBJ: dut02Obj, OSPF_ROUTER_KEY: "2.2.2.2", }

        LogOutput('info', "Step 1 - Configure switch1,switch2 and switch3")
        OSPF_ROUTER_ID_DUT1 = dict_01[OSPF_ROUTER_KEY]
        configure(dict_01)

        OSPF_ROUTER_ID_DUT2 = dict_02[OSPF_ROUTER_KEY]
        configure(dict_02)

        LogOutput('info', "Step 2 - Waiting for adjacency")
        LogOutput('info', "Step 3 - Verify Router ID using show ip ospf "
                  "neighbor command")
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        retval = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW2 with SW1 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT1)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT1

        LogOutput('info', "Step 4 - verify router ID"
                  " using show ip ospf command")
        router_id = get_router_id(dut01Obj)
        if OSPF_ROUTER_ID_DUT1 in router_id:
            LogOutput('info', "Router-id is verfied for switch")
        else:
            LogOutput('info', "Router-id verification failed")
            assert "Router-id verification failed"

        dump_str = getTcpdump(dut01Obj)
        neighbor_id = get_nbor_id_frm_dump(dut01Obj,
                                           str(dict02[OSPF_IP_ADDR_KEY]),
                                           dump_str)
        if (neighbor_id == OSPF_ROUTER_ID_DUT1):
            LogOutput('info', "Router-id found in hello packet")
        else:
            LogOutput('info', "Router-id not seen in hello packet")
            assert "Router-id not seen in hello packet"

        LogOutput('info', "******[1.04] Passed ******")

    # [2.01] - Test case to verify that the
    #  hello packets are exchanged periodically
    def test_verify_hello_packets_exchanged(self):
        LogOutput('info', "*****[2.01] Verifying that the hello packets are "
                  "exchanged periodically ******")

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        dut04Obj = self.topoObj.deviceObjGet(device="dut04")
        dict02_2[OSPF_DUT_OBJ] = dut02Obj
        dict03[OSPF_DUT_OBJ] = dut03Obj
        dict03_2[OSPF_DUT_OBJ] = dut03Obj
        dict04[OSPF_DUT_OBJ] = dut04Obj

        LogOutput('info', "Step 1 - Configure switch1, switch2, switch3"
                  " and switch4")

        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT2 = dict02[OSPF_ROUTER_KEY]
        configure(dict02_2)

        OSPF_ROUTER_ID_DUT3 = dict03[OSPF_ROUTER_KEY]
        configure(dict03)
        configure(dict03_2)

        OSPF_ROUTER_ID_DUT4 = dict04[OSPF_ROUTER_KEY]
        configure(dict04)

        LogOutput('info', "Step 2 - Waiting for adjacency")
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW2 with SW1 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT1)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT1

        retVal = wait_for_adjacency(dut03Obj, OSPF_ROUTER_ID_DUT2, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        retVal = wait_for_adjacency(dut04Obj, OSPF_ROUTER_ID_DUT3, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW4 with SW3 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT3)
        else:
            assert False, "Adjacency not formed in SW4 with SW3(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT3

        LogOutput('info', "Step 3 - verify count of hello packets")
        dump_str = getTcpdump(dut01Obj)
        count = get_packet_count(dut01Obj, dump_str)
        if (count > 1):
            LogOutput('info', "Hello packets exchanged periodically")
        else:
            LogOutput('info', "Hello packets are not exchanged")
            assert "Hello packets are not exchanged"

        LogOutput('info', "Step 4 - verify router ID of switch1"
                  " in hello packet recevied from switch2")

        neighbor_id = get_nbor_id_frm_dump(dut01Obj,
                                           str(dict02[OSPF_IP_ADDR_KEY]),
                                           dump_str)
        if (neighbor_id == OSPF_ROUTER_ID_DUT1):
            LogOutput('info', "Router-id found in hello packet")
        else:
            LogOutput('info', "Router-id not seen in hello packet")
            assert "Router-id not seen in hello packet"

        LogOutput('info', "******[2.01] Passed ******")

    # [2.02] - Test case to verify that the neighbors are discovered
    # When pkt capture is in place we have to check the router id in the packet
    # configuring area id as ipv4 address
    def test_neighbors_are_discoverd(self):
        LogOutput('info', "*****[2.02] Verifying that the"
                  " neighbors are discovered******")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        dut04Obj = self.topoObj.deviceObjGet(device="dut04")

        LogOutput('info', "Step 1 - Configure switch1 ,switch2 and switch3")
        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT2 = dict02[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT3 = dict03[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT4 = dict04[OSPF_ROUTER_KEY]

        LogOutput('info', "Step 2 - Waiting for adjacency")
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW2 with SW1 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT1)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT1

        retVal = wait_for_adjacency(dut03Obj, OSPF_ROUTER_ID_DUT2, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        LogOutput('info', "Step 3 - Verify state of each router "
                  "(DR/BDR/DROther) ")

        state = verify_ospf_states(dut01Obj)
        if (state == "DRBackup"):
            LogOutput('info', "Switch1 in DRBackup state")
        else:
            LogOutput('info', "Switch1 not in correct state")
            assert "switch1 not in correct state"

        state = verify_ospf_states(dut02Obj)
        if (state == "DR"):
            LogOutput('info', "Switch2 in DR state")
        else:
            LogOutput('info', "Switch2 not in correct state")
            assert "switch2 not in correct state"

        LogOutput('info', "Step 4 - verify router ID of switch1 "
                  "in hello packet recevied from switch2")
        dump_str = getTcpdump(dut01Obj)
        neighbor_id = get_nbor_id_frm_dump(dut01Obj,
                                           str(dict02[OSPF_IP_ADDR_KEY]),
                                           dump_str)
        if (neighbor_id == OSPF_ROUTER_ID_DUT1):
            LogOutput('info', "Router-id found in neighbor list")
        else:
            LogOutput('info', "Router-id not found in neighbor list")
            assert "switch1 router-id not found in switch2 eighbor list"

        LogOutput('info', "******[2.02] Passed ******")

    # [2.04] -Test case to verify that neighbor information
    # is updated when one of the neighbor goes down
    def test_adjacency_by_disabling_interface(self):

        LogOutput('info', "******[2.04] Verifying that neighbor information "
                  "is updated when one of the neighbor goes down*****")

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        dut04Obj = self.topoObj.deviceObjGet(device="dut04")

        LogOutput('info', "Step 1 - Configure switch1, switch2 and switch3")
        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT2 = dict02[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT3 = dict03[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT4 = dict04[OSPF_ROUTER_KEY]

        LogOutput('info', "Step 2 - Wait for adjacency")
        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1)
        if retVal:
            LogOutput('info', "Adjacency formed in SW2 with SW1 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT1)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT1

        retVal = wait_for_adjacency(dut03Obj, OSPF_ROUTER_ID_DUT2)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        retVal = wait_for_adjacency(dut04Obj, OSPF_ROUTER_ID_DUT3)
        if retVal:
            LogOutput('info', "Adjacency formed in SW4 with SW3 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT3)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT3

        LogOutput('info', "Step 3 - Disable interface between "
                  "switch1 and switch2 in switch2")
        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]

        interface_value = dut02Obj.linkPortMapping["lnk01"]
        info_str = interface_value + " on " + str(dut01Obj)
        LogOutput('info', "Disabling interface " + info_str)
        retStruct = InterfaceEnable(deviceObj=dut02Obj, enable=False,
                                    interface=interface_value)
        retCode = retStruct.returnCode()
        if retCode != 0:
            assert_msg = "unable to disable " + interface_value
            assert assert_msg

        LogOutput('info', "Step 4 - Disable interface between "
                  "switch2 and switch3 in switch2")
        interface_value = dut02Obj.linkPortMapping["lnk02"]
        LogOutput('info', "Disabling interface " + info_str)
        retStruct = InterfaceEnable(deviceObj=dut02Obj, enable=False,
                                    interface=interface_value)
        retCode = retStruct.returnCode()
        if retCode != 0:
            assert_msg = "unable to disable " + interface_value
            assert assert_msg

        LogOutput('info', "Step 5 - Check adjacency in swich1,"
                  " switch2 and switch3")
        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1, False)
        if retVal:
            LogOutput('info', "Adjacency exist in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT1)
            assert False, "Adjacency not torn in SW2 with "
            " SW3(Router-id % s)" % OSPF_ROUTER_ID_DUT1
        else:
            LogOutput('info', "Adjacency torn in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT1)

        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT3, False)
        if retVal:
            LogOutput('info', "Adjacency exist in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT3)
            assert False, "Adjacency not torn in SW2 with "
            " SW3(Router-id % s)" % OSPF_ROUTER_ID_DUT3
        else:
            LogOutput('info', "Adjacency torn in SW2 with SW3 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT3)

        LogOutput('info', "******[2.04] Passed ******")

    # [2.03]Test case to verify that neighbor information
    # is updated when ospfv2 is disabled in one of the switches
    def test_adjacency_by_deleting_instance(self):
        LogOutput('info', "***** [2.03] Verifying that neighbor information"
                  " is updated when ospfv2 is disabled in one"
                  " of the switch*****")

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        dut04Obj = self.topoObj.deviceObjGet(device="dut04")

        dict01[OSPF_DUT_OBJ] = dut01Obj
        dict02[OSPF_DUT_OBJ] = dut02Obj
        dict02_2[OSPF_DUT_OBJ] = dut02Obj
        dict03[OSPF_DUT_OBJ] = dut03Obj
        dict03_2[OSPF_DUT_OBJ] = dut03Obj
        dict04[OSPF_DUT_OBJ] = dut04Obj

        # Changing area-id to area-ip
        dict01[OSPF_AREA_KEY] = "1.2.3.4"
        dict02[OSPF_AREA_KEY] = "1.2.3.4"
        dict02_2[OSPF_AREA_KEY] = "1.2.3.4"
        dict03[OSPF_AREA_KEY] = "1.2.3.4"
        dict03_2[OSPF_AREA_KEY] = "1.2.3.4"
        dict04[OSPF_AREA_KEY] = "1.2.3.4"

        LogOutput('info', "Step 1 - Configure switch1, switch2 and switch3")

        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        configure(dict01)

        OSPF_ROUTER_ID_DUT2 = dict02[OSPF_ROUTER_KEY]
        configure(dict02)
        configure(dict02_2)

        OSPF_ROUTER_ID_DUT3 = dict03[OSPF_ROUTER_KEY]
        configure(dict03)
        configure(dict03_2)
        configure(dict04)

        LogOutput('info', "Step 2 - Wait for adjacency")
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1)
        if retVal:
            LogOutput('info', "Adjacency formed in SW2 with SW1 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT1)
        else:
            assert False, "Adjacency not formed in SW2 with SW1(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT1

        retVal = wait_for_adjacency(dut03Obj, OSPF_ROUTER_ID_DUT2)
        if retVal:
            LogOutput('info', "Adjacency formed in SW3 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW3 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        retVal = wait_for_adjacency(dut04Obj, OSPF_ROUTER_ID_DUT3)
        if retVal:
            LogOutput('info', "Adjacency formed in SW4 with SW3 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT3)
        else:
            assert False, "Adjacency not formed in SW4 with SW3(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT3

        LogOutput('info', "Step 3 - Delete switch1 and switch3 instance")
        retVal = deleteRouterInstanceTest(dut01Obj)
        assert retVal is True, "Failed to delete Router instance"
        retVal = deleteRouterInstanceTest(dut03Obj)
        assert retVal is True, "Failed to delete Router instance"

        LogOutput('info', "Step 4 - Check for adjacency in Switch 1,"
                  " switch 2 and switch 3")
        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1, False)
        if retVal:
            LogOutput('info', "Adjacency still exist in SW2 with"
                      "SW1(Router-id % s)" % OSPF_ROUTER_ID_DUT1)
            assert False, "Adjacency not torn in SW1 with"
            " SW2(Router-id % s)" % OSPF_ROUTER_ID_DUT1
        else:
            LogOutput('info', "Adjacency torn in SW2 with SW1 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT1)

        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT3, False)
        if retVal:
            LogOutput('info', "Adjacency still exist in SW2 with"
                      "SW3(Router-id % s)" % OSPF_ROUTER_ID_DUT3)
            assert False, "Adjacency not torn in SW2 with"
            "SW3(Router-id % s)" % OSPF_ROUTER_ID_DUT3
        else:
            LogOutput('info', "Adjacency torn in SW2 with SW3 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT3)

        LogOutput('info', "******[2.03] Passed ******")


class Test_ospf_configuration_l2switch:

    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_ospf_configuration_l2switch.testObj = \
            testEnviron(topoDict=topoDict1)
        #    Get topology object
        Test_ospf_configuration_l2switch.topoObj = \
            Test_ospf_configuration_l2switch.testObj.topoObjGet()

    def teardown_class(cls):
        Test_ospf_configuration_l2switch.topoObj.terminate_nodes()

    def test_dr_bdr_selection(self):
        LogOutput('info', "***** [3.01] Test case to verify "
                  "that the DR and BDR is selected")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        dut04Obj = self.topoObj.deviceObjGet(device="dut04")
        dict1_01[OSPF_DUT_OBJ] = dut01Obj
        dict1_02[OSPF_DUT_OBJ] = dut02Obj
        dict1_03[OSPF_DUT_OBJ] = dut03Obj

        LogOutput('info', "Step 1 - configuring SW1, SW2 and SW3")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        OSPF_ROUTER_ID_DUT1 = dict1_01[OSPF_ROUTER_KEY]
        configure(dict1_01)

        OSPF_ROUTER_ID_DUT2 = dict1_02[OSPF_ROUTER_KEY]
        configure(dict1_02)

        OSPF_ROUTER_ID_DUT3 = dict1_03[OSPF_ROUTER_KEY]
        configure(dict1_03)

        # DUT04 is Layer 2 switch hence we are configuring
        # no routing on interfaces
        LogOutput('info', "****** Configure Switch4 interfaces"
                  " with (no routing)  *******")
        enterInterfaceContext(dut04Obj, 1, True)
        enterInterfaceContext(dut04Obj, 2, True)
        enterInterfaceContext(dut04Obj, 3, True)
        exitContext(dut04Obj)
        LogOutput('info', "****** Configure Switch4 interfaces"
                  " with (no routing) finished *******")

        LogOutput('info', "Step 2 - Waiting for adjacency")

        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        LogOutput('info', "Step 3 - Verifying states of switches")
        state = verify_ospf_states(dut01Obj)
        if (state == "DRBackup"):
            LogOutput('info', "Switch1 in DRBackup state")
        else:
            LogOutput('info', "Switch1 not in correct state")
            assert "Switch1 not in correct state"

        state = verify_ospf_states(dut02Obj)
        if (state == "DR"):
            LogOutput('info', "Switch2 in DR  state")
        else:
            LogOutput('info', "Switch2 not in correct state")
            assert "Switch2 not in correct state"

        state = verify_ospf_states(dut03Obj)
        if (state == "DROther"):
            LogOutput('info', "Switch3 in DROther state")
        else:
            LogOutput('info', "Switch3 not in correct state")
            assert "Switch3 not in correct state"

        LogOutput('info', "******[3.01] Passed ******")
        # changing router-id of dut01 to verify DR/BDR/DROther election
        LogOutput('info', "***** [3.04] Test case to verify that the DR"
                  " election is triggered when router ids are changed.")

        LogOutput('info', "Step 1 - Changing router-id of SW1 from 1.1.1.1"
                  " to 5.5.5.5.")
        dict1_01[OSPF_ROUTER_KEY] = "5.5.5.5"
        OSPF_ROUTER_ID_DUT1 = dict1_01[OSPF_ROUTER_KEY]
        configure(dict1_01)

        LogOutput('info', "Step 2 - Waiting for adjacency")
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        LogOutput('info', "Step 3 - Verfiying states of switches")
        state = verify_ospf_states(dut01Obj)
        if (state == "DR"):
            LogOutput('info', "Switch1 in DR state")
        else:
            LogOutput('info', "Switch1 not in correct state")
            assert "Switch1 not in correct state"

        state = verify_ospf_states(dut02Obj)
        if (state == "DROther"):
            LogOutput('info', "Switch2 in DROther state")
        else:
            LogOutput('info', "Switch2 not in correct state")
            assert "Switch2 not in correct state"

        state = verify_ospf_states(dut03Obj)
        if (state == "DRBackup"):
            LogOutput('info', "Switch3 in DRBackup  state")
        else:
            LogOutput('info', "Switch3 not in correct state")
            assert "Switch3 not in correct state"

        LogOutput('info', "******[3.04] Passed ******")

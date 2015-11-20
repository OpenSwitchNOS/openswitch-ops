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
# Name:        test_lacp_ft_modify_non_existent_dynamic.py
#
# Description: Tests that a non-existent dynamic Link Aggregation does not
#              modify an existing configuration. The current link should keep
#              working fine and the configuration retain the same settings
#
# Author:      Jose Calvo
#
# Topology:  |Host A| ---- |Switch A| ---------------- |Switch B| ---- |Host B|
#                                  (Dynamic LAG - 2 links)
#
# Success Criteria:  PASS -> Traffic flow between hosts is not stopped after
#                            applying dynamic LAG configuration and current
#                            configuration is not modified
#
#                    FAILED -> Traffic between hosts stops crossing the dynamic
#                              LAG link or configuration changes, interfaces
#                              reset or any other unexpected behavior
#
###############################################################################

import pytest
from lib_test import *
from opstestfw.switch.CLI import *
from opstestfw import *

topoDict = {"topoExecution": 2000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut02:wrkston02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation"}


# Parses the output of "show run" and verify that the config is empty.
# Returns True if the configuration is empty, False otherwise
def val_empty_config(devices):
    for dev in devices:
        output = showRun(deviceObj=dev).buffer()
        ret_expression = re.search(
            r'Current configuration:\s*!\s*!\s*!\s*(.*)\s*exit',
            output,
            re.DOTALL
        )
        if ret_expression.group(1) != "":
            return False
    return True


# Parses the output of "show interface <int>" and verify the status of
# a link. Returns True if the link is up, False otherwise
def get_int_status(dev, interface):
    output = showInterface(deviceObj=dev, interface=interface).buffer()
    ret_expression = re.search(
        r'Interface \d is (down|up)',
        output
    )
    if ret_expression.group(1) == "up":
        return True
    return False


# Parses the output of "show vlan" and verify that the given VLAN exists
# in the database. Returns True if the VLAN exists, False otherwise
def verify_vlan(dev, vlan_id):
    return_data = vlanVerify(dev, vlan_id)
    if return_data == 0:
        return True
    else:
        return False


# Parses the output of "show vlan" and verify that the given VLAN is
# assigned to the specified switchport.
# Returns True if port belongs to the VLAN, False otherwise
def verify_vlan_ports(dev, vlan_id, port):
    return_data = vlanVerifyPorts(dev, vlan_id, port)
    return return_data


# Creates a dynamic LAG and assign three interfaces to it on the same
# VLAN. Returns 0 if the operations on the switch were successful,
# -1 otherwise
def lag_create_dynamic(devices):
    for dev in devices:
        set_create = lagCreation(
            deviceObj=dev,
            lagId=1,
            configFlag=True
        ).returnCode()
        set_mode = lagMode(
            deviceObj=dev,
            lagId=1,
            lacpMode="active"
        ).returnCode()
        if set_create != 0 or set_mode != 0:
            LogOutput('error', "Could not set link aggregation on the switch")
            return -1
        set_vlan = AddPortToVlan(
            deviceObj=dev,
            vlanId=10,
            interface="lag 1",
            access=True
        ).returnCode()
        if set_vlan != 0:
            LogOutput('error', "A problem occurred while adding VLAN to LAG")
            return -1
        for i in range(2, 4):
            set_int_lag = InterfaceLagIdConfig(
                deviceObj=dev,
                lagId=1,
                interface=i,
                enable=True
            ).returnCode()
            if set_int_lag != 0:
                LogOutput('error', "Problem occurred while adding link to LAG")
                return -1
    return 0


# Sends packets between hosts. Returns 0 if the success rate is 100%
def ping_host(source, dstip_add):
    ret_struct = source.Ping(ipAddr=dstip_add)
    if ret_struct.returnCode() != 0:
        LogOutput('error', "Ping failed...\n")
        ret_code = -1
    else:
        LogOutput('info', "Ping to destination: " + dstip_add)
        LogOutput('info', "\n")
        packet_loss = ret_struct.valueGet(key='packet_loss')
        if packet_loss != 0:
            LogOutput('error', "Packet Loss > 0%, lost" + str(packet_loss))
            ret_code = -1
        else:
            LogOutput('info', "Success is 100%...\n")
            ret_code = 0
    return ret_code


# Check the current LACP configuration for a specific LAG ID. Returns True
# if the configuration exists, False Otherwise
def verify_lacp_settings(dev, int_list, lag_id):
    LogOutput('info', "\nChecking LACP configuration for LAG ID " +
              str(lag_id) + "\n")
    status = lagVerifyConfig(
        deviceObj=dev,
        lagId=lag_id,
        interfaces=int_list,
        lacpMode='active',
        lacpFastFlag=False,
    )
    if not status:
        return False
    return True


# Validates the return code from other functions and throws an exception
# accordingly
def validate_step(code, step):
    if code != 0:
        raise Exception("Test case failed on step " + str(step) + "\n\n")


# Configuration rollback from all devices in the topology. Returns True if
# successfull, False otherwise
def dev_cleanup(dev1, dev2):
    results = []
    dut01 = {'obj': dev1, 'links': ['lnk01', 'lnk03', 'lnk04'],
             'wrkston_links': ['lnk01']}
    dut02 = {'obj': dev2, 'links': ['lnk02', 'lnk03', 'lnk04'],
             'wrkston_links': ['lnk02']}

    LogOutput('info', "Removing Link Aggregation from devices\n")
    results.append(lagCreate(dev1, '1', False, [], None))
    results.append(lagCreate(dev2, '1', False, [], None))

    LogOutput('info', "\nSetting switch interfaces to their default config\n")
    for dut in [dut01, dut02]:
        LogOutput('info', "Configuring switch %s" % dut['obj'].device)
        for link in dut['wrkston_links']:
            results.append(interfaceEnableRouting(
                dut['obj'],
                dut['obj'].linkPortMapping[link],
                True)
            )

    for dut in [dut01, dut02]:
        LogOutput('info', "Configuring switch %s" % dut['obj'].device)
        for link in dut['links']:
            results.append(switchEnableInterface(
                dut['obj'],
                dut['obj'].linkPortMapping[link],
                False)
            )

    LogOutput('info', "\nRemoving VLAN information\n")
    results.append(vlanConfigure(dev1, 10, False))
    results.append(vlanConfigure(dev2, 10, False))

    for i in results:
        if not i:
            return False
    return True


# Main class that runs the steps of the test
class Test_ft_framework_basics:
    def setup_class(cls):
        Test_ft_framework_basics.testObj = testEnviron(topoDict=topoDict)
        Test_ft_framework_basics.topoObj =\
            Test_ft_framework_basics.testObj.topoObjGet()

    def teardown_class(cls):
        Test_ft_framework_basics.topoObj.terminate_nodes()

# Step 1: Initialize devices
    def test_initialize_dev(self):
        LogOutput('info', "#############################")
        LogOutput('info', "STEP 1 - INITIALIZING DEVICES\n")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        devices = []
        test = True
        dut01Obj.Reboot()
        dut02Obj.Reboot()

        devices.append(dut01Obj)
        devices.append(dut02Obj)
        val_config = val_empty_config(devices)

        if not val_config:
            LogOutput('info', "Could not initialize devices\n")
            test = False

        if not test:
            LogOutput('error', "       STEP 1 - FAILED      ")
        else:
            LogOutput('info', "\n")
            LogOutput('info', "Devices set with the default configuration")
            LogOutput('info', "\n")
            LogOutput('info', "       STEP 1 - SUCCESS      ")
        LogOutput('info', "\n")
        LogOutput('info', "        STEP 1 COMPLETE      ")
        LogOutput('info', "#############################")

# Step 2: Create VLAN on both switches
    def test_set_vlans(self):
        LogOutput('info', "\n")
        LogOutput('info', "######################")
        LogOutput('info', "STEP 2 - CREATING VLAN\n")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        devices = []
        test = True

        devices.append(dut01Obj)
        devices.append(dut02Obj)

        for dev in devices:
            ret_code = VlanStatus(
                deviceObj=dev,
                vlanId=10,
                status=True
            ).returnCode()

            try:
                validate_step(ret_code, 2)
            except Exception as err:
                LogOutput('error', "TEST FAILED: " + str(err))
                test = False
                break

            vlan_status = verify_vlan(dev, 10)
            if vlan_status is False:
                LogOutput('error', "Vlan not found")
                test = False
                break

        if not test:
            LogOutput('error', "       STEP 2 - FAILED      ")
        else:
            LogOutput('info', "\n")
            LogOutput('info', "Vlan created successfully")
            LogOutput('info', "\n")
            LogOutput('info', "       STEP 2 - SUCCESS      ")
        LogOutput('info', "\n")
        LogOutput('info', "        STEP 2 COMPLETE      ")
        LogOutput('info', "#############################")

# Step 3: Assign VLAN to host switchports
    def test_assign_vlans(self):
        LogOutput('info', "\n")
        LogOutput('info', "#####################################")
        LogOutput('info', "STEP 3 - ASSIGNING VLAN TO INTERFACES\n")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        devices = []
        test = True

        devices.append(dut01Obj)
        devices.append(dut02Obj)

        for dev in devices:
            LogOutput('info', "Adding Interface 1 to VLAN 10...")
            ret_code = AddPortToVlan(
                deviceObj=dev,
                vlanId=10,
                interface=1,
                access=True
            ).returnCode()

            try:
                validate_step(ret_code, 3)
            except Exception as err:
                LogOutput('error', "TEST FAILED: " + str(err))
                test = False
                break

            port_vlan = verify_vlan_ports(dev, 10, "1")

            if port_vlan is False:
                LogOutput('error', "VLAN not found on interface")
                test = False
                break

        if not test:
            LogOutput('error', "       STEP 3 - FAILED      ")
        else:
            LogOutput('info', "\n")
            LogOutput('info', "Interfaces assigned to VLAN successfully")
            LogOutput('info', "\n")
            LogOutput('info', "       STEP 3 - SUCCESS      ")
        LogOutput('info', "\n")
        LogOutput('info', "        STEP 3 COMPLETE      ")
        LogOutput('info', "#############################")

# Step 4: Create dynamic LAG and assign it to switch interfaces
    def test_create_lag(self):
        LogOutput('info', "\n")
        LogOutput('info', "##################################")
        LogOutput('info', "STEP 4 - CREATING LINK AGGREGATION\n")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        devices = []
        links = ['2', '3']
        test = True

        devices.append(dut01Obj)
        devices.append(dut02Obj)

        ret_code = lag_create_dynamic(devices)

        try:
            validate_step(ret_code, 4)
        except Exception as err:
            LogOutput('error', "TEST FAILED: " + str(err))
            test = False

        lag_status = verify_lacp_settings(dut01Obj, links, '1')

        if not lag_status:
            LogOutput('error', "Incorrect LAG configuration for Switch A")
            test = False

        lag_status = verify_lacp_settings(dut02Obj, links, '1')

        if not lag_status:
            LogOutput('error', "Incorrect LAG configuration for Switch B")
            test = False

        if not test:
            LogOutput('error', "       STEP 4 - FAILED      ")
        else:
            LogOutput('info', "\n")
            LogOutput('info', "Link Aggregation created successfully")
            LogOutput('info', "\n")
            LogOutput('info', "       STEP 4 - SUCCESS      ")
        LogOutput('info', "\n")
        LogOutput('info', "        STEP 4 COMPLETE      ")
        LogOutput('info', "#############################")

# Step 5: Enable links between devices
    def test_set_links(self):
        LogOutput('info', "\n")
        LogOutput('info', "#######################")
        LogOutput('info', "STEP 5 - ENABLING LINKS\n")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        devices = []
        test = True

        devices.append(dut01Obj)
        devices.append(dut02Obj)

        LogOutput('info', "\n")
        LogOutput('info', "Configuring Switch A, Interface 1...")
        InterfaceEnable(
            deviceObj=dut01Obj,
            enable=True,
            interface=dut01Obj.linkPortMapping['lnk01']
        )
        LogOutput('info', "Configuring Switch A, Interface 2...")
        InterfaceEnable(
            deviceObj=dut01Obj,
            enable=True,
            interface=dut01Obj.linkPortMapping['lnk03']
        )
        LogOutput('info', "Configuring Switch A, Interface 3...")
        InterfaceEnable(
            deviceObj=dut01Obj,
            enable=True,
            interface=dut01Obj.linkPortMapping['lnk04']
        )
        LogOutput('info', "\nConfiguring Switch B, Interface 1...")
        InterfaceEnable(
            deviceObj=dut02Obj,
            enable=True,
            interface=dut02Obj.linkPortMapping['lnk02']
        )
        LogOutput('info', "Configuring Switch B, Interface 2...")
        InterfaceEnable(
            deviceObj=dut02Obj,
            enable=True,
            interface=dut02Obj.linkPortMapping['lnk03']
        )
        LogOutput('info', "Configuring Switch B, Interface 3...")
        InterfaceEnable(
            deviceObj=dut02Obj,
            enable=True,
            interface=dut02Obj.linkPortMapping['lnk04']
        )

        LogOutput('info', "\nConfiguring Host A IP Address")
        ret_code = wrkston01Obj.NetworkConfig(
            ipAddr="192.168.1.10",
            netMask="255.255.255.0",
            broadcast="192.168.1.255",
            interface=wrkston01Obj.linkPortMapping['lnk01'],
            config=True
        ).returnCode()
        try:
            validate_step(ret_code, 5)
        except Exception as err:
            LogOutput('error', "Host A: cannot set IP Address\n" + str(err))
            test = False

        LogOutput('info', "\nConfiguring Host B IP Address")
        ret_code = wrkston02Obj.NetworkConfig(
            ipAddr="192.168.1.11",
            netMask="255.255.255.0",
            broadcast="192.168.1.255",
            interface=wrkston02Obj.linkPortMapping['lnk02'],
            config=True
        ).returnCode()
        try:
            validate_step(ret_code, 5)
        except Exception as err:
            LogOutput('error', "Host B: cannot set IP Address\n" + str(err))
            test = False

        int_status = True
        LogOutput('info', "\n")
        for dev in devices:
            for i in range(1, 4):
                LogOutput('info', "Checking interface " + str(i) + " status")
                int_status = get_int_status(dev, str(i))
                if not int_status:
                    LogOutput('info', "\tFAILED")
                    break
            LogOutput('info', "\n")

        check_h1 = ping_host(wrkston01Obj, "192.168.1.10")
        check_h2 = ping_host(wrkston02Obj, "192.168.1.11")

        if not int_status or check_h1 != 0 or check_h2 != 0:
            LogOutput('info', "One or more interfaces are down\n")
            test = False

        if not test:
            LogOutput('error', "       STEP 5 - FAILED      ")
        else:
            LogOutput('info', "\n")
            LogOutput('info', "Device interfaces have been enabled")
            LogOutput('info', "\n")
            LogOutput('info', "       STEP 5 - SUCCESS      ")
        LogOutput('info', "\n")
        LogOutput('info', "\n        STEP 5 COMPLETE      ")
        LogOutput('info', "#############################")

# Step 6: Send traffic between hosts
    def test_send_traffic(self):
        LogOutput('info', "\n")
        LogOutput('info', "######################################")
        LogOutput('info', "STEP 6 - SENDING PACKETS BETWEEN HOSTS\n")
        host01Obj = self.topoObj.deviceObjGet(device="wrkston01")

        test = True
        ret_code = ping_host(host01Obj, "192.168.1.11")

        try:
            validate_step(ret_code, 6)
        except Exception as err:
            LogOutput('error', "TEST FAILED: " + str(err))
            test = False

        if not test:
            LogOutput('error', "       STEP 6 - FAILED      ")
        else:
            LogOutput('info', "\n")
            LogOutput('info', "Communication between hosts OK")
            LogOutput('info', "\n")
            LogOutput('info', "       STEP 6 - SUCCESS      ")
        LogOutput('info', "\n")
        LogOutput('info', "        STEP 6 COMPLETE      ")
        LogOutput('info', "#############################")

# Step 7: Apply invalid LAG config and verify settings
    def test_apply_invalid_lag(self):
        LogOutput('info', "\n")
        LogOutput('info', "#################################")
        LogOutput('info', "STEP 7 - APPLY INVALID LAG CONFIG\n")

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        devices = []
        links = ['2', '3']
        test = True

        devices.append(dut01Obj)
        devices.append(dut02Obj)

        LogOutput('info', "Attempt to configure non-existent LAG 5...\n")

        for i in range(2, 4):
            InterfaceLagIdConfig(
                deviceObj=dut01Obj,
                lagId=5,
                interface=i,
                enable=True
            )

        lag_invalid = verify_lacp_settings(dut01Obj, links, '5')

        if lag_invalid:
            LogOutput('error', "\nInvalid LAG configuration found for LAG 5\n")
            test = False
        else:
            LogOutput('info', "\nNon-existent LAG not found\n")

        lag_status = verify_lacp_settings(dut01Obj, links, '1')

        if lag_status:
            LogOutput('info', "Existent LAG configuration found for LAG 1")
        else:
            LogOutput('error', "\nA problem with the existent LAG occurred")
            test = False

        if not test:
            LogOutput('error', "       STEP 7 - FAILED      ")
        else:
            LogOutput('info', "\n")
            LogOutput('info', "Unable to configure non-existent LAG")
            LogOutput('info', "\n")
            LogOutput('info', "       STEP 7 - SUCCESS      ")

        LogOutput('info', "\n")
        LogOutput('info', "       STEP 7 COMPLETE")
        LogOutput('info', "#############################")

# Step 8: Validates that traffic is still crossing the links
    def test_send_traffic_lag(self):
        LogOutput('info', "\n")
        LogOutput('info', "##################################################")
        LogOutput('info', "STEP 8 - VALIDATING TRAFFIC FORWARDING OVER LAG \n")
        host01Obj = self.topoObj.deviceObjGet(device="wrkston01")

        test = True
        ret_code = ping_host(host01Obj, "192.168.1.11")

        try:
            validate_step(ret_code, 8)
        except Exception as err:
            LogOutput('error', "TEST FAILED: " + str(err))
            test = False

        if not test:
            LogOutput('error', "       STEP 8 - FAILED      ")
        else:
            LogOutput('info', "\n")
            LogOutput('info', "Communication between hosts OK")
            LogOutput('info', "\n")
            LogOutput('info', "       STEP 8 - SUCCESS      ")
        LogOutput('info', "\n")
        LogOutput('info', "        STEP 8 COMPLETE      ")
        LogOutput('info', "#############################")


# Step 9: Device cleanup
    def test_device_cleanup(self):
        LogOutput('info', "\n")
        LogOutput('info', "#######################")
        LogOutput('info', "STEP 9 - DEVICE CLEANUP\n")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")

        ret_code = dev_cleanup(dut01Obj, dut02Obj)

        if not ret_code:
            LogOutput('error', "\nFailed to clear device configuration\n")
        else:
            LogOutput('info', "\nSuccessfully deleted current configuration\n")

        dut01Obj.Reboot()
        dut02Obj.Reboot()

        LogOutput('info', "Removing addresses from hosts\n")

        wrkston01Obj.NetworkConfig(
            ipAddr="192.168.1.10",
            netMask="255.255.255.0",
            broadcast="192.168.1.255",
            interface=wrkston01Obj.linkPortMapping['lnk01'],
            config=False
        )

        wrkston02Obj.NetworkConfig(
            ipAddr="192.168.1.11",
            netMask="255.255.255.0",
            broadcast="192.168.1.255",
            interface=wrkston02Obj.linkPortMapping['lnk02'],
            config=False
        )
        LogOutput('info', "\n")
        LogOutput('info', "       STEP 9 COMPLETE       ")
        LogOutput('info', "#############################\n")
        LogOutput('info', "############################################")
        LogOutput('info', "                TEST COMPLETE               ")
        LogOutput('info', "############################################")

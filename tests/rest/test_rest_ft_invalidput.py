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
import json
from opstestfw.switch.CLI import *
from opstestfw import *
topoDict = {"topoExecution": 3000,
            "topoTarget": "dut01",
            "topoDevices": "dut01 wrkston01",
            "topoLinks": "lnk01:dut01:wrkston01",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston01:docker-image:host/freeradius-ubuntu",
            "topoLinkFilter": "lnk01:dut01:interface:eth0"}
switchMgmtAddr = "10.10.10.2"
restClientAddr = "10.10.10.3"
broadcast = "10.10.10.255"
netmask = "255.255.255.0"
subnetMaskBits = 24


def switch_reboot(dut01):
    # Reboot switch
    info('###  Reboot switch  ###\n')
    dut01.Reboot()
    rebootRetStruct = returnStruct(returnCode=0)
    return rebootRetStruct


def config_rest_environment(dut01, wrkston01):
    #Configuring REST environment
    global switchMgmtAddr
    global restClientAddr

    retStruct = InterfaceIpConfig(deviceObj=dut01,
                                  interface="mgmt",
                                  addr=switchMgmtAddr,
                                  mask=subnetMaskBits,
                                  config=True)
    assert retStruct.returnCode() == 0, 'Failed to configure IP on switchport'
    info('### Successfully configured ip on switch port ###\n')
    cmdOut = dut01.cmdVtysh(command="show run")
    info('### Running config of the switch:\n' + cmdOut + ' ###\n')
    info('### Configuring workstations ###\n')
    retStruct = wrkston01.NetworkConfig(
                                ipAddr=restClientAddr,
                                netMask=netmask,
                                broadcast=broadcast,
                                interface=wrkston01.linkPortMapping['lnk01'],
                                config=True)
    assert retStruct.returnCode() == 0, 'Failed to configure IP workstation'
    info('### Successfully configured IP on workstation ###\n')
    cmdOut = wrkston01.cmd("ifconfig " + wrkston01.linkPortMapping['lnk01'])
    info('### Ifconfig info for workstation 1:\n' + cmdOut + '###\n')
    retStruct = GetLinuxInterfaceIp(deviceObj=wrkston01)
    assert retStruct.returnCode() == 0, 'Failed to get linux\
    interface ip on switch'
    info('### Successful in getting linux interface ip on\
    the workstation ###\n')

    retStruct = returnStruct(returnCode=0)
    return retStruct


def deviceCleanup(dut01, wrkston01):
    retStruct = wrkston01.NetworkConfig(
                                ipAddr=restClientAddr,
                                netMask=netmask,
                                broadcast=broadcast,
                                interface=wrkston01.linkPortMapping['lnk01'],
                                config=False)
    assert retStruct.returnCode() == 0, 'Failed to unconfigure IP\
    address on workstation 1'
    info('### Successfully unconfigured ip on Workstation 1 ###\n')
    cmdOut = wrkston01.cmd("ifconfig " + wrkston01.linkPortMapping['lnk01'])
    info('### Ifconfig info for workstation 1:\n' + cmdOut + ' ###')
    retStruct = InterfaceIpConfig(deviceObj=dut01,
                                  interface="mgmt",
                                  addr=switchMgmtAddr,
                                  mask=subnetMaskBits,
                                  config=False)
    assert retStruct.returnCode() == 0, 'Failed to unconfigure IP\
    address on dut01 port'
    info('### Unconfigured IP address on dut01 port " ###\n')
    cmdOut = dut01.cmdVtysh(command="show run")
    info('Running config of the switch:\n' + cmdOut)
    retStruct = returnStruct(returnCode=0)
    return retStruct


def restTestInvalidputmethod(wrkston01):
    data = {
        "configuration": {
            "bridges": ["/rest/v1/system/bridge_normal"],
            "lacp_config": {},
            "dns_servers": [],
            "aaa": {
                "ssh_publickeyauthentication": "enable",
                "fallback": "true",
                "radius": "false",
                "ssh_passkeyauthentication": "enable"},
            "logrotate_config": {},
            "hostname": "openswitch",
            "manager_options": [],
            "subsystems": ["/rest/v1/system/base"],
            "asset_tag_number": "",
            "ssl": [],
            "mgmt_intf": {
                "ip": switchMgmtAddr,
                "subnet-mask": "%d" % subnetMaskBits,
                "mode": "static",
                "name": "eth0",
                "default-gateway": ""},
            "radius_servers": [],
            "management_vrf": [],
            "other_config": {
                "enable-statistics": "true"},
            "daemons": [
                "/rest/v1/system/fan",
                "/rest/v1/system/power",
                "/rest/v1/system/sys",
                "/rest/v1/system/led",
                "/rest/v1/system/pm",
                "/rest/v1/system/temp"],
            "bufmon_config": {},
            "external_ids": {},
            "ecmp_config": {},
            "vrfs": ["/rest/v1/system/vrf"]}}
    putdata = {
        "configuration": {
            "split_parent": ["/rest/v1/system/interfaces/1"],
            "name": "1",
            "other_config": {},
            "user_config": {},
            "split_children": [],
            "external_ids": {},
            "type": "integer",
            "options": {}
        }
    }
    retStruct = wrkston01.RestCmd(
        switch_ip=switchMgmtAddr,
        url="/rest/v1/system",
        method="PUT",
        data=data)
    assert retStruct.returnCode(
    ) == 0, 'FAILED in executing the rest command \
    "PUT as not expected for url=/rest/v1/system"'
    info('### PASSED in Execute rest command \
    "PUT as expected for url=/rest/v1/system" ###\n')
    info('http return code' + retStruct.data['http_retcode'])
    info('###' + retStruct.data['response_body'] + '###\n')
    assert retStruct.data['http_retcode'].find(
        '200') == -1, 'Rest INVALID PUT PASSED as not expected for system\n' +\
        retStruct.data['response_body']
    info('### Success in INVALID Rest PUT for system ###\n')
    info('###' + retStruct.data['response_body'] + '###\n')
    retStruct = wrkston01.RestCmd(
        switch_ip=switchMgmtAddr,
        url="/rest/v1/system/interfaces/1",
        method="PUT",
        data=putdata)
    assert retStruct.returnCode(
    ) == 0, 'FAILED in executing the rest command \
    "PUT as not expected for url=/rest/v1/system/interfaces/1"'
    info('### PASSED in Execute rest command \
    "PUT as expected for url=/rest/v1/system/interfaces/1 ###\n')
    info('http return code' + retStruct.data['http_retcode'])
    info('###' + retStruct.data['response_body'] + '###\n')
    assert retStruct.data['http_retcode'].find(
        '200') == -1, 'Rest INVALID PUT PASSED as not expected\
        for Interfaces id\n' + retStruct.data['response_body']
    info('### Success in INVALID Rest PUT for Interfaces id ###\n')
    info('###' + retStruct.data['response_body'] + '###\n')
    retStruct = returnStruct(returnCode=0)
    return retStruct


class Test_ft_framework_rest:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_ft_framework_rest.testObj = testEnviron(topoDict=topoDict)
        Test_ft_framework_rest.topoObj = \
            Test_ft_framework_rest.testObj.topoObjGet()
        wrkston01Obj = Test_ft_framework_rest.topoObj.deviceObjGet(
            device="wrkston01")
        wrkston01Obj.CreateRestEnviron()

    def teardown_class(cls):
        # Terminate all nodes
        Test_ft_framework_rest.topoObj.terminate_nodes()

    def test_reboot_switch(self):
        info('########################################################\n')
        info('############       Reboot the switch          ##########\n')
        info('########################################################\n')
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        retStruct = switch_reboot(dut01Obj)
        assert retStruct.returnCode() == 0, 'Failed to reboot Switch'
        info('### Successful in Switch Reboot piece ###\n')

    def test_config_rest_environment(self):
        info('#######################################################\n')
        info('######        Configure REST environment           ####\n')
        info('#######################################################\n')
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        retStruct = config_rest_environment(dut01Obj, wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to config REST environment'
        info('### Successful in config REST environment test ###\n')

    def test_restTestInvalidputmethod(self):
        info('#######################################################\n')
        info('######   Testing REST Invalid PUT Method functionality   ####\n')
        info('#######################################################\n')
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        retStruct = restTestInvalidputmethod(wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to\
        test rest Invalid PUT Method'
        info('### Successful in test rest Invalid PUT Method ###\n')

    def test_clean_up_devices(self):
        info('#######################################################\n')
        info('######    Device Cleanup - rolling back config     ####\n')
        info('#######################################################\n')
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        retStruct = deviceCleanup(dut01Obj, wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to cleanup device'
        info('### Successfully Cleaned up devices ###\n')

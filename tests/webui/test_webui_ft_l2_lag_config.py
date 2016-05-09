#!/usr/bin/env python
#
# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
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

from utils.wrapper import retry_wrapper
from opsvsi.docker import Mininet
from mininet.util import irange
from opsvsi.opsvsitest import (
    Topo,
    OpsVsiTest,
    VsiOpenSwitch,
    OpsVsiHost,
    OpsVsiLink
)

from mininet.log import info

import json
import httplib
import urllib

from opsvsiutils.restutils.utils import (
    execute_request,
    get_switch_ip,
    get_json,
    rest_sanity_check,
    login,
    get_server_crt,
    remove_server_crt
)

import copy

NUM_OF_SWITCHES = 2
NUM_HOSTS = 2

PATCH_LAG_PRT = [{"op": "add", "path": "/admin", "value": "up"}]

VLAN_MODE_PATCH_PRT = {"op": "add", "path": "/vlan_mode", "value": "access"}

PATCH_PRT = {"op": "add", "path": "/ports", "value": []}

ADM_PATCH_INT = [{"op": "add", "path": "/user_config",
                  "value": {"admin": "up"}}]

LACP_KEY_PATCH_INT = {"op": "add",
                      "path": "/other_config",
                      "value": {"lacp-aggregation-key": "1"}}

LACP_KEY_DELETE_PATCH_INT = {"op": "remove",
                             "path": "/other_config/lacp-aggregation-key"}

LAG_PORT_DATA = {
    "configuration": {
        "name": "lag1",
        "interfaces": ["/rest/v1/system/interfaces/1"],
        "other_config": {"lacp-time": "fast"}
    },
    "referenced_by": [{"uri": "/rest/v1/system/bridges/bridge_normal"}]
}

ADD = "ADD"
REMOVE = "REMOVE"

SWITCH_PREFIX = "s"
HOST_PREFIX = "h"
PORT_1 = "1"
PORT_2 = "2"
PORT_3 = "3"

LAG_ID = "12"
INTERFACES = {"1", "2"}

LACP_AGGREGATION_KEY = "lacp-aggregation-key"

# The host IPs are based on 10.0.0.0/8

INTERFACE_STATE_STEP = 10
INTERFACE_STATE_TIMEOUT = 70

LAG_STATE_STEP = 5
LAG_STATE_TIMEOUT = 45

LAG_DELETION_STEP = 1
LAG_DELETION_TIMEOUT = 5


@pytest.fixture
def netop_login(request):
    request.cls.test_var.COOKIE_HDR_1 = login(request.cls.test_var.SWITCH_IP1)
    request.cls.test_var.COOKIE_HDR_2 = login(request.cls.test_var.SWITCH_IP2)


class myTopo(Topo):

    def build(self, hsts=0, sws=2, **_opts):
        self.hsts = hsts
        self.sws = sws
        self.addSwitch("%s1" % SWITCH_PREFIX)
        self.addSwitch("%s2" % SWITCH_PREFIX)

        # Add the hosts. One per switch.
        for i in irange(1, hsts):
            hostName = "%s%s" % (HOST_PREFIX, i)
            self.addHost(hostName)
        # Connect the hosts to the switches
        for i in irange(1, sws):
            self.addLink("%s%s" % (SWITCH_PREFIX, i),
                         "%s%s" % (HOST_PREFIX, i), int(PORT_3), int(PORT_3))
        # Connect the switches
        for i in irange(2, sws):
            self.addLink("%s%s" % (SWITCH_PREFIX, i-1),
                         "%s%s" % (SWITCH_PREFIX, i), int(PORT_1), int(PORT_1))
            self.addLink("%s%s" % (SWITCH_PREFIX, i-1),
                         "%s%s" % (SWITCH_PREFIX, i), int(PORT_2), int(PORT_2))


class Test_CreateLag(OpsVsiTest):
    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=NUM_HOSTS,
                                       sws=NUM_OF_SWITCHES,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                           switch=VsiOpenSwitch,
                           host=OpsVsiHost,
                           link=OpsVsiLink,
                           ipBase="10.0.0.0/8",
                           controller=None,
                           build=True)

        self.SWITCH_IP1 = get_switch_ip(self.net.switches[0])
        self.SWITCH_IP2 = get_switch_ip(self.net.switches[1])
        self.PATH = "/rest/v1/system"
        self.PATH_PORTS = self.PATH + "/ports"
        self.PATH_INT = self.PATH + "/interfaces"
        self.PATH_VRF_DEFAULT = self.PATH + "/vrfs/vrf_default"
        self.PATH_BRIDGE_NORMAL = self.PATH + "/bridges/bridge_normal"

    def retry_validate_turn_on_interfaces(self, sw, cookie_header, interfaces,
                                          init_msg, err_msg,
                                          time_steps, timeout):
        validate_func = retry_wrapper(init_msg, err_msg,
                                      time_steps, timeout
                                      )(self.validate_turn_on_interfaces)
        validate_func(sw, cookie_header, interfaces)

    def retry_validate_lag_ok(self,
                              init_msg, err_msg,
                              time_steps, timeout,
                              lagName, mode='active'):
        validate_func = retry_wrapper(init_msg,
                                      err_msg,
                                      time_steps,
                                      timeout)(self.validate_lag_ok)
        validate_func(lagName, mode)

    def retry_validate_lag_deletion_ok(self, lagName,
                                       init_msg, err_msg,
                                       time_steps, timeout):
        validate_deletion_func = retry_wrapper(init_msg, err_msg,
                                               time_steps, timeout
                                               )(self.validate_lag_deletion_ok)
        validate_deletion_func(lagName)

    def create_topo_no_lag(self):
        # set up port 1, 2 and 3 on switch 1
        self.int_admin_up(self.SWITCH_IP1, self.COOKIE_HDR_1, PORT_1)
        self.int_admin_up(self.SWITCH_IP1, self.COOKIE_HDR_1, PORT_2)
        self.int_admin_up(self.SWITCH_IP1, self.COOKIE_HDR_1, PORT_3)
        # set up port 1, 2 and 3 on switch 2
        self.int_admin_up(self.SWITCH_IP2, self.COOKIE_HDR_2, PORT_1)
        self.int_admin_up(self.SWITCH_IP2, self.COOKIE_HDR_2, PORT_2)
        self.int_admin_up(self.SWITCH_IP2, self.COOKIE_HDR_2, PORT_3)

    def test_create_l2_lag(self):
        self.create_topo_no_lag()
        self.create_l2_lag(self.SWITCH_IP1, self.COOKIE_HDR_1,
                           LAG_ID, INTERFACES, "active")
        self.set_vlan_mode(self.SWITCH_IP1, self.COOKIE_HDR_1,
                           "lag" + LAG_ID, "trunk")
        self.create_l2_lag(self.SWITCH_IP2, self.COOKIE_HDR_2,
                           LAG_ID, INTERFACES, "passive")
        self.set_vlan_mode(self.SWITCH_IP2, self.COOKIE_HDR_2,
                           "lag" + LAG_ID, "trunk")
        self.verify_lag_ok("lag" + LAG_ID)

    def test_delete_lag(self):
        # called after test_create_lag()
        self.delete_lag(self.SWITCH_IP1, self.COOKIE_HDR_1,
                        LAG_ID, INTERFACES)
        self.delete_lag(self.SWITCH_IP2, self.COOKIE_HDR_2,
                        LAG_ID, INTERFACES)
        self.verify_lag_deleted("lag" + LAG_ID)

    def create_l2_lag(self, switch, cookie_header, lagId, interfaces, mode):
        port_path = self.PATH_PORTS + "/" + lagId
        port_data = copy.deepcopy(LAG_PORT_DATA)
        port_data["configuration"]["name"] = "lag" + lagId
        port_data["configuration"]["admin"] = "up"
        port_data["configuration"]["lacp"] = mode

        # build array of interfaces
        ints = []
        for interface in interfaces:
            ints.append("/rest/v1/system/interfaces/" + interface)
        port_data["configuration"]["interfaces"] = ints
        info("\n########## Switch " + switch + ": Create LAG " +
             lagId + " ##########\n")
        status_code, response_data = execute_request(
            self.PATH_PORTS, "POST", json.dumps(port_data), switch, False,
            xtra_header=cookie_header)

        assert status_code == httplib.CREATED, "Error creating a Port.Status" \
            + " code: %s Response data: %s " % (status_code, response_data)
        info("### Port Created. Status code is 201 CREATED  ###\n")
        self.assign_lacp_aggregation_key_ints(switch, cookie_header,
                                              lagId, interfaces)

    def delete_lag(self, switch, cookie_header, lagId, interfaces):
        port_path = self.PATH_PORTS + "/lag" + lagId
        info("\n########## Switch " + switch + ": Delete LAG " +
             lagId + " ##########\n")
        status_code, response_data = execute_request(
            port_path, "DELETE", None, switch, False,
            xtra_header=cookie_header)

        assert status_code == httplib.NO_CONTENT,\
            "Error deleting a Lag Port. Status" \
            + " code: %s Response data: %s " % (status_code, response_data)
        info("### Lag Port Deleted. Status code is 201 DELETED  ###\n")
        #self.remove_lacp_aggregation_key_ints(switch, interfaces)

    def assign_lacp_aggregation_key_ints(self, switch, cookie_header,
                                         lagId, interfaces):
        for interface in interfaces:
            self.assign_lacp_aggregation_key_int(switch, cookie_header,
                                                 lagId, interface)

    def assign_lacp_aggregation_key_int(self, switch, cookie_header,
                                        lagId, interface):
        int_path = self.PATH_INT + "/" + interface
        int_data = copy.deepcopy(LACP_KEY_PATCH_INT)
        int_data["value"][LACP_AGGREGATION_KEY] = lagId
        status_code, response_data = execute_request(
            int_path,
            "PATCH",
            json.dumps([int_data]),
            switch,
            False,
            xtra_header=cookie_header)

        assert status_code == httplib.NO_CONTENT, "Error patching an "\
            "Interface. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### Interface Patched. Status code is 204 NO CONTENT  ###\n")

    def set_vlan_mode(self, switch, cookie_header, port, mode):
        port_path = self.PATH_PORTS + "/" + port
        port_data = copy.deepcopy(VLAN_MODE_PATCH_PRT)
        port_data["value"] = mode
        status_code, response_data = execute_request(
            port_path,
            "PATCH",
            json.dumps([port_data]),
            switch,
            False,
            xtra_header=cookie_header)

        assert status_code == httplib.NO_CONTENT, "Error patching an "\
            "Interface. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### VLAN mode Patched. Status code is 204 NO CONTENT  ###\n")

    def delete_port(self, switch, cookie_header, interface):
        port_path = self.PATH_PORTS + interface
        info("\n########## Switch " + switch + ": Delete Port " +
             interface + " ##########\n")
        status_code, response_data = execute_request(
            port_path, "DELETE", None, switch, False,
            xtra_header=cookie_header)

        info("### Port Deleted. " + httplib.NO_CONTENT + ".  ###\n")

    def remove_lacp_aggregation_key_ints(self, switch, cookie_header,
                                         interfaces):
        for interface in interfaces:
            self.remove_lacp_aggregation_key_int(switch, interface)

    def remove_lacp_aggregation_key_int(self, switch, interface):
        int_path = self.PATH_INT + "/" + interface
        int_data = copy.deepcopy(LACP_KEY_DELETE_PATCH_INT)
        status_code, response_data = execute_request(
            int_path,
            "PATCH",
            json.dumps([int_data]),
            switch,
            False,
            xtra_header=cookie_header)

        assert status_code == httplib.NO_CONTENT, "Error patching an "\
            "Interface. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### Interface Patched. Status code is 204 NO CONTENT  ###\n")

    def verify_lag_ok(self, lagName, mode="active"):
        # Wait for interfaces to be on, then wait for lag to be ok
        info("Waiting for interfaces to turn on")

        self.retry_validate_turn_on_interfaces(
            self.SWITCH_IP1,
            self.COOKIE_HDR_1,
            INTERFACES,
            "\nVerify interfaces are up in " + self.SWITCH_IP1 + "\n",
            "\nRetry to make sure interfaces are up",
            INTERFACE_STATE_STEP,
            INTERFACE_STATE_TIMEOUT)

        self.retry_validate_turn_on_interfaces(
            self.SWITCH_IP2,
            self.COOKIE_HDR_2,
            INTERFACES,
            "\nVerify interfaces are up in " + self.SWITCH_IP2 + "\n",
            "\nRetry to make sure interfaces are up",
            INTERFACE_STATE_STEP,
            INTERFACE_STATE_TIMEOUT)

        self.retry_validate_lag_ok(
            "Ensure lag creation returns status OK",
            "Lag is not yet ready",
            LAG_STATE_STEP,
            LAG_STATE_TIMEOUT,
            lagName,
            mode)

    def verify_lag_deleted(self, lagName):
        self.retry_validate_lag_deletion_ok(
            lagName,
            "Ensure lag deletion returns status OK",
            "Lag deletion is not yet complete",
            LAG_DELETION_STEP,
            LAG_DELETION_TIMEOUT)

    def get_interface_status(self, switch, cookie_header, interface):
        int_path = self.PATH_INT + "/" + interface
        info("### GET INTF STATUS " + switch + "[" + interface + "] ###\n")
        status_code, response_data = execute_request(
            int_path, "GET",
            None,
            switch,
            False,
            xtra_header=cookie_header)
        assert status_code == httplib.OK,\
            "Failed to query Interface " + interface
        return get_json(response_data).get("status")

    def validate_turn_on_interfaces(self, switch, cookie_header, interfaces):
        for intf in interfaces:
            status = self.get_interface_status(switch, cookie_header, intf)
            assert status and status["admin_state"] == 'up' and \
                status["link_state"] == 'up',\
                "Interface link state for " + intf + " is down"

    def validate_lag_ok(self, lagName, mode):
            # assert status bond_hw_handle has value for static lag
            # assert status lacp_status bond_status ok for dynamic lag
            # Verify data
            port_path = self.PATH_PORTS + "/" + lagName
            for switch in [self.SWITCH_IP1, self.SWITCH_IP2]:
                info("### Checking switch " + switch + "###\n")
                if switch == self.SWITCH_IP1:
                    cookie_hdr = self.COOKIE_HDR_1
                else:
                    cookie_hdr = self.COOKIE_HDR_2
                status_code, response_data = execute_request(
                    port_path, "GET",
                    None,
                    switch,
                    False,
                    xtra_header=cookie_hdr)
                assert status_code == httplib.OK,\
                    "Failed to query LAG " + lagName
                json_data = get_json(response_data)
                if mode != "off":
                    assert json_data["status"]["lacp_status"]["bond_status"] \
                        == "ok", "Lag bond status is not OK"
                info("### Switch " + switch + " Lag is ok ###\n")

    def validate_lag_deletion_ok(self, lagName):
        port_path = self.PATH_PORTS + "/" + lagName
        for switch in [self.SWITCH_IP1, self.SWITCH_IP2]:
            info("### Checking switch " + switch + "###\n")
            if switch == self.SWITCH_IP1:
                cookie_hdr = self.COOKIE_HDR_1
            else:
                cookie_hdr = self.COOKIE_HDR_2
            status_code, response_data = execute_request(
                port_path, "GET",
                None,
                switch,
                False,
                xtra_header=cookie_hdr)

            assert status_code == httplib.NOT_FOUND, "Lag deletion is not OK"
            info("### Switch " + switch + " lag deletion is ok ###\n")

    def int_admin_up(self, switch, cookie_header, port):
        int_path = self.PATH_INT + "/" + port

        status_code, response_data = execute_request(
            int_path, "PATCH", json.dumps(ADM_PATCH_INT), switch,
            False, xtra_header=cookie_header)

        assert status_code == httplib.NO_CONTENT, "Error patching an "\
            "Interface. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### Interface Patched. Status code is 204 NO CONTENT  ###\n")


class Test_WebUIREST:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        cls.test_var = Test_CreateLag()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.SWITCH_IP1)
        get_server_crt(cls.test_var.net.switches[1])
        rest_sanity_check(cls.test_var.SWITCH_IP2)

    def teardown_class(cls):
        cls.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run_create_l2_lag(self, netop_login):
        self.test_var.test_create_l2_lag()

    def test_run_delete_lag(self, netop_login):
        self.test_var.test_delete_lag()

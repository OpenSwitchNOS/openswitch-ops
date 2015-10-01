#!/usr/bin/env python
#
# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
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

from opsvsi.docker import *
from opsvsi.opsvsitest import *

import json
import httplib
import urllib

import request_test_utils
import port_test_utils

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

class myTopo(Topo):
    def build (self, hsts=0, sws=1, **_opts):

        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")

class configTest (OpsVsiTest):
    def setupNet (self):
        self.fake_bridge = "fake_bridge"
        self.path = "/rest/v1/system/bridges"
        self.switch_ip = ""
        self.switch_port = 8091
        self.test_path = "%s/%s/vlans" % (self.path, self.fake_bridge)

        self.net = Mininet(topo=myTopo(hsts = NUM_HOSTS_PER_SWITCH,
                                       sws = NUM_OF_SWITCHES,
                                       hopts = self.getHostOpts(),
                                       sopts = self.getSwitchOpts()),
                                       switch = VsiOpenSwitch,
                                       host = None,
                                       link = None,
                                       controller = None,
                                       build = True)

    ###########################################################################
    #                                                                         #
    #   Utils                                                                 #
    #                                                                         #
    ###########################################################################
    def setup_switch_ip(self):
        self.switch_ip = port_test_utils.get_switch_ip(self.net.switches[0])

    def create_fake_port(self, fake_port_name):

        info("\n---------- Creating fake port (%s) ----------\n" % fake_port_name)
        data =  """
                {
                    "configuration": {
                        "name": "%s",
                        "interfaces": ["/rest/v1/system/interfaces/1"],
                        "trunks": [413],
                        "ip4_address_secondary": ["192.168.0.1"],
                        "lacp": ["active"],
                        "bond_mode": ["l2-src-dst-hash"],
                        "tag": 654,
                        "vlan_mode": "trunk",
                        "ip6_address": ["2001:0db8:85a3:0000:0000:8a2e:0370:7334"],
                        "external_ids": {"extid1key": "extid1value"},
                        "bond_options": {"key1": "value1"},
                        "mac": ["01:23:45:67:89:ab"],
                        "other_config": {"cfg-1key": "cfg1val"},
                        "bond_active_slave": "null",
                        "ip6_address_secondary": ["01:23:45:67:89:ab"],
                        "vlan_options": {"opt1key": "opt2val"},
                        "ip4_address": "192.168.0.1",
                        "admin": "up"
                    },
                    "referenced_by": [{"uri": "/rest/v1/system/bridges/bridge_normal"}]
                }
                """ % fake_port_name

        path = "/rest/v1/system/ports"
        info("Testing path: %s\nTesting data: %s\n" % (path, data))

        response_status, response_data = request_test_utils.execute_request(path, "POST", data, self.switch_ip)

        assert response.status == httplib.OK, "Response status received: %s\n" % response_status
        info("Fake port \"%s\" created!\n" % fake_port_name)

        assert response_data is "", "Response data received: %s\n" % response_data
        info("Response data: %s)" % response_data)
        info("---------- Creating fake port (%s) done ----------\n" % fake_port_name)

    def create_fake_vlan(self, bridge_name, fake_vlan_name):
        info("\n---------- Creating fake vlan (%s) ----------\n" % fake_vlan_name)

        data =  """
                {
                    "configuration": {
                        "name": "%s",
                        "id": 1,
                        "description": "test vlan",
                        "admin": ["up"],
                        "other_config": {},
                        "external_ids": {}
                    }
                }
                """ % fake_vlan_name

        path = "%s/%s/vlans" % (self.path, bridge_name)
        info("Testing Path: %s\nTesting Data: %s\n" % (path, data))

        response_status, response_data = request_test_utils.execute_request(path, "POST", data, self.switch_ip)

        assert response_status == httplib.CREATED, "Response status received: %s\n" % response_status
        info("Fake VLAN \"%s\" created!\n" % fake_vlan_name)

        assert response_data is "", "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)
        info("---------- Creating fake vlan (%s) done ----------\n" % fake_vlan_name)

    def create_fake_bridge(self, fake_bridge_name):
        info("\n---------- Creating fake bridge (%s) ----------\n" % fake_bridge_name)
        data =  """
                {
                    "configuration": {
                        "name": "%s",
                        "ports": [],
                        "vlans": [],
                        "datapath_type": "",
                        "other_config": {},
                        "external_ids": {}
                     }
                }
                """ % fake_bridge_name

        path = self.path

        info("Testing path: %s\nTesting data: %s\n" % (path, data))

        response_status, response_data = request_test_utils.execute_request(path, "POST", data, self.switch_ip)

        assert response_status == httplib.CREATED, "Response status: %s\n" % response_status
        info("Bridge \"%s\" created!\n" % fake_bridge_name)

        assert response_data is "", "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("---------- Creating fake bridge (%s) done ----------\n" % fake_bridge_name)

    ###########################################################################
    #                                                                         #
    #   Basic validation                                                      #
    #                                                                         #
    ###########################################################################
    def test_post_system_bridges(self):
        fake_vlan = "fake_vlan_1"

        data =  """
                {
                    "configuration": {
                        "name": "%s",
                        "id": 1,
                        "description": "test vlan",
                        "admin": ["up"],
                        "other_config": {},
                        "external_ids": {}
                    }
                }
                """ % fake_vlan

        info("\n########## Executing POST for /system/bridges ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", data, self.switch_ip)

        assert response_status == httplib.CREATED, "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is "", "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing POST for /system/bridges done ##########\n")

    ###########################################################################
    #                                                                         #
    #   Name validation                                                       #
    #                                                                         #
    ###########################################################################
    def test_post_system_bridges_bad_name(self):
        fake_vlan = "fake_vlan_2"

        data = {}
        data["int"]             =  """{ "configuration": { "name": 1, "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": {} } }"""
        data["empty array"]     =  """{ "configuration": { "name": [], "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": {} } }"""
        data["multiple string"] =  """{ "configuration": { "name": ["test_name", "another_name"], "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": {} } }"""
        data["dict"]            =  """{ "configuration": { "name": {}, "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": {} } }"""
        data["None"]            =  """{ "configuration": { "name": None, "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": {} } }"""
        data["null"]            =  """{ "configuration": { "name": null, "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": {} } }"""

        info("\n########## Executing POST for /system/bridges ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for i in data:
            info("Testing field \"name\" as %s with value: %s\n" % (i, data[i]))

            response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", data[i], self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST for /system/bridges done ##########\n")

    ###########################################################################
    #                                                                         #
    #   Id validation                                                         #
    #                                                                         #
    ###########################################################################
    def test_post_system_bridges_bad_id(self):
        fake_vlan = "fake_vlan_3"

        data = {}
        data["string"]          =  """{ "configuration": { "name": "%s", "id": "1", "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["empty array"]     =  """{ "configuration": { "name": "%s", "id": [], "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["array"]           =  """{ "configuration": { "name": "%s", "id": ["1"], "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["multiple string"] =  """{ "configuration": { "name": "%s", "id": ["1", "2"], "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["dict"]            =  """{ "configuration": { "name": "%s", "id": {}, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["None"]            =  """{ "configuration": { "name": "%s", "id": None, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["null"]            =  """{ "configuration": { "name": "%s", "id": null, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": {} } }""" % fake_vlan

        info("\n########## Executing POST for /system/bridges ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for i in data:
            info("Testing field \"id\" as %s with value: %s\n" % (i, data[i]))

            response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", data[i], self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST for /system/bridges done ##########\n")

    ###########################################################################
    #                                                                         #
    #   Description validation                                                #
    #                                                                         #
    ###########################################################################
    def test_post_system_bridges_bad_description(self):
        fake_vlan = "fake_vlan_4"

        # TODO: Verify valid fields
        data = {}
        data["int"]              =  """{ "configuration": { "name": "%s", "id": 1, "description": 1, "admin": ["up"], "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["empty array"]      =  """{ "configuration": { "name": "%s", "id": 1, "description": [], "admin": ["up"], "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["multiple string"]  =  """{ "configuration": { "name": "%s", "id": 1, "description": ["test vlan", "another_vlan"], "admin": ["up"], "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["dict"]             =  """{ "configuration": { "name": "%s", "id": 1, "description": {}, "admin": ["up"], "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["None"]             =  """{ "configuration": { "name": "%s", "id": 1, "description": None, "admin": ["up"], "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["null"]             =  """{ "configuration": { "name": "%s", "id": 1, "description": null, "admin": ["up"], "other_config": {}, "external_ids": {} } }""" % fake_vlan

        info("\n########## Executing POST for /system/bridges ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for i in data:
            info("Testing field \"description\" as %s with value: %s\n" % (i, data[i]))

            response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", data[i], self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST for /system/bridges done ##########\n")

    ###########################################################################
    #                                                                         #
    #   Admin validation                                                      #
    #                                                                         #
    ###########################################################################
    def test_post_system_bridges_bad_admin(self):
        fake_vlan = "fake_vlan_5"

        # TODO: Verify valid fields
        data = {}
        data["int"]              =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": 1, "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["string"]           =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": "test", "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["empty array"]      =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": [], "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["multiple string"]  =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up", "down"], "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["dict"]             =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": {}, "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["None"]             =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": None, "other_config": {}, "external_ids": {} } }""" % fake_vlan
        data["null"]             =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": null, "other_config": {}, "external_ids": {} } }""" % fake_vlan

        info("\n########## Executing POST for /system/bridges ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for i in data:
            info("Testing field \"admin\" as %s with value: %s\n" % (i, data[i]))

            response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", data[i], self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST for /system/bridges done ##########\n")

    ###########################################################################
    #                                                                         #
    #   Other_Config validation                                               #
    #                                                                         #
    ###########################################################################
    def test_post_system_bridges_bad_other_config(self):
        fake_vlan = "fake_vlan_6"

        data = {}
        data["int"]              =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": 1, "external_ids": {} } }""" % fake_vlan
        data["string"]           =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": "other config", "external_ids": {} } }""" % fake_vlan
        data["empty array"]      =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": [], "external_ids": {} } }""" % fake_vlan
        data["array"]            =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": ["other config"], "external_ids": {} } }""" % fake_vlan
        data["multiple string"]  =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": ["test 1", "test 2"], "external_ids": {} } }""" % fake_vlan
        data["None"]             =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": None, "external_ids": {} } }""" % fake_vlan
        data["null"]             =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": null, "external_ids": {} } }""" % fake_vlan

        info("\n########## Executing POST for /system/bridges ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for i in data:
            info("Testing field \"other_config\" as %s with value: %s\n" % (i, data[i]))

            response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", data[i], self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST for /system/bridges done ##########\n")

    ###########################################################################
    #                                                                         #
    #   External_ids validation                                               #
    #                                                                         #
    ###########################################################################
    def test_post_system_bridges_bad_external_ids(self):
        fake_vlan = "fake_vlan_7"

        data = {}
        data["int"]             =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": 1 } }""" % fake_vlan
        data["string"]          =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": "external_ids" } }""" % fake_vlan
        data["empty array"]     =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": [] } }""" % fake_vlan
        data["string array"]    =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": ["external_ids"] } }""" % fake_vlan
        data["multiple string"] =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": ["external_ids_1", "external_ids_2"] } }""" % fake_vlan
        data["None"]            =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": None } }""" % fake_vlan
        data["null"]            =  """{ "configuration": { "name": "%s", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": null } }""" % fake_vlan

        info("\n########## Executing POST for /system/bridges ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for i in data:
            info("Testing field \"external_ids\" as %s with value: %s\n" % (i, data[i]))

            response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", data[i], self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST for /system/bridges done ##########\n")

    ###########################################################################
    #                                                                         #
    #   Missing fields validation                                             #
    #                                                                         #
    ###########################################################################
    def test_post_system_bridges_bad_missing_fields(self):
        fake_vlan = "fake_vlan_8"

        data = {}
        data["name"]            =  """{ "configuration": { "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": [] } }"""
        data["id"]              =  """{ "configuration": { "name": "%s", "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": "external_ids" } }""" % fake_vlan
        data["description"]     =  """{ "configuration": { "name": "%s", "id": 1, "admin": ["up"], "other_config": {}, "external_ids": None } }""" % fake_vlan
        data["admin"]           =  """{ "configuration": { "name": "%s", "description": "test vlan", "other_config": {}, "external_ids": "external_ids" } }""" % fake_vlan
        data["other_config"]    =  """{ "configuration": { "name": "%s", "description": "test vlan", "admin": ["up"], "external_ids": "external_ids" } }""" % fake_vlan
        data["external_ids"]    =  """{ "configuration": { "name": "%s", "description": "test vlan", "admin": ["up"], "other_config": {} } }""" % fake_vlan

        info("\n########## Executing POST for /system/bridges ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for i in data:
            info("Testing missing field \"%s\" with value: %s\n" % (i, data[i]))

            response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", data[i], self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST for /system/bridges done ##########\n")

    ###########################################################################
    #                                                                         #
    #   Duplicated VLAN validation                                            #
    #                                                                         #
    ###########################################################################
    def test_post_system_bridges_duplicated(self):
        fake_vlan = "fake_vlan_9"

        data =  """
                {
                    "configuration": {
                        "name": "%s",
                        "id": 1,
                        "description": "test vlan",
                        "admin": ["up"],
                        "other_config": {},
                        "external_ids": {}
                    }
                }
                """ % fake_vlan

        info("\n########## Executing POST for /system/bridges ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", data, self.switch_ip)

        assert response_status == httplib.CREATED, "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is "", "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        # Create duplicated
        info("Creating VLAN duplicate: %s\n" % fake_vlan)
        response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", data, self.switch_ip)

        assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is not "", "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing POST for /system/bridges done ##########\n")

    def run_all(self):
        info("\n########## Starting VLAN POST tests ##########\n")
        self.create_fake_bridge(self.fake_bridge)
        self.test_post_system_bridges()
        self.test_post_system_bridges_bad_name()
        self.test_post_system_bridges_bad_id()
        self.test_post_system_bridges_bad_description()
        self.test_post_system_bridges_bad_admin()
        self.test_post_system_bridges_bad_other_config()
        self.test_post_system_bridges_bad_external_ids()
        self.test_post_system_bridges_bad_missing_fields()
        self.test_post_system_bridges_duplicated()
        info("\n########## VLAN POST Tests done ##########\n\n")

class Test_config:
    def setup (self):
        pass

    def teardown (self):
        pass

    def setup_class (cls):
        Test_config.test_var = configTest()

    def teardown_class (cls):
        Test_config.test_var.net.stop()

    def setup_method (self, method):
        pass

    def teardown_method (self, method):
        pass

    def __del__ (self):
        del self.test_var

    def test_run (self):
        self.test_var.setup_switch_ip()
        self.test_var.run_all()

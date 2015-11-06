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

from utils.utils import *

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

class myTopo(Topo):
    def build (self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")

class QueryInterfaceTest (OpsVsiTest):
    def setupNet (self):
        self.net = Mininet(topo=myTopo(hsts=NUM_HOSTS_PER_SWITCH,
                                       sws=NUM_OF_SWITCHES,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                                       switch=VsiOpenSwitch,
                                       host=None,
                                       link=None,
                                       controller=None,
                                       build=True)

        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.PATH = "/rest/v1/system/interfaces"

    def query_recursive_get_depth_1 (self):
        expected_data = "/rest/v1/system/interfaces/50"

        info("\n########## Test to Validate recursive GET Interface 50-1 depth=1 request ##########\n")

        new_path = self.PATH + "?depth=1;name=50-1"
        status_code, response_data = execute_request(new_path, "GET", None, self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        json_data = {}
        try:
            json_data = json.loads(response_data)[0]
        except:
            assert False, "Malformed JSON"

        assert json_data["configuration"] is not None, "configuration key is not present"
        assert json_data["statistics"] is not None, "statistics key is not present"
        assert json_data["status"] is not None, "status key is not present"
        info("### Configuration, statistics and status keys present ###\n")

        assert json_data["configuration"]["split_parent"] is not None, "split_parent key is not present"
        assert json_data["configuration"]["split_children"] is not None, "split_children key is not present"
        info("### split_parent, split_children keys present ###\n")

        assert json_data["configuration"] == INTERFACE_DATA["configuration"], "Configuration data is not equal that posted data"
        info("### Configuration data validated ###\n")

        assert json_data["configuration"]["split_parent"][0] == expected_data, "Correct URI received\n"
        info("### URI for the second level received ###\n")

        info("########## End Test to Validate recursive GET Interface 50-1 depth=1 request ##########\n")

    def query_recursive_get_depth_2 (self):
        expected_data = {"configuration": {
            "split_children": [
              "/rest/v1/system/interfaces/50-1",
              "/rest/v1/system/interfaces/50-2",
              "/rest/v1/system/interfaces/50-3",
              "/rest/v1/system/interfaces/50-4"
            ]
          },
          "referenced_by": [{"uri":"/rest/v1/system/interfaces?depth=2;name=50-1"}]}

        info("\n########## Test to Validate recursive GET Interface 50-1 depth=2 request ##########\n")

        new_path = self.PATH + "?depth=2;name=50-1"
        status_code, response_data = execute_request(new_path, "GET", None, self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        json_data = {}
        try:
            json_data = json.loads(response_data)[0]
        except:
            assert False, "Malformed JSON"

        json_third_level_data = json_data["configuration"]["split_parent"][0]

        assert json_third_level_data["configuration"] is not None, "configuration key is not present"
        assert json_third_level_data["statistics"] is not None, "statistics key is not present"
        assert json_third_level_data["status"] is not None, "status key is not present"
        info("### Configuration, statistics and status keys present ###\n")

        assert json_third_level_data["configuration"]["split_children"].sort() \
        == expected_data["configuration"]["split_children"].sort(), \
        "Configuration data is not equal that posted data"
        info("### URI for the third level received ###\n")

        info("########## End Test to Validate recursive GET Interface 50-1 depth=2 request ##########\n")

    def query_recursive_get_negative_depth_value (self):
        new_path = self.PATH + "?depth=-1"
        status_code, response_data = execute_request(new_path, "GET", None, self.SWITCH_IP)

        info("\n########## Test to Validate recursive GET Interface 50-1 depth=-1 request ##########\n")

        assert status_code == httplib.BAD_REQUEST, "Wrong status code %s " % status_code
        info("### Status code is BAD_REQUEST for URI: %s ###\n" % new_path)

        info("########## End Test to Validate recursive GET Interface 50-1 depth=-1 request ##########\n")

    def query_recursive_get_string_depth_value (self):
        new_path = self.PATH + "?depth=a"
        status_code, response_data = execute_request(new_path, "GET", None, self.SWITCH_IP)

        info("\n########## Test to Validate recursive GET Interface 50-1 depth=a request ##########\n")

        assert status_code == httplib.BAD_REQUEST, "Wrong status code %s " % status_code
        info("### Status code is BAD_REQUEST for URI: %s ###\n" % new_path)

        info("########## End Test to Validate recursive GET Interface 50-1 depth=a request ##########\n")

    def query_all_interfaces_with_depth_zero (self):
        info("\n########## Test to Validate first GET all Interfaces request ##########\n")

        new_path = self.PATH + "?depth=0"
        status_code, response_data = execute_request(new_path, "GET", None, self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"

        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        assert len(json_data) > 0, "Wrong interfaces size %s " % len(json_data)
        info("### There is at least one interface  ###\n")

        info("########## End Test to Validate first GET all Interfaces request ##########\n")

    def query_recursive_get_depth_1_specific_uri (self):
        expected_data = "/rest/v1/system/interfaces/50"

        info("\n########## Test to Validate recursive GET Interface 50-1 \
        depth=1 specific uri request ##########\n")

        new_path = self.PATH + "/50-1?depth=1"
        status_code, response_data = execute_request(new_path, "GET", None, self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        assert json_data["configuration"] is not None, "configuration key is not present"
        assert json_data["statistics"] is not None, "statistics key is not present"
        assert json_data["status"] is not None, "status key is not present"
        info("### Configuration, statistics and status keys present ###\n")

        assert json_data["configuration"]["split_parent"] is not None, "split_parent key is not present"
        assert json_data["configuration"]["split_children"] is not None, "split_children key is not present"
        info("### split_parent, split_children keys present ###\n")

        assert json_data["configuration"] == INTERFACE_DATA["configuration"], "Configuration data is not equal that posted data"
        info("### Configuration data validated ###\n")

        assert json_data["configuration"]["split_parent"][0] == expected_data, "Correct URI received\n"
        info("### URI for the second level received ###\n")

        info("########## End Test to Validate recursive GET Interface 50-1 \
        depth=1 specific uri request ##########\n")

    def query_recursive_get_depth_2_specific_uri (self):
        expected_data = {"configuration": {
            "split_children": [
              "/rest/v1/system/interfaces/50-1",
              "/rest/v1/system/interfaces/50-2",
              "/rest/v1/system/interfaces/50-3",
              "/rest/v1/system/interfaces/50-4"
            ]
          },
          "referenced_by": [{"uri":"/rest/v1/system/interfaces/50-1?depth=2"}]}

        info("\n########## Test to Validate recursive GET Interface 50-1 \
        depth=2 specific uri request ##########\n")

        new_path = self.PATH + "/50-1?depth=2"
        status_code, response_data = execute_request(new_path, "GET", None, self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        json_third_level_data = json_data["configuration"]["split_parent"][0]

        assert json_third_level_data["configuration"] is not None, "configuration key is not present"
        assert json_third_level_data["statistics"] is not None, "statistics key is not present"
        assert json_third_level_data["status"] is not None, "status key is not present"
        info("### Configuration, statistics and status keys present ###\n")

        assert json_third_level_data["configuration"]["split_children"].sort() \
        == expected_data["configuration"]["split_children"].sort(), \
        "Configuration data is not equal that posted data"
        info("### URI for the third level received ###\n")

        info("########## End Test to Validate recursive GET Interface 50-1 \
        depth=2 specific uri request ##########\n")

    def query_recursive_get_negative_depth_value_specific_uri (self):
        new_path = self.PATH + "/50-1?depth=-1"
        status_code, response_data = execute_request(new_path, "GET", None, self.SWITCH_IP)

        info("\n########## Test to Validate recursive GET Interface 50-1 \
        depth=<negative value> specific uri request\n")

        assert status_code == httplib.BAD_REQUEST, "Wrong status code %s " % status_code
        info("### Status code is BAD_REQUEST for URI: %s ###\n" % new_path)

        info("########## End Test to Validate recursive GET Interface 50-1 \
        depth=<negative value> specific uri request\n")

    def query_recursive_get_string_depth_value_specific_uri (self):
        new_path = self.PATH + "/50-1?depth=a"
        status_code, response_data = execute_request(new_path, "GET", None, self.SWITCH_IP)

        info("\n########## Test to Validate recursive GET Interface 50-1 \
        depth=<string> specific uri request\n")

        assert status_code == httplib.BAD_REQUEST, "Wrong status code %s " % status_code
        info("### Status code is BAD_REQUEST for URI: %s ###\n" % new_path)

        info("########## End Test to Validate recursive GET Interface 50-1 \
        depth=<string> specific uri request\n")

    def query_recursive_get_specific_uri_with_depth_zero (self):
        expected_data = "/rest/v1/system/interfaces/50"

        info("\n########## Test to Validate GET specific Interface with depth=0 request ##########\n")

        new_path = self.PATH + "/50-1?depth=0"
        status_code, response_data = execute_request(new_path, "GET", None, self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"

        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        assert json_data["configuration"] is not None, "configuration key is not present"
        assert json_data["statistics"] is not None, "statistics key is not present"
        assert json_data["status"] is not None, "status key is not present"
        info("### Configuration, statistics and status keys present ###\n")

        assert json_data["configuration"]["split_parent"] is not None, "split_parent key is not present"
        assert json_data["configuration"]["split_children"] is not None, "split_children key is not present"
        info("### split_parent, split_children keys present ###\n")

        assert json_data["configuration"] == INTERFACE_DATA["configuration"], "Configuration data is not equal that posted data"
        info("### Configuration data validated ###\n")

        assert json_data["configuration"]["split_parent"][0] == expected_data, "Correct URI received\n"
        info("### URI for the second level received ###\n")

        info("########## End Test to Validate GET specific Interface with depth=0 request ##########\n")

class Test_QueryInterface:
    def setup (self):
        pass

    def teardown (self):
        pass

    def setup_class (cls):
        Test_QueryInterface.test_var = QueryInterfaceTest()

    def teardown_class (cls):
        Test_QueryInterface.test_var.net.stop()

    def setup_method (self, method):
        pass

    def teardown_method (self, method):
        pass

    def __del__ (self):
        del self.test_var

    def test_run (self):
        self.test_var.query_all_interfaces_with_depth_zero()
        self.test_var.query_recursive_get_depth_1()
        self.test_var.query_recursive_get_depth_2()
        self.test_var.query_recursive_get_negative_depth_value()
        self.test_var.query_recursive_get_string_depth_value()
        self.test_var.query_recursive_get_depth_1_specific_uri()
        self.test_var.query_recursive_get_depth_2_specific_uri()
        self.test_var.query_recursive_get_negative_depth_value_specific_uri()
        self.test_var.query_recursive_get_string_depth_value_specific_uri()
        self.test_var.query_recursive_get_specific_uri_with_depth_zero()

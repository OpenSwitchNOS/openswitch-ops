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

import os
import sys
import time
import pytest
import subprocess
import shutil

from opsvsi.docker import *
from opsvsi.opsvsitest import *

import json
import httplib
import urllib

from utils.utils import *

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

path = "/rest/v1/system/ports"
port_path = path + "/Port1"

class myTopo(Topo):
    def build (self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class DeletePortTest (OpsVsiTest):
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
        self.PATH = "/rest/v1/system/ports"
        self.PORT_PATH = self.PATH + "/Port1"

    def delete_port (self):
        info("\n########## Test delete Port ##########\n")
        status_code, response_data = execute_request(self.PORT_PATH, "DELETE", None, self.SWITCH_IP)
        assert status_code == httplib.NO_CONTENT, "Is not sending No Content status code. Status code: %s" % status_code
        info("### Status code is 204 No Content  ###\n")

        info("\n########## End Test delete Port ##########\n")

    def delete_port_if_match (self):
        info("\n########## Test delete Port if-match ##########\n")
        selector_sufix = "?selector=configuration"
        cond_path = self.PORT_PATH + selector_sufix

        status_code, response_data = execute_request(self.PATH, "POST", json.dumps(PORT_DATA), self.SWITCH_IP)
        assert status_code == httplib.CREATED, "Error creating a Port. Status code: %s Response data: %s " % (status_code, response_data)
        info("### Port Created. Status code is 201 CREATED  ###\n")

        response, response_data = execute_request(cond_path, "GET", None, self.SWITCH_IP, True)
        status_code = response.status
        assert status_code == httplib.OK, "Port %s doesn't exists" % self.PORT_PATH

        etag = response.getheader("Etag")
        if etag:
            wrong_etag = etag[::-1]
        else:
            wrong_etag = '"abcdef"'

        status_code, response_data = execute_request(cond_path, "DELETE", None, self.SWITCH_IP, False, {'If-Match':wrong_etag})
        assert status_code == httplib.PRECONDITION_FAILED, "Is not sending Precondition failed code. Status code: %s" % status_code
        info("### Status code is 412 Precondition Failed  ###\n")

        status_code, response_data = execute_request(cond_path, "DELETE", None, self.SWITCH_IP, False, {'If-Match':etag})
        assert status_code == httplib.NO_CONTENT, "Is not sending No Content status code. Status code: %s" % status_code
        info("### Status code is 204 No Content  ###\n")

        new_path = self.PATH + "/Port2" + selector_sufix
        status_code, response_data = execute_request(new_path, "DELETE", None, self.SWITCH_IP, False, {'If-Match':etag})

        assert status_code == httplib.NOT_FOUND, "Validation failed, is not sending Not Found error. Status code: %s" % status_code
        info("### Status code is 404 Not Found  ###\n")

        info("\n########## End Test delete Port if-match ##########\n")


    def verify_deleted_port_from_port_list(self):
        info("\n########## Test Verify if Port is been deleted from port list ##########\n")
        # Verify if port has been deleted from the list
        status_code, response_data = execute_request(self.PATH, "GET", None, self.SWITCH_IP)
        json_data = []
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        assert port_path not in json_data, "Port has not been deleted from port list"
        info("### Port not in list  ###\n")

        info("\n########## End Test Verify if Port is been deleted from port list ##########\n")

    def verify_deleted_port(self):
        info("\n########## Test Verify if Port is found ##########\n")
        # Verify deleted port
        status_code, response_data = execute_request(self.PORT_PATH, "GET", None, self.SWITCH_IP)
        assert status_code == httplib.NOT_FOUND, "Port has not be deleted"
        info("### Port not found  ###\n")

        info("\n########## End Test Verify if Port is found ##########\n")

    def delete_non_existent_port(self):
        info("\n########## Test delete non-existent Port ##########\n")
        new_path = self.PATH + "/Port2"
        status_code, response_data = execute_request(new_path, "DELETE", None, self.SWITCH_IP)

        assert status_code == httplib.NOT_FOUND, "Validation failed, is not sending Not Found error. Status code: %s" % status_code
        info("### Status code is 404 Not Found  ###\n")

        info("\n########## End Test delete non-existent Port  ##########\n")

class Test_DeletePort:
    def setup (self):
        pass

    def teardown (self):
        pass

    def setup_class (cls):
        Test_DeletePort.test_var = DeletePortTest()
        # Add a test port
        create_test_port(Test_DeletePort.test_var.SWITCH_IP)

    def teardown_class (cls):
        Test_DeletePort.test_var.net.stop()

    def setup_method (self, method):
        pass

    def teardown_method (self, method):
        pass

    def __del__ (self):
        del self.test_var

    def test_run (self):
        self.test_var.delete_port()
        self.test_var.verify_deleted_port_from_port_list()
        self.test_var.verify_deleted_port()
        self.test_var.delete_non_existent_port()
        # If Match Tests
        # TODO Fix this test because it fails randomly
        # self.test_var.delete_port_if_match()
        # self.test_var.verify_deleted_port_from_port_list()
        # self.test_var.verify_deleted_port()

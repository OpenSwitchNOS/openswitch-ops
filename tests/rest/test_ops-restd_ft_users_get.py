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

import inspect

from utils.utils import *

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class QueryUserTest(OpsVsiTest):
    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=NUM_HOSTS_PER_SWITCH,
                                       sws=NUM_OF_SWITCHES,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                           switch=VsiOpenSwitch,
                           host=None,
                           link=None,
                           controller=None,
                           build=True)

        self.switch = self.net.switches[0]
        self.SWITCH_IP = get_switch_ip(self.switch)
        self.PATH = "/rest/v1/system/users"

    def create_user(self, user_prefix, user_group, user_prompt, num):
        user_list = []
        if user_group == "ovsdb_users":
            user_list.append({"username": "admin"})
        for i in range(0, num):
            user_name = user_prefix + "_user_" + str(i)
            self.switch.cmd("useradd " + user_name + " -g " + user_group +
                            " -s " + user_prompt)
            user_list.append({"username": user_name})
        return user_list

    def delete_user(self, user_prefix, num):
        for i in range(0, num):
            user_name = user_prefix + "_user_" + str(i)
            self.switch.cmd("userdel -r " + user_name)

    def get_json(self, response_data):
        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        return json_data

    def validate_keys_complete_object(self, json_data):
        assert json_data["configuration"] is not None, \
            "configuration key is not present"
        assert json_data["statistics"] is not None, \
            "statistics key is not present"
        assert json_data["status"] is not None, "status key is not present"

        return True

    def test_get_all_users(self):
        users_list = []
        prompt = "/usr/bin/vtysh"
        expected_data = self.create_user("test", "ovsdb_users", prompt, 100)
        status_code, response_data = execute_request(self.PATH, "GET", None,
                                                     self.SWITCH_IP)
        json_data = self.get_json(response_data)

        info("\n########## Test to Validate GET All Users ##########\n")

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        for data in json_data:
            assert self.validate_keys_complete_object(data)
            users_list.append(data['configuration'])
        info("### Configuration, statistics and status keys present ###\n")

        assert expected_data == users_list, "Wrong expected data\n"
        info("### Data returned as expected ###\n")

        self.delete_user("test", 100)
        info("########## End Test to Validate GET All Users ##########\n")

    def test_get_only_ovsdb_group_users(self):
        users_list = []
        prompt = "/usr/bin/vtysh"
        expected_data = self.create_user("test", "ovsdb_users", prompt, 10)
        self.create_user("user_not_in_ovsdb_group", "nobody", prompt, 1)
        status_code, response_data = execute_request(self.PATH, "GET", None,
                                                     self.SWITCH_IP)
        json_data = self.get_json(response_data)

        info("\n########## Test to Validate GET only OVSDB_GROUP "
             "Users ##########\n")

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        for data in json_data:
            assert self.validate_keys_complete_object(data)
            users_list.append(data['configuration'])
        info("### Configuration, statistics and status keys present ###\n")

        assert expected_data == users_list, "Wrong expected data\n"
        info("### Data returned as expected ###\n")

        self.delete_user("test", 10)
        self.delete_user("user_not_in_ovsdb_group", 1)
        info("########## End Test to Validate GET only OVSDB_GROUP "
             "Users ##########\n")

    def test_get_users_with_not_relevant_argument(self):
        users_list = []
        prompt = "/usr/bin/bash"
        expected_data = self.create_user("test", "ovsdb_users", prompt, 10)
        status_code, response_data = execute_request(self.PATH, "GET", None,
                                                     self.SWITCH_IP)
        json_data = self.get_json(response_data)

        info("\n########## Test to Validate GET All Users in OVSDB_GROUP "
             "with not relevant argument ##########\n")

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        for data in json_data:
            assert self.validate_keys_complete_object(data)
            users_list.append(data['configuration'])
        info("### Configuration, statistics and status keys present ###\n")

        assert expected_data == users_list, "Wrong expected data\n"
        info("### Data returned as expected ###\n")

        self.delete_user("test", 10)
        info("########## End Test to Validate GET All Users in OVSDB_GROUP "
             "With not relevant argument ##########\n")

    def test_get_default_users(self):
        users_list = []
        expected_data = [{'username': 'admin'}]
        status_code, response_data = execute_request(self.PATH, "GET", None,
                                                     self.SWITCH_IP)
        json_data = self.get_json(response_data)

        info("\n########## Test to Validate GET Default User ##########\n")

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        for data in json_data:
            assert self.validate_keys_complete_object(data)
            users_list.append(data['configuration'])
        info("### Configuration, statistics and status keys present ###\n")

        assert expected_data == users_list, "Wrong expected data\n"
        info("### Data returned as expected ###\n")

        info("########## End Test to Validate GET Default User ##########\n")

    def run_tests(self):
        """
        This method will inspect itself to retrieve all existing methods.

        Only methods that begin with "test_" will be executed.
        """
        methodlist = [n for n, v in inspect.getmembers(self,
                                                       inspect.ismethod)
                      if isinstance(v, types.MethodType)]

        info("\n########## Starting Retrieve Users Get Tests ##########\n")
        for name in methodlist:
            if name.startswith("test_"):
                getattr(self, "%s" % name)()
        info("\n########## Ending Retrieve Users Get Tests ##########\n")


class Test_QueryUser:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_QueryUser.test_var = QueryUserTest()

    def teardown_class(cls):
        Test_QueryUser.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def _del_(self):
        del self.test_var

    def test_run(self):
        self.test_var.run_tests()

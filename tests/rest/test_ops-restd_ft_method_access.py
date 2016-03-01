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


from opsvsi.docker import *
from opsvsi.opsvsitest import *

import json
import httplib
from copy import deepcopy

from opsvsiutils.restutils.utils import get_switch_ip, execute_request, \
    rest_sanity_check, login

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

# Using basic data instead of the
# whole thing in utils, for simplicity
BASIC_PORT_DATA = {
    "configuration": {
        "name": "1",
        "interfaces": ["/rest/v1/system/interfaces/1"]
    },
    "referenced_by": [{"uri": "/rest/v1/system/bridges/bridge_normal"}]
}
TEST_PATCH = [{"op": "add",
               "path": "/other_config",
               "value": {}},
              {"op": "add",
               "path": "/other_config/patch_test",
               "value": "test"}]


TEST_HEADER = "Method access permission validation:"
TEST_START = "\n########## " + TEST_HEADER + " %s ##########\n"
TEST_END = "########## End " + TEST_HEADER + " %s ##########\n"

OPS_NETOP = 'ops_netop'
OPS_ADMIN = 'ops_admin'

class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        self.addSwitch("s1")


class MethodAccessTest(OpsVsiTest):
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

        self.BASE_PATH = '/rest/v1'
        self.PATH = self.BASE_PATH + '/system/ports'
        self.PORT_PATH = self.PATH + '/1'
        self.CONFIG_PATH = self.BASE_PATH + '/system/full-configuration'
        self.LOGS_PATH = self.BASE_PATH + '/logs'
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.OPS_ADMIN_USER = 'admin'
        self.OPS_ADMIN_PASS = 'admin'
        self.cookie_header = None

    def ovsdb_POST_method_access_test(self, expected_code, user):
        '''
        Test user permissions for a POST.
        '''
        test_title = "%s user POST, expecting code: %s" % (user, expected_code)
        info(TEST_START % test_title)

        status_code, response_data = \
            execute_request(self.PATH, "POST", json.dumps(BASIC_PORT_DATA),
                            self.SWITCH_IP, xtra_header=self.cookie_header)

        assert status_code == expected_code, \
            "Wrong expected status code for POST: %s Response data: %s " % \
            (status_code, response_data)

        info(TEST_END % test_title.replace("expecting", "received"))

    def ovsdb_PUT_method_access_test(self, expected_code, user):
        '''
        Test user permissions for a PUT.
        '''
        test_title = "%s user PUT, expecting code: %s" % (user, expected_code)
        info(TEST_START % test_title)

        data = deepcopy(BASIC_PORT_DATA)
        data['configuration']['other_config'] = {'test': 'test'}
        del data['referenced_by']

        status_code, response_data = \
            execute_request(self.PATH + "/bridge_normal", "PUT",
                            json.dumps(data), self.SWITCH_IP,
                            xtra_header=self.cookie_header)

        assert status_code == expected_code, \
            "Wrong expected status code for PUT: %s Response data: %s " % \
            (status_code, response_data)

        info(TEST_END % test_title.replace("expecting", "received"))

    def ovsdb_PATCH_method_access_test(self, expected_code, user):
        '''
        Test user permissions for a PATCH.
        '''
        test_title = "%s user PATCH, expecting code: %s" % \
            (user, expected_code)
        info(TEST_START % test_title)

        status_code, response_data = \
            execute_request(self.PATH + "/bridge_normal", "PATCH",
                            json.dumps(TEST_PATCH), self.SWITCH_IP,
                            xtra_header=self.cookie_header)

        assert status_code == expected_code, \
            "Wrong expected status code for PATCH: %s Response data: %s " % \
            (status_code, response_data)

        info(TEST_END % test_title.replace("expecting", "received"))

    def ovsdb_GET_method_access_test(self, expected_code, user):
        '''
        Test user permissions for a GET.
        '''
        test_title = "%s user GET, expecting code: %s" % (user, expected_code)
        info(TEST_START % test_title)

        status_code, response_data = \
            execute_request(self.PATH + "/bridge_normal", "GET",
                            None, self.SWITCH_IP,
                            xtra_header=self.cookie_header)

        assert status_code == expected_code, \
            "Wrong expected status code for GET: %s Response data: %s " % \
            (status_code, response_data)

        info(TEST_END % test_title.replace("expecting", "received"))

    def ovsdb_DELETE_method_access_test(self, expected_code, user):
        '''
        Test user permissions for a DELETE.
        '''
        test_title = "%s user DELETE, expecting code: %s" % \
            (user, expected_code)
        info(TEST_START % test_title)

        status_code, response_data = \
            execute_request(self.PATH + "/1", "DELETE", None,
                            self.SWITCH_IP, xtra_header=self.cookie_header)

        assert status_code == expected_code, \
            "Wrong expected status code for DELETE: %s Response data: %s " % \
            (status_code, response_data)

        info(TEST_END % test_title.replace("expecting", "received"))

    def runconfig_GET_method_access_test(self, expected_code, user):
        '''
        Test user permissions for GET on Config.
        '''
        test_title = "%s user GET on Config, expecting code: %s" % \
            (user, expected_code)
        info(TEST_START % test_title)

        status_code, response_data = \
            execute_request(self.CONFIG_PATH, "GET",
                            None, self.SWITCH_IP,
                            xtra_header=self.cookie_header)

        assert status_code == expected_code, "Wrong expected status code " + \
            "for GET on Config: %s Response data: %s " % \
            (status_code, response_data)

        info(TEST_END % test_title.replace("expecting", "received"))

    def runconfig_PUT_method_access_test(self, expected_code, user):
        '''
        Test user permissions for a PUT on Config.
        '''
        test_title = "%s user PUT on Config, expecting code: %s" % \
            (user, expected_code)
        info(TEST_START % test_title)

        data = {"System": {"hostname": "", "asset_tag_number": ""}}

        status_code, response_data = \
            execute_request(self.CONFIG_PATH, "PUT",
                            json.dumps(data), self.SWITCH_IP,
                            xtra_header=self.cookie_header)

        assert status_code == expected_code, \
            "Wrong expected status code for PUT: %s Response data: %s " % \
            (status_code, response_data)

        info(TEST_END % test_title.replace("expecting", "received"))

    def logs_GET_method_access_test(self, expected_code, user):
        '''
        Test user permissions for GET on Logs.
        '''
        test_title = "%s user GET on Logs, expecting code: %s" % \
            (user, expected_code)
        info(TEST_START % test_title)

        status_code, response_data = \
            execute_request(self.LOGS_PATH, "GET",
                            None, self.SWITCH_IP,
                            xtra_header=self.cookie_header)

        assert status_code == expected_code, "Wrong expected status code " + \
            "for GET: %s Response data: %s " % (status_code, response_data)

        info(TEST_END % test_title.replace("expecting", "received"))


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


@pytest.fixture
def admin_login(request):
    switch_ip = request.cls.test_var.SWITCH_IP
    ops_admin_user = request.cls.test_var.OPS_ADMIN_USER
    ops_admin_pass = request.cls.test_var.OPS_ADMIN_PASS
    request.cls.test_var.cookie_header = login(switch_ip,
                                               username=ops_admin_user,
                                               password=ops_admin_pass)

admin_login_disabled = \
    pytest.mark.skipif(True, reason="ops_admin login is disabled in REST")
logs_disabled = \
    pytest.mark.skipif(True, reason="disable until logs API is in master")


class Test_MethodAccess:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        cls.test_var = MethodAccessTest()
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        cls.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_POST_method_access_test(self, netop_login):
        self.test_var.ovsdb_POST_method_access_test(httplib.CREATED, OPS_NETOP)

    def test_PUT_method_access_test(self, netop_login):
        self.test_var.ovsdb_PUT_method_access_test(httplib.OK, OPS_NETOP)

    def test_PATCH_method_access_test(self, netop_login):
        self.test_var.ovsdb_PATCH_method_access_test(httplib.NO_CONTENT,
                                                     OPS_NETOP)

    def test_GET_method_access_test(self, netop_login):
        self.test_var.ovsdb_GET_method_access_test(httplib.OK, OPS_NETOP)

    def test_DELETE_method_access_test(self, netop_login):
        self.test_var.ovsdb_DELETE_method_access_test(httplib.NO_CONTENT,
                                                      OPS_NETOP)

    def test_runconfig_GET_method_access_test(self, netop_login):
        self.test_var.runconfig_GET_method_access_test(httplib.OK, OPS_NETOP)

    def test_runconfig_PUT_method_access_test(self, netop_login):
        self.test_var.runconfig_PUT_method_access_test(httplib.OK, OPS_NETOP)

    @logs_disabled
    def test_logs_GET_method_access_test(self, netop_login):
        self.test_var.logs_GET_method_access_test(httplib.OK, OPS_NETOP)

    '''
    The following tests are intended to test the restriction of REST's methods
    based on permissions. However, currently, REST allows authentication only
    for users with READ_SWITCH_CONFIG and WRITE_SWITCH_CONFIG permissions; at
    the time of this writing, the only user with either of these permissions is
    netop, which actually has both, so you can't essentially test that a user
    without one of them can't execute a method not allowed by the permission.
    Therefore, these tests are disabled in production. In order to test the
    restriction is actually working, you have to build a version of REST that
    would allow admin to authenticate, re-enable these tests, and run them
    locally, as the admin user does not currently has either of the allowed
    permissions. This is necessary until there exists, by default, a user that
    would be allowed to authenticate while having a different set of
    permissions that serves testing purposes.
    '''

    @admin_login_disabled
    def test_ops_admin_POST_method(self, admin_login):
        self.test_var.ovsdb_POST_method_access_test(httplib.FORBIDDEN,
                                                    OPS_ADMIN)

    @admin_login_disabled
    def test_ops_admin_PUT_method(self, admin_login):
        self.test_var.ovsdb_PUT_method_access_test(httplib.FORBIDDEN,
                                                   OPS_ADMIN)

    @admin_login_disabled
    def test_ops_admin_PATCH_method(self, admin_login):
        self.test_var.ovsdb_PATCH_method_access_test(httplib.FORBIDDEN,
                                                     OPS_ADMIN)

    @admin_login_disabled
    def test_ops_admin_GET_method(self, admin_login):
        self.test_var.ovsdb_GET_method_access_test(httplib.FORBIDDEN,
                                                   OPS_ADMIN)

    @admin_login_disabled
    def test_ops_admin_DELETE_method(self, admin_login):
        self.test_var.ovsdb_DELETE_method_access_test(httplib.FORBIDDEN,
                                                      OPS_ADMIN)

    @admin_login_disabled
    def test_ops_admin_runconfig_GET_method(self, admin_login):
        self.test_var.runconfig_GET_method_access_test(httplib.FORBIDDEN,
                                                       OPS_ADMIN)

    @admin_login_disabled
    def test_ops_admin_runconfig_PUT_method(self, admin_login):
        self.test_var.runconfig_PUT_method_access_test(httplib.FORBIDDEN,
                                                       OPS_ADMIN)

    @admin_login_disabled
    @logs_disabled
    def test_ops_admin_logs_GET_method(self, admin_login):
        self.test_var.logs_GET_method_access_test(httplib.FORBIDDEN,
                                                  OPS_ADMIN)

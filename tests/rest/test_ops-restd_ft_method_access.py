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

        self.PATH = '/rest/v1/system/ports'
        self.PORT_PATH = self.PATH + '/1'
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.OPS_ADMIN_USER = 'admin'
        self.OPS_ADMIN_PASS = 'admin'
        self.cookie_header = None

    def ops_netop_POST_method(self):
        '''
        Test netop user permissions for a POST, should be allowed.
        '''
        test_title = "ops_netop user POST"
        info(TEST_START % test_title)

        status_code, response_data = \
            execute_request(self.PATH, "POST", json.dumps(BASIC_PORT_DATA),
                            self.SWITCH_IP, xtra_header=self.cookie_header)

        assert status_code == httplib.CREATED, \
            "POST unsuccessful. Status code: %s Response data: %s " % \
            (status_code, response_data)

        info(TEST_END % test_title)

    def ops_netop_PUT_method(self):
        '''
        Test netop user permissions for a PUT, should be allowed.
        '''
        test_title = "ops_netop user PUT"
        info(TEST_START % test_title)

        data = deepcopy(BASIC_PORT_DATA)
        data['configuration']['other_config'] = {'test': 'test'}
        del data['referenced_by']

        status_code, response_data = \
            execute_request(self.PATH + "/bridge_normal", "PUT",
                            json.dumps(data), self.SWITCH_IP,
                            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, \
            "PUT unsuccessful. Status code: %s Response data: %s " % \
            (status_code, response_data)

        info(TEST_END % test_title)

    def ops_netop_PATCH_method(self):
        '''
        Test netop user permissions for a PATCH, should be allowed.
        '''
        test_title = "ops_netop user PATCH"
        info(TEST_START % test_title)

        status_code, response_data = \
            execute_request(self.PATH + "/bridge_normal", "PATCH",
                            json.dumps(TEST_PATCH), self.SWITCH_IP,
                            xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, \
            "PATCH unsuccessful. Status code: %s Response data: %s " % \
            (status_code, response_data)

        info(TEST_END % test_title)

    def ops_netop_GET_method(self):
        '''
        Test netop user permissions for a GET, should be allowed.
        '''
        test_title = "ops_netop user GET"
        info(TEST_START % test_title)

        status_code, response_data = \
            execute_request(self.PATH + "/bridge_normal", "GET",
                            None, self.SWITCH_IP,
                            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, \
            "GET unsuccessful. Status code: %s Response data: %s " % \
            (status_code, response_data)

        info(TEST_END % test_title)

    def ops_netop_DELETE_method(self):
        '''
        Test netop user permissions for a DELETE, should be allowed.
        '''
        test_title = "ops_netop user DELETE"
        info(TEST_START % test_title)

        status_code, response_data = \
            execute_request(self.PATH + "/1", "DELETE", None,
                            self.SWITCH_IP, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, \
            "DELETE unsuccessful. Status code: %s Response data: %s " % \
            (status_code, response_data)

        info(TEST_END % test_title)

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

    def ops_admin_POST_method(self):
        '''
        Test admin user permissions for a POST, should not be allowed.
        '''
        test_title = "ops_admin user POST"
        info(TEST_START % test_title)

        admin_cookie_header = login(self.SWITCH_IP,
                                    username=self.OPS_ADMIN_USER,
                                    password=self.OPS_ADMIN_PASS)

        status_code, response_data = \
            execute_request(self.PATH, "POST", json.dumps(BASIC_PORT_DATA),
                            self.SWITCH_IP,
                            xtra_header=admin_cookie_header)

        assert status_code == httplib.FORBIDDEN, \
            "Unauthorized POST successful. " + \
            "Status code: %s Response data: %s " % (status_code, response_data)

        info(TEST_END % test_title)

    def ops_admin_PUT_method(self):
        '''
        Test admin user permissions for a PUT, should not be allowed.
        '''
        test_title = "ops_admin user PUT"
        info(TEST_START % test_title)

        data = deepcopy(BASIC_PORT_DATA)
        data['configuration']['other_config'] = {'test': 'test'}
        del data['referenced_by']

        admin_cookie_header = login(self.SWITCH_IP,
                                    username=self.OPS_ADMIN_USER,
                                    password=self.OPS_ADMIN_PASS)

        status_code, response_data = \
            execute_request(self.PATH + "/bridge_normal", "PUT",
                            json.dumps(data), self.SWITCH_IP,
                            xtra_header=admin_cookie_header)

        assert status_code == httplib.FORBIDDEN, \
            "Unauthorized PUT successful. " + \
            "Status code: %s Response data: %s " % (status_code, response_data)

        info(TEST_END % test_title)

    def ops_admin_PATCH_method(self):
        '''
        Test admin user permissions for a PATCH, should not be allowed.
        '''
        test_title = "ops_admin user PATCH"
        info(TEST_START % test_title)

        admin_cookie_header = login(self.SWITCH_IP,
                                    username=self.OPS_ADMIN_USER,
                                    password=self.OPS_ADMIN_PASS)

        status_code, response_data = \
            execute_request(self.PATH + "/bridge_normal", "PATCH",
                            json.dumps(TEST_PATCH), self.SWITCH_IP,
                            xtra_header=admin_cookie_header)

        assert status_code == httplib.FORBIDDEN, \
            "Unauthorized PATCH successful. " + \
            "Status code: %s Response data: %s " % (status_code, response_data)

        info(TEST_END % test_title)

    def ops_admin_GET_method(self):
        '''
        Test admin user permissions for a GET, should not be allowed.
        '''
        test_title = "ops_admin user GET"
        info(TEST_START % test_title)

        admin_cookie_header = login(self.SWITCH_IP,
                                    username=self.OPS_ADMIN_USER,
                                    password=self.OPS_ADMIN_PASS)

        status_code, response_data = \
            execute_request(self.PATH + "/bridge_normal", "GET",
                            None, self.SWITCH_IP,
                            xtra_header=admin_cookie_header)

        assert status_code == httplib.FORBIDDEN, \
            "Unauthorized GET successful. " + \
            "Status code: %s Response data: %s " % (status_code, response_data)

        info(TEST_END % test_title)

    def ops_admin_DELETE_method(self):
        '''
        Test admin user permissions for a DELETE, should not be allowed.
        '''
        test_title = "ops_admin user DELETE"
        info(TEST_START % test_title)

        admin_cookie_header = login(self.SWITCH_IP,
                                    username=self.OPS_ADMIN_USER,
                                    password=self.OPS_ADMIN_PASS)

        status_code, response_data = \
            execute_request(self.PATH + "/1", "DELETE", None,
                            self.SWITCH_IP,
                            xtra_header=admin_cookie_header)

        assert status_code == httplib.FORBIDDEN, \
            "Unauthorized DELETE successful. " + \
            "Status code: %s Response data: %s " % (status_code, response_data)

        info(TEST_END % test_title)


admin_login_disabled = \
    pytest.mark.skipif(True, reason="ops_admin login is disabled in REST")


class Test_MethodAccess:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        cls.test_var = MethodAccessTest()
        rest_sanity_check(cls.test_var.SWITCH_IP)
        # Login with default user
        cls.test_var.cookie_header = login(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        cls.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_ops_netop_POST_method(self):
        self.test_var.ops_netop_POST_method()

    def test_ops_netop_PUT_method(self):
        self.test_var.ops_netop_PUT_method()

    def test_ops_netop_PATCH_method(self):
        self.test_var.ops_netop_PATCH_method()

    def test_ops_netop_GET_method(self):
        self.test_var.ops_netop_GET_method()

    def test_ops_netop_DELETE_method(self):
        self.test_var.ops_netop_DELETE_method()

    @admin_login_disabled
    def test_ops_admin_POST_method(self):
        self.test_var.ops_admin_POST_method()

    @admin_login_disabled
    def test_ops_admin_PUT_method(self):
        self.test_var.ops_admin_PUT_method()

    @admin_login_disabled
    def test_ops_admin_PATCH_method(self):
        self.test_var.ops_admin_PATCH_method()

    @admin_login_disabled
    def test_ops_admin_GET_method(self):
        self.test_var.ops_admin_GET_method()

    @admin_login_disabled
    def test_ops_admin_DELETE_method(self):
        self.test_var.ops_admin_DELETE_method()

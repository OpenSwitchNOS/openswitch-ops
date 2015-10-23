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
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws

        switch = self.addSwitch("s1")

class systemTest(OpsVsiTest):

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

        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.SWITCH_PORT = 8091
        self.PATH = "/rest/v1/system"

    def call_system_get(self):
        info("\n########## Executing GET request on %s ##########\n" % self.PATH)

        # # Execute GET

        response, json_string = execute_request(self.PATH, "GET", None, self.SWITCH_IP, True)

        assert response.status == httplib.OK, "GET request failed: {0} {1}".format(response.status, response.reason)

        get_data = {}

        try:
            # A malformed json should throw an exception here
            get_data = json.loads(json_string)
        except:
            assert False, "GET: Malformed JSON in response body"

        # # Check data was received

        assert get_data, "GET: Empty response"
        assert type(get_data) is dict, "GET: Malformed response"
        assert len(get_data) > 0, "GET: No data in response"

        info("\n########## Finished executing GET request on %s ##########\n" % self.PATH)

    def call_system_options(self):
        info("\n########## Executing OPTIONS request on %s ##########\n" % self.PATH)

        # # Execute OPTIONS

        response, json_string = execute_request(self.PATH, "OPTIONS", None, self.SWITCH_IP, True)

        assert response.status == httplib.OK, "OPTIONS request failed: {0} {1}".format(response.status, response.reason)

        # # Check expected options are correct

        # TODO change these to propper expected values after correct OPTIONS is implemented
        expected_allow = ["DELETE", "GET", "OPTIONS", "POST", "PUT"]
        response_allow = response.getheader("allow").split(", ")

        assert expected_allow == response_allow, "OPTIONS: unexpected 'allow' options"

        # TODO change these to propper expected values after correct OPTIONS is implemented
        expected_access_control_allow_methods = ["DELETE", "GET", "OPTIONS", "POST", "PUT"]
        response_access_control_allow_methods = response.getheader("access-control-allow-methods").split(", ")

        assert expected_access_control_allow_methods == response_access_control_allow_methods, "OPTIONS: unexpected 'access-control-allow-methods' options"

        info("\n########## Finished executing OPTIONS request on %s ##########\n" % self.PATH)

    def call_system_put(self):
        info("\n########## Executing PUT request on %s ##########\n" % self.PATH)

        # # Get initial data

        # Perform GET until all required status keys are present in the reply
        mgmt_intf = {}
        while not mgmt_intf:

            response, pre_put_json_string = execute_request(self.PATH, "GET", None, self.SWITCH_IP, True)

            assert response.status == httplib.OK, "PUT: initial GET request failed: {0} {1}".format(response.status, response.reason)

            pre_put_get_data = {}

            try:
                # A malformed json should throw an exception here
                pre_put_get_data = json.loads(pre_put_json_string)
            except:
                assert False, "PUT: Malformed JSON in response body for initial GET request"

            if not ('ip' not in pre_put_get_data['status']['mgmt_intf_status'] or
                    'subnet_mask' not in pre_put_get_data['status']['mgmt_intf_status'] or
                    'default_gateway' not in pre_put_get_data['status']['mgmt_intf_status']):
                mgmt_intf = pre_put_get_data['status']['mgmt_intf_status']

        # # Execute PUT request

        put_data = pre_put_get_data['configuration']

        # Modify config keys
        put_data['hostname'] = 'switch'
        put_data['dns_servers'].append("8.8.8.8")
        put_data['asset_tag_number'] = "1"

        put_data['other_config'].update({
            'stats-update-interval': "5001",
            'min_internal_vlan': "1024",
            'internal_vlan_policy': 'ascending',
            'max_internal_vlan': "4094",
            'enable-statistics': "false"
        })

        put_data['external_ids'] = {"id1": "value1"}

        # Some keys from mgmt_intf come inside status dict
        # but they are required in the request data in order
        # for it to be validated by the rest daemon

        mgmt_intf = pre_put_get_data['status']['mgmt_intf_status']

        if 'hostname' in mgmt_intf:
            del mgmt_intf['hostname']
        if 'link_state' in mgmt_intf:
            del mgmt_intf['link_state']
        if 'ipv6_linklocal' in mgmt_intf:
            del mgmt_intf['ipv6_linklocal']

        put_data['mgmt_intf'].update(mgmt_intf)
        put_data['mgmt_intf'].update({
            'default_gateway_v6': '',
            'dns_server_2': '',
            'mode': 'dhcp',
            'ipv6': '',
            'dns_server_1': ''
        })

        put_data['ecmp_config'].update({
            'hash_srcip_enabled': "false",
            'hash_srcport_enabled': "false",
            'hash_dstip_enabled': "false",
            'enabled': "false",
            'hash_dstport_enabled': "false"
        })

        put_data['bufmon_config'].update({
            'collection_period': "5",
            'threshold_trigger_rate_limit': "60",
            'periodic_collection_enabled': "false",
            'counters_mode': 'current',
            'enabled': "false",
            'snapshot_on_threshold_trigger': "false",
            'threshold_trigger_collection_enabled': "false"
        })

        put_data['logrotate_config'].update({
            'maxsize': "10",
            'period': 'daily',
            'target': ''
        })

        # FIXME these should be re-added once they are in the schema
        if 'ssh_publickeyauthentication' in put_data['aaa']:
            del put_data['aaa']['ssh_publickeyauthentication']
        if 'ssh_passkeyauthentication' in put_data['aaa']:
            del put_data['aaa']['ssh_passkeyauthentication']

        response, json_string = execute_request(self.PATH, "PUT", json.dumps({'configuration': put_data}), self.SWITCH_IP, True)

        assert response.status == httplib.OK, "PUT request failed: {0} {1}".format(response.status, response.reason)

        # # Get post-PUT data

        response, post_put_json_string = execute_request(self.PATH, "GET", None, self.SWITCH_IP, True)

        assert response.status == httplib.OK, "PUT: Post-PUT GET request failed: {0} {1}".format(response.status, response.reason)

        post_put_get_data = {}

        try:
            # A malformed json should throw an exception here
            post_put_get_data = json.loads(post_put_json_string)
        except:
            assert False, "PUT: Malformed JSON in post-PUT GET request body"

        # post-PUT data should be the same as pre-PUT data
        post_put_data = post_put_get_data['configuration']

        assert put_data == post_put_data, "PUT: Mismatch between PUT request data and post-PUT GET response"

        # # Perform bad PUT request

        json_string = json.dumps({'configuration': put_data})
        json_string += ","

        response, json_string = execute_request(self.PATH, "PUT", json_string, self.SWITCH_IP, True)

        assert response.status == httplib.BAD_REQUEST, "PUT: Malformed JSON did not yield BAD_REQUEST: {0} {1}".format(response.status, response.reason)

        info("\n########## Finished executing PUT request on %s ##########\n" % self.PATH)

class Test_system:
    def setup (self):
        pass

    def teardown (self):
        pass

    def setup_class (cls):
        Test_system.test_var = systemTest()

    def teardown_class (cls):
        Test_system.test_var.net.stop()

    def setup_method (self, method):
        pass

    def teardown_method (self, method):
        pass

    def __del__ (self):
        del self.test_var

    def test_run (self):
        self.test_var.setup_switch_ip()
        self.test_var.call_system_get()
        self.test_var.call_system_options()
        self.test_var.call_system_put()

# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
TOPOLOGY = """
# +-------+     +---------+     +---------+     +-------+
# |       |     |         <----->         |     |       |
# |  hs1  <----->   sw1   |-----|   sw1   <----->  hs2  |
# |       |     |         <----->         |     |       |
# +-------+     +---------+     +---------+     +-------+
# Nodes
[type=openswitch name="Switch 1"] sw1
[type=openswitch name="Switch 2"] sw2
[type=host name="Host 1"] hs1
[type=host name="Host 2"] hs2
# Links
hs1:1 -- sw1:p1
hs2:1 -- sw2:q1
sw1:p2 -- sw2:q2
sw1:p3 -- sw2:q3
sw1:p4 -- sw2:q4
"""
# Global Variable
vlan_id = "900"
lag_id = "1"
"""
Author: Tamilmannan Harikrishnan - tamilmannan.h@hpe.com
testID: LAG FT Test
test name: DynamicLagModifyLowNumberOfMembers
test Description:  Tests that previously configured static Link Aggregation
                   can be modified to have between 0 and 2 members."""


def enable_interface(ops1, interface, step):
    step("ENABLE THE INTERFACE")
    with ops1.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.no_routing()
        ctx.no_shutdown()


def create_vlan(ops1, vlan_id, step):
    step("CONFIGURE THE VLAN")
    with ops1.libs.vtysh.ConfigVlan(vlan_id) as ctx:
        ctx.no_shutdown()


def assign_accessvlan(ops1, interface, vlan_id, step):
    step("CONFIG ACCESS VLANS ON INTERFACE")
    with ops1.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.vlan_access(vlan_id)


def config_lag(ops1, lag_id, step):
    step("CONFIGURE THE LAG INTERFACE")
    with ops1.libs.vtysh.ConfigInterfaceLag(lag_id) as ctx:
        ctx.no_routing()
        ctx.no_shutdown()


def lag_possitive_validation(ops1, lag_name, step):
    step("LAG POSSITIVE VALIDATION")
    status = ops1.libs.vtysh.show_lacp_aggregates()
    print(status)
    key = "lag" + str(lag_name)
    assert status[str(key)]['name'] == key


def config_active_lag(ops1, lag_id, step):
    step("CONFIGURE ACTIVE MODE TO THE LAG INTERFACE")
    with ops1.libs.vtysh.ConfigInterfaceLag(lag_id) as ctx:
        ctx.lacp_mode_active()


def config_lagoninterface(ops1, lag_id, interface, step):
    step("CONFIGURE LAG ON INTERFACE")
    with ops1.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.lag(lag_id)


def unconfig_lagoninterface(ops1, lag_id, interface, step):
    step("UNCONFIGURE LAG ON INTERFACE")
    with ops1.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.no_lag(lag_id)


def test_dynamiclagmodifylownumberofmembers(topology, step):
    step("TEST CASE DynamicLagModifyLowNumberOfMembers VALIDATION")
    sw1 = topology.get('sw1')
    sw2 = topology.get('sw2')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')
    assert sw1 is not None
    assert sw2 is not None
    assert hs1 is not None
    assert hs2 is not None
    p1 = sw1.ports['p1']
    p2 = sw1.ports['p2']
    p3 = sw1.ports['p3']
    p4 = sw1.ports['p4']
    q1 = sw2.ports['q1']
    q2 = sw2.ports['q2']
    q3 = sw2.ports['q3']
    q4 = sw2.ports['q4']
    enable_interface(sw1, p2, step)
    enable_interface(sw1, p3, step)
    enable_interface(sw1, p4, step)
    enable_interface(sw2, q2, step)
    enable_interface(sw2, q3, step)
    enable_interface(sw2, q4, step)
    config_lag(sw1, lag_id, step)
    config_active_lag(sw1, lag_id, step)
    config_lagoninterface(sw1, lag_id, p2, step)
    config_lagoninterface(sw1, lag_id, p3, step)
    config_lagoninterface(sw1, lag_id, p4, step)
    lag_possitive_validation(sw1, lag_id, step)
    config_lag(sw2, lag_id, step)
    config_active_lag(sw2, lag_id, step)
    config_lagoninterface(sw2, lag_id, q2, step)
    config_lagoninterface(sw2, lag_id, q3, step)
    config_lagoninterface(sw2, lag_id, q4, step)
    lag_possitive_validation(sw2, lag_id, step)
    create_vlan(sw1, vlan_id, step)
    enable_interface(sw1, p1, step)
    assign_accessvlan(sw1, p1, vlan_id, step)
    assign_accessvlan(sw1, "lag 1", vlan_id, step)
    create_vlan(sw2, vlan_id, step)
    enable_interface(sw2, q1, step)
    assign_accessvlan(sw2, q1, vlan_id, step)
    assign_accessvlan(sw2, "lag 1", vlan_id, step)
    hs1.libs.ip.interface('1', addr='192.168.1.10/24', up=True)
    hs2.libs.ip.interface('1', addr='192.168.1.11/24', up=True)
    ping = hs1.libs.ping.ping(1, "192.168.1.11")
    assert ping['transmitted'] == ping['received'] == 1
    unconfig_lagoninterface(sw1, lag_id, p2, step)
    unconfig_lagoninterface(sw2, lag_id, q2, step)
    ping = hs1.libs.ping.ping(1, "192.168.1.11")
    assert ping['transmitted'] == ping['received'] == 1
    config_lagoninterface(sw1, lag_id, p2, step)
    config_lagoninterface(sw2, lag_id, q2, step)
    ping = hs1.libs.ping.ping(1, "192.168.1.11")
    assert ping['transmitted'] == ping['received'] == 1
    unconfig_lagoninterface(sw1, lag_id, p2, step)
    unconfig_lagoninterface(sw1, lag_id, p3, step)
    unconfig_lagoninterface(sw1, lag_id, p4, step)
    unconfig_lagoninterface(sw2, lag_id, q2, step)
    unconfig_lagoninterface(sw2, lag_id, q3, step)
    unconfig_lagoninterface(sw2, lag_id, q4, step)
    ping = hs1.libs.ping.ping(1, "192.168.1.11")
    assert ping['transmitted'] == ping['received'] == 1
    config_lagoninterface(sw1, lag_id, p2, step)
    config_lagoninterface(sw1, lag_id, p3, step)
    config_lagoninterface(sw1, lag_id, p4, step)
    config_lagoninterface(sw2, lag_id, q2, step)
    config_lagoninterface(sw2, lag_id, q3, step)
    config_lagoninterface(sw2, lag_id, q4, step)
    ping = hs1.libs.ping.ping(1, "192.168.1.11")
    assert ping['transmitted'] == ping['received'] == 1
    unconfig_lagoninterface(sw1, lag_id, p3, step)
    unconfig_lagoninterface(sw1, lag_id, p4, step)
    unconfig_lagoninterface(sw2, lag_id, q3, step)
    unconfig_lagoninterface(sw2, lag_id, q4, step)
    ping = hs1.libs.ping.ping(1, "192.168.1.11")
    assert ping['transmitted'] == ping['received'] == 1
    config_lagoninterface(sw1, lag_id, p3, step)
    config_lagoninterface(sw1, lag_id, p4, step)
    config_lagoninterface(sw2, lag_id, q3, step)
    config_lagoninterface(sw2, lag_id, q4, step)
    ping = hs1.libs.ping.ping(1, "192.168.1.11")
    assert ping['transmitted'] == ping['received'] == 1

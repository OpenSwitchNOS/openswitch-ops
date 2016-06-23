# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016 Hewlett Packard Enterprise Development LP
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

"""
OpenSwitch Test for dynamic lag after removing one member in LAG

"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from time import sleep

TOPOLOGY = """
# +-------+     +--------+        +-------+       +-------+
# |       |     |        |<-----> |       |       |       |
# |  hs1  <---->|  ops1  |<-----> |  ops2 |<----->  hs2   |
# |       |     +--------+        +-------+       |       |
# +-------+                                       +-------+

# Nodes
[type=openswitch name="OpenSwitch 1"] ops1
[type=openswitch name="OpenSwitch 2"] ops2
[type=host name="Host 1"] hs1
[type=host name="Host 2"] hs2

# Links
hs1:1 -- ops1:p9
ops1:p1 -- ops2:p1
ops1:p2 -- ops2:p2
ops1:p3 -- ops2:p2
ops1:p4 -- ops2:p2
ops1:p5 -- ops2:p2
ops1:p6 -- ops2:p2
ops1:p7 -- ops2:p2
ops2:p9 -- hs2:1
"""

# Global Variable :

lag_id = "1"
vlan_id = "10"
hs1ip = "10.0.10.150"
hs2ip = "10.0.10.160"


def enable_interfaces(ops, interface, step):
    step("Enabling Interface " + interface)
    with ops.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.no_routing()
        ctx.no_shutdown()


def create_dynamic_lag(ops, lag_id, mode, step):
    step("Create static lag")
    with ops.libs.vtysh.ConfigInterfaceLag(lag_id) as ctx:
        ctx.no_shutdown()
        ctx.no_routing()
        if mode == "active":
            ctx.lacp_mode_active()
        else:
            ctx.lacp_mode_passive()


def config_lag_on_interface(ops, lag_id, interface, step):
    step("CONFIG LAG ON INTERFACE")
    with ops.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.lag(lag_id)


def create_vlan(ops, vlan_id, step):
    step("CONFIGURE THE VLAN")
    with ops.libs.vtysh.ConfigVlan(vlan_id) as ctx:
        ctx.no_shutdown()


def assign_accessvlan(ops, interface, vlan_id, step):
    step("CONFIG ACCESS VLANS ON INTERFACE")
    with ops.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.vlan_access(vlan_id)


def delete_lag_member(ops, interface, step):
    step("Delete one lag member" + interface)
    with ops.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.no_lag(lag_id)


def test_ft_lag_dynamic_lag_delete_max_number_of_members(topology, step):

    ops1 = topology.get('ops1')
    ops2 = topology.get('ops2')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')
    assert ops1 is not None
    assert ops2 is not None
    assert hs1 is not None
    assert hs2 is not None
    s1p1 = ops1.ports['p1']
    s1p2 = ops1.ports['p2']
    s1p3 = ops1.ports['p3']
    s1p4 = ops1.ports['p4']
    s1p5 = ops1.ports['p5']
    s1p6 = ops1.ports['p6']
    s1p7 = ops1.ports['p7']
    s1p8 = ops1.ports['p8']
    s1p9 = ops1.ports['p9']
    s2p1 = ops2.ports['p1']
    s2p2 = ops2.ports['p2']
    s2p3 = ops2.ports['p3']
    s2p4 = ops2.ports['p4']
    s2p5 = ops2.ports['p5']
    s2p6 = ops2.ports['p6']
    s2p7 = ops2.ports['p7']
    s2p8 = ops2.ports['p8']
    s2p9 = ops2.ports['p9']

    # Configure interfaces up
    enable_interfaces(ops1, s1p1, step)
    enable_interfaces(ops1, s1p2, step)
    enable_interfaces(ops1, s1p3, step)
    enable_interfaces(ops1, s1p4, step)
    enable_interfaces(ops1, s1p5, step)
    enable_interfaces(ops1, s1p6, step)
    enable_interfaces(ops1, s1p7, step)
    enable_interfaces(ops1, s1p8, step)
    enable_interfaces(ops1, s1p9, step)
    enable_interfaces(ops2, s2p1, step)
    enable_interfaces(ops2, s2p2, step)
    enable_interfaces(ops2, s2p3, step)
    enable_interfaces(ops2, s2p4, step)
    enable_interfaces(ops2, s2p5, step)
    enable_interfaces(ops2, s2p6, step)
    enable_interfaces(ops2, s2p7, step)
    enable_interfaces(ops2, s2p8, step)
    enable_interfaces(ops2, s2p9, step)

    # Create dynamic LAG :
    create_dynamic_lag(ops1, lag_id, "active", step)
    create_dynamic_lag(ops2, lag_id, "passive", step)

    # Assign interface to the lag created above.
    config_lag_on_interface(ops1, lag_id, s1p1, step)
    config_lag_on_interface(ops1, lag_id, s1p2, step)
    config_lag_on_interface(ops1, lag_id, s1p3, step)
    config_lag_on_interface(ops1, lag_id, s1p4, step)
    config_lag_on_interface(ops1, lag_id, s1p5, step)
    config_lag_on_interface(ops1, lag_id, s1p6, step)
    config_lag_on_interface(ops1, lag_id, s1p7, step)
    config_lag_on_interface(ops1, lag_id, s1p8, step)
    config_lag_on_interface(ops2, lag_id, s2p1, step)
    config_lag_on_interface(ops2, lag_id, s2p2, step)
    config_lag_on_interface(ops2, lag_id, s2p3, step)
    config_lag_on_interface(ops2, lag_id, s2p4, step)
    config_lag_on_interface(ops2, lag_id, s2p5, step)
    config_lag_on_interface(ops2, lag_id, s2p6, step)
    config_lag_on_interface(ops2, lag_id, s2p7, step)
    config_lag_on_interface(ops2, lag_id, s2p8, step)

    # Configure vlan and assign to interfaces
    create_vlan(ops1, vlan_id, step)
    assign_accessvlan(ops1, s1p9, vlan_id, step)
    assign_accessvlan(ops1, "lag 1", vlan_id, step)
    create_vlan(ops2, vlan_id, step)
    assign_accessvlan(ops2, s2p9, vlan_id, step)
    assign_accessvlan(ops2, "lag 1", vlan_id, step)
    sleep(5)

    # Bring up 2 hosts with IP configured :
    hs1.libs.ip.interface('1', addr=hs1ip, up=True)
    hs2.libs.ip.interface('1', addr=hs2ip, up=True)
    sleep(5)

    # Test ping
    # ping = hs1.libs.ping.ping(1, hs2ip)
    # assert ping['transmitted'] == ping['received'] == 1

    # Delete one member of the lag in both the switches
    delete_lag_member(ops1, s1p1, step)
    delete_lag_member(ops1, s1p2, step)
    delete_lag_member(ops1, s1p3, step)
    delete_lag_member(ops1, s1p4, step)
    delete_lag_member(ops1, s1p5, step)
    delete_lag_member(ops1, s1p6, step)
    delete_lag_member(ops1, s1p7, step)
    delete_lag_member(ops1, s1p8, step)
    delete_lag_member(ops2, s2p1, step)
    delete_lag_member(ops2, s2p2, step)
    delete_lag_member(ops2, s2p3, step)
    delete_lag_member(ops2, s2p4, step)
    delete_lag_member(ops2, s2p5, step)
    delete_lag_member(ops2, s2p6, step)
    delete_lag_member(ops2, s2p7, step)
    delete_lag_member(ops2, s2p8, step)
    sleep(5)

    # Test ping
    ping = hs1.libs.ping.ping(1, hs2ip)
    assert ping['transmitted'] == ping['received'] == 0

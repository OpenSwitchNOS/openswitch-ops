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
OpenSwitch Test for dynamic lag in alternative interface

"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from time import sleep

TOPOLOGY = """
# +-------+     +--------+        +-------+       +-------+
# |       |     |        |<-----> |       |       |       |
# |  hs1  <---->|  ops1  |<-----> |  ops2 |<------>  hs2  |
# |       |     +--------+        +-------+       |       |
# +-------+                                       +-------+

# Nodes
[type=openswitch name="OpenSwitch 1"] ops1
[type=openswitch name="OpenSwitch 2"] ops2
[type=host name="Host 1"] hs1
[type=host name="Host 2"] hs2

# Links
hs1:1 -- ops1:p2
ops1:p1 -- ops2:p1
ops1:p3 -- ops2:p3
ops2:p2 -- hs2:1
"""

# Global Variable :

lag_id = "1"
hs1ip = "10.0.10.150"
hs2ip = "10.0.10.160"


def test_staticnonconsecutiveinterfaces(topology):

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
    s2p1 = ops2.ports['p1']
    s2p2 = ops2.ports['p2']
    s2p3 = ops2.ports['p3']

    # Configure interfaces up
    with ops1.libs.vtysh.ConfigInterface(s1p1) as ctx:
        ctx.no_routing()
        ctx.no_shutdown()
    with ops1.libs.vtysh.ConfigInterface(s1p2) as ctx:
        ctx.no_routing()
        ctx.no_shutdown()
    with ops1.libs.vtysh.ConfigInterface(s1p3) as ctx:
        ctx.no_routing()
        ctx.no_shutdown()
    with ops2.libs.vtysh.ConfigInterface(s2p1) as ctx:
        ctx.no_routing()
        ctx.no_shutdown()
    with ops2.libs.vtysh.ConfigInterface(s2p2) as ctx:
        ctx.no_routing()
        ctx.no_shutdown()
    with ops2.libs.vtysh.ConfigInterface(s2p3) as ctx:
        ctx.no_routing()
        ctx.no_shutdown()

    # Create Dynamic LAG :
    with ops1.libs.vtysh.ConfigInterfaceLag(lag_id) as ctx:
        ctx.no_shutdown()
        ctx.no_routing()
    with ops2.libs.vtysh.ConfigInterfaceLag(lag_id) as ctx:
        ctx.no_shutdown()
        ctx.no_routing()

    # Assign alternative interface to the lag created above.
    with ops1.libs.vtysh.ConfigInterface(s1p1) as ctx:
        ctx.lag(lag_id)
    with ops1.libs.vtysh.ConfigInterface(s1p3) as ctx:
        ctx.lag(lag_id)
    with ops2.libs.vtysh.ConfigInterface(s2p1) as ctx:
        ctx.lag(lag_id)
    with ops2.libs.vtysh.ConfigInterface(s2p3) as ctx:
        ctx.lag(lag_id)

    # Configure vlan and switch interfaces
    with ops1.libs.vtysh.ConfigVlan('10') as ctx:
        ctx.no_shutdown()
    with ops2.libs.vtysh.ConfigVlan('10') as ctx:
        ctx.no_shutdown()
    with ops1.libs.vtysh.ConfigInterface(s1p2) as ctx:
        ctx.vlan_access('10')
    with ops2.libs.vtysh.ConfigInterface(s2p2) as ctx:
        ctx.vlan_access('10')
    with ops1.libs.vtysh.ConfigInterfaceLag(lag_id) as ctx:
        ctx.vlan_access('10')
    with ops2.libs.vtysh.ConfigInterfaceLag(lag_id) as ctx:
        ctx.vlan_access('10')
    sleep(20)
    # Bring up 2 hosts with IP configured :
    hs1.libs.ip.interface('1', addr=hs1ip, up=True)
    hs2.libs.ip.interface('1', addr=hs2ip, up=True)
    sleep(20)
    # Test ping
    ping = hs1.libs.ping.ping(1, hs2ip)
    assert ping['transmitted'] == ping['received'] == 1
    # Shut one of the interface , to verify if ping stil passes
    with ops1.libs.vtysh.ConfigInterface(s1p1) as ctx:
        ctx.shutdown()
    with ops2.libs.vtysh.ConfigInterface(s2p1) as ctx:
        ctx.shutdown()
    sleep(20)
    # Test ping
    ping = hs1.libs.ping.ping(1, hs2ip)
    assert ping['transmitted'] == ping['received'] == 1

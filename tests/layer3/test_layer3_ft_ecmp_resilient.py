
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
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
OpenSwitch Test for ECMP Resilient Hash
"""

from pytest import mark
# from pytest import set_trace
from time import sleep
from re import match


TOPOLOGY = """
#                             +-------+
#                             |       |
#                    +-------->  nh1  |
#                    |        |       |
#                    |        +-------+
#                    |
# +-------+          |        +-------+
# |       |     +----v--+     |       |
# |  hs1  <----->  sw1  <----->  nh2  |
# |       |     +----^--+     |       |
# +-------+          |        +-------+
#                    |
#                    |        +-------+
#                    |        |       |
#                    +-------->  nh3  |
#                             |       |
#                             +-------+

# Nodes
[type=openswitch name="Switch 1"] sw1
[type=host name="Host 1"] hs1
[type=host name="Nexthop 1"] nh1
[type=host name="Nexthop 2"] nh2
[type=host name="Nexthop 3"] nh3

# Links
sw1:1 -- nh1:1
sw1:2 -- nh2:1
sw1:3 -- nh3:1
sw1:4 -- hs1:1
"""

PING_DEST_RE = (
    r'^From (?P<source>[0-9a-f.:]+) icmp_seq=\d+ .+$'
)


@mark.test_id(10000)
def test_ecmp(topology):
    """
    Set network addresses and static routes between a host, switch, and 3
    hosts acting as next hops. Use the response from ping to ensure flows
    not disrupted when a next hop is removed or added
    """
    sw1 = topology.get('sw1')
    hs1 = topology.get('hs1')
    nh1 = topology.get('nh1')
    nh2 = topology.get('nh2')
    nh3 = topology.get('nh3')

    assert sw1 is not None
    assert hs1 is not None
    assert nh1 is not None
    assert nh2 is not None
    assert nh3 is not None

    ps1hs1 = sw1.ports['4']
    ps1nh1 = sw1.ports['1']
    ps1nh2 = sw1.ports['2']
    ps1nh3 = sw1.ports['3']
    phs1 = hs1.ports['1']
    pnh1 = nh1.ports['1']
    pnh2 = nh2.ports['1']
    pnh3 = nh3.ports['1']

    # Configure IP and bring UP host 1 interfaces
    hs1.libs.ip.interface(phs1, addr='20.0.0.10/24', up=True)

    # Configure IP and bring UP nexthop 1 interfaces
    nh1.libs.ip.interface(pnh1, addr='1.0.0.1/24', up=True)

    # Configure IP and bring UP nexthop 2 interfaces
    nh2.libs.ip.interface(pnh2, addr='2.0.0.1/24', up=True)

    # Configure IP and bring UP nexthop 3 interfaces
    nh3.libs.ip.interface(pnh3, addr='3.0.0.1/24', up=True)

    # Configure IP and bring UP switch 1 interfaces
    # sw1 <-> hs1
    with sw1.libs.vtysh.ConfigInterface(ps1hs1) as ctx:
        ctx.ip_address('20.0.0.1/24')
        ctx.no_shutdown()

    # sw1 <-> nh1
    with sw1.libs.vtysh.ConfigInterface(ps1nh1) as ctx:
        ctx.ip_address('1.0.0.2/24')
        ctx.no_shutdown()

    # sw1 <-> nh2
    with sw1.libs.vtysh.ConfigInterface(ps1nh2) as ctx:
        ctx.ip_address('2.0.0.2/24')
        ctx.no_shutdown()

    # sw1 <-> nh3
    with sw1.libs.vtysh.ConfigInterface(ps1nh3) as ctx:
        ctx.ip_address('3.0.0.2/24')
        ctx.no_shutdown()

    # now wait for interfaces to come up
    show_int1 = ''
    show_int2 = ''
    show_int3 = ''
    show_int4 = ''
    attempts = 10
    while (
      ("Interface {ps1hs1} is up".format(**locals()) not in show_int1) and
      ("Interface {ps1hs1} is up".format(**locals()) not in show_int2) and
      ("Interface {ps1hs1} is up".format(**locals()) not in show_int3) and
      ("Interface {ps1hs1} is up".format(**locals()) not in show_int4) and
      attempts > 0):
        sleep(2)
        show_int1 = sw1('show interface {ps1hs1}'.format(**locals()))
        show_int2 = sw1('show interface {ps1nh1}'.format(**locals()))
        show_int3 = sw1('show interface {ps1nh2}'.format(**locals()))
        show_int4 = sw1('show interface {ps1nh3}'.format(**locals()))
        attempts = attempts + 1

    # Set ECMP static routes in switch
    with sw1.libs.vtysh.Configure() as ctx:
        ctx.ip_route('70.0.0.0/24', '1.0.0.1')
        ctx.ip_route('70.0.0.0/24', '2.0.0.1')
        ctx.ip_route('70.0.0.0/24', '3.0.0.1')

    # Set gateway in host
    hs1.libs.ip.add_route('default', '20.0.0.1')

    # Next hops need a route back to the hs1 for the icmp replies
    nh1.libs.ip.add_route('20.0.0.0/24', '1.0.0.2')
    nh2.libs.ip.add_route('20.0.0.0/24', '2.0.0.2')
    nh3.libs.ip.add_route('20.0.0.0/24', '3.0.0.2')

    # What we SHOULD do here is get multiple pings going in parallel
    # then drop a link and ensure flows to remaining next hops don't get
    # redistributed but that is too hard in this framework right now, and
    # is likely better off as part of a stress test
    next_hops = []
    for dest in ('70.0.0.1', '70.0.0.2', '70.0.0.3', '70.0.0.4', '70.0.0.5'):
        responding_next_hop = None
        ping_raw = hs1('ping -c 5 {0}'.format(dest))
        for line in ping_raw.splitlines():
            m = match(PING_DEST_RE, line)
            if m:
                if responding_next_hop is None:
                    responding_next_hop = m.group('source')
                    next_hops.append(responding_next_hop)
                else:
                    assert m.group('source') == responding_next_hop

        # Take down one of the next hops
        nh1.libs.ip.interface(pnh1, up=False)
        if responding_next_hop == '1.0.0.1':
            responding_next_hop = None

        # If Resilient ECMP is working, the ping flow shouldn't shift
        ping_raw = hs1('ping -c 5 {0}'.format(dest))
        for line in ping_raw.splitlines():
            m = match(PING_DEST_RE, line)
            if m:
                if responding_next_hop is None:
                    responding_next_hop = m.group('source')
                    next_hops.append(responding_next_hop)
                else:
                    assert m.group('source') == responding_next_hop
        nh1.libs.ip.interface(pnh1, up=True)

    # Make sure we hit each of the next hops
    assert '1.0.0.1' in next_hops
    assert '2.0.0.1' in next_hops
    assert '3.0.0.1' in next_hops

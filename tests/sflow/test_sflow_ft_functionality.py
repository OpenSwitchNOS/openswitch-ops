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
OpenSwitch Test for sFlow functionality.
"""

import time
import pytest


TOPOLOGY = """
#                    +----------------+
#                    |                |
#                    |   Host 3       |
#                    |  (sflowtool)   |
#                    |                |
#                    +-+--------------+
#                      |
#                      |
#         +------------+--+
#         |               |
#         |               |
#         |    Open       |
#         |    Switch     |
#         |               |
#         |               |
#         +-+----------+--+
#           |          |
#           |          |
#+----------+--+     +-+------------+
#|             |     |              |
#|             |     |              |
#|  Host 1     |     |  Host 2      |
#|             |     |              |
#+-------------+     +--------------+

# Nodes
[type=openswitch name="OpenSwitch 1"] ops1
[type=host name="Host 1"] hs1
[type=host name="Host 2"] hs2
[type=host name="Host 3" image="openswitch/sflowtool:latest"] hs3

# Links
hs1:1 -- ops1:1
hs2:1 -- ops1:2
hs3:1 -- ops1:3
"""


@pytest.mark.skipif(True, reason="Waiting for new framework integration")
def test_sflow_ft_functionality(topology, step):
    """
    Test sflow enable/disable.
    Test sampling of following types of packets:
        1. CPU destined traffic
        2. Routed packets (L3)
        3. Switched packets (L2)
    """
    ops1 = topology.get('ops1')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')
    hs3 = topology.get('hs3')

    assert ops1 is not None
    assert hs1 is not None
    assert hs2 is not None
    assert hs3 is not None

    ping_count = 200
    ping_interval = 0.02
    sampling_rate = 20
    vlan = '10'

    # We expect at least 70% of packets to be sampled and seen by the collector
    # Multiplier of 2 to account for ingress and egress rates
    # TODO : Need to bump up the expected samples to 80%
    expected_samples = int(2 * ping_count/sampling_rate * (70/100))

    # Configure host interfaces
    step("### Configuring host interfaces ###")
    hs1.libs.ip.interface('1', addr='10.10.10.2/24', up=True)
    hs2.libs.ip.interface('1', addr='10.10.11.2/24', up=True)
    hs3.libs.ip.interface('1', addr='10.10.12.2/24', up=True)

    # Add routes on hosts
    step("### Adding routes on hosts ###")
    hs1.libs.ip.add_route('10.10.11.0/24', '10.10.10.1')
    hs2.libs.ip.add_route('10.10.10.0/24', '10.10.11.1')

    # Configure interfaces on the switch
    step("Configuring interface 1 of switch")
    with ops1.libs.vtysh.ConfigInterface('1') as ctx:
        ctx.ip_address('10.10.10.1/24')
        ctx.no_shutdown()

    step("Configuring interface 2 of switch")
    with ops1.libs.vtysh.ConfigInterface('2') as ctx:
        ctx.ip_address('10.10.11.1/24')
        ctx.no_shutdown()

    step("Configuring interface 3 of switch")
    with ops1.libs.vtysh.ConfigInterface('3') as ctx:
        ctx.ip_address('10.10.12.1/24')
        ctx.no_shutdown()

    # Need to remove below lines after bug fix
    assert not ops1("ovs-appctl -t ops-switchd vlog/set sim_plugin:syslog:dbg",
                    shell="bash")
    assert not ops1("ovs-appctl -t ops-switchd vlog/set "
                    "ofproto_provider_sim:syslog:dbg", shell="bash")
    assert not ops1("ovs-appctl -t ops-switchd vlog/set netdev_sim:syslog:dbg",
                    shell="bash")

    # Configure sFlow
    step("### Configuring sFlow ###")
    with ops1.libs.vtysh.Configure() as ctx:
        ctx.sflow_enable()
        ctx.sflow_sampling(sampling_rate)
        ctx.sflow_agent_interface('3')
        ctx.sflow_collector('10.10.12.2')

    # Write library after CLI is finalized
    ops1('show sflow')

    # Start sflowtool
    hs3.libs.sflow.sflowtool_start(mode='line')

    # Generate CPU destined traffic
    step("### Checking CPU destined traffic ###")
    ping = hs1.libs.ping.ping(ping_count, '10.10.10.1', ping_interval)
    step("Ping transmitted: " + str(ping['transmitted']))
    step("Ping received: " + str(ping['received']))

    # TODO : Remove sleeps
    time.sleep(15)

    # Stop sflowtool
    result = hs3.libs.sflow.sflowtool_stop()
    step("Expected samples: " + str(expected_samples))
    step("Flow count: " + str(result['flow_count']))
    assert result['flow_count'] >= expected_samples

    # Generate L3 traffic
    step("### Checking Routed traffic (L3) ###")
    hs3.libs.sflow.sflowtool_start(mode='line')

    ping = hs1.libs.ping.ping(ping_count, '10.10.11.2', ping_interval)

    time.sleep(15)

    result = hs3.libs.sflow.sflowtool_stop()
    assert result['flow_count'] >= expected_samples

    step("### Disabling sFlow ###")
    with ops1.libs.vtysh.Configure() as ctx:
        ctx.no_sflow_enable()

    # Check sampling when sFlow is disabled
    step("### Checking Routed traffic (L3) on disable ###")
    hs3.libs.sflow.sflowtool_start(mode='line')

    ping = hs1.libs.ping.ping(ping_count, '10.10.11.2', ping_interval)

    result = hs3.libs.sflow.sflowtool_stop()
    assert result['flow_count'] == 0 and result['sample_count'] == 0

    # Enable sFlow again
    step("### Enabling sFlow again ###")
    with ops1.libs.vtysh.Configure() as ctx:
        ctx.sflow_enable()

    # Configure VLAN on switch
    step("### Configuring vlan ###")
    with ops1.libs.vtysh.ConfigVlan(vlan) as ctx:
        ctx.no_shutdown()

    # Configure switch interfaces connected to hosts to be part of VLAN
    step("### Configuring interfaces 1 & 2 to be "
         "part of vlan in access mode ###")
    with ops1.libs.vtysh.ConfigInterface('1') as ctx:
        ctx.no_routing()
        ctx.vlan_access(vlan)

    with ops1.libs.vtysh.ConfigInterface('2') as ctx:
        ctx.no_routing()
        ctx.vlan_access(vlan)

    ops1('show vlan')

    # Change IP of Host 2 to same subnet as Host 1
    step("### Re-assigning IP to Host 2 to be on same subnet as Host 1 ###")
    hs2.libs.ip.remove_ip('1', addr='10.10.11.2/24')
    hs2.libs.ip.interface('1', addr='10.10.10.3/24', up=True)

    # Generate L2 traffic
    step("### Checking Switched traffic (L2) ###")
    hs3.libs.sflow.sflowtool_start(mode='line')

    ping = hs1.libs.ping.ping(ping_count, '10.10.10.3', ping_interval)

    time.sleep(15)

    result = hs3.libs.sflow.sflowtool_stop()
    assert result['flow_count'] >= expected_samples

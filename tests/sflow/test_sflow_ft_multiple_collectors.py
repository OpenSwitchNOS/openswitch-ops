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
OpenSwitch Test for sFlow feature with multiple collectors.
"""

import time
import pytest


TOPOLOGY = """
#+----------------+      +----------------+
#|                |      |                |
#|    Host-4      |      |    Host-3      |
#|  (sflowtool-3) |      |  (sflowtool-2) |
#|                |      |                |
#+--------------+-+      +-+--------------+
#               |          |
#               |          |
#             +-+----------+--+
#             |               |
#             |               |
#             |    Switch     |
#             |               |
#             |               |
#             |               |
#             +-+----------+--+
#               |          |
#               |          |
#       +-------+--+     +-+--------------+
#       |          |     |                |
#       |          |     |    Host-2      |
#       | Host-1   |     |  (sflowtool-1) |
#       |          |     |                |
#       +----------+     +----------------+

# Nodes
[type=openswitch name="OpenSwitch 1"] ops1
[type=host name="Host 1"] hs1
[type=host name="Host 2" image="openswitch/sflowtool:latest"] hs2
[type=host name="Host 3" image="openswitch/sflowtool:latest"] hs3
[type=host name="Host 4" image="openswitch/sflowtool:latest"] hs4

# Links
hs1:1 -- ops1:1
hs2:1 -- ops1:2
hs3:1 -- ops1:3
hs4:1 -- ops1:4
"""


@pytest.mark.skipif(True, reason="Waiting for new framework integration")
def test_sflow_ft_multiple_collectors(topology, step):
    """
    Test sflow is able to send packets to multiple collectors
    """
    ops1 = topology.get('ops1')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')
    hs3 = topology.get('hs3')
    hs4 = topology.get('hs4')

    assert ops1 is not None
    assert hs1 is not None
    assert hs2 is not None
    assert hs3 is not None
    assert hs4 is not None

    ping_count = 200
    ping_interval = 0.02
    sampling_rate = 20

    # We expect at least 70% of packets to be sampled and seen by the collector
    # Multiplier of 2 to account for ingress and egress rates
    # TODO : Need to bump up the expected samples to 80%
    expected_samples = int(2 * ping_count/sampling_rate * (70/100))

    # Configure host interfaces
    step("### Configuring host interfaces ###")
    hs1.libs.ip.interface('1', addr='10.10.10.2/24', up=True)
    hs2.libs.ip.interface('1', addr='10.10.11.2/24', up=True)
    hs3.libs.ip.interface('1', addr='10.10.12.2/24', up=True)
    hs4.libs.ip.interface('1', addr='10.10.13.2/24', up=True)

    # Configure interfaces on the switch
    step("Configuring interfaces of the switch")
    with ops1.libs.vtysh.ConfigInterface('1') as ctx:
        ctx.ip_address('10.10.10.1/24')
        ctx.no_shutdown()

    with ops1.libs.vtysh.ConfigInterface('2') as ctx:
        ctx.ip_address('10.10.11.1/24')
        ctx.no_shutdown()

    with ops1.libs.vtysh.ConfigInterface('3') as ctx:
        ctx.ip_address('10.10.12.1/24')
        ctx.no_shutdown()

    with ops1.libs.vtysh.ConfigInterface('4') as ctx:
        ctx.ip_address('10.10.13.1/24')
        ctx.no_shutdown()

    with ops1.libs.vtysh.ConfigInterface('5') as ctx:
        ctx.ip_address('100.10.25.1/24')
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
        ctx.sflow_agent_interface('5')
        ctx.sflow_collector('10.10.11.2')
        ctx.sflow_collector('10.10.12.2')
        ctx.sflow_collector('10.10.13.2')

    # Write library after CLI is finalized
    ops1('show sflow')

    # Start sflowtool
    hs2.libs.sflow.sflowtool_start(mode='line')
    hs3.libs.sflow.sflowtool_start(mode='line')
    hs4.libs.sflow.sflowtool_start(mode='line')

    # Generate CPU destined traffic
    step("### Checking CPU destined traffic ###")
    ping = hs1.libs.ping.ping(ping_count, '10.10.10.1', ping_interval)
    step("Ping transmitted: " + str(ping['transmitted']))
    step("Ping received: " + str(ping['received']))

    time.sleep(15)

    # Stop sflowtool on Hosts
    result_hs2 = hs2.libs.sflow.sflowtool_stop()
    result_hs3 = hs3.libs.sflow.sflowtool_stop()
    result_hs4 = hs4.libs.sflow.sflowtool_stop()

    step("Flow count hs2: " + str(result_hs2['flow_count']))
    step("Flow count hs3: " + str(result_hs3['flow_count']))
    step("Flow count hs4: " + str(result_hs4['flow_count']))

    assert result_hs2['flow_count'] >= expected_samples
    assert result_hs3['flow_count'] >= expected_samples
    assert result_hs4['flow_count'] >= expected_samples

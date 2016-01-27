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
OpenSwitch Test for sFlow agent interface ip.
"""

import time

TOPOLOGY = """
#                    +----------------+
#                    |                |
#                    |   Host 2       |
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
#         +-+-------------+
#           |
#           |
#+----------+--+
#|             |
#|             |
#|  Host 1     |
#|             |
#+-------------+

# Nodes
[type=openswitch name="OpenSwitch 1" image="openswitch/sflow2:latest"] ops1
[type=host name="Host 1"] hs1
[type=host name="Host 2" image="openswitch/sflowtool:latest"] hs2

# Links
hs1:1 -- ops1:1
hs2:1 -- ops1:2
"""


def test_sflow_agent_interface(topology, step):
    """
    Tests agent interface ip.
    """
    ops1 = topology.get('ops1')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')

    assert ops1 is not None
    assert hs1 is not None
    assert hs2 is not None

    ping_count = 100
    ping_interval = 0.02
    sampling_rate = 20

    # Configure host interfaces
    step("### Configuring host interfaces ###")
    hs1.libs.ip.interface('1', addr='10.10.10.2/24', up=True)
    hs2.libs.ip.interface('1', addr='10.10.11.2/24', up=True)

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
        ctx.sflow_agent_interface('1')
        ctx.sflow_collector('10.10.11.2')

    # Write library after CLI is finalized
    ops1('show sflow')

    # Start sflowtool
    hs2.libs.sflow.sflowtool_start(mode='line')

    # Generate CPU destined traffic
    hs1.libs.ping.ping(ping_count, '10.10.10.1', ping_interval)

    # Stop sflowtool
    result = hs2.libs.sflow.sflowtool_stop()

    # Checking agent interface ip for interface 1 in FLOW
    for x in range(0, len(result['packets'])):
        if str(result['packets'][x]['packet_type']) == 'FLOW':
            break
    assert str(result['packets'][x]['agent_address']) == "10.10.10.1"

    # Configure sFlow agent interface
    step("### Configuring sFlow ###")
    with ops1.libs.vtysh.Configure() as ctx:
        ctx.sflow_agent_interface('3')

    # Write library after CLI is finalized
    ops1('show sflow')

    # Start sflowtool
    hs2.libs.sflow.sflowtool_start(mode='line')

    step("### Sleeping to allow interface flow packets to be sent ###")
    time.sleep(15)

    # Generate CPU destined traffic
    hs1.libs.ping.ping(ping_count, '10.10.10.1', ping_interval)

    # Stop sflowtool
    result = hs2.libs.sflow.sflowtool_stop()

    # Checking agent interface ip for interface 3 in FLOW
    for x in range(0, len(result['packets'])):
        if str(result['packets'][x]['packet_type']) == 'FLOW':
            break
    assert str(result['packets'][x]['agent_address']) == "10.10.12.1"

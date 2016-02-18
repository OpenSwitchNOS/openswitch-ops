# -*- coding: utf-8 -*-
#
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

"""
OpenSwitch Test for LACPD heartbeat configurations.
"""

from pytest import mark
from re import compile
from time import sleep

TOPOLOGY = """
# +-------+                                  +-------+
# |       |    +--------+  LAG  +--------+   |       |
# |  hs1  <---->  ops1  <------->  ops2  <--->  hs2  |
# |       |    |   A    <------->    P   |   |       |
# +-------+    |        <------->        |   +-------+
#              +--------+       +--------+

# Nodes
[type=openswitch name="OpenSwitch 1 LAG active"] ops1
[type=openswitch name="OpenSwitch 2 LAG passive"] ops2
[type=host name="Host 1"] hs1
[type=host name="Host 2"] hs2

# Links
hs1:1 -- ops1:4
ops1:1 -- ops2:1
ops1:2 -- ops2:2
ops1:3 -- ops2:3
hs2:1 -- ops2:4
"""


def switch_create_vlan(obj_switch, vid):
    """
    Creates a VLAN
    """
    with obj_switch.libs.vtysh.ConfigVlan(vid) as ctx:
        ctx.no_shutdown()


def switch_add_interface_to_vlan(obj_switch, n_if, vid):
    """
    Adds an interface to a VLAN
    """
    with obj_switch.libs.vtysh.ConfigInterface(n_if) as ctx:
        ctx.no_routing()
        ctx.no_shutdown()
        ctx.vlan_access(vid)


def switch_create_lag(obj_switch, n_lag, vid=None, lacp_mode=None):
    """
    Creates a LAG and optionally sets vlan and lacp mode
    """
    with obj_switch.libs.vtysh.ConfigInterfaceLag(n_lag) as ctx:
        ctx.no_routing()
        if vid:
            ctx.vlan_access(vid)
        if lacp_mode:
            if lacp_mode.lower() == 'active':
                ctx.lacp_mode_active()
            elif lacp_mode.lower() == 'passive':
                ctx.lacp_mode_passive()


def switch_add_interface_to_lag(obj_switch, n_if, n_lag):
    """
    Adds an interface to a LAG
    """
    with obj_switch.libs.vtysh.ConfigInterface(n_if) as ctx:
        ctx.no_shutdown()
        ctx.lag(n_lag)


def switch_config_lacp_rate(obj_switch, n_lag, lacp_rate='slow'):
    """
    Sets lacp rate (slow|fast), default value is slow
    """
    with obj_switch.libs.vtysh.ConfigInterfaceLag(n_lag) as ctx:
        if lacp_rate.lower() == 'slow':
            ctx.no_lacp_rate_fast()
        elif lacp_rate.lower() == 'fast':
            ctx.lacp_rate_fast()


def switch_get_interfaces(obj_switch):
    """
    Gets switch interfaces and return a dictionary indexed
    by interface number and mac address
    """
    res_ifs = {'index': {}, 'mac_addr': {}}
    # Get interfaces (up and running)
    cmd_output = obj_switch(
        'tcpdump -D | grep "Up, Running" | cut -d " " -f 1',
        shell='bash_swns'
    )
    # Filter interfaces to get name and index
    res = compile(r'(\d+)[.](\S+)')
    up_interfaces = res.findall(cmd_output)

    # Get corresponding index and mac address for each interface
    for up_if in up_interfaces:
        res_ifs['index'][up_if[1]] = up_if[0]
        # Get mac address with bash commands
        mac_addr = obj_switch(
            'ip addr show dev {up_if[1]} | grep link/ether '
            .format(**locals()) +
            '| awk \'{print $2}\'',
            shell='bash_swns')
        res_ifs['mac_addr'][up_if[1]] = mac_addr

    return res_ifs


def switch_capture_packets_start(obj_switch, interface, t_filter=None):
    """
    Starts tcpdump process and returns its PID
    """
    tcpdump_command = 'tcpdump -vv -i {interface} '.format(**locals())
    if t_filter:
        tcpdump_command += '{t_filter}'.format(**locals())
    tcpdump_command += ' > /tmp/ops_{interface}.cap 2>&1 &'.format(**locals())
    cmd_output = obj_switch(
        tcpdump_command,
        shell='bash_swns'
    )

    res = compile(r'\[\d+\] (\d+)')
    res_pid = res.findall(cmd_output)

    if len(res_pid) == 1:
        tcpdump_pid = int(res_pid[0])
    else:
        tcpdump_pid = -1

    return tcpdump_pid


def switch_capture_packets_stop(obj_switch, interface, tcpdump_pid):
    """
    Stops tcpdump process and return results
    tcpdump needs to be killed
    """
    final_result = {}
    cmd_output = obj_switch(
        'kill {tcpdump_pid}'.format(**locals()),
        shell='bash_swns'
    )

    sleep(1)
    # This is to avoid the 'Done' message after killing tcpdump
    cmd_output = obj_switch(
        'ls', shell='bash_swns'
    )
    # Create counters array
    for td_counter in ['captured', 'received', 'dropped']:
        cap_text = obj_switch(
            'grep {td_counter} /tmp/ops_{interface}.cap'
            .format(**locals()),
            shell='bash_swns'
        )

        res = compile('\d+')
        format_res = res.findall(cap_text)
        assert len(format_res) == 1
        final_result[td_counter] = int(format_res[0])

    return final_result


@mark.test_id(108)
@mark.timeout(540)
def test_lacpd_heartbeat(topology):
    """
    Tests LACP heartbeat average rate (slow/fast)
    """

    # VID for testing
    test_vlan = 256
    # LAG ID for testing
    test_lag = 2
    # number of pings
    num_ping = 5
    # seconds for tcpdump capture
    wait_time = 90
    # interfaces to be added to LAG
    lag_interfaces = ['1', '2', '3']
    # interface connected to host
    host_interface = '4'
    # List of interface indexes (as tcpdump -D sees them) and mac address
    lag_interfaces_idx = {'index': {}, 'mac_addr': {}}
    # List of tcpdump PIDs for each interface
    tcpdump_pids = {}
    # List of tcpdump counters (captured, received, dropped)
    tcpdump_counters = {}
    # heart beats packets per second depending on rate
    hb_per_sec = {False: (1/30), True: 1}

    ops1 = topology.get('ops1')
    ops2 = topology.get('ops2')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')

    assert ops1 is not None
    assert ops2 is not None
    assert hs1 is not None
    assert hs2 is not None

    # Configure switches
    # ----------------------------------
    # Create vlans
    for curr_ops in [ops1, ops2]:
        switch_create_vlan(curr_ops, test_vlan)

    # Create and configure lags
    # ops1 lacp mode active
    switch_create_lag(ops1, test_lag, test_vlan, 'active')
    # ops2 lacp mode passive
    switch_create_lag(ops2, test_lag, test_vlan, 'passive')

    for curr_ops in [ops1, ops2]:
        # Mark interfaces as enabled
        for curr_p in lag_interfaces + [host_interface]:
            px = curr_ops.ports[curr_p]
            assert not curr_ops(
                'set interface {px} user_config:admin=up'.
                format(**locals()),
                shell='vsctl'
            )

        # Add interfaces to LAG
        for curr_if in lag_interfaces:
            switch_add_interface_to_lag(curr_ops, curr_if, test_lag)
        # Interface 4 is connected to one host
        switch_add_interface_to_vlan(curr_ops, host_interface, test_vlan)

    # Configure host interfaces
    hs1.libs.ip.interface('1', addr='10.0.11.10/24', up=True)
    hs2.libs.ip.interface('1', addr='10.0.11.11/24', up=True)
    # Wait few seconds to wait everything is up
    sleep(30)

    # Pinging to verify connections are OK
    ping = hs1.libs.ping.ping(num_ping, '10.0.11.11')
    assert ping['transmitted'] == ping['received'] == num_ping
    ping = hs2.libs.ping.ping(num_ping, '10.0.11.10')
    assert ping['transmitted'] == ping['received'] == num_ping

    # Test for rates slow and fast
    for is_fast_rate in [False, True]:
        heartbeats = (wait_time * hb_per_sec[is_fast_rate])
        # Setting values for slow|fast
        if is_fast_rate:
            print('Test LAG with fast rate')
            for c_sw in [ops1, ops2]:
                switch_config_lacp_rate(c_sw, test_lag, 'fast')
        else:
            print('Test LAG with slow rate')
            # Configuration for slow rate should not appear here because
            # is default value, but it's necessary if test starts with
            # fast rate
            for c_sw in [ops1, ops2]:
                switch_config_lacp_rate(c_sw, test_lag, 'slow')

        for curr_ops in [ops1, ops2]:
            # Get switch interfaces (as seen by tcpdump -D)
            lag_interfaces_idx = switch_get_interfaces(curr_ops)
            # Listen with tcpdump for each interface
            for lag_if in lag_interfaces:
                curr_if = lag_interfaces_idx['index'][lag_if]
                curr_mac = lag_interfaces_idx['mac_addr'][lag_if]
                # Start capturing packets
                p_id = switch_capture_packets_start(
                    curr_ops,
                    curr_if,
                    '-e ether src {curr_mac}'.format(**locals()))

                assert p_id > 0

                tcpdump_pids[curr_if] = p_id

            # Wait for tcpdump finished capturing packets
            sleep(wait_time)

            for lag_if in lag_interfaces:
                # Get index for interface
                curr_if = lag_interfaces_idx['index'][lag_if]
                p_id = tcpdump_pids[curr_if]

                tcpdump_counters = switch_capture_packets_stop(
                    curr_ops, curr_if, p_id)

                final_result = tcpdump_counters['received']

                assert (final_result / heartbeats) >= 0.9 and\
                    (final_result / heartbeats) <= 1

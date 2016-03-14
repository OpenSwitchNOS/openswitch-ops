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
OpenSwitch Test for LAG load Balancing.

Testing with l2-src-dst, l3-src-dst and l4-src-dst hash algorithms.
The purpose is to try with these algorithms, traffic must be transmitted
in both LAG interfaces.
"""

from pytest import mark
from re import compile
from time import sleep

from lacp_lib import create_lag
from lacp_lib import create_vlan
from lacp_lib import associate_interface_to_lag
from lacp_lib import associate_vlan_to_lag
from lacp_lib import associate_vlan_to_l2_interface
from lacp_lib import set_lag_lb_hash
from lacp_lib import check_lag_lb_hash
from lacp_lib import check_connectivity_between_hosts
from lacp_lib import turn_on_interface
from lacp_lib import validate_turn_on_interfaces

TOPOLOGY = """
# +-------+                                   +-------+
# |       |    +--------+  LAG  +--------+    |       |
# |  hs1  <---->        <------->        <---->  hs2  |
# |       |    |  ops1  <------->  ops2  |    |       |
# +-------+    |        |       |        <-+  +-------+
#              +--------+       +--------+ |
#                                          |  +-------+
#                                          |  |       |
#                                          +-->  hs3  |
#                                             |       |
#                                             +-------+

# Nodes
[type=openswitch name="OpenSwitch 1"] ops1
[type=openswitch name="OpenSwitch 2"] ops2
[type=host name="Host src 1"] hs1
[type=host name="Host dst 2"] hs2
[type=host name="Host dst 3"] hs3

# Links
hs1:1 -- ops1:1
hs2:1 -- ops2:1
hs3:1 -- ops2:4
ops1:2 -- ops2:2
ops1:3 -- ops2:3
"""


def host_open_ipv4_port(obj_host, num_port, udp_port=False):
    """
    Opens (listens) in a specific port (udp/tcp)
    Returns PID of listening process
    """
    listen_command = 'nc -4vk'
    if udp_port:
        listen_command += 'u'
    listen_command += 'lw 1 {num_port} > /tmp/nc_{num_port} &'\
        .format(**locals())
    cmd_output = obj_host(listen_command, shell='bash')
    res = compile(r'\[\d+\] (\d+)')
    res_pid = res.findall(cmd_output)

    if len(res_pid) == 1:
        nc_pid = int(res_pid[0])
    else:
        nc_pid = -1

    return nc_pid


def host_send_data(obj_host, r_host, r_port, r_data, udp_port=False):
    """
    Sends tcp/udp data to another host
    """
    send_command = 'echo -n {r_data} | nc -4v'.format(**locals())
    if udp_port:
        send_command += 'u'
    send_command += ' -w 1 {r_host} {r_port}'.format(**locals())
    cmd_output = obj_host(send_command, shell='bash')

    res = compile('Connection to (\S+) (\d+) port (\S+)/(\S+) '
                  'succeed[\S+]')

    res_tmp = res.findall(cmd_output)

    if udp_port and len(res_tmp) == 0:
        return True

    res_data = res_tmp[0]

    if len(res_data) == 4:
        if res_data[0] == r_host and int(res_data[1]) == r_port:
            if udp_port:
                return res_data[2] == '[udp'
            else:
                return res_data[2] == '[tcp'
            return True
    return False


@mark.platform_incompatible(['docker'])
def test_lacpd_load_balance(topology):
    """
    Tests LAG load balance with l2, l3 and l4 hash algorithms
    """

    # VID for testing
    test_vlan = '256'
    # LAG ID for testing
    test_lag = '2'
    # Ports for testing
    test_port_tcp = 778
    test_port_udp = 777
    # number of pings
    num_ping = 5
    # seconds for tcpdump capture
    wait_time = 90
    times_to_send = 20
    # interfaces to be added to LAG
    lag_interfaces = ['2', '3']
    # traffic counters
    lag_intf_counter_b = {}
    lag_intf_counter_a = {}
    delta_tx = {}

    data_to_send = '0F'

    lag_lb_algorithms = ['l2-src-dst', 'l3-src-dst', 'l4-src-dst']
    sw1_host_interfaces = ['1']
    sw2_host_interfaces = ['1', '4']
    host1_addr = '10.0.11.10'
    host2_addr = '10.0.11.11'
    host3_addr = '10.0.11.12'

    ops1 = topology.get('ops1')
    ops2 = topology.get('ops2')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')
    hs3 = topology.get('hs3')

    assert ops1 is not None, 'Topology failed getting object ops1'
    assert ops2 is not None, 'Topology failed getting object ops2'
    assert hs1 is not None, 'Topology failed getting object hs1'
    assert hs2 is not None, 'Topology failed getting object hs2'
    assert hs3 is not None, 'Topology failed getting object hs3'

    # Turn on interfaces
    for curr_if in lag_interfaces + sw1_host_interfaces:
        turn_on_interface(ops1, curr_if)

    for curr_if in lag_interfaces + sw2_host_interfaces:
        turn_on_interface(ops2, curr_if)

    # Wait for interface become up
    sleep(5)
    validate_turn_on_interfaces(ops1, lag_interfaces + sw1_host_interfaces)
    validate_turn_on_interfaces(ops2, lag_interfaces + sw2_host_interfaces)

    # Configure switches
    for curr_ops in [ops1, ops2]:
        create_vlan(curr_ops, test_vlan)
        create_lag(curr_ops, test_lag)
        associate_vlan_to_lag(curr_ops, test_vlan, test_lag)
        for curr_if in lag_interfaces:
            associate_interface_to_lag(curr_ops, curr_if, test_lag)

    for curr_p in sw1_host_interfaces:
        associate_vlan_to_l2_interface(ops1, test_vlan, curr_p)

    for curr_p in sw2_host_interfaces:
        associate_vlan_to_l2_interface(ops2, test_vlan, curr_p)

    # Configure host interfaces
    hs1.libs.ip.interface('1', addr='{host1_addr}/24'.format(**locals()),
                          up=True)

    hs2.libs.ip.interface('1', addr='{host2_addr}/24'.format(**locals()),
                          up=True)

    hs3.libs.ip.interface('1', addr='{host3_addr}/24'.format(**locals()),
                          up=True)

    print('Sleep few seconds to wait everything is up')
    sleep(30)

    # Pinging to verify connections are OK
    check_connectivity_between_hosts(hs1, host1_addr,
                                     hs2, host2_addr)
    check_connectivity_between_hosts(hs1, host1_addr,
                                     hs3, host3_addr)

    host_open_ipv4_port(hs2, test_port_tcp)
    host_open_ipv4_port(hs3, test_port_tcp)
    host_open_ipv4_port(hs2, test_port_udp, True)

    for lb_algorithm in lag_lb_algorithms:
        print('========== Testing with {lb_algorithm} =========='
              .format(**locals()))
        for curr_ops in [ops1, ops2]:
            set_lag_lb_hash(curr_ops, test_lag, lb_algorithm)
            # Check that hash is properly set
            check_lag_lb_hash(curr_ops, test_lag, lb_algorithm)

        for curr_p in lag_interfaces:
            intf_info = ops1.libs.vtysh.show_interface(curr_p)
            lag_intf_counter_b[curr_p] = intf_info['tx_packets']

        for x in range(0, times_to_send):
            assert host_send_data(
                hs1, host2_addr,
                test_port_tcp, data_to_send
            ), 'Could not send data to hs2 (tcp)'

            if lb_algorithm == 'l4-src-dst':
                assert host_send_data(
                    hs1, host2_addr,
                    test_port_udp, data_to_send, True
                ), 'Could not send data to hs2 (udp)'
            else:
                assert host_send_data(
                    hs1, host3_addr,
                    test_port_tcp, data_to_send
                ), 'Could not send data to hs3 (tcp)'

        for curr_p in lag_interfaces:
            intf_info = ops1.libs.vtysh.show_interface(curr_p)
            lag_intf_counter_a[curr_p] = intf_info['tx_packets']
            delta_tx[curr_p] = lag_intf_counter_a[curr_p]\
                - lag_intf_counter_b[curr_p]

            assert delta_tx[curr_p] > 0,\
                'Just one interface was used with {lb_algorithm}'\
                .format(**locals())

        # Print a summary of counters
        print('======== {lb_algorithm} ============'.format(**locals()))
        for curr_p in lag_interfaces:
            print('Interface: {curr_p}'.format(**locals()))
            dt = delta_tx[curr_p]
            print('TX packets: {dt}'.format(**locals()))
            print('--')
        print('====================================')

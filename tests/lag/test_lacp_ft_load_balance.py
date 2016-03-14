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
hs1:eth1 -- ops1:1
hs2:eth1 -- ops2:1
hs3:eth1 -- ops2:4
ops1:2 -- ops2:2
ops1:3 -- ops2:3
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


def switch_lag_lb_hash_set(obj_switch, n_lag, lb_hash):
    """
    Sets hash algorithm for load balancing
    """
    # Actually framework does not support all hashes
    output_cmd = obj_switch(
        'set port lag{n_lag} other_config=bond_mode={lb_hash}-hash'.
        format(**locals()),
        shell='vsctl'
    )

    return output_cmd


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
    tcpdump_command = 'tcpdump -nnvvv -i {interface} '.format(**locals())
    if t_filter:
        tcpdump_command += '{t_filter}'.format(**locals())
    tcpdump_command += ' > /tmp/ops_{interface}.cap 2>&1 &'.format(**locals())
    obj_switch("ls", shell='bash')
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
        if len(format_res) == 1:
            final_result[td_counter] = int(format_res[0])
        else:
            final_result[td_counter] = 0

    return final_result


def host_open_ipv4_port(obj_host, num_port, udp_port=False):
    """
    Opens (listens) in a specific port (udp/tcp)
    Returns PID of listening process
    """
    listen_command = 'nc -vk'
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


def host_get_mac_address(obj_host, h_intf):
    """
    Gets mac address from host interface
    """
    get_mac_cmd = 'ip addr show dev {h_intf}'.format(**locals())
    get_mac_cmd += ' | grep link/ether | awk \'{print $2}\''
    mac_addr = obj_host(get_mac_cmd, shell='bash')

    return mac_addr


@mark.test_id(3482)
@mark.platform_incompatible(['docker'])
def test_lacpd_load_balance(topology):
    """
    Tests LAG load balance with l2, l3 and l4 hash algorithms
    """

    # VID for testing
    test_vlan = 256
    # LAG ID for testing
    test_lag = 2
    # Ports for testing
    test_port_tcp = 778
    test_port_udp = 777
    # number of pings
    num_ping = 5
    # seconds for tcpdump capture
    wait_time = 90
    # interfaces to be added to LAG
    lag_interfaces = ['2', '3']
    # List of tcpdump PIDs for each interface
    tcpdump_pids = {}
    # List of tcpdump counters (captured, received, dropped)
    tcpdump_counters = {}

    data_to_send = "0FCAFECAFE0202ACDCACDC000FFFFFFFFF"

    lag_lb_algorithms = ['l2-src-dst', 'l3-src-dst', 'l4-src-dst']
    host_eth_interface = 'eth1'
    sw1_host_interfaces = ['1']
    sw2_host_interfaces = ['1', '4']
    host1_addr = {'ipv4': '10.0.11.10', 'mac': ''}
    host2_addr = {'ipv4': '10.0.11.11', 'mac': ''}
    host3_addr = {'ipv4': '10.0.11.12', 'mac': ''}

    ops1 = topology.get('ops1')
    ops2 = topology.get('ops2')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')
    hs3 = topology.get('hs3')

    assert ops1 is not None, 'Topology failed getting object ops1'
    assert ops2 is not None, 'Topology failed getting object ops2'
    assert hs1 is not None, 'Topology failed getting object hs1'
    assert hs2 is not None, 'Topology failed getting object hs2'

    # Configure switches
    for curr_ops in [ops1, ops2]:
        switch_create_vlan(curr_ops, test_vlan)
        # Create and configure lags
        switch_create_lag(curr_ops, test_lag, test_vlan)
        for curr_if in lag_interfaces:
            switch_add_interface_to_lag(curr_ops, curr_if, test_lag)

    for curr_p in sw1_host_interfaces:
        switch_add_interface_to_vlan(ops1, curr_p, test_vlan)

    for curr_p in sw2_host_interfaces:
        switch_add_interface_to_vlan(ops2, curr_p, test_vlan)

    # Configure host interfaces
    ip_addr = host1_addr['ipv4']
    hs1.libs.ip.interface(host_eth_interface,
                          addr='{ip_addr}/24'.format(**locals()),
                          up=True)
    host1_addr['mac'] = host_get_mac_address(hs1, host_eth_interface)

    ip_addr = host2_addr['ipv4']
    hs2.libs.ip.interface(host_eth_interface,
                          addr='{ip_addr}/24'.format(**locals()),
                          up=True)
    host2_addr['mac'] = host_get_mac_address(hs2, host_eth_interface)

    ip_addr = host3_addr['ipv4']
    hs3.libs.ip.interface(host_eth_interface,
                          addr='{ip_addr}/24'.format(**locals()),
                          up=True)
    host3_addr['mac'] = host_get_mac_address(hs3, host_eth_interface)

    print('Sleep few seconds to wait everything is up')
    sleep(20)

    # Pinging to verify connections are OK
    ping = hs1.libs.ping.ping(num_ping, host2_addr['ipv4'])
    assert ping['transmitted'] == ping['received'] == num_ping,\
        'Connection to hs2 from hs1 failed'

    ping = hs1.libs.ping.ping(num_ping, host3_addr['ipv4'])
    assert ping['transmitted'] == ping['received'] == num_ping,\
        'Connection to hs3 from hs1 failed'

    ping = hs2.libs.ping.ping(num_ping, host1_addr['ipv4'])
    assert ping['transmitted'] == ping['received'] == num_ping,\
        'Connection to hs1 from hs2 failed'

    ping = hs3.libs.ping.ping(num_ping, host1_addr['ipv4'])
    assert ping['transmitted'] == ping['received'] == num_ping,\
        'Connection to hs1 from hs3 failed'

    lag_interfaces_idx = switch_get_interfaces(ops1)
    print(lag_interfaces_idx)

    host_open_ipv4_port(hs2, test_port_tcp)
    host_open_ipv4_port(hs3, test_port_tcp)
    host_open_ipv4_port(hs2, test_port_udp, True)

    for lb_algorithm in lag_lb_algorithms:
        print('========== Testing with {lb_algorithm} =========='
              .format(**locals()))
        for curr_ops in [ops1, ops2]:
            assert not switch_lag_lb_hash_set(
                curr_ops, test_lag, lb_algorithm)

        # Listen with tcpdump for each interface
        for lag_if in lag_interfaces:
            print(lag_interfaces_idx['index'][lag_if])
            curr_if = lag_interfaces_idx['index'][lag_if]
            # Start capturing packets
            ip_addr = host1_addr['ipv4']
            p_id = switch_capture_packets_start(
                ops1,
                curr_if,
                'src {ip_addr}'.format(**locals()))

            assert p_id > 0, 'Could not get tcpdump pid'

            tcpdump_pids[curr_if] = p_id

        for x in range(0, 30):
            assert host_send_data(
                hs1, host2_addr['ipv4'],
                test_port_tcp, data_to_send
            ), 'Could not send data to hs2 (tcp)'

            if lb_algorithm == 'l4-src-dst':
                assert host_send_data(
                    hs1, host2_addr['ipv4'],
                    test_port_udp, data_to_send, True
                ), 'Could not send data to hs2 (udp)'
            else:
                assert host_send_data(
                    hs1, host3_addr['ipv4'],
                    test_port_tcp, data_to_send
                ), 'Could not send data to hs3 (tcp)'

        for lag_if in lag_interfaces:
            # Get index for interface
            curr_if = lag_interfaces_idx['index'][lag_if]
            p_id = tcpdump_pids[curr_if]

            tcpdump_counters = switch_capture_packets_stop(
                ops1, curr_if, p_id)

            assert tcpdump_counters['received'] > 0,\
                'Just one interface used with {lb_algorithm}'\
                .format(**locals())

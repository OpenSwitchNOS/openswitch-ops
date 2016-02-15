# (C) Copyright 2016 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

##########################################################################
# Name:        ft_lacp_library.py
#
# Objective:   Library for all utils function used across all LACP tests
#
# Topology:    N/A
#
##########################################################################

"""
OpenSwitch Test Library for LACP
"""

import re
import time

LOCAL_STATE = 'local_state'
REMOTE_STATE = 'remote_state'
ACTOR = 'Actor'
PARTNER = 'Partner'
LACP_PROTOCOL = '0x8809'
LACP_MAC_HEADER = '01:80:c2:00:00:02'


def create_lag_active(sw, lag_id):
    with sw.libs.vtysh.ConfigInterfaceLag(lag_id) as ctx:
        ctx.lacp_mode_active()


def create_lag_passive(sw, lag_id):
    with sw.libs.vtysh.ConfigInterfaceLag(lag_id) as ctx:
        ctx.lacp_mode_passive()


def delete_lag(sw, lag_id):
    with sw.libs.vtysh.Configure() as ctx:
        ctx.no_interface_lag(lag_id)


def associate_interface_to_lag(sw, interface, lag_id):
    with sw.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.lag(lag_id)


def associate_vlan_to_lag(sw, vlan_id, lag_id):
    with sw.libs.vtysh.ConfigInterfaceLag(lag_id) as ctx:
        ctx.no_routing()
        ctx.vlan_access(vlan_id)


def turn_on_interface(sw, interface):
    with sw.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.no_shutdown()


def turn_off_interface(sw, interface):
    with sw.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.shutdown()


def validate_local_key(map_lacp, lag_id):
    assert map_lacp['local_key'] == lag_id,\
        "Actor Key is not the same as the LAG ID"


def validate_remote_key(map_lacp, lag_id):
    assert map_lacp['remote_key'] == lag_id,\
        "Partner Key is not the same as the LAG ID"


def validate_lag_name(map_lacp, lag_id):
    assert map_lacp['lag_id'] == lag_id,\
        "LAG ID should be " + lag_id


def validate_lag_state_sync(map_lacp, state):
    assert map_lacp[state]['active'] is True,\
        "LAG state should be active"
    assert map_lacp[state]['long_timeout'] is True,\
        "LAG state should have long timeout"
    assert map_lacp[state]['aggregable'] is True,\
        "LAG state should have aggregable enabled"
    assert map_lacp[state]['in_sync'] is True,\
        "LAG state should be In Sync"
    assert map_lacp[state]['collecting'] is True,\
        "LAG state should be in collecting"
    assert map_lacp[state]['distributing'] is True,\
        "LAG state should be in distributing"


def validate_lag_state_out_of_sync(map_lacp, state):
    assert map_lacp[state]['active'] is True,\
        "LAG state should be active"
    assert map_lacp[state]['in_sync'] is False,\
        "LAG state should be out of sync"
    assert map_lacp[state]['aggregable'] is True,\
        "LAG state should have aggregable enabled"
    assert map_lacp[state]['collecting'] is False,\
        "LAG state should not be in collecting"
    assert map_lacp[state]['distributing'] is False,\
        "LAG state should not be in distributing"
    assert map_lacp[state]['out_sync'] is True,\
        "LAG state should not be out of sync"


def validate_lag_state_alfn(map_lacp, state):
    assert map_lacp[state]['active'] is True,\
        "LAG state should be active"
    assert map_lacp[state]['long_timeout'] is True,\
        "LAG state should have long timeout"
    assert map_lacp[state]['aggregable'] is True,\
        "LAG state should have aggregable enabled"
    assert map_lacp[state]['in_sync'] is True,\
        "LAG state should be In Sync"
    assert map_lacp[state]['collecting'] is False,\
        "LAG state should not be in collecting"
    assert map_lacp[state]['distributing'] is False,\
        "LAG state should not be in distributing"


def validate_lag_state_default_neighbor(map_lacp, state):
    assert map_lacp[state]['neighbor_state'] is True,\
        "LAG state should have default neighbor state"


def get_device_mac_address(sw, interface):
    cmd_output = sw('ifconfig'.format(**locals()),
                    shell='bash_swns')
    mac_re = (r'' + interface + '\s*Link\sencap:Ethernet\s*HWaddr\s'
              r'(?P<mac_address>([0-9A-Fa-f]{2}[:-]){5}'
              r'[0-9A-Fa-f]{2})')

    re_result = re.search(mac_re, cmd_output)
    assert re_result

    result = re_result.groupdict()
    print(result)

    return result['mac_address']


def tcpdump_capture_interface(sw, interface_id, wait_time):
    cmd_output = sw('tcpdump -D'.format(**locals()),
                    shell='bash_swns')
    interface_re = (r'(?P<linux_interface>\d)\.' + interface_id +
                    r'\s[\[Up, Running\]]')
    re_result = re.search(interface_re, cmd_output)
    assert re_result
    result = re_result.groupdict()

    sw('tcpdump -ni ' + result['linux_interface'] +
        ' -e ether proto ' + LACP_PROTOCOL + ' -vv'
        '> /tmp/interface.cap 2>&1 &'.format(**locals()),
        shell='bash_swns')

    time.sleep(wait_time)

    sw('killall tcpdump'.format(**locals()),
        shell='bash_swns')

    capture = sw('cat /tmp/interface.cap'.format(**locals()),
                 shell='bash_swns')

    sw('rm /tmp/interface.cap'.format(**locals()),
       shell='bash_swns')

    return capture


def get_info_from_packet_capture(capture, switch_side, sw_mac):
    packet_re = (r'[\s \S]*' + sw_mac.lower() + '\s\>\s' + LACP_MAC_HEADER +
                 r'\,[\s \S]*'
                 r'' + switch_side + '\sInformation\sTLV\s\(0x\d*\)'
                 r'\,\slength\s\d*\s*'
                 r'System\s(?P<system_id>([0-9A-Fa-f]{2}[:-]){5}'
                 r'[0-9A-Fa-f]{2})\,\s'
                 r'System\sPriority\s(?P<system_priority>\d*)\,\s'
                 r'Key\s(?P<key>\d*)\,\s'
                 r'Port\s(?P<port_id>\d*)\,\s'
                 r'Port\sPriority\s(?P<port_priority>\d*)')

    re_result = re.search(packet_re, capture)
    assert re_result

    result = re_result.groupdict()

    return result


def set_debug(sw):
    sw('ovs-appctl -t ops-lacpd vlog/set dbg'.format(**locals()),
       shell='bash')


def create_vlan(sw, vlan_id):
    with sw.libs.vtysh.ConfigVlan(vlan_id) as ctx:
        ctx.no_shutdown()


def associate_vlan_to_l2_interface(sw, vlan_id, interface):
    with sw.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.no_routing()
        ctx.vlan_access(vlan_id)


def check_connectivity_between_hosts(h1, h1_ip, h2, h2_ip):
    ping = h1.libs.ping.ping(1, h2_ip)
    assert ping['transmitted'] == ping['received'] == 1,\
        'Ping between ' + h1_ip + ' and ' + h2_ip + ' failed'
    ping = h2.libs.ping.ping(1, h1_ip)
    assert ping['transmitted'] == ping['received'] == 1,\
        'Ping between ' + h2_ip + ' and ' + h1_ip + ' failed'

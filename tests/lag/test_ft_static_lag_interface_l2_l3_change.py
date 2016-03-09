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

##########################################################################
# Name:        test_ft_static_lag_interface_l2_l3_change.py
#
# Objective:   Verify an interface switches correctly from L2 LAG to L3 LAG
#              and viceversa
#
# Topology:    2 switches (DUT running Halon) connected by 3 interfaces
#              2 workstations connected by the 2 switches
#
##########################################################################

from time import sleep
from lacp_lib import create_lag_off
from lacp_lib import delete_lag
from lacp_lib import associate_interface_to_lag
from lacp_lib import remove_interface_from_lag
from lacp_lib import turn_on_interface
from lacp_lib import turn_off_interface
from lacp_lib import validate_turn_on_interfaces
from lacp_lib import create_vlan
from lacp_lib import delete_vlan
from lacp_lib import associate_vlan_to_lag
from lacp_lib import associate_vlan_to_l2_interface
from lacp_lib import assign_ip_to_lag


TOPOLOGY = """
#  +-----------------+
#  |                 |
#  |  Workstation 1  |
#  |                 |
#  +-------+---------+
#          |
#          |
#    +-----+------+
#    |            |
#    |  Switch 1  |
#    |  1  2  3   |
#    +--+--+--+---+
#       |  |  |
#  L2   |  |  |  L3
#  LAG  |  |  |  LAG
#    +--+--+--+---+
#    |  1  2  3   |
#    |  Switch 2  |
#    |            |
#    +-----+------+
#          |
#          |
#  +-------+---------+
#  |                 |
#  |  Workstation 2  |
#  |                 |
#  +-----------------+

# Nodes
[type=openswitch name="OpenSwitch 1"] sw1
[type=openswitch name="OpenSwitch 2"] sw2
[type=host name="Host 1"] hs1
[type=host name="Host 2"] hs2

# Links
hs1:1 -- sw1:4
sw1:1 -- sw2:1
sw1:2 -- sw2:2
sw1:3 -- sw2:3
sw2:4 -- hs2:1
"""


def ping_workstations(hs1, hs2, hs1_ip_address, hs2_ip_address,
                      pings_transmitted, pings_received):
    print("Ping workstation 2 from workstation 1")
    ping = hs1.libs.ping.ping(pings_transmitted, hs2_ip_address)
    assert ping['transmitted'] == pings_transmitted and\
        ping['received'] == pings_received,\
        "Number of pings transmitted is %d and should be %d. "\
        % (ping['transmitted'], pings_transmitted) +\
        "Number of pings received is %s and should be %s"\
        % (ping['received'], pings_received)

    print("Ping workstation 1 from workstation 2")
    ping = hs2.libs.ping.ping(pings_transmitted, hs1_ip_address)
    assert ping['transmitted'] == pings_transmitted and\
        ping['received'] == pings_received,\
        "Number of pings transmitted is %d and should be %d. "\
        % (ping['transmitted'], pings_transmitted) +\
        "Number of pings received is %s and should be %s"\
        % (ping['received'], pings_received)


def ping_switches(sw1, sw2, sw1_ip_address, sw2_ip_address,
                  pings_transmitted, pings_received):
    print("Ping switch2 from switch1")
    ping = sw1.libs.vtysh.ping_repetitions(sw2_ip_address, pings_transmitted)
    assert ping['transmitted'] == pings_transmitted and\
        ping['received'] == pings_received,\
        "Number of pings transmitted is %d and should be %d. "\
        % (ping['transmitted'], pings_transmitted) +\
        "Number of pings received is %s and should be %s"\
        % (ping['received'], pings_received)

    print("Ping switch1 from switch2")
    ping = sw2.libs.vtysh.ping_repetitions(sw1_ip_address, pings_transmitted)
    assert ping['transmitted'] == pings_transmitted and\
        ping['received'] == pings_received,\
        "Number of pings transmitted is %d and should be %d. "\
        % (ping['transmitted'], pings_transmitted) +\
        "Number of pings received is %s and should be %s"\
        % (ping['received'], pings_received)


def test_l2_l3_interface_switch_case_1(topology):
    """
    Case 1:
        This test verifies the functionality of 2 LAGs when an interface is
        changed from a L2 LAG to a L3 LAG and viceversa.
    """
    sw1 = topology.get('sw1')
    sw2 = topology.get('sw2')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')
    ip_address_mask = '24'
    hs1_ip_address = '10.0.10.1'
    hs2_ip_address = '10.0.10.2'
    hs1_ip_address_with_mask = hs1_ip_address + '/' + ip_address_mask
    hs2_ip_address_with_mask = hs2_ip_address + '/' + ip_address_mask
    sw1_l3_lag_ip_address = '10.0.0.1'
    sw2_l3_lag_ip_address = '10.0.0.2'
    l2_lag_id = '2'
    l3_lag_id = '3'
    vlan_identifier = '8'
    number_pings = 5

    assert sw1 is not None
    assert sw2 is not None
    assert hs1 is not None
    assert hs2 is not None

    p11 = sw1.ports['1']
    p12 = sw1.ports['2']
    p13 = sw1.ports['3']
    p14 = sw1.ports['4']
    p21 = sw2.ports['1']
    p22 = sw2.ports['2']
    p23 = sw2.ports['3']
    p24 = sw2.ports['4']

    print("Turning on all interfaces used in this test")
    ports_sw1 = [p11, p12, p13, p14]
    for port in ports_sw1:
        turn_on_interface(sw1, port)

    ports_sw2 = [p21, p22, p23, p24]
    for port in ports_sw2:
        turn_on_interface(sw2, port)

    print("Waiting some time for the interfaces to be up")
    sleep(15)

    print("Verify all interface are up")
    validate_turn_on_interfaces(sw1, ports_sw1)
    validate_turn_on_interfaces(sw2, ports_sw2)

    print("Assign an IP address on the same range to each workstation")
    hs1.libs.ip.interface('1', addr=hs1_ip_address_with_mask, up=True)
    hs2.libs.ip.interface('1', addr=hs2_ip_address_with_mask, up=True)

    print('Creating VLAN in both switches')
    create_vlan(sw1, vlan_identifier)
    create_vlan(sw2, vlan_identifier)

    print("Create L2 LAG in both switches")
    create_lag_off(sw1, l2_lag_id)
    create_lag_off(sw2, l2_lag_id)

    print("Associate interfaces [1, 2] to L2 LAG in both switches")
    associate_interface_to_lag(sw1, p11, l2_lag_id)
    associate_interface_to_lag(sw1, p12, l2_lag_id)
    associate_interface_to_lag(sw2, p21, l2_lag_id)
    associate_interface_to_lag(sw2, p22, l2_lag_id)

    print("Create L3 LAG in both switches")
    create_lag_off(sw1, l3_lag_id)
    create_lag_off(sw2, l3_lag_id)

    print("Associate interface 3 to L3 LAG in both switches")
    associate_interface_to_lag(sw1, p13, l3_lag_id)
    associate_interface_to_lag(sw2, p23, l3_lag_id)

    print("Configure LAGs and workstations interfaces with same VLAN")
    associate_vlan_to_lag(sw1, vlan_identifier, l2_lag_id)
    associate_vlan_to_lag(sw2, vlan_identifier, l2_lag_id)
    associate_vlan_to_l2_interface(sw1, vlan_identifier, p14)
    associate_vlan_to_l2_interface(sw2, vlan_identifier, p24)

    print("Assign IP on the same range to LAG in both switches")
    assign_ip_to_lag(sw1, l3_lag_id, sw1_l3_lag_ip_address, ip_address_mask)
    assign_ip_to_lag(sw2, l3_lag_id, sw2_l3_lag_ip_address, ip_address_mask)

    print("Waiting some time for change to apply")
    sleep(5)
    # Ping between workstations should succeed
    ping_workstations(hs1, hs2, hs1_ip_address, hs2_ip_address,
                      number_pings, number_pings)
    # Ping between switches should succeed
    ping_switches(sw1, sw2, sw1_l3_lag_ip_address, sw2_l3_lag_ip_address,
                  number_pings, number_pings)

    print("Associate interface 2 to L3 LAG in both switches")
    associate_interface_to_lag(sw1, p12, l3_lag_id)
    associate_interface_to_lag(sw2, p22, l3_lag_id)

    print("Waiting some time for change to apply")
    sleep(5)
    # Ping between workstations should succeed
    ping_workstations(hs1, hs2, hs1_ip_address, hs2_ip_address,
                      number_pings, number_pings)
    # Ping between switches should succeed
    ping_switches(sw1, sw2, sw1_l3_lag_ip_address, sw2_l3_lag_ip_address,
                  number_pings, number_pings)

    print("Associate interface 2 to L2 LAG in both switches")
    associate_interface_to_lag(sw1, p12, l2_lag_id)
    associate_interface_to_lag(sw2, p22, l2_lag_id)

    print("Waiting some time for change to apply")
    sleep(5)
    # Ping between workstations should succeed
    ping_workstations(hs1, hs2, hs1_ip_address, hs2_ip_address,
                      number_pings, number_pings)
    # Ping between switches should succeed
    ping_switches(sw1, sw2, sw1_l3_lag_ip_address, sw2_l3_lag_ip_address,
                  number_pings, number_pings)

    print("Remove interface 2 from L2 LAG in both switches")
    remove_interface_from_lag(sw1, p12, l2_lag_id)
    remove_interface_from_lag(sw2, p22, l2_lag_id)

    print("Associate interface 2 to L3 LAG in both switches")
    associate_interface_to_lag(sw1, p12, l3_lag_id)
    associate_interface_to_lag(sw2, p22, l3_lag_id)

    print("Waiting some time for change to apply")
    sleep(5)
    # Ping between workstations should succeed
    ping_workstations(hs1, hs2, hs1_ip_address, hs2_ip_address,
                      number_pings, number_pings)
    # Ping between switches should succeed
    ping_switches(sw1, sw2, sw1_l3_lag_ip_address, sw2_l3_lag_ip_address,
                  number_pings, number_pings)

    print("Remove interface 2 from L3 LAG in both switches")
    remove_interface_from_lag(sw1, p12, l3_lag_id)
    remove_interface_from_lag(sw2, p22, l3_lag_id)

    print("Associate interface 2 to L2 LAG in both switches")
    associate_interface_to_lag(sw1, p12, l2_lag_id)
    associate_interface_to_lag(sw2, p22, l2_lag_id)

    print("Waiting some time for change to apply")
    sleep(5)
    # Ping between workstations should succeed
    ping_workstations(hs1, hs2, hs1_ip_address, hs2_ip_address,
                      number_pings, number_pings)
    # Ping between switches should succeed
    ping_switches(sw1, sw2, sw1_l3_lag_ip_address, sw2_l3_lag_ip_address,
                  number_pings, number_pings)

    print("Cleaning configuration")
    for port in ports_sw1:
        turn_off_interface(sw1, port)

    for port in ports_sw2:
        turn_off_interface(sw2, port)

    delete_vlan(sw1, vlan_identifier)
    delete_vlan(sw2, vlan_identifier)

    delete_lag(sw1, l2_lag_id)
    delete_lag(sw2, l2_lag_id)
    delete_lag(sw1, l3_lag_id)
    delete_lag(sw2, l3_lag_id)

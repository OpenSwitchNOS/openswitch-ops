#!/usr/bin/env python

# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Configure Switch Utility.

Name:
    configure_switch

Objective:
    Used to automate swtich configuration using a dictionary provided from a
    test case.
"""

from keys import (
    INTF_ENABLE, INTF_NAME, IP_ADDR, IP_ENABLE, IP_INTF, IP_MASK, IP_V6,
    KEY_INTF, KEY_IP, KEY_IPV6, KEY_LAG, KEY_ROUTE, LAG_ENABLE, LAG_ID,
    ROUTE_ENABLE, ROUTE_IPV6, ROUTE_MASK, ROUTE_NEXTHOP, ROUTE_ROUTE
)

from opstestfw import LogOutput
from opstestfw.switch.CLI import (
    InterfaceEnable,
    InterfaceIpConfig,
    InterfaceLagIdConfig,
    IpRouteConfig,
    lagCreation
)


def switch_create_lag(switch, lags):
    """Configure LAG section.

    Params:
        - switch: Device to be configure
        - lags: Array of dictionaries
    """
    for lag in lags:
        LogOutput('info', 'Creating LAG %s on switch' % lag[LAG_ID])
        ret_struct = lagCreation(deviceObj=switch,
                                 lagId=lag[LAG_ID],
                                 configFlag=lag[LAG_ENABLE])
        assert not ret_struct.returnCode(), \
            'Unable to create LAG %s on device' % (lag[LAG_ID])


def switch_enable_interface(switch, interfaces):
    """Configure Enable interface section.

    Param:
        - switch: Device to be configure
        - interfaces: Array of dictionaries
    """
    for intf in interfaces:

        LogOutput('info',
                  'Enabling interface %s on device' % intf[INTF_NAME])

        ret_struct = InterfaceEnable(
                        deviceObj=switch,
                        enable=intf['enable'],
                        interface=switch.linkPortMapping[intf[INTF_NAME]])
        assert not ret_struct.returnCode(), \
            'Unable to enable interface %s on device' % (intf[INTF_NAME])


def switch_configure_lag_interface(switch, interfaces):
    """Configure Interface to LAG section.

    Param:
        - switch: Device to be configure
        - interfaces: Array of dictionaries
    """
    for intf in interfaces:

        if KEY_LAG in intf:
            LogOutput('info',
                      'Configuring LAG %s to interface %s' %
                      (intf[LAG_ID], intf[INTF_NAME]))

            ret_struct = InterfaceLagIdConfig(
                            deviceObj=switch,
                            interface=switch.linkPortMapping[intf[INTF_NAME]],
                            lagId=intf[LAG_ID],
                            enable=intf[INTF_ENABLE])
            assert not ret_struct.returnCode(), \
                'Unable to configure LAG %s to interface %s' % \
                (intf[LAG_ID], intf[INTF_NAME])


def switch_configure_interface_ip(switch, ips):
    """Configure IPv4/IPv6 section.

    Params:
        - switch: Device to be configure
        - ips: Array of dictionaries
    """
    for ip in ips:
        ret_struct = False

        if KEY_IPV6 in ip:
            LogOutput('info',
                      'Configuring IPv6 address on Interface %s' %
                      ip[IP_INTF])

            ret_struct = InterfaceIpConfig(
                            deviceObj=switch,
                            interface=switch.linkPortMapping[ip[IP_INTF]],
                            addr=ip[IP_ADDR],
                            mask=ip[IP_MASK],
                            ipv6flag=ip[IP_V6],
                            config=ip[IP_ENABLE])
        else:
            LogOutput('info',
                      'Configuring IPv4 address on Interface %s' %
                      ip[IP_INTF])

            ret_struct = InterfaceIpConfig(
                            deviceObj=switch,
                            interface=switch.linkPortMapping[ip[IP_INTF]],
                            addr=ip[IP_ADDR],
                            mask=ip[IP_MASK],
                            config=ip[IP_ENABLE])

    assert not ret_struct.returnCode(), 'Failed to configure an IP address'


def switch_configure_route(switch, routes):
    """Configure routes section.

    Params:
        - switch: Device to be configure
        - routes: Array of dictionaries
    """
    for route in routes:
        ret_struct = False

        if KEY_IPV6 in route:
            LogOutput('info', 'Configuring IPv6 static route')
            ret_struct = IpRouteConfig(deviceObj=switch,
                                       route=route[ROUTE_ROUTE],
                                       mask=route[ROUTE_MASK],
                                       nexthop=route[ROUTE_NEXTHOP],
                                       config=route[ROUTE_ENABLE],
                                       ipv6flag=route[ROUTE_IPV6])
        else:
            LogOutput('info', 'Configuring IPv4 static route')
            ret_struct = IpRouteConfig(deviceObj=switch,
                                       route=route[ROUTE_ROUTE],
                                       mask=route[ROUTE_MASK],
                                       nexthop=route[ROUTE_NEXTHOP],
                                       config=route[ROUTE_ENABLE])

    assert not ret_struct.returnCode(), 'Failed to configure static route'


def configure_switch(switch, config):
    """Used for switch basic configuration.

    The idea of this function is to simplify device configuration, prevent
    multiple failure points across the test, it also to improve legibility when
    you are debugging. All switch configuration values will be defined in a
    single variable, not across the test setup.

    Params:

        switch:
            Device to be configured

        config:
            Dictionary with values to be configured

    The logic of how a device should be configured must be written here.
    """
    LogOutput('info', 'Starting switch configuration!')
    if KEY_LAG in config:
        switch_create_lag(switch, config[KEY_LAG])

    if KEY_INTF in config:
        switch_enable_interface(switch, config[KEY_INTF])

        if KEY_LAG in config:
            switch_configure_lag_interface(switch,
                                           config[KEY_INTF])

        switch_configure_interface_ip(switch, config[KEY_IP])

        if KEY_ROUTE in config:
            switch_configure_route(switch, config[KEY_ROUTE])

    LogOutput('info', 'Switch configuration DONE!')

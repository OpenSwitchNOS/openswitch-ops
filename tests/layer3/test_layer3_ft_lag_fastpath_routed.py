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

from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch.OVS import *

from utils.configure_host import *
from utils.configure_switch import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,"
                         "lnk02:dut01:dut02,"
                         "lnk03:dut02:wrkston02",
            "topoFilters": "dut01:system-category:switch,"
                           "dut02:system-category:switch,"
                           "wrkston01:system-category:workstation,"
                           "wrkston02:system-category:workstation"}


def fastpath_ping(**kwargs):
    """Test description

    Topology:

        [h1] <-----> [s1] <-----> [s2] <-----> [h2]

    Objective:
        Test successful and failure ping executions betwen h1 and h2 through
        two switches configured with static routes and a LAG. The ping
        executions will be done using IPv4 and IPv6.

    Cases:
        - Execute successful pings between hosts with static routes configured.
        - Execute unsuccessful pings between hosts when there are no static
          routes configured.
    """
    switch1 = kwargs.get('device1', None)
    switch2 = kwargs.get('device2', None)
    host1 = kwargs.get('device3', None)
    host2 = kwargs.get('device4', None)

    ###########################################################################
    #                                                                         #
    #                   [H1] ------- ping -------> [H2]                       #
    #                                                                         #
    ###########################################################################
    LogOutput('info', " Pinging host 1 to host 2 using IPv4")
    retStruct = host1.Ping(ipAddr="10.0.30.1", packetCount=1)

    assert not retStruct.returnCode(), "Failed to do IPv4 ping"

    LogOutput('info', "IPv4 Ping from host 1 to host 2 return JSON:\n")
    retStruct.printValueString()
    LogOutput('info', "IPv4 Ping Passed")

    LogOutput('info', "Pinging host 1 to host 2 using IPv6")
    retStruct = host1.Ping(ipAddr="2002::1", packetCount=1, ipv6Flag=True)

    assert not retStruct.returnCode(), "Failed to do IPv6 ping"

    LogOutput('info', "IPv6 Ping from host 1 to host 2 return JSON:\n")
    retStruct.printValueString()
    LogOutput('info', "IPv6 Ping Passed")

    ###########################################################################
    #                                                                         #
    #                   [H1] <------- ping ------- [H2]                       #
    #                                                                         #
    ###########################################################################
    LogOutput('info', "Pinging host 2 to host 1 using IPv4")
    retStruct = host2.Ping(ipAddr="10.0.10.1", packetCount=1)

    assert not retStruct.returnCode(), "Failed to do IPv4 ping"

    LogOutput('info', "IPv4 Ping from host 2 to host 1 return JSON:\n")
    retStruct.printValueString()
    LogOutput('info', "IPv4 Ping Passed")

    LogOutput('info', "Pinging host 2 to host 1 using IPv6")
    retStruct = host2.Ping(ipAddr="2000::1", packetCount=1, ipv6Flag=True)

    assert not retStruct.returnCode(), "Failed to do IPv6 ping"

    LogOutput('info', "IPv6 Ping from host 2 to host 1 return JSON:\n")
    retStruct.printValueString()
    LogOutput('info', "IPv6 Ping Passed")

    ###########################################################################
    # Removing static routes                                                  #
    ###########################################################################
    LogOutput('info', "Removing static Routes on s1 and s2")
    retStruct = IpRouteConfig(deviceObj=switch1,
                              route="10.0.30.0",
                              mask=24,
                              nexthop="10.0.20.2",
                              config=False)
    assert not retStruct.returnCode(), \
        "Failed to unconfigure IPv4 address route"

    retStruct = IpRouteConfig(deviceObj=switch2,
                              route="10.0.10.0",
                              mask=24,
                              nexthop="10.0.20.1",
                              config=False)
    assert not retStruct.returnCode(), \
        "Failed to unconfigure IPv4 address route"

    retStruct = IpRouteConfig(deviceObj=switch1,
                              route="2002::",
                              mask=120,
                              nexthop="2001::2",
                              config=False,
                              ipv6flag=True)
    assert not retStruct.returnCode(), \
        "Failed to unconfigure IPv6 address route"

    retStruct = IpRouteConfig(deviceObj=switch2,
                              route="2000::",
                              mask=120,
                              nexthop="2001::1",
                              config=False,
                              ipv6flag=True)
    assert not retStruct.returnCode(), \
        "Failed to unconfigure IPv6 address route"

    LogOutput('info', "Ping after removing static route from S1 and S2")
    ###########################################################################
    #                                                                         #
    #                   [H1] ------- ping -------> [H2]                       #
    #                                                                         #
    ###########################################################################
    # IPv4
    LogOutput('info', "Pinging host 1 to host 2 using IPv4")
    retStruct = host1.Ping(ipAddr="10.0.30.1", packetCount=1)

    assert retStruct.returnCode(), "Failed: Successful IPv4 ping done!"

    LogOutput('info', "IPv4 Ping from host 1 to host 2 return JSON:\n")
    retStruct.printValueString()
    LogOutput('info', "IPv4 Ping Passed")

    # IPv6
    LogOutput('info', "Pinging host 1 to host 2 using IPv6")
    retStruct = host1.Ping(ipAddr="2002::1", packetCount=1, ipv6Flag=True)

    assert retStruct.returnCode(), "Failed: Successful IPv6 ping done!"

    LogOutput('info', "IPv6 Ping from host 1 to host 2 return JSON:\n")
    retStruct.printValueString()
    LogOutput('info', "IPv6 Ping Passed")

    ###########################################################################
    #                                                                         #
    #                   [H1] <------- ping ------- [H2]                       #
    #                                                                         #
    ###########################################################################
    # IPv4
    LogOutput('info', "Pinging host 2 to host 1 using IPv4")
    retStruct = host2.Ping(ipAddr="10.0.10.1", packetCount=1)

    assert retStruct.returnCode(), "Failed: Successful IPv4 ping done!"

    LogOutput('info', "IPv4 Ping from host 2 to host 1 return JSON:\n")
    retStruct.printValueString()
    LogOutput('info', "IPv4 Ping Passed")

    # IPv6
    LogOutput('info', "Pinging host 2 to host 1 using IPv6")
    retStruct = host2.Ping(ipAddr="2000::1", packetCount=1, ipv6Flag=True)

    assert retStruct.returnCode(), "Failed: Successful IPv6 ping done!"

    LogOutput('info', "IPv6 Ping from host 2 to host 1 return JSON:\n")
    retStruct.printValueString()
    LogOutput('info', "IPv6 Ping Passed")


class Test_fastpath_ping:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_fastpath_ping.testObj = testEnviron(topoDict=topoDict)
        # Get topology object
        Test_fastpath_ping.topoObj = Test_fastpath_ping.testObj.topoObjGet()

    def teardown_class(cls):
        Test_fastpath_ping.topoObj.terminate_nodes()

    def setup_method(self, method):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")

        LAG_ID = 100

        config_sw1 = \
            {"lag": [{"id": LAG_ID,
                      "enable": True}],
             "intf": [{"name": "lnk01",
                       "enable": True},
                      {"name": "lnk02",
                       "enable": True,
                       "lag": LAG_ID}],
             "ip": [{"intf": "lnk01",
                     "addr": "10.0.10.2",
                     "mask": 24,
                     "enable": True},
                    {"intf": "lnk01",
                     "addr": "2000::2",
                     "mask": 120,
                     "enable": True,
                     "ipv6": True},
                    {"intf": "lnk02",
                     "addr": "10.0.20.1",
                     "mask": 24,
                     "enable": True},
                    {"intf": "lnk02",
                     "addr": "2001::1",
                     "mask": 120,
                     "enable": True,
                     "ipv6": True}],
             "route": [{"route": "10.0.30.0",
                        "mask": 24,
                        "nexthop": "10.0.20.2",
                        "enable": True},
                       {"route": "2002::",
                        "mask": 120,
                        "nexthop": "2001::2",
                        "enable": True,
                        "ipv6": True}]}
        configure_switch(dut01Obj, config_sw1)

        config_sw2 = \
            {"lag": [{"id": LAG_ID,
                      "enable": True}],
             "intf": [{"name": "lnk03",
                       "enable": True},
                      {"name": "lnk02",
                       "enable": True,
                       "lag": LAG_ID}],
             "ip": [{"intf": "lnk03",
                     "addr": "10.0.30.2",
                     "mask": 24,
                     "enable": True},
                    {"intf": "lnk03",
                     "addr": "2002::2",
                     "mask": 120,
                     "enable": True,
                     "ipv6": True},
                    {"intf": "lnk02",
                     "addr": "10.0.20.2",
                     "mask": 24,
                     "enable": True},
                    {"intf": "lnk02",
                     "addr": "2001::2",
                     "mask": 120,
                     "enable": True,
                     "ipv6": True}],
             "route": [{"route": "10.0.10.0",
                        "mask": 24,
                        "nexthop": "10.0.20.1",
                        "enable": True},
                       {"route": "2000::",
                        "mask": 120,
                        "nexthop": "2001::1",
                        "enable": True,
                        "ipv6": True}]}
        configure_switch(dut02Obj, config_sw2)

        config_h1 = \
            {"ip": [{"intf": "lnk01",
                     "addr": "10.0.10.1",
                     "mask": "255.255.255.0",
                     "broadcast": "10.0.10.0",
                     "enable": True},
                    {"intf": "lnk01",
                     "addr": "2000::1",
                     "mask": 120,
                     "broadcast": "2000::0",
                     "ipv6": True,
                     "enable": True}],
             "route": [{"dst": "10.0.20.0",
                        "mask": 24,
                        "gateway": "10.0.10.2",
                        "enable": True},
                       {"dst": "10.0.30.0",
                        "mask": 24,
                        "gateway": "10.0.10.2",
                        "enable": True},
                       {"dst": "2001::0",
                        "mask": 120,
                        "gateway": "2000::2",
                        "ipv6": True,
                        "enable": True},
                       {"dst": "2002::0",
                        "mask": 120,
                        "gateway": "2000::2",
                        "ipv6": True,
                        "enable": True}]}
        configure_host(wrkston01Obj, config_h1)

        config_h2 = \
            {"ip": [{"intf": "lnk03",
                     "addr": "10.0.30.1",
                     "mask": "255.255.255.0",
                     "broadcast": "10.0.30.0",
                     "enable": True},
                    {"intf": "lnk03",
                     "addr": "2002::1",
                     "mask": 120,
                     "broadcast": "2002::0",
                     "ipv6": True,
                     "enable": True}],
             "route": [{"dst": "10.0.10.0",
                        "mask": 24,
                        "gateway": "10.0.30.2",
                        "enable": True},
                       {"dst": "10.0.20.0",
                        "mask": 24,
                        "gateway": "10.0.30.2",
                        "enable": True},
                       {"dst": "2000::0",
                        "mask": 120,
                        "gateway": "2002::2",
                        "ipv6": True,
                        "enable": True},
                       {"dst": "2001::0",
                        "mask": 120,
                        "gateway": "2002::2",
                        "ipv6": True,
                        "enable": True}]}
        configure_host(wrkston02Obj, config_h2)

    def test_fastpath_ping(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        fastpath_ping(device1=dut01Obj,
                      device2=dut02Obj,
                      device3=wrkston01Obj,
                      device4=wrkston02Obj)

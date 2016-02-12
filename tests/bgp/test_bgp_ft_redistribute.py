#!/usr/bin/python

# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
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

import pytest
from opsvsi.docker import *
from opsvsi.opsvsitest import *
import time
#
# This test verifies the following commands
#  *    redistribute (connected|static|ospf)
#  *    redistribute (connected|static|ospf) route-map WORD
#
# For this test, we need 3 switches.
#
#
# S1 [interface 1]<--->[interface 1] S2 [interface 2]<---->[interface 1]S3

class myTopo(Topo):

    def build(self, sws=3 , **_opts):
        '''Function to build the topology of \
        two switches'''
        self.sws = sws
        # Add list of switches
        for s in irange(1, sws):
            switch = self.addSwitch('s%s' % s)
        # Add links between nodes based on custom topology
        self.addLink('s1', 's2')
        self.addLink('s2', 's3')

class bgpRedistributeTest(OpsVsiTest):
    def setupNet(self):
        self.net = Mininet(topo=myTopo(sws=3,
                                       sopts=self.getSwitchOpts()),
                                       switch=VsiOpenSwitch,
                                       link=OpsVsiLink, controller=None,
                                       build=True)
    def testConfigure(self):
        info('\n### Testing Redistribute configuration ###\n')
        s1 = self.net.switches[0]

        # Configure switch s1
        s1.cmdCLI("configure terminal")

        # Configure interface 1 on switch s1
        s1.cmdCLI("interface 1")
        s1.cmdCLI("no shutdown")
        s1.cmdCLI("ip address 7.0.0.1/8")
        s1.cmdCLI("exit")

        s2 = self.net.switches[1]

        # Configure switch s2
        s2.cmdCLI("configure terminal")

        # Configure interface 1 on switch s2
        s2.cmdCLI("interface 1")
        s2.cmdCLI("no shutdown")
        s2.cmdCLI("ip address 7.0.0.2/8")
        s2.cmdCLI("exit")

        # Configure interface 2 on switch s2
        s2.cmdCLI("interface 2")
        s2.cmdCLI("no shutdown")
        s2.cmdCLI("ip address 8.0.0.2/8")
        s2.cmdCLI("exit")

        s2.cmdCLI("router bgp 1")
        s2.cmdCLI("bgp router-id 8.0.0.2")
        s2.cmdCLI("network 10.0.0.0/8")
        s2.cmdCLI("neighbor 8.0.0.3 remote-as 2")

        s3 = self.net.switches[2]

        # Configure switch s3
        s3.cmdCLI("configure terminal")

        # Configure interface 1 on switch s3
        s3.cmdCLI("interface 1")
        s3.cmdCLI("no shutdown")
        s3.cmdCLI("ip address 8.0.0.3/8")
        s3.cmdCLI("exit")

        s3.cmdCLI("router bgp 2")
        s3.cmdCLI("bgp router-id 8.0.0.3")
        s3.cmdCLI("network 19.0.0.0/8")
        s3.cmdCLI("neighbor 8.0.0.2 remote-as 1")

    def testAddRedistribute(self):
        info('\n### Verify redistribute configuration add ###\n')
        redist_config = False
        s2 = self.net.switches[1]
        s2.cmdCLI("router bgp 1")
        s2.cmdCLI("redistribute connected")
        s2.cmdCLI("exit")
        dump = s2.cmdCLI("do show ip bgp")
        lines = dump.split('\n')
        for line in lines:
            if "7.0.0.0/8        0.0.0.0" \
                in line :
                redist_config = True

        assert redist_config == True, \
            'Test to verify redistribute configuration add - FAILED!'

        return True

    def testDeleteRedistribute(self):
        info('\n### Verify redistribute configuration delete ###\n')
        redist_delete = True
        s2 = self.net.switches[1]
        s2.cmdCLI("router bgp 1")
        s2.cmdCLI("no redistribute connected")
        sleep(10)
        out = s2.cmdCLI("do show ip bgp")
        lines = out.split('\n')
        for line in lines:
            if "7.0.0.0/8        0.0.0.0" \
                in line :
                redist_delete = False

        assert redist_delete == True, \
            'Test to verify redistribute configuration delete - FAILED!'

        return True

    def testAddRedistributeRoutemap(self):
        info('\n### Verify redistribute route-map configuration add ###\n')
        redist_config = False
        s2 = self.net.switches[1]
        s2.cmdCLI("ip prefix-list TEST seq 10 permit any")
        s2.cmdCLI("route-map TEST permit 20")
        s2.cmdCLI("match ip address prefix-list TEST")
        s2.cmdCLI("exit")
        s2.cmdCLI("router bgp 1")
        s2.cmdCLI("redistribute connected route-map TEST")
        s2.cmdCLI("exit")
        dump = s2.cmdCLI("do show ip bgp")
        lines = dump.split('\n')
        for line in lines:
            if "7.0.0.0/8        0.0.0.0" \
                in line :
                redist_config = True

        assert redist_config == True, \
            'Test to verify redistribute route-map configuration add - FAILED!'

        return True

    def testDeleteRedistributeRoutemap(self):
        info('\n### Verify redistribute route-map configuration delete ###\n')
        redist_delete = True
        s2 = self.net.switches[1]
        s2.cmdCLI("router bgp 1")
        s2.cmdCLI("no redistribute connected route-map TEST")
        sleep(10)
        info('\n### redistribute route-map configuration deleted ###\n')
        s2.cmdCLI("exit")
        dump = s2.cmdCLI("do show ip bgp")
        lines = dump.split('\n')
        for line in lines:
            if "7.0.0.0/8        0.0.0.0" \
                in line :
                redist_delete = False

        assert redist_delete == True, \
            'Test to verify redistribute route-map configuration delete'\
            ' - FAILED!'

        return True


class Test_redistribute:

    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_redistribute.bgpRedistributeTest = bgpRedistributeTest()

    def setup_method(self, method):
        pass

    def teardown_class(cls):
        # Stop the Docker containers, and
        # mininet topology
        Test_redistribute.bgpRedistributeTest.net.stop()

    def test_redistribute(self):
        info('\n########## Test redistribute '\
             'configuration ##########\n')
        self.bgpRedistributeTest.testConfigure()

        if self.bgpRedistributeTest.testAddRedistribute():
             info("\n### Test to verify redistribute configuration add "
                  "- SUCCESS!  ###\n")

        if self.bgpRedistributeTest.testDeleteRedistribute():
             info("\n### Test to verify redistribute configuration delete "
                  "- SUCESS! ###\n")

        if self.bgpRedistributeTest.testAddRedistributeRoutemap():
             info("\n### Test to verify redistribute route-map configuration"
                  " add - SUCESS! ###\n")

        if self.bgpRedistributeTest.testDeleteRedistributeRoutemap():
             info("\n### Test to verify redistribute route-map configuration"
                  " delete - SUCESS! ###\n")

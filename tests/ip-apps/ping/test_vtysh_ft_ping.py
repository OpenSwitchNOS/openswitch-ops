#!/usr/bin/python

# (c) Copyright 2015 Hewlett Packard Enterprise Development LP
#
# GNU Zebra is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any
# later version.
#
# GNU Zebra is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Zebra; see the file COPYING.  If not, write to the Free
# Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

from opsvsi.docker import *
from opsvsi.opsvsitest import *

#
# The purpose of this test is to test
# functionality of ping Ip-App
#
# For this test, we need 2 switches connected to
# each other
# S1 [interface 1]<--->[interface 1] S2
#

# Topology definition


class myTopo(Topo):

    def build(self, hsts=0, sws=2, **_opts):
        self.hsts = hsts
        self.sws = sws
        for s in irange(1, sws):
            switch = self.addSwitch('s%s' % s)

        self.addLink('s1', 's2')


class pingTest(OpsVsiTest):

    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=0, sws=2,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                                       switch=VsiOpenSwitch,
                                       host=OpsVsiHost,
                                       link=OpsVsiLink,
                                       controller=None,
                                       build=True)

    def configure(self):
        info('\n### Configuring switches with IPv4 and IPv6 address ###\n')
        s1 = self.net.switches[0]
        s2 = self.net.switches[1]

        # Configure switch s1
        s1.cmdCLI("configure terminal")
        s1.cmdCLI("interface 1")
        s1.cmdCLI("no shutdown")
        s1.cmdCLI("ip address 10.0.10.1/8")
        s1.cmdCLI("ipv6 address 2000::1/120")
        s1.cmdCLI("exit")
        s1.cmdCLI("exit")

        # Configure switch s2
        s2.cmdCLI("configure terminal")
        s2.cmdCLI("interface 1")
        s2.cmdCLI("no shutdown")
        s2.cmdCLI("ip address 10.0.10.2/8")
        s2.cmdCLI("ipv6 address 2000::2/120")
        s2.cmdCLI("exit")
        s2.cmdCLI("exit")

        #inputString = raw_input()

        cmdOut = s1.cmdCLI("show run")
        info('### Running config of s1 ### \n' + cmdOut)

        cmdOut = s2.cmdCLI("show run")
        info('### Running config of s2 ###\n' + cmdOut)

    def pingIPv4Target(self):
        ping_target_ip_set = False
        s1 = self.net.switches[0]
        s2 = self.net.switches[1]

        #Ping s2 from s1
        cmdOut = s1.cmdCLI("ping 10.0.10.2")
        for curLine in cmdOut.split('\n'):
            if 'PING 10.0.10.2 (10.0.10.2): 100 data bytes' in curLine:
                ping_target_ip_set = True

        info('\n\n')
        if ping_target_ip_set is True:
            info('### Ping from s1 to s2 is successful ###\n')
        else:
            info('### Ping from s1 to s2 is unsuccessful ###\n')

        #Ping s1 from s2
        ping_target_ip_set = False
        cmdOut = s1.cmdCLI("ping 10.0.10.1")
        for curLine in cmdOut.split('\n'):
            if 'PING 10.0.10.1 (10.0.10.1): 100 data bytes' in curLine:
                ping_target_ip_set = True

        info('\n')
        if ping_target_ip_set is True:
            info('### Ping from s2 to s1 is successful ###\n')
        else:
            info('### Ping from s2 to s1 is unsuccessful ###\n')

        #ping with multiple options
        ping_target_ip_set = False
        cmdOut = s1.cmdCLI("ping 10.0.10.1 data-fill dee datagram-size 200"
                           " interval 2 repetitions 1 timeout 2 tos 0")
        for curLine in cmdOut.split('\n'):
            if 'PING 10.0.10.1 (10.0.10.1): 200 data bytes' in curLine:
                ping_target_ip_set = True

        info('\n')
        if ping_target_ip_set is True:
            info('### Ping from s1 to s2 with multiple parameters '
                 'is successful ###\n')
        else:
            info('### Ping from s1 to s2 with multiple parameters '
                 'is unsuccessful ###\n')

    def pingIPv4TargetIpOption(self):
        ping_target_ip_set = False
        s1 = self.net.switches[0]
        s2 = self.net.switches[1]

        cmdOut = s1.cmdCLI("ping 10.0.10.1 ip-option record-route")
        for curLine in cmdOut.split('\n'):
            if 'RR: 	switch (10.0.10.1)' in curLine:
                ping_target_ip_set = True

        info('\n')
        if ping_target_ip_set is True:
            info('### Ping from s1 to s2 with record-route '
                 'ip-option is successful ###\n')
        else:
            info('### Ping from s1 to s2 with record-route '
                 'ip-option is unsuccessful ###\n')

        ping_target_ip_set = False
        cmdOut = s1.cmdCLI("ping 10.0.10.1 ip-option include-timestamp")
        for curLine in cmdOut.split('\n'):
            if 'TS:' in curLine:
                ping_target_ip_set = True

        info('\n')
        if ping_target_ip_set is True:
            info('### Ping from s1 to s2 with include-timestamp '
                 'ip-option is successful ###\n')
        else:
            info('### Ping from s1 to s2 with include-timestamp '
                 'ip-option is unsuccessful ###\n')

        ping_target_ip_set = False
        cmdOut = s2.cmdCLI("ping 10.0.10.2 "
                           "ip-option include-timestamp-and-address")
        for curLine in cmdOut.split('\n'):
            if 'TS:	switch (10.0.10.2)' in curLine:
                ping_target_ip_set = True

        info('\n')
        if ping_target_ip_set is True:
            info('### Ping from s2 to s1 with include-timestamp-and-address '
                 'ip-option is successful ### \n')
        else:
            info('### Ping from s2 to s1 with include-timestamp-and-address '
                 'ip-option is unsuccessful ###\n')

    def pingIPv6Target(self):
        ping_target_ipv6_set = False
        s1 = self.net.switches[0]
        s2 = self.net.switches[1]

        #Ping6 s2 from s1
        cmdOut = s1.cmdCLI("ping6 2000::2")
        for curLine in cmdOut.split('\n'):
            if 'PING 2000::2 (2000::2): 100 data bytes' in curLine:
                ping_target_ipv6_set = True

        info('\n')
        if ping_target_ipv6_set is True:
            info('### Ping6 from s1 to s2 is successful ###\n')
        else:
            info('### Ping6 from s1 to s2 is unsuccessful ###\n')

        #Ping6 s1 from s2
        cmdOut = s2.cmdCLI("ping6 2000::1")
        for curLine in cmdOut.split('\n'):
            if 'PING 2000::1 (2000::1): 100 data bytes' in curLine:
                ping_target_ipv6_set = True

        info('\n')
        if ping_target_ipv6_set is True:
            info('### Ping6 from s2 to s1 is successful ###\n')
        else:
            info('### Ping6 from s2 to s1 is unsuccessful ###\n')

        #ping6 with multiple options
        ping_target_ipv6_set = False
        cmdOut = s1.cmdCLI("ping6 2000::2 data-fill dee datagram-size 200"
                           " interval 2 repetitions 1")
        for curLine in cmdOut.split('\n'):
            if 'PING 2000::2 (2000::2):' and '200 data bytes' in curLine:
                ping_target_ipv6_set = True

        info('\n')
        if ping_target_ipv6_set is True:
            info('### Ping6 from s1 to s2 with multiple parameters '
                 'is successful ###\n')
        else:
            info('### Ping6 from s1 to s2 with multiple parameters '
                 'is unsuccessful ###\n')

        info('\n')


class Test_vtysh_ping:

    def setup_class(cls):
        # Create a test topology
        Test_vtysh_ping.pingTest = pingTest()

    def teardown_class(cls):
        # Stop the Docker containers, and
        # mininet topology
        Test_vtysh_ping.pingTest.net.stop()

    def test_pingAll(self):
        info('\n Test Ping Functionality \n')
        self.pingTest.configure()
        self.pingTest.pingIPv4Target()
        self.pingTest.pingIPv4TargetIpOption()
        self.pingTest.pingIPv6Target()

    def __del__(self):
        del self.pingTest

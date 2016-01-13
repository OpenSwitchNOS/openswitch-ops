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
import re
from  opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *
from opsvsi.docker import *
from opsvsi.opsvsitest import *

# The purpose of this test is to test that ntp config
# works as per the design and we receive the output as provided

SERVER1 = "1.1.1.1"
SERVER2 = "2.2.2.2"
SERVER3 = "3.3.3.3"
SERVER4 = "time.microsoft.com"


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.sws = sws
        # Add list of switches
        for s in irange(1, sws):
            switch = self.addSwitch('s%s' % s)

class ntpConfigTest(OpsVsiTest):

	def setupNet(self):
            self.net = Mininet(topo=myTopo(hsts=0, sws=1,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                                       switch=VsiOpenSwitch,
                                       host=Host,
                                       link=OpsVsiLink, controller=None,
                                       build=True)

	def ntpConfig(self):
            info('\n### Configure different ntp associations ###\n')
	    s1 = self.net.switches[0]
            s1.cmdCLI("configure terminal")
            s1.cmdCLI("ntp server 1.1.1.1" )
            s1.cmdCLI("ntp server 2.2.2.2" )
            s1.cmdCLI("ntp server 3.3.3.3 prefer")
            s1.cmdCLI("ntp server time.microsoft.com prefer version 4")
            s1.cmdCLI("exit")

	def testNtpAssociationsConfig(self):
            info('\n### Verify ntp associations table ###\n')
            s1 = self.net.switches[0]
            #parse the ntp associations command
            dump = s1.cmdCLI("show ntp associations")
            lines = dump.split('\n')
            count = 0
            for line in lines:
               if SERVER1 in line:
                  info("###found %s in db###\n" % SERVER1)
                  count = count + 1

               if SERVER2 in line:
                  info('###found %s in db###\n'% SERVER2)
                  count = count + 1

               if SERVER3 in line:
                  info('###found %s in db###\n'% SERVER3)
                  count = count + 1

               if SERVER4 in line:
                  info('###found %s in db###\n'% SERVER4)
                  count = count + 1

               assert count == 4, \
                   'tests are not successful\n'

            info('\n### testNtpAssociationsConfig: Test Passed ###\n')

class Test_ntp_config:

	def setup(self):
            pass

        def teardown(self):
            pass

        def setup_class(cls):
            Test_ntp_config.ntpConfigTest = ntpConfigTest()

        def teardown_class(cls):
            # Stop the Docker containers, and
            # mininet topology
            Test_ntp_config.ntpConfigTest.net.stop()

        def __del__(self):
            del self.ntpConfigTest

        def test_ntp_full(self):
            info('\n########## Test NTP configuration ##########\n')
            self.ntpConfigTest.ntpConfig()
            self.ntpConfigTest.testNtpAssociationsConfig()
            info('\n########## End of test NTP configuration configuration ##########\n')

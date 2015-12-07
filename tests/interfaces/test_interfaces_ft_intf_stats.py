# (C) Copyright 2015 Hewlett Packard Enterprise Development LP
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
# Test Plan for Interfaces:
#
# USER CONFIG
#
# Interface Statistics
#
# Verify Interface Statistics
#
# dut01: vtysh cmd:     configure terminal
# dut01: vtysh cmd:     vlan 10
# dut01: vtysh cmd:     no shutdown
# dut01: vtysh cmd:     exit
# dut01: vtysh cmd:     interface 2
# dut01: vtysh cmd:     no routing
# dut01: vtysh cmd:     vlan access 10
# dut01: vtysh cmd:     no shutdown
# dut01: vtysh cmd:     interface 1
# dut01: vtysh cmd:     no routing
# dut01: vtysh cmd:     vlan access 10
# dut01: vtysh cmd:     no shutdown
# dut01: vtysh cmd:     exit
# dut01: vtysh cmd:     exit
# dut01: vtysh cmd:     show interface 1
# dut01: vtysh cmd:     show interface 2
#      : verify   :     <collect baseline for stats>
# wrkston01: shell cmd: ping <to wrkston02 ip addr>
#      : action   :     sleep(5)
# dut01: vtysh cmd:     show interface 1
# dut01: vtysh cmd:     show interface 2
#      : verify   :     stats updated correctly
# wrkston02: shell cmd: ping <to wrkston01 ip addr>
#      : action   :     sleep(5)
# dut01: vtysh cmd:     show interface 1
# dut01: vtysh cmd:     show interface 2
#      : verify   :     stats updated correctly
#      : action   :     sleep(10)
# dut01: vtysh cmd:     show interface 1
# dut01: vtysh cmd:     show interface 2
#      : verify   :     stats not updated


import pytest
from opstestfw import *
from opstestfw.switch.CLI import *

# Topology definition

topoDict = {"topoType" : "physical",
            "topoExecution": 1000,
            "topoTarget": "dut01",
            "topoDevices": "dut01 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01, \
                          lnk02:dut01:wrkston02",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation",
            "topoLinkFilter": "lnk01:dut01:interface:1, \
                               lnk02:dut01:interface:2"}

STAT_SYNC_DELAY_SECS = 8
PING_BYTES = 128
PING_CNT = 10
RC_ERR_FMT = "vtysh exit code non-zero, %d"
NET_1 = "10.10.10"
WS1_IP = NET_1 + ".1"
WS2_IP = NET_1 + ".2"
NET1_MASK = "255.255.255.0"
NET1_BCAST = NET_1 + ".0"

class Test_template:

    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_template.testObj = testEnviron(topoDict=topoDict)
        Test_template.topoObj = Test_template.testObj.topoObjGet()

    def teardown_class(cls):
        # Terminate all nodes
        Test_template.topoObj.terminate_nodes()
        LogOutput('info', "Tearing Down Topology")

    def init_intf(self, obj, type="w"):
        if (type == "s"):
            rc = obj.cmd("ifconfig " + obj._intf + " " + obj._ip)
            rc = obj.cmd("ifconfig " + obj._intf + " netmask " + obj._netm)
            rc = obj.cmd("ifconfig " + obj._intf + " broadcast " + obj._bcast)
        else:
            rc = obj.NetworkConfig(ipAddr=obj._ip, netMask=obj._netm, \
                                   interface=obj._intf, \
                                   broadcast=obj._bcast, config=True)

    def init_devices(self):
        # Switch 1
        self.s1 = self.topoObj.deviceObjGet(device="dut01")

        # Reboot the switch
        LogOutput('info', "Rebooting the switch")
        self.s1.Reboot()

        # Workstation 1
        self.w1 = self.topoObj.deviceObjGet(device="wrkston01")
        self.w1._ip = WS1_IP
        self.w1._netm = NET1_MASK
        self.w1._bcast = NET1_BCAST
        self.w1._intf = "eth1"
        # Workstation 2
        self.w2 = self.topoObj.deviceObjGet(device="wrkston02")
        self.w2._ip = WS2_IP
        self.w2._netm = NET1_MASK
        self.w2._bcast = NET1_BCAST
        self.w2._intf = "eth1"

        # Bring up the interfaces
        LogOutput('info', "Bringup up w1 eth1")
        self.init_intf(self.w1)
        LogOutput('info', "Bringup up w2 eth1")
        self.init_intf(self.w2)

        LogOutput('info', "Device init complete")

    def open_vtysh(self):
        self.vtyconn = self.s1
        rc = self.vtyconn.VtyshShell()

    def close_vtysh(self):
        rc = self.vtyconn.VtyshShell(configOption="exit")

    def startup_sequence(self):
        # Setup devices
        LogOutput('info', "Setting up devices")
        self.init_devices()

        # Start vtysh session
        LogOutput('info', "Opening up vtysh session")
        self.open_vtysh()

    def verify_ping(self, src, dest, expected):
        out = src.Ping(ipAddr=dest._ip, interval=.2, errorCheck=False)

        if out is None:
            assert 1 == 0, "ping command failed, no output"

        LogOutput("info", "%s" % out.data)
        success = False;
        if out.data['packets_transmitted'] == out.data['packets_received']:
            success = True;

        assert success == expected, "ping was %s, expected %s" % (success, expected)

    def parse_stats(self, stats):
        lines = stats.splitlines()
        # Remove everything up to "RX"
        found = False
        for line in lines[:]:
            lines.remove(line)
            if " RX" in line:
                found = True
                break

        if not found:
            assert 1 == 0, "parse_stats failed...no RX found. Line is [%s]\nLines is [%s]" % (line, lines)

        mydict = {}
        try:
            data = lines[0].split()
        except Exception as e:
            assert 1 == 0, "Invalid stats: exception error is %s" % e

        mydict["rx_packets"] = int(data[0])
        mydict["rx_bytes"] = int(data[3])
        data = lines[1].split()
        mydict["rx_error"] = int(data[0])
        mydict["rx_dropped"] = int(data[3])
        data = lines[2].split()
        mydict["rx_crc"] = int(data[0])

        data = lines[4].split()
        mydict["tx_packets"] = int(data[0])
        mydict["tx_bytes"] = int(data[3])
        data = lines[5].split()
        mydict["tx_error"] = int(data[0])
        mydict["tx_dropped"] = int(data[3])
        data = lines[6].split()
        mydict["tx_collision"] = int(data[0])

        return mydict

    def baseline_stats(self):
        i1 = self.vtyconn.cmd("show interface 1")
        self.i1_stat = self.parse_stats(i1)

    def verify_stats(self, incr=True):
        i1 = self.vtyconn.cmd("show interface 1")
        i1_new = self.parse_stats(i1)

        # Per request, will put retry loops around tx and rx stats.
        # Verify RX bytes
        for iteration in range(0, 5):
            if (i1_new['rx_bytes'] - self.i1_stat['rx_bytes']) >= \
                (PING_CNT * PING_BYTES):
                break
            LogOutput('info',
                      "Retrying statistic - waiting for rx_bytes to update")
            Sleep(seconds=5, message="\nWaiting")
            # grab stats again
            i1 = self.vtyconn.cmd("show interface 1")
            i1_new = self.parse_stats(i1)
        # If we have hit this assert, we have an issue
        assert (i1_new['rx_bytes'] - self.i1_stat['rx_bytes']) >= \
                (PING_CNT * PING_BYTES), \
                "rx_bytes wrong. Was %d, is %d" % (self.i1_stat['rx_bytes'], \
                                                   i1_new['rx_bytes'])

        # Verify TX bytes
        for iteration in range(0, 5):
            if (i1_new['tx_bytes'] - self.i1_stat['tx_bytes']) >= \
                (PING_CNT * PING_BYTES):
                break;
            LogOutput('info',
                      "Retrying statistic - waiting for tx_bytes to update")
            Sleep(seconds=5, message="\nWaiting")
            # grab stats again
            i1 = self.vtyconn.cmd("show interface 1")
            i1_new = self.parse_stats(i1)

        # If we have hit this assert, we have an issue
        assert (i1_new['tx_bytes'] - self.i1_stat['tx_bytes']) >= \
                (PING_CNT * PING_BYTES), \
                "tx_bytes wrong. Was %d, is %d" % (self.i1_stat['tx_bytes'], \
                                                   i1_new['tx_bytes'])

        # Verify RX packets
        for iteration in range(0, 5):
            if (i1_new['rx_packets'] - self.i1_stat['rx_packets']) >= PING_CNT:
                break
            LogOutput('info',
                      "Retrying statistic - waiting for rx_packets to update")
            Sleep(seconds=5, message="\nWaiting")
            # grab stats again
            i1 = self.vtyconn.cmd("show interface 1")
            i1_new = self.parse_stats(i1)
        # If we have hit this assert, we have an issue
        assert (i1_new['rx_packets'] - self.i1_stat['rx_packets']) >= PING_CNT, \
                "rx_packets wrong. Was %d, is %d" % (self.i1_stat['rx_packets'], \
                                                   i1_new['rx_packets'])

        # Verify TX packets
        for iteration in range(0, 5):
            if (i1_new['tx_packets'] - self.i1_stat['tx_packets']) >= PING_CNT:
                break
            LogOutput('info',
                      "Retrying statistic - waiting for tx_packets to update")
            Sleep(seconds=5, message="\nWaiting")
            # grab stats again
            i1 = self.vtyconn.cmd("show interface 1")
            i1_new = self.parse_stats(i1)
        # If we have hit this assert, we have an issue
        assert (i1_new['tx_packets'] - self.i1_stat['tx_packets']) >= PING_CNT, \
                "tx_packets wrong. Was %d, is %d" % (self.i1_stat['tx_packets'], \
                                                   i1_new['tx_packets'])

        # Verify RX error
        assert i1_new['rx_error'] == self.i1_stat['rx_error'], \
                "rx_error wrong. Was %d, is %d" % (self.i1_stat['rx_error'], \
                                                   i1_new['rx_error'])

        # Verify TX error
        assert i1_new['tx_error'] == self.i1_stat['tx_error'], \
                "tx_error wrong. Was %d, is %d" % (self.i1_stat['tx_error'], \
                                                   i1_new['tx_error'])

        # Verify RX dropped
        assert i1_new['rx_dropped'] == self.i1_stat['rx_dropped'], \
                "rx_dropped wrong. Was %d, is %d" % (self.i1_stat['rx_dropped'], \
                                                   i1_new['rx_dropped'])

        # Verify TX dropped
        assert i1_new['tx_dropped'] == self.i1_stat['tx_dropped'], \
                "tx_dropped wrong. Was %d, is %d" % (self.i1_stat['tx_dropped'], \
                                                   i1_new['tx_dropped'])

        # Verify RX CRC
        assert i1_new['rx_crc'] == self.i1_stat['rx_crc'], \
                "rx_crc wrong. Was %d, is %d" % (self.i1_stat['rx_crc'], \
                                                   i1_new['rx_crc'])

        # Verify TX collision
        assert i1_new['tx_collision'] == self.i1_stat['tx_collision'], \
                "tx_collision wrong. Was %d, is %d" % (self.i1_stat['tx_collision'], \
                                                   i1_new['tx_collision'])

    def cmd_set_1(self, obj):
        # Issue "configure terminal" command
        LogOutput("info", "sending configure terminal")
        rc = obj.cmd("configure terminal")
        LogOutput("info", "sending vlan 10")
        rc = obj.cmd("vlan 10")
        LogOutput("info", "sending no shutdown")
        rc = obj.cmd("no shutdown")
        LogOutput("info", "sending exit")
        rc = obj.cmd("exit")
        LogOutput("info", "sending interface 2")
        rc = obj.cmd("interface 2")
        LogOutput("info", "sending no routing")
        rc = obj.cmd("no routing")
        LogOutput("info", "sending vlan access 10")
        rc = obj.cmd("vlan access 10")
        LogOutput("info", "sending no shutdown")
        rc = obj.cmd("no shutdown")
        LogOutput("info", "sending interface 1")
        rc = obj.cmd("interface 1")
        LogOutput("info", "sending no routing")
        rc = obj.cmd("no routing")
        LogOutput("info", "sending vlan access 10")
        rc = obj.cmd("vlan access 10")

    def test_statistics(self):
        # Get everything initially configured
        LogOutput('info', "*****Testing statistics*****")
        self.startup_sequence()

        # Configure interfaces 1 & 2 on vlan 10, with 1 down and 2 up.
        LogOutput('info', "Cfg intfs 1 & 2 on vlan 10, with 1 down and 2 up")
        self.cmd_set_1(self.vtyconn)

        # Bring up interface 1
        LogOutput('info', "Bring intf 1 up")
        rc = self.vtyconn.cmd("no shutdown")

        # Back out to CLI main
        rc = self.vtyconn.cmd("exit")
        rc = self.vtyconn.cmd("exit")

        Sleep(seconds=10, message="\nWaiting")
        # Baseline the statistics
        LogOutput('info', "Baselining the statistics")
        self.baseline_stats()

        # Ping w2->w3, switch port 1 to switch port 2.
        LogOutput('info', "Ping w2->w3")
        self.verify_ping(self.w1, self.w2, True)

        # Verify stats are correctly updated.
        sleep(STAT_SYNC_DELAY_SECS)
        LogOutput('info', "Verify stats are correctly updated")
        self.verify_stats(incr=True)

        # Baseline the statistics
        LogOutput('info', "Baselining the statistics")
        self.baseline_stats()

        # Ping w3->w2, switch port 1 to switch port 2.
        LogOutput('info', "Ping w3->w2")
        self.verify_ping(self.w2, self.w1, True)

        # Verify stats are correctly updated.
        sleep(STAT_SYNC_DELAY_SECS)
        LogOutput('info', "Verify stats are correctly updated")
        self.verify_stats(incr=True)

        LogOutput('info', "succeeded!")

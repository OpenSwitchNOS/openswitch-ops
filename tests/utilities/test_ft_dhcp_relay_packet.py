#!/usr/bin/python

# (c) Copyright 2016 Hewlett Packard Enterprise Development LP
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
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *

#
# The purpose of this test is to test
# functionality of DHCP-Relay

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02 dut03",
            "topoDevices": "dut01 dut02 dut03 ",
            "topoLinks": "lnk01:dut01:dut02,lnk02:dut02:dut03",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch"}


def configure_server(server):

    LogOutput('info', "Configure DHCP server")

    #Entering vtysh server
    retStruct = server.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    devIntRetStruct = server.DeviceInteract(command="conf t")
    devIntRetStruct = server.DeviceInteract(command="dhcp-server")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enable dhcp-server"

    cmd = "range pool1 start-ip-address 20.0.0.100 end-ip-address 20.0.0.200 \
          netmask 255.0.0.0 broadcast 20.255.255.255 lease-duration 5"
    devIntRetStruct = server.DeviceInteract(command=cmd)
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to configure ip pool1"

    devIntRetStruct = server.DeviceInteract(command="exit")
    devIntRetStruct = server.DeviceInteract(command="exit")

    #Exit vtysh server
    retStruct = server.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    return True


def configure(**kwargs):

    client = kwargs.get('switch1', None)
    relay = kwargs.get('switch2', None)
    server = kwargs.get('switch3', None)

    #Enabling interface 1 on client
    LogOutput('info', "Enabling interface 1 on client")
    retStruct = InterfaceEnable(deviceObj=client, enable=True,
                                interface=client.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 1 on dhcp relay"

    #Entering interface for link 1 client giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 1 client")
    retStruct = InterfaceIpConfig(deviceObj=client,
                                  interface=client.linkPortMapping['lnk01'],
                                  addr="20.0.0.1", mask=8, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Enabling interface 1 on dhcp relay
    LogOutput('info', "Enabling interface 1 on dhcp relay")
    retStruct = InterfaceEnable(deviceObj=relay, enable=True,
                                interface=relay.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 1 on dhcp relay"

    #Entering interface for link 1 dhcp relay, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 1 dhcp relay")
    retStruct = InterfaceIpConfig(deviceObj=relay,
                                  interface=relay.linkPortMapping['lnk01'],
                                  addr="20.0.0.2", mask=8, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Enabling interface 2 on dhcp relay
    LogOutput('info', "Enabling interface 2 on dhcp relay")
    retStruct = InterfaceEnable(deviceObj=relay, enable=True,
                                interface=relay.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 2 on dhcp relay"

    #Entering interface for link 2 dhcp relay, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 2 dhcp relay")
    retStruct = InterfaceIpConfig(deviceObj=relay,
                                  interface=relay.linkPortMapping['lnk02'],
                                  addr="10.0.10.1", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Enabling interface 1 on server
    LogOutput('info', "Enabling interface 1 on server")
    retStruct = InterfaceEnable(deviceObj=server, enable=True,
                                interface=server.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 1 on server"

    #Entering interface for link 2 server 1, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 2 server")
    retStruct = InterfaceIpConfig(deviceObj=server,
                                  interface=server.linkPortMapping['lnk02'],
                                  addr="10.0.10.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Configuring static routes on server and host
    LogOutput('info', "Configuring static IPv4 route on server to client")
    retStruct = IpRouteConfig(deviceObj=server, route="20.0.0.0", mask=8,
                              nexthop="10.0.10.1", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure static IPv4 route on server to client"

    LogOutput('info', "Configuring static IPv4 route on client to server")
    retStruct = IpRouteConfig(deviceObj=client, route="10.0.10.0", mask=24,
                              nexthop="20.0.0.2", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure static IPv4 route on client to server"

    #Entering vtysh dhcp relay
    retStruct = relay.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    LogOutput('info', "configure helper ip address on dhcp relay")
    devIntRetStruct = relay.DeviceInteract(command="conf t")
    devIntRetStruct = relay.DeviceInteract(command="int 1")
    devIntRetStruct = relay.DeviceInteract(command="ip helper-address"
                                           " 10.0.10.2")
    devIntRetStruct = relay.DeviceInteract(command="exit")
    devIntRetStruct = relay.DeviceInteract(command="exit")

    retStruct = client.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    #Entering vtysh server
    retStruct = server.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    LogOutput('info', "sh run on relay")
    devIntRetStruct = relay.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)

    LogOutput('info', "sh run on client")
    devIntRetStruct = client.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)

    LogOutput('info', "sh run on server")
    devIntRetStruct = server.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)

    LogOutput('info', "Ping from server to client")
    devIntRetStruct = server.DeviceInteract(command="ping 20.0.0.1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from server to client"

    retBuffer = devIntRetStruct.get('buffer')
    print retBuffer
    assert '0% packet loss' in retBuffer, "Ping"
    " from server to client failed"

    #Exit vtysh prompt
    retStruct = relay.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    retStruct = server.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    retStruct = client.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    if configure_server(server) is False:
        return False

    return True


def send_discover_packet(client):

    filename = '/tmp/packet.py'

    cmd = "echo -E " + '"'
    cmd = cmd + r"""
#!/usr/bin/env python
import socket
import struct
from uuid import getnode as get_mac
from random import randint

def getMacInBytes():
    mac = str(hex(get_mac()))
    mac = mac[2:]
    while len(mac) < 12 :
        mac = '0' + mac
    macb = b''
    for i in range(0, 12, 2) :
        m = int(mac[i:i + 2], 16)
        macb += struct.pack('!B', m)
    return macb

class DHCPDiscover:
    def __init__(self):
        self.transactionID = b''
        for i in range(4):
            t = randint(0, 255)
            self.transactionID += struct.pack('!B', t)

    def buildPacket(self):
        macb = getMacInBytes()
        packet = b''
        packet += b'\x01'   #Message type: Boot Request (1)
        packet += b'\x01'   #Hardware type: Ethernet
        packet += b'\x06'   #Hardware address length: 6
        packet += b'\x00'   #Hops: 0
        packet += self.transactionID       #Transaction ID
        packet += b'\x00\x00'    #Seconds elapsed: 0
        packet += b'\x80\x00'   #Bootp flags: 0x8000 (Broadcast) + reserved flags
        packet += b'\x00\x00\x00\x00'   #Client IP address: 0.0.0.0
        packet += b'\x00\x00\x00\x00'   #Your (client) IP address: 0.0.0.0
        packet += b'\x00\x00\x00\x00'   #Next server IP address: 0.0.0.0
        packet += b'\x00\x00\x00\x00'   #Relay agent IP address: 0.0.0.0
        #packet += b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
        packet += macb
        packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
        packet += b'\x00' * 67  #Server host name not given
        packet += b'\x00' * 125 #Boot file name not given
        packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
        packet += b'\x35\x01\x01'   #Option: (t=53,l=1) DHCP Message Type = DHCP Discover
        #packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'   #Option: (t=61,l=6) Client identifier
        packet += b'\x3d\x06' + macb
        packet += b'\x37\x03\x03\x01\x06'   #Option: (t=55,l=3) Parameter Request List
        packet += b'\xff'   #End Option
        return packet

if __name__ == '__main__':
    #defining the socket
    dhcps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #internet, UDP
    dhcps.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #broadcast

    try:
        dhcps.bind(('20.0.0.1', 68))    #we want to send from port 68
    except Exception as e:
        print('port 68 in use...')
        dhcps.close()

    #building and sending the DHCPDiscover packet
    discoverPacket = DHCPDiscover()
    dhcps.sendto(discoverPacket.buildPacket(), ('<broadcast>', 67))
    print('DHCP Discover sent.\n')
    dhcps.close()   #we close the socket '"""
    cmd = cmd + '" > ' + filename

    cmdOut = client.cmd(cmd)
    cmdOut = client.cmd("ip netns exec swns python /tmp/packet.py")
    assert 'DHCP Discover sent.' in cmdOut, " Sending discover packet failed"

    #cmdOut = client.cmd("rm /tmp/packet.py")

    return True


def helper_address_configuration(**kwargs):

    client = kwargs.get('switch1', None)
    relay = kwargs.get('switch2', None)

    if send_discover_packet(client) is False:
        return False

    # TODO : check packet count
    #unconfigure helper address
    retStruct = relay.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    LogOutput('info', "unconfigure helper ip address on dhcp relay")
    devIntRetStruct = relay.DeviceInteract(command="conf t")
    devIntRetStruct = relay.DeviceInteract(command="int 1")
    devIntRetStruct = relay.DeviceInteract(command="no ip helper-address"
                                           " 10.0.10.2")
    devIntRetStruct = relay.DeviceInteract(command="exit")
    devIntRetStruct = relay.DeviceInteract(command="exit")

    retStruct = relay.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    if send_discover_packet(client) is False:
        return False

    # TODO : check packet count
    return True


class Test_dhcp_relay_configuration:

    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_dhcp_relay_configuration.testObj = testEnviron(topoDict=topoDict)
        #Get topology object
        Test_dhcp_relay_configuration.topoObj = \
            Test_dhcp_relay_configuration.testObj.topoObjGet()

    #def teardown_class(cls):
        #Test_dhcp_relay_configuration.topoObj.terminate_nodes()

    def test_configure(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        if configure(switch1=dut01Obj,
                     switch2=dut02Obj, switch3=dut03Obj) is True:
            LogOutput('info', "dhcp relay config success")
        else:
            LogOutput('info', "dhcp relay config failed")

    def test_helper_address_configuration(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        if helper_address_configuration(switch1=dut01Obj,
           switch2=dut02Obj, switch3=dut03Obj) is True:
            LogOutput('info', "helper address configuration config success")
        else:
            LogOutput('info', "helper address configuration config failed")

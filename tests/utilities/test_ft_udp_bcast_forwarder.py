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
from socket import *

#
# The purpose of this script is to test
# functionality of UDP Broadcast Forwarder

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02 dut03 dut04",
            "topoDevices": "dut01 dut02 dut03 dut04",
            "topoLinks": "lnk01:dut01:dut02,lnk02:dut02:dut03,\
                          lnk03:dut02:dut04",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch,\
                            dut04:system-category:switch"}


def enterConfigShell(dut01):
    retStruct = dut01.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    retStruct = dut01.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    return True


def exitContext(dut01):
    retStruct = dut01.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit config terminal"

    retStruct = dut01.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    return True


# Configures the multiple switches required for the test cases
# to be performed
def configure(**kwargs):
    client = kwargs.get('switch1', None)
    forwarder = kwargs.get('switch2', None)
    server1 = kwargs.get('switch3', None)
    server2 = kwargs.get('switch4', None)

    # Client configuration
    LogOutput('info', "Configuring client")

    # Enable interface 1 on client
    LogOutput('info', "Enabling interface 1 on client")
    retStruct = InterfaceEnable(deviceObj=client, enable=True,
                                interface=client.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Enable interface 1 on client failed"

    # Entering interface for link 1 client, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 1 client")
    retStruct = InterfaceIpConfig(deviceObj=client,
                                  interface=client.linkPortMapping['lnk01'],
                                  addr="10.0.0.1", mask=8, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"
    devIntRetStruct = client.DeviceInteract(command="end")

    # Enable interface 1 on forwarder
    LogOutput('info', "Enabling interface 1 on forwarder")
    retStruct = InterfaceEnable(deviceObj=forwarder, enable=True,
                                interface=forwarder.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Enable interface 1 on forwarder failed"

    # Entering interface for link 1 forwarder, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 1 forwarder")
    retStruct = InterfaceIpConfig(deviceObj=forwarder,
                                  interface=forwarder.linkPortMapping['lnk01'],
                                  addr="10.0.0.2", mask=8, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    # Enable interface 2 on forwarder
    LogOutput('info', "Enabling interface 2 on forwarder")
    retStruct = InterfaceEnable(deviceObj=forwarder, enable=True,
                                interface=forwarder.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Enable interface 2 on forwarder failed"

    # Entering interface for link 2 forwarder, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 2 forwarder")
    retStruct = InterfaceIpConfig(deviceObj=forwarder,
                                  interface=forwarder.linkPortMapping['lnk02'],
                                  addr="10.0.1.1", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    # Enable interface 3 on forwarder
    LogOutput('info', "Enabling interface 3 on forwarder")
    retStruct = InterfaceEnable(deviceObj=forwarder, enable=True,
                                interface=forwarder.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Enable interface 3 on forwarder failed"

    # Entering interface for link 3 forwarder, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 3 forwarder")
    retStruct = InterfaceIpConfig(deviceObj=forwarder,
                                  interface=forwarder.linkPortMapping['lnk03'],
                                  addr="10.0.2.1", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"
    devIntRetStruct = forwarder.DeviceInteract(command="end")

    # Enable interface 1 on server 1
    LogOutput('info', "Enabling interface 1 on server 1")
    retStruct = InterfaceEnable(deviceObj=server1, enable=True,
                                interface=server1.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Enable interface 1 on server 1 failed"

    # Entering interface for link 2 server 1, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 2 server 1")
    retStruct = InterfaceIpConfig(deviceObj=server1,
                                  interface=server1.linkPortMapping['lnk02'],
                                  addr="10.0.1.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"
    devIntRetStruct = server1.DeviceInteract(command="end")

    # Enabling interface 1 on server 2
    LogOutput('info', "Enabling interface 1 on server 2")
    retStruct = InterfaceEnable(deviceObj=server2, enable=True,
                                interface=server2.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Enable interface 1 on server 2 failed"

    # Entering interface for link 3 server 2, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 3 server 2")
    retStruct = InterfaceIpConfig(deviceObj=server2,
                                  interface=server2.linkPortMapping['lnk03'],
                                  addr="10.0.2.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"
    devIntRetStruct = server2.DeviceInteract(command="end")

    # Entering vtysh client
    retStruct = client.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering vtysh forwarder
    retStruct = forwarder.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering vtysh server 1
    retStruct = server1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering vtysh server 2
    retStruct = server2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Verify the show running outputs
    LogOutput('info', "show run on client")
    cmd = "show running-config"
    devIntRetStruct = client.DeviceInteract(command=cmd)
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)
    assert '10.0.0.1' in retBuffer, \
           "Client configuration verification failed"

    LogOutput('info', "show run on forwarder")
    devIntRetStruct = forwarder.DeviceInteract(command=cmd)
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)
    assert '10.0.0.2' in retBuffer and \
           '10.0.1.1' in retBuffer and \
           '10.0.2.1' in retBuffer, \
           "Forwarder configuration verification failed"

    LogOutput('info', "show run on server 1")
    devIntRetStruct = server1.DeviceInteract(command=cmd)
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)
    assert '10.0.1.2' in retBuffer, \
           "Server1 configuration verification failed"

    LogOutput('info', "show run on server 2")
    devIntRetStruct = server2.DeviceInteract(command=cmd)
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)
    assert '10.0.2.2' in retBuffer, \
           "Server2 configuration verification failed"

    # Configure a static route on the servers
    cmd = "ip route 10.0.0.0/24 10.0.1.1"
    server1.DeviceInteract(command="configure terminal")
    devIntReturn = server1.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to setup a ip route"
    server1.DeviceInteract(command="end")

    cmd = "ip route 10.0.0.0/24 10.0.2.1"
    server2.DeviceInteract(command="configure terminal")
    devIntReturn = server2.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to setup a ip route"
    server2.DeviceInteract(command="end")

    # Exit vtysh on client
    retStruct = client.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Exit vtysh on forwarder
    retStruct = forwarder.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Exit vtysh on server1
    retStruct = server1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Exit vtysh server 2
    retStruct = server2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Create the scripts required
    create_udpreceiver_script_file(server=server1)
    create_udpreceiver_script_file(server=server2)
    create_udpgenerate_script_file(client=client)

    # Start listening on the server1 for all UDP protocols
    server_listen(server=server1, udp_dport=53,
                    clientIP='10.0.0.1', serverIP='10.0.1.2')
    server_listen(server=server1, udp_dport=123,
                    clientIP='10.0.0.1', serverIP='10.0.1.2')
    server_listen(server=server1, udp_dport=137,
                    clientIP='10.0.0.1', serverIP='10.0.1.2')
    server_listen(server=server1, udp_dport=138,
                    clientIP='10.0.0.1', serverIP='10.0.1.2')
    server_listen(server=server1, udp_dport=1812,
                    clientIP='10.0.0.1', serverIP='10.0.1.2')
    server_listen(server=server1, udp_dport=1645,
                    clientIP='10.0.0.1', serverIP='10.0.1.2')
    server_listen(server=server1, udp_dport=520,
                    clientIP='10.0.0.1', serverIP='10.0.1.2')
    server_listen(server=server1, udp_dport=161,
                    clientIP='10.0.0.1', serverIP='10.0.1.2')
    server_listen(server=server1, udp_dport=162,
                    clientIP='10.0.0.1', serverIP='10.0.1.2')
    server_listen(server=server1, udp_dport=69,
                    clientIP='10.0.0.1', serverIP='10.0.1.2')
    server_listen(server=server1, udp_dport=37,
                    clientIP='10.0.0.1', serverIP='10.0.1.2')

    # Start listening on server2 for only the UDP protocols that will
    # be configured later
    server_listen(server=server2, udp_dport=53,
                  clientIP='10.0.0.1', serverIP='10.0.2.2')
    server_listen(server=server2, udp_dport=161,
                  clientIP='10.0.0.1', serverIP='10.0.2.2')

    return True


# Create script file that generates UDP bcast packets on the client machine
def create_udpgenerate_script_file(**kwargs):
    client = kwargs.get('client', None)

    filename = "/tmp/packet.py"
    cmd = "echo -E " + '"'
    cmd = cmd + r"""
#!/usr/bin/env python
import socket
import struct
import sys

port = sys.argv[1]
count = int(sys.argv[2])
# Sending the packet
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #broadcast
sock.bind(('10.0.0.1', 8888))
sock.settimeout(2)
while (count):
    sock.sendto('This is a dummy udp packet', ('<broadcast>', int(port)))
    count -= 1
sock.close()"""

    cmd = cmd + '" > ' + filename
    cmdOut = client.cmd(cmd)

    return


# Create UDP receiver script file on the server
def create_udpreceiver_script_file(**kwargs):
    server = kwargs.get('server', None)

    filename = '/tmp/recv.py'
    cmd = "echo -E " + '"'
    cmd = cmd + r"""
import socket
import sys

if __name__ == '__main__':

    # getting the output file name
    port = sys.argv[1]
    client = sys.argv[2]
    server = sys.argv[3]

    #defining the socket
    count = 0
    recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #internet, UDP
    recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse of the IP
    recv.bind((str(server), int(port)))

    path = '/tmp/'+ str(port)
    f = open(path, 'w')
    line = str(count)
    f.write(line)
    f.write('\n')
    f.close()

    while True:
        data, addr = recv.recvfrom(1024) # buffer size is 1024 bytes
        if (addr[0] == client) :
            count += 1
            f = open(path, 'w')
            line = str(count)
            f.write(line)
            f.write('\n')
            f.close()

    recv.close()   #we close the socket '"""
    cmd = cmd + '" > ' + filename
    cmdOut = server.cmd(cmd)

    return


# Generate UDP broadcast packets from client
def generate_packets(**kwargs):
    client = kwargs.get('client', None)
    udp_dport = kwargs.get('udp_dport', None)
    count = kwargs.get('count', None)

    filename = "/tmp/packet.py"
    cmd = "ip netns exec swns python "+filename+" "+str(udp_dport) + " " + str(count)
    cmdOut = client.cmd(cmd)

    return True


# Listen for packets on the server
def server_listen(**kwargs):
    # Listens on particular UDP port in the socket
    server = kwargs.get('server', None)
    udp_dport = kwargs.get('udp_dport', None)
    clientIP = kwargs.get('clientIP', None)
    serverIP = kwargs.get('serverIP', None)

    filename = "/tmp/recv.py"
    cmd = "ip netns exec swns python " + filename+ " " \
          + str(udp_dport) + " " + str(clientIP) + " " + str(serverIP) + " &"
    cmdOut = server.cmd(cmd)

    return True


# To find out the count of forwarded packets
# recieved for the specific UDP protocol
def getpacket_count(**kwargs):
    server = kwargs.get('server', None)
    port = kwargs.get('udp_dport', None)

    filename = '/tmp/' + str(port)
    cmd = 'cat ' + filename
    devIntReturn = server.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "File not found"
    retBuffer = devIntReturn.get('buffer')
    assert "No such file or directory" not in retBuffer, \
           "File not found..!!!!"

    # Get the count value
    line = retBuffer.split('\n')
    lines = line[1].split('\r')
    count = int(lines[0])

    return count


# Configure an UDP forward protocol
# Transmit the broadcast packet from client
# Listen for the respective protocol packet
# at the server and validate the broadcast packet
# reception
def udp_forward_protocol_config(**kwargs):
    client = kwargs.get('client', None)
    forwarder = kwargs.get('forwarder', None)
    server = kwargs.get('server', None)
    serverIP = kwargs.get('serverIP', None)
    udp_dport = kwargs.get('udp_dport', None)
    interface = kwargs.get('interface', None)
    no_of_pkts = kwargs.get('no_of_pkts', None)
    check = kwargs.get('check', None)

    positive = 'pos'
    negative = 'neg'
    cmdI = "interface "+interface
    cmd = "ip forward-protocol udp "+serverIP+" "+str(udp_dport)
    # Configure UDP forward protocol
    if (enterConfigShell(forwarder) is False):
        return False

    devIntReturn = forwarder.DeviceInteract(command=cmdI)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter Interface context"

    devIntReturn = forwarder.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to configure UDP " \
                         "forward-protocol"

    # cache the count
    prev_count = getpacket_count(server=server, udp_dport=udp_dport)

    # Create a pkt from the client and send it to the forwarder
    generate_packets(client=client, udp_dport=udp_dport, count=no_of_pkts)

    # Validate the output
    cur_count = getpacket_count(server=server, udp_dport=udp_dport)

    if (check == positive):
        # Positive validation
        if ((cur_count - prev_count) != no_of_pkts):
            assert "Test Failed..!!!!"
    else:
        # Negative validation
        if ((cur_count - prev_count) == no_of_pkts):
            assert "Test Failed..!!!!"

    # Unconfigure UDP forward protocol
    cmd = "no ip forward-protocol udp "+serverIP+" "+str(udp_dport)
    devIntReturn = forwarder.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to unconfigure UDP " \
                         "forward-protocol"

    forwarder.DeviceInteract(command="exit")

    if (exitContext(forwarder) is False):
        return False

    return True


# Verify the broadcast packets are not forwarded when UDP
# forwarding is globally disabled
def udp_bcast_forwarder_no_global(**kwargs):
    client = kwargs.get('switch1', None)
    forwarder = kwargs.get('switch2', None)
    server = kwargs.get('switch3', None)

    # Global UDP Broadcast Forwarding is disabled by default
    # Disable it again to be double sure
    if (enterConfigShell(forwarder) is False):
        return False

    cmd = "no ip udp-bcast-forward"
    devIntReturn = forwarder.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to disable the global " \
                         "UDP broadcast forwarding"

    if(exitContext(forwarder)) is False:
        return False

    # Configure a UDP forward protocol for dns and verify
    # the packet forwarding is not happening
    if ((udp_forward_protocol_config(client=client, forwarder=forwarder,
         server=server, serverIP="10.0.1.2", udp_dport=53, interface="1",
         no_of_pkts=10, check='neg')) is False):
        LogOutput('error', "Broadcast of packet succeeded even when "
                           "UDP forwarding is globally disabled")
        return False

    # Unconfigure
    # Enable the global UDP broadcast forwarding
    if (enterConfigShell(forwarder) is False):
        return False

    cmd = "ip udp-bcast-forward"
    devIntReturn = forwarder.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enable the global " \
                         "UDP broadcast forwarding"

    if(exitContext(forwarder)) is False:
        return False

    return True


# Verify all the supported UDP protocols
def udp_bcast_forwarder_config_protocols(**kwargs):
    client = kwargs.get('switch1', None)
    forwarder = kwargs.get('switch2', None)
    server = kwargs.get('switch3', None)

    # Configure UDP forward-protocols for different UDP protocols
    if (enterConfigShell(forwarder) is False):
        return False

    # Enable the global UDP broadcast forwarding
    cmd = "ip udp-bcast-forward"
    devIntReturn = forwarder.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enable the global " \
                         "UDP broadcast forwarding"

    if (exitContext(forwarder) is False):
        return False

    # UDP forward-protocol - dns
    if ((udp_forward_protocol_config(client=client, forwarder=forwarder,
         server=server, serverIP="10.0.1.2", udp_dport=53, interface="1",
         no_of_pkts=10, check='pos')) is False):
        LogOutput('error', "UDP forward protocol for dns failed")
        return False

    LogOutput('info', "UDP forward-protocol for dns succeeded")

    # UDP forward-protocol - ntp
    if ((udp_forward_protocol_config(client=client, forwarder=forwarder,
         server=server, serverIP="10.0.1.2", udp_dport=123, interface="1",
         no_of_pkts=10, check='pos')) is False):
        LogOutput('error', "UDP forward protocol for ntp failed")
        return False

    LogOutput('info', "UDP forward-protocol for ntp succeeded")

    # UDP forward-protocol -  netbios-ns
    if ((udp_forward_protocol_config(client=client, forwarder=forwarder,
         server=server, serverIP="10.0.1.2", udp_dport=137, interface="1",
         no_of_pkts=10, check='pos')) is False):
        LogOutput('error', "UDP forward protocol for netbios-ns failed")
        return False

    LogOutput('info', "UDP forward-protocol for netbios-ns succeeded")

    # UDP forward-protocol - netbios-dgm
    if ((udp_forward_protocol_config(client=client, forwarder=forwarder,
         server=server, serverIP="10.0.1.2", udp_dport=138, interface="1",
         no_of_pkts=10, check='pos')) is False):
        LogOutput('error', "UDP forward protocol for netbios-dgm failed")
        return False

    LogOutput('info', "UDP forward-protocol for netbios-dgm succeeded")

    # UDP forward-protocol - radius
    if ((udp_forward_protocol_config(client=client, forwarder=forwarder,
         server=server, serverIP="10.0.1.2", udp_dport=1812, interface="1",
         no_of_pkts=10, check='pos')) is False):
        LogOutput('error', "UDP forward protocol for radius failed")
        return False

    LogOutput('info', "UDP forward-protocol for radius succeeded")

    # UDP forward-protocol - radius-old
    if ((udp_forward_protocol_config(client=client, forwarder=forwarder,
         server=server, serverIP="10.0.1.2", udp_dport=1645, interface="1",
         no_of_pkts=10, check='pos')) is False):
        LogOutput('error', "UDP forward protocol for radius-old failed")
        return False

    LogOutput('info', "UDP forward-protocol for radius-old succeeded")

    # UDP forward-protocol - rip
    if ((udp_forward_protocol_config(client=client, forwarder=forwarder,
         server=server, serverIP="10.0.1.2", udp_dport=520, interface="1",
         no_of_pkts=10, check='pos')) is False):
        LogOutput('error', "UDP forward protocol for rip failed")
        return False

    LogOutput('info', "UDP forward-protocol for rip succeeded")

    # UDP forward-protocol - snmp
    if ((udp_forward_protocol_config(client=client, forwarder=forwarder,
         server=server, serverIP="10.0.1.2", udp_dport=161, interface="1",
         no_of_pkts=10, check='pos')) is False):
        LogOutput('error', "UDP forward protocol for snmp failed")
        return False

    LogOutput('info', "UDP forward-protocol for snmp succeeded")

    # UDP forward-protocol - snmp-trap
    if ((udp_forward_protocol_config(client=client, forwarder=forwarder,
         server=server, serverIP="10.0.1.2", udp_dport=162, interface="1",
         no_of_pkts=10, check='pos')) is False):
        LogOutput('error', "UDP forward protocol for snmp-trap failed")
        return False

    LogOutput('info', "UDP forward-protocol for snmp-trap succeeded")

    # UDP forward-protocol - tftp
    if ((udp_forward_protocol_config(client=client, forwarder=forwarder,
         server=server, serverIP="10.0.1.2", udp_dport=69, interface="1",
         no_of_pkts=10, check='pos')) is False):
        LogOutput('error', "UDP forward protocol for tftp failed")
        return False

    LogOutput('info', "UDP forward-protocol for tftp succeeded")

    # UDP forward-protocol - timep
    if ((udp_forward_protocol_config(client=client, forwarder=forwarder,
         server=server, serverIP="10.0.1.2", udp_dport=37, interface="1",
         no_of_pkts=10, check='pos')) is False):
        LogOutput('error', "UDP forward protocol for timep failed")
        return False

    LogOutput('info', "UDP forward-protocol for timep succeeded")

    return True


class Test_udp_bcast_forwarder_configuration:

    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_udp_bcast_forwarder_configuration.testObj = \
                                    testEnviron(topoDict=topoDict)
        #Get topology object
        Test_udp_bcast_forwarder_configuration.topoObj = \
            Test_udp_bcast_forwarder_configuration.testObj.topoObjGet()

    def teardown_class(cls):
        Test_udp_bcast_forwarder_configuration.topoObj.terminate_nodes()

    def test_configure(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        dut04Obj = self.topoObj.deviceObjGet(device="dut04")
        retValue = configure(switch1=dut01Obj, switch2=dut02Obj,
                             switch3=dut03Obj, switch4=dut04Obj)
        if(retValue):
            LogOutput('info', "UDP Forwarder basic configuration passed")
        else:
            LogOutput('error', "UDP Forwarder basic configuration failed")

    def test_udp_bcast_forwarder_no_global(self):
        # Verify the broadcast packets are not forwarded when UDP
        # forwarding is globally disabled
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        retValue = udp_bcast_forwarder_no_global(switch1=dut01Obj,
                    switch2=dut02Obj, switch3=dut03Obj)
        if(retValue):
            LogOutput('info', "Test to verify broadcast packets "
                              "forwarding when UDP broadcast "
                              "forwading is globally disabled passed")
        else:
            LogOutput('error', "Test to verify broadcast packets "
                              "forwarding when UDP broadcast "
                              "forwading is globally disabled failed")

    def test_udp_bcast_forwarder_config_protocols(self):
        # Verify configuration of all the supported UDP protocols
        # for the UDP Forwarder
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        retValue = udp_bcast_forwarder_config_protocols(switch1=dut01Obj,
                    switch2=dut02Obj, switch3=dut03Obj)
        if(retValue):
            LogOutput('info', "UDP Forwarder to configure "
                              "all supported UDP protocols passed")
        else:
            LogOutput('error', "UDP Forwarder to configure "
                               "all supported UDP protocols failed")

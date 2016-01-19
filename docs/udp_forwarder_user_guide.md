# UDP Broadcast Forwarder

## Contents
   - [Overview](#overview)
   - [Configure the UDP broadcast forwarder](#configure-the-udp-broadcast-forwarder)
   - [How to use the UDP broadcast forwarder](#how-to-use-the-udp-broadcast-forwarder)

## Overview
The routers by default do not forward broadcast packets. This is to avoid packet flooding on the network. However, there are situations where it is desirable to forward certain broadcast packets.
The UDP (User Datagram Protocol) broadcast forwarder takes up the client's UDP broadcast packet and forwards it to the specified server in a different subnet. Some applications rely on client requests sent as limited IP broadcasts addressed to a UDP application port. If a server for the application receives such a broadcast, the server can reply to the client. By default, a router's UDP broadcast forwarding is disabled, so a client's UDP broadcast requests cannot reach a target server on a different subnet unless explicitly configured on the router to forward client UDP broadcasts to that server.
UDP broadcast forwarding addresses can be configured regardless of whether UDP broadcast forwarding is globally enabled on the device. However, the feature does not operate unless globally enabled.
A UDP forwarding entry includes the desired UDP port number, and can be either an IP unicast address or an IP subnet broadcast address of the subnet on which the server operates. Thus, an incoming UDP packet carrying the configured port number will be:
1. Forwarded to a specific host if a unicast server address is configured for that port number.
2. Broadcast on the appropriate destination subnet if a subnet address is configured for that port number.

Note : UDP broadcast forwarder allows multiple unicast server IPs to be configured for a single UDP port.

## Configure the UDP broadcast forwarder
Note : IP routing has to be enabled before configuring the UDP broadcast forwarder.

Syntax:
`[no] ip udp-bcast-forward`
*Enable/disable UDP broadcast forwarding. By default, it is disabled.*

`[no] ip forward-protocol udp <IPv4-address> <port-number | protocol-name>`
*Configure UDP broadcast server(s) on the interface for a
 particular udp port.*

Explanation of parameters
• IPv4-address - The IPv4 address of the protocol server. This can be either be a unicast address of a destination server on another subnet or a broadcast address of the subnet on which a destination server operates.
• port-number - Any UDP port number corresponding to a UDP application supported on a device.
• protocol-name - Allows the use of common names for certain well-known UDP port numbers.
Supported UDP protocols:
•dns: Domain Name Service (53)•ntp: Network Time Protocol (123)•netbios-ns: NetBIOS Name Service (137)•netbios-dgm: NetBIOS Datagram Service (138)•radius: Remote Authentication Dial-In User Service (1812)•radius-old: Remote Authentication Dial-In User Service (1645)•rip: Routing Information Protocol (520)•snmp: Simple Network Management Protocol (161)•snmp-trap: Simple Network Management Protocol (162)•tftp: Trivial File Transfer Protocol (69)•timep: Time Protocol (37)

`show ip forward-protocol [interface <WORD>]`
*Display the server addresses where broadcast requests received by the device are to be forwarded based on configured port.*

Explanation of parameters
•   interface <WORD> - The interface on which server addresses are configured.

## How to use the UDP broadcast forwarder

### Example

```
switch(config)#ip udp-bcast-forward

switch#show ip forward-protocol
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Enabled

  IP Forward Addresses UDP Port
  -------------------- --------

switch#show running-config
Current configuration:
ip udp-bcast-forward
!
!
!

switch(config)#interface 1
switch(config-if)#ip forward-protocol udp 1.1.1.1 53

switch#show ip forward-protocol
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Enabled
interface 1
  IP Forward Addresses UDP Port
  -------------------- --------
  1.1.1.1              53

switch#show ip forward-protocol interface 1
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Enabled

  IP Forward Addresses UDP Port
  -------------------- --------
  1.1.1.1              53

switch#show running-config
Current configuration:
ip udp-bcast-forward
!
!
!
interface 1
    no shutdown
    ip forward-protocol udp 1.1.1.1 53

switch(config)#interface 1
switch(config-if)#ip forward-protocol udp 2.2.2.2 161

switch#show ip forward-protocol
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Enabled
interface 1
  IP Forward Addresses UDP Port
  -------------------- --------
  1.1.1.1              53
  2.2.2.2              161

switch#show ip forward-protocol interface 1
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Enabled

  IP Forward Addresses UDP Port
  -------------------- --------
  1.1.1.1              53
  2.2.2.2              161

switch#show running-config
Current configuration:
ip udp-bcast-forward
!
!
!
interface 1
    no shutdown
    ip forward-protocol udp 1.1.1.1 53
    ip forward-protocol udp 2.2.2.2 161

switch(config)#no ip udp-bcast-forward
switch#show ip forward-protocol
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Disabled
interface 1
  IP Forward Addresses UDP Port
  -------------------- --------
  1.1.1.1              53
  2.2.2.2              161

switch#show ip forward-protocol interface 1
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Disabled

  IP Forward Addresses UDP Port
  -------------------- --------
  1.1.1.1              53
  2.2.2.2              161

switch#show running-config
Current configuration:
!
!
!
interface 1
    no shutdown
    ip forward-protocol udp 1.1.1.1 53
    ip forward-protocol udp 2.2.2.2 161

switch(config)#interface 1
switch(config-if)#no ip forward-protocol udp 1.1.1.1 53
switch#show ip forward-protocol
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Disabled

  IP Forward Addresses UDP Port
  -------------------- --------
  2.2.2.2              161

switch#show ip forward-protocol interface 1
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Disabled

  IP Forward Addresses UDP Port
  -------------------- --------
  2.2.2.2              161

switch#show running-config
Current configuration:
!
!
!
interface 1
    no shutdown
    ip forward-protocol udp 2.2.2.2 161
```

# UDP Broadcast Forwarder

## Contents
   - [Overview](#overview)
   - [Configure UDP broadcast forwarder](#configure-udp-broadcast-forwarder)
   - [How to use UDP broadcast forwarder](#how-to-use-udp-broadcast-forwarder)

## Overview
The routers by default don’t forward broadcast packets. This is to avoid packet flooding on the network. However there are situations where it is desirable to forward certain broadcast packets.
This is where an UDP(User Datagram Protocol) broadcast forwarder comes into picture which takes up the client's UDP broadcast packet and forwards to the specified server in a different subnet.
Some applications rely on client requests sent as limited IP broadcast addressed to a UDP application port. If a server for the application receives such a broadcast, the server can reply to the client. By default, router's UDP broadcast forwarding is disabled, so a client's UDP broadcast requests cannot reach a target server on a different subnet unless explicitly configured on the router to forward client UDP broadcasts to that server.
UDP broadcast forwarding addresses can be configured regardless of whether UDP broadcast forwarding is globally enabled on the device. However, the feature does not operate unless globally enabled.
An UDP forwarding entry includes the desired UDP port number, and can be either an IP unicast address or an IP subnet broadcast address of the subnet server is in. Thus, an incoming UDP packet carrying the configured port number will be :
1. Forwarded to a specific host if a unicast server address is configured for that port number.
2. Broadcast on the appropriate destination subnet if a subnet address is configured for that port number.

Note : UDP broadcast forwarder allows multiple unicast server IPs to be configured on an UDP port.

## Configure UDP broadcast forwarder
Note : IP routing has to be enabled before configuring UDP broadcast forwarder.

Syntax:
`[no] ip udp-bcast-forward`
*Enable/disable UDP broadcast forwarding. By default, it is disabled.*

`[no] ip forward-protocol udp <IPv4-address> <port-number | port-name>`
*Configure UDP broadcast server(s) on the interface for a
 particular udp port.*

Explanation of parameters
•   IPv4-address - IPv4 address of the protocol server. This can be either be a unicast address of a destination server on another subnet or broadcast address of the subnet on which a destination server operates.
•   port-number  - Any UDP port number corresponding to a UDP application supported on a device.
•   port-number  - Allows use of common names for certain well-known UDP port numbers.

`show ip forward-protocol [interface <1-4094>]`
*Display the server addresses where broadcast requests received by the device are to be forwarded based on configured port.*

Explanation of parameters
•   interface <1-4094> - Interface on which server addresses are configured.

## How to use UDP broadcast forwarder

### Example 1

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
```

### Example 2

```
switch(config)#ip udp-bcast-forward
switch(config)#interface 1
switch(config-if)#ip forward-protocol udp 1.1.1.1 53

switch#show ip forward-protocol
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Enabled
interface 1
  IP Forward Addresses UDP Port
  -------------------- --------
  1.1.1.1			   53

switch#show ip forward-protocol interface 1
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Enabled

  IP Forward Addresses UDP Port
  -------------------- --------
  1.1.1.1			   53

switch#show running-config
Current configuration:
ip udp-bcast-forward
!
!
!
interface 1
    no shutdown
    ip forward-protocol udp 1.1.1.1 53
```

### Example 3

```
switch(config)#no ip udp-bcast-forward
switch#show ip forward-protocol
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Disabled
interface 1
  IP Forward Addresses UDP Port
  -------------------- --------
  1.1.1.1			   53

switch#show ip forward-protocol interface 1
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Disabled

  IP Forward Addresses UDP Port
  -------------------- --------
  1.1.1.1			   53

switch#show running-config
Current configuration:
!
!
!
interface 1
    no shutdown
    ip forward-protocol udp 1.1.1.1 53
```

### Example 4

```
switch(config)#no ip udp-bcast-forward
switch(config)#interface 1
switch(config-if)#no ip forward-protocol udp 1.1.1.1 53
switch#show ip forward-protocol
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Disabled

  IP Forward Addresses UDP Port
  -------------------- --------

switch#show ip forward-protocol interface 1
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Disabled

  IP Forward Addresses UDP Port
  -------------------- --------

switch#show running-config
Current configuration:
!
!
!
```

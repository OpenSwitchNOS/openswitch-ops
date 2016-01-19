# UDP Broadcast Forwarder

## Contents

- [UDP broadcast forwarding](#udp-broadcast-forwarding)
    - [Global Enable/Disable UDP broadcast forwarder](#global-enable/disable-udp-broadcast-forwarder)
    - [Configure UDP forward protocol on interface](#configure-udp-forward-protocol-on-interface)
    - [Show UDP forward protocol](#show-udp-forward-protocol)

## UDP broadcast forwarding
### Global Enable/Disable UDP broadcast forwarder
#### Syntax
`[no] ip udp-bcast-forward`
#### Description
This command enables/disables the UDP broadcast forwarding.
Note : ip routing has to be enabled on the device before enabling UDP broadcast forwarder.
#### Parameters
No parameters.
#### Authority
Root and Admin user.
#### Examples
```
switch(config)#ip udp-bcast-forward

switch(config)#no ip udp-bcast-forward
```

### Configure UDP forward protocol on interface
#### Syntax
`[no] ip forward-protocol udp <IPv4-address> <port-number | protocol-name>`
#### Description
This command configures a UDP broadcast server on the interface for a particular udp port.
#### Parameters
| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:------------------------|
| *IPv4-address* | Required | A.B.C.D | IPv4 address of of the protocol server. This can be either be a unicast address of a destination server on another subnet or broadcast address of the subnet on which a destination server operates.
| *port-number* | Required | integer | Any UDP port number corresponding to a UDP application supported on a device.
| *protocol-name* | Required | string |  Any common names for certain well-known UDP port numbers. Supported protocols are : dns: Domain Name Service (53), ntp: Network Time Protocol (123), netbios-ns: NetBIOS Name Service (137), netbios-dgm: NetBIOS Datagram Service (138), radius: Remote Authentication Dial-In User Service (1812), radius-old: Remote Authentication Dial-In User Service (1645), rip: Routing Information Protocol (520), snmp: Simple Network Management Protocol (161), snmp-trap: Simple Network Management Protocol (162), tftp: Trivial File Transfer Protocol (69), timep: Time Protocol (37).
#### Authority
Root and Admin user.
#### Examples
```
switch(config)#interface 1
switch(config-if)#ip forward-protocol udp 1.1.1.1 53

switch(config)#interface 1
switch(config-if)#ip forward-protocol udp 1.1.1.1 dns

```

### Show UDP forward protocol
#### Syntax
`show ip forward-protocol [interface <WORD>]`
#### Description
This command shows the server addresses where broadcast requests received by the switch are to be forwarded.
#### Parameters
| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:------------------------|
| *interface <WORD>* | Optional | string | select the interface on which UDP broadcast forwarding information needs to be displayed.
#### Authority
Root and Admin user.
#### Examples
```
switch(config)#ip udp-bcast-forward
switch(config)#interface 1
switch(config-if)#ip forward-protocol udp 1.1.1.1 123
switch(config)#interface 2
switch(config-if)#ip forward-protocol udp 2.2.2.2 161


switch#show ip forward-protocol
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Enabled
interface 1
  IP Forward Addresses UDP Port
  -------------------- --------
  1.1.1.1              123
interface 2
  IP Forward Addresses UDP Port
  -------------------- --------
  2.2.2.2              161


switch#show ip forward-protocol interface 1
 IP Forwarder Addresses

    UDP Broadcast Forwarding: Enabled

  IP Forward Addresses UDP Port
  -------------------- --------
  1.1.1.1              123

```

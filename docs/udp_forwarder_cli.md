# UDP Broadcast Forwarder

## Contents

- [UDP broadcast forwarding](#udp-broadcast-forwarding)
	- [Enable/Disable](#enable/disable)
	- [Configure command](#configure-command)
	- [Show command](#show-command)

## UDP broadcast forwarding
### Enable/Disable
#### Syntax
`[no] ip udp-bcast-forward`
#### Description
This command enables/disables the UDP broadcast forwarding.
#### Parameters
No parameters.
#### Authority
Root and Admin user.
#### Examples
```
switch(config)#ip udp-bcast-forward

switch(config)#no ip udp-bcast-forward
```

### Configure command
#### Syntax
`[no] ip forward-protocol udp <IPv4-address> <port-number | port-name>`
#### Description
This command configures a UDP broadcast server on the interface for a particular udp port.
#### Parameters
| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:------------------------|
| *IPv4-address* | Required | A.B.C.D | IPv4 address of of the protocol server. This can be either be a unicast address of a destination server on another subnet or broadcast address of the subnet on which a destination server operates.
| *port-number* | Required | integer | Any UDP port number corresponding to a UDP application supported on a device.
| *port-name* | Required | string |  Any common names for certain well-known UDP port numbers.
#### Authority
Root and Admin user.
#### Examples
```
switch(config)#interface 1
switch(config-if)#ip forward-protocol udp 1.1.1.1 53

switch(config)#interface 1
switch(config-if)#ip forward-protocol udp 1.1.1.1 dns

```

### Show command
#### Syntax
`show ip forward-protocol [interface <1-4094>]`
#### Description
This command shows the server addresses where broadcast requests received by the switch are to be forwarded.
#### Parameters
| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:------------------------|
| *interface <1-4094>* | Optional | string | select the interface between 1 and 4094 on which UDP broadcast forwarding information needs to be displayed.
#### Authority
Root and Admin user.
#### Examples
```
switch# show ip forward-protocol

 IP Forwarder Addresses

    UDP Broadcast Forwarding: Enabled

  IP Forward Addresses UDP Port
  -------------------- --------

switch# show ip forward-protocol interface 1

 IP Forwarder Addresses

    UDP Broadcast Forwarding: Enabled
interface 1
  IP Forward Addresses UDP Port
  -------------------- --------

```

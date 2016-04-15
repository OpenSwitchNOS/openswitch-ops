# DHCPv6 Relay CLI Commands

## Contents

- [DHCPv6 relay configuration commands](#dhcpv6-relay-configuration-commands)
    - [Configure DHCPv6-Relay](#configure-dhcpv6-relay)
    - [Configure DHCPv6-Relay helper-address](#configure-dhcpv6-relay-helper-address)
- [DHCPv6 relay option 79 configuration commands](#dhcpv6-relay-option-79-configuration-commands)
    - [Configure DHCPv6-Relay option 79](#configure-dhcpv6-relay-option-79)
    - [Unconfigure DHCPv6-Relay option 79](#unconfigure-dhcpv6-relay-option-79)
- [DHCPv6 relay show commands](#dhcpv6-relay-show-commands)
    - [Show DHCPv6-Relay configuration](#show-dhcpv6-relay-configuration)
    - [Show helper-address configuration](#show-helper-address-configuration)
    - [Show running configuration](#show-running-configuration)

## DHCPv6 relay configuration commands
### Configure DHCPv6-Relay
#### Syntax
`[no] dhcpv6-relay`
#### Description
This command works in the configuration context, and is used to enable/disable the DHCPv6-relay feature on the device.
DHCPv6-Relay is disabled by default.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# dhcpv6-relay
ops-as5712(config)# no dhcpv6-relay
```

## DHCPv6 relay option 79 configuration commands
### Configure DHCPv6-Relay option 79
#### Syntax
`dhcpv6-relay option 79`
#### Description
This command is used to configure DHCPv6-Relay option 79. Enabling option 79 will force the DHCPv6-Relay agent to forward the client Link-layer address.
DHCPv6-relay option 79 is disabled by default.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# dhcpv6-relay option 79
```

### Unconfigure DHCPv6-Relay option 79
#### Syntax
`no dhcpv6-relay option 79`
#### Description
This command is used to unconfigure DHCPv6-Relay option 79.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no dhcpv6-relay option 79
```

### Configure DHCPv6-Relay helper-address
#### Syntax
`[no] ipv6 helper-address unicast <ipv6-unicast-helper-addr>`
`[no] ipv6 helper-address multicast <all-dhcp-servers | ipv6-multicast-helper-addr> egress <port-name>`
#### Description
This command is used to configure/unconfigure a remote DHCPv6 server IP address on the device interface. Here the helper address is same as the DHCPv6 server address. A maximum of 8 helper-addresses can be configured per interface.
Even if routing is disabled on an interface, helper address configuration is allowed, but interface DHCPv6-Relay functionality will be inactive. In case a client has received an IPv6 address, and no routing is configured, the IPv6 address is valid on the client until the lease time expires.
The helper address configuration is allowed only on data plane interfaces. The helper address should not be loopback address.
#### Authority
All users.
#### Parameters
Choose one of the parameters from the following table to identify the multicast helper-address.

| Parameter | Status | Syntax | Description |
|-----------|--------|--------|---------------------------------------|
| *all-dhcp-servers* | Required | string   | Specifies all the DHCP server IPv6 addresses.|
| *IPv6-address*     | Required | X:X::X:X | A DHCP server IPv6 address.|

| Parameter | Status | Syntax | Description |
|-----------|--------|--------|---------------------------------------|
|*port-name*| Required| string  | Specifies the port name.|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# ipv6 helper-address unicast 2001:db8:0:1::
ops-as5712(config-if)# ipv6 helper-address multicast FF01::1:1000/118 egress 2
ops-as5712(config-if)# ipv6 helper-address unicast 2001:db8:0:1::
ops-as5712(config)# interface 2
ops-as5712(config-if)# ipv6 helper-address unicast 2001:db8:0:2::
```

## DHCPv6 relay show commands

### Show DHCPv6-Relay configuration
#### Syntax
`show dhcpv6-relay`
#### Description
This command is used to display the DHCPv6-Relay configuration.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# show dhcpv6-relay

  DHCPv6 Relay Agent : Enabled
  Option 79          : Enabled
  DHCPv6 Relay Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  0          0          0          0
```

### Show helper-address configuration
#### Syntax
`show ipv6 helper-address [interface <interface-name>]`
#### Description
This command is used to display the DHCPv6-Relay helper-address configuration.
#### Authority
All users.

#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *interface* | Optional | IFNAME | The name of the interface.|
#### Examples
```
ops-as5712# show ipv6 helper-address

 Interface: 1
 IPv6 Helper Address                            Egress Port
 ---------------------------------------------- -----------
 2001:db8:0:1::                                 -
 FF01::1:1000/118                               2

 Interface: 2
 IPv6 Helper Address                            Egress Port
 --------------------------------------------   -----------
 2001:db8:0:1::                                 -

ops-as5712# show ipv6 helper-address interface 1

 Interface: 1
 IPv6 Helper Address                            Egress Port
 ---------------------------------------------- -----------
 2001:db8:0:1::                                 -
 FF01::1:1000/118                               2

```

### Show running configuration
#### Syntax
`show running-config`
#### Description
This command displays the current non-default configuration on the switch.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# show running-config
Current configuration:
!
!
!
dhcpv6-relay
dhcpv6-relay option 79
interface 1
    ipv6 helper-address unicast 2001:db8:0:1::
    ipv6 helper-address multicast ff01::1 egress 2
interface 2
    ipv6 helper-address unicast 2001:db8:0:1::
```

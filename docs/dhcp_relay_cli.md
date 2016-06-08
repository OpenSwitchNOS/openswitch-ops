# DHCP Relay Commands

## Contents
- [Configuration commands](#configuration-commands)
    - [dhcp-relay](#dhcp-relay)
    - [ip helper-address](#ip-helper-address)
    - [dhcp-relay option 82](#dhcp-relay-option-82)
    - [ip bootp-gateway](#ip-bootp-gateway)
    - [dhcp-relay hop-count-increment](#dhcp-relay-hop-count-increment)
- [Display commands](#display-commands)
    - [show dhcp-relay](#show-dhcp-relay)
    - [show ip helper-address](#show-ip-helper-address)
    - [show dhcp-relay bootp-gateway](#show-dhcp-relay-bootp-gateway)
    - [show running configuration](#show-running-configuration)


## Configuration commands

### dhcp-relay

#### Syntax
```
dhcp-relay
no dhcp-relay
```

#### Description
Enables support for the DHCP relay feature on all interfaces. A DHCP relay agent receives DHCP requests from clients and forwards them to one or more DHCP servers. The DHCP server(s) to which requests are forwarded must be configured individually on each interface using the `ip help-address` command.

Use the `no` form of this command to disable DHCP relay support on all interfaces.

#### Command mode
Configuration mode (config).

#### Authority
All users.

#### Parameters
None.

#### Examples

###### Enabling DHCP relay
```
switch(config)# dhcp-relay
```

###### Disabling DHCP relay
```
switch(config)# no dhcp-relay
```


### ip helper-address

#### Syntax
```
ip helper-address <IPv4-address>
no ip helper-address <IPv4-address>
```

#### Description
Sets the IP address of a remote DHCP server for an interface. Up to 16 addresses can be defined per interface.

DHCP requests are only forwarded to a DHCP server if:
- the DHCP server feature is enabled
- the interface has an IPv4 address
- routing is enabled on the interface

If multiple servers are defined, requests are forwarded to all  servers at the same time.

Note: If a client has received an IP address, even though none of the above conditions are true, the address remains valid until its lease time expires.

Use the `no` form of this command to remove the IP address of a remote DHCP server.

#### Command Mode
Interface mode (config-if).

#### Authority
All users.

#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|---------------------------------------|
| *IPv4-address* | Required | A.B.C.D | IPv4 address of a remote DHCP server. Do not specify a multicast or loopback address. |

#### Examples

###### Adding DHCP server addresses to interface 1
```
switch(config)# interface 1
switch(config-if)# ip helper-address 192.168.10.1
switch(config-if)# ip helper-address 192.168.20.1
```
###### Removing DHCP server addresses from interface 1
```
switch(config-if)# no ip helper-address 192.168.10.1
switch(config-if)# no ip helper-address 192.168.20.1
```


### dhcp-relay option 82

#### Syntax
```
dhcp-relay option 82 replace [validate] [ip | mac]
dhcp-relay option 82 drop [validate] [ip | mac]
dhcp-relay option 82 keep [ip | mac]
dhcp-relay option 82 validate [replace | drop] [ip | mac]
no dhcp-relay option 82
no dhcp-relay option 82 validate
```

#### Description
Configures support for DHCP option 82. Option 82 is called the relay agent information option and is inserted by the DHCP relay agent when forwarding client-originated DHCP packets to a DHCP server. Servers recognizing the relay agent information option can use the information to implement IP address or other parameter assignment policies. The DHCP server echoes the option back verbatim to the relay agent in server-to-client replies, and the relay agent strips the option before forwarding the reply to the client.

The routing switch can operate as a DHCP relay agent to enable communication between a client and a DHCP server on a different subnet. Without Option 82, DHCP operation modifies client IP address request packets to the extent needed to forward the packets to a DHCP server. Option 82 enhances this operation by enabling the routing switch to append an Option 82 field to such client requests. This field includes two suboptions for identifying the routing switch (by MAC address or IP address) and the routing switch port the client is using to access the network. A DHCP server with Option 82 capability can read the appended field and use this data as criteria for selecting the IP addressing it will return to the client through the usual DHCP server response packet. This operation provides several advantages over DHCP without Option 82:

- An Option 82 DHCP server can use a relay agent's identity and client source port information to administer IP addressing policies based on client and relay agent location within the network, regardless of whether the relay agent is the client's primary relay agent or a secondary agent.
- A routing switch operating as a primary Option 82 relay agent for DHCP clients requesting an IP address can enhance network access protection by blocking attempts to use an invalid Option 82 field to imitate an authorized client, or by blocking attempts to use response packets with missing or invalid Option 82 suboptions to imitate valid response packets from an authorized DHCP server.
- An Option 82 relay agent can also eliminate unnecessary broadcast traffic by forwarding an Option 82 DHCP server response only to the port on which the requesting client is connected, instead of broadcasting the DHCP response to all ports on the VLAN.

The DHCP relay information (Option 82) feature can be used in networks where the DHCP servers are compliant with RFC 3046 Option 82 operation. DHCP servers that are not compliant with Option 82 operation ignore Option 82 fields.

It is not necessary for all relay agents on the path between a DHCP client and the server to support Option 82, and a relay agent without Option 82 should forward DHCP packets regardless of whether they include Option 82 fields. However, Option 82 relay agents should be positioned at the DHCP policy boundaries in a network to provide maximum support and security for the IP addressing policies configured in the server.

Use the 'no' form of this command to remove support for option 82.

#### Command Mode
Configuration mode (config).

#### Authority
All users.

#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|---------------------------------------|
| **replace** | Required | Literal | 	Replaces existing Option 82 fields in an inbound client DHCP packet with an Option 82 field for the switch. The replacement Option 82 field includes the switch circuit ID (inbound port number) associated with the client DHCP packet and the switch remote ID. The default switch remote ID is the MAC address of the switch on which the packet was received from the client.|
| **keep**    | Required | Literal | 	If the relay agent receives a client request that already has one or more Option 82 fields, keep causes the relay agent to retain such fields and forward the request without adding another Option 82 field. But if the incoming client request does not already have any Option 82 fields, the relay agent appends an Option 82 field before forwarding the request.|
| **drop**    | Required | Literal | Drops an inbound client requests with an Option 82 field already appended. If no Option 82 fields are present, drop causes the switch to add an Option 82 field and forward the request. As a general guideline, configure drop on relay agents at the edge of a network, where an inbound client request with an appended Option 82 field may be unauthorized, a security risk, or for some other reason, should not be allowed.|
| **validate**|Optional| Literal | Validates the DHCP server responses to client requests. This enhances protection against DHCP server responses that are either from untrusted sources or are carrying invalid Option 82 information.|
| **mac** | Optional | String | Sets the Option 82 remote ID to the MAC address of the switch when adding or replacing Option 82 fields.|
| **ip**  | Optional | String | Sets the Option 82 remote ID to the IP address of the VLAN on which the client packet entered the switch.|

#### Examples

###### Enabling DHCP relay option 82 using the MAC address of a switch
```
switch(config)# dhcp-relay option 82 replace validate mac
```

###### Disabling DHCP relay option 82
```
switch(config)# no dhcp-relay option 82
```


### ip bootp-gateway

#### Syntax
```
ip bootp-gateway <IPv4-address>
no ip bootp-gateway <IPv4-address>
```

#### Description
Configures a gateway address that the DHCP relay agent will use for DHCP requests. If not configured, the DHCP relay agent automatically uses the lowest-numbered IP address. Only supported for IPv4.

Use the  `no` form of this command to remove a gateway address.

#### Command Mode
Interface mode (config-if).

#### Authority
All users.

#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|---------------------------------------|
| *IPv4-address* | Required | A.B.C.D | IPv4 address of the gateway.|

#### Examples

###### Adding a gateway to interface 1, 2, and 3
```
switch(config)# interface 1
switch(config-if)# ip bootp-gateway 1.1.1.1
switch(config)# interface 2
switch(config-if)# ip bootp-gateway 1.1.1.2
switch(config)# interface 3
switch(config-if)# ip bootp-gateway 1.1.1.3
```

###### Removing a gateway from interface 3
```
switch(config)# interface 3
switch(config-if)# no ip bootp-gateway 1.1.1.3
```


### dhcp-relay hop-count-increment

#### Syntax
```
dhcp-relay hop-count-increment
no dhcp-relay hop-count-increment
```

#### Description
Enables DHCP relay hop count increment. This causes the DHCP relay agent to increase the hop count by one before forwarding a DHCP request to a DHCP server.

Use the `no` form of this command to disable DHCP relay hop count increment.

#### Command Mode
Configuration mode (config).

#### Authority
All users.

#### Parameters
None.

#### Examples

###### Enabling hop count
```
switch(config)# dhcp-relay hop-count-increment
```

###### Disabling hop count
```
switch(config)# no dhcp-relay hop-count-increment
```

## Display commands

### show dhcp-relay

#### Syntax
`show dhcp-relay`

#### Description
Displays DHCP relay configuration settings.

#### Command Mode
Enable mode.

#### Authority
All users.

#### Parameters
None.

#### Example
```
switch# show dhcp-relay

 DHCP Relay Agent                 : Enabled
 DHCP Request Hop Count Increment : Enabled
 Option 82                        : Disabled
 Response Validation              : Disabled
 Option 82 Handle Policy          : replace
 Remote ID                        : mac

 DHCP Relay Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  60         10         60         10

  DHCP Relay Option 82 Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  50         8          50         8
```


### show ip helper-address

#### Syntax
`show ip helper-address [interface <interface-name>]`

#### Description
Displays DHCP relay helper address configuration settings.

#### Command Mode
Enable mode.

#### Authority
All users.

#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| **interface** | Optional | Literal | Displays information for the specified interface.|
| *interface-name* | Optional | String | The name of an interface.|

#### Examples
```
switch# show ip helper-address
 IP Helper Addresses

 Interface: 1
  IP Helper Address
  -----------------
  192.168.20.1
  192.168.10.1

 Interface: 2
  IP Helper Address
  -----------------
  192.168.10.1

switch# show ip helper-address interface 1
 IP Helper Addresses

 Interface: 1
  IP Helper Address
  -----------------
  192.168.20.1
  192.168.10.1

```


### show dhcp-relay bootp-gateway

#### Syntax
`show dhcp-relay bootp-gateway [interface <interface-name>]`

#### Description
Displays DHCP relay BOOTP gateway configuration settings.

#### Command Mode
Enable mode.

#### Authority
All users.

#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| **interface** | Optional | Literal | Displays information for the specified interface.|
| *interface-name* | Optional | String | The name of an interface.|

#### Examples

###### Displaying configuration settings for all interfaces
```
switch# show dhcp-relay bootp-gateway

 BOOTP Gateway Entries

 Interface            BOOTP Gateway
 -------------------- ---------------
 1                    1.1.1.1
 2                    1.1.1.2
```

###### Displaying configuration settings for interface 1
```
switch# show ip helper-address interface 1
 BOOTP Gateway Entries

 Interface            BOOTP Gateway
 -------------------- ---------------
 1                    1.1.1.1
```

### show running configuration

#### Syntax
`show running-config`

#### Description
Displays the current non-default configuration on the switch.

#### Authority
All users.

#### Parameters
None.

#### Examples
```
ops-as5712# show running-config
Current configuration:
!
!
!
no dhcp-relay
no dhcp-relay hop-count-increment
interface 1
    helper-address 192.168.10.1
    helper-address 192.168.20.1
    ip bootp-gateway 1.1.1.1
interface 2
    helper-address 192.168.10.1
    ip bootp-gateway 1.1.1.2

```
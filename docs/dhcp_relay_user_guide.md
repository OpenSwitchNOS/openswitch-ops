# DHCP Relay

## Contents
   - [Overview](#overview)
   - [Configure DHCP relay](#configure-dhcp-relay)
   - [How to use DHCP relay](#how-to-use-dhcp-relay)

## Overview
The Dynamic Host Configuration Protocol (DHCP) is used for configuring hosts with IP address and other configuration parameters without human intervention. The protocol is composed of three components: the DHCP client, the DHCP server, and the DHCP relay agent.
The DHCP client sends broadcast request packets to the network, the DHCP servers respond with broadcast packets that offer IP parameters, such as an IP address for the client.
After the client chooses the IP parameters, communication between the client and server is by unicast packets.
The function of the DHCP relay agent is to forward the DHCP messages to other subnets so that the DHCP server doesn’t have to be on the same subnet as the DHCP clients. The DHCP relay agent transfers the DHCP messages from the DHCP clients located on a subnet without DHCP server, to other subnets. It also relays answers from DHCP servers to DHCP clients.
The DHCP relay agent on the routing switch forwards DHCP client packets to all DHCP servers ( Helper IP addresses) that are configured in the table administrated for each interface.

## Configure DHCP relay
Note : IP routing has to be enabled before configuring DHCP relay.

Syntax:
`[no] dhcp-relay`
*Enable/Disable DHCP relay. By default, it is disabled.*

`[no]`ip helper-address IPv4-address`
*Configure IP helper-address needed by DHCP relay on a particular interface.*

Explanation of parameters
•   IPv4-address - IPv4 address of the protocol server. This is a unicast address of a destination server on another subnet.

`show dhcp-relay [interface <interface-name>]`
*Display whether DHCP relay is enabled or disabled.*

`show ip helper-address [ interface <interface-name>]`
*Display the configured IP helper address(es).*

Explanation of parameters
•   interface <interface-name> - Interface on which server addresses are configured.

## How to use DHCP relay

### Example 1

```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-relay

ops-as5712# show dhcp-relay
DHCP Relay Agent                 : Enabled
```

### Example 2

```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# ip helper-address 192.168.10.1
ops-as5712(config-if)# ip helper-address 192.168.20.1
ops-as5712(config-if)# ip helper-address 192.168.30.1

ops-as5712# show ip helper-address

IP Helper Addresses

 Interface: 1
  IP Helper Address
  -----------------
  192.168.10.1
  192.168.20.1
  192.168.30.1
```
### Example 3

```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no ip helper-address 192.168.10.1
ops-as5712(config-if)# no ip helper-address 192.168.20.1
ops-as5712(config-if)# no ip helper-address 192.168.30.1
ops-as5712# show ip helper-address

IP Helper Addresses

 Interface: 1
  IP Helper Address
  -----------------
```

### Example 4

```
ops-as5712# configure terminal
ops-as5712(config)# no dhcp-relay

ops-as5712# show dhcp-relay
DHCP Relay Agent                 : Disabled
```
DHCP-Relay Commands
======
## Contents

- [DHCP-Relay Configuration Commands](#dhcp-relay-configuration-commands)
	- [Enable DHCP-Relay](#enable-dhcp-relay)
    - [Disable DHCP-Relay](#disable-dhcp-relay)
	- [Configure a server IP address](#configure-a-server-ip-address)
    - [Unconfigure a server IP address](#unconfigure-a-server-ip-address)
- [DHCP-Relay Show Commands](#dhcp-relay-show-commands)
	- [Show DHCP-Relay Configuration](#show-dhcp-relay-configuration)
	- [Show DHCP Server IP Address](#show-dhcp-server-ip-address)

## DHCP-Relay Configuration Commands

### Enable DHCP-Relay
#### Syntax
`dhcp-relay`
#### Description
This command works in the configuration context and enables the DHCP-Relay feature in the DHCP-Relay agent device.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-relay
```
### Disable DHCP-Relay
#### Syntax
`no dhcp-relay`
#### Description
This command works in the configuration context and disables the DHCP-Relay feature in the DHCP-Relay agent device.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no dhcp-relay
```
### Configure a server IP address
#### Syntax
`ip helper-address IP-ADDR`
#### Description
This command works in the interface context and sets a server IP address in the DHCP-Relay agent device.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description |
|-----------|--------|---------------------------------------|
| *helper-address* | A.B.C.D | Sets the IP address defined on any interface as a server IP address.|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# ip helper-address 192.168.10.1
```
### Unconfigure a server IP address
#### Syntax
`no ip helper-address IP-ADDR`
#### Description
This command works in the interface context and unsets a server IP address in the DHCP-Relay agent device.
#### Authority
All users.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *helper-address* | Required | A.B.C.D | Unsets the IP address defined on any interface as a server IP address.|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no ip helper-address 192.168.10.1
```
## DHCP-Relay Show Commands

### Show DHCP-Relay Configuration
#### Syntax
`show dhcp-relay [ interface <interface-name> ]`
#### Description
This command displays the DHCP-Relay statistics.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# show dhcp-relay
  DHCP Relay Agent                 : Enabled
```
### Show DHCP Server IP Address
#### Syntax
`show ip helper-address [ interface <interface-name> ]`
#### Description
This command displays the DHCP-Relay helper addresses.
#### Authority
All users.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *interface* | Optional | System defined | Name of the interface. System defined.|
#### Examples
```
ops-as5712# show ip helper-address
 IP Helper Addresses

 Interface: 1
  IP Helper Address
  -----------------
  192.168.10.1

 Interface: 2
  IP Helper Address
  -----------------
  192.168.20.1

```

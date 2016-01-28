# DHCP-Relay CLI Commands

## Contents

- [DHCP-Relay configuration commands](#dhcp-relay-configuration-commands)
	- [Configure dhcp-relay](#configure-dhcp-relay)
	- [Configure a helper-address](#configure-a-helper-address)
- [DHCP-Relay show commands](#dhcp-relay-show-commands)
	- [Show dhcp-relay configuration](#show-dhcp-relay-configuration)
	- [Show helper-address configuration](#show-helper-address-configuration)

## DHCP-Relay configuration commands
### Configure dhcp-relay
#### Syntax
`[no] dhcp-relay`
#### Description
This command works in the configuration context, and is used to enable/disable the DHCP-Relay feature on the device.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-relay
ops-as5712(config)# no dhcp-relay
```
### Configure a helper-address
#### Syntax
`[no] ip helper-address IP-ADDR`
#### Description
This command supports multiple helper-address configurations under an interface context, and is used to configure/unconfigure a remote DHCP server IP address on the device.
#### Authority
All users.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|---------------------------------------|
| *helper-address* | Required | A.B.C.D | A DHCP server IP address.|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# ip helper-address 192.168.10.1
ops-as5712(config-if)# ip helper-address 192.168.20.1
ops-as5712(config-if)# no ip helper-address 192.168.10.1
ops-as5712(config-if)# no ip helper-address 192.168.20.1
ops-as5712(config)# interface 2
ops-as5712(config-if)# ip helper-address 192.168.30.1
```
## DHCP-Relay show commands

### Show dhcp-relay configuration
#### Syntax
`show dhcp-relay`
#### Description
This command is used to display the DHCP-Relay statistics.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# show dhcp-relay
  DHCP Relay Agent        : Enabled
```
### Show helper-address configuration
#### Syntax
`show ip helper-address [interface <interface-name>]`
#### Description
This command is used to display the DHCP-Relay helper-address configuration.
#### Authority
All users.

#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *interface* | Optional | System defined. | Name of the interface. It is system defined.|
#### Examples
```
ops-as5712# show ip helper-address
 IP Helper Addresses

 Interface: 1
  IP Helper Address
  -----------------
  192.168.10.1
  192.168.20.1

 Interface: 2
  IP Helper Address
  -----------------
  192.168.30.1

ops-as5712# show ip helper-address interface 1
 IP Helper Addresses

 Interface: 1
  IP Helper Address
  -----------------
  192.168.10.1
  192.168.20.1

```

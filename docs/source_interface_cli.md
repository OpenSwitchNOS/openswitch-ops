Source Interface commands

## Contents

- [Source Interface configuration commands](#source-interface-configuration-commands)
	- [Setting a source-interface IP address to TFTP protocol](#setting-a-source-interafce-ip-address-to-tftp-protocol)
    - [Setting a source-interface IP address to all the specified protocols](#setting-a-source-interafce-IP-address-to-all-the-specified-protocols)
    - [Setting a source-interface to TFTP protocol](#setting-a-source-interafce-to-tftp-protocol)
    - [Setting a source-interface to all the specified protocols](#setting-a-source-interafce-to-all-the-specified-protocols)
    - [Unsetting a source-interface to TFTP protocol](#unsetting-a-source-interafce-to-tftp-protocol)
    - [Unsetting a source-interface to all the specified protocols](#unsetting-a-source-interafce-to-all-the-specified-protocols)
- [Using source-interface show commands](#using-source-interface-show-commands)
	- [Showing source-interface selection configuration to TFTP protocol](#showing-source-interface-selection-configuration-to-tftp-protocol)
    - [Showing source-interface selection configuration to all the specified protocols](#showing-source-interface-selection-configuration-all-the-specified-protocols)


## Source Interface configuration commands

### Setting a source-interface IP address to TFTP protocol
##### Syntax
`ip source-interface tftp address <A.B.C.D>`
#### Description
This command works in the configuration context and sets a source-interface IP address to TFTP protocol.
#### Authority
All users.
#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *address* | Set the IP address defined on any interface to tftp protocol.|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# ip source-interface tftp address 1.1.1.1
```
### Setting a source-interface IP address to all the specified protocols
##### Syntax
`ip source-interface all address <A.B.C.D>`
#### Description
This command works in the configuration context and sets a source-interface IP address to all the specified protocols.
#### Authority
All users.
#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *address* | Set the IP address defined on any interface to all the specified protocols.|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# ip source-interface all address 1.1.1.1
```
### Setting a source-interface to TFTP protocol
##### Syntax
`ip source-interface tftp interface <IFNAME>`
#### Description
This command works in the configuration context and sets a source-interface to TFTP protocol.
#### Authority
All users.
#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *interface* | Set an IP address defined interafce to tftp protocol.|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# ip source-interface tftp interface 1
```
### Setting a source-interface to all the defined protocols
##### Syntax
`ip source-interface all interface <IFNAME>`
#### Description
This command works in the configuration context and sets a source-interface to all the specified protocols.
#### Authority
All users.
#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *interafce* | Set an IP address defined interafce to all the specified protocols.|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# ip source-interface tftp interface 1
```
### Unsetting a source-interface to TFTP protocol
##### Syntax
`no ip source-interface tftp`
#### Description
This command works in the configuration context and unsets a source-interface to TFTP protocol.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no ip source-interface tftp
```
### Unsetting a source-interface to all the specified protocols
##### Syntax
`no ip source-interface tftp`
#### Description
This command works in the configuration context and unsets a source-interface to all the specified protocols.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no ip source-interface all
```
## Using source-interface show commands
### Showing source-interface selection configuration to TFTP protocol
##### Syntax
`show ip source-interface tftp`
#### Description
This command displays source-interface selection configuration to TFTP protocol.
#### Authority
All users.
#### Parameters
No parameters.
#### Example
```
ops-as5712# show ip source-interface tftp


Source-interface Configuration Information

Protocol        Source Interface
--------        ----------------
tftp            1
```

### Showing source-interface selectio configuration to all the specified protocols
##### Syntax
`show ip source-interface`
#### Description
This command displays source-interface selection configuration to all the specified protocols
#### Authority
All users.
#### Parameters
No parameters.
#### Example
```
ops-as5712# show ip source-interface


Source-interface Configuration Information

Protocol        Source Interface
--------        ----------------
tftp            1
```

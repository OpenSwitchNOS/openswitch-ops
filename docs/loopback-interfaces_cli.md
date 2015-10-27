# Loopback Interface Commands
<!-- TOC depth:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Loopback Interface Commands](#loopback-interface-commands)
	- [Configuration Commands](#configuration-commands)
		- [Create loopback interface](#create-loopback-interface)
			- [Syntax](#syntax)
			- [Description](#description)
			- [Authority](#authority)
			- [Parameters](#parameters)
			- [Examples](#examples)
		- [Delete Loopback interface](#delete-loopback-interface)
			- [Syntax](#syntax)
			- [Description](#description)
			- [Authority](#authority)
			- [Parameters](#parameters)
			- [Examples](#examples)
		- [Set/Unset IPv4 address](#setunset-ipv4-address)
			- [Syntax](#syntax)
			- [Description](#description)
			- [Authority](#authority)
			- [Parameters](#parameters)
			- [Examples](#examples)
		- [Set/Unset IPv6 address](#setunset-ipv6-address)
			- [Syntax](#syntax)
			- [Description](#description)
			- [Authority](#authority)
			- [Parameters](#parameters)
			- [Examples](#examples)
	- [Display Commands](#display-commands)
		- [Show Running Configuration](#show-running-configuration)
			- [Syntax](#syntax)
			- [Description](#description)
			- [Authority](#authority)
			- [Examples](#examples)
		- [Show loopback interfaces](#show-loopback-interfaces)
			- [Syntax](#syntax)
			- [Description](#description)
			- [Authority](#authority)
			- [Parameters](#parameters)
			- [Examples](#examples)
		- [Show Loopback interface](#show-loopback-interface)
			- [Syntax](#syntax)
			- [Description](#description)
			- [Authority](#authority)
			- [Parameters](#parameters)
			- [Examples](#examples)
	- [References](#references)
<!-- /TOC -->

## Configuration Commands
###  Create loopback interface
#### Syntax
```
interface loopback instance
```
#### Description
This command creates a loopback interface and enters loopback configuration mode
#### Authority
All Users
#### Parameters
| Parameter | Status   | Syntax |	Description |
|-----------|----------|----------------------|
| **instance** | Required | Integer | loopback interface ID 1 to 2147483647 |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface loopback 1
ops-as5712(config-loopback-if)#
```
###  Delete Loopback interface
#### Syntax
```
no interface loopback instance
```
#### Description
This command deletes a loopback interface
#### Authority
All Users
#### Parameters
| Parameter | Status   | Syntax |	Description |
|-----------|----------|----------------------|
| **instance** | Required | Integer | loopback interface ID 1 to 2147483647 |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no interface loopback 1
```
###  Set/Unset IPv4 address
#### Syntax
```
[no] ip address <ipv4_address/prefix-length>
```
#### Description
This command sets the ipv4 address for a loopback interface.
#### Authority
All Users
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *ipv4_address/prefix-length* | Required | A.B.C.D/M | IPV4 address with prefix-length for the loopback interface |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface loopback 1
ops-as5712(config-loopback-if)# ip address 16.93.50.2/24
```
###  Set/Unset IPv6 address
#### Syntax
```
[no] ip address <ipv6_address/prefix-length>
```
#### Description
This command sets the ipv6 address for a loopback interface.
#### Authority
All Users
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *ipv6_address/prefix-length* | Required | X:X::X:X/P | IPV6 address with prefix-length for the loopback interface |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface loopback 1
ops-as5712(config-loopback-if)# ipv6 address fd00:5708::f02d:4df6/64
```
##Display Commands
### Show Running Configuration
#### Syntax
`show running-config`
#### Description
The display of this command includes all loopback interfaces
#### Authority
All users
#### Examples
```
ops-as5712# show running-config
.............................
.............................
interface loopback 1
    no shutdown
    ip address 192.168.1.1/24
interface loopback 2
    no shutdown
    ip address 182.168.1.1/24
.............................
.............................
```
### Show loopback interfaces
#### Syntax
`show interface loopback [brief]`
#### Description
This command displays all configured loopback interfaces
#### Authority
All users
#### Parameters
None
#### Examples
```
ops-as5712# show interface loopback
Interface loopback 1 is up
 Hardware is Loopback
 IPv4 address 192.168.1.1/24
 MTU 1500
 RX
      0 input packets     0 bytes
      0 input error       0 dropped
      0 CRC/FCS
 TX
      0 output packets  0 bytes
      0 input error     0 dropped
      0 collision
Interface loopback 2 is up
 Hardware is Loopback
 IPv4 address 182.168.1.1/24
 MTU 1500
 RX
      0 input packets     0 bytes
      0 input error       0 dropped
      0 CRC/FCS
 TX
      0 output packets  0 bytes
      0 input error     0 dropped
      0 collision

ops-as5712# show interface loopback brief
....................................................................................................
Loop         IPv4 Address    Status
Interface
...................................................................................................
  1          192.168.1.1/24    up
  2          192.168.1.2/24    up
```
### Show Loopback interface
#### Syntax
`show interface loopback instance`
#### Description
This command displays the configuration and status of a loopback interface.
#### Authority
All users
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| **instance** | Required | Integer | loopback interface ID 1 to  2147483647 |
#### Examples
```
ops-as5712# show interface loopback 1
Interface loopback 1 is up
 Hardware is Loopback
 IPv4 address 192.168.1.1/24
 MTU 1500
 RX
      0 input packets     0 bytes
      0 input error       0 dropped
      0 CRC/FCS
 TX
      0 output packets  0 bytes
      0 input error     0 dropped
      0 collision
```
##References
* [Reference 1]`interface_cli.md`
* [Reference 2]`loopback_interface_design.md`

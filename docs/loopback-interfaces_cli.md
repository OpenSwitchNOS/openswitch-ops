# Loopback Interface Commands
[TOC]
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
| **instance** | Required | Integer | loopback interface ID 1 to 1024 |
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
| **instance** | Required | Integer | loopback ID 1 to 1024 |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no interface loopback 1
```
###  Set IPv4 address
#### Syntax
```
ip address <ipv4_address/mask>
```
### Enable interface
#### Syntax
`no shutdown`
#### Description
This command enables a loopback interface.
#### Authority
All Users
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface loopback 1
ops-as5712(config-subif)# no shutdown
```
### Disable interface
#### Syntax
`shutdown`
#### Description
This command disables a loopback interface.
#### Authority
All Users
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface loopback 1
ops-as5712(config-if)# shutdown
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
`show interface loopback-interface [brief]`
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
`show interface loopback instance [brief]`
#### Description
This command displays the configuration and status of a loopback interface.
#### Authority
All users
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| **instance** | Required | Integer | loopback interface ID 1 to 1024 |
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
ops-as5712# show interface loopback 1 brief
....................................................................................................
Loop         IPv4 Address    Status
Interface
...................................................................................................
  1          192.168.1.1/24    up
```
##References
* [Reference 1]`interface_cli.md`

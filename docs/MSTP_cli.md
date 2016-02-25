MSTP commands
=============
# Contents
- [MSTP configuration command](#mstp-configuration-commands)
	- [Config context commands](#config-context-commands)
		- [Enable MSTP protocol](#enbale-mstp-protocol)
		- [Disable MSTP protocol](#disable-mstp-protocol)
		- [Modify MSTP protocol status](#modify-mstp-protocol-status)
		- [Set MSTP config name](#set-mstp-config-name)
		- [Set default MSTP config name](#set-default-mstp-config-name)
		- [Set MSTP config revision number](#set-mstp-config-revision-number)
		- [Add VLAN to instance](#add-vlan-to-instance)
		- [Remove VLAN from instance](#remove-vlan-from-instance)
		- [Set forward delay](#set-forward-delay)
		- [Set default forward delay](#set-default-forward-delay)
		- [Set hello time](#set-hello-time)
		- [Set default hello time](#set-default-hello-time)
		- [Set max age](#set-max-age)
		- [Set default max age](#set-default-max-age)
		- [Set max hops](#set-max-hops)
		- [Set default max hops](#set-default-max-hops)
		- [Set port type](#set-port-type)
		- [Set default port type](#set-default-port-type)
		- [Enable port guard](#enable-port-guard)
	- [MSTP show commands](#mstp-show-commands)
	    - [show spanning tree global configuration](#show-spanning-tree-global-configuration)
		- [show MSTP global configuration](#show-mstp-global-configuration)
		- [show MSTP running configuration](#show-mstp-running-configuration)

# MSTP configuration commands
In vtysh every command belongs to a particular context.
## Config context commands
### Enable MSTP protocol
#### Syntax ####
`spanning-tree`
#### Description ####
This command enables MSTP feature for all the instance.
#### Authority ####
All users.
#### Examples ####
```
switch# configure terminal
switch# spanning-tree
```
### Disable MSTP protocol
#### Syntax ####
`no spanning-tree`
#### Description ####
This command disables MSTP feature for all the instance.
#### Authority ####
All users.
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree
```
### Modify MSTP protocol status
#### Syntax ####
`spanning-tree [ enable | disable ]`
#### Description ####
This command modifies MSTP feature status for all the instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status     |Description |
|:---------------|:-----------|:--------------|
| *admin_status* | Optional   |Specifies the MSTP feature status value |
#### Examples ####
```
switch# configure terminal
switch# spanning-tree enable
switch# spanning-tree disable
```
### Set MSTP config name
#### Syntax ####
`spanning-tree config-name <configuration-name>`
#### Description ####
This command set config name for MSTP.
#### Authority ####
All users.
#### Parameters ####
| Parameter            | Status    | Description |
|:---------------------|:----------|:--------------|
| *configuration-name* | Required  | Specifies the MSTP configuration name |
#### Examples ####
```
switch# configure terminal
switch# spanning-tree config-name MST0
```
### Set default MSTP config name
#### Syntax ####
`spanning-tree config-name <configuration-name>`
#### Description ####
This command set config name for MSTP.
#### Authority ####
All users.
#### Parameters ####
| Parameter     |  Status      | Description |
|:--------------|:-------------|:----------------|
| *config-name* | Optional     | Specifies the MSTP configuration name |
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree config-name
```
### Set MSTP config revision number
#### Syntax ####
`spanning-tree config-revision <revision-number>`
#### Description ####
This command set config revision number for the all the instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter         | Status   | Syntax         | Description |
|:------------------|:---------|:---------------|:--------------|
| *revision-number* | Required | <1-40>         | Specifies the MSTP configuration revision number value|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree config-revision 40
```
### Add VLAN to instance
#### Syntax ####
`spanning-tree instance <instance-id> vlan <VLAN-ID>`
#### Description ####
This command maps the VLAN-ID to corresponding  instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter     | Status   | Syntax    | Description   |
|:--------------|:---------|:----------|:--------------|
| *instance-id* | Required | <1-64>    | Specifies the MSTP instance number|
| *VLAN-ID*     | Required | <1-4094>  | Specifies the VLAN-ID number|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree instance 1 vlan 1
switch# spanning-tree instance 1 vlan 2
```
### Remove VLAN from instance
#### Syntax ####
`no spanning-tree instance <instance-id> vlan <VLAN-ID>`
#### Description ####
This command removes the VLAN-ID from the MSTP instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter     | Status   | Syntax    | Description   |
|:--------------|:---------|:----------|:--------------|
| *instance-id* | Required | <1-64>    | Specifies the MSTP instance number|
| *VLAN-ID*     | Required | <1-4094>  | Specifies the VLAN-ID number|
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree instance 1 vlan 1
switch# no spanning-tree instance 1 vlan 2
```
###Set forward delay
#### Syntax ####
`spanning-tree forward-delay <delay-in-secs>`
#### Description ####
This command set the forward-delay for all the MSTP instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *delay-in-secs*| Required | <4-30>    | Specifies the forward delay in secs|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree forward-delay 6
```
###Set default forward delay
#### Syntax ####
`no spanning-tree forward-delay [<delay-in-secs>]`
#### Description ####
This command set the default forward-delay for all the MSTP instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *delay-in-secs*| Optional | <4-30>    | Specifies the forward delay in secs|
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree forward-delay
```
###Set hello time
#### Syntax ####
`spanning-tree hello-time <hello-in-secs>`
#### Description ####
This command set the hello interval for all the MSTP instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *hello-in-secs*| Required | <2-10>    | Specifies the hello interval in secs|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree hello-time 6
```
###Set default hello time
#### Syntax ####
`no spanning-tree hello-time [<hello-in-secs>]`
#### Description ####
This command set the default hello interval for all the MSTP instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *hello-in-secs*| Optional | <2-10>    | Specifies the hello interval in secs|
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree hello-time
```
###Set max age
#### Syntax ####
`spanning-tree max-age <age-in-secs>`
#### Description ####
This command set the max age for all the MSTP instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *age-in-secs*  | Required | <6-30>    | Specifies the max age in secs|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree max-age 10
```
###Set default max age
#### Syntax ####
`no spanning-tree max-age [<age-in-secs>]`
#### Description ####
This command set the default max age for all the MSTP instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *age-in-secs*  | Optional | <6-30>    | Specifies the max age in secs|
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree max-age
```
###Set max hops
#### Syntax ####
`spanning-tree max-hops <hop-count>`
#### Description ####
This command set the hop count for all the MSTP instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *hop-count*    | Required | <1-40>    | Specifies the maximum number of hops|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree max-hops 10
```
###Set default max hops
#### Syntax ####
`no spanning-tree max-hops [<hop-count>]`
#### Description ####
This command set the default hop count for all the MSTP instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *hop-count*    | Optional | <1-40>    | Specifies the maximum number of hops|
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree max-hops
```
###Set port type
#### Syntax ####
`spanning-tree port-type (admin-edge | admin-network)`
#### Description ####
This command set the port-type for all the MSTP instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *admin-edge*   | Optional |Specifies the port as admin-edge|
| *admin-network*| Optional |Specifies the port as admin-network|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree port-type admin-edge
switch# spanning-tree port-type admin-network
```
###Set default port type
#### Syntax ####
`no spanning-tree port-type [admin-edge | admin-network]`
#### Description ####
This command set the default port-type for all the MSTP instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *admin-edge*   | Optional |Specifies the port as admin-edge|
| *admin-network*| Optional |Specifies the port as admin-network|
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree port-type
```
###Enable port guard
#### Syntax ####
`spanning-tree {bpdu-guard | root-guard | loop-guard | bpdu-filter} [enable | disable]`
#### Description ####
This command enable the port guard for all the MSTP instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *bpdu-guard*   | Optional |Specifies the bpdu-guard|
| *root-guard*   | Optional |Specifies the root-guard|
| *loop-guard*   | Optional |Specifies the loop-guard|
| *bpdu-filter*  | Optional |Specifies the bpdu-filter|
| *enable*       | Optional |Specifies the status parameter|
| *disable*      | Optional |Specifies the status parameter|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree bpdu-guard enable
switch# spanning-tree root-guard disable
```
# MSTP show commands
### show spanning tree global configuration
#### Syntax ####
`show spanning-tree`
#### Description ####
This command shows priority, address, Hello-time, Max-age, Forward-delay for bridge and root node.
#### Authority ####
All users.
#### Examples ####
```
MST0
  Spanning tree enabled protocol mstp
  Root ID    Priority   : 32768
             MACADDRESS : 70:72:cf:e1:b9:16
             This bridge is the root
             Hello time : 2     Max Age : 20    Forward Delay : 15


  Bridge ID  Priority   : 32768
             MACADDRESS : 70:72:cf:e1:b9:16
             Hello time : 2     Max Age : 20    Forward Delay : 15


Interface    Role  State    Cost       Priority Type
------------ ----- -------- ---------- -------- --------

```
# MSTP show commands
### show MSTP global configuration
#### Syntax ####
`show spanning-tree mst-config`
#### Description ####
This command shows MSTP instance and corresponding vlans.
#### Authority ####
All users.
#### Examples ####
```
MST Configuration Identifier Information
   MST Configuration Identifier Information : MST0
   MST Configuration Revision     : 33
   Instances configured           : 2

Instance ID     Mapped VLANs
--------------- ----------------------------------
3               3
1               1,2
```
### show MSTP running configuration
#### Syntax ####
`show running-config spanning-tree`
#### Description ####
This command shows configured commands for MSTP.
#### Authority ####
All users.
#### Examples ####
```
spanning-tree enable
spanning-tree config-name MST0
spanning-tree config-revision 33
spanning-tree instance 3 vlan 3
spanning-tree instance 1 vlan 1,2
```

DHCP TFTP Commands
-------
[TOC]

## DHCP-TFTP Server Configuration Commands <a id="dhcptftpmain"></a> ##
In vtysh every command belongs to a particular context. All dhcp server configuration commands, except "dhcp-server", works in dhcp server context. All tftp server configuration commands,except "tftp-server", works in tftp server context.
### Change to dhcp server context <a id="dhcpservercontext"></a> ###
### Syntax ###
`dhcp-server`
#### Description ####
This commad changes vtysh context to dhcp server. This command works in config context.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)#
```
### Set DHCP Dynamic configuration <a id="dhcpdynamic"></a> ###
### Syntax ###
`range <range-name> start-ip-address ( <ipv4_address> | <ipv6_address> ) end-ip-address ( <ipv4_address> | <ipv6_address> ) netmask <subnet_mask> broadcast <broadcast_address> match tags <match_tag_names> set tag <set_tag_name> prefix-len <prefix_length_value> lease-duration <lease_duration_value> static`
#### Description ####
This command works in the dhcp-server context. This command sets DHCP dynamic configuration values for the DHCP server. Parameters netmask and broadcast should not be set for IPv6 and prefix-len should not be set for IPv4. Parameter end-ip-address must be set before setting netmask. Parameter netmask must be set before broadcast. Parameter static should be specified only for static IP address allocation within the range set. Parameters netmask, broadcast, match tags, set tags, perfix-len, lease-duration and static are optional. The default value of prefix-len is 64 and the default value of lease-duration is 60 minutes. Parameter match tags can have multiple tags and parameter set tag should be single tag.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description                                |
|:-----------|:----------------:|:---------------------------------------|
| *range-name*   | string | Set DHCP dynamic configuration name.Length must be less than 15.
| *ipv4_address* | A.B.C.D | Set IPV4 address.
| *ipv6_address* | X:X::X:X | Set IPV6 address.
| *subnet_mask*  | A.B.C.D  | Set the network mask.
| *broadcast_address* | A.B.C.D | Set the broadcast address.
| *match_tag_names* | string | Set the match tags list.Each tag length must be less than 15.
| *set_tag_name* | string | Set the set tag name.Length must be less than 15.
| *prefix-len* | 64-128 | Set the IPV6 prefix length value.
| *lease-duration* | value in minutes | Set the lease duration value.
#### Example ###
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)# range dynamic start-ip-address 10.0.0.1 end-ip-address 10.255.255.254 netmask 255.0.0.0 broadcast 10.255.255.255 match tags tag1,tag2,tag3 set tag tag4
```
### Remove DHCP Dynamic configuration <a id="dhcpnodynamic"></a> ###
### Syntax ###
`no range <range-name> start-ip-address ( <ipv4_address> | <ipv6_address> ) end-ip-address ( <ipv4_address> | <ipv6_address> ) netmask <subnet_mask> broadcast <broadcast_address> match tags <match_tag_names> set tag <set_tag_name> prefix-len <prefix_length_value> lease-duration <lease_duration_value> static`
#### Description ####
This command works in the dhcp-server context.This command deletes DHCP dynamic configuration values.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description                                |
|:-----------|:----------------:|:---------------------------------------|
| *range-name*   | string | Specify DHCP dynamic configuration name.Length must be less than 15.
| *ipv4_address* | A.B.C.D | Specify IPV4 address.
| *ipv6_address* | X:X::X:X | Specify IPV6 address.
| *subnet_mask*  | A.B.C.D  | Specify the network mask.
| *broadcast_address* | A.B.C.D | Specify the broadcast address.
| *match_tag_names* | string | Specify the match tags list.Each tag length must be less than 15.
| *set_tag_name* | string | Specify the set tag name.Length must be less than 15.
| *prefix-len* | 64-128 | Specify the IPV6 prefix length value.
| *lease-duration* | value in minutes | Specify the lease duration value in minutes
#### Example ###
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)# no range dynamic start-ip-address 10.0.0.1 end-ip-address 10.255.255.254 netmask 255.0.0.0 broadcast 10.255.255.255 match tags tag1,tag2,tag3 set tag tag4
```
### Set DHCP Static configuration <a id="dhcpstatic"></a> ###
### Syntax ###
`static  ( <ipv4_address> | <ipv6_address> ) match-mac-addresses <mac_addresses> match-client-hostname <hostname> match-client-id <client-id> set tags <set_tag_names> lease-duration <lease_duration_value>`
#### Description ####
This command works in the dhcp-server context. This command sets DHCP static configuration values for the DHCP server. Parameters match-mac-addresses, match-client-hostname, match-cliend-id are optional but atleast one among the three must be specified. Multiple MAC addresses can be specified for the parameter match-mac-addresses and multiple tags can be specified for the parameter set tags. Parameters set tags and lease-duration are optional and the default value of lease-duration is 60 minutes.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description                                |
|:-----------|:----------------:|:---------------------------------------|
| *ipv4_address* | A.B.C.D | Set IPV4 address.
| *ipv6_address* | X:X::X:X | Set IPV6 address.
| *mac_addresses*  | XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX | Set the MAC address.
| *hostname* | string | Set the client hostname.Length must be less than 15.
| *client-id* | string | Set the client id.Length must be less than 15.
| *set_tag_names* | string | Set the set tags list.Each tag length must be less than 15.
| *lease-duration* | value in minutes | Set the lease duration value.
#### Example ###
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)#static 10.0.0.25 match-mac-addresses 36:d4:1b:12:ea:52 match-client-hostname 95_h2 set tags tag1,tag2,tag3 lease-duration 120
```
### Remove DHCP Static configuration <a id="dhcpnostatic"></a> ###
### Syntax ###
`no static  ( <ipv4_address> | <ipv6_address> ) match-mac-addresses <mac_addresses> match-client-hostname <hostname> match-client-id <client-id> set tags <set_tag_names> lease-duration <lease_duration_value>`
#### Description ####
This command works in the dhcp-server context.This command removes DHCP static configuration values for the DHCP server.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description                                |
|:-----------|:----------------:|:---------------------------------------|
| *ipv4_address* | A.B.C.D | Specify IPV4 address.
| *ipv6_address* | X:X::X:X | Specify IPV6 address.
| *mac_addresses*  | XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX | Specify the MAC address.
| *hostname* | string | Specify the client hostname.Length must be less than 15.
| *client-id* | string | Specify the client id.Length must be less than 15.
| *set_tag_names* | string | Specify the set tags list.Each tag Length must be less than 15.
| *lease-duration* | value in minutes | Specify the lease duration value.
#### Example ###
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)#no static 10.0.0.25 match-mac-addresses 36:d4:1b:12:ea:52 match-client-hostname 95_h2 set tags tag1,tag2,tag3 lease-duration 120
```
### Set DHCP Options configuration using option name <a id="dhcpoptionname"></a> ###
### Syntax ###
`option set option-name <option_name> option-value <option_value>  match tags <match_tag_names> ipv6`
#### Description ####
This command works in the dhcp-server context. This command sets DHCP option configuration values for the DHCP server by specifying the option name. Parameter match-tags is optional. Multiple tags can be specified for the parameter match-tags. The optional parameter ipv6 specifies whether the options are IPv6 options or not.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description                                |
|:-----------|:----------------:|:---------------------------------------|
| *option_name* | string | Set DHCP option name.Length must be less than 15.
| *option_value* | | Set DHCP option value.
| *match_tag_names* | string | Specify the match tags list.Length must be less than 15.
#### Example ###
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)#option set option-name Router option-value 10.0.0.1 match tags tag1,tag2,tag3
```
### Remove DHCP Options configuration using option name <a id="dhcpnooptionname"></a> ###
### Syntax ###
`no option set option-name <option_name> option-value <option_value>  match tags <match_tag_names> ipv6`
#### Description ####
This command works in the dhcp-server context. This command removes DHCP option configuration values by specifying the option name.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description                                |
|:-----------|:----------------:|:---------------------------------------|
| *option_name* | string | Set DHCP option name.Length must be less than 15.
| *option_value* | | Set DHCP option value.
| *match_tag_names* | string | Specify the match tags list.Each tag length must be less than 15.
#### Example ###
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)# no option set option-name Router option-value 10.0.0.1 match tags tag1,tag2,tag3
```
### Set DHCP Options configuration using option number <a id="dhcpoptionnumber"></a> ###
### Syntax ###
`option set option-number <option_number> option-value <option_value>  match tags <match_tag_names> ipv6`#### Description ####
This command works in the dhcp-server context. This command sets DHCP option configuration values for the DHCP server by specifying the option number. Parameter match-tags is optional. Multiple tags can be specified for the parameter match-tags. The optional parameter ipv6 specifies whether the options are IPv6 options or not.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description                                |
|:-----------|:----------------:|:---------------------------------------|
| *option_number* | 0-255 | Set DHCP option number.
| *option_value* | | Set DHCP option value.
| *match_tag_names* | string | Set the match tags list.Each tag length must be less than 15.
#### Example ###
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)#option set option-number 3 option-value 10.0.0.1 match tags tag1,tag2,tag3```
### Remove DHCP Options configuration using option number <a id="dhcpnooptionnumber"></a> ###
### Syntax ###
`no option set option-number <option_number> option-value <option_value>  match tags <match_tag_names> ipv6`
#### Description ####
This command works in the dhcp-server context. This command removes DHCP option configuration values by specifying the option number.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description                                |
|:-----------|:----------------:|:---------------------------------------|
| *option_number* | 0-255 | Specify DHCP option name.
| *option_value* | | Specify DHCP option value.
| *match_tag_names* | string | Specify the match tags list.Each tag length must be less than 15.
#### Example ###
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)# no option set option-number 3 option-value 10.0.0.1 match tags tag1,tag2,tag3
```
### Set DHCP Match configuration using option name <a id="dhcpmatchoptionname"></a> ###
### Syntax ###
`match set tag <set_tag_name> match-option-name <option_name> match-option-value <option_value>`
#### Description ####
This command works in the dhcp-server context. Parameter option-value is optional. If option-value is not specified, this command sets the tag if the client sends a DHCP option of the given name. If the option-value is specified, then the tag would be set only if the option is sent and matches the value.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description                                |
|:-----------|:----------------:|:---------------------------------------|
| *set_tag_name* | string | Set the set tag name.Length must be less than 15.
| *option_name* | string | Set DHCP option name.Length must be less than 15.
| *option_value* | | Set DHCP option value.
#### Example ###
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)# match set tag tag1 match-option-name Router match-option-value 10.0.0.1
```
### Removes DHCP Match configuration using option name <a id="dhcpnomatchoptionname"></a> ###
### Syntax ###
`no match set tag <set_tag_name> match-option-name <option_name> match-option-value <option_value>`
#### Description ####
This command works in the dhcp-server context. This command removes the dhcp match configuration.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description                                |
|:-----------|:----------------:|:---------------------------------------|
| *set_tag_name* | string | Set the set tag name.Length must be less than 15.
| *option_name* | string | Set DHCP option name.Length must be less than 15.
| *option_value* | | Set DHCP option value.
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)# no match set tag tag1 match-option-number 3 match-option-value 10.0.0.1
```
### Set DHCP Match configuration using option number <a id="dhcpmatchoptionnumber"></a> ###
### Syntax ###
`match set tag <set_tag_name> match-option-number <option_number> match-option-value <option_value>`
#### Description ####
This command works in the dhcp-server context. Parameter option-value is optional. If option-value is not specified, this command sets the tag if the client sends a DHCP option of the given number. If the option-value is specified, then the tag would be set only if the option is sent and matches the value.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description                                |
|:-----------|:----------------:|:---------------------------------------|
| *set_tag_name* | string | Set the set tag name.Length must be less than 15.
| *option_number* | 0-255 | Set DHCP option number.
| *option_value* | | Set DHCP option value.
#### Example ###
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)# match set tag tag1 match-option-number 3 match-option-value 10.0.0.1
```
### Removes DHCP Match configuration using option number <a id="dhcpnomatchoptionnumber"></a> ###
### Syntax ###
`no match set tag <set_tag_name> match-option-number <option_number> match-option-value <option_value>`
#### Description ####
This command works in the dhcp-server context.This command removes the dhcp match configuration.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description                                |
|:-----------|:----------------:|:---------------------------------------|
| *set_tag_name* | string | Set the set tag name.
| *option_number* | string | Set DHCP option number.
| *option_value* | | Set DHCP option value.
#### Example ###
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)#no match set tag tag1 match-option-number 3 match-option-value 10.0.0.1
```
### Set DHCP BOOTP configuration <a id="dhcpbootp"></a> ###
### Syntax ###
`boot set file <file_name> match tag <match_tag_name>`
#### Description ####
This command works in the dhcp-server context. This command set the BOOTP options to be returned by the DHCP server.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description                                |
|:-----------|:----------------:|:---------------------------------------|
| *file_name* |  | Set the file name.
| *match_tag_name* | string | Set match tag name.Length must be less than 15.
#### Example ###
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)# boot set file /tmp/tftp_file match tag tag1
```
### Remove DHCP BOOTP configuration <a id="dhcpnobootp"></a> ###
### Syntax ###
`no boot set file <file_name> match tag <match_tag_name>`
#### Description ####
This command works in the dhcp-server context. This command removes the BOOTP options.
#### Authority
All users.
#### Parameters
| Parameter | Syntax | Description                                |
|:-----------|:----------------:|:---------------------------------------|
| *file_name* |  | Set the file name.
| *match_tag_name* | string | Set match tag name.Length must be less than 15.
#### Example ###
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)# no boot set file /tmp/tftp_file match tag tag1
```
### Change to tftp server context <a id="tftpservercontext"></a> ###
### Syntax
`tftp-server`
#### Description ####
This commad changes vtysh context to tftp server.This command works in config context.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
ops-as5712# configure terminal
ops-as5712(config)# tftp-server
ops-as5712(config-tftp-server)#
```
### Enabling TFTP Server ### <a id="tftpenable"></a> ###
### Syntax ###
`enable`
#### Description ####
This command works in the tftp-server context. This command enables the TFTP Server.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
ops-as5712# configure terminal
ops-as5712(config)# tftp-server
ops-as5712(config-tftp-server)# enable
```
### Disabling TFTP Server ### <a id="tftpdisable"></a>
### Syntax ###
`disable`
#### Description ####
This command works in the tftp-server context. This command disables the TFTP Server.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
ops-as5712# configure terminal
ops-as5712(config)# tftp-server
ops-as5712(config-tftp-server)# no enable
```
### Enabling TFTP Server Secure mode ### <a id="tftpenablesecure"></a>
### Syntax ###
`secure-mode`
#### Description ####
This command works in the tftp-server context. This command enables the TFTP server secure mode.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
ops-as5712# configure terminal
ops-as5712(config)# tftp-server
ops-as5712(config-tftp-server)# secure-mode
```
### Disabling TFTP Server Secure mode### <a id="tftpdisablesecure"></a>
### Syntax ###
`no secure-mode`
#### Description ####
This command works in the tftp-server context. This command disables the TFTP server secure mode.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
ops-as5712# configure terminal
ops-as5712(config)# tftp-server
ops-as5712(config-tftp-server)# no secure-mode
```
### Set TFTP root ### <a id="tftproot"></a>
### Syntax ###
`path <path_name>`
#### Description ####
This command works in the tftp-server context. This command sets the tftp root path location.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Description |
|:-----------|:---------------------------------------|
| *path* | Set the tftp root path location.
#### Examples ####
```
ops-as5712# configure terminal
ops-as5712(config)# tftp-server
ops-as5712(config-tftp-server)# path /tmp/
```
## DHCP-TFTP Server Show Commands <a id="showdhcptftpserver"></a> ##
### Show DHCP Server Configuration <a id="showdhcpserverconf"></a> ###
#### Syntax ####
`show dhcp-server`
#### Description ####
This command displays various DHCP server configurations. The configuration includes the DHCP Dynamic configuration, DHCP Static Configuration, DHCP Options configuration, DHCP Match configuration and DHCP BOOT configuration.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Example ####
```
ops-as5712# show dhcp-server

DHCP dynamic IP allocation configuration
----------------------------------------
Name     Start IP Address    End IP Address    Netmask     Broadcast
----------------------------------------------------------------------------
dynamic  10.0.0.1           10.255.255.254    255.0.0.0   10.255.255.255


DHCP static IP allocation configuration
---------------------------------------
IP Address  Hostname  Lease time  MAC-Address        Set tags
----------------------------------------------------------------------------
10.0.0.25   95_h2     65          36:d4:1b:12:ea:52  tag1,tag2,tag3


DHCP options configuration
--------------------------
Option Number  Option Name       Option Value          ipv6   Match tags
----------------------------------------------------------------------------
3              *                 10.0.0.1              False  tag1,tag2,tag3
*              Router            10.0.0.1              False  tag1,tag2,tag3


DHCP Match configuration
------------------------
Option Number  Option Name       Option Value          Set tag
--------------------------------------------------------------
3              *                 10.0.0.1              tag1
*              Router            10.0.0.1              tag1


DHCP BOOTP configuration
------------------------
Tag               File
----------------------
tag1              /tmp/tftp_file
```

### Show DHCP Server Leases configurations <a id="showdhcpleases"></a> ###
#### Syntax ####
`show dhcp-server leases`
#### Description ####
This command displays DHCP Server leases configurations.The configurations contains the IP address, MAC address, lease expiry time, client hostname and client id. The configurations are updated by the DHCP Server after it assigns an IP address to the client.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Example ####
```
ops-as5712# show dhcp-server leases
Expiry Time               MAC Address        IP Address  Hostname and Client-id
-------------------------------------------------------------------------------
Wed Sep 23 23:07:12 2015  df:36:12:1b:54:ea  10.0.0.5    95_h1            *
Wed Sep 23 22:05:10 2015  36:d4:1b:12:ea:52  10.0.0.25   95_h2            *
```

### Show TFTP Server Configuration <a id="showtftpserverconf"></a> ###
#### Syntax ####
`show tftp-server`
#### Description ####
This command displays TFTP server configurations.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Example ####
```
ops-as5712# show tftp-server

TFTP server configuration
-------------------------
TFTP server : Enabled
TFTP server secure mode : Enabled
TFTP server file path : /tmp/
```

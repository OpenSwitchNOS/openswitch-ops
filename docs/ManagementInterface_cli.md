
<!--  See the https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet for additional information about markdown text.
Here are a few suggestions in regards to style and grammar:
* Use active voice. With active voice, the subject is the doer of the action. Tell the reader what
to do by using the imperative mood, for example, Press Enter to view the next screen. See https://en.wikipedia.org/wiki/Active_voice for more information about the active voice. 
* Use present tense. See https://en.wikipedia.org/wiki/Present_tense for more information about using the present tense. 
* Avoid the use of I or third person. Address your instructions to the user. In text, refer to the reader as you (second person) rather than as the user (third person). The exception to not using the third-person is when the documentation is for an administrator. In that case, *the user* is someone the reader interacts with, for example, teach your users how to back up their laptop. 
* See https://en.wikipedia.org/wiki/Wikipedia%3aManual_of_Style for an online style guide.
Note regarding anchors:
--StackEdit automatically creates an anchor tag based off of each heading.  Spaces and other nonconforming characters are substituted by other characters in the anchor when the file is converted to HTML. 
 --> 
Configuration support for Management Interface 
=======

<!--Provide the name of the grouping of commands, for example, LLDP commands-->

 1. Management interface configuration commands
 
	1.1  Management Interface Context Command

	1.2  Static Mode configuration

	1.3  DHCP Mode configuration

	1.4  Default Gateway configuration

	1.5  Nameserver configuration

 2. Management interface show commands
 
 	2.1 Show command

	2.2 Show running configuration

	2.3 Show running configuration for interface level

 
## 1. Management interface Configuration Commands ##
<!-- Change LLDP -->
### 1.1 Management Interface Context ###
This command is used to enter the management interface context.
#### Syntax ####
<!--For example,    myprogramstart [option] <process_name> -->
interface mgmt

#### Description ####
<!--Provide a description of the command. -->
This command is used to enter the management interface. All the management interface commands are available in this context only.
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
Admin
#### Parameters ####
<!--Provide for the parameters for the command.-->
None

#### Examples ####
<!--    myprogramstart -s process_xyz-->
	(conf #) interface mgmt

### 1.2 Static Mode Configuration ###
This command is used to configure the mode of the management interface as static.
#### Syntax ####
<!--For example,    myprogramstart [option] <process_name> -->
ip static { ipv4/subnet | ipv6/subnet}

#### Description ####
<!--Provide a description of the command. -->
This command is used to configure the IP address of the management interface. Both Ipv4 and IPv6 address is supported.
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
Admin
#### Parameters ####
<!--Provide for the parameters for the command.-->
This command is executed in the management interface context.

All valid IPv4 and IPv6 address (Reserved IP, Multicast IP, Broadcast IP and loopback address are not allowed) can be configured. It is possible to configure both IPv4 and IPv6 address. 
However, only one IP acn be configured per address family.
#### Examples ####
<!--    myprogramstart -s process_xyz-->
	as5712(config-if-mgmt)#ip static 192.168.1.10/16
	
	as5712(config-if-mgmt)#ip static 2001:db8:0:1::129/64 
### 1.3 DHCP mode configuration ###
<!--Change the value of the anchor tag above, so this command can be directly linked. -->
This command configures the mode of management interface as DHCP.
#### Syntax ####
<!--For example,    myprogramstart [option] <process_name> -->
ip dhcp
#### Description ####
<!--Provide a description of the command. -->
When the mode is set to dhcp, the IP and other management interface attributes are received from DHCP server. Any static configuration configured earlier is removed when the mode is changed to dhcp.
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
Admin
#### Parameters ####
<!--Provide for the parameters for the command.-->
None
#### Examples ####
<!--    myprogramstart -s process_xyz-->
	as5712(config-if-mgmt)#ip dhcp

### 1.4 Default Gateway configuration ###
<!--Change the value of the anchor tag above, so this command can be directly linked. -->
This command configures the IPv4 and IPv6 default gateway.
#### Syntax ####
<!--For example,    myprogramstart [option] <process_name> -->
[no] default-gateway {ipv4-address | ipv6-address}
#### Description ####
<!--Provide a description of the command. -->
The default gateway can be manually configured only in static mode. An IPv4 default gateway can be configured only if IPv4 address is configured on the management interface. Same argument holds good for IPv6 also. It is possible to configure both IPv4 and IPv6 addresses.
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
Admin
#### Parameters ####
<!--Provide for the parameters for the command.-->
This command is executed in the management interface context.

All valid IPv4 and IPv6 address (Reserved IP, Multicast IP, Broadcast IP and loopback address are not allowed) can be configured.  
However, only one IP can be configured per address family.

When "no" is specified the default gateway specified is removed. If user tries to remove a default gateway that was not configured, error messages is displayed.
#### Examples ####
<!--    myprogramstart -s process_xyz-->
	as5712(config-if-mgmt)#default-gateway 192.168.1.5
	
	as5712(config-if-mgmt)#default-gateway 2001:db8:0:1::128
	
	as5712(config-if-mgmt)#no default-gateway 192.168.1.5
	
	as5712(config-if-mgmt)#no default-gateway 2001:db8:0:1::128
### 1.5 Nameserver configuration ###
<!--Change the value of the anchor tag above, so this command can be directly linked. -->
This command configures the nameserver.
#### Syntax ####
<!--For example,    myprogramstart [option] <process_name> -->
[no] nameserver address-1 [address-2]
#### Description ####
<!--Provide a description of the command. -->
The nameserver can be manually configured only in static mode. It is possible to configure both IPv4 and IPv6 addresses. It is also possible to configure one nameserver as IPv4 address and the other one as IPv6 address. An IPv4 nameserver can be configured only if IPv4 address is configured on the management interface. Same argument holds good for IPv6 also.
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
Admin
#### Parameters ####
<!--Provide for the parameters for the command.-->
This command is executed in the management interface context.

All valid IPv4 and IPv6 address (Reserved IP, Multicast IP, Broadcast IP and loopback address are not allowed) can be configured.  

Address-1 is configured as primary nameserver and Address-2 (if specified) is configured as secondary nameserver.

When "no" is specified the namserver specified is removed. If user tries to remove a nameserver that was not configured, error messages is displayed. It is not possible to remove secondary nameserver without removing the primary nameserver.
#### Examples ####
<!--    myprogramstart -s process_xyz-->
	as5712(config-if-mgmt)#nameserver 192.168.1.1
	
	as5712(config-if-mgmt)#nameserver 192.168.1.2 192.168.1.3
	
	as5712(config-if-mgmt)#nameserver 2001:db8:0:1::100
	
	as5712(config-if-mgmt)#nameserver 2001:db8:0:2::100 2001:db8:0:3::150
	
	as5712(config-if-mgmt)#no nameserver 192.168.1.2 192.168.1.3
	
	as5712(config-if-mgmt)#no nameserver 2001:db8:0:2::100 2001:db8:0:3::150

##2. Display Commands ##
### 2.1 show command ###
<!--Change the value of the anchor tag above, so this command can be directly linked. -->
#### Syntax ####
<!--For example,    myprogramstart [option] <process_name> -->
show interface mgmt
#### Description ####
<!--Provide a description of the command. -->
The show command displays the attributes of management interface like IP, subnet, default gateway and nameserver.
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
all users
#### Parameters ####
<!--Provide for the parameters for the command.-->
None
#### Examples ####
<!--    myprogramstart -s process_xyz-->
	as5712#show interface mgmt
	
	  Address Mode 						: static
	
	  IPv4 address/subnet-mask 			: 192.168.1.100/16
	
	  Default gateway IPv4   			: 192.168.1.5
	
	  IPv6 address/prefix       	    : 2001:db8:0:1::129/64
	
	  IPv6 link local address/prefix	: fe80::7272:cfff:fefd:e485/64
	
	  Default gateway IPv6          	: 2001:db8:0:1::128
	
	  Primary Nameserver                : 2001:db8:0:2::100
	
	  Secondary Nameserver              : 2001:db8:0:3::150 

### 2.2 Show running configuration ###
<!--Change the value of the anchor tag above, so this command can be directly linked. -->
#### Syntax ####
<!--For example,    myprogramstart [option] <process_name> -->
show running-config
#### Description ####
<!--Provide a description of the command. -->
To display the configuration on the switch
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
admin
#### Parameters ####
<!--Provide for the parameters for the command.-->
None
#### Examples ####
<!--    myprogramstart -s process_xyz-->
The example shows the interface management information in the show running-config output.

	as5712# show running-config
	Current configuration:
	!
	interface mgmt
	    ip static 192.168.1.100/16
	    ip static 2001:db8:0:1::129/64
	    default-gateway 192.168.1.5
	    default-gateway 2001:db8:0:1::128
	    nameserver 2001:db8:0:2::100 2001:db8:0:3::150

### 2.3 Show running configuration for interface level###
<!--Change the value of the anchor tag above, so this command can be directly linked. -->
#### Syntax ####
<!--For example,    myprogramstart [option] <process_name> -->
show running-config interface mgmt
#### Description ####
<!--Provide a description of the command. -->
To display the configuration on the switch at the interface level.
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
admin
#### Parameters ####
<!--Provide for the parameters for the command.-->
None
#### Examples ####
<!--    myprogramstart -s process_xyz-->
The example shows the interface management information in the show running-config output.

	as5712# show running-config interface mgmt
	Current configuration:
	!
	interface mgmt
	    ip static 192.168.1.100/16
	    ip static 2001:db8:0:1::129/64
	    default-gateway 192.168.1.5
	    default-gateway 2001:db8:0:1::128
	    nameserver 2001:db8:0:2::100 2001:db8:0:3::150


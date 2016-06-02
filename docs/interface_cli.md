# Interface Commands

## Contents
- [Configuration commands](#configuration-commands)
	- [interface](#interface)
	- [description](#description)
	- [shutdown](#shutdown)
	- [routing](#routing)
	- [speed](#speed)
	- [mtu](#mtu)
	- [duplex](#duplex)
	- [flowcontrol](#flowcontrol)
	- [Setting the autonegotiation state](#setting-the-autonegotiation-state)
	- [ip address](#ip-address)
	- [ipv6 address](#ipv6-address)
	- [split](#split)
- [Display commands](#display-commands)
	- [show interface](#show-interface)
	- [show interface transceiver](#show-interface-transceiver)
	- [show running-config interface](#show-running-config-interface)
	- [show interface dom](#show-interface-dom)

## Configuration commands

### interface

#### Syntax
`interface <interface-name>`

#### Description
Changes to interface mode for the specified interface. To see a list of supported interfaces, use the `show interface` command.

#### Command mode
Configuration mode (config).

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:----------|:---------|:---------------|:--------------------------------------|
| *interface-name* | Required | String | Name of an interface on the switch. |

#### Example
```
switch(config)# interface 1
switch(config-if)#
```


### description

#### Syntax
```
description <description>
no description
```

#### Description
Adds a description to an interface.

Use the `no` form of this command to remove an interface description.

#### Command mode
Interface mode (config-if).

#### Authority
All users.

#### Parameters
| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:--------------------------|
| *description* | Required | String | Description of the interface. |

#### Examples

###### Adding a description to an interface
```
switch(config-if)# description This is interface 1
```

###### Removing a description from an interface
```
switch(config-if)# no description
```


### shutdown

#### Syntax
```
shutdown
no shutdown
```

#### Description
Disables an interface.

Use the `no` form of this command to enable an interface.

#### Command mode
Interface mode (config-if).

#### Authority
All users.

#### Parameters
None.

#### Examples

###### Enabling interface 1
```
switch(config)# interface 1
switch(config-if)# no shutdown
```

###### Disabling interface 1
```
switch(config)# interface 1
switch(config-if)# shutdown
```


### routing

#### Syntax
```
routing
no routing
```

#### Description
Enables routing on an interface, creating a L3 (layer 3) interface on which the switch can route IPv4/IPv6 traffic to other devices.

Use the `no` form of this command to disable routing on the interface.

#### Command mode
Interface mode (config-if).

#### Authority
All users.

#### Parameters
None.

#### Examples

###### Enabling routing on interface 1
```
switch(config)# interface 1
switch(config-if)# routing
```

###### Disabling routing on interface 1
```
switch(config)# interface 1
switch(config-if)# no routing
```


### speed

#### Syntax
```
speed (auto | 1000 | 10000 | 100000 | 40000)
no speed
```

#### Description
Sets the operating speed of an interface. Choose a value that matches the speed of the interafce, or use `auto` to let the switch negotiate the speed.

Speed settings are dependant on the auto-negotiation state defined by the command `autonegotiation`.

- When `autonegotiation` is enabled, `speed` must be set to `auto`.
- When `autonegotiation` is disabled, `speed` must be set to a static value: 1000, 10000, 100000, or 40000

Use the `no` form of this command to set speed to the default value.

#### Command mode
Interface mode (config-if).

#### Authority
All users.

#### Parameters
| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:--------------------------|
| **auto** | Required | Literal | Sets auto mode which enables the interface to negotiate the speed to be used with the remote device to which it is connected. This is the default setting.|
| **1000** | Required | Literal | Sets the speed to 1 Gbps. |
| **10000** | Required | Literal | Sets the speed to 10 Gbps. |
| **100000** | Required | Literal | Sets the speed to 100 Gbps. |
| **40000** | Required | Literal | Sets the speed to 40 Gbps. |


#### Example

###### Setting interface 1 to 10 Gbps
```
switch(config)# interface 1
switch(config-if)# speed 10000
```

###### Setting interface 1 to default speed
```
switch(config)# interface 1
switch(config-if)# no speed
```


### mtu

#### Syntax
```
mtu (auto | <value>)
no mtu
```

#### Description
Sets the MTU (maximum transmission unit) for an interface. This defines the maximum size an IP packet can be when encapsulated in a layer 2 packet. Packets larger than the MTU are fragmented into multiple parts which can reduce throughtput.

Use the `no` form of this command to set MTU to the default value.

#### Command mode
Interface mode (config-if).

#### Authority
All users.

#### Parameters
| Parameter | Status | Syntax | Description |
|:----------|:-------|:------:|:------------|
| **auto** | Required | Literal | Sets MTU to 1500. Default.|
| *value* | Required | Integer | Sets MTU to value between 576 and 16360 bytes.

#### Examples

###### Setting interface 1 to an MTU of 580
```
switch(config)# interface 1
switch(config-if)# mtu 580
```

###### Setting interface 1 to the default MTU
```
switch(config)# interface 1
switch(config-if)# no mtu
```


### duplex

#### Syntax
```
duplex (half | full)
no duplex
```

#### Description
Sets an interface to be either half-duplex or full-duplex.

Use the `no` form of this command to set duplex to the default value.

#### Command mode
Interface mode (config-if).

#### Authority
All users.

#### Parameters
| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:--------------------------|
| **half** | Required | Literal | Sets half-duplex mode. |
| **full** | Required | Literal | Sets full-duplex mode. Default.|

#### Examples

###### Setting interface 1 to half-duplex
```
switch(config)# interface 1
switch(config-if)# duplex half
```
###### Setting interface 1 to the default value
```
witch(config)# interface 1
switch(config-if)# no duplex
```


### flowcontrol

#### Syntax
```
flowcontrol (receive | send) (off | on)
no flowcontrol (receive | send)
```

#### Description
Enables flow control, which allows the interface to regulate data transmission when communicating with faster or slower devices to ensure no loss of data.

Use the `no` form of this command to set flow control to the default value.

#### Command mode
Interface mode (config-if).

#### Authority
All users.

#### Parameters
| Parameter  | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:--------------------------|
| **receive** | Required | Literal |Configures flow control for receiving data. |
| **send** | Required | Literal |Configures flow control for sending data. |
| **off** | Required | Literal | Disables flow control. Default. |
| **on** | Required | Literal | Enables flow control. |

#### Example

###### Enabling send and receive flow control on interface 1
```
switch(config)# interface 1
switch(config-if)# flowcontrol receive on
switch(config-if)# flowcontrol send on
```

###### Disabling send and receive flow control on interface 1
```
switch(config-if)# no flowcontrol receive
switch(config-if)# no flowcontrol send
```


### autonegotiation

#### Syntax
```
autonegotiation (on | off)
no autonegotiation
```

#### Description
Sets the autonegotiation state of the interface. Controls how the interface speed can be set with the `speed` command.

Use the `no` form of this command to disable autonegotiation.

#### Command mode
Interface mode (config-if).

#### Authority
All users.

#### Parameters
| Parameter  | Status    | Syntax           | Description |
|:-----------|:----------|:----------------:|:--------------------------|
| **off** | Required | Literal | Turns off autonegotiation. Allows static interface speeds to be set. |
| **on** | Required | Literal | Turns on autonegotiation. Enables the interface to negotiate the speed to be used with the remote device to which it is connected. |

#### Examples

###### Enabling autonegotiation on interface 1
```
switch(config)# interface 1
switch(config-if)# autonegotiation on
```

###### Disabling autonegotiation on interface 1
```
switch(config)# interface 1
switch(config-if)# no autonegotiation
```


### ip address

#### Syntax
```
ip address <ipv4-address>/<mask> [secondary]
no ip address <ipv4-address>/<mask> [secondary]
```

#### Description
Sets an IPv4 address on the interface. This command only works when the interface is configured as L3 using the `routing` command. Two IPv4 addresses can be configured per interface.

Use the `no` form of this command to remove an IPv4 address from an interface.

#### Command mode
Interface mode (config-if).

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *ipv4-address* | Required | A.B.C.D | IPv4 adddress to assign to the interface. |
| *mask* | Required | Integer | Mask in CIDR format. |
| **secondary** | Optional| Literal  | Sets the address as the secondary address. |

#### Examples

###### Setting IPv4 addresses on interface 1
```
switch(config)# interface 1
switch(config-if)# ip address 16.93.50.2/24
switch(config-if)# ip address 16.93.50.3/24 secondary
```

###### Deleting IPv4 addresses on interface 1
```
switch(config)# interface 1
switch(config-if)# no ip address 16.93.50.2/24
switch(config-if)# no ip address 16.93.50.3/24 secondary
```


### ipv6 address

#### Syntax
```
ipv6 address <ipv6-address>/<mask> [secondary]
no ipv6 address <ipv6-address>/<mask> [secondary]
```

#### Description
Sets an IPv6 address on the interface. This command only works when the interface is configured as L3 using the `routing` command. Two IPv6 addresses can be configured per interface.

Use the `no` form of this command to remove an IPv6 address from an interface.

#### Command mode
Interface mode (config-if).

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *ipv6-address* | Required | X:X::X:X | IPv6 address to assign to the interface. |
| *mask* | Required | Integer | Mask in CIDR format. |
| **secondary** | Optional| Literal  | Sets the address as the secondary address. |

#### Example

###### Setting IPv6 addresses on interface 1
```
switch(config)# interface 1
switch(config-if)# ipv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:7334/24
switch(config-if)# ipv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:733/24 secondary
```

###### Removing IPv6 addresses on interface 1
```
switch(config)# interface 1
switch(config-if)# no ipv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:7334/24
switch(config-if)# no ipv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:733/24 secondary
```


### split

#### Syntax
```
split
no split
```

#### Description
Splits a 40 Gb Quad Small Form-factor Pluggable (QSPF) port to operate as four seperate 10 Gb interfaces. The QSPF port must support a splitter capable of creating four independent Ethernet connections. Names for the new interfaces a created by appending the suffixes -1,-2,-3, and -4 to the original name for the QSPF port. For example, if the QSPF port name is 54, then the split interface names are: 54-1, 54-2, 54-3, and 54-4.

Use the `no` form of this command to combine the split QSPF port into a single 40 Gb interface.

#### Command mode
Interface mode (config-if).

#### Authority
All users.

#### Parameters
None.

#### Example

###### Splitting interface 54
```
switch(config)# interface 54
switch(config-if)# split
```

###### Combining interface 54
```
switch(config)# interface 54
switch(config-if)# no split
```


## Display commands

### show interface

#### Syntax
`show interface [<interface-name>] [brief]`

#### Description
Displays status and configuration information for switch interfaces.

#### Command mode
Enable mode.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface-name* | Optional | String | Name of an interface. |
| **brief** | Optional| Literal  | Displays the status and configuration information in a table. |

#### Examples

###### Displaying status and configuration information for all interfaces
```
switch# show interface
Interface 1 is down (Administratively down)
Admin state is down
State information: admin_down
Hardware: Ethernet, MAC Address: 70:72:cf:fd:e7:b4
MTU 9388
Half-duplex
Speed 0 Mb/s
Auto-Negotiation is turned on
Input flow-control is on, output flow-control is on
RX
   0 input packets 0 bytes
   0 input error   0 dropped
   0 CRC/FCS
TX
   0 output packets 0 bytes
   0 input error    4 dropped
   0 collision
Interface 10 is down (Administratively down)
Admin state is down
State information: admin_down
Hardware: Ethernet, MAC Address: 70:72:cf:fd:e7:b4
MTU 9388
Half-duplex
Speed 0 Mb/s
Auto-Negotiation is turned on
Input flow-control is on, output flow-control is on
RX
   0 input packets 0 bytes
   0 input error   0 dropped
   0 CRC/FCS
TX
   0 output packets 0 bytes
   0 input error    4 dropped
   0 collision
.........
.........
```

###### Displaying status and configuration information for all interfaces in brief format
```
switch# show interface brief
....................................................................................................
Ethernet      VLAN     Type    Mode    Status         Reason             Speed   Port
Interface                                                                (Mb/s)   Ch#
....................................................................................................
 1             ..       eth     ..      down     Administratively down    auto    ..
 10            ..       eth     ..      down     Administratively down    auto    ..
 11            ..       eth     ..      down     Administratively down    auto    ..
...............
...............

```

###### Displaying status and configuration information for interface 1
```
switch# show interface 1
Interface 1 is up
 Admin state is up
 Hardware: Ethernet, MAC Address: 70:72:cf:fd:e7:b4
 MTU 1500
 Full-duplex
 Speed 1000 Mb/s
 Auto-Negotiation is turned on
 Input flow-control is off, output flow-control is off
 RX
      0 input packets     0 bytes
      0 input error       0 dropped
      0 CRC/FCS
 TX
      0 output packets  0 bytes
      0 input error     0 dropped
      0 collision
```

###### Displaying status and configuration information for interface 1 in brief format
```
switch# show interface 1 brief
....................................................................................................
Ethernet    VLAN   Type   Mode    Status   Reason                    Speed     Port
Interface                                                            (Mb/s)    Ch#
....................................................................................................
  1          ..    eth     ..     down    Administratively down       auto     ..
```


### show interface transceiver

#### Syntax
`show interface [<interface-name>] transceiver [brief]`

#### Description
Displays information about pluggable modules or fixed interfaces present in the switch.

#### Command mode
Enable mode.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface-name* | Optional | String | Name of an interface. |
| **brief** | Optional| Literal  | Displays the information in a table. |

#### Examples

###### Displaying pluggable module information for all interfaces
```
switch# show interface transceiver
Interface 1:
 Connector: SFP+
 Transceiver module: SFP_RJ45
 Connector status: supported
 Vendor name: AVAGO
 Part number: ABCU-5710RZ-HP8
 Part revision:
 Serial number: MY36G2C52D
 Supported speeds: 1000
Interface 10:
 Connector: SFP+
 Transceiver module: not present
Interface 11:
 Connector: SFP+
 Transceiver module: not present
 -------
 -------
```

###### Displaying pluggable module information for all interfaces in brief format
```
switch# show interface transceiver brief
-----------------------------------------------
Ethernet      Connector    Module     Module
Interface                  Type       Status
-----------------------------------------------
 1              SFP+       SFP_RJ45   supported
 10             SFP+       --         --
 11             SFP+       --         --
 12             SFP+       --         --
 13             SFP+       --         --
 -------
 -------
```

###### Displaying pluggable module information for interface 1
```
switch# show interface 1 transceiver
Interface 1:
 Connector: SFP+
 Transceiver module: SFP_RJ45
 Connector status: supported
 Vendor name: AVAGO
 Part number: ABCU-5710RZ-HP8
 Part revision:
 Serial number: MY36G2C52D
 Supported speeds: 1000
```

###### Displaying pluggable module information for interface 1 in brief format
```
switch# show interface 1 transceiver brief
-----------------------------------------------
Ethernet      Connector    Module     Module
Interface                  Type       Status
-----------------------------------------------
 1              SFP+       SFP_RJ45   supported
```


### show running-config interface

#### Syntax
`show running-config interface [<interface-name>]`


#### Description
Displays the currently active configuration for switch interfaces.

#### Command mode
Enable mode.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface-name* | Optional | String | Name of an interface. |

#### Examples

###### Displaying the active configuration for all interfaces
```
switch# show running-config interface
Interface 2
   no shutdown
   speed 40000
   autonegotiation on
   exit
Interface 1
   no shutdown
   exit
.............
.............
```

###### Displaying the active configuration for all interfaces
```
switch# show running-config interface
interface bridge_normal
   no shutdown
   no routing
   exit
interface 2
   no shutdown
   lag 100
   exit
interface lag 100
   no routing
   lacp mode active
```

###### Displaying the active configuration for interface 2
```
switch# show running-config interface 2
Interface 2
   no shutdown
   speed 40000
   autonegotiation on
   exit
```

###### Displaying the active configuration for lag100
```
switch# do show running-config interface lag100
interface lag 100
   no routing
   lacp mode active
```


### show interface dom

#### Syntax
`show interface [<interface-name>] dom`

#### Description
Displays diagnostics information, and alarm and warning flags for optical transceivers (SFP, SFP+, QSFP+), on all interfaces or the specified interface. This information is known as DOM (Digital Optical Monitoring). DOM information also consists of vendor determined thresholds which trigger high/low alarm and warning flags.

#### Command mode
Enable mode.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface-name* | Optional | String | Name of an interface. |

#### Examples

###### Displaying DOM for all interfaces
```
switch# show interface dom
Interface 1:
 Connector: SFP+
 Transceiver module: SFP_SR
  Temperature: 18.00C
  Temperature high alarm: Off
  Temperature low alarm: Off
  Temperature high warning: Off
  Temperature low warning: Off
  Temperature high alarm threshold: 73.00C
  Temperature low alarm threshold: -3.00C
  Temperature high warning threshold: 70.00C
  Temperature low warning threshold: 0.00C
  Voltage: 3.41V
  Voltage high alarm: Off
  Voltage high alarm: Off
  Voltage high alarm: Off
  Voltage low warning: Off
  Voltage high alarm threshold: 3.80V
  Voltage low alarm threshold: 2.81V
  Voltage high warning threshold: 3.46V
  Voltage low warning threshold: 3.13V
  Bias current: 0.16mA
  Bias current high alarm: Off
  Bias current low alarm: On
  Bias current high warning: Off
  Bias current low warning: On
  Bias current high alarm threshold: 13.20mA
  Bias current low alarm threshold: 1.00mA
  Bias current high warning threshold: 12.60mA
  Bias current low warning threshold: 1.00mA
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: On
  Rx power high warning: Off
  Rx power low warning: On
  Rx power high alarm threshold: 1.26mW
  Rx power low alarm threshold: 0.11mW
  Rx power high warning threshold: 0.79mW
  Rx power low warning threshold: 0.18mW
  Tx power: 0.01mW
  Tx power high alarm: Off
  Tx power low alarm: On
  Tx power high warning: Off
  Tx power low warning: On
  Tx power high alarm threshold: 1.00mW
  Tx power low alarm threshold: 0.09mW
  Tx power high warning threshold: 0.79mW
  Tx power low warning threshold: 0.19mW
Interface 3:
 Connector: SFP+
 Transceiver module: SFP_DAC
 % No DOM information available
Interface 4:
 Connector: SFP+
 Transceiver module: SFP_DAC
 % No DOM information available
Interface 5:
 Connector: SFP+
 Transceiver module: not present
Interface 6:
 Connector: SFP+
 Transceiver module: not present
switch# sh int 49 dom
Interface 49:
 Connector: QSFP (splittable)
 Transceiver module: QSFP_SR4
  Temperature: 24.00C
  Voltage: 3.37V
 Lane 1:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off
 Lane 2:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off
 Lane 3:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off
 Lane 4:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off
Interface 50:
 Connector: QSFP (splittable)
 Transceiver module: QSFP_CR4
 % No DOM information available
Interface 50-1:
 Connector: QSFP
Interface 50-2:
 Connector: QSFP
Interface 50-3:
 Connector: QSFP
Interface 50-4:
 Connector: QSFP
Interface 51:
 Connector: QSFP (splittable)
 Transceiver module: not present
```

###### Displaying DOM for interface 1
```
switch# show interface 1 dom
Interface 1:
 Connector: SFP+
 Transceiver module: SFP_SR
  Temperature: 18.00C
  Temperature high alarm: Off
  Temperature low alarm: Off
  Temperature high warning: Off
  Temperature low warning: Off
  Temperature high alarm threshold: 73.00C
  Temperature low alarm threshold: -3.00C
  Temperature high warning threshold: 70.00C
  Temperature low warning threshold: 0.00C
  Voltage: 3.41V
  Voltage high alarm: Off
  Voltage high alarm: Off
  Voltage high alarm: Off
  Voltage low warning: Off
  Voltage high alarm threshold: 3.80V
  Voltage low alarm threshold: 2.81V
  Voltage high warning threshold: 3.46V
  Voltage low warning threshold: 3.13V
  Bias current: 0.16mA
  Bias current high alarm: Off
  Bias current low alarm: On
  Bias current high warning: Off
  Bias current low warning: On
  Bias current high alarm threshold: 13.20mA
  Bias current low alarm threshold: 1.00mA
  Bias current high warning threshold: 12.60mA
  Bias current low warning threshold: 1.00mA
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: On
  Rx power high warning: Off
  Rx power low warning: On
  Rx power high alarm threshold: 1.26mW
  Rx power low alarm threshold: 0.11mW
  Rx power high warning threshold: 0.79mW
  Rx power low warning threshold: 0.18mW
  Tx power: 0.01mW
  Tx power high alarm: Off
  Tx power low alarm: On
  Tx power high warning: Off
  Tx power low warning: On
  Tx power high alarm threshold: 1.00mW
  Tx power low alarm threshold: 0.09mW
  Tx power high warning threshold: 0.79mW
  Tx power low warning threshold: 0.19mW
```

###### Displaying DOM for interface 50
```
switch# show interface 50 dom
Interface 50:
 Connector: QSFP (splittable)
 Transceiver module: QSFP_SR4
  Temperature: 24.00C
  Voltage: 3.37V
 Lane 1:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off
 Lane 2:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off
 Lane 3:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off
 Lane 4:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off
```

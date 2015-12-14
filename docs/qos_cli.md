QoS Commands
======

## Contents
- [Configuration Commands](#configuration-commands)
  - [qos cos-map](#qos-cos-map)
  - [qos dscp-map](#qos-dscp-map)
  - [qos trust](#qos-trust)
- [Display Commands](#display-commands)
  - [Show Running Config](#show-running-config)
  - [Show Running Config Interface](#show-running-config-interface)
  - [Show Interface](#show-interface)

## Configuration Commands

### qos cos-map

#### Syntax
`qos cos-map COS local-priority NUM [color COLOR] [name STRING]`

#### Description
The global cos-map uses the value from the packet header as an index into the cos-map to retrieve the local-class and color assignment.

#### Authority
All users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *COS* | The 802.1 VLAN Priority Code Point.
| *NUM* | The ASIC-specific local priority value.
| *COLOR* | One of the following tokens: 'green', 'yellow', or 'red'.
| *STRING* | Contains up to 64 characters for customer documentation.

#### Examples
```
switch# configure terminal
switch(config)# qos cos-map 1 local-priority 2 color green name EntryName
```

### qos dscp-map

#### Syntax
`qos dscp-map DSCP local-priority NUM [cos COS] [color COLOR] [name STRING]`

#### Description
The global dscp-map uses the value from the packet header as an index into the dscp-map to retrieve the local-class and color assignment.

#### Authority
All users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *DSCP* | The IP Differentiated Services Code Point.
| *NUM* | The ASIC-specific local priority value.
| *COS* | The 802.1 VLAN Priority Code Point.
| *COLOR* | One of the following tokens: 'green', 'yellow', or 'red'.
| *STRING* | Contains up to 64 characters for customer documentation.

#### Examples
```
switch# configure terminal
switch(config)# qos dscp-map 1 local-priority 2 cos 3 color green name EntryName
```

### qos trust

#### Syntax
To configure globally:
`$ qos trust {none|cos|dscp}`

To configure per port:
`interface ### $ [no] qos trust {none|cos|dscp}`

#### Description
The Trust command configures one of three modes that be applied globally or overridden per port.

#### Authority
All users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *none* | Ignores all packet headers. The packet is initially assigned local_priority of zero and color of green.
| *cos* | For 802.1 VLAN tagged packets, use the priority code point field of the outermost VLAN header, if any, as the index into the COS Map. If the packet is untagged, use the meta-data values at index zero of the COS Map.
| *dscp* | For IP packets, use the DSCP field as the index into the DSCP Map. For non-IP packets with VLAN tag(s), use the priority code point field of the outermost tag header as the index into the COS Map.  For untagged non-IP packets, assign use the meta-data values at index zero of the COS Map.

#### Examples
To configure globally:
```
switch# configure terminal
switch(config)# qos trust dscp
```

To configure per port:
```
switch# configure terminal
switch(config)# interface 1
switch(config-if)# qos trust dscp
```

## Display Commands
The following commands show configuration information.

### Show Running Config

#### Syntax
`show running-config`

#### Description
This command displays the QoS settings that have been configured.

#### Authority
All users.

#### Parameters
No parameters.

#### Examples
```
switch# configure terminal
switch(config)# qos trust dscp
switch(config)# interface 1
switch(config-if)# qos trust cos
switch(config-if)# interface lag 10
switch(config-lag-if)# qos trust none
switch(config-lag-if)# end
switch# show running-config
Current configuration:
!
QoS Trust dscp
!
!
interface 1
    QoS Trust cos
interface lag 10
    QoS Trust none
```

### Show Running Config Interface

#### Syntax
`show running-config interface <interface>`

#### Description
This command displays the QoS settings that have been configured for an interface.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *interface* | Required | System defined | Name of the interface. |

#### Examples
```
switch# configure terminal
switch(config)# interface 1
switch(config-if)# qos trust dscp
switch(config-if)# end
switch# show running-config interface 1
interface 1
    QoS Trust dscp
   exit
```

### Show Interface

#### Syntax
`show interface <interface>`

#### Description
This command displays the QoS settings that have been configured for an interface.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *interface* | Required | System defined | Name of the interface. |

#### Examples
```
switch# configure terminal
switch(config)# interface 1
switch(config-if)# qos trust dscp
switch(config-if)# end
switch# show interface 1

Interface 1 is down (Administratively down)
 Admin state is down
 State information: admin_down
 Hardware: Ethernet, MAC Address: 70:72:cf:fc:51:de
 MTU 0
 Half-duplex
 QoS Trust dscp
 Speed 0 Mb/s
 Auto-Negotiation is turned on
 Input flow-control is off, output flow-control is off
 RX
            0 input packets              0 bytes
            0 input error                0 dropped
            0 CRC/FCS
 TX
            0 output packets             0 bytes
            0 input error                0 dropped
            0 collision

```

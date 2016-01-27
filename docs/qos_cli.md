QoS Commands
======

## Contents
- [Global Configuration Commands](#configuration-commands)
  - [qos cos-map](#qos-cos-map)
  - [qos dscp-map](#qos-dscp-map)
  - [qos trust](#qos-trust)
- [Display Commands](#display-commands)
  - [show qos cos-map](#show-qos-cos-map)
  - [show qos dscp-map](#show-qos-dscp-map)
  - [show qos trust](#show-qos-trust)
  - [show running config](#show-running-config)
  - [show running config interface](#show-running-config-interface)
  - [show interface](#show-interface)

## QOS Global Configuration Commands

These commands are entered in the global configuration context.

### qos cos-map

#### Syntax
`qos cos-map <0-7> local-priority <NUM> [color <COLOR>] [name <DESCRIPTION>]`
`no qos cos-map <0-7>`

#### Description
The global cos-map associates local-priority, color, and name to each 802.1 VLAN Priority Code Point (COS).  This command configures the local-priority and color assignment to each code point.

This table is used for ports whose qos trust mode is set to 'cos' to assign the packets initial local-priority and color.

The default color is 'green'.  The default name is an empty string.

The 'no' form of the command will restore the assignments for a Priority Code Point back to its factory default.

#### Authority
All users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *COS* |  802.1 VLAN Priority Code Point from 0 to 7
| *NUM* |  ASIC-specific local priority value
| *COLOR* | One of the following tokens: 'green', 'yellow', or 'red'
| *DESCRIPTION* | Contains up to 64 characters for customer documentation. Must be surrounded with double-quotes if spaces are used.

#### Examples
```
switch# configure terminal
switch(config)# qos cos-map 1 local-priority 2 color green name EntryName
```

### qos dscp-map

#### Syntax
`qos dscp-map <0-63> local-priority <NUM> [cos <0-7>] [color <COLOR>] [name <DESCRIPTION>]`
`no qos dscp-map <0-63>`

#### Description
The global cos-map associates local-priority, color, and name to each IP Differentiated Services Code Point (DSCP).  This command configures the local-priority, color, and cos assignment to each code point.

This table is used for ports whose qos trust mode is set to 'dscp' to assign the packets initial local-priority, color, and optionally cos.

The default color is 'green'.  The default name is an empty string.  The default cos is 'no-override'.

The 'no' form of the command will restore the assignments for a code point back to its factory default.

#### Authority
All users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *DSCP* | IP Differentiated Services Code Point from 0 to 63
| *NUM* |  ASIC-specific local priority value from 0 to 7
| *COS* |  802.1 VLAN Priority Code Point
| *COLOR* | One of the following tokens: 'green', 'yellow', or 'red'
| *DESCRIPTION* | Contains up to 64 characters for customer documentation.  Must be surrounded with double-quotes if spaces are used.
#### Examples
```
switch# configure terminal
switch(config)# qos dscp-map 1 local-priority 2 cos 3 color green name EntryName
```

### qos trust

#### Syntax
To configure globally:
`[no] qos trust {none|cos|dscp}`

To configure per port:
`interface ### $ [no] qos trust {none|cos|dscp}`

#### Description
The Trust command configures one of three modes that be applied globally or overridden per port.

The 'no' form of the command in the interface context will set the port's mode to match the global trust mode.  The 'no' form of the command in the global context will restore the trust mode back to the factory default.

#### Authority
All users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| none | Ignores all packet headers. The packet is initially assigned local_priority of zero and color of green.
| cos | For 802.1 VLAN tagged packets, use the priority code point field of the outermost VLAN header, if any, as the index into the COS Map. If the packet is untagged, use the meta-data values at index zero of the COS Map.
| dscp | For IP packets, use the DSCP field as the index into the DSCP Map. For non-IP packets with 802.1 VLAN tag(s), use the priority code point field of the outermost tag header as the index into the DSCP Map.  For untagged, non-IP packets, assign use the meta-data values at index zero of the DSCP Map.

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

### show qos cos-map

#### Syntax
`show qos cos-map [default]`

#### Description
This command displays the QoS cos-map.

#### Authority
All users.

#### Parameters
The optional 'default' parameter will display the factory default values.

#### Examples
```
switch# show qos cos-map default
code_point local_priority color   name
---------- -------------- ------- ----
0          1              green   "Best Effort"
1          0              green   "Background"
2          2              green   "Excellent Effort"
3          3              green   "Critical Applications"
4          4              green   "Video"
5          5              green   "Voice"
6          6              green   "Internetwork Control"
7          7              green   "Network Control"
```

### show qos dscp-map

#### Syntax
`show qos dscp-map [default]`

#### Description
This command displays the QoS dscp-map.

#### Authority
All users.

#### Parameters
The optional 'default' parameter will display the factory default values.

#### Examples
```
switch# show qos dscp-map default
code_point local_priority cos color   name
---------- -------------- --- ------- ----
0          0              1   green   "CS0"
1          0              1   green
2          0              1   green
3          0              1   green
4          0              1   green
5          0              1   green
6          0              1   green
7          0              1   green
8          1              0   green   "CS1"
9          1              0   green
10         1              0   green   "AF11"
11         1              0   green
12         1              0   yellow  "AF12"
13         1              0   green
14         1              0   red     "AF13"
15         1              0   green
16         2              2   green   "CS2"
17         2              2   green
18         2              2   green   "AF21"
19         2              2   green
20         2              2   yellow  "AF22"
21         2              2   green
22         2              2   red     "AF23"
23         2              2   green
24         3              3   green   "CS3"
25         3              3   green
26         3              3   green   "AF31"
27         3              3   green
28         3              3   yellow  "AF32"
29         3              3   green
30         3              3   red     "AF33"
31         3              3   green
32         4              4   green   "CS4"
33         4              4   green
34         4              4   green   "AF41"
35         4              4   green
36         4              4   yellow  "AF42"
37         4              4   green
38         4              4   red     "AF43"
39         4              4   green
40         5              5   green   "CS5"
41         5              5   green
42         5              5   green
43         5              5   green
44         5              5   green
45         5              5   green
46         5              5   green   "EF"
47         5              5   green
48         6              6   green   "CS6"
49         6              6   green
50         6              6   green
51         6              6   green
52         6              6   green
53         6              6   green
54         6              6   green
55         6              6   green
56         7              7   green   "CS7"
57         7              7   green
58         7              7   green
59         7              7   green
60         7              7   green
61         7              7   green
62         7              7   green
63         7              7   green
```

### show qos trust

#### Syntax
`show qos trust [default]`

#### Description
This command displays the global QoS trust setting.

#### Authority
All users.

#### Parameters
The optional 'default' parameter will display the factory default value.

#### Examples
```
switch# show qos trust default
qos trust none
```

### show running config

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
qos trust dscp
!
!
interface 1
    qos trust cos
interface lag 10
    qos trust none
```

### show running config interface

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
    qos trust dscp
   exit
```

### show interface

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

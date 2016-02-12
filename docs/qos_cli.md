Quality Of Service Commands
===========================

## Contents
- [Definition of Terms](#Definition-of-Terms)
- [QoS Global Configuration Commands](#qos-global-configuration-commands)
  - [apply qos](#apply-qos)
  - [qos cos-map](#qos-cos-map)
  - [qos dscp-map](#qos-dscp-map)
  - [qos queue-profile](#qos-queue-profile)
  - [qos schedule-profile](#qos-schedule-profile)
  - [qos trust](#qos-trust)
- [QoS Interface Configuration Commands](#qos-interface-configuration-commands)
  - [apply qos](#interface-apply-qos)
  - [qos cos](#interface-qos-cos)
  - [qos dscp](#interface-qos-dscp)
  - [qos trust](#interface-qos-trust)
- [QoS Queue Profile Configuration Commands](#qos-queue-profile-configuration-commands)
  - [name](#name)
  - [map](#map)
- [QoS Schedule Profile Configuration Commands](#qos-schedule-profile-configuration-commands)
  - [strict](#strict)
  - [wrr](#wrr)
- [QoS Show Commands](#display-commands)
  - [show interface](#show-interface)
  - [show interface queues](#show-interface-queues)
  - [show qos cos-map](#show-qos-cos-map)
  - [show qos dscp-map](#show-qos-dscp-map)
  - [show qos queue-profile](#show-qos-queue-profile)
  - [show qos schedule-profile](#show-qos-schedule-profile)
  - [show qos trust](#show-qos-trust)
  - [show running config](#show-running-config)
  - [show running config interface](#show-running-config-interface)



## Definition of Terms
| Term | Description |
|:-----------|:---------------------------------------|
| **class** | <ol><li>General term for things sharing some common characteristic (e.g. all students of the same grade).</li><li>For networking, a set of packets sharing some common characteristic (e.g all IPv4 packets)</li><ol> |
| **code<br>point**| Used in two different ways - either as a name of a packet header field or as a name of the values carried within a packet header field:<ul><li>Priority Code Point (PCP) is the name of a field in the [IEEE 802.1Q](http://www.ieee802.org/1/pages/802.1Q.html) VLAN tag</li><li> Differentiated Services Code Point (DSCP) is the name of values carried within a IP header field.
| **color** | A meta-data label associated with each packet within the switch with three values: "green", "yellow", or "red".  It is used by the switch when packets encounter congestion for resource (queue) to distinguish which packets should be more likely be dropped.  |
| **CoS** | Class of Service<ol><li>General term when there are different levels of treatment (e.g. fare class).</li><li>For Ethernet, a 3-bit value used to mark packets with one of 8 classes (levels of priority).  It is carried within the Priority Code Point (PCP) field of the [IEEE 802.1Q](http://www.ieee802.org/1/pages/802.1Q.html) VLAN tag.</li></ol> |
| **DSCP** | Differentiated Services Code Point<p>A 6-bit value used to mark packets for different Per Hop Behavior as originally defined by [IETF RFC 2474](https://tools.ietf.org/html/rfc2474). It is carried within a portion of the IPv4 ToS or IPv6 TC header field.
| **local-<br>priority** | A meta-data label associated with a packet within a network switch.  It is used by the  switch to distinguish packets for different treatment (e.g. queue assignment, etc).   |
| **meta-<br>data** | Information labels associated with each packet in the switch separate from the packet headers and data.  These labels are used by the switch in its handling of the packet.  Examples are: arrival port, egress port, vlan membership, local priority, color, etc. |
| **PCP** |  Priority Code Point<p> The name of a 3-bit  field in the [IEEE 802.1Q](http://www.ieee802.org/1/pages/802.1Q.html) VLAN tag.  It carries the CoS value to mark a packet with one of 8 classes (priority levels). |
| **QoS** | Quality of Service<ol><li>General term used when describing or measuring performance.</li><li>For networking, it means how different classes of packets are treated across the network or device.<br>(see [https://en.wikipedia.org/wiki/Quality_of_service](https://en.wikipedia.org/wiki/Quality_of_service))</li></ol> |
| **TC** | Traffic Class<ol><li>A set of packets sharing some common characteristic.</li><li>An 8-bit field in the IPv6 header as originally defined by [IETF RFC 2460](https://tools.ietf.org/html/rfc2460#section-7).  Its usage has been superseded by [IETF RFC 2474](https://tools.ietf.org/html/rfc2474) to carry DSCP values.</li><ol> |
| **ToS** | Type of Service<ol><li>General term when there are different levels of treatment (e.g. fare class).</li><li>A 8-bit field in the IPv4 header as originally defined by [IETF RFC 791](https://tools.ietf.org/html/rfc791#section-3.1) that carried Delay, Precedence, Reliability, and Throughput values. Its usage has been superseded by [IETF RFC 2474](https://tools.ietf.org/html/rfc2474) to carry DSCP values.</li></ol> |



## QOS Global Configuration Commands

These commands are entered in the global configuration context.

## apply qos

#### Syntax

`apply qos queue-profile <NAME> schedule-profile {<NAME> | strict}`

#### Description
The **apply qos** command in the global configuration context will configure the given queue profile and schedule profile at the global level.  Global profiles are configured on all Ethernet interfaces and LAGGs that have not applied their own profiles.``

**This may cause the interface(s) or LAGG(s) to shutdown briefly during the reconfiguration.**

For a queue profile to be complete and ready to be applied, all local priorities must be mapped to some queue.

For the schedule profile to be complete and ready to be applied, it must have configuration for each queue defined by the queue profile. All queues must use the same algorithm except for the highest numbered queue which may be 'strict'.

There is a special, pre-defined schedule-profile named 'strict'.  It is always present and unalterable.  This 'strict' profile will service all queues of an associated queue profile using the Strict Priority algorithm.

The queue profile and the schedule profile must both specify the same number of queues.

An applied profile cannot be updated or deleted until such time that no longer applied.

The **no apply qos** command is disallowed in the global configuration context.  It is required to always have a global and schedule profile applied.  To cease the use of a profile, apply a different profile.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* | The name of the profile to apply
| *strict* | Use the strict schedule profile

#### Examples
```
switch# configure terminal
switch(config)# apply qos queue-profile default schedule-profile strict
```


## qos cos-map

#### Syntax
`qos cos-map <0-7> local-priority <NUM> [color <COLOR>] [name <DESCRIPTION>]`
`no qos cos-map <0-7>`

#### Description
The **cos-map** command associates local-priority, color, and optionally a descriptive name to each 802.1 VLAN Priority Code Point (COS).

This table is used when ports  QoS trust mode is set to 'cos' to mark packets initial local-priority and color (see [qos trust](#qos-trust)).

The default color is 'green'.  The default name is an empty string.

The **no cos-map** command will restore the assignments for a Priority Code Point back to its factory default.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *COS* |  802.1 VLAN Priority Code Point from 0 to 7
| *NUM* |  Switch-specific local priority value
| *COLOR* | One of the following tokens: 'green', 'yellow', or 'red'
| *DESCRIPTION* | Contains up to 64 characters for customer documentation. Must be surrounded with double-quotes if spaces are used.

#### Examples
```
switch# configure terminal
switch(config)# qos cos-map 1 local-priority 2 color green name EntryName
```

## qos dscp-map

#### Syntax
`qos dscp-map <0-63> local-priority <NUM> [cos <0-7>] [color <COLOR>] [name <DESCRIPTION>]`
`no qos dscp-map <0-63>`

#### Description
The **cos-map** command associates local-priority, color, and optionally a descriptive name to each IP Differentiated Services Code Point (DSCP).  This command can optionally remark the incoming 802.1 VLAN COS (Priority Code Point).

This table is used when ports  QoS trust mode is set to 'cos' to assign the packets initial local-priority color, and optionally COS (see [qos trust](#qos-trust)).

The default color is 'green'.  The default name is an empty string.  The default cos is 'no-override'.

The 'no' form of the command will restore the assignments for a code point back to its factory default.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *DSCP* | IP Differentiated Services Code Point from 0 to 63
| *NUM* |  ASIC-specific local priority value from 0 to 7
| *COS* |  Remark the 802.1 VLAN Priority Code Point field with this value
| *COLOR* | One of the following tokens: 'green', 'yellow', or 'red'
| *DESCRIPTION* | Contains up to 64 characters for customer documentation.  Must be surrounded with double-quotes if spaces are used. |
#### Examples
```
switch# configure terminal
switch(config)# qos dscp-map 1 local-priority 2 cos 3 color green name EntryName
```


## qos queue-profile

#### Syntax
`qos queue-profile <NAME>`
`no qos queue-profile <NAME>`

#### Description
The queue-profile command is used to enter the queue-profile configuration context to create, or edit, a named queue profile.

The no form of the command will delete the named queue profile, if it is not currently applied.

##### Default Profile

There is a special, pre-defined profile named 'default'.  At installation an factory supplied default queue-profile is automatically applied. The 'default' profile is editable as long as it is not applied.

**show qos queue-profile default** will display current contents of the profile.

The profile named 'default' cannot be deleted. **no queue-profile default** will reset it back to the factory supplied profile.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* |  Up to 64 character name for the profile<ul><li>ASCII letters, upper or lower case<li>numbers<li>underscores</ul>

#### Examples
```
switch# configure terminal
switch(config)# qos queue-profile Profile_Name_v1
```


## qos schedule-profile

#### Syntax
`qos schedule-profile <NAME>`
`no qos schedule-profile <NAME>`

#### Description
The schedule-profile command is used to enter the schedule-profile configuration context to create, or edit, a named schedule profile.

The no form of the command will delete the named schedule profile, if it is not currently applied.

##### Default Schedule Profile

There is a special, pre-defined profile named 'default'.  At installation an factory supplied default schedule-profile is automatically applied. The 'default' profile is editable as long as it is not applied.

**show qos schedule-profile default** will display current contents of the profile.

The profile named 'default' cannot be deleted. **no schedule-profile default** will reset it back to the factory supplied profile.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* |  Up to 64 character name for the profile<ul><li>ASCII letters, upper or lower case<li>numbers<li>underscores</ul>

#### Examples
```
switch# configure terminal
switch(config)# qos schedule-profile Profile_Name_v2
```


## qos trust

#### Syntax
`qos trust {none|cos|dscp}`
`no qos trust`

#### Description
The Trust command configures one of three modes that be applied globally on all Ethernet interfaces and LAGGs.

**no qos trust** will restore the trust mode back to the factory default.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| none | Ignores all packet headers. The packet is initially assigned local_priority of zero and color of green.
| cos | For 802.1 VLAN tagged packets, use the priority code point field of the outermost VLAN header, if any, as the index into the COS Map. If the packet is untagged, use the meta-data values at index zero of the COS Map.
| dscp | For IP packets, use the DSCP field as the index into the DSCP Map. For non-IP packets with 802.1 VLAN tag(s), use the priority code point field of the outermost tag header as the index into the DSCP Map.  For untagged, non-IP packets, assign use the meta-data values at index zero of the DSCP Map.

#### Examples
```
switch# configure terminal
switch(config)# qos trust dscp
```



## QoS Interface Configuration Commands

These commands are entered in the interface configuration context.

## interface apply qos

#### Syntax

`(config-if)# apply qos schedule-profile {<NAME> | strict}`
`(config-if)# no apply qos schedule-profile`

#### Description
The **apply qos** command in the Ethernet or LAGG interface configuration context will configure the given schedule profile just for that interface.  It will override any schedule-profile applied in the global context.

**This may cause the interface (or LAGG) to shutdown briefly during the reconfiguration.**

**NOTE:**  It is allowed to apply the same name as currently applied schedule-profile in the global context.  This guarantees the interface will always use this schedule-profile even when the global context schedule-profile subsequently changes.

For the schedule profile to be complete and ready to be applied, it must have configuration for each queue defined by the queue profile.  All queues must use the same algorithm (e.g. WRR) except for the highest numbered queue which may be 'strict'.

An applied profile cannot be updated or deleted until such time that is no longer applied.

##### Strict Schedule Profile
There is a special, pre-defined profile named 'strict'.  It is always present and unalterable.  The strict  profile will service all queues of an associated queue profile using Strict Priority scheduling.

The **no apply qos schedule-profile** command will clear a schedule profile override for a given interface and the interface will use the global schedule profile.  This is the only way to remove a schedule-profile override from the interface.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* | The name of the profile to apply
| *strict* | Use the strict schedule profile

#### Examples
```
switch# configure terminal
switch(config)# interface 1
switch(config-if)# apply qos schedule-profile strict
```


## interface qos cos

#### Syntax

`(config-if)# qos cos <0-7>`
`(config-if)# $ no qos cos`

#### Description
The **qos cos** command in the Ethernet or LAGG interface configuration context will configure a COS override override just for that interface.  It is only allowed if the interface trust mode is 'none'.

All packets arriving on the Ethernet or LAGG interface will:
- Have their local-priority and color meta-data assigned from the CoS map entry indexed by the parameter.
- Packet COS will be remarked with the parameter's value.
	- If the packet is subsequently transmitted with a VLAN tag, the PCP field will contain the parameter's value.

The **no qos cos** command will clear the COS override for the interface.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *<0-7>* | Index into the COS Map

#### Examples
```
switch# configure terminal
switch(config)# qos trust dscp
switch(config)# interface 1
switch(config-if)# qos trust none
switch(config-if)# qos cos 0
```


## interface qos dscp

#### Syntax

`(config-if)# qos dscp <0-63>`
`(config-if)# $ no qos dscp`

#### Description
The **qos dscp** command in the Ethernet or LAGG interface configuration context will configure a COS override override just for that interface.  It is only allowed if the interface trust mode is **none**.

For all arriving IPv4 or IPv6 packets:
- Initial local-priority and color meta-data are assigned from the DSCP Map entry indexed by the parameter.
- Remark the DSCP value in IPv4 ToS and IPv6 TC header fields with the parameter's value
- If the DSCP Map entry specifies a COS override, the packet's CoS will be remarked with that value
	- If the packet is subsequently transmitted with a 802.1Q VLAN tag, the PCP field will contain that value
	- If the DSCP Map entry does not specify a COS override, the packet's CoS is unchanged unless there also is a COS override configured

For all arriving non-IP packets and a COS override is also configured on the same interface or LAGG:
- Initial local-priority and color meta-data are assigned from the CoS Map entry indexed by CoS override parameter.
- Packet COS will be remarked with the COS override's parameter value.
	- If the packet is subsequently transmitted with a 802.1Q VLAN tag, the PCP field will contain the CoS override parameter's value.

Otherwise all arrving non-IP packets CoS are unchanged and the initial local-priority and color meta-data are assigned from the CoS Map entry index 0.

The **no qos dscp** command will clear the DSCP override for the interface.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *<0-63>* | Index into the DSCP Map

#### Examples
```
switch# configure terminal
switch(config)# qos trust cos
switch(config)# interface 1
switch(config-if)# qos trust none
switch(config-if)# qos dscp 0
```


## interface qos trust

#### Syntax

`(config-if)# qos trust {none|cos|dscp}`
`(config-if)# $ no qos trust`

#### Description
The **qos trust** command in the Ethernet or LAGG interface configuration context will configure a trust mode override just for that interface.  It will override the trust mode applied in the global context.

The **no qos trust** command will clear the trust mode override for a given interface and the interface will use the global schedule profile.  This is the only way to remove a trust mode override from the interface.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| none | Ignores all packet headers. The packet is initially assigned local_priority of zero and color of green.
| cos | For 802.1 VLAN tagged packets, use the priority code point field of the outermost VLAN header, if any, as the index into the COS Map. If the packet is untagged, use the meta-data values at index zero of the COS Map.
| dscp | For IP packets, use the DSCP field as the index into the DSCP Map. For non-IP packets with 802.1 VLAN tag(s), use the priority code point field of the outermost tag header as the index into the COS Map.  For untagged, non-IP packets, assign use the meta-data values at index zero of the DSCP Map.

#### Examples
```
switch# configure terminal
switch(config)# interface 1
switch(config-if)# qos trust dscp
```

## QOS Queue Profile Configuration Commands

To enter the Queue Profile context, enter the [qos queue-profile](#qos-queue-profile) command.   The following commands are available in Queue Profile context:
- name
- map

##### Queue Numbering

Queues are numbered consecutively starting from zero.  Queue zero is the lowest priority queue.  The larger the queue number the higher priority the queue has in scheduling algorithms (see [QOS Schedule Profile Configuration Commands](#qos-schedule-profile-configuration-commands)).  The maximum allowed queue number may vary by  product.  For products supporting 8 queues, the largest queue number is 7. Please refer to the product specifications for the maximum.

##### Default Profile

There is a special, pre-defined profile named 'default'.  At installation an factory supplied default queue-profile is automatically applied. The 'default' profile is editable as long as it is not applied.


## name

#### Syntax
`name queue <0-7> <DESCRIPTION>`
`no name queue <0-7>`

#### Description
The **name** command assigns a descriptive string to a queue number in a queue profile.  It has no affect on the product configuration.

The descriptive string is limited to 64 characters.  If there are spaces, the name string must be surrounded by double quotes.

The **no name** command will delete the name of a queue number in a queue profile.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *QUEUE* |  The queue number from 0 to 7
| *DESCRIPTION* |  The  string to assign to the queue number

#### Examples
```
switch# configure terminal
switch(config)# qos queue-profile Profile_Name
switch(config-queue)# name queue 0 "Scavenger and backup data"
```

## map

#### Syntax
`map queue <0-7> local-priority <0-7>`
`no map queue <0-7> [local-priority <0-7>]`

#### Description
The **map** command assigns a local priority to a queue number in a queue profile. Packets marked with that local-priority will use the queue.

More than one local-priority can be assigned to use the same queue. A queue without any local-priorities assigned will not be used to store packets.

For a queue profile to be suitable to be applied (see [apply qos](#apply-qos)), all local-priorities must be assigned to some queue in the profile.

The **no map** command will remove the assignment of the local priority from the queue number. If no local priority is provided, then the assignment of all local priorities will be removed from the queue.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *QUEUE* |  The queue number from 0 to 7
| *LOCAL_PRIORITY* |  The local priority to add or remove from the queue number

#### Examples
```
switch# configure terminal
switch(config)# qos queue-profile ProfileName
switch(config-queue)# map queue 0 local-priority 1
```

## QOS Schedule Profile Configuration Commands

To enter the Schedule Profile context, enter the [qos schedule-profile](#qos-schedule-profile) command. The following commands are available in Queue Profile context:
- strict
- wrr (weighted round robin)

##### Queue Numbering

Queues in a schedule profile are numbered consecutively starting from zero.  Queue zero is the lowest priority queue.  The larger the queue number the higher priority the queue has in scheduling algorithms.  The maximum allowed queue number may vary by  product.  For products supporting 8 queues, the largest queue number is 7. Please refer to the product specifications for the maximum.

##### Allowed Forms

There are two allowed forms for schedule profiles:
1. All queues use the same scheduling algorithm (e.g. wrr)
2. The highest queue number uses Strict Priority and all remaining (lower) queues use the same algorithm (e.g. wrr).

The second form supports priority scheduling behavior necessary for the [IEFT RFC 3246 Expedited Forwarding](https://tools.ietf.org/html/rfc3246) specification.

##### Default Schedule Profile

There is a special, pre-defined profile named 'default'.  At installation an factory supplied default schedule-profile is automatically applied. The 'default' profile is editable as long as it is not applied.

##### Strict Schedule Profile
There is a special, pre-defined profile named 'strict'.  It is always present and unalterable.  The strict profile will service all queues of an associated queue profile using the Strict Priority algorithm.


## strict

#### Syntax
`strict queue <0-7>`
`no strict queue <0-7>`

#### Description
The **strict** command assigns the Strict Priority algorithm to a queue.  Strict Priority will service all packets awaiting in a queue before any packets in lower priority queues are serviced.

The **no strict** command will only clear the algorithm for a queue when the algorithm already assigned is Strict Priority.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *QUEUE* |  The queue number from 0 to 7

#### Examples
```
switch# configure terminal
switch(config)# qos schedule-profile Profile_1p7q
switch(config-schedule)# strict queue 7
```

## wrr

#### Syntax
`wrr queue <0-7> weight <0-127>`
`no wrr queue <0-7>`

#### Description
The **wrr** command assigns (Deficit) Weighted Round Robin algorithm and its byte weight to a queue.

(Deficit) Weight Round Robin will apportion available bandwidth among all (non-empty) queues in relation to their queue weights.  A product will either support Deficit Weighted Round Robin or Weighted Round Robin but not both.  Please refer to the specifications for the product.

The **no wrr** command will only clear the algorithm for a queue when the algorithm already  assigned is (Deficit) Weighted Round Robin.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *QUEUE* |  The queue number from 0 to 7
| *WEIGHT* |  The weight to use for the wrr scheduling

#### Examples
```
switch# configure terminal
switch(config)# qos schedule-profile ProfileName
switch(config-schedule)# wrr queue 0 weight 11
switch(config-schedule)# wrr queue 1 weight 17
```


## Display Commands
The following commands show configuration and status information.


## show interface

#### Syntax
`show interface <INTERFACE>`

#### Description
This command's display includes the QoS settings that have been configured for an interface.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *INTERFACE* | Required | System defined | Name of the interface. |

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


## show interface

#### Syntax
`show interface <INTERFACE> queues`

#### Description
This command will display statistics from each queue for an interface:
- Number of packets transmitted
- Number of bytes transmitted
- Number of packets that were not transmmited due to an error (i.e. queue full)

Queues are numbered consecutively starting from zero.  Queue zero is the lowest priority queue.  The larger the queue number the higher priority the queue has in scheduling algorithms.  The maximum allowed queue number may vary by  product.  For products supporting 8 queues, the largest queue number is 7. Please refer to the product specifications for the maximum.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *INTERFACE* | Required | System defined | Name of the interface. |

#### Examples
```

switch# show interface 1

Interface 1 is  (Administratively down)
 Admin state is down
 State information: admin_down
         Tx Packets             Tx Bytes  Tx Packet Errors
 Q0             100                 8000                 0
 Q1         1234567          12345678908                 5
 Q2              0                     0                 0
 Q3              0                     0                 0
 Q4              0                     0                 0
 Q5              0                     0                 0
 Q6              0                     0                 0
 Q7              0                     0                 0
```



## show qos cos-map

#### Syntax
`show qos cos-map [default]`

#### Description
This command displays the QoS cos-map.

#### Authority
All configuration users.

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

## show qos dscp-map

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


## show qos queue-profile

#### Syntax
`show qos queue-profile [{<NAME> | factory-default}]`

#### Description
When no parameter is provided, then a sorted list of defined profile names and their status will be shown.

When a name is given, this command will display the details of the specified profile.  The name 'default' can be used to display the current details of that profile.

When 'factory-default' parameter is used in place of a name, then the factory supplied profile will be displayed.

#### Authority
All users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* |  The name of the profile to show
| *factory-default* |  Show the factory default profile

#### Examples
```
switch# show qos queue-profile factory-default
queue_num local_priorities name
--------- ---------------- ----
0         0                Scavenger and backup data
1         1
2         2
3         3
4         4
5         5
6         6
7         7
```

## show qos schedule-profile

#### Syntax
`show qos schedule-profile [{<NAME> | factory-default}]`

#### Description
When no parameter is provided, then a sorted list of defined profile names and their status will be shown.

When a name is given, this command will display the details of the specified profile.  The name 'default' can be used to display the current details of that profile.

When 'factory-default' parameter is used in place of a name, then the factory supplied profile will be displayed.

#### Authority
All users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* |  The name of the profile to show
| *factory-default* |  Show the factory default profile

#### Examples
```
switch# show qos schedule-profile factory-default
queue_num algorithm weight
--------- --------- ------
0         wrr       1
1         wrr       2
2         wrr       3
3         wrr       4
4         wrr       5
5         wrr       6
6         wrr       7
7         strict
```

## show qos trust

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


## show running config

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

## show running config interface

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

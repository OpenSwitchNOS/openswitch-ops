QoS User Guide
======

## Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Configuring QoS Trust](#configuring-qos-trust)
    - [local-priority](#local-priority)
    - [color](#color)
    - [qos cos-map](#qos-cos-map)
    - [qos dscp-map](#qos-dscp-map)
    - [qos trust](#qos-trust)
        - [none](#none)
        - [cos](#cos)
        - [dscp](#dscp)
    - [Verifying the configuration](#verifying-the-configuration)
- [CLI](#cli)

## Overview
Global Quality of Service (QoS) provides the capability for networked devices to assign traffic priority based on configured packet attributes.

The QoS Trust feature restricts which packet QoS information may be used to determine inbound queue servicing and any priority information to be permitted into the local hop. It is typically used at the network edge (or anywhere that connects to end-nodes or other potentially untrusted sources).

## Prerequisites
None.

## Configuring QoS Trust
ASICs can be configured to inspect the VLAN tag or IP header of newly arrived packets to generate the initial values of the QoS meta-data: local-priority and color. These two QoS meta-data values are used by ASICs to differentiate packets' handling and buffering. Later stages of processing may over-write (remark) these meta-data.

### local-priority
The local-priority is generally one of 8 levels (0-7), although industry practice uses a 64-level encoding. Zero is the lowest. The allowed maximum will vary per ASIC family.

### color
The color is one of three values (0-2), commonly named green (0), yellow (1), and red (2). These are mostly used with packets marked with Assured Forwarding code points.

Several configuration commands being considered are:

### qos cos-map
The global cos-map uses the value from the packet header as an index into the cos-map to retrieve the local-class and color assignment.

`qos cos-map COS local-priority NUM [color COLOR] [name STRING]`

where:
COS is the 802.1 VLAN Priority Code Point
NUM is the ASIC-specific local priority value
COLOR is one of the following tokens: 'green', 'yellow', or 'red'
STRING contains up to 64 characters for customer documentation

There is not a 'no' form of this command, since there must exist an entry for every code point. At boot, there will be entries for all code points by default.

### qos dscp-map
The global dscp-map uses the value from the packet header as an index into the dscp-map to retrieve the local-class and color assignment.

`qos dscp-map DSCP local-priority NUM [cos COS] [color COLOR] [name STRING]`

where:
DSCP is the IP Differentiated Services Code Point
NUM is the ASIC-specific local priority value
COS is the 802.1 VLAN Priority Code Point
COLOR is one of the following tokens: 'green', 'yellow', or 'red'
STRING contains up to 64 characters for customer documentation

There is not a 'no' form of this command, since there must exist an entry for every code point. At boot, there will be entries for all code points by default.

### qos trust
The Trust command configures one of three modes that be applied globally or overridden per port:

To configure globally:
`$ qos trust {none|cos|dscp}`

To configure per port:
`interface ### $ [no] qos trust {none|cos|dscp}`

where:

#### none
Ignores all packet headers. The packet is initially assigned local_priority of zero and color of green.

#### cos
For 802.1 VLAN tagged packets, use the priority code point field of the outermost VLAN header, if any, as the index into the COS Map. If the packet is untagged, use the meta-data values at index zero of the COS Map.

#### dscp
For IP packets, use the DSCP field as the index into the DSCP Map. For non-IP packets with VLAN tag(s), use the priority code point field of the outermost tag header as the index into the COS Map.  For untagged non-IP packets, assign use the meta-data values at index zero of the COS Map.

There is not a 'no' form of the trust command in the global context, since there always has to be a global default. The 'no' form within the interface context will remove a port override and configure the port to match the default trust mode.

### Verifying the configuration
The `show running-config` command displays the current QoS configuration.
```
switch# show running-config
Current configuration:
!
!
!
interface 1
    QoS Trust dscp
```

## CLI
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here](/documents/user/qos_cli) for the CLI commands related to the QoS feature.

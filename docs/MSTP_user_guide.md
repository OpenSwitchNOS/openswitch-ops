# MSTP feature
## Contents
- [Overview](#overview)
- [MSTP Structure](#mstp-structure)
    - [Common and Internal Spanning Tree(CIST)](#cist)
    - [Common Spanning Tree (CST)](#cst)
    - [MST Region](#mst)
    - [Internal Spanning Tree (IST)](#ist)
    - [Types of Multiple Spanning Tree Instances](#types-of-multiple-spanning-tree-instances)
        - [Internal Spanning-Tree Instance (IST Instance)](#ist-instance)
        - [MSTI (Multiple Spanning Tree Instance)](#mst-instance)
- [How MSTP Operates](#how-mstp-operates)
- [Terminology](#terminology)
    - [Common and Internal Spanning Tree (CIST)](#t_cist)
    - [Internal Spanning Tree (IST)](#t_ist)
    - [MSTP (Multiple Spanning Tree Protocol)](#t_mstp)
    - [MSTP BPDU(Bridge Protocol Data Unit)](#t_bpdu)
    - [MSTP Bridge](#t_bridge)
    - [MSTP Region](#t_region)
- [Operating Rules](#operating-rules)
- [How to use the feature](#how-to-use-the-feature)
    - [Scenario 1](#scenario-1)
        - [Setting up scenario 1 basic configuration](#setting-up-scenario-1-basic-configuration)
            - [Physical Topology](#physical-topology)
            - [Logical Topology](#logical-topology)
        - [Configure MSTP global parameters](#configure-mstp-global-parameters)
        - [Configure MSTP optional parameters](#configure-mstp-optional-parameters)
        - [Verifying scenario 1 configuration](#verifying-scenario-1-configuration)
        - [Troubleshooting scenario 1 configuration](#troubleshooting-scenario-1-configuration)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
The MSTP feature is used for preventing loops in network.
Without spanning tree, having more than one active path between a pair of nodes causes loops in the network, which can result in duplication of messages, leading to a “broadcast storm” that can bring down the network.

- Multiple-Instance spanning tree operation (802.1s) ensures that only one active path exists between any two nodes in a spanning-tree instance.
- spanning-tree instance comprises a unique set of VLANs, and belongs to a specific spanning-tree region.
- A region can comprise multiple spanning-tree instances (each with a different set of VLANs), and allows one active path among regions in a network.
- Applying VLAN tagging to the ports in a multipleinstance spanning-tree network enables blocking of redundant links in one instance while allowing forwarding over the same links for non-redundant use by another instance.

This feature currently works on physical interface and lags.

## MSTP Structure
MSTP maps active, separate paths through separate spanning tree instances and between MST regions. Each MST region comprises one or more MSTP switches.

<div id='cist'/>
- ####Common and Internal Spanning Tree(CIST):
The CIST identifies the regions in a network and administers the CIST root bridge for the network, the root bridge for each region, and the root bridge for each spanning-tree instance in each region.

<div id='cst'/>
- ####Common Spanning Tree (CST):
The CST administers the connectivity among the MST regions in a bridged network.

<div id='mst'/>
- ####MST Region:
An MST region comprises the VLANs configured on physically connected MSTP switches. All switches in a given region must be configured with the same VLANs and Multiple Spanning Tree Instances (MSTIs).

<div id='ist'/>
- ####Internal Spanning Tree (IST):
The IST administers the topology within a given MST region. When you configure a switch for MSTP operation, the switch automatically includes all of the static VLANs configured on the switch in a single, active spanning tree topology (instance) within the IST. This is termed the “IST instance”. Any VLANs you subsequently configure on the switch are added to this IST instance. To create separate forwarding paths within a region, group specific VLANs into different Multiple Spanning Tree Instances (MSTIs).

- ####Types of Multiple Spanning Tree Instances
A multiple spanning tree network comprises separate spanning-tree instances existing in an MST region. (There can be multiple regions in a network.) Each instance defines a single forwarding topology for an exclusive set of VLANs.
<div id='ist-instance'/>
    - ####Internal Spanning-Tree Instance (IST Instance):
        This is the default spanning tree instance in any MST region. It provides the root switch for the region and comprises all VLANs configured on the switches in the region that are not specifically assigned to Multiple Spanning Tree Instances (MSTIs, described below). All VLANs in the IST instance of a region are part of the same, single spanning tree topology, which allows only one forwarding path between any two nodes belonging to any of the VLANs included in the IST instance. All switches in the region must belong  to the set of VLANs that comprise the IST instance.
<div id='mst-instance'/>
    - ####MSTI (Multiple Spanning Tree Instance):
        This is the default spanning tree instance in any MST region. It provides the root switch for the region and comprises all VLANs configured on the switches in the region that are not specifically assigned to Multiple Spanning Tree Instances (MSTIs, described below). All VLANs in the IST instance of a region are part of the same, single spanning tree topology, which allows only one forwarding path between any two nodes belonging to any of the VLANs included in the IST instance. All switches in the region must belong to the set of VLANs that comprise the IST instance. Note that the switch automatically places dynamic VLANs (resulting from GVRP operation) in the IST instance. Dynamic VLANs cannot exist in an MSTI.

##How MSTP Operates
- In the factory default configuration, spanning tree operation is off. Also, the switch retains its currently configured spanning tree parameter settings when disabled. Thus, if you disable spanning tree, then later re-enable it, the parameter settings will be the same as before spanning tree was disabled.
- All MSTP switches in a given region must be configured with the same VLANs. Also, each MSTP switch within the same region must have the same VLAN-toinstance assignments. (A VLAN can belong to only one instance within any region.) Within a region:
- All of the VLANs belonging to a given instance compose a single, active spanning-tree topology for that instance
- Each instance operates independently of other regions.
- Between regions there is a single, active spanning-tree topology.

##Terminology
<div id='t_cist'/>
- ####Common and Internal Spanning Tree (CIST):
Comprises all LANs and MSTP regions in a network. The CIST automatically determines the MST regions in a network and defines the root bridge (switch) and designated port for each region. The CIST includes the Common Spanning Tree (CST), the Internal Spanning Tree (IST) within each region, and any multiple spanning-tree instances (MSTIs) in a region.

<div id='t_ist'/>
- ####Internal Spanning Tree (IST):
Comprises all VLANs within a region that are not assigned to a multiple spanning-tree instance configured within the region. All MST switches in a region should belong to the IST. In a given region “X”, the IST root switch is the regional root switch and provides information on region “X” to other regions.

<div id='t_mstp'/>
- ####MSTP (Multiple Spanning Tree Protocol):
A network supporting MSTP allows multiple spanning tree instances within configured regions, and a single spanning tree among regions.

<div id='t_bpdu'/>
- ####MSTP BPDU(Bridge Protocol Data Unit):
These BPDUs carry region-specific information, such as the region identifier (region name and revision number). If a switch receives an MSTP BPDU with a region identifier that differs from its own, then the port on which that BPDU was received is on the boundary of the region in which the switch resides.

<div id='t_bridge'/>
- ####MSTP Bridge:
In this manual, an MSTP bridge is a switch (or another 802.1s compatible device) configured for MSTP operation.

<div id='t_region'/>
- ####MST Region:
An MST region forms a multiple spanning tree domain and is a component of a single spanning-tree domain within a network. For switches internal to the MST region:
    - All switches have identical MST configuration identifiers (region name and revision number).
    - All switches have identical VLAN assignments to the region’s IST and (optional) MST instances.
    - One switch functions as the designated bridge (IST root) for the region.
    - No switch has a point-to-point connection to a bridging device that cannot process RSTP BPDUs.

##Operating Rules
- All switches in a region must be configured with the same set of VLANs, as well as the same MST configuration name and MST configuration number.
- Within a region, a VLAN can be allocated to either a single MSTI or to the region’s IST instance.
- All switches in a region must have the same VID-to-MST instance and VID-to-IST instance assignments.
- There is one root MST switch per configured MST instance.
- Within any region, the root switch for the IST instance is also the root switch for the region. Because boundary ports provide the VLAN connectivity between regions, all boundary ports on a region's root switch should be configured as members of all static VLANs defined in the region.
- There is one root switch for the Common and Internal Spanning Tree(CIST). Note that the per-port hello-time parameter assignments on the CIST root switch propagate to the ports on downstream switches in the network and override the hello-time configured on the downstream switch ports.
- Where multiple MST regions exist in a network, there is only one active, physical communication path between any two regions, or between an MST region and an STP or RSTP switch. MSTP blocks any other physical paths as long as the currently active path remains in service.
- Within an MSTI, there is one spanning tree (one physical, communication path) between any two nodes. That is, within an MSTI, there is one instance of spanning tree, regardless of how many VLANs belong to the MSTI. Within an IST instance, there is also one spanning tree across all VLANs belonging to the IST instance.
- An MSTI comprises a unique set of VLANs and forms a single spanning-tree instance within the region to which it belongs.
- An MSTI at least should have one VLAN configured to it.
- Removing an MSTI internally moves the configured VLANs from MSTI to IST.
- Communication between MST regions uses a single spanning tree.
- If a port on a switch configured for MSTP receives a legacy (STP/802.1D or RSTP/802.1w) BPDU, it automatically operates as a legacy port. In this case, the MSTP switch interoperates with the connected STP or RSTP switch as a separate MST region.
- Within an MST region, there is one logical forwarding topology per instance, and each instance comprises a unique set of VLANs. Where multiple paths exist between a pair of nodes using VLANs belonging to the same instance, all but one of those paths will be blocked for that instance. However, if there are different paths in different instances, all such paths are available for traffic. Separate forwarding paths exist through separate spanning tree instances.
- A port can have different states (forwarding or blocking) for different instances (which represent different forwarding paths).
- MSTP interprets a switch mesh as a single link.

## How to use the feature
### Scenario 1
#### Setting up scenario 1 basic configuration
 - Create a 3 switch topology as specified below.
##### Physical Topology
- ```
+-----------------------------------------------------------------------------+
|    Region "A": Physical Topology                                            |
|                            +----------------+                               |
|                Link-2      +      SW_1      +      Link-1                   |
|          +-----------------+                +----------------+              |
|          |                 +                +                |              |
|          |                 +----------------+                |              |
|          +                                                   +              |
|   +------+---------+                                +--------+--------+     |
|   |                |            lINK-3              +                 |     |
|   |     SW_3       +--------------------------------+      SW_2       |     |
|   |                |                                +                 |     |
|   +----------------+                                +-----------------+     |
|                                                                             |
+-----------------------------------------------------------------------------+
```

- Configure instance 1 and 2 as specified below

    VLANS      | Instance 1 | Instance 2
    -----    | ---------- | ---------
    10,11,12 | Yes           | No
    20,21,22 | No           | Yes

- The logical and physical topologies resulting from these VLAN/Instance groupings result in blocking on different links for different VLANs:
##### Logical Topology
-    ```
+-----------------------------------------------------------------------------+
|  Logical topology for Instance-1                                            |
|                           +--------------------+                            |
|              Link-2       |       SW-1         |   Link-1                   |
|         +-----------------+ Root for Instance 1+---------------+            |
|         |                 |  VLANs = 10,11,12  |               |            |
|         |                 +--------------------+               |            |
|         |                                                      |            |
|         |                                                      |            |
|  +------+----------+                                  +--------+---------+  |
|  |     SW-2        |           Link-3(Blocked)        |     SW-3         |  |
|  |  Instance-1     +----------------------------------+  Instance-1      |  |
|  | VLANs = 10,11,12|                                  | VLANS = 10,11,12 |  |
|  +-----------------+                                  +------------------+  |
|                                                                             |
+-----------------------------------------------------------------------------+
```
- ```
+-----------------------------------------------------------------------------+
|  Logical topology for Instance-2                                            |
|                           +--------------------+                            |
|              Link-2       |       SW-1         |   Link-1(Blocked)          |
|         +-----------------+ Root for Instance 2+---------------+            |
|         |                 |  VLANs = 20,21,22  |               |            |
|         |                 +--------------------+               |            |
|         |                                                      |            |
|         |                                                      |            |
|  +------+----------+                                  +--------+---------+  |
|  |     SW-2        |           Link-3                 |     SW-3         |  |
|  |  Instance-2     +----------------------------------+  Instance-2      |  |
|  | VLANs = 20,21,22|                                  | VLANS = 20,21,22 |  |
|  +-----------------+                                  +------------------+  |
|                                                                             |
+-----------------------------------------------------------------------------+
```
- The logical and physical topologies resulting from these VLAN/Instance groupings result in blocking on different links for different VLANs:
- The Multiple Spanning Tree protocol (MSTP) uses VLANs to create multiple spanning trees in a network, which significantly improves network resource utilization while maintaining a loop-free environment.
- Thus, where a port belongs to multiple VLANs, it may be dynamically blocked in one spanning tree instance, but forwarding in another instance. This achieves load-balancing across the network while keeping the switch’s CPU load at a moderate level (by aggregating multiple VLANs in a single spanning tree instance).

- ####Configure MSTP global parameters
Configure the same region name and revision number in all the 3 switch:
        spanning-tree config-name mst
        spanning-tree config-revision 1
        spanning-tree
Create 2 MSTP instance and map the VLANS as mentioned below:
        spanning-tree instance 1 vlan 10
        spanning-tree instance 1 vlan 11
        spanning-tree instance 1 vlan 12

        spanning-tree instance 2 vlan 20
        spanning-tree instance 2 vlan 21
        spanning-tree instance 2 vlan 22

- ####Configure MSTP optional parameters

        spanning-tree max-hops 10
        spanning-tree hello-time 8
        spanning-tree forward-delay 8

- ####Verifying scenario 1 configuration
    MSTP details on Root switch
    ```
        switch# sh spanning-tree mst detail
        #### MST0
        Vlans mapped:  1-9,11-4095
        Bridge         Address:70:72:cf:03:d3:e9    priority:32768
        Root
        Regional Root
        Operational    Hello time(in seconds): 2  Forward delay(in seconds):15  Max-age(in seconds):20  txHoldCount(in pps): 6
        Configured     Hello time(in seconds): 2  Forward delay(in seconds):15  Max-age(in seconds):20  txHoldCount(in pps): 6

        Port           Role           State      Cost       Priority   Type
        -------------- -------------- ---------- ---------- ---------- ----------
        1              Designated     Forwarding 0          128        point_to_point
        2              Designated     Forwarding 0          128        point_to_point

        #### MST1
        Vlans mapped:  10
        Bridge         Address:70:72:cf:03:d3:e9    Priority:32768
        Root           Address:70:72:cf:03:d3:e9    Priority:32769
                       Port:, Cost:20000, Rem Hops:0

        Port           Role           State      Cost    Priority   Type
        -------------- -------------- ---------- ------- ---------- ----------
        1              Designated     Forwarding 0       128        point_to_point
        2              Designated     Forwarding 0       128        point_to_point

        Port 1
        Designated root address            : 70:72:cf:03:d3:e9
        Designated regional root address   : 70:72:cf:03:d3:e9
        Designated bridge address          : 32768.0.70:72:cf:03:d3:e9
        Timers:    Message expires in 1 sec, Forward delay expiry:18, Forward transitions:18
        Bpdus sent 183, received 4

        Port 2
        Designated root address            : 70:72:cf:03:d3:e9
        Designated regional root address   : 70:72:cf:03:d3:e9
        Designated bridge address          : 32768.0.70:72:cf:03:d3:e9
        Timers:    Message expires in 1 sec, Forward delay expiry:18, Forward transitions:18
        Bpdus sent 183, received 4
```

####Troubleshooting scenario 1 configuration
- Duplicate packets on a VLAN, or packets not arriving on a LAN at all. The allocation of VLANs to MSTIs may not be identical among all switches in a region.
- A Switch Intended To Operate Within a Region Does Not Receive Traffic from Other Switches in the Region. An MSTP switch intended for a particular region may not have the same configuration name or region revision number as the other switches intended for the same region. The MSTP Configuration Name and MSTP Configuration Revision number must be identical on all MSTP switches intended for the same region. Another possibility is that the set of VLANs configured on the switch may not match the set of VLANs configured on other switches in the intended region.

<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
## CLI
- Click [here](http://git.openswitch.net/cgit/openswitch/ops/plain/docs/MSTP_cli.md) for the CLI commands related to the MSTP feature.

## Related features
- When configuring the switch for MSTP, it might also be necessary to configure [Physical Interface](/documents/user/interface_user_guide) so that interface to which neighbor is connected will act as expected.

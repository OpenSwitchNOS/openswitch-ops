# OSPF

## Table of contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [How to use the feature](#how-to-use-the-feature)
	- [Setting up the basic configuration](#setting-up-the-basic-configuration)
	- [Setting up the optional configuration](#setting-up-the-optional-configuration)
	- [Verifying the configuration](#verifying-the-configuration)
	- [Troubleshooting the configuration](#troubleshooting-the-configuration)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
OSPFv2 (or simply OSPF) is an interior gateway protocol (IGP) that routes packets within a single autonomous system (AS). OSPF uses link-state information to make routing decisions, making route calculations using the shortest-path-first (SPF) algorithm (also referred to as the Dijkstra algorithm). Each router running OSPF floods link-state advertisements throughout the AS or area that contain information about that router’s attached interfaces and routing metrics. Each router uses the information in these link-state advertisements to calculate the least cost path to each network and create a routing table for the protocol.

## Prerequisites
- User is familiar with the OSPF fundamentals.
- User have access to the switch and have logged in.
- User have configured at least one interface for IPv4 that can communicate with a remote OSPFv2 neighbor.
- IP routing feature have been enabled.


## How to use the feature
### Setting up the basic configuration
1. Creating an OSPF instance
    Create the OSPF instance using the command `router ospf` in configure context. When a router instance is created it is enabled by default.
2. Configuring OSPF network for an area
	Specify the OSPF enabled interface(s) using the command `network <network_prefix> area (<area_ip>|<area_id>)` in router context. If the interface has an address from range specified as argument, then the command enables ospf on this interface so router can provide network information to the other ospf routers via this interface.

### Setting up the optional configuration
1. Configure router id
	Configure router id using the command, `router-id <A.B.C.D>` in router context. If the router id is not configured then the dynamic router id provided by the zebra will be used.

For more OSPF configurations refer the [OSPF command reference document](/documents/user/ospf_cli).

### Verifying the configuration

 1. Verify the configured values and area related information using the `show ip ospf` command.
 2. For the interfaces related information and neighbors related information use `show ip ospf interface` and `show ip neighbor detail`  command respectively.

 For more OSPF configurations refer the [OSPF command reference document](/documents/user/ospf_cli).

### Troubleshooting the configuration

#### Scenario 1
##### Condition
The OSPF packets are not reaching the daemon.

##### Cause
- User has not configured router id and Zebra not able to allocate router id.

##### Remedy
- Check the syslog for error message.

#### Scenario 2
##### Condition
The neighbors are not discovered.

##### Cause
- The interface is passive.
- The neighbors are not reachable.

##### Remedy
- Check the syslog for error message.
- Check the reachability of the network using ping command.

#### Scenario 3
##### Condition
Neighbors are reachable but the adjacency are not formed.

##### Cause
- The authentication type or key is not matching.
- The timer intervals like hello interval or dead interval is misconfigured.
- MTU values mismatch and "mtu ignore" is not configured.
- The neighbors are not in same area.

##### Remedy
- Check the syslog for error message.

#### Scenario 4
##### Condition
Neighbors are reachable. Adjacency is formed in some switches and not in others.

##### Cause
- The neighbor FSM is not in "full" state.

##### Remedy
- If the state is "init", this implies that the local router is able to see the OSPF hello from neighbors. But the neighbor has not seen OSPF hello from local router.

#### Scenario 5
##### Condition
No DR/BDR is seen in the network.

##### Cause
- If the priority is 0 in all the OSPF routers then none of the routers will be selected as DR/BDR.

##### Remedy
- Configure any non-zero values as priority.

#### Scenario 6
##### Condition
Routes are not being learnt/advertised.

##### Cause
- Adjacencies are not formed (neighbor fsm is not in "full" state).
- No corresponding LSAs are present.

##### Remedy
- Check the syslog for error message.


## CLI
Click [here-TBL](/documents/user/ospf_cli) for the CLI commands related to the OSPF feature.

## Related features
None.

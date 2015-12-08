# OSPFv2

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
OSPFv2 is an interior gateway protocol (IGP) that routes packets within a single autonomous system (AS). OSPFv2 uses link-state information to make routing decisions and route calculations using the Dijkstra's shortest-path-first (SPF) algorithm. Each router runs the OSPFv2 floods link-state advertisements throughout the AS or area that contains information about that router’s attached interfaces and routing metrics. Each router uses the information in these link-state advertisements to calculate the least cost path to each network and populates the routing information base for the router.

## Prerequisites

User must be familiar with OSPFv2 fundamentals and have the following set up:
- Access to the switch and be logged in.
- Configured at least one interface for IPv4 that can communicate with peering OSPFv2 router.
- Enabled IPv4 routing feature.

## How to use the feature
### Setting up the basic configuration
**1. Creating an OSPFV2 instance**
    Create the OSPFv2 instance using the command `router ospf` in configuration context. When a router instance is created it is enabled by default.

**2. Configuring OSPFv2 network for an area**
	Specify the OSPFv2 enabled interface(s) using the command `network <network_prefix> area (<area_ip>|<area_id>)` in router ospf context. If any interfaces has a primary IPv4 address enabled on the subnetwork which is matching to the "network" or subset of the "network", then those will participate in the OSPFv2. i.e., OSPFv2 protocol will be enabled on those interfaces.

### Setting up the optional configuration
**1. Configure router id**
	Configure router id using the command, `router-id <A.B.C.D>` in router ospf context. If the router id is not configured then the dynamic router id provided by the routing manager daemon i.e. zebra will be used.

**2. Modifying the default timers**
	Modify the default value of the timers such as dead interval, hello interval, and retransmit interval by using the following commands in the interface context:
    - Dead interval: `ip ospf dead-interval <dead_interval>`
    - Hello interval: `ip ospf hello-interval <hello_interval>`
    - retransmit interval: `ip ospf retransmit-interval <retransmit_interval>`

**3. Configuring route summarizations**
	Summarize the routes from other protocols using the `summary-address <ip_prefix> {not-advertise | tag <tag>}` command in the router ospf context.

**4. Configuring route redistribution**
	Redistirbute routes originating from other protocols into OSPFv2 by using the `redistribute {bgp | connected | static}` command. The `default-metric <metric_value>` command in OSPFv2 router context sets the default metric to be used for redistributed routes.

**5. Configuring virtual links**
	The virtual link and the authentication type for the virtual link can be configured using the command `area (<area_ip>|<area_id>) virtual-link <remote_address> {authentication (message-digest|
null)}` in router ospf context.

**6. Configuring NSSA**
	Configure an area as not so stubby using the `area (<area_ip>|<area_id>) nssa {translate-candidate|translate-never|translate-always} [no-summary]` command in the router ospf context.

**7. Configuring stub areas**
	Use the `area (<area_ip>|<area_id>) stub [no_summary]` command in the router ospf context to set the area type as stub.

**8. Configuring filter lists for border routers**
	Filter networks between OSPFv2 areas using the `area (<area_ip>|<area_id>) filter-list <list-name> (in|out)` command in the router ospf context. The filtering is done as per the prefix lists. Only use this command on area border routers.

For more OSPFv2 configurations refer to the [OSPFv2 command reference document](/documents/user/OSPFv2_cli).

### Verifying the configuration

 1. Verify the configured values and area related information using the `show ip ospf` command.
 2. For the interfaces related information and neighbors related information use `show ip ospf interface` and `show ip neighbor detail` commands respectively.
 3. The `show ip ospf database {asbr-summary|external|network|router|summary|nssa-external|opaque-link|opaque-area|opaque-as|max-age} [<lsa_id>] {self-originate | adv-router <router_id>}` command shows the OSPFv2 link state database summary.
 4. The OSPFv2 routing table can be verified using the `show ip ospf route` command.
 5. The configurations can be verified using the command `show running-config` or `show running-config router ospf`.
 An example of the `show running-config router ospf` command follows:
 ```
 Switch#show running-config router ospf
 !
 router ospf
     router-id 1.1.1.1
     network 10.0.0.0/24 area 100
     area  100 default-cost 2
     area 100 filter-list list2 out
	 area 100 virtual-link  100.0.1.1
     area 100 virtual-link  100.0.1.1 hello-interval 30
     area 100 virtual-link  100.0.1.1 retransmit-interval 30
```
 For more OSPFv2 configurations refer to the [OSPFv2 command reference document](/documents/user/OSPFv2_cli).

### Troubleshooting the configuration

#### Scenario 1
##### Condition
The OSPFv2 packets are not reaching the daemon.

##### Cause
1.  The user has not configured the router id in the router ospf context. Furthermore, `ospfd` has not received a system global router-id.
2. OSPFv2 is not enabled or configured for any network.
3. No interfaces have IPv4 address matching to any of the OSPFv2 enabled "networks".

##### Remedy
- Check the syslog for error messages.
- Capture and validate the OSPFv2 protocol packets using any supported compatible packet capture utility such as `tcpdump` as an example.

#### Scenario 2
##### Condition
The neighbors are not discovered.

##### Cause
- The interface is passive.
- The neighbors are not reachable.

##### Remedy
- Check the syslog for error messages.
- Check the reachability of the network using the ping command.
- Capture and validate the OSPFv2 protocol packets using any supported compatible packet capture utility such as `tcpdump` as an example.

#### Scenario 3
##### Condition
Neighbors are reachable but the adjacency is not formed.

##### Cause
- Area types are not matching.
- Peer's subnet and subnet mask are not matching for the connected interfaces.
- Duplicate Router-id.
- Duplicate interface iPv4 addresses.
- Interface type mismatch.
- DR Priority 0 for both the routers.
- The authentication type or key is not matching.
- The timer intervals like hello interval or dead interval are not matching.
- MTU value is not matching and "mtu ignore" is not configured.
- The neighbors are not in the same area.

##### Remedy
- Check the syslog for error messages.
- Check if the required configurations are correct and valid using the show commands specified in the "verifying the configuration" section. If any of the values do not match, then correct the configuration.

#### Scenario 4
##### Condition
Neighbors are reachable. Adjacency is formed in some of the switches and not in others.

##### Cause
- The neighbor FSM is not in a "full" state.
- The "FULL" state can be established with DR or BDR only, The state that has all DR-Other is in a 2-Way state.

##### Remedy
- If the state is "init", this implies that the local router is able to see the OSPFv2 hello from neighbors. But the neighbor has not seen OSPFv2 hello from local router. Check the reachability on both the sides using the ping command.
- Capture and validate the OSPFv2 protocol packets using any supported compatible packet capture utility such as `tcpdump` as an example.
- Check if the required configurations are correct and valid.

#### Scenario 5
##### Condition
No DR or BDR is seen in the network.

##### Cause
- If the priority is zero on all the OSPFv2 routers, then none of the routers are selected as DR or BDR. The `show ip osppf neighbor` command lists the neighbors and their priorities.

##### Remedy
- Configure any non-zero values as priority.

#### Scenario 6
##### Condition
Routes are not being learnt or advertised.

##### Cause
- Adjacencies are not formed (neighbor fsm is not in "full" state). This can be verified using the `show ip ospf neighbor` command.
- No corresponding LSAs are present. The `show ip osppf database` command lists the LSA.

##### Remedy
- Check the syslog for error messages.
- Capture and validate the OSPFv2 protocol packets using any supported compatible packet capture utility such as `tcpdump` as an example.

#### Scenario 7
##### Condition
SPF algorithm is getting executed many times. This can be seen from the `show ip ospf` command.

##### Cause
- Links are flapping in the network. The change in the topology can be verified using the `show ip ospf database router` command.
- The SPF minimum hold time or maximum hold time is less. The SPF timer related configurations can be verified using `show ip ospf` command.

##### Remedy
- Go to each network and check the interfaces using `show interface` to identify the flapping link.
- Fine tune the SPF timer related configurations.

#### Scenario 8
##### Condition
SPF algorithm is not getting executed. This can be seen from the `show ip ospf` command.

##### Cause
- The SPF minimum hold time or maximum hold time is set to very large values. The SPF timer related configurations can be verified using `show ip ospf` command.

##### Remedy
- Fine tune the SPF timer related configurations.

## CLI
Click [here](/documents/user/OSPFv2_cli) for the CLI commands related to the OSPFv2 feature.

## Related features
None.

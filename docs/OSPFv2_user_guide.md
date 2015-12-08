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
OSPFv2 is an interior gateway protocol (IGP) that routes packets within a single autonomous system (AS). OSPFv2 uses link-state information to make routing decisions, making route calculations using the Dijkstra's shortest-path-first (SPF) algorithm. Each router running OSPFv2 floods link-state advertisements throughout the AS or area that contain information about that router’s attached interfaces and routing metrics. Each router uses the information in these link-state advertisements to calculate the least cost path to each network and populates routing information base for the router.

## Prerequisites
- User is familiar with the OSPFv2 fundamentals.
- User have access to the switch and have logged in.
- User have configured at least one interface for IPv4 that can communicate with peering OSPFv2 router.
- IP routing feature have been enabled.


## How to use the feature
### Setting up the basic configuration
1. Creating an OSPFV2 instance
    Create the OSPFv2 instance using the command `router ospf` in configuration context. When a router instance is created it is enabled by default.
2. Configuring OSPFv2 network for an area
	Specify the OSPFv2 enabled interface(s) using the command `network <network_prefix> area (<area_ip>|<area_id>)` in router ospf context. If any interfaces has a primary IPv4 address enabled on the subnetwork which is matching to the "network" or subset of the "network", then those will participate in the OSPFv2. i.e., OSPFv2 protocol will be enabled on those interfaces.

### Setting up the optional configuration
1. Configure router id
	Configure router id using the command, `router-id <A.B.C.D>` in router ospf context. If the router id is not configured then the dynamic router id provided by the zebra will be used.
2. Modifying the default timers
	The default value of timers like dead timer, hello interval, retransmit interval can be modified using the command `area (<area_ip>|<area_id>) virtual-link <remote_address> (hello-interval | retransmit-interval | transmit-delay  | dead-interval) <time_value>` in ospf router context.
3. Configuring route summarizations
	The routes from other protocols can be summarized using the command `summary-address <ip_prefix> {not-advertise | tag <tag>}` in ospf router context.
4. Configuring Redistribution
	The command `redistribute {bgp | connected | static}` in ospf router context redistributes routes originating from other protocols into OSPF. The `default-metric <metric_value>` command in ospf router context sets the default metric to be used for redistributed routes into OSPF.
5. Configuring Virtual Links
	The virtual link and the authentication type for the virtual link can be configured using the command `area (<area_ip>|<area_id>) virtual-link <remote_address> {authentication (message-digest|null)}` in ospf router context.
6. Configuring NSSA
	An area can be configured as not so stubby using the command `area (<area_ip>|<area_id>) nssa {translate-candidate|translate-never|translate-always} [no-summary]` in ospf router context.
7. Configuring Stub Areas
	The command `area (<area_ip>|<area_id>) stub [no_summary]` in ospf router co isntext is used to set the area type as stub.

8. Configuring Filter Lists for Border Routers
	The command `area (<area_ip>|<area_id>) filter-list <list-name> (in|out)` in ospf router context filters networks between OSPF areas. The filtering is done as per the prefix lists. This command make sense only on area border routers.
For more OSPFv2 configurations refer the [OSPFv2 command reference document](/documents/user/OSPFv2_cli).

### Verifying the configuration

 1. Verify the configured values and area related information using the `show ip ospf` command.
 2. For the interfaces related information and neighbors related information use `show ip ospf interface` and `show ip neighbor detail`  command respectively.
 3. The `show ip ospf database {asbr-summary|external|network|router|summary|nssa-external|opaque-link|opaque-area|opaque-as|max-age} [<lsa_id>] {self-originate | adv-router <router_id>}` command shows OSPF link state database summary.
 4. The OSPF routing table can be verified using the command `show ip ospf route`.
 5. The configurations can be verified using the command `show running-config` or `show running-config router ospf`.
 Example of `show running-config router ospf` is:
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
 For more OSPFv2 configurations refer the [OSPFv2 command reference document](/documents/user/OSPFv2_cli).

### Troubleshooting the configuration

#### Scenario 1
##### Condition
The OSPFv2 packets are not reaching the daemon.

##### Cause
1. User has not configured router id in "router ospf" context. And also ospfd hasn't received a system global router-id.
2. OSPFv2 is not enabled/configured for any network.
3. No interfaces have IPv4 address matching to the any OSPFv2 enabled "network".

##### Remedy
- Check the syslog for error message.
- Capture the OSPFv2 protocol packets using any compatible / supported packet capture utility (like tcpdump, for example) and validate it.

#### Scenario 2
##### Condition
The neighbors are not discovered.

##### Cause
1. The interface is passive.
2. The neighbors are not reachable.

##### Remedy
- Check the syslog for error message.
- Check the reachability of the network using ping command.
- Capture the OSPFv2 protocol packets using any compatible / supported packet capture utility (like tcpdump, for example) and validate it.

#### Scenario 3
##### Condition
Neighbors are reachable but the adjacency are not formed.

##### Cause
1.  Area types are not matching.
2.  Subnet and subnet mask are not matching for the connected interfaces of the peers.
3.  Duplicate Router-id.
4.  Duplicate interface iPv4 addresses.
5.  Interface type mismatch.
6.  DR Priority 0 for both the routers.
7.  The authentication type or key is not matching.
8.  The timer intervals like hello interval or dead interval is not matching.
9.  MTU values is not matching and "mtu ignore" is not configured.
10. The neighbors are not in same area.

##### Remedy
- Check the syslog for error message.
- Check if the required configurations are correct and valid. If any of the values does not match, then correct the configuration.

#### Scenario 4
##### Condition
Neighbors are reachable. Adjacency is formed in some switches and not in others.

##### Cause
1. The neighbor FSM is not in "full" state.
2. The "FULL" state can be established with DR/BDR only, State with all DR-Other will be in 2-Way state.

##### Remedy
- If the state is "init", this implies that the local router is able to see the OSPFv2 hello from neighbors. But the neighbor has not seen OSPFv2 hello from local router.
- Capture the OSPFv2 protocol packets using any compatible / supported packet capture utility (like tcpdump, for example) and validate it.
- Check if the required configurations are correct and valid.

#### Scenario 5
##### Condition
No DR/BDR is seen in the network.

##### Cause
1. If the priority is 0 in all the OSPFv2 routers then none of the routers will be selected as DR/BDR.

##### Remedy
- Configure any non-zero values as priority.

#### Scenario 6
##### Condition
Routes are not being learnt/advertised.

##### Cause
1. Adjacencies are not formed (neighbor fsm is not in "full" state).
2. No corresponding LSAs are present.

##### Remedy
- Check the syslog for error message.
- Capture the OSPFv2 protocol packets using any compatible / supported packet capture utility (like tcpdump, for example) and validate it.


## CLI
Click [here](/documents/user/OSPFv2_cli) for the CLI commands related to the OSPFv2 feature.

## Related features
None.

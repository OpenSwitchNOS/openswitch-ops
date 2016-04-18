# OSPFv2

## Contents
- [Overview](#overview)adjacencyadjacency
- [Prerequisites](#prerequisites)
- [List of abbreviations](#list-of-abbreviations)
- [How to use the feature](#how-to-use-the-feature)
	- [Setting up the basic configuration](#setting-up-the-basic-configuration)
	- [Setting up the optional configuration](#setting-up-the-optional-configuration)
	- [Verifying the configuration](#verifying-the-configuration)
- [OSPFv2 supportability](#ospfv2-supportability)
	- [Enabling the debug knobs for OSPFv2](#enabling-the-debug-knobs-for-ospfv2)
- [Troubleshooting the configuration](#troubleshooting-the-configuration)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
OSPFv2 is an interior gateway protocol (IGP) that routes packets within a single autonomous system (AS). OSPFv2 uses link-state information to make routing decisions and route calculations using the Dijkstra's shortest-path-first (SPF) algorithm. Each router runs the OSPFv2 floods link-state advertisements throughout the AS or area that contains information about that router’s attached interfaces and routing metrics. Each router uses the information in these link-state advertisements to calculate the least cost path to each network, and populates the routing information base for the router.

## Prerequisites

Users must be familiar with OSPFv2 fundamentals and have the following set up:
- Access to the switch and be logged in.
- At least one interface configured for IPv4 that can communicate with a peering OSPFv2 router.
- Enabled the IPv4 routing feature.

## List of abbreviations
|Abbreviation   | Expansion   |
|---|---|
|  BDR | Backup Designated Router  |
|  DR | Designated Router  |
|  OSPF |  Open Shortest Path First |
|  SPF | Shortest Path First  |

## How to use the feature
### Setting up the basic configuration
**1. Enabling OSPFv2**
** Creating an OSPFV2 instance**
    Create the OSPFv2 instance using the `router ospf` command in the configuration context. When a router instance is created it is enabled by default.

** Configuring the OSPFv2 network for an area**
	Specify the OSPFv2 enabled interface(s) using the `network <network_prefix> area (<area_ip>|<area_id>)` command in the router ospf context. If any interface has a primary IPv4 address enabled on the subnetwork that matches the "network" or subset of the "network", then the OSPFv2 protocol is enabled on that interface.

**2. Configuring the router ID**
	Configure the router ID using the `router-id <A.B.C.D>` command in the router ospf context. If the router ID is not configured then the dynamic router ID provided by the routing manager daemon (for example, zebra) is used.


### Setting up the optional configuration

**1. Configuring OSPFv2 authentication**
** Configuring authentication for an area**
	Configure authentication for all networks in an area using the `area  (<area_ip>|<area_id>) authentication [message-digest]` command in the router ospf context, and the `ip ospf authentication-key <key>` and `ip ospf message-digest-key <key_id> md5 <message_digest_key>` commands in the interface context.

** Configuring authentication for an interface**
	Configure authentication for individual interfaces using the `ip ospf authentication {message-digest}`, `ip ospf authentication-key <key>` and `ip ospf message-digest-key <key_id> md5 <message_digest_key>` commands in the interface context.

** Configuring authentication for virtual links**
	The authentication type for the virtual link can be configured using the `area (<area_ip>|<area_id>) virtual-link <remote_address> {authentication (message-digest|
null)}` command in the router ospf context.

**2. Configuring OSPFv2 interface parameters**
** Modifying the default timers**
	Modify the default value of the timers, such as dead interval, hello interval, and retransmit interval, by using the following commands in the interface context:
   - Dead interval: `ip ospf dead-interval <dead_interval>`
   - Hello interval: `ip ospf hello-interval <hello_interval>`
   - retransmit interval: `ip ospf retransmit-interval <retransmit_interval>`

** Configuring OSPFv2 priority **
	Configure the OSPFv2 priority for the interface using the `ip ospf priority <priority_value>` command in the interface context.

** Configuring OSPFv2 network type **
	Configure the OSPFv2 network type for the interface using the `ip ospf network (broadcast|point-to-point)` command in the interface context.

** Configuring interface cost **
	Configure the interface cost using the `ip ospf cost <interface_cost>` command in the interface context.

**3. Configuring the OSPFv2 area**
** Configuring route summarizations**
	Summarize the routes matching the specified address/mask using the `area (<area_ip>|<area_id>) range <ipv4_address> {cost <range_cost> | not-advertise}` command in the router ospf context.

** Configuring virtual links**
	Configure the virtual link using the `area (<area_ip>|<area_id>) virtual-link <remote_address>` command in the router ospf context.

** Configuring NSSA**
	Configure an area as not so stubby using the `area (<area_ip>|<area_id>) nssa {translate-candidate|translate-never|translate-always} [no-summary]` command in the router ospf context.

** Configuring stub areas**
	Use the `area (<area_ip>|<area_id>) stub` command in the router ospf context to set the area type as stub.

** Configuring totally stubby areas**
	Use the `area (<area_ip>|<area_id>) stub [no_summary]` command in the router ospf context to set the area type as a totally stubby area, and prevent all summary route updates from going into the stub area.

** Configuring filter lists for border routers**
	Filter networks between OSPFv2 areas using the `area (<area_ip>|<area_id>) filter-list <list-name> (in|out)` command in the router ospf context. The filtering is done per the prefix lists. Only use this command on area border routers.

**4. Redistributing routes into OSPFv2**
	Redistirbute routes originating from other protocols into OSPFv2 by using the `redistribute {bgp | connected | static}` command. The `default-metric <metric_value>` command in the OSPFv2 router context sets the default metric used for redistributed routes.

**5. Configuring a passive interface**
	An interface can be configured as a passive interface using the `passive-interface <interface>` command in the router ospf context. To configure all the OSPFv2 enabled interfaces as passive, use the `passive-interface default` command in the router ospf context.

**6. Configuring NBMA neighbor**
	Configure the NBMA neighbor address, poll interval, and priority value using the `neighbor <neighbor_ip> {poll-interval <poll_value> | priority <priority_value>}` command in the router ospf context

For more OSPFv2 configurations, refer to the [OSPFv2 command reference document](/documents/user/OSPFv2_cli).

### Verifying the configuration

 1. Verify the configured values and area related information using the `show ip ospf` command.
 2. For the interfaces related information and neighbors related information use the `show ip ospf interface` and `show ip neighbor detail` commands respectively.
 3. The `show ip ospf database {asbr-summary|external|network|router|summary|nssa-external|opaque-link|opaque-area|opaque-as|max-age} [lsa_id] {self-originate | adv-router router_id}` command shows the OSPFv2 link state database summary.
 4. Verify the OSPFv2 routing table using the `show ip ospf route` command.
 5. Verify the configurations using the `show running-config` or `show running-config router ospf` commands.
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
 For more OSPFv2 configurations, refer to the [OSPFv2 command reference document](/documents/user/OSPFv2_cli).


A sample topology and example configuration follows:

** Topology **
```ditaa
+---------------+             +---------------+          +---------------+
|               |    Area 0   |               |  Area 1  |               |
| Switch 1     1+-------------+1  Switch 2   2+----------+1  Switch 3    |
|               |             |               |          |               |
|               |             |               |          |               |
+---------------+             +---------------+          +---------------+
```

** Configuration example **
```
SWITCH 1
switch#config t
switch(conf)#router ospf
switch(conf)#network 10.10.10.0/24 area 0

SWITCH 2
switch#config t
switch(conf)#router ospf
switch(conf)#network 10.10.10.0/24 area 0
switch(conf)#network 20.20.20.0/24 area 1

SWITCH 3
switch#config t
switch(conf)#router ospf
switch(conf)#network 20.20.20.0/24 area 1
```
Using the above configuration, OSPFv2 can be enabled on interface 1 of Switch 1, interface 1 and 2 of Switch 2, and interface 1 of Switch 3. The adjacency is formed between them. Switch 2 acts as an ABR.

## OSPFv2 supportability
VLOG and ZLOG are the logging used for troubleshooting purposes. Logging levels for VLOG (and ZLOG also) can be changed using the following commands:

	switch(conf)# vlog feature ospfv2 (syslog | file | all) (emer | err | warn | info | dbg | off)
											OR
    switch(conf)# vlog daemon ops-ospfd (syslog | file | all) (emer | err | warn | info | dbg | off)

This configures the specified logging level, and only those logs with the specified priority level and above appear.


### Enabling the debug knobs for OSPFv2
Use the following command to enable the debug knobs in the OSPFv2 daemon for troubleshooting purposes:

    switch(conf)# debug ospfv2 packet (hello|dd|ls-request|ls-update|ls-ack|all)

The above command enables the "packet" knobs, and the logging destination (default : syslog) contains the logs for the packet sent between routers.

## Troubleshooting the configuration
The location of the log files used to troubleshoot depends on the platform on which OSPFv2 is running. For physical switchse the logging is handled by VLOG, and the log files are store at /var/log/messages. For simulated environments the log files are stored at /var/log/syslog/ on the virtual machine running the simulated image. Therefore, log files are used generically in the following scenarios.

#### Scenario 1
##### Condition
The OSPFv2 packets are not reaching the daemon.

##### Cause
1.  The router ID is not configured in the router ospf context. This can be verified using the `show ip ospf` command. Furthermore, `ospfd` has not received a system global router-id.
2. OSPFv2 is not configured for any network. If this is the case, then the `show ip ospf interface` command does not display any entry.
3. No interfaces have an IPv4 address matching any of the OSPFv2 enabled "networks". In this case the `show ip ospf interface` command does not display any entry.

##### Remedy
- The `show ip ospf` command output displays the configured router ID value (if configured). If no router ID value is displayed, then configure the router ID using the command `router <router-id>` in the router ospf context.
- If `show ip ospf interface` does not display any entry, or there is no entry matching the configured network range, then configure the proper network range using the `network <network_prefix> area (<area_ip>|<area_id>)` command in the router ospf context.

#### Scenario 2
##### Condition
The neighbors are not discovered.

##### Cause
- The interface is passive. The `show ip ospf interface` command displays that interface is passive.
- The neighbors are not reachable. Check the reachability of the network using the ping command.

##### Remedy
- If the interface has been configured as passive, check if the configuration/topology is correct.
- If the network is not reachable, then configure the required routes and default gateway to make the switches reachable.
- Capture and validate the OSPFv2 protocol packets using any supported compatible packet capture utility, such as `tcpdump`.
- Check the log file for error messages.

#### Scenario 3
##### Condition
Neighbors are reachable, but the adjacency is not formed.

##### Cause
- Area types are not matching. Check the area type using the `show ip ospf interface` command.
- The peer's subnet and the subnet mask are not matching for the connected interfaces. Check the interface value using the `show ip ospf interface` command.
- Duplicate Router-id. Check the router ID using the `show ip ospf` command.

- The designated router (DR) priority is zero for both of the routers. Check the priority value using the `show ip ospf interface` command.
- The authentication type or key is not matching. Check the log file for any authentication related failure message.
- The neighbors are not in the same area. Check the area ID using the `show ip ospf` command.

Use the `show ip ospf interface` command to verify the following causes:

- The timer intervals, such as the hello interval or the dead interval, are not matching.
- The MTU value is not matching, and "mtu ignore" is not configured.
- An interface type mismatch.
- Duplicate interface IPv4 addresses.

##### Remedy
- If the log file contains any authentication related failure, then configure the appropriate authentication method and keys using the `ip ospf authentication {message-digest}` and `ip ospf authentication-key <key>` commands in the interface context.
- If any timer values are mismatched, then configure the appropriate timer values using the `ip ospf {dead-interval <dead_interval> } | {hello-interval <hello_interval>} | mtu-ignore` command in the interface context.
- If the prirotiy is 0, configure the proper priority value using the `ip ospf priority <priority_value>` command in the interface context.
- If areas are not matching, then configure proper areas using the command `network <network_prefix> area (<area_ip>|<area_id>)` in router ospf context.
- If the area type is mismatched then configure the proper area type using the `area (<area_ip>|<area_id>) nssa {translate-candidate|translate-never|translate-always} [no-summary]` command in the router ospf context.
- For mismatching network types, configure matching network types using the `ip ospf network (broadcast|point-to-point)` command in the interface context.

If none of the above remedies work then:
- Capture and validate the OSPFv2 protocol packets using any supported compatible packet capture utility, such as `tcpdump`. If the packets are corrupted, then there is a bug in the software.
- Check the log file for error messages.

#### Scenario 4
##### Condition
Neighbors are reachable. Adjacency is formed in some of the switches, but not in others.

##### Cause
- The `show ip ospf neighbor` command displays some neighbors with states other than "full". On broadcast media and non-broadcast multiaccess networks, a router becomes full only with the designated router (DR) and the backup designated router (BDR); it stays in the 2-way state with all other neighbors.

##### Remedy
- If the state is "init", this implies that the local router is able to see the OSPFv2 hello from the neighbor, but the neighbor has not seen the OSPFv2 hello from the local router. Check the reachability on both the sides using the ping command.
- Capture and validate the OSPFv2 protocol packets using any supported compatible packet capture utility, such as `tcpdump`.
- Check if the configurations listed in "Setting up the basic configuration" are correct and valid.
- Check if any other configurations that were modified are valid. The `show running-config router ospf` command lists all of the configurations.

#### Scenario 5
##### Condition
No DR or BDR is seen in the network.

##### Cause
- If the priority is zero on all of the OSPFv2 routers, then none of the routers are selected as DR or BDR. The `show ip ospf neighbor` command lists the neighbors and their priorities.

##### Remedy
- Configure a non-zero value as the priority using the `ip ospf priority <priority_value>` command in the interface context.

#### Scenario 6
##### Condition
Routes are not being learned or advertised.

##### Cause
- Adjacencies are not formed (neighbor fsm is not in the "full" state). Verify this using the `show ip ospf neighbor` command.
- No corresponding LSAs are present. The `show ip ospf database` command lists the LSA.

##### Remedy
- If the adjacencies are not formed, then try the remedies listed in the scenarios "Neighbors are reachable but the adjacency is not formed" and "The neighbors are not discovered".
- Capture and validate the OSPFv2 protocol packets using any supported compatible packet capture utility, such as `tcpdump`.

#### Scenario 7
##### Condition
The SPF algorithm is being executed many times. This is seen from the `show ip ospf` command.

##### Cause
- Links are flapping in the network. Verify the change in the topology using the `show ip ospf database router` command.
- The SPF minimum hold time or maximum hold time is a low value. Verify the SPF timer related configurations using the `show ip ospf` command.

##### Remedy
- Go to each switch and check the interfaces using the `show interface` command to identify the flapping link.
- Fine tune the SPF timer related configurations using the `timers throttle spf <spf_delay_time> <spf_hold_time> <spf_maximum_time>` command in the router ospf context.

#### Scenario 8
##### Condition
The SPF algorithm is not being executed. This is seen from the `show ip ospf` command.

##### Cause
- The SPF minimum hold time or the maximum hold time is set to a very large value. Verify the SPF timer related configurations using the `show ip ospf` command.

##### Remedy
- Fine tune the SPF timer related configurations using the `timers throttle spf <spf_delay_time> <spf_hold_time> <spf_maximum_time>` command in the router ospf context.

## CLI
Click [here](/documents/user/OSPFv2_cli) for the CLI commands related to the OSPFv2 feature.

## Related features
None.

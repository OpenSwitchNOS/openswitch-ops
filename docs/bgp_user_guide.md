## BGP ##

## Overview ##
Border Gateway Protocol (BGP) is most commonly used **inter-AS** (autonomous system) routing protocol. The latest BGP version is 4. **BGP-4** supports Classless Inter-Domain Routing (CIDR) i.e. advertises the routes based on destinations as an IP prefix and not the network "class" within BGP.
BGP is a **path-vector** protocol which provides routing information across various BGP routers to be exchanged using destination-based forwarding. For example: The router sends packets based merely on the destination IP address carried in the IP header of the packet. In most cases, we have multiple routes to the same destination and then BGP decides which route to choose using the path attributes, such as *Shortest AS_Path, Multi_Exit_Disc (Multi-exit discriminator, or MED), Origin, Next_hop, Local_pref,* and so on.
BGP provides routing for routers or switches or both, that can be deployed in ISP, Enterprise, and data centers.

## Setting up the basic configuration ##
The following is the minimum configuration needed to set up the BGP router. The AS number is unique to the Autonomous system and is used to distinguish between internal or external or both BGP connections.

 1. The *'router bgp < asn >'* enables the BGP router for the AS number. The AS numbers range from 1 to 65535.
 2. The *'bgp router-id A.B.C.D'* command sets the BGP router-id to A.B.C.D.
 3. You can also disable the BGP router with the *'no bgp router-id A.B.C.D'* or *'no bgp router-id'*. This command defaults the router-id to 0.0.0.0.
 4. The *'no router bgp < asn >'* disables the BGP process with given AS number.

## Setting up the optional configuration ##
To set up the optional configuration, first you need to setup the basic BGP router config with *'router bgp < asn >'*  and  *'bgp router-id A.B.C.D'*. All BGP commands should be executed under **'router bgp < asn >'** context.

 1. **Maximum number of paths:** Limits the maximum number of paths for BGP. If global ECMP is enabled and BGP maximum-paths is set greater than global maximum-paths, then, global overrides BGP maximum-paths. If global ECMP is disabled then only single best path gets selected. Set up the maximum-paths with following commands: *'router bgp < asn >', 'maximum-paths < paths >'.* The *'no maximum-paths'* defaults the number of maximum paths and sets to "1".

 2. **BGP timers:** The *'timers bgp < keepalive > < holdtime >'* sets the keepalive interval and holdtime timer for BGP router.  To set up timers use following commands: *'router bgp < asn >', 'timers bgp < keepalive > < holdtime >'*. Timers can be set to default with 'no timers bgp < keepalive > < holdtime >'*. Default keepalive interval is 180 seconds and holdtime is 60 seconds.

 3. **BGP Network**: To add the static network to BGP routing table, use following command: *'router bgp < asn >', 'network A.B.C.D/M'*. It announces the specified network to all peers in the AS. The 'no network A.B.C.D/M' removes the announced network for this BGP router.

 4. **BGP Peer**: Following  are the neighbor configuration commands.
	 5. Define a new peer with remote-as as < asn > and < peer > is IPv4 address with following command: *'router bgp < asn >',  'neighbor < peer > remote-as < asn >'*. If remote-as is not configured, *bgpd* throws an error as *"can’t find neighbor peer"*. The *'no neighbor peer remote-as asn'*, deletes the peer.
	 6. Set up the peer description using *'router bgp < asn >', 'neighbor < peer > description < some_description>'*. The *'no  neighbor peer description < some_description >'* deletes the neighbor description info.
	 7. Enable MD5 authentication on TCP connection between BGP peers with following commands: *'router bgp < asn >', 'neighbor < peer > password < some_password >'*. The *'no neighbor peer password < some_password >'* disables MD5 authentication on TCP connection between BGP peers.
	 8. Set up the keepalive interval or holdtime timer for a peer with following commands:  *'router bgp < asn >', 'neighbor peer timers < keepalive > < holdtimer >'*. The *'no neighbor peer timers < keepalive > < holdtimer >'* clears the keepalive interval and holdtime timer for that peer.
	 9. Specify the number of times BGP allows an instance of AS to be in the AS_PATH using following command: *'router bgp < asn >', 'neighbor peer allowas-in < ASN_instances_allowed >'*. ASN_instances_allowed range is from 1 to 10. The *'no neighbor peer allowas-in < ASN_instances_allowed >'* prevents the asn to be added to the AS_PATH by setting ASN_instances_allowed to '0'.
	 10. Removes private AS numbers from the AS path in outbound routing updates with following command: *'router bgp < asn >', 'neighbor peer remove-private-AS'*.  The *'no neighbor peer remove-private-AS'* allows the private AS numbers from the AS path in outbound routing updates.
	 11. Enables software-based reconfiguration to generate inbound updates from a neighbor without clearing the BGP session with following command: *'router bgp < asn >', 'neighbor peer soft-reconfiguration inbound'*. The *'no neighbor peer soft-reconfiguration inbound'* disables the software-based reconfiguration.

 5. **BGP Peer-Group**: Peer-group is a collection of peers which shares same outbound policy. Neighbors belonging to the same peer-group might have different inbound policies. All peer commands are applicable to peer-group as well. Following  are the peer-group configuration commands.

	 6. Define a new peer-group with < word > as name of the peer-group using following commands: *'router bgp < asn >', 'neighbor < word > peer-group'*. The 'neighbor < word > peer-group' deletes the peer-group.
	 7. Bind a specific peer to the peer-group provided with following commands: *'router bgp < asn >', 'neighbor peer peer-group word'*

 6. **Peer filtering**
	 7. **Route Map**: Configure the route map for given sequence number with following command: *'route-map < word > (deny|permit) < sequence_num >'* . < word > is a name of route map. < sequence_num > range is from 1 to 65535. The *'no route-map < word > (deny|permit) < sequence_num >'* deletes the route map. All route map commands should be executed under **'route-map < word > (deny|permit) < sequence_num >'** context Following are the route map configuration commands:
		 9. Assign the route map to the peer for given direction with *'route-map < word > (deny|permit) < sequence_num >'* , *'neighbor < peer > route-map < word > in|out'*. The *'no neighbor < peer > route-map < word > in|out'* removes the route map from the peer.
		 10. Add route map description with *'route-map < word > (deny|permit) < sequence_num >'* , *'description < some_route_map_description >'*. The *'no description < some_route_map_description >'* removes the route map description.
		 11. Assigns or changes community for route map with *'route-map < word > (deny|permit) < sequence_num >'* , *'set community .AA:NN additive'*. The *'no set community .AA:NN additive'* removes the community.
		 12. Set or change metric for route map with *'route-map < word > (deny|permit) < sequence_num >'* , *'set metric <0-4294967295>'*. You can use this command consequently to overwrite the previously set metric. The *'no set metric <0-4294967295>'* resets the metric to '0'.
	 1. **IP Prefix List**: Following are the ip prefix list configuration commands:
		 2. Configure the ip prefix-list for given route map with *'ip prefix-list < word > seq <1-4294967295>(deny|permit) (A.B.C.D/M|any)'*. The *'no ip prefix-list < word > seq <1-4294967295> (deny|permit) (A.B.C.D/M|any)'* deletes the ip prefix-list for the given route map.
		 3. Configure prefix-list for match on given IP address with *'match ip address prefix-list < word >'*. The *'no match ip address prefix-list < word >'* removes the rule for match on ip address from the prefix-list.

## Verifying the configuration ##
Use the `show running-config` to verify the configuration. All active configurations are displayed with the show running-config command. See the sample output below:

> s1# show running-config
> Current configuration:
!
ip prefix-list BGP1 seq 5 permit 11.0.0.0/8
ip prefix-list BGP1 seq 6 deny 12.0.0.0/8
!
route-map BGP2 permit 5
     description tsting route map description
     match ip address prefix-list bgp1
     set community 123:345 additive
     set metric 1000
!
router bgp 6001
     bgp router-id 9.0.0.1
     network 11.0.0.0/8
     maximum-paths 5
     timers bgp 3 10
     neighbor openswitch peer-group
     neighbor 9.0.0.2 remote-as 2
     neighbor 9.0.0.2 description abcd
     neighbor 9.0.0.2 password abcdef
     neighbor 9.0.0.2 timers 3 10
     neighbor 9.0.0.2 route-map BGP2 in
     neighbor 9.0.0.2 route-map BGP2 out
     neighbor 9.0.0.2 allowas-in 7
     neighbor 9.0.0.2 remove-private-AS
     neighbor 9.0.0.2 soft-reconfiguration inbound
     neighbor 9.0.0.2 peer-group openswitch
!

## Troubleshooting the configuration ##

The following commands verify the BGP route related information:

The `show ip bgp` verifies that all the routes are advertised from the peers.
> **s1# show ip bgp**
Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
              i internal, S Stale, R Removed
Origin codes: i - IGP, e - EGP, ? - incomplete
Local router-id 9.0.0.2
   Network           Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       9.0.0.1                  0      0      0 1 i
*> 12.0.0.0/8       0.0.0.0                  0      0  32768  i
Total number of entries 2

For more information about a specific peer, use the below `show` command.
> **s1# show ip bgp 11.0.0.0/8**
BGP routing table entry for 11.0.0.0/8
Paths: (1 available, best #1)
AS: 1
    9.0.0.1 from 9.0.0.1
      Origin IGP, metric 0, localpref 0, weight 0, valid, external, best
      Last update: Thu Sep 24 22:45:52 2015

The `show ip bgp summary` command provides peer status and additional neighbor information such as BGP packet statistics, total RIB entries, bgp router-id, local AS number.

>**s1# show ip bgp summary**
BGP router identifier 9.0.0.2, local AS number 2
RIB entries 2
Peers 1
Neighbor             AS MsgRcvd MsgSent Up/Down  State

The `show ip bgp neighbors` command provides detailed information about the neighbor such as neighbor state, description, tcp port number, password (if any), and statistics.

> **s1# show ip bgp neighbors**
  name: 9.0.0.1, remote-as: 1
    state: Established
    description: abcd
    password: abcd
    tcp_port_number: 179
    statistics:
       bgp_peer_dropped_count: 1
       bgp_peer_dynamic_cap_in_count: 0
       bgp_peer_dynamic_cap_out_count: 0
       bgp_peer_established_count: 1
       bgp_peer_keepalive_in_count: 3
       bgp_peer_keepalive_out_count: 4
       bgp_peer_notify_in_count: 0
       bgp_peer_notify_out_count: 1
       bgp_peer_open_in_count: 1
       bgp_peer_open_out_count: 1
       bgp_peer_readtime: 25066
       bgp_peer_refresh_in_count: 0
       bgp_peer_refresh_out_count: 0
       bgp_peer_resettime: 25101
       bgp_peer_update_in_count: 2
       bgp_peer_update_out_count: 2
       bgp_peer_uptime: 25101

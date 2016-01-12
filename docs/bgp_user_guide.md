# BGP

##Contents
   - [Overview](#overview)
   - [Setting up the basic configuration](#setting-up-the-basic-configuration)
   - [Setting up the optional configuration](#setting-up-the-optional-configuration)
   - [Verifying the configuration](#verifying-the-configuration)
   - [Troubleshooting the configuration](#troubleshooting-the-configuration)

## Overview
Border Gateway Protocol (BGP) is most commonly used **inter-AS** (autonomous system) routing protocol. The latest BGP version is 4. **BGP-4** supports Classless Inter-Domain Routing (CIDR). The BGP advertises the routes based on destinations as an IP prefix and not the network "class" within BGP.
BGP is a **path-vector** protocol which provides routing information across various BGP routers to be exchanged using destination-based forwarding. For example: The router sends packets based merely on the destination IP address carried in the IP header of the packet. In most cases, we have multiple routes to the same destination and then BGP decides which route to choose using the path attributes, such as *Shortest AS_Path, Multi_Exit_Disc (Multi-exit discriminator, or MED), Origin, Next_hop, Local_pref,* and so on.
BGP provides routing for routers or switches or both, that can be deployed in ISP, Enterprise, and data centers.

## Setting up the basic configuration
The following is the minimum configuration needed to set up the BGP router. The AS number is unique to the Autonomous system and is used to distinguish between internal or external or both BGP connections. Enter the following commands in the order shown:

- The *`router bgp < asn >`* enables the BGP router for the AS number. The AS numbers range from 1 to 65535.
- Set the  BGP router-id with the following command:
  *`bgp router-id A.B.C.D`*.
  You can also disable the BGP router with the *`no bgp router-id A.B.C.D`* or *`no bgp router-id`*. The command defaults the router-id to 0.0.0.0.

  Note: The *`no router bgp < asn >`* disables the BGP process with given AS number.

## Setting up the optional configuration
To set up the optional configuration:

- Enter the router bgp command with the required AS number. For example:
  *`router bgp < asn >`*
  The *`router bgp < asn >`* command enables the BGP router for the AS number. The AS numbers range from 1 to 65535.

- Set the BGP router id with the following command:
  *`bgp router-id <A.B.C.D>`*
  You can also disable the BGP router with the *`no bgp router-id A.B.C.D`* or *`no bgp router-id` *. This command defaults the router-id to 0.0.0.0.

- Set up the maximum-paths with following commands:
  *`router bgp < asn >`*, *`maximum-paths < paths >`*
  The  Maximum number of paths limits the maximum number of paths for BGP. If global ECMP is enabled and BGP maximum-paths is set greater than global maximum-paths, then, global overrides BGP maximum-paths. If global ECMP is disabled then only single best path gets selected. BGP multiple-paths carries risks of routing oscillations, if  MED, IGP costs, and how the BGP and IGP topologies are not cautiously considered. Since AS path, community and extended community are the aggregated attributes of the multi-path routes, BGP multi-pathing results in the propagated route having the attributes of the 'best route' of the multi-path.
  The *`no maximum-paths`* defaults the number of maximum paths and sets to "1".

- Set up timers use following commands:
  *`router bgp < asn >`*, *`timers bgp < keepalive > < holdtime >`*.
  The *`timers bgp < keepalive > < holdtime >`* sets the keepalive interval and holdtime timer for BGP router.
  Timers can be set to default with `no timers bgp < keepalive > < holdtime >`*. The default keepalive interval is 180 seconds and holdtime is 60 seconds.

- To add the static network to BGP routing table, enter following command:
  *`router bgp < asn >`*, *`network A.B.C.D/M`*.
  It announces the specified network to all peers in the AS. The `no network A.B.C.D/M` removes the announced network for this BGP router.

- To advertise the IPv6 prefix network:
  *`router bgp < asn >`*, *`network < ipv6 >`*.
  Use this command in router configuration mode to advertise the specified prefix into the IPv6 BGP database.
  The *`no network < ipv6 >`* is to stop advertising the specified prefix into the IPv6 BGP database.

- To enable fast external failover for BGP directly connected peering sessions:
  *`router bgp < asn >`*, *`bgp fast-external-failover`*.
  Use this command in router configuration mode to terminate external BGP sessions of any directly adjacent peer if the link used to reach the peer goes down, without waiting for the hold-down timer to expire.
  The *`no bgp fast-external-failover`* is to disable the BGP fast external failover.

- To enable logging of BGP neighbor status changes:
  *`router bgp < asn >`*, *`bgp log-neighbor-changes`*.
  Use this command in router configuration mode to log changes in the status of BGP neighbors (up, down, reset).
  The *`no bgp log-neighbor-changes`* is used to disallow  to log changes in the status of BGP neighbors.

- Enter the following neighbor configuration commands in the order shown:

        - Define a new peer with remote-as as < asn > and < peer > is IPv4 address with the following command:
          *`router bgp < asn >`*,  *`neighbor < peer > remote-as < asn >`*.
          If remote-as is not configured, *bgpd* throws an error as 'can’t find neighbor peer'.
          The *`no neighbor peer`* deletes the peer.

        - Set up the peer description with the following command:
          *`router bgp < asn >`*, *`neighbor < peer > description < some_description>`*.
          The *`no  neighbor peer description`* deletes the neighbor description info.

        - Enable MD5 authentication on TCP connection between BGP peers with the following command:
          *`router bgp < asn >`*, *`neighbor < peer > password < some_password >`*.
          The *`no neighbor peer password < some_password >`* disables MD5 authentication on TCP connection between BGP peers.

        - Set up the keepalive interval or holdtime timer for a peer with the following command:
          *`router bgp < asn >`*, *`neighbor peer timers < keepalive > < holdtimer >`*.
          The *`no neighbor peer timers < keepalive > < holdtimer >`* clears the keepalive interval and holdtime timer for that peer.

        - Specify the number of times BGP allows an instance of AS to be in the AS_PATH using following command:
          *`router bgp < asn >`*, *`neighbor peer allowas-in < ASN_instances_allowed >`*.
          The ASN_instances_allowed range is from 1 to 10.
          The *`no neighbor peer allowas-in < ASN_instances_allowed >`* prevents the asn to be added to the AS_PATH by setting ASN_instances_allowed to '0'.

        - Removes private AS numbers from the AS path in outbound routing updates with the following command: *`router bgp < asn >`*, *`neighbor peer remove-private-AS`*.
          The *`no neighbor peer remove-private-AS`* allows the private AS numbers from the AS path in outbound routing updates.

        - Enables software-based reconfiguration to generate inbound updates from a neighbor without clearing the BGP session with the following command:
          *`router bgp < asn >`*, *`neighbor peer soft-reconfiguration inbound`*.
          The *`no neighbor peer soft-reconfiguration inbound`* disables the software-based reconfiguration.

        - Set the advertisement interval for route updates for specified neighbor/peer with ipv4 and ipv6 address. Default value is set to 30 seconds.
          *`router bgp < asn >`*, *`neighbor peer advertisement-interval <interval>`*.
          The time interval for sending BGP routing updates is in range <0-600> secs. The *`no neighbor peer advertisement-interval <interval>`* unsets advertisement interval   for route updates for specified neighbor/peer with ipv4 and ipv6  address.

        - Configure filter-list on the neighbor to filter incoming and outgoing routes using the following commands.
          *`router bgp < asn >`, `neighbor <A.B.C.D|X:X::X:X|WORD> filter-list WORD (in|out)`*
          The *`no neighbor <A.B.C.D|X:X::X:X|WORD> filter-list WORD (in|out)`* uninstalls the filter-list.

        - Apply prefix-list on the neighbor to filter updates to and from the neighbor using the following commands.
          *`router bgp < asn >`, `neighbor (A.B.C.D|X:X::X:X|WORD) prefix-list WORD (in|out)`*
          The *`no neighbor (A.B.C.D|X:X::X:X|WORD) prefix-list WORD (in|out)`* uninstalls the applied prefix-list.

        - Allow inbound soft reconfiguration for a neighbor using the following command.
          *`router bgp < asn >`, `neighbor (A.B.C.D|X:X::X:X|WORD) soft-reconfiguration inbound`*
          The *`no neighbor (A.B.C.D|X:X::X:X|WORD) soft-reconfiguration inbound`* disables the inbound soft reconfiguration.

        - Specify the maximum number of hops to the BGP peer using the following command.
          *`router bgp < asn >`, `neighbor (A.B.C.D|X:X::X:X|WORD) ttl-security hops <1-254>`*
          The *`no neighbor (A.B.C.D|X:X::X:X|WORD) ttl-security hops <1-254>`* disables the maximum number of hops specification.

        - Specify the source address to use for the BGP session to the neighbour.
          *`router bgp < asn >`, `neighbor (A.B.C.D|X:X::X:X|WORD) update-source (A.B.C.D|X:X::X:X|WORD)`*
          The *`neighbor (A.B.C.D|X:X::X:X|WORD) update-source (A.B.C.D|X:X::X:X|WORD)`* removes the source address.

- Peer-group is a collection of peers which shares same outbound policy. Neighbors belonging to the same peer-group might have different inbound policies. All peer commands are applicable to peer-group as well. Following  are the peer-group configuration commands.Enter the following BGP Peer-Group commands in the order shown:

        - Define a new peer-group with < word > as name of the peer-group using the following command:
          *`router bgp < asn >`, `neighbor < word > peer-group`*.
          The `neighbor < word > peer-group` deletes the peer-group.
        - Bind a specific peer to the peer-group provided with the following command:
          *`router bgp < asn >`, `neighbor peer peer-group word`*.

- Following are the route map configuration commands:

        - Configure the peer filtering route map for given sequence number with the following command:
          *`route-map < word > (deny|permit) < sequence_num >`*.
          The variable < word > is a name of route map and the variable < sequence_num > range is from 1 to 65535. The *`no route-map < word > (deny|permit) < sequence_num >`* deletes the route map. All route map commands should be executed under *`route-map < word > (deny|permit) < sequence_num >`* context.

        - Assign the route map to the peer for given direction with the following command:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`neighbor < peer > route-map  <word > in|out`*.
          The *`no neighbor < peer > route-map < word > in|out`* removes the route map from the peer.

        - Add route map description with the following command:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`description < some_route_map_description >`*.

        - Assigns or changes community for route map with the following command:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set community .AA:NN additive`*.
          The *`no set community .AA:NN additive`* removes the community.

        - Set or change metric for route map with the following command:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set metric <0-4294967295>`*.
          You can use this command consequently to overwrite the previously set metric. The *`no set metric <0-4294967295>`* resets the metric to `0`.

        - Set the originating AS of an aggregated route.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set aggregator as <value> <set-aggregator-ip>`*.
          The value specifies at which AS the aggregate route originated. The range is from 1-4294967295. The set-aggregator-ip value must also be set to further identify the originating AS.
          The *`no set aggregator as <value> <set-aggregator-ip>`* removes the aggregator entry.

        - Exclude the given AS number from the AS_PATH
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set as-path exclude <value>`*.
          The value specifies the AS to be excluded. The range is from 1-4294967295.
          The *`no set as-path exclude <value>`* removes the AS from exclusion list.

        - Prepend the given AS number to AS_PATH
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set as-path prepend <value>`*.
          The value specifies the AS to be prepended to AS path. The range is from 1-4294967295.
          The *`no set as-path prepend <value>`* removes the AS from AS path.

        - Enable warning to upstream routers through the ATOMIC_AGGREGATE attribute that address aggregation has occurred on an aggregate route.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set atomic-aggregate`*.
          The *`no set atomic-aggregate`* disables warnings to upstream neighbor about route aggregation.

        - This command removes the COMMUNITY attributes from the BGP routes identified in the specified community list. Deletes matching communities for route-map.
          Prerequisites: community-list needs to be configured as below:
          *`ip community-list <1-99> (deny|permit) .AA:NN`*
          *`ip community-list <100-500> (deny|permit) .LINE`*
          Communities can be set for route map using the following.
          *`set community .AA:NN`*
          *`set extcommunity rt .ASN:nn_or_IP-address:nn`*
          *`set extcommunity soo .ASN:nn_or_IP-address:nn`*
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set comm-list <value> delete`*.
          Value could be standard community in range <1-99> or extended community in range <100-500> or a community name.
          The *`no set comm-list <value> delete`* removes communities in route-map matching the ones in community list from deleted communities list.

        - Set COMMUNITY attributes for the route-map.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set community <community-number>`*.
          Community number is in aa:nn format or local-AS|no-advertise|no-export|internet or additive or none.
          The *`no set community <community-number>`* removes community attribute for route-map.

        - Set the target extended community (in decimal notation) of a BGP route.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set extcommunity rt <asn-community-identifier>`*.
          The <asn-community-identifier> attribute value has the syntax AA:NN, where AA represents an AS, and NN is the community identifier.
          The *`no set extcommunity rt <asn-community-identifier>`* unsets target extended community for route-map.

        - Set the site-of-origin extended community (in decimal notation) of a BGP route.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set extcommunity soo <asn-community-identifier>`*.
          The <asn-community-identifier> attribute value has the syntax AA:NN, where AA represents an AS, and NN is the community identifier.
          The *`no set extcommunity soo <asn-community-identifier>`* unsets site-of-origin extended community for route-map.

        - Set the ip address for next-hop.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set ip next-hop <peer-ipv4-address>`*.
          The *`no set ip next-hop <peer-ipv4-address>`* removes next-hop peer entry from route-map.

        - Enables iBGP learn router to forward the packet to its peer address instead of the external router IP address.
          In BGP routing protocol, the update from the external AS will contain the next hop address of the external hop itself. Therefore, when the router receives the update from the external AS and advertises the update to the other routers via iBGP, the other routers will see the next hop of the advertised networks via the external router IP address.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set ip next-hop peer-address`*.
          The *`no set ip next-hop peer-address`* prevents forwarding BGP route update packets to peer as next-hop.

        - Set BGP-4+ global IPv6 nexthop address.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set ipv6 next-hop global <ipv6-address>`*.
          ipv6 address is of the form X:X::X:X
          The *`no set ipv6 next-hop global <ipv6-address>`* unsets IPv6 nexthop address.

        - Set BGP-4+ link-local IPv6 nexthop address.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set ipv6 next-hop link-local <ipv6-address>`*.
          ipv6 address is of the form X:X::X:X. The *`no set ipv6 next-hop link-local <ipv6-address>`* unsets IPv6 link-local nexthop address.

        - Set the local preference value of an IBGP route. The value is advertised to IBGP peers.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set local-preference <value>`*.
          The <value> attribute range is from 0 to 4294967295. A higher number signifies a preferred route among multiple routes to the same destination.
          The *`no set local-preference <value>`* resets local-preference value for the route to 0.

        - Specify the relative change of metric which is used with BGP route advertisement.
          It can take the current metric of a route and increase or decrease it by a specified value before it propagates it.
          If the value is specified as negative and ends up being negative after metric decrease, the value would be interpreted as an increase in metric.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set metric <expr>`*.
          `expr` attribute is the metric expression to increment/decrement metric of a route using +/-<metric-value>.
          The *`no set metric <expr>`* is a no-op. The metric has to be reset using `set metric <expr>` or `set metric <metric-value>` commands.

        - Set metric value for the route which is used with BGP route advertisement.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set metric <value>`*.
          `value` attribute is in range 0 - 4294967295.
          The *`no set metric <value>`* resets the metric to 0 for the route.

        - Set the metric type for the destination routing protocol.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set metric <type>`*.
          `type` attribute is either type-1 or type-2.
          The *`no set metric <type>`* unsets the metric typei for route-map.

        - Set the ORIGIN attribute of a local BGP route to one of the following:
          egp, igp or incomplete
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set origin <origin-type>`*.
          *`origin-type`* attribute is one of the following:
          *`egp`* attribute -  sets the value to the NLRI learned from the Exterior Gateway Protocol (EGP).
          *`igp`* attribute -  sets the value to the NLRI learned from a protocol internal to the originating AS.
          *`incomplete`* attribute -  if not egp or igp.
          The *`no set origin <origin-type>`* unsets set origin-type.

        - Set the ORIGINATOR_ID attribute, which is equivalent to the router-id of the originator of the route in the local AS.
          Route reflectors use this value to prevent routing loops.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set originator-id <ipv4-address>`*.
          The *`no set originator-id <ipv4-address>`* unsets originator-id for route-map.

        - Set the preferred source address for matching routes when installing in the kernel, within a route-map.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set src <ipv4-address>`*.
          The *`no set src <ipv4-address>`* unsets preferred source address for matching routes in the kernel.

        - Set the tag for redistributions, that external routers use to filter incoming distributions of route-maps.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set tag <value>`*.
          `value` attribute is in range 0 - 65535.
          The *`no set tag <value>`* unsets the tag value for route-map.

        - Set next-hop ip address for vpnv4 updates.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set vpnv4 next-hop <ipv4-address>`*.
          The *`no set vpnv4 next-hop <ipv4-address>`* unsets vpnv4 next-hop ip address.

        - Set the weight of a BGP route. A routes weight has the most influence when two identical BGP routes are compared. A higher number signifies a greater preference.
          *`route-map < word > (deny|permit) < sequence_num >`* , *`set weight <value>`*.
          `value` attribute is in range 0 - 4294967295.
          The *`no set weight <value>`* unsets the weight value for route-map.

        - To match BGP AS path access list for route map:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match as-path WORD`*.
          Use this command in route map configuration mode to match a BGP autonomous system path access list.
          The *`no match as-path WORD`* removes the AS path access list entry.

        - To match a BGP community:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match community (<1-99>|<100-500>|WORD)`*.
          Use this command in route map configuration mode to match a BGP community.
          The *`no match community (<1-99>|<100-500>|WORD)`* removes the match community entry.

        - To match a BGP community with an exact-match:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match community (<1-99>|<100-500>|WORD) exact-match`*.
          Use this command in route map configuration mode to match a BGP community with an exact match of communities.
          The *`no match community (<1-99>|<100-500>|WORD) exact-match`* removes the match entry for exact match community.

        - To match BGP extended community list:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match extcommunity (<1-99>|<100-500>|WORD)`*.
          Use this command in route map configuration mode to match BGP extended community list attributes.
          The *`no match extcommunity (<1-99>|<100-500>|WORD)`* removes the BGP extended community list attribute entry.

        - To match an interface:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match interface WORD`*.
          Use this command in route map configuration mode to distribute routes that have their nexthop out of the interface specified.
          The *`no match interface WORD`* removes the match interface entry.

        - To match an IP address:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match ip address (<1-199>|<1300-2699>|WORD)`*.
          Use this command in route map configuration mode to distribute any routes that have a destination network address that is permitted by a standard or extended access list.
          The *`no match ip address (<1-199>|<1300-2699>|WORD)`* removes the match ip address entry.

        - To match an IP address prefix list:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match ip address prefix-list WORD`*.
          Use this command in route map configuration mode to distribute any routes that have a destination network address that is permitted by a prefix list.
          The *`no match ip address prefix-list WORD`* removes the match ip address prefix list entry.

        - To match an IP nexthop:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match ip next-hop (<1-199>|<1300-2699>|WORD)`*.
          Use this command in route map configuration mode to redistribute any routes that have a next hop router address passed by one of the access lists specified.
          The *`no match ip next-hop (<1-199>|<1300-2699>|WORD)`* removes the match ip next-hop entry.

        - To match an IP nexthop prefix list:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match ip next-hop prefix-list WORD`*.
          Use this command in route map configuration mode to redistribute any routes that have a next hop router address passed by one of the prefix lists specified.
          The *`no match ip next-hop prefix-list WORD`* removes the match ip next hop prefix list entry.

        - To match an IP route source:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match ip route-source (<1-199>|<1300-2699>|WORD)`*.
          Use this command in route map configuration mode to redistribute routes that have been advertised by routers and access servers at the address specified by the access lists.
          The *`no match ip route-source (<1-199>|<1300-2699>|WORD)`* removes the match ip route source entry.

        - To match an IP route source prefix list:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match ip route-source prefix-list WORD`*.
          Use this command in route map configuration mode to redistribute routes that have been advertised by routers and access servers at the address specified by the prefix lists.
          The *`no match ip route-source prefix-list WORD`* removes the match route source prefix list entry.

        - To match an IPv6 address:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match ipv6 address WORD`*.
          Use this command in route map configuration mode to distribute IPv6 routes that have a prefix specified by an IPv6 access list.
          The *`no match ipv6 address WORD`* removes the match ipv6 address entry.

        - To match an IPv6 address prefix list:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match ipv6 address prefix-list WORD`*.
          Use this command in route map configuration mode to distribute IPv6 routes that have a prefix specified by an IPv6 prefix list.
          The *`no match ipv6 address prefix-list`* removes the match ipv6 address prefix list entry.

        - To match an ipv6 next hop:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match ipv6 next-hop X:X::X:X`*.
          Use this command in route map configuration mode to distribute IPv6 routes that have a specific next hop.
          The *`no match ipv6 next-hop X:X::X:X`* removes the match ipv6 next hop entry.

        - To match a metric:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match metric <0-4294967295>`*.
          Use this command in route map configuration mode to distribute routes with the metric specified.
          The *`no match metric <0-4294967295>`* removes the match metric entry.

        - To match an origin:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match origin (egp|igp|incomplete)`*.
          Use this command in route map configuration mode to match BGP routes based on the origin of the route specified.
          The *`no match origin (egp|igp|incomplete)`* removes the match origin entry.

        - To match a peer:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match peer (A.B.C.D|X:X::X:X)`*.
          Use this command in route map configuration mode to match BGP routes based on the peer address.
           The *`no match peer (A.B.C.D|X:X::X:X)`* removes the match peer entry.

        - To match a peer local:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match peer local`*.
          Use this command in route map configuration mode to match BGP routes against static or redistributed routes.
          The *`no match peer local`* removes the match peer entry.

        - To match probability:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match probability <0-100>`*.
          Use this command in route map configuration mode to match portion of BGP routes defined by percentage value.
          The *`no match probability`* removes the match probability entry.

        - To match tag:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`match tag <0-65535>`*.
          Use this command in route map configuration mode to match tag value of route.
          The *`no match tag <0-65535>`* removes the match tag entry.

        - To initialize exit policy to goto:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`on-match goto <0-65535>`*.
          Use this command in route map configuration mode to initialize exit policy on matches to goto clause.
          The *`no match tag <0-65535>`* deinitialize exit policy.

        - To initialize exit policy to next:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`on-match next`*.
          Use this command in route map configuration mode to initialize exit policy on matches to next clause.
          The *`no match tag <0-65535>`* deinitialize exit policy.

        - To jump to another route map:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`call WORD`*.
          Use this command in route map configuration mode to jump to another route-map after match and set.
          The *`no call WORD`* disables jumping to another route-map.

        - To continue on a different entry:
          *`route-map < word > (deny|permit) < sequence_num >`* , *`continue <1-65535>`*.
          Use this command in route map configuration mode to continue on a different entry.
          The *`no call WORD`* disables continuing on a different entry

- Enter the following peer filtering ip perfix-list commands as order shown:

        - Configure the ip prefix-list for given route map with the following command:
          *`ip prefix-list WORD seq <1-4294967295>(deny|permit) (A.B.C.D/M|any)`*.
          The *`no ip prefix-list < word > seq <1-4294967295> (deny|permit) (A.B.C.D/M|any)`* deletes the ip prefix-list for the given route map.

        - Configure the ip prefix-list for given route map with prefix length specification using one of the following commands:
          *`ip prefix-list WORD seq <1-4294967295> deny|permit <A.B.C.D/M> ge <length>`*
          *`ip prefix-list WORD seq <1-4294967295> deny|permit <A.B.C.D/M> ge <length> le <length>`*.
          *`ip prefix-list WORD seq <1-4294967295> deny|permit <A.B.C.D/M> le <length>`*.
          The *`no ip prefix-list WORD`* deletes the ip prefix-list for the given route map.


        - Configure the ipv6 prefix-list for given route map with the following commands:
          *`ipv6 prefix-list WORD seq <1-4294967295> deny|permit <X:X::X:X/M|any>`*
          The *`no ipv6 prefix-list WORD`* deletes the ipv6 prefix-list for the given route map.

        - Configure the ipv6 prefix-list for the given route map with the prefix list description using the following command:
          *`ipv6 prefix-list WORD description .LINE`* .
          The *`no ipv6 prefix-list WORD`* deletes the ipv6 prefix-list for the given route map.

        - Configure the ipv6 prefix-list for given route map with prefix length specification using one of the following commands:
          *`ipv6 prefix-list WORD seq <1-4294967295> deny|permit <X:X::X:X/M> ge <length>`*
          *`ipv6 prefix-list WORD seq <1-4294967295> deny|permit <X:X::X:X/M> ge <length> le <length>`*.
          *`ipv6 prefix-list WORD seq <1-4294967295> deny|permit <X:X::X:X/M> le <length>`*.
          The *`no ipv6 prefix-list WORD`* deletes the ipv6 prefix-list for the given route map.

- Configure as path access-lists using the following :
  Facilitate configuration of access lists based on autonomous system path that enable to control routing updates based on BGP autonomous paths information. Access lists are filters that enable to restrict the routing information a router learns or advertises to and from a neighbor. Multiple BGP peers or route maps can reference a single access list. These access lists can be applied to both inbound route updates and outbound route updates. Each route update is passed through the access-list. BGP applies each rule in the access list in the order it appears in the list. When a route matches any rule, the decision to permit the route through the filter or deny is made, and no further rules are processed.

  *`ip as-path access-list WORD  <deny | permit> .LINE`*
  LINE is a pattern used to match against an input string. In BGP, one can build a regular expression to match information about an autonomous system path. The *`no ip as-path access-list WORD <deny|permit> .LINE`* disables access-list configuration for as-path.

- Define a new community list as shown:
          The community is compiled into community structure. We can define multiple community list under same name. In that case match will happen user defined order. Once the community list matches to communities attribute in BGP updates it return permit or deny by the community list definition. When there is no matched entry, deny will be returned. When community is empty it matches to any routes.
          *`ip  community-list WORD <deny|permit> .LINE`*
          *`,LINE`* is a string expression of communities attribute --> [1-2]00 , ^0:.*_, .*
          *`WORD`* is a string.
          The *`no ip  community-list expanded WORD <deny|permit> .LINE`* disables community list for configured communities.

- Enter the following extended community lists definition commands as shown:
          Configure the extended community list with the following command:
          *`ip extcommunity-list  WORD <deny|permit> .LINE`*.
          The *`no ip extcommunity-list  WORD`* command deletes the extended community list.

- Configure prefix-list for match on given IP address with the following command:
          *`match ip address prefix-list < word >`*.
          The *`no match ip address prefix-list < word >`* removes the rule for match on ip address from the prefix-list.

- The command *`neighbor <ipv4_address | ipv6_address | peer_group_name> ebgp-multihop`* attempts to connect to the external Autonomous System routers which are not directly connected. It take either IPv4/IPv6 address or the peer-group name to establish a connection.
  To remove the ebgp-multihop configuration, use the *`no neighbor <ipv4_address | ipv6_address | peer_group_name> ebgp-multihop`* command.


## Verifying the configuration
Use the *`show running-config`* to verify the configuration. All active configurations are displayed with the show running-config command. See the sample output below:

```
          s1# show running-config
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
```

## Troubleshooting the configuration

The following commands verify the BGP route related information:

- The *`show ip bgp`* verifies that all the routes are advertised from the peers.

```
          s1# show ip bgp
          Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
                        i internal, S Stale, R Removed
          Origin codes: i - IGP, e - EGP, ? - incomplete
          Local router-id 9.0.0.2
          Network             Next Hop            Metric LocPrf Weight Path
          *> 11.0.0.0/8       9.0.0.1                  0      0      0 1 i
          *> 12.0.0.0/8       0.0.0.0                  0      0  32768  i
          Total number of entries 2
```

- For more information about a specific peer, use the below `show` command.

```
          s1# show ip bgp 11.0.0.0/8
          BGP routing table entry for 11.0.0.0/8
          Paths: (1 available, best #1)
          AS: 1
              9.0.0.1 from 9.0.0.1
          Origin IGP, metric 0, localpref 0, weight 0, valid, external, best
          Last update: Thu Sep 24 22:45:52 2015
```

- The *`show ip bgp summary`* command provides peer status and additional neighbor information such as BGP packet statistics, total RIB entries, bgp router-id and local AS number.

```
          s1# show ip bgp summary
          BGP router identifier 9.0.0.2, local AS number 2
          RIB entri es 2
          Peers 1
          Neighbor             AS MsgRcvd MsgSent Up/Down  State
```
- The *`show ip bgp neighbors`* command provides detailed information about the neighbor such as neighbor state, description, tcp port number, password (if any), and statistics.

```
          s1# show ip bgp neighbors
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
```

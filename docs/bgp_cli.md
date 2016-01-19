#BGP Command Reference
=======================

##Contents
- [BGP configuration commands](#bgp-configuration-commands)
	- [router bgp](#router-bgp)
	- [bgp router-id](#bgp-router-id)
	- [IPv4 network](#ipv4-network)
	- [maximum-paths](#maximum-paths)
	- [timers bgp](#timers-bgp)
	- [IPv6 network](#ipv6-network)
	- [bgp fast-external-failover](#bgp-fast-external-failover)
	- [bgp log-neighbor-changes](#bgp-log-neighbor-changes)
	- [redistribute routes](#redistribute-routes)
	- [BGP neighbor commands](#bgp-neighbor-commands)
		- [neighbor remote-as](#neighbor-remote-as)
		- [neighbor description](#neighbor-description)
		- [neighbor password](#neighbor-password)
		- [neighbor timers](#neighbor-timers)
		- [neighbor allowas-in](#neighbor-allowas-in)
		- [neighbor remove-private-AS](#neighbor-remove-private-as)
		- [neighbor soft-reconfiguration inbound](#neighbor-soft-reconfiguration-inbound)
		- [neighbor shutdown](#neighbor-shutdown)
		- [neighbor peer-group](#neighbor-peer-group)
		- [neighbor route-map](#neighbor-route-map)
		- [neighbor advertisement-interval](#neighbor-advertisement-interval)
		- [neighbor ebgp-multihop](#neighbor-ebgp-multihop)
		- [neighbor filter-list](#neighbor-filter-list)
		- [neighbor prefix-list](#neighbor-prefix-list)
		- [neighbor soft-reconfiguration](#neighbor-soft-reconfiguration)
		- [neighbor ttl-security](#neighbor-ttl-security)
		- [neighbor update-source](#neighbor-update-source)
	- [as-path access-list](#as-path-access-list)
- [Route-map configuration commands](#route-map-configuration-commands)
	- [route-map](#route-map)
	- [Route-map match](#route-map-match)
		- [match prefix-list](#match-prefix-list)
		- [match as-path](#match-as-path)
		- [match community](#match-community)
		- [match community exact-match](#match-community-exact-match)
		- [match  extcommunity](#match-extcommunity)
		- [match interface](#match-interface)
		- [match ip address](#match-ip-address)
		- [match ip address prefix-list](#match-ip-address-prefix-list)
		- [match ip next-hop](#match-ip-nexthop)
		- [match ip next-hop prefix-list](#match-ip-nexthop-prefix-list)
		- [match ip route-source](#match-ip-route-source)
		- [match ip route-source prefix-list](#match-ip-route-source-prefix-list)
		- [match ipv6 address](#match-ipv6-address)
		- [match ipv6 address prefix-list](#match-ipv6-address-prefix-list)
		- [match ipv6 next-hop](#match-ipv6-next-hop)
		- [match metric](#match-metric)
		- [match origin](#match-origin)
		- [match peer](#match-peer)
		- [match peer local](#match-peer-local)
		- [match probability](#match-probability)
		- [match tag](#match-tag)
		- [on-match goto](#on-match-goto)
		- [on-match next](#on-match-next)
	- [Route-map set](#route-map-set)
		- [set aggregator](#set-aggregator)
		- [set as-path exclude](#set-as-path-exclude)
		- [set as-path prepend](#set-as-path-prepend)
		- [set atomic-aggregate](#set-atomic-aggregate)
		- [set comm-list delete](#set-comm-list-delete)
		- [set community](#set-community)
		- [set community rt](#set-community-rt)
		- [set extcommunity soo](#set-extcommunity-soo)
		- [set ip next-hop](#set-ip-next-hop)
		- [set ip next-hop peer-address](#set-ip-next-hop-peer-address)
		- [set ipv6 next-hop global](#set-ipv6-next-hop-global)
		- [set ipv6 next-hop local](#set-ipv6-next-hop-local)
		- [set local-preference](#set-local-preference)
		- [set metric](#set-metric)
		- [set metric-type](#set-metric-type)
		- [set origin](#set-origin)
		- [set originator-id](#set-originator-id)
		- [set src](#set-src)
		- [set tag](#set-tag)
		- [set vpnv4 next-hop](#set-vpnv4-next-hop)
		- [set weight](#set-weight)
	- [Route-map description](#route-map-description)
	- [Route-map call](#route-map-call)
	- [Route-map continue](#route-map-continue)
- [IP prefix-list configuration commands](#ip-prefix-list-configuration-commands)
	- [IPv4 prefix-list](#ipv4-prefix-list)
	- [IPv6 prefix-list](#ipv6-prefix-list)
- [Community lists configuration commands](#community-lists-configuration-commands)
- [Extended community lists configuration commands](#extended-community-lists-configuration-commands)
- [Display commands](#display-commands)
	- [show ip bgp](#show-ip-bgp)
	- [show ip bgp summary](#show-ip-bgp-summary)
	- [show bgp neighbors](#show-bgp-neighbors)

## BGP configuration commands

### router bgp

To use the BGP feature, first configure the BGP router as shown below.

#### Syntax
```
[no] router bgp <asn>
```

#### Description
This command is used to configure the BGP router. The Autonomous System (AS) number is needed to configure the BGP router. The BGP protocol uses the AS number to detect whether the BGP connection is internal or external.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *asn*  | Required | 1 - 4294967295 | The AS number. |
| **no** | Optional | Literal | Destroys a BGP router with the specified AS number. |

#### Examples
```
s1(config)#router bgp 6001
s1(config)#no router bgp 6001
```

### bgp router-id
#### Syntax
```
[no] bgp router-id <A.B.C.D>
```

#### Description
This command specifies the BGP router-ID for a BGP router.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The IPv4 address. |
| **no** | Optional | Literal | Deletes the BGP router IP address. |

#### Examples
```
s1(config-router)# bgp router-id 9.0.0.1
s1(config-router)# no bgp router-id 9.0.0.1
```

### IPv4 network
#### Syntax
```
[no] network <A.B.C.D/M>
```

#### Description
This command adds the announcement network.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D/M*  | Required | A.B.C.D/M | IPv4 address with the prefix length.|
| **no** | Optional | Literal | Removes the announced network for the BGP router. |

#### Examples
The following configuration example shows that network 10.0.0.0/8 is announced to all neighbors:

```
s1(config-router)# network 10.0.0.0/8
s1(config)# do sh run
Current configuration:
!
router bgp 6001
     bgp router-id 9.0.0.1
     network 10.0.0.0/8
```

### maximum-paths
#### Syntax
```
[no] maximum-paths <num>
```

#### Description
This command sets the maximum number of paths for a BGP router.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *num*  | Required | 1-255 | Maximum number of paths. |
| **no** | Optional | Literal | Sets the maximum number of paths to the default value of 1. |


#### Examples
```
s1(config)# router bgp 6001
s1(config-router)# maximum-paths 5
```

### timers bgp
#### Syntax
```
[no] timers bgp <keepalive> <holdtime>
```

#### Description
This command sets the keepalive interval and hold time for a BGP router.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *Keepalive*  | Required | 0 - 65535 | The keepalive interval in seconds. |
| *holdtime* | Required| 0 - 65535 | Hold time in seconds. |
| **no** | Optional | Literal | Resets the keepalive and hold time values to their default values (60 seconds for the keepalive interval and 180 seconds for the hold time value).  |

#### Examples
```
s1(config)# router bgp 6001
s1(config-router)# timers bgp 60 30
```

### IPv6 network
#### Syntax
```
[no] network <X:X::X:X/M>
```

#### Description
This command advertises the IPv6 prefix network.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *X:X::X:X/M*  | Required | X:X::X:X/M | The IPv6 prefix address and prefix length. |
| **no** | Optional | Literal | Deletes the IPv6 prefix network. |

#### Examples
```
s1(config-router)# ipv6 bgp network 2001:1::1/64
s1(config-router)# no ipv6 bgp network 2001:1::1/64
```

### bgp fast-external-failover
#### Syntax
```
[no] bgp fast-external-failover
```

#### Description
This command is used to enable fast external failover for BGP directly connected peering sessions.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Disables BGP fast external failover. |

#### Examples
```
s1(config-router)# bgp fast-external-failover
s1(config-router)# no bgp fast-external-failover
```

### bgp log-neighbor-changes
#### Syntax
```
[no] bgp log-neighbor-changes
```

#### Description
This command enables logging of BGP neighbor resets and status changes (up and down).

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The IPv4 address. |
| **no** | Optional | Literal | Disables the logging of neighbor status changes. |

#### Examples
```
s1(config-router)# bgp log-neighbor-changes
s1(config-router)# no bgp log-neighbor-changes
```

### redistribute routes
#### Syntax
```
[no] redistribute <kernel | connected | static | rip | ospf | isis | babel> route-map <name>
```
#### Description
This command configures the route redistribution of the specified protocol or kind into BGP; filtering the routes using the given route-map, if specified.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *name*  | Optional | String of maximum length 80 characters. | The route-map name. |
| **no** | Optional | Literal | Removes the redistribution of routes from BGP. |

#### Examples
```
s1(config)# router bgp 6001
s1(config-router)# redistribute kernel
s1(config-router)# redistribute connected
s1(config-router)# redistribute static
s1(config-router)# redistribute ospf
s1(config-router)# redistribute kernel route-map rm1
s1(config-router)# redistribute connected route-map rm1
s1(config-router)# redistribute static route-map rm1
s1(config-router)# redistribute ospf route-map rm1
```

### BGP neighbor commands
#### neighbor remote-as

##### Syntax
```
[no] neighbor <A.B.C.D> remote-as <asn>
```

##### Description
This command creates a neighbor whose remote-as is *asn*, an autonomous system number. Currently only IPv4 addresses are supported.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| *asn* | Required| 1 - 4294967295 |  The autonomous system number of the peer. |
| **no** | Optional | Literal | Deletes a configured BGP peer. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# no neighbor 9.0.0.2 remote-as 6002
```

#### neighbor description
##### Syntax
```
[no] neighbor <A.B.C.D> description <text>
```

##### Description
This command sets the description for the peer.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| *text* | Required| String of maximum length 80 characters. | Description of the peer. |
| **no** | Optional | Literal | Deletes the peer description. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 description peer1
```

#### neighbor password
##### Syntax
```
[no] neighbor <A.B.C.D> password <text>
```

##### Description
This command enables MD5 authentication on a TCP connection between BGP peers.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| *text* | Required| String of maximum length 80 characters. | Password for the peer connection. |
| **no** | Optional | Literal | Disables authentication for the peer connection. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 password secret
```

#### neighbor timers
##### Syntax
```
[no] neighbor <A.B.C.D> timers <keepalive> <holdtimer>
```

##### Description
This command sets the keepalive interval and hold time for a specific BGP peer.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *Keepalive*  | Required | 0 - 65535 | The keepalive interval in seconds. |
| *holdtime* | Required| 0 - 65535 | The hold time in seconds. |
| **no** | Optional | Literal | Resets the keepalive and hold time values to their default values which are 0.  |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 timers 20 10
```

#### neighbor allowas-in
##### Syntax
```
[no] neighbor <A.B.C.D> allowas-in <val>
```

##### Description
This command specifies an allow-as-in occurrence number for an AS to be in the AS path. Issue the `no` command to clear the state.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| *val* | Required| 1-10| Number of times BGP allows an instance of AS to be in the AS_PATH. |
| **no** | Optional | Literal | Clears the state. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 allowas-in 2
```

#### neighbor remove-private-AS

##### Syntax
```
[no] neighbor <A.B.C.D> remove-private-AS
```

##### Description
This command removes private AS numbers from the AS path in outbound routing updates.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| **no** | Optional | Literal |Resets to a cleared state (default). |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 remove-private-AS
```

#### neighbor soft-reconfiguration inbound
##### Syntax
```
[no] neighbor <A.B.C.D> soft-reconfiguration inbound
```

##### Description
This command enables software-based reconfiguration to generate inbound updates from a neighbor without clearing the BGP session. Issue the `no` command to clear this state.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| **no** | Optional | Literal |Resets to a cleared state (default). |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 soft-reconfiguration inbound
```

#### neighbor shutdown
##### Syntax
```
[no] neighbor <A.B.C.D> shutdown
```

##### Description
This command shuts down the peer. Use this syntax to preserve the neighbor configuration, but drop the BGP peer state.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| **no** | Optional | Literal | Deletes the neighbor state of the peer. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 shutdown
```

#### neighbor peer-group
##### Syntax
```
[no] neighbor <A.B.C.D> peer-group <name>
```

##### Description
This command assigns a neighbor to a peer-group.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| *name*  | Required | String of maximum length 80 characters. | The peer-group name. |
| **no** | Optional | Literal | Removes the neighbor from the peer-group. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 peer-group pg1
```

#### neighbor route-map
##### Syntax
```
[no] neighbor <A.B.C.D> route-map <name> in|out
```
##### Description
This command applies a route-map on the neighbor for the direction given (in or out).

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| *name*  | Required | String of maximum length of 80 characters. | The route-map name. |
| **no** | Optional | Literal |Removes the route-map for the neighbor. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 route-map rm1 in
```

#### neighbor advertisement-interval

##### Syntax
```
[no] neighbor <A.B.C.D|X:X::X:X> advertisement-interval <interval>
```

##### Description
This command sets the advertisement interval for route updates for a specified neighbor with an IPv4 or IPv6 address.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Optional | X:X:X:X | The peer IPv6 address. |
| *interval* | Required| 0-600 |  The time interval for sending BGP routing updates in secs. |
| **no** | Optional | Literal | Deletes the advertisement interval for a configured BGP peer. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 advertisement-interval 400
s1(config-router)# no neighbor 9.0.0.2 advertisement-interval 400
```
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 2001:db8:0:1 advertisement-interval 400
s1(config-router)# no neighbor 2001:db8:0:1 advertisement-interval 400
```

#### neighbor ebgp-multihop
##### Syntax
```
[no] neighbor <A.B.C.D | X:X::X:X | peer_group_name> ebgp-multihop
```
##### Description
This command attempts BGP connections with external AS routers that are not directly connected.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Required | X:X::X:X | The peer IPv6 address. |
| *peer_group_name*  | Required | String of maximum length 80 characters. | The peer-group name. |
| **no** | Optional | Literal | Removes the ebgp-multihop configuration for the neighbor. |

##### Examples
```
s1(config-router)# neighbor 10.0.2.15 ebgp-multihop
s1(config-router)# no neighbor 10.0.2.15 ebgp-multihop
```

#### neighbor filter-list
##### Syntax
```
[no] neighbor <A.B.C.D|X:X::X:X|WORD> filter-list WORD (in|out)
```
##### Description
This command applies a filter list to the neighbor to filter incoming and outgoing routes.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Optional | X:X:X:X | The peer IPv6 address. |
| *WORD*  | Optional | WORD | The neighbor tag. |
| *WORD*  | Required | WORD | The AS_PATH access list name. |
| *in*  | Optional | in | Filters incoming routes. |
| *out*  | Optional | out | Filters outgoing routes. |

##### Examples
```
s1(config-router)# neighbor 172.16.1.1 filter-list 1 out
s1(config-router)# no neighbor 172.16.1.1 filter-list 1 out
```

#### neighbor prefix-list
##### Syntax
```
[no] neighbor (A.B.C.D|X:X::X:X|WORD) prefix-list WORD (in|out)
```
##### Description
This command applies a prefix-list to the neighbor to filter updates to and from the neighbor.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Optional | X:X:X:X | The peer IPv6 address. |
| *WORD*  | Optional | WORD | The neighbor tag. |
| *WORD*  | Required | WORD | The name of a prefix list. |
| *in*  | Optional | in | Filters incoming routes. |
| *out*  | Optional | out | Filters outgoing routes. |

##### Examples
```
s1(config-router)# neighbor 10.23.4.2 prefix-list abc in
s1(config-router)# no neighbor 10.23.4.2 prefix-list abc in
```

#### neighbor soft-reconfiguration
##### Syntax
```
[no] neighbor (A.B.C.D|X:X::X:X|WORD) soft-reconfiguration inbound
```
##### Description
This command allows an inbound soft reconfiguration of the neighbor.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Optional | X:X:X:X | The peer IPv6 address. |
| *WORD*  | Optional | WORD | The neighbor tag. |

##### Examples
```
s1(config-router)# neighbor 10.108.1.1 soft-reconfiguration inbound
s1(config-router)# no neighbor 10.108.1.1 soft-reconfiguration inbound
```

#### neighbor ttl-security
##### Syntax
```
[no] neighbor (A.B.C.D|X:X::X:X|WORD) ttl-security hops <1-254>
```
##### Description
This command specifies the maximum number of hops to the BGP peer.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Optional | X:X:X:X | The peer IPv6 address. |
| *WORD*  | Optional | WORD | The neighbor tag. |
| *<1-254>*  | Required | 1-254 | The hop count. |

##### Examples
```
s1(config-router)# neighbor 10.1.1.1 ttl-security hops 2
s1(config-router)# no neighbor 10.1.1.1 ttl-security hops 2
```

#### neighbor update-source
##### Syntax
```
[no] neighbor (A.B.C.D|X:X::X:X|WORD) update-source (A.B.C.D|X:X::X:X|WORD)
```
##### Description
This command updates the neighbor's source address to use for the BGP session.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Optional | X:X:X:X | The peer IPv6 address. |
| *WORD*  | Optional | WORD | The neighbor tag. |
| *A.B.C.D*  | Optional | A.B.C.D | The IPv4 address. |
| *X:X::X:X*  | Optional | X:X:X:X | The IPv6 address. |
| *WORD*  | Optional | WORD | The interface name. |

##### Examples
```
s1(config-router)# neighbor 10.0.0.1 update-source loopback0
s1(config-router)# no neighbor 10.0.0.1 update-source loopback0
```

### as-path access-list
#### Syntax
```
[no]  ip as-path access-list WORD <deny|permit> .LINE
```

#### Description
This command facilitates the configuration of access lists, based on autonomous system paths that control routing updates. Autonomous system paths are based on BGP autonomous paths information. Access lists are filters that restrict the routing information that a router learns or advertises to and from a neighbor. Multiple BGP peers or route maps can reference a single access list. These access lists can be applied to both inbound and outbound route updates. Each route update is passed through the access list. BGP applies each rule in the access list in the order it appears in the list. When a route matches a rule, the decision to permit the route through or deny the route from the filter is made, and no further rules are processed. A regular expression is a pattern used to match against an input string. In BGP, regular expression can be built to match information about an autonomous system path.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length 80 characters. | The access list name |
| **deny** | Required | Literal | Denies access for matching conditions. |
| **permit** | Required | Literal | Permits access for matching conditions. |
| *.LINE* | Required | String of maximum length 80 characters. | An autonomous system in the access list in the form of a regular expression. |
| **no** | Optional | Literal | Disables an access list rule. |

#### Examples
```
s1(config)#ip as-path access-list 1 permit _234_
s1(config)#ip as-path access-list 1 permit _345_
s1(config)#ip as-path access-list 1 deny any
```

## Route-map configuration commands

### route-map
#### Syntax
```
[no] route-map WORD <deny|permit> <order>
```

#### Description
This command configures the order of the entry in the route map name with either the permit or deny match policy.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length 80 characters. | The route map name. |
| *order*  | Required |1-65535| The order number of the route map. |
| **deny** | Required | Literal | Denies the order of the entry. |
| **permit** | Required | Literal | Permits the order of the entry. |
| **no** | Optional | Literal | Deletes the route map. |

#### Examples
```
s1(config)# route-map rm1 deny 1
```

### Route-map match
#### match prefix-list

##### Syntax
```
[no] match ip address prefix-list WORD
```

##### Description
This command configures a match clause for the route map to distribute any routes with a destination network number address that is permitted by a prefix-list.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length 80 characters. | The IP prefix list name. |
| **no** | Optional | Literal | Deletes the match clause for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)# match ip address prefix-list PLIST1
```

#### match as-path
##### Syntax
```
[no] match as-path WORD
```

##### Description
This command matches a BGP autonomous system path access list.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | The AS path access list name. |
| **no** | Optional | Literal | Deletes the AS path access list entry. |

##### Examples
```
s1(config-route-map)# match as-path WORD
s1(config-route-map)# no match as-path WORD
s1(config-route-map)# no match as-path
```

#### match community
##### Syntax
```
[no] match community (<1-99>|<100-500>|WORD)
```

##### Description
This command matches a BGP community; use this command in route-map configuration mode.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-99>*  | Optional | 1-99 | The community list number (standard). |
| *<100-500>*  | Optional | 100-500 | The community list number (expanded). |
| *WORD*  | Optional | WORD | The community list name. |
| **no** | Optional | Literal | Removes the match community entry. |

##### Examples
```
s1(config-route-map)# match community 10
s1(config-route-map)# no match community 10
s1(config-route-map)# no match community
```

#### match community exact-match
##### Syntax
```
[no] match community (<1-99>|<100-500>|WORD) exact-match
```

##### Description
This command matches a BGP community with an exact match of communities.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-99>*  | Optional | 1-99 | The community list number (standard). |
| *<100-500>*  | Optional | 100-500 | The community list number (expanded). |
| *WORD*  | Optional | WORD | The community list name. |
| *exact-match*  | Required | exact-match | Does exact matching of communities. |
| **no** | Optional | Literal | Removes the match community exact-match entry. |

##### Examples
```
s1(config-route-map)# match community c1 exact-match
s1(config-route-map)# no match community c1 exact-match
```

#### match  extcommunity
##### Syntax
```
[no] match extcommunity (<1-99>|<100-500>|WORD)
```

##### Description
This command matches the BGP extended community list attributes; use this command in route-map mode.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-99>*  | Optional | 1-99 | The extended community list number (standard). |
| *<100-500>*  | Optional | 100-500 | The extended community list number (expanded). |
| *WORD*  | Optional | WORD | The extended community list name. |
| **no** | Optional | Literal | Removes the match extcommunity entry. |

##### Examples
```
s1(config-route-map)# match extcommunity 10
s1(config-route-map)# no match extcommunity 10
s1(config-route-map)# no match extcommunity
```

#### match interface
##### Syntax
```
[no] match interface WORD
```

##### Description
This command distributes routes that have their next hop out of the specified interface.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | The interface name. |
| **no** | Optional | Literal | Removes the match interface entry. |

##### Examples
```
s1(config-route-map)# match interface 1
s1(config-route-map)# no match interface 1
s1(config-route-map)# no match interface
```

#### match ip address
##### Syntax
```
[no] match ip address (<1-199>|<1300-2699>|WORD)
```

##### Description
This command distributes any routes with a destination network number address that is permitted by a standard or extended access list.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-199>*  | Optional | 1-199 | The IP access list number .|
| *<1300-2699>*  | Optional | 1300-2699 | The IP access list number (expanded range). |
| *WORD*  | Optional | WORD | The IP access list name |
| **no** | Optional | Literal | Removes the match ip address entry. |

##### Examples
```
s1(config-route-map)# match ip address 1500
s1(config-route-map)# no match ip address 1500
s1(config-route-map)# no match ip address
```

#### match ip address prefix-list
##### Syntax
```
[no] match ip address prefix-list WORD
```

##### Description
To distribute any routes that have a destination network number address that is permitted by a prefix list.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | The IP prefix list name. |
| **no** | Optional | Literal | Removes the match ip address prefix-list entry. |

##### Examples
```
s1(config-route-map)# match ip address prefix-list pl1
s1(config-route-map)# no match ip address prefix-list pl1
s1(config-route-map)# no match ip address prefix-list
```

#### match ip next-hop
##### Syntax
```
[no] match ip next-hop (<1-199>|<1300-2699>|WORD)
```

##### Description
This command redistributes any routes that have a next hop router address passed by one of the specified access lists.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-199>*  | Optional | 1-199 | The IP access list number. |
| *<1300-2699>*  | Optional | 1300-2699 | The IP access list number (expanded range). |
| *WORD*  | Optional | WORD | The IP access list name. |
| **no** | Optional | Literal | Deletes the match ip next hop entry. |

##### Examples
```
s1(config-route-map)# match ip next-hop 100
s1(config-route-map)# no match ip next-hop 100
s1(config-route-map)# no match ip next-hop
```

#### match ip next-hop prefix-list
##### Syntax
```
[no] match ip next-hop prefix-list WORD
```

##### Description
This command redistributes any routes with a next hop router address passed by one of the specified prefix lists.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | The IP prefix list name. |
| **no** | Optional | Literal | Removes the match ip next-hop prefix-list entry. |

##### Examples
```
s1(config-route-map)# match ip next-hop prefix-list pfl1
s1(config-route-map)# no match ip next-hop prefix-list pfl1
s1(config-route-map)# no match ip next-hop prefix-list
```

#### match ip route-source
##### Syntax
```
[no] match ip route-source (<1-199>|<1300-2699>|WORD)
```

##### Description
This command redistributes routes that have been advertised by routers and access servers at the addresses specified in the access list.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-199>*  | Optional | 1-199 | The IP access list number. |
| *<1300-2699>*  | Optional | 1300-2699 | The IP access list number (expanded range). |
| *WORD*  | Optional | WORD | The IP access list name. |
| **no** | Optional | Literal | Removes the match ip route-source entry. |

##### Examples
```
s1(config-route-map)# match ip route-source 2000
s1(config-route-map)# no match ip route-source 2000
s1(config-route-map)# no match ip route-source
```

#### match ip route-source prefix-list
##### Syntax
```
[no] match ip route-source prefix-list WORD
```

##### Description
This command redistributes routes that have been advertised by routers and access servers at the addresses specified in the prefix list.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | The IP prefix list name. |
| **no** | Optional | Literal | Removes the match ip route-source prefix-list entry |

##### Examples
```
s1(config-route-map)# match ip route-source prefix-list p1
s1(config-route-map)# no match ip route-source prefix-list p1
s1(config-route-map)# no match ip route-source prefix-list
```

#### match ipv6 address
##### Syntax
```
[no] match ipv6 address WORD
```

##### Description
This command distributes IPv6 routes that have a prefix specified in an IPv6 access list.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | The IPv6 access list name. |
| **no** | Optional | Literal | Removes the match ipv6 address entry. |

##### Examples
```
s1(config-route-map)# match ipv6 address acl1
s1(config-route-map)# no match ipv6 address acl1
```

#### match ipv6 address prefix-list
##### Syntax
```
[no] match ipv6 address prefix-list WORD
```

##### Description
This command distributes IPv6 routes that have a prefix specified in an IPv6 prefix list.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | The IPv6 prefix list. |
| **no** | Optional | Literal | Removes the match ipv6 address prefix-list entry. |

##### Examples
```
s1(config-route-map)# match ipv6 address prefix-list p1
s1(config-route-map)# no match ipv6 address prefix-list p1
```

#### match ipv6 next-hop
##### Syntax
```
[no] match ipv6 next-hop X:X::X:X
```

##### Description
This command distributes IPv6 routes that have a specified next hop.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *X:X::X:X*  | Required | X:X::X:X | The IPv6 address of the next hop. |
| **no** | Optional | Literal | Removes the match ipv6 next-hop entry. |

##### Examples
```
s1(config-route-map)# match ipv6 next-hop 2001::1
s1(config-route-map)# no match ipv6 next-hop 2001::1
```

#### match metric
##### Syntax
```
[no] match metric <0-4294967295>
```

##### Description
This command redistributes routes with the specified metric.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<0-4294967295>*  | Required | Integer in the range <0-4294967295>. | The metric value. |
| **no** | Optional | Literal | Removes the match metric entry. |

##### Examples
```
s1(config-route-map)# match metric 400
s1(config-route-map)# no match metric 400
s1(config-route-map)# no match metric
```

#### match origin
##### Syntax
```
[no] match origin (egp|igp|incomplete)
```

##### Description
This command matches BGP routes based on the origin of the specified route.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *egp*  | Optional | egp | Remote egp. |
| *igp*  | Optional | igp | Local igp .|
| *incomplete*  | Optional | incomplete | Unknown heritage. |
| **no** | Optional | Literal | Removes the match origin entry. |

##### Examples
```
s1(config-route-map)# match origin egp
s1(config-route-map)# no match origin egp
s1(config-route-map)# no match origin
```

#### match peer
##### Syntax
```
[no] match peer (A.B.C.D|X:X::X:X)
```

##### Description
This command matches BGP routes based on the peer address.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Optional | X:X::X:X | The peer IPv6 address. |
| **no** | Optional | Literal | Removes the match peer entry. |

##### Examples
```
s1(config-route-map)# match peer 10.10.10.1
s1(config-route-map)# no match peer 10.10.10.1
s1(config-route-map)# no match peer
```

#### match peer local
##### Syntax
```
[no] match peer local
```

##### Description
This command matches BGP routes against static or redistributed routes.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *local*  | Required | local | Static or redistributed routes. |
| **no** | Optional | Literal | Removes the match peer local entry. |

##### Examples
```
s1(config-route-map)# match peer local
s1(config-route-map)# no match peer local
s1(config-route-map)# no match peer
```

#### match probability
##### Syntax
```
[no] match probability <0-100>
```

##### Description
This command matches the portion of BGP routes defined by percentage value.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<0-100>*  | Required | 0-100 | Percentage of routes. |
| **no** | Optional | Literal | Removes match probability entry. |

##### Examples
```
s1(config-route-map)# match probability 50
s1(config-route-map)# no match probability 50
s1(config-route-map)# no match probability
```

#### match tag
##### Syntax
```
[no] match tag <0-65535>
```

##### Description
This command matches the tag of the route.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<0-65535>*  | Required | 0-65535 | The tag value. |
| **no** | Optional | Literal | Removes the match tag entry. |

##### Examples
```
s1(config-route-map)# match tag 600
s1(config-route-map)# no match tag 600
s1(config-route-map)# no match tag
```

#### on-match goto
##### Syntax
```
[no] on-match goto <1-65535>
```

##### Description
This command initializes the exit policy on matches with a goto clause.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-65535>*  | Required | 1-65535 | The goto clause number. |
| **no** | Optional | Literal | Deinitializes the exit policy.  |

##### Examples
```
s1(config-route-map)# on-match goto 200
s1(config-route-map)# no on-match goto
```

#### on-match next
##### Syntax
```
[no] on-match next
```

##### Description
This command initializes the exit policy on matches with a next clause.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Deinitializes the exit policy. |

##### Examples
```
s1(config-router)# on-match next
s1(config-router)# no on-match next
```

### Route-map set
#### Syntax
```
Route-map Command: [no] set community <AA:NN> [additive]
Route-map Command: [no] set metric <val>
```

#### Description
The `set community` command sets the BGP community attribute. The `set metric` command sets the BGP attribute MED.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *AA:NN*  | Required | AS1:AS2 where AS is an integer in the range <1-4294967295>. | Sets the BGP community attribute. |
| *val*  | Required | Integer in the range <0-4294967295>.  | Sets the metric value. |
| **no** | Optional | Literal | Clears the community attribute. |

#### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)# set community 6001:7002 additive
s1(config-route-map)# set metric 100
s1(config-route-map)# no set metric 100
```

#### set aggregator
##### Syntax
```
[no] set aggregator as <value> <A.B.C.D>
```

##### Description
This command sets the originating AS of an aggregated route. The value specifies from which AS the aggregate route originated. The range is from 1-4294967295. The `set-aggregator-ip` value must also be set to further identify the originating AS.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value*  | Required | Integer in the range <1-4294967295>. | The AS value. |
| *A.B.C.D* | Required | String of maximum length 80 characters. | The IPv4 address of AS. |
| **no** | Optional | Literal | Clears the aggregator configuration for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set aggregator as 1 9.0.0.1
```

#### set as-path exclude
##### Syntax
```
[no] set as-path exclude .<value>
```

##### Description
This command excludes the given AS number from the AS_PATH.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value*  | Required | Integer in the range <1-4294967295>. | The AS value to be excluded from the AS_PATH. |
| **no** | Optional | Literal | Clears the AS value exclusion from the AS_PATH. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set as-path exclude 2
```

#### set as-path prepend
##### Syntax
```
[no] set as-path prepend .<value>
```

##### Description
This command prepends the given AS number to the AS_PATH.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value*  | Required | Integer in the range <1-4294967295>. | The AS value to be added to the AS_PATH. |
| **no** | Optional | Literal | Clears the AS value from the AS_PATH. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set as-path prepend 2
```

#### set atomic-aggregate
##### Syntax
```
[no] set atomic-aggregate
```

##### Description
This command enables a warning to upstream routers, through the ATOMIC_AGGREGATE attribute, that address aggregation has occurred on an aggregate route.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Disables the route-aggregation notification to upstream routers. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set atomic-aggregate
```

#### set comm-list delete
##### Syntax
```
[no] set comm-list <list-name> delete
```

##### Description
This command removes the COMMUNITY attributes from the BGP routes identified in the specified community list. It also deletes matching communities for the route map.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *list-name* | Required | Integer in the range <1-99> or <100-500>, or a valid community string not exceeding 80 characters. | The community list name. |
| **no** | Optional | Literal | Deletes the community list exclusion under the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set comm-list 1 delete
```

#### set community
##### Syntax
```
[no] set community <list-name>
```

##### Description
This command sets the COMMUNITY attributes for route-map. The community number may be one of the following:
- aa:nn format
- local-AS|no-advertise|no-export|internet
- Additive
- None

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *list-name* | Required | An integer in the range <1-99> or <100-500>, or a valid community string not exceeding 80 characters. | The community list name. |
| **no** | Optional | Literal | Deletes the community list configuration under the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set community 6000:100
```

#### set community rt
##### Syntax
```
[no] set extcommunity rt <asn-community-identifier>
```

##### Description
This command sets the target extended community (in decimal notation) of a BGP route. The COMMUNITY attribute value has the syntax AA:NN, where AA represents an AS or IP address, and NN is the community identifier.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *asn-community-identifier* | Required | AS1:AS2, where AS is an integer in the range <1 - 4294967295>, or a string not exceeding 80 characters. | The community attribute in the form of AA:nn or IP address:nn. |
| **no** | Optional | Literal | Deletes the configuration for the rt extended community list under the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set extcommunity rt 6000:100
s1(config-route-map)#set extcommunity rt 9.0.0.1:100
```

#### set extcommunity soo
##### Syntax
```
[no] set extcommunity soo <asn-community-identifier>
```

##### Description
This command sets the site-of-origin extended community (in decimal notation) of a BGP route. The COMMUNITY attribute value has the syntax AA:NN, where AA represents an AS or IP address, and NN is the community identifier.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *asn-community-identifier* | Required | AS1:AS2, where AS is an integer in the range <1 - 4294967295>, or a string not exceeding 80 characters. | The community attribute in the form of AA:nn or IP address:nn. |
| **no** | Optional | Literal | Deletes the configuration for the site-of-origin extended community list under the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set extcommunity soo 6000:100
s1(config-route-map)#set extcommunity soo 9.0.0.1:100
```

#### set ip next-hop
##### Syntax
```
[no] set ip next-hop <A.B.C.D>
```

##### Description
This command sets the IP address for the next hop.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D* | Required | A.B.C.D | The IPv4 address, or a string not exceeding 80 characters. |
| **no** | Optional | Literal | Unsets the next hop IP address for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set ip next-hop 9.0.0.1
```

#### set ip next-hop peer-address
##### Syntax
```
[no] set ip next-hop peer-address
```

##### Description
In the BGP routing protocol, an update from the external AS contains the next hop address of the external hop itself. Therefore, when the router receives an update from the external AS and advertises that update to the other routers via iBGP, the other routers see the next hop of the advertised networks via the external router IP address.

This command enables the iBGP learn router to forward the packet to its peer address instead of the external router's IP address.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Unsets the IP address from the next-hop peer-address for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set ip next-hop peer-address
```

#### set ipv6 next-hop global
##### Syntax
```
[no] set ipv6 next-hop global <X:X::X:X>
```

##### Description
This command sets the BGP-4+ global IPv6 next hop address.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *X:X::X:X*  | Required | X:X::X:X | The IPv6 address. |
| **no** | Optional | Literal | Unsets the BGP-4+ global IPv6 next hop address for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set ipv6 next-hop global 2001:db8:0:1
```

#### set ipv6 next-hop local
##### Syntax
```
[no] set ipv6 next-hop local <X:X::X:X>
```

##### Description
This command sets the BGP-4+ link-local IPv6 next hop address.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *X:X::X:X*  | Required | X:X::X:X | The IPv6 address. |
| **no** | Optional | Literal | Unsets the BGP-4+ link-local IPv6 next hop address for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set ipv6 next-hop local 2001:db8:0:1
```

#### set local-preference
##### Syntax
```
[no] set local-preference <value>
```

##### Description
This command sets the BGP local preference and the local preference value of an IBGP route. The value is advertised to IBGP peers. The range is from 0 to 4294967295. A higher number signifies a preferred route among multiple routes to the same destination.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value* | Required | Integer in the range <0-4294967295>.  | The IPv6 address. |
| **no** | Optional | Literal | Unsets the BGP local preference for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set local-preference 1
```

#### set metric
##### Syntax
```
[no] set metric <expr>
```

##### Description
This command specifies the relative change of metric which is used with BGP route advertisement. This command takes the route's current metric and increases or decreases it by a specified value before it is propagated. If the value is specified as negative and ends up being negative after the metric decrease, the value is interpreted as an increase in metric.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *expr* | Required | String of maximum length 80 characters. | The metric expression. |
| **no** | Optional | Literal | Unsets the BGP local preference for the route map |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set metric +2

s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set metric -367
In this case -367 is treated as +367.
```

#### set metric-type
##### Syntax
```
[no] set metric-type <type-1 | type-2>
```

##### Description
This command sets the metric type for the destination routing protocol.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| **type-1** | Required | Literal  | Specifies the type-1 metric. |
| **type-2** | Required | Literal  | Specifies the type-2 metric. |
| **no** | Optional | Literal | Unsets the BGP metric type for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set metric-type type-1
```

#### set origin
##### Syntax
```
[no] set origin <egp | igp | incomplete>
```

##### Description
This command sets the ORIGIN attribute of a local BGP route to one of the following:
- `egp`: Sets the value to the Network Layer Reachablility Information (NLRI) learned from the Exterior Gateway Protocol (EGP).
- `igp`: Sets the value to the NLRI learned from a protocol internal to the originating AS.
- `incomplete`: If the value is not `egp` or `igp`.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| **egp** | Required | Literal  | Specifies the type-1 metric. |
| **igp** | Required | Literal  | Specifies the type-2 metric. |
| **incomplete** | Required | Literal  | Specifies the type-2 metric. |
| **no** | Optional | Literal | Unsets the BGP origin attribute for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set origin egp
```

#### set originator-id
##### Syntax
```
[no] set originator-id <A.B.C.D>
```

##### Description
This command sets the ORIGINATOR_ID attribute, which is equivalent to the router-id of the originator of the route in the local AS. Route reflectors use this value to prevent routing loops.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The IPv4 address. |
| **no** | Optional | Literal | Unsets the BGP originator-id attribute for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set originator-id 9.0.0.1
```

#### set src
##### Syntax
```
[no] set src <A.B.C.D>
```

##### Description
This command sets the preferred source address for matching routes within a route map, when installing in the kernel.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The IPv4 address. |
| **no** | Optional | Literal | Unsets the BGP src attribute for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set src 9.0.0.1
```

#### set tag
##### Syntax
```
[no] set tag <value>
```

##### Description
This command sets the tag for redistributions which external routers use to filter incoming distributions of route maps.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value*  | Required | Integer in the range <0-65535>. | The tag value. |
| **no** | Optional | Literal | Unsets the BGP tag attribute for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set tag 9
```

#### set vpnv4 next-hop
##### Syntax
```
[no] set vpnv4 next-hop <A.B.C.D>
```

##### Description
This command sets the next hop IP address for VPNv4 updates.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The IPv4 address. |
| **no** | Optional | Literal | Unsets the vpnv4 next-hop attribute for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set vpnv4 next-hop 9.0.0.1
```

#### set weight
##### Syntax
```
[no] set weight <value>
```

##### Description
This command sets the weight of a BGP route. A route`s weight has the most influence when two identical BGP routes are compared. A higher number signifies a greater preference.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value*  | Required | Integer in the range <1-4294967295>. | The weight value. |
| **no** | Optional | Literal | Unsets the weight attribute for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)# set weight 9
```

### Route-map description
#### Syntax
```
Route-map Command: [no] description <text>
```

#### Description
This command sets the route-map description.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *text*  | Required | String of maximum length 80 characters. | The route-map description. |
| **no** | Optional | Literal | Clears the description for the route map. |

#### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)# description rmap-mcast
```

### Route-map call
#### Syntax
```
[no] call WORD
```
#### Description
This command jumps to another route map after match and set.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | The target route map name. |
| **no** | Optional | Literal | Disables jumping to another route map. |

#### Examples
```
s1(config-route-map)# call rmap
s1(config-route-map)# no call
```

### Route-map continue
#### Syntax
```
[no] continue <1-65535>
```

#### Description
This command continues onto a different entry within the route map.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-65535>*  | Required | 1-65535 | The route map entry sequence number. |
| **no** | Optional | Literal | Disables continuing onto a different entry. |

#### Examples
```
s1(config-route-map)# continue 300
s1(config-route-map)# no continue 300
s1(config-route-map)# no continue
```

## IP prefix-list configuration commands
###  IPv4 prefix-list
#### Syntax
```
[no] ip prefix-list WORD seq <num> (deny|permit) <A.B.C.D/M|any>
[no] ip prefix-list WORD seq <num> (deny|permit) A.B.C.D/M le <0-32> ge <0-32>
[no] ip prefix-list WORD seq <num> (deny|permit) A.B.C.D/M ge <0-32>
[no] ip prefix-list WORD seq <num> (deny|permit) A.B.C.D/M le <0-32>
```

#### Description
The `ip prefix-list` command provides a powerful prefix-based filtering mechanism. It has prefix length range and sequential number specifications. You can add or delete prefix-based filters to arbitrary points of a prefix-list by using a sequential number specification. If `no ip prefix-list` is specified, it acts as a permit. If the  `ip prefix-list` is defined, and no match is found, the default deny is applied.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *name*  | Required | String of maximum length 80 characters. | The IP prefix-list name. |
| *num*  | Required | 1-4294967295 | The sequence number. |
| *A.B.C.D/M*  | Required | A.B.C.D/M | The IPv4 prefix. |
| *0-32*  | Required | 0-32 | Minimum prefix length to be matched. |
| *0-32*  | Required | 0-32 | Maximum prefix length to be matched. |
| **no** | Optional | Literal |Deletes the IP prefix-list. |

#### Examples
```
s1(config)# ip prefix-list PLIST1 seq 5 deny 11.0.0.0/8
s1(config)# ip prefix-list PLIST2 seq 10 permit 10.0.0.0/8
s1(config)# no ip prefix-list PLIST1 seq 5 deny 11.0.0.0/8
s1(config)# no ip prefix-list PLIST2
```
###  IPv6 prefix-list
#### Syntax
```
[no] ipv6 prefix-list WORD description .LINE
[no] ipv6 prefix-list WORD seq <num> <deny|permit> <X:X::X:X/M|any>
[no] ipv6 prefix-list WORD seq <num> <deny|permit> <X:X::X:X/M> ge <length>
[no] ipv6 prefix-list WORD seq <num> <deny|permit> <X:X::X:X/M> ge <length> le <length>
[no] ipv6 prefix-list WORD seq <num> <deny|permit> <X:X::X:X/M> le <length>
```

#### Description
The `ipv6 prefix-list` command provides IPv6 prefix-based filtering mechanism. Descriptions may be added to prefix lists. The `description` command adds a description to the prefix list. The `ge` command specifies prefix length, and the prefix list is applied if the prefix length is greater than or equal to the `ge` prefix length. The `le` command specifies prefix length, and the prefix list is be applied if the prefix length is less than or equal to the `le` prefix length. If `no ipv6 prefix-list` is specified, it acts as permit. If `ipv6 prefix-list` is defined, and no match is found, the default deny is applied.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length of 80 characters. | The IP prefix-list name. |
| *num*  | Required | 1-4294967295 | The sequence number. |
| *.LINE*  | Required | String of maximum length 80 characters. | The prefix list description |
| *X:X::X:X/M*  | Required | X:X::X:X/M | The IPv6 prefix. |
| *length* | Required | 0-128 | The prefix length. |
| **no** | Optional | Literal | Deletes the IPv6 prefix-list. |

#### Examples
```
s1(config)# ipv6 prefix-list COMMON-PREFIXES description prefixes
s1(config)# no ipv6 prefix-list COMMON-PREFIXES
s1(config)# ipv6 prefix-list COMMON-PREFIXES seq 5 permit 2001:0DB8:0000::/48
s1(config)# ipv6 prefix-list COMMON-PREFIXES seq 10 deny any
s1(config)# ipv6 prefix-list COMMON-PREFIXES seq 15 permit 2001:0DB8:0000::/48 ge 64
s1(config)# no ipv6 prefix-list COMMON-PREFIXES
s1(config)# ipv6 prefix-list PEER-A-PREFIXES seq 5 permit 2001:0DB8:AAAA::/48 ge 64 le 64
s1(config)# no ipv6 prefix-list PEER-A-PREFIXES
```


## Community lists configuration commands

#### Syntax
```
[no] ip  community-list WORD <deny|permit> .LINE
```

#### Description
This command defines a new community list. LINE is a string expression of the communities attribute. LINE can include a regular expression to match the communities attribute in BGP updates. The community is compiled into a community structure. Multiple community lists can be defined under the same name. In that case, the match happens in user-defined order. Once the community list matches to the communities attribute in BGP updates, it returns a permit or deny based on the community list definition. When there is no matched entry, deny is returned. When the community is empty, the system matches to any routes.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length 80 characters. | The community list name. |
| **deny** | Required | Literal | Denies access for matching conditions. |
| **permit** | Required | Literal | Permits access for matching conditions. |
| *.LINE* | Required | String of maximum length 80 characters. | Community numbers specified as regular expressions. |
| **no** | Optional | Literal | Deletes the rule for the specified community. |

#### Examples
```
S1(config)#ip community-list EXPANDED permit [1-2]00
S1(config)#ip community-list ANY-COMMUNITIES deny ^0:.*_
S1(config)#ip community-list ANY-COMMUNITIES deny ^65000:.*_
S1(config)#ip community-list ANY-COMMUNITIES permit .*
```


## Extended community lists configuration commands
#### Syntax
```
[no] ip extcommunity-list WORD <deny|permit> .LINE
```
#### Description
This command defines a new extended community list.  LINE is a string expression of the extended communities attribute, and can include a regular expression to match the extended communities attribute in BGP updates.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length 80 characters. | The extended community list name. |
| *.LINE*  | Required | String of maximum length 80 characters. | The string expression of the extended communities attribute. |
| **deny** | Required | Literal | Denies access for matching conditions. |
| **permit** | Required | Literal | Permits access for matching conditions. |
| **no** | Optional | Literal | Deletes the extended community list. |

#### Examples
```
s1(config)# ip extcommunity-list expanded ROUTES permit REGULAR_EXPRESSION
s1(config)# no ip extcommunity-list expanded ROUTES
```

##Display commands

### show ip bgp
#### Syntax
```
show ip bgp [A.B.C.D][A.B.C.D/M]
```

#### Description
This command displays BGP routes from the BGP route table. When no route is specified, all IPv4 routes are displayed.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The IPv4 prefix. |
| *A.B.C.D/M*  | Optional | A.B.C.D/M | The IPv4 prefix with prefix length. |

#### Examples
```ditaa
s1# show ip bgp
Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
              i internal, S Stale, R Removed
Origin codes: i - IGP, e - EGP, ? - incomplete

Local router-id 9.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       0.0.0.0                  0      0  32768  i
*> 12.0.0.0/8       10.10.10.2               0      0      0 2 5 i
*  12.0.0.0/8       20.20.20.2               0      0      0 3 5 i
*  12.0.0.0/8       30.30.30.2               0      0      0 4 5 i
Total number of entries 4
```

### show ip bgp summary
#### Syntax
```
show ip bgp summary
```

#### Description
The command provides a summary of the BGP neighbor status.

#### Authority
Admin user.

#### Parameters
None

#### Examples
```ditaa
s1# show ip bgp summary
BGP router identifier 9.0.0.1, local AS number 1
RIB entries 2
Peers 1

Neighbor             AS MsgRcvd MsgSent Up/Down  State
9.0.0.2               2       4       5 00:00:28 Established
```

###  show bgp neighbors
#### Syntax
```
show bgp neighbors
```

#### Description
This command displays detailed information about BGP neighbor connections.

#### Authority
Admin user.

#### Parameters
None

#### Examples
```ditaa
s1# show bgp neighbors
  name: 9.0.0.2, remote-as: 6002
    state: undefined
    shutdown: yes
    description: peer1
    capability: undefined
    local_as: undefined
    local_interface: undefined
    inbound_soft_reconfiguration: yes
    maximum_prefix_limit: undefined
    tcp_port_number: undefined
    statistics:
  name: pg1, remote-as: undefined
    state: undefined
    shutdown: undefined
    description: undefined
    capability: undefined
    local_as: undefined
    local_interface: undefined
    inbound_soft_reconfiguration: undefined
    maximum_prefix_limit: undefined
    tcp_port_number: undefined
    statistics:
```
## CLI 
Click [here](http://www.openswitch.net/documents/user/bpg_cli) for CLI commands related to the BGP feature.

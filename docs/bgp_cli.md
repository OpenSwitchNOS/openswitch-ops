BGP Commands Reference
=======================

- [BGP Configuration Commands](#bgp-configuration-commands)
	- [router bgp](#router-bgp)
	- [bgp router-id](#bgp-router-id)
	- [network](#network)
	- [maximum-paths](#maximum-paths)
	- [timers bgp](#timers-bgp)
        - [address-family ipv6](#address-family-ipv6)
        - [network](#network)
        - [bgp always-compare-med](#bgp-always-compare-med)
        - [bgp bestpath compare-routerid](#bgp-bestpath-compare-routerid)
        - [bgp deterministic-med](#bgp-deterministic-med)
        - [bgp fast-external-failover](#bgp-fast-external-failover)
        - [bgp log-neighbor-changes](#bgp-log-neighbor-changes)
        - [bgp network import-check](#bgp-network-import-check)
        - [redistribute routes](#redistribute-routes)
	- [BGP Neighbor](#bgp-neighbor)
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
		- [neighbor interface](#neighbor-interface)
		- [neighbor strict-capability-match](#neighbor-strict-capability-match)
		- [neighbor activate](#neighbor-activate)
		- [neighbor capability dynamic](#neighbor-capability-dynamic)
		- [neighbor capability orf](#neighbor-capability-orf)
		- [neighbor capability distribute-list](#neighbor-capability-distribute-list)
		- [neighbor dont-capability-negotiate](#neighbor-dont-capability-negotiate)
		- [neighbor override-capability](#neighbor-override-capability)
		- [neighbor ebgp-multihop](#neighbor-ebgp-multihop)
		- [neighbor filter-list](#neighbor-filter-list)
		- [neighbor prefix-list](#neighbor-prefix-list)
		- [neighbor send-community](#neighbor-send-community)
		- [neighbor soft-reconfiguration](#neighbor-soft-reconfiguration)
		- [neighbor ttl-security](#neighbor-ttl-security)
		- [neighbor update-source](#neighbor-update-source)
- [AS-Path Access List Configuration Command](as-path-access-list-configuration-command)
- [Route Map Configuration Commands](#route-map-configuration-commands)
	- [Route Map](#route-map)
	- [Route Map Match](#route-map-match)
        - [match prefix-list](#match-prefix-list)
        - [match as-path](#match-as-path)
        - [match community](#match-community)
        - [match community exact-match](#match-community-exact-match)
        - [match extcommunity](#match-extcommunity)
        - [match interface](#match-interface)
        - [match ip address](#match-ip-address)
        - [match ip address prefix-list](#match-ip-address-prefix-list)
        - [match ip nexthop](#match-ip-nexthop)
        - [match ip nexthop prefix-list](#match-ip-nexthop-prefix-list)
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
	- [Route Map Set](#route-map-set)
	    - [set aggregator](#set-aggregator)
	    - [set as-path exclude](#set-as-path-exclude)
	    - [set as-path prepend](#set-as-path-prepend)
	    - [set atomic aggregate](#set-atomic-aggregate)
	    - [set community list delete](#set-community-list-delete)
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
	- [Route Map Description](#route-map-description)
	- [Route Map Call](#route-map-call)
    - [Route Map Continue](#route-map-continue)
- [IP Prefix-list Configuration Commands](#ip-prefix-list-configuration-commands)
	- [IPv4 prefix-list](#ipv4-prefix-list)
	- [IPv6 prefix-list](#ipv6-prefix-list)
- [Community Lists Configuration Commands](#community-lists-configuration-commands)
- [Extended Community Lists Configuration Commands](#extended-community-lists-configuration-commands)
- [Display Commands](#display-commands)
    - [show ip bgp](#show-ip-bgp)
    - [show ip bgp summary](#show-ip-bgp-summary)
    - [show bgp neighbors](#show-bgp-neighbors)

## BGP Configuration Commands

### router bgp

To use the BGP feature, you must first configure BGP router as shown below.

#### Syntax
```
[no] router bgp <asn>
```

#### Description
This command is used to configure the BGP router. To configure the BGP router, you need the Autonomous System (AS) number. The BGP protocol uses the AS number for detecting whether the BGP connection is internal or external.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *asn*  | Required | 1 - 4294967295 | AS number |
| **no** | Optional | Literal | Destroys a BGP router with the specified ASN |

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
This command specifies the BGP router-ID for a BGP Router.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | IPv4 address |
| **no** | Optional | Literal | Deletes BGP Router IP address |

#### Examples
```
s1(config-router)# bgp router-id 9.0.0.1
s1(config-router)# no bgp router-id 9.0.0.1
```

### network
#### Syntax
```
[no] network <A.B.C.D/M>
```

#### Description
This command adds the announcement network.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D/M*  | Required | A.B.C.D/M | IPv4 address with the prefix length.|
| **no** | Optional | Literal | Removes the announced network for this BGP router. |

#### Examples
This configuration example shows that network 10.0.0.0/8 is announced to all neighbors.

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
This command sets the maximum number of paths for a BGP route.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *num*  | Required | 1-255 | Maximum number of paths |
| **no** | Optional | Literal | Sets the maximum number of paths to the default value of 1 |


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
admin

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *Keepalive*  | Required | 0 - 65535 | The keepalive interval in seconds |
| *holdtime* | Required| 0 - 65535 | Hold time in seconds |
| **no** | Optional | Literal | Resets the keepalive and hold time values to their default values (60 seconds for the keepalive interval and 180 seconds for the hold time value)  |

#### Examples
```
s1(config)# router bgp 6001
s1(config-router)# timers bgp 60 30
```

### address-family ipv6
#### Syntax
```
[no] address-family ipv6
```
#### Description
Use this command in router configuration mode to enter address family configuration mode for configuring routing protocols that use IPv6 address prefixes.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Disables address family configuration mode |

#### Examples
```
s1(config-router)#address-family ipv6
s1(config-router)#no address-family ipv6
```

### network
#### Syntax
```
[no] ipv6 bgp network X:X::X:X/M
```

#### Description
This command advertises the IPv6 prefix network.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *X:X::X:X/M*  | Required | X:X::X:X/M | IPv6 prefix address and prefix length |
| **no** | Optional | Literal | Deletes the IPv6 prefix network |

#### Examples
```
s1(config-router)# ipv6 bgp network 2001:1::1/64
s1(config-router)# no ipv6 bgp network 2001:1::1/64
```

### bgp always-compare-med
#### Syntax
```
[no] bgp always-compare-med
```

#### Description
This command when enabled ensures the comparison of MED for paths from neighbors in different autonomous systems.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | To disallow the comparison of the MED |

#### Examples
```
s1(config-router)# bgp always-compare-med
s1(config-router)# no bgp always-compare-med
```

### bgp bestpath compare-routerid
#### Syntax
```
[no] bgp bestpath compare-routerid
```

#### Description
This command is used to configure a BGP routing process to compare identical routes received from different external peers during the best path selection process and to select the route with the lowest router ID as the best path

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | To return the BGP process to the default operation |

#### Examples
```
s1(config-router)# bgp bestpath compare-routerid
s1(config-router)# no bgp bestpath compare-routerid
```

### bgp deterministic-med
#### Syntax
```
[no] bgp deterministic-med
```

#### Description
This command ensures the comparison of the MED variable when choosing routes advertised by different peers in the same autonomous system.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | To disable the comparison of the MED |

#### Examples
```
s1(config-router)# bgp deterministic-med
s1(config-router)# no bgp deterministic-med
```

### bgp fast-external-failover
#### Syntax
```
[no] bgp fast-external-failover
```

#### Description
This command is used to enable fast external failover for BGP directly connected peering sessions.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Disables BGP fast external failover |

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
This command enables logging of BGP neighbor status changes (up and down) and resets.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | IPv4 address |
| **no** | Optional | Literal | Disable the logging of neighbor status change |

#### Examples
```
s1(config-router)# bgp log-neighbor-changes
s1(config-router)# no bgp log-neighbor-changes
```

### bgp network import-check
#### Syntax
```
[no] bgp network import-check
```

#### Description
This command is used to enable the advertising of the BGP network in IGP.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Disable advertising of the BGP network in IGP |

#### Examples
```
s1(config-router)# bgp network import-check
s1(config-router)# no bgp network import-check
```

### redistribute routes
#### Syntax
```
[no] redistribute <kernel | connected | static | rip | ospf | isis | babel> route-map <name>
```
#### Description
This command configures the redistribution of routes of the specified protocol or kind into BGP, filtering the routes using the given route-map if specified.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *name*  | Optional | String of maximum length of 80 chars | Route-map name |
| **no** | Optional | Literal | Removes the redistribution of routes into BGP |

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

### BGP Neighbor
#### neighbor remote-as

##### Syntax
```
[no] neighbor <A.B.C.D> remote-as <asn>
```

##### Description
This command creates a neighbor whose remote-as is *asn*, an autonomous system number. Currently only an IPv4 address is supported.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | Peer IPv4 address |
| *asn* | Required| 1 - 4294967295 |  The autonomous system number of the peer |
| **no** | Optional | Literal | Deletes a configured BGP peer|

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
admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | Peer IPv4 address |
| *text* | Required| String of maximum length 80 chars| Description of the peer |
| **no** | Optional | Literal | Deletes the peer description|

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
admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | Peer IPv4 address |
| *text* | Required| String of maximum length 80 chars| Password for peer connection |
| **no** | Optional | Literal | Disables authentication for the peer connection|

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
admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *Keepalive*  | Required | 0 - 65535 | The keepalive interval in seconds |
| *holdtime* | Required| 0 - 65535 | Hold time in seconds |
| **no** | Optional | Literal | Resets the keepalive and hold time values to their default values which is 0  |

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
admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | Peer IPv4 address |
| *val* | Required| 1-10| Number of times BGP can allow an instance of AS to be in the AS_PATH  |
| **no** | Optional | Literal | Clears the state |

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
admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | Peer IPv4 address |
| **no** | Optional | Literal |Resets to a cleared state (default) |

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
| *A.B.C.D*  | Required | A.B.C.D | Peer IPv4 address |
| **no** | Optional | Literal |Resets to a cleared state (default) |

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
This command shuts down the peer. When you want to preserve the neighbor configuration, but want to drop the BGP peer state, use this syntax.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | Peer IPv4 address |
| **no** | Optional | Literal | Deletes the neighbor state of the peer |

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
admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | Peer IPv4 address |
| *name*  | Required | String of maximum length of 80 chars | Peer-Group name |
| **no** | Optional | Literal |Removes the neighbor from the peer-group |

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
admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | Peer IPv4 address |
| *name*  | Required | String of maximum length of 80 chars | Route-map name |
| **no** | Optional | Literal |Removes the route-map for this neighbor |

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
This command sets advertisement interval for route updates for specified neighbor with ipv4 and ipv6 address.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | Peer IPv4 address |
| *X:X::X:X*  | Optional | X:X:X:X | Peer IPv6 address |
| *interval* | Required| 0-600 |  The time interval for sending BGP routing updates in secs |
| **no** | Optional | Literal | Deletes advertisement interval for configured BGP peer|

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

#### neighbor interface

##### Syntax
```
[no] neighbor <A.B.C.D|X:X::X:X> interface <ifname>
```

##### Description
This command is used when connecting to a BGP peer over an IPv6 link-local address. This command  may be deprecated in future releases.
##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | Peer IPv4 address |
| *X:X::X:X*  | Optional | X:X:X:X | Peer IPv6 address |
| *ifname* | Required|  ifname |  Interface connecting to neighboring peer |
| **no** | Optional | Literal | Deletes interface used to connect to a BGP peer over an IPv6 link-local address |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 2001:db8:0:1 interface eth0
s1(config-router)# no neighbor 2001:db8:0:1 interface eth0
```

#### neighbor strict-capability-match

##### Syntax
```
[no] neighbor <A.B.C.D|X:X::X:X> strict-capability-match
```

##### Description
This command strictly compares remote capabilities and local capabilities with specified BGP peer. If capabilities are different, Unsupported Capability error is sent and connection is reset.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | Peer IPv4 address |
| *X:X::X:X*  | Optional | X:X:X:X | Peer IPv6 address |
| **no** | Optional | Literal | Deletes state of local and remote capabailites comparison with neighboring BGP peer |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 2001:db8:0:1 strict-capability-match
s1(config-router)# no neighbor 2001:db8:0:1 strict-capability-match
```
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.1 strict-capability-match
s1(config-router)# no neighbor 9.0.0.1 strict-capability-match
```

#### neighbor activate

##### Syntax
```
[no] neighbor <A.B.C.D|X:X::X:X|WORD> activate
```

##### Description
This command activates specified neighboring peer to facilitate multicast routing updates.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | Peer IPv4 address |
| *X:X::X:X*  | Optional | X:X:X:X | Peer IPv6 address |
| *WORD*  | Optional | WORD | Peer group name |
| **no** | Optional | Literal | Disables exchange of multicast routing updates with neighboring BGP peer |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 2001:db8:0:1 activate
s1(config-router)# no neighbor 2001:db8:0:1 activate
```
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.1 activate
s1(config-router)# no neighbor 9.0.0.1 activate
```

#### neighbor capability dynamic

##### Syntax
```
[no] neighbor <A.B.C.D|X:X::X:X|WORD> capability dynamic
```

##### Description
This command facilitates support of negotiation of capabilities (sending new capabilities or removing previously negotiated capabilities) without performing a hard clear of the BGP session; the capability data field includes a list of capabilities that can be dynamically negotiated.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | Peer IPv4 address |
| *X:X::X:X*  | Optional | X:X:X:X | Peer IPv6 address |
| *WORD*  | Optional | WORD | Peer group name |
| **no** | Optional | Literal | Disables negotiation of capabilities with neighboring BGP peer |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 2001:db8:0:1 capability dynamic
s1(config-router)# no neighbor 2001:db8:0:1 capability dynamic
```
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.1 capability dynamic
s1(config-router)# no neighbor 9.0.0.1 capability dynamic
```

#### neighbor capability orf

##### Syntax
```
[no] neighbor <A.B.C.D|X:X::X:X|WORD> capability orf prefix-list <both|send|receive>
```

##### Description
This command facilitates support of cooperative route filtering to install a BGP speaker inbound route filter as an outbound route filter on the peer. Installs the filter (any inbound prefix list or distribute list) as an outbound prefix list.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | Peer IPv4 address |
| *X:X::X:X*  | Optional | X:X:X:X | Peer IPv6 address |
| *WORD*  | Optional | WORD | Peer group name |
| *both* | Required | Literal | Facilitates both send and receive of BGP speakers router filter with neighboring BGP peer |
| *send* | Required | Literal | Facilitates send of BGP speakers router filter to neighboring BGP peer |
| *receive*  |  Required  |  Literal | Facilitates reception of BGP speakers router filter from neighboring BGP peer |
| **no** | Optional | Literal | Disables negotiation of capabilities with neighboring BGP peer |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 2001:db8:0:1 capability orf prefix-list both
s1(config-router)# no neighbor 2001:db8:0:1 capability orf prefix-list both
```
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.1 capability orf prefix-list both
s1(config-router)# no neighbor 9.0.0.1 capability orf prefix-list both
```


#### neighbor dont-capability-negotiate

##### Syntax
```
[no] neighbor <A.B.C.D|X:X::X:X|peer-group-name> dont-capability-negotiate
```

##### Description
This command  suppresses sending of capability negotiation as OPEN message optional parameter to the peer. This command only affects the peer is configured other than IPv4 unicast configuration.
When remote peer does not have capability negotiation feature, remote peer will not send any capabilities at all. In that case, bgp configures the peer with configured capabilities.
Locally configured capabilities are preferred to negotiated capabilities even though remote peer sends capabilities.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D* | Required | A.B.C.D  | Peer IPv4 address |
| *X:X::X:X*| Required | X:X::X:X | Peer IPv6 address |
| *peer-group-name* | Required | String of maximum length 80 characters  | Peer group name |
| **no** | Optional | Literal | Disables suppression of capability negotiation |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 2001:db8:0:1 dont-capability-negotiate
s1(config-router)# no neighbor 2001:db8:0:1 dont-capability-negotiate
```
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.1 dont-capability-negotiate
s1(config-router)# no neighbor 9.0.0.1 dont-capability-negotiate
```

#### neighbor override-capability

##### Syntax
```
[no] neighbor <A.B.C.D|X:X::X:X|peer-group-name> override-capability
```

##### Description
This command overrides the result of capability negotiation with local configuration to ignore remote peer`s capability value.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D* | Required | A.B.C.D  | Peer IPv4 address |
| *X:X::X:X*| Required | X:X::X:X | Peer IPv6 address |
| *peer-group-name* | Required | String of maximum length 80 characters  | Peer group name |
| **no** | Optional | Literal | Disables capabilities override of BGP peer |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 2001:db8:0:1 override-capability
s1(config-router)# no neighbor 2001:db8:0:1 override-capability
```
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.1 override-capability
s1(config-router)# no neighbor 9.0.0.1 override-capability
```

#### neighbor ebgp-multihop
##### Syntax
```
[no] neighbor <A.B.C.D | X:X::X:X | peer_group_name> ebgp-multihop <1-255>
```
##### Description
This command attempts BGP connections with external AS routers that are not directly connected.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | Peer IPv4 address |
| *X:X::X:X*  | Required | X:X::X:X | Peer IPv6 address |
| *peer_group_name*  | Required | String of maximum length 80 chars| Peer-group name |
| *<1-255>*  | Optional | 1-255 | Time-to-live hop count value |
| **no** | Optional | Literal |Removes the ebgp-multihop configuration for this neighbor |

##### Examples
```
s1(config-router)# neighbor 10.0.2.15 ebgp-multihop
s1(config-router)# neighbor 10.0.2.15 ebgp-multihop 255
s1(config-router)# no neighbor 10.0.2.15 ebgp-multihop
```

#### neighbor filter-list
##### Syntax
```
[no] neighbor <A.B.C.D|X:X::X:X|WORD> filter-list WORD (in|out)
```
##### Description
This command applies a filter-list on the neighbor to filter incoming and outgoing routes.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | Peer IPv4 address |
| *X:X::X:X*  | Optional | X:X:X:X | Peer IPv6 address |
| *WORD*  | Optional | WORD | Neighbor tag |
| *WORD*  | Required | WORD | AS path access-list name |
| *in*  | Optional | in | Filter incoming routes |
| *out*  | Optional | out | Filter outgoing routes |

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
This command applies a prefix-list on the neighbor to filter updates to and from the neighbor.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | Peer IPv4 address |
| *X:X::X:X*  | Optional | X:X:X:X | Peer IPv6 address |
| *WORD*  | Optional | WORD | Neighbor tag |
| *WORD*  | Required | WORD | Name of a prefix list |
| *in*  | Optional | in | Filter incoming routes |
| *out*  | Optional | out | Filter outgoing routes |

##### Examples
```
s1(config-router)# neighbor 10.23.4.2 prefix-list abc in
s1(config-router)# no neighbor 10.23.4.2 prefix-list abc in
```

#### neighbor send-community
##### Syntax
```
[no] neighbor (A.B.C.D|X:X::X:X|WORD) send-community (both|extended|standard)
```
##### Description
This command allows to specify that a communities attribute should be sent to a BGP neighbor.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | Peer IPv4 address |
| *X:X::X:X*  | Optional | X:X:X:X | Peer IPv6 address |
| *WORD*  | Optional | WORD | Neighbor tag |
| *both*  | Optional | both | Send Standard and Extended Community attributes |
| *extended*  | Optional | extended | Send Extended Community attributes |
| *standard*  | Optional | standard | Send Extended Community attributes |

##### Examples
```
s1(config-router)# neighbor 172.16.70.23 send-community
s1(config-router)# no neighbor 172.16.70.23 send-community
```

#### neighbor soft-reconfiguration
##### Syntax
```
[no] neighbor (A.B.C.D|X:X::X:X|WORD) soft-reconfiguration inbound
```
##### Description
This command is to allow inbound soft reconfiguration for this neighbor.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | Peer IPv4 address |
| *X:X::X:X*  | Optional | X:X:X:X | Peer IPv6 address |
| *WORD*  | Optional | WORD | Neighbor tag |

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
This command allows to specify the maximum number of hops to the BGP peer.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | Peer IPv4 address |
| *X:X::X:X*  | Optional | X:X:X:X | Peer IPv6 address |
| *WORD*  | Optional | WORD | Neighbor tag |
| *<1-254>*  | Required | 1-254 | Hop count |

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
This command allows to specify the source address to use for the BGP session to the neighbour.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | Peer IPv4 address |
| *X:X::X:X*  | Optional | X:X:X:X | Peer IPv6 address |
| *WORD*  | Optional | WORD | Neighbor tag |
| *A.B.C.D*  | Optional | A.B.C.D | IPv4 address |
| *X:X::X:X*  | Optional | X:X:X:X | IPv6 address |
| *WORD*  | Optional | WORD | Interface name |

##### Examples
```
s1(config-router)# neighbor 10.0.0.1 update-source loopback0
s1(config-router)# no neighbor 10.0.0.1 update-source loopback0
```

### AS-Path Access List Configuration Command
#### Syntax
```
[no]  ip as-path access-list WORD <deny|permit> .LINE
```

#### Description
This command facilitates configuration of access lists based on autonomous system path that enable to control routing updates based on BGP autonomous paths information. Access lists are filters that enable to restrict the routing information a router learns or advertises to and from a neighbor.Multiple BGP peers or route maps can reference a single access list. These access lists can be applied to both inbound route updates and outbound route updates. Each route update is passed through the access-list. BGP applies each rule in the access list in the order it appears in the list. When a route matches any rule, the decision to permit the route through the filter or deny is made, and no further rules are processed.A regular expression is a pattern used to match against an input string. In BGP, one can build a regular expression to match information about an autonomous system path.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length 80 characters | Access list name |
| **deny** | Required | Literal | Deny access for matching conditions |
| **permit** | Required | Literal | Permit access for matching conditions |
| *.LINE* | Required | String of maximum length of 80 characters | Autonomous system in the access list in form of regular expression |
| **no** | Optional | Literal | Disables access list rule |

#### Examples
```
s1(config)#ip as-path access-list 1 permit _234_
s1(config)#ip as-path access-list 1 permit _345_
s1(config)#ip as-path access-list 1 deny any
```

## Route Map Configuration Commands

### Route Map
#### Syntax
```
[no] route-map WORD <deny|permit> <order>
```

#### Description
This command configures the order of the entry in the route-map name with the Match Policy of either permit or deny.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length of 80 chars | Route-map name |
| *order*  | Required |1-65535| Order number of the route-map |
| **deny** | Required | Literal | Denies the order of the entry |
| **permit** | Required | Literal | Permits the order of the entry |
| **no** | Optional | Literal |Deletes the route-map |

#### Examples
```
s1(config)# route-map rm1 deny 1
```

### Route Map Match
#### match prefix-list

##### Syntax
```
[no] match ip address prefix-list WORD
```

##### Description
This command configures a match clause for route map to distribute any routes that have a destination network number address that is permitted by a prefix-list.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length of 80 chars | IP prefix-list name |
| **no** | Optional | Literal |Deletes match clause for route-map |

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
This command is used to match a BGP autonomous system path access list.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | AS path access-list name |
| **no** | Optional | Literal | Delete the AS path access list entry|

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
To match a BGP community, use this command in route-map configuration mode.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-99>*  | Optional | 1-99 | Community-list number (standard) |
| *<100-500>*  | Optional | 100-500 | Community-list number (expanded) |
| *WORD*  | Optional | WORD | Community-list name |
| **no** | Optional | Literal | Removes the match community entry |

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
To match a BGP community with an exact match of communities.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-99>*  | Optional | 1-99 | Community-list number (standard) |
| *<100-500>*  | Optional | 100-500 | Community-list number (expanded) |
| *WORD*  | Optional | WORD | Community-list name |
| *exact-match*  | Required | exact-match | Do exact matching of communities |
| **no** | Optional | Literal | Removes the match entry for exact match community |

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
Use this command in route-map mode to match BGP extended community list attributes.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-99>*  | Optional | 1-99 | Extended Community-list number (standard) |
| *<100-500>*  | Optional | 100-500 | Extended Community-list number (expanded) |
| *WORD*  | Optional | WORD | Extended Community-list name |
| **no** | Optional | Literal | To remove the BGP extended community list attribute entry |

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
This command is used to distribute routes that have their next hop out of the interface specified.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | Interface name |
| **no** | Optional | Literal | To remove match interface entry |

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
To distribute any routes that have a destination network number address that is permitted by a standard or extended access list.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-199>*  | Optional | 1-199 | IP access-list number |
| *<1300-2699>*  | Optional | 1300-2699 | IP access-list number (expanded range) |
| *WORD*  | Optional | WORD | IP access-list name |
| **no** | Optional | Literal | To remove match ip address entry |

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
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | IP prefix-list name |
| **no** | Optional | Literal | To remove match ip address prefix list entry |

##### Examples
```
s1(config-route-map)# match ip address prefix-list pl1
s1(config-route-map)# no match ip address prefix-list pl1
s1(config-route-map)# no match ip address prefix-list
```

#### match ip nexthop
##### Syntax
```
[no] match ip next-hop (<1-199>|<1300-2699>|WORD)
```

##### Description
To redistribute any routes that have a next hop router address passed by one of the access lists specified.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-199>*  | Optional | 1-199 | IP access-list number |
| *<1300-2699>*  | Optional | 1300-2699 | IP access-list number (expanded range) |
| *WORD*  | Optional | WORD | IP access-list name |
| **no** | Optional | Literal | To delete match ip next-hop entry |

##### Examples
```
s1(config-route-map)# match ip next-hop 100
s1(config-route-map)# no match ip next-hop 100
s1(config-route-map)# no match ip next-hop
```

#### match ip nexthop prefix-list
##### Syntax
```
[no] match ip next-hop prefix-list WORD
```

##### Description
To redistribute any routes that have a next hop router address passed by one of the prefix lists specified.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | IP prefix-list name |
| **no** | Optional | Literal | To remove match ip next hop prefix list entry |

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
To redistribute routes that have been advertised by routers and access servers at the address specified by the access lists.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-199>*  | Optional | 1-199 | IP access-list number |
| *<1300-2699>*  | Optional | 1300-2699 | IP access-list number (expanded range) |
| *WORD*  | Optional | WORD | IP access-list name |
| **no** | Optional | Literal | To remove match ip route source entry |

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
To redistribute routes that have been advertised by routers and access servers at the address specified by the prefix lists.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | IP prefix-list name |
| **no** | Optional | Literal | To remove match ip route source prefix list entry |

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
To distribute IPv6 routes that have a prefix specified by an IPv6 access list.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | IPv6 access-list name |
| **no** | Optional | Literal | To remove the match ipv6 address entry |

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
To distribute IPv6 routes that have a prefix specified by an IPv6 prefix list.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | IPv6 prefix list |
| **no** | Optional | Literal | To remove the match ipv6 address prefix list entry |

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
To distribute IPv6 routes that have a specified next hop.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *X:X::X:X*  | Required | X:X::X:X | IPv6 address of next hop |
| **no** | Optional | Literal | To remove match ipv6 next hop entry |

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
To redistribute routes with the metric specified.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<0-4294967295>*  | Required | 0-4294967295 | Metric value |
| **no** | Optional | Literal | To remove match metric entry |

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
To match BGP routes based on the origin of the route specified.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *egp*  | Optional | egp | Remote egp |
| *igp*  | Optional | igp | Local igp |
| *incomplete*  | Optional | incomplete | Unknown heritage |
| **no** | Optional | Literal | To remove match origin entry |

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
To match BGP routes based on the peer address.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | IPv4 address of peer |
| *X:X::X:X*  | Optional | X:X::X:X | IPv6 address of peer |
| **no** | Optional | Literal | To remove the match peer entry |

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
To match BGP routes against static or redistributed routes.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *local*  | Required | local | Static or redistributed routes |
| **no** | Optional | Literal | To remove match peer local entry |

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
To match portion of BGP routes defined by percentage value

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<0-100>*  | Required | 0-100 | Percentage of routes |
| **no** | Optional | Literal | To remove match probability entry |

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
To match the tag of route.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<0-65535>*  | Required | 0-65535 | Tag value |
| **no** | Optional | Literal | To remove match tag entry |

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
To initialize exit policy on matches to goto clause.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-65535>*  | Required | 1-65535 | Goto clause number |
| **no** | Optional | Literal | To deinitialize exit policy  |

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
To initialize exit policy on matches to next clause.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | To deinitialize exit policy |

##### Examples
```
s1(config-router)# on-match next
s1(config-router)# no on-match next
```

### Route Map Set
#### Syntax
```
Route-map Command: [no] set community <AA:NN> [additive]
Route-map Command: [no] set metric <val>
```

#### Description
Use the `set community` command to set the BGP community attribute. Use the `set metric` command to set the BGP attribute MED.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *AA:NN*  | Required | AS1:AS2 where AS is 1 - 4294967295 | Sets BGP community attribute |
| *val*  | Required |0-4294967295  | Sets metric value |
| **no** | Optional | Literal |Clears community attribute |

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

#### Description
This command sets the originating AS of an aggregated route. The value specifies at which AS the aggregate route originated. The range is from 1-4294967295. The set-aggregator-ip value must also be set to further identify the originating AS.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value*  | Required | Integer in range <1-4294967295> | AS value |
| *A.B.C.D* | Required | String of maximum length 80 characters | ipv4 address of AS |
| **no** | Optional | Literal |Clears aggregator config for route-map |

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
Exclude the given AS number from the AS_PATH

##### Authority
admin

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value*  | Required | Integer in range <1-4294967295> | AS value to be excluded from AS path |
| **no** | Optional | Literal | Clears exclusion for as value from as path for route-map |

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
Prepend the given AS number to the AS_PATH

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value*  | Required | Integer in range <1-4294967295> | AS value to be added to AS path |
| **no** | Optional | Literal | Clears as value from as path for route-map |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set as-path prepend 2
```

#### set atomic aggregate
##### Syntax
```
[no] set atomic-aggregate
```

##### Description
This command enables warning to upstream routers through the ATOMIC_AGGREGATE attribute that address aggregation has occurred on an aggregate route.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Disables route-aggregation notification to upstream neighbor for route-map |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set atomic-aggregate
```

#### set community list delete
##### Syntax
```
[no] set comm-list <list-name> delete
```

##### Description
This command removes the COMMUNITY attributes from the BGP routes identified in the specified community list. Deletes matching communities for route-map.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *list-name* | Required | Integer in range <1-99> or <100-500> or valid community string not exceeding 80 characters |Community list name
| **no** | Optional | Literal | Deletes configuration for community-list exclusion under route map |

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
This command sets COMMUNITY attributes for the route-map. Community number is in aa:nn format or local-AS|no-advertise|no-export|internet or additive or none.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *list-name* | Required | Integer in range <1-99> or <100-500> or valid community string not exceeding 80 characters |Community list name
| **no** | Optional | Literal | Deletes configuration for community-list under route map |

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
This command sets the target extended community (in decimal notation) of a BGP route. The COMMUNITY attribute value has the syntax AA:NN, where AA represents an AS, and NN is the community identifier.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *asn-community-identifier* | Required |                           AS1:AS2 where AS is 1 - 4294967295 , String not exceeding 80 characters | Community attribute in form of AA:nn or IP address:nn |
| **no** | Optional | Literal | Deletes configuration for rt extended community-list under route map |

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
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *asn-community-identifier* | Required |                        AS1:AS2 where AS is 1 - 4294967295, String not exceeding 80 characters |Community attribute in form of AA:nn or IP address:nn |
| **no** | Optional | Literal | Deletes configuration for site-of-origin extended community-list under route map |

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
This command sets the ip address for next-hop.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D* | Required | A.B.C.D |IPV4 address, string not exceeding 80 characters |
| **no** | Optional | Literal | Unsets next hop ip address for route map |

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
In BGP routing protocol, the update from the external AS will contains the next hop address of the external hop itself. Therefore, when the router receives the update from the external AS and advertises the update to the other routers via iBGP, the other routers will see the next hop of the advertised networks via the external router IP address.

This command enables iBGP learn router to forward the packet to its peer address instead of the external router IP address.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Unsets next hop to peer ip address for route map |

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
This command sets the BGP-4+ global IPv6 nexthop address.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *X:X::X:X*  | Required | X:X::X:X | ipv6 address
| **no** | Optional | Literal | Unsets BGP-4+ global IPv6 nexthop address for route map |

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
This command sets the BGP-4+ link-local IPv6 nexthop address.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *X:X::X:X*  | Required | X:X::X:X | ipv6 address
| **no** | Optional | Literal | Unsets BGP-4+ link-local IPv6 nexthop address for route map |

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
This command sets the BGP local preference.This command sets the loca preference value of an IBGP route. The value is advertised to IBGP peers. The range is from 0 to 4 294 967 295. A higher number signifies a preferred route among multiple routes to the same destination.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value* | Required | Integer in range <0-4294967295>  | ipv6 address
| **no** | Optional | Literal | Unsets BGP local preference for route map |

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
This command specifies the relative change of metric and which is used with BGP route advertisement. It can take the current metric of a route and increase or decrease it by a specified value before it propagates it.If the value is specified as negative and ends up being negative after metric decrease, the value would be interpreted as an increase in metric.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *expr* | Required | String of not more than 80 characters  | metric expression
| **no** | Optional | Literal | Unsets BGP local preference for route map |

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
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| **type-1** | Required | Literal  | Specifies type-1 metric |
| **type-2** | Required | Literal  | Specifies type-2 metric |
| **no** | Optional | Literal | Unsets BGP metric type for route map |

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
egp  set the value to the NLRI learned from the Exterior Gateway Protocol (EGP).
igp  set the value to the NLRI learned from a protocol internal to the originating AS.
incomplete  if not egp or igp.
NLRI- Network Layer reachablility Info.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| **egp** | Required | Literal  | Specifies type-1 metric |
| **igp** | Required | Literal  | Specifies type-2 metric |
| **incomplete** | Required | Literal  | Specifies type-2 metric |
| **no** | Optional | Literal | Unsets BGP origin attribute for route map |

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
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | IPv4 address |
| **no** | Optional | Literal | Unsets BGP originator-id attribute for route map |

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
This command sets the preferred source address for matching routes when installing in the kernel, within a route-map.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | IPv4 address |
| **no** | Optional | Literal | Unsets BGP src attribute for route map |

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
This command sets the tag for redistributions, that external routers use to filter incoming distributions of
route-maps.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value*  | Required | Integer in range <0-65535> | tag value |
| **no** | Optional | Literal | Unsets BGP tag attribute for route map |

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
This command sets next-hop ip address for vpnv4 updates.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | ipv4 address |
| **no** | Optional | Literal | Unsets vpnv4 next-hop attribute for route map |

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
admin

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value*  | Required | Integer in range <1-4294967295> | weight value |
| **no** | Optional | Literal | Unsets weight attribute for route map |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)# set weight 9
```

### Route Map Description
#### Syntax
```
Route-map Command: [no] description <text>
```

#### Description
Sets Route-map description.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *text*  | Required | String of maximum length of 80 chars | Route-map description |
| **no** | Optional | Literal |Clears description for route-map |

#### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)# description rmap-mcast
```

### Route Map Call
#### Syntax
```
[no] call WORD
```
#### Description
To jump to another route-map after match and set.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | Target route-map name |
| **no** | Optional | Literal | To disable jumping to another route-map |

#### Examples
```
s1(config-route-map)# call rmap
s1(config-route-map)# no call
```

### Route Map Continue
#### Syntax
```
[no] continue <1-65535>
```

#### Description
To continue on a different entry within the route-map

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-65535>*  | Required | 1-65535 | Route-map entry sequence number |
| **no** | Optional | Literal | To disable continuing on a different entry |

#### Examples
```
s1(config-route-map)# continue 300
s1(config-route-map)# no continue 300
s1(config-route-map)# no continue
```

## IP Prefix-list Configuration Commands
###  IPv4 prefix-list
#### Syntax
```
[no] ip prefix-list WORD seq <num> (deny|permit) <A.B.C.D/M|any>
[no] ip prefix-list WORD seq <num> (deny|permit) A.B.C.D/M le <0-32> ge <0-32>
[no] ip prefix-list WORD seq <num> (deny|permit) A.B.C.D/M ge <0-32>
[no] ip prefix-list WORD seq <num> (deny|permit) A.B.C.D/M le <0-32>
```

#### Description
The `ip prefix-list` command provides a powerful prefix-based filtering mechanism. It has prefix length range  and sequential number specifications. You can add or delete prefix-based filters to arbitrary points of a prefix-list by using a sequential number specification. If `no ip prefix-list` is specified, it acts as permit. If `ip prefix-list` is defined, and no match is found, the default deny is applied.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *name*  | Required | String of maximum length of 80 chars | IP prefix-list name |
| *num*  | Required | 1-4294967295 | Sequence number |
| *A.B.C.D/M*  | Required | A.B.C.D/M | IPv4 prefix |
| *0-32*  | Required | 0-32 | Minimum prefix length to be matched |
| *0-32*  | Required | 0-32 | Maximum prefix length to be matched |
| **no** | Optional | Literal |Deletes IP prefix-list |

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
The `ipv6 prefix-list` command provides IPv6 prefix-based filtering mechanism. Descriptions may be added to prefix lists. "description" command  adds a description to the prefix list. "ge" command specifies prefix length and  the prefix list will be applied if the prefix length is greater than or equal to the "ge" prefix length. "le" command specifies prefix length and the prefix list will be applied if the prefix length is less than or equal to the "le" prefix length. If `no ipv6 prefix-list` is specified, it acts as permit. If `ipv6 prefix-list` is defined, and no match is found, the default deny is applied.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length of 80 chars | IP prefix-list name |
| *num*  | Required | 1-4294967295 | Sequence number |
| *.LINE*  | Required | String of maximum length of 80 chars | Prefix list description |
| *X:X::X:X/M*  | Required | X:X::X:X/M | IPv6 prefix |
| *length* | Required | 0-128 | Prefix length |
| **no** | Optional | Literal | Deletes IPv6 prefix-list |

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


## Community Lists Configuration Commands

#### Syntax
```
[no] ip  community-list WORD <deny|permit> .LINE
```

#### Description
This command defines a new  community list. LINE is a string expression of communities attribute. LINE can include regular expression to match communities attribute in BGP updates. The community is compiled into community structure. We can define multiple community list under same name. In that case match will happen user defined order. Once the community list matches to communities attribute in BGP updates it return permit or deny by the community list definition. When there is no matched entry, deny will be returned. When community is empty it matches to any routes.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length 80 characters | Community list name |
| **deny** | Required | Literal | Deny access for matching conditions |
| **permit** | Required | Literal | Permit access for matching conditions |
| *.LINE* | Required | String of maximum length of 80 characters |Community numbers specified as regular expressions |
| **no** | Optional | Literal | Deletes rule for specified community |

#### Examples
```
S1(config)#ip community-list EXPANDED permit [1-2]00
S1(config)#ip community-list ANY-COMMUNITIES deny ^0:.*_
S1(config)#ip community-list ANY-COMMUNITIES deny ^65000:.*_
S1(config)#ip community-list ANY-COMMUNITIES permit .*
```


## Extended Community Lists Configuration Commands
#### Syntax
```
[no] ip extcommunity-list WORD <deny|permit> .LINE
```
#### Description
This command defines a new expanded extended community list.  LINE is a string expression of extended communities attribute and can include regular expression to match extended communities attribute in BGP updates.
#### Authority
admin
#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length of 80 chars | Extended community list name |
| *.LINE*  | Required | String of maximum length of 80 chars | String expression of extended communities attribute |
| **deny** | Required | Literal | Deny access for matching conditions |
| **permit** | Required | Literal | Permit access for matching conditions |
| **no** | Optional | Literal | Deletes extended community list |

#### Examples
```
s1(config)# ip extcommunity-list expanded ROUTES permit REGULAR_EXPRESSION
s1(config)# no ip extcommunity-list expanded ROUTES
```

##Display Commands

### show ip bgp
#### Syntax
```
show ip bgp [A.B.C.D][A.B.C.D/M]
```

#### Description
This command displays BGP routes from the BGP Route table. When no route is specified, all IPv4 routes are displayed.

#### Authority
admin

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | IPv4 prefix |
| *A.B.C.D/M*  | Optional | A.B.C.D/M | IPv4 prefix with prefix length |

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
admin

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
admin

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

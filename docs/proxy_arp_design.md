# Proxy ARP and Local proxy ARP Design

## Contents
   - [High level design](#high-level-design)
   - [Design choices](#design-choices)
   - [Internal structure](#internal-structure)
   - [OVSDB schema](#ovsdb-schema)
    - [Proxy ARP](#proxy-arp)
    - [Local Proxy ARP](#local-proxy-arp)
   - [References](#references)


## High level design

Proxy ARP is a technique by which a device on a given network answers the ARP queries for a network address that is not on that network. The ARP proxy is aware of the location of the traffic's destination, and offers its own MAC address as the final destination.

Local proxy ARP feature is used to enable an interface-local proxying of ARP requests. Enabling of local proxy ARP will make the router answer all ARP requests on configured subnet.The local proxy ARP feature can be used without enabling the IP proxy ARP feature.

OpenSwitch uses the native support in the Linux kernel for implementing the proxy ARP and local proxy ARP feature.

Here are some key aspects about these features:
	* The features can be enabled on the following types of interfaces:
	   - L3 port
	   - L3 split port
	   - L3 VLAN interface
	* The features cannot be enabled on the following types of interfaces:
	   - L2 interface
	   - Sub-interface
	   - Loopback interface
	* The features are restricted to data plane interfaces. It cannot be enabled on an out of band management interface.
	* The features are disabled by default on all interfaces.
	* OpenSwitch OVSDB table 'Port' stores the state of the feature on a per port basis.
	* The ops-portd daemon is responsible to listen to state changes of the feature and update the kernel.
	* Routing has to be enabled on the interface for the features to be enabled.

## Design choices
N/A

## Internal structure
```ditaa
                            +-------------------+
                            | Management Daemons|
                            |  (CLI, REST, etc.)|
                            |                   |
                            +-------+-----------+
                                    |
                                    |
                      +-------------+----------------+
                      |             |          OVSDB |
                      |             |                |
                      |      +----------------+      |
                      |      |                |      |
                      |      |   Port Table   |      |
                      |      |                |      |
                      |      |                |      |
                      |      +----------------+      |
                      |              |               |
                      +--------------+---------------+
                                     |
                                     |
                                +----+-----+
                                |          |
                                |ops-portd |
                                |          |
                                |          |
                                +----+-----+
                                     |
                                     |
                            +--------+---------+
                            |                  |
                            |                  |
                            |     Kernel       |
                            |                  |
                            |                  |
                            +------------------+

```

#### Management daemons
Management daemons refers to the components through which the device can be configured. This can be in the form of CLI, REST APIs, etc. Proxy ARP and local proxy ARP will be configured from one of the Management daemons. Proxy ARP and local proxy ARP state will be populated in the **'Port'** table of OVSDB.

#### OVSDB
Communication between management daemon and the portd daemon is facilitated through OVSDB. **'Port'** table is used in OVSDB for proxy ARP and local proxy ARP support.

#### ops-portd
ops-portd daemon is responsible for updating the status of proxy ARP and local proxy ARP on an interface in the kernel on getting the notification from OVSDB.

## OVSDB Schema
####Proxy ARP
In the OVSDB table **'Port'**, a {key, value} pair in **other_config** column with **proxy_arp_enabled** as the key and type **boolean** as the value tracks the state of the feature.

####Local proxy ARP
In the OVSDB table **'Port'**, a {key, value} pair in **other_config** column with **local_proxy_arp_enabled** as the key and type **boolean** as the value tracks the state of the feature.

## References
[Linux_proxy_arp]http://www.linuxproblem.org/art_8.html
[RFC 1027]https://tools.ietf.org/html/rfc1027

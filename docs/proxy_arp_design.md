# Proxy ARP Design

## Contents
   - [High level design](#high-level-design)
   - [Design choices](#design-choices)
   - [Internal structure](#internal-structure)
   - [OVSDB schema](#ovsdb-schema)
   - [References](#references)

## High level design
Proxy ARP is a technique by which a device on a given network answers the ARP queries for a network address that is not on that network. The ARP Proxy is aware of the location of the traffic destination, and offers its own MAC address as destination.

OpenSwitch uses the native support in the Linux kernel for implementing the Proxy ARP feature.

Here are some key aspects about the feature:
	* The feature can be enabled on a per interface basis.
	* The feature is disabled by default on all interfaces.
	* OpenSwitch OVSDB table 'Port' stores the state of the feature on a per port basis.
	* The ops-portd daemon is responsible to listen to state changes of the feature and update the kernel.
	* Routing has to be enabled on the interface for the feature to work. Else the feature is inactive.

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

## OVSDB Schema
In the OVSDB table **'Port'**, a {key, value} pair in **other_config** column with **proxy_arp_enabled** as the key and type **boolean** as the value tracks the state of the feature.

## References
[Linux_proxy_arp]http://www.linuxproblem.org/art_8.html
[RFC 1027]https://tools.ietf.org/html/rfc1027

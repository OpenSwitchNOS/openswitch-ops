# Basic Layer3 Design#

#Introduction#

In the modern day hyperscale datacenter, routing, as opposed to switching, is the latest trend. In the past, routing was limited to aggregation and core devices, but modern day datacenters have routing enabled as deep as the Top of Rach (TOR) switches. The most common use case is to have the uplinks (links facing the aggregation and core devices) participating in layer3 while the downlinks (links facing the servers) still use traditional layer 2 switching. As more customers redesign their datacenters to use layer3, the TOR switches should be fully capable of behaving as a layer3 device.

Openswitch is designed to support layer3 features and protocols.
To facilitate this, the following capabilities have been added.

- **VRF support**
- **Layer3 Interfaces**
- **Static Routes**
- **Slow-path Routing (Routing in kernel)**
- **Fast-path Routing (Hardware based routing)**
- **Equal Cost Multipath (ECMP)**
- **Vlan Interfaces**
- **InterVLAN Routing**

## VRF##
Virtual Routing and Forwarding (VRF) is used in switches with multi-tenancy hosting. Each tenant is isolated from the other tenants on the switch. This way a single physical switch can virtually host multiple routers. Each VRF maintains its own routing tables, neighbor tables, physical and virtual interfaces etc. Support for VRF is built into Openswitch. However in the first phase, this support is restricted to only one "default" vrf although the architecture is designed to support multiple vrf.

###Linux Network Namespaces###
Openswitch leverages the concept of Linux network namespaces to completely isolate VRFs. Namespaces can be used to isolate routing tables, neighbor tables etc. Extensive information about namespaces is available on the web. For basic reference: http://man7.org/linux/man-pages/man7/namespaces.7.html

## Layer3 Interfaces##
Layer3 interfaces are critical in most modern day datacenters. They are heavily used in TOR uplinks and uplinks and downlinks in the spine. In Openswitch, a physical layer3 interface has the following properties

- Port has an IP address and mask.
- Port does not have any layer2 configuration.
- Port is part of a VRF (default VRF in the initial phase). This port is not part of any bridge.
- Packets arriving at this interface will have a destination MAC matching one of the device MAC.

## InterVLAN Routing##
InterVLAN routing is important in scenarios where routing is needed between 2 different VLANs on a switch. When a packet is ingressing and egressing on physical interfaces which are layer2 and both the interfaces are participating in different VLANs, routing between these VLANs is achieved by creating 2 logical interfaces. These logical interfaces have the following properties:

- Each logical interface is associated with one of the VLANs.
- Logical interface is associated with a bridge. This is a internal bridge created solely for isolating vlan traffic to the logical interfaces.
- Switching happens between the physical layer2 interface and the corresponding logical interface in that VLAN
- Logical interface has IP address and associated with a VRF.
- Routing happens between the 2 logical interfaces.

## ECMP ##
Equal Cost Multipath is a scenario where a single prefix can have multiple "Equal Cost" route nexthops. Openswitch supports 32 ECMP nexthops per prefix in the initial phase. Openswitch supports ECMp for IPv4 prefixes in the inital phase.
NOTE: Routes for the same prefix contributed by different routing protocols are not considered "equal cost".

#High Level Architecture and Design#

Multiple components are involved in supporting layer3.

The below diagram highlights how the different components inter-communicate:

    {%ditaa%}
    +--------------------------------------------------------+
    |                                                        |
    |        Management Interface (CLI, Rest etc.)           |
    |                                                        |
    +--------------------------+-----------------------------+
       Layer3 Interfaces       |
       Static Routes           |
       ECMP Configs            |
    +--------------------------v-----------------------------+
    |                                                        |
    |                        OVSDB                           |
    |                                                        |
    |                                                        |
    +-----^--------------^-------------^---------------^-----+
          |              |             |               |
          |              |             |               |
    +-----v-----+  +-----v-----+  +----v------+  +-----v-----+
    |           |  |           |  |           |  |           |
    | arpmgrd   |  |   portd   |  |   zebra   |  |  vswitchd |
    |           |  |           |  |           |  |           |
    +----^------+  +-----+-----+  +------+----+  +-----^-----+
         |               |               |             |
    +----+---------------v---------------v----+  +-----v-----+
    |                                         |  |           |
    |                 Kernel                  |  |   ASIC    |
    |                                         |  |           |
    +-----------------------------------------+  +-----------+
    {%endditaa%}

The role of each of these components are explained below

- portd - responsible for IP address configuration to kernel
- arpmgrd - reads kernel ARP notification and updates the OVSDB
- zebra - active route selection and configuring the routes to kernel
- vswitchd - configuring layer3 interfaces, active routes and established neighbors to the hardware
- Management Interface (CLI, REST, etc.) - Configuration
- OVSDB - central database with the latest state of the system
- Hardware Plugin Module - shim layer used by vswitchd to communicate with the ASIC. Openswitch currently supports Broadcom platforms that support OpenNSL

###portd###
portd is responsible for configuring layer3 addresses to the kernel. In Openswitch, each layer3 interface is associated with an unique vlan which is not used by any other interface. portd is responsible for the internal vlan management. This daemon is also responsible for creation/deletion of logical vlan interfaces in the OVSDB which facilitate intervlan routing (routing between 2 different layer2 vlans). Refer the portd Component Design for more information on this daemon.

###arpmgrd###
arpmgrd is responsible for maintaining consistency between the OVSDB neighbor entries with the kernel neighbor entries. This daemon reads neighbor updates from kernel and updates the OVSDB with these entries. Refer the arpmgrd Component Design for more information on this daemon.

###zebra###
zebra is responsible for active route selection (also known as Forwarding Information Base (FIB) routes). All the routes from routing protocols and static routes are advertised to zebra through OVSDB. On selecting/unselecting an active route, zebra updates the kernel with these routes. This decision is also communicated to vswitchd through OVSDB. Refer the zebra Component Design for more information on this daemon.

###vswitchd###
From routing perspective, vswitchd is responsible for downloading all the information from the OVSDB to the ASIC. This daemon uses the plugin layer to invoke the necessary OpenNSL SDK api to program the asic with the  configurations (interface, ecmp, etc.) and routes. It is also responsible for the creation/deletion of the actual VLAN interfaces to enable InterVLAN routing. Refer the openvswitch Component Design for more information on this daemon.

###Management Interface###
Management Interface here refers to all the components through which the device can be configured. This can be in the form of vtysh, REST apis, etc. Refer to the User Guide and component design of each of these modules to understand the usage.

###OVSDB###
OVSDB is the central database used in Openswitch. All the communication between different modules are facilitated through this database. The following tables are used in OVSDB for layer3 support:

- Port - Layer3 addresses. Refer portd Design.md for detailed usage of this table
- Interface - Interface state. Refer portd Design.md for detailed usage of this table
- Route - All the active routes. Refer zebra Design.md for detailed usage of this table
- Nexthop - Address of the downstream device or the outgoing interface. Refer zebra Design.md for detailed usage of this table
- Neighbor - Adjancency information for the device. Refer arpmgrd Design.md for detailed usage of this table

NOTE: Each of the above table is VRF aware i.e. VRF-ID is a "key" for each entry in Route and Neighbor tables. Every layer3 Port is associated with one VRF only.

Extensive documentation for OVSDB is available in the RFC-7047.


References
----------
* [Reference 1](http://www.openswitch.net/docs/redest1)


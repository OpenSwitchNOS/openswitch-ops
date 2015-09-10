# Basic Layer3 Design#

#Introduction#

OpenSwitch is designed to support layer3 features and protocols. To facilitate this, the following capabilities have been added.

- **VRF support**
- **Layer3 Interfaces**
- **Static Routes**
- **Slow-path Routing (Routing in kernel)**
- **Fast-path Routing (Hardware based routing)**
- **Equal Cost Multipath (ECMP)**
- **VLAN Interfaces**
- **InterVLAN Routing**

##VRF##
Virtual Routing and Forwarding (VRF) is used in switches with multi-tenancy hosting. Each tenant is isolated from the other tenants on the switch. This way a single physical switch can virtually host multiple routers. Each VRF maintains its own routing tables, neighbor tables, physical and virtual interfaces etc. However in the first phase, this support is restricted to only one "default" VRF although the architecture is designed to support multiple VRF. Linux networking namespaces is used to support VRF on OpenSwitch. Every daemon in OpenSwitch is started inside the context of a networking namespace. Currently OpenSwitch has 2 network namespaces: "nonet" and "swns". All the networking daemons i.e the daemons that is interested in accessing the network interfaces, will be started in the "swns" namespace.

###Linux Network Namespaces###
OpenSwitch leverages the concept of Linux network namespaces to completely isolate VRFs. Namespaces can be used to isolate routing tables, neighbor tables etc. Extensive information about namespaces is available on the web. For basic reference: http://man7.org/linux/man-pages/man7/namespaces.7.html

##Layer3 Interfaces##
In OpenSwitch, a physical layer3 interface has the following properties

- Port has an IP address and mask.
- Port does not have any layer2 configuration.
- Port is part of a VRF (default VRF in the initial phase). This port is not part of any bridge.
- Packets arriving at this interface will have a destination MAC matching one of the device MAC.

###VLAN Reservations###
The purpose of a layer3 interface is to route the packet. This means that these interfaces should not switch (layer2 switch) the packets. For this reason, each layer3 interface is associated with an unique VLAN id that is internally allocated. These VLAN ids cannot be re-used for user VLAN configurations. The default range for allocating the VLAN ids is 1024-4094. Alternatively user can configure any VLAN range (from 1-4095) to be used for this purpose. Only one range can be configured per VRF. When an user reconfigures the VLAN range, the VLAN ids that were already used for existing interfaces from the old range are not moved over to the new range. Any subsequent interface creations will use VLAN ids from the new range.

##Static Routes##
Static routes are important in the absence of routing layer3 protocols or when user wishes to override the routes advertised by the routing protocols. User configures the static routes from one of the management daemons i.e. CLI, REST etc. which are written to the OVSDB. Static routes have the least distance (highest priority) compared to the routes advertised by the routing protocols. So for the same destination prefix, a static route will be preferred (and selected as active route )over any other protocol.

##Slow-path Routing##
In OpenSwitch, slow routing refers to instances where the routing happens in the kernel. The kernel has a copy of all the active routes and neighbors. When a transit packet is received by the kernel, the destination prefix is looked up in the kernel routing table (Forwarding Information Base, FIB) for the longest match. Once a match is found, the kernel uses information from the route nexthop and the corresponding ARP entry to reconstruct the packet and send it to the correct egress interface. OpenSwitch running on a virtual machine always use slow-routing whereas OpenSwitch running on a physical device will use slow routing on need basis when the necessary information is not available in the ASIC for fast routing.

##Fast-path Routing##
In OpenSwitch, fast-path routing refers to instances where routing happens in the ASIC. ASICs that are capable of switching/routing packets are programmed with a copy of the FIB entries (similar to the kernel FIB entries) and neighbor entries (neighbors identified by kernel using ARP). The ASIC is able to perform a longest-prefix match and find the appropriate route for packets. Similar to kernel, the ASIC uses the route, nexthop and the corresponding ARP entry to route the packets. Sometimes the corresponding ARP for a route nexthop may not be resolved and hence unavailable in the ASIC. In such cases, these packets are sent to the kernel for ARP resolution and subsequently routing (slow-path). When the kernel resolves the new neighbor based on the recent ARP, this information is again programmed back to the ASIC. This way subsequent packets to the same destination prefix can be routed in the fast-path.

##ECMP ##
Equal Cost Multipath is a scenario where a single prefix can have multiple "Equal Cost" route nexthops. OpenSwitch supports 32 ECMP nexthops per prefix in the initial phase. OpenSwitch supports ECMP for IPv4 prefixes in the initial phase.
NOTE: Routes for the same prefix contributed by different routing protocols are not considered "equal cost".

##InterVLAN Routing and VLAN Interfaces##
InterVLAN routing is important in scenarios where routing is needed between 2 different VLANs on a switch. When a packet is ingressing and egressing on physical interfaces that are layer2 and both the interfaces are participating in different VLANs, routing between these VLANs is achieved by creating 2 virtual interfaces. These virtual interfaces have the following properties:

- Each virtual interface is associated with one of the VLANs.
- Virtual interface is associated with a bridge. This is an internal bridge created solely for isolating VLAN traffic to the virtual interfaces.
- Switching happens between the physical layer2 interface and the corresponding virtual interface in that VLAN.
- The virtual interface has an IP address associated with a VRF.
- Routing happens between the 2 virtual interfaces.

#High Level Architecture and Design#

Multiple components are involved in supporting layer3.

The below diagram highlights how the different components intercommunicate:

    ```ditaa
    +------------------------+   +---------------------------+
    |  Management Daemons    |   |   Routing Protocol        |
    |  (CLI, REST, etc.)     |   |       Daemons             |
    |                        |   |   (BGP, OSPF etc.)        |
    |                        |   |                           |
    +------------------------+   +------------+--------------+
    L3 Interfaces|                Protocol    |
    Static Routes|                Routes      |
    ECMP Configs |                            |
    +------------v----------------------------v--------------+
    |                                                        |
    |                        OVSDB                           |
    |                                                        |
    |                                                        |
    +-----^--------------^-------------^---------------^-----+
      Nbr.|       Intf.  |       Route |         Routes|Intf.
      Info|       Configs|       Info. |         Nbr.  |
    +-----v-----+  +-----v-----+  +----v------+  +-----v------+
    |           |  |           |  |           |  |            |
    |ops-arpmgrd|  | ops-portd |  |ops-zebra  |  | ops-switchd|
    |           |  |           |  |           |  |            |
    +----^------+  +-----^-----+  +-----------+  +-----^------+
     Nbr.|         Intf. |         Routes|             |
    +----v---------------v---------------v----+  +-----v-----+
    |                                         |  |           |
    |                 Kernel                  <--+   ASIC    |
    |                                         |  |           |
    +-----------------------------------------+  +-----------+

    ```

The role of each of these components is explained below

- ops-portd - responsible for configuring IP address in the kernel.
- ops-arpmgrd - reads kernel ARP notification and updates the OVSDB.
              - responsible for refreshing ARP entries for neighbors with active data traffic.
- Protocol Daemons - responsible for contributing learned routes to zebra.
- ops-zebra - active route selection and configuring the routes to kernel.
- ops-vswitchd - configuring layer3 interfaces, active routes and established neighbors to the hardware.
- Management Daemons (CLI, REST, etc.) - Configuration
- OVSDB - central database with the latest state of the system.

###ops-portd###
ops-portd is responsible for configuring layer3 addresses to the kernel. In OpenSwitch, each layer3 interface is associated with an unique VLAN which is not used by any other interface. ops-portd is responsible for the internal VLAN management. This daemon is also responsible for creation/deletion of logical VLAN interfaces in the OVSDB which facilitate interVLAN routing (routing between 2 different layer2 VLANs). This daemon is also responsible for updating the kernel interface admin status to UP or DOWN depending on the user configuration. In order to maintain consistency with the kernel, routes for directly connected subnets are also added to the Route table. ops-portd is responsible for adding these directly connected subnet routes to the Route table in the OVSDB.
Refer the ops-portd Component Design for more information on this daemon.

###ops-arpmgrd###
ops-arpmgrd is responsible for maintaining consistency among the OVSDB neighbor entries with the kernel neighbor entries. This daemon reads neighbor updates from kernel and updates the OVSDB with these entries. Additionally the daemon actively requests the kernel to refresh the ARP entries for neighbors that have active data traffic.
Refer the ops-arpmgrd Component Design for more information on this daemon.

###Management Daemons###
Management Daemons here refers to all the components through which the device can be configured. This can be in the form of CLI, REST APIs, etc. Refer to the User Guide and component design of each of these modules to understand the usage. Static routes are configured from one of the Management Daemons discussed above. Static routes are also populated in the Route and Nexthop tables similar to the routes advertised by the protocol daemons.

###Protocol Daemons###
Routing protocols like BGP, OSPF etc. learn routes by communicating with their routing peers. The learned routes from various routing protocols are advertised to zebra daemon which makes the final decision on the routes that will be programmed to the kernel and ASIC. The routing protocols write the learned routes and their nexthops to the Route and Nexthop tables in the OVSDB.
Refer to the individual protocol design docs for more information on the specific routing protocol.

###zebra###
zebra is responsible for active route selection (also known as Forwarding Information Base (FIB) routes). All the routes from routing protocols and static routes are advertised to zebra through OVSDB. zebra takes all the advertised routes into account and internally decides which of those routes will be programmed to the kernel and the ASIC. On selecting an active route, zebra updates the kernel with these routes. This decision is also communicated to ops-vswitchd through OVSDB for further programming these routes to the ASIC.
Refer the zebra Component Design for more information on this daemon.

###ops-vswitchd###
From routing perspective, ops-vswitchd is responsible for downloading all the information from the OVSDB to the ASIC. This daemon uses the plugin layer to invoke the necessary SDK API to program the ASIC with the  neighbors, routes and configurations (interface, ECMP, etc.). It is also responsible for the creation/deletion of the actual VLAN interfaces to enable InterVLAN routing.
Refer the Openvswitch Component Design for more information on this daemon.

###OVSDB###
OVSDB is the central database used in OpenSwitch. All the communication between different modules are facilitated through this database. The following tables are used in OVSDB for layer3 support:

- Port Table
- Interface Table
- Route Table
- Nexthop Table
- Neighbor Table

####Port Table####
Each interface in OpenSwitch has a corresponding entry in the Port table. Port table has the non-physical properties of an interface. Since layer3 addresses are a logical property, they are in the Port table. Every entry in the port table has a direct reference to one or more rows in the Interface table.
Refer ops-portd Design.md for detailed usage of this table.

####Interface Table####
Along with other physical properties of an interface, the Interface table also has the user configuration of interface states. This information is used to configure the kernel with the corresponding interface state.

####Neighbor Table####
Neighbor table contains the list of directly connected neighbors. ops-arpmgrd populates this table by listening to kernel ARP updates. The ops-arpmgrd daemon uses the dp_hit in the status column to actively request the kernel to refresh the ARP entries for neighbors with active data traffic.

####Route Table####
Routes from different protocols (and static routes) are stored in the Route table. VRF, prefix, protocol, nexthops are all stored in a route entry. This table stores IPv4 and IPv6 routes. Each route can refer to one or more nexthops. The "selected" column in the Route table is updated by zebra on active route selection. When a route is selected for routing, zebra updates the "selected" column for that route to true.

####Nexthop Table####
Nexthops are theoretically an extension of the routes themselves. But for ease of maintenance and other optimizations, Nexthops are stored in a different table in the OVSDB. Each route entry can refer to one or more nexthops (more than one nexthops for ECMP). Nexthops information consists of downstream device IP address or the outgoing interface or both.

NOTE: Each of the above table is VRF aware i.e. VRF-ID is a "key" for each entry in Route and Neighbor tables. Every layer3 Port is associated with one VRF only.

Extensive documentation for OVSDB is available in the RFC-7047.


References
----------
* [Linux Network Namespaces](http://man7.org/linux/man-pages/man7/namespaces.7.html)
* [RFC 7047](https://tools.ietf.org/html/rfc7047)


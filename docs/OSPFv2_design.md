#<u>High level design of OSPFv2</u>


#OSPFv2 Introduction
OSPFv2 (Open Shortest Path First version 2) is a routing protocol which is described in RFC2328 entitled OSPF Version 2. OSPFv2 is a Link State-based IGP (Interior Gateway Protocol) routing protocol. OSPFv2 is widely used with medium to large-sized enterprise networks.

#Scope
The document describes the integration design for OSPFv2 routing protocol's stack in OpenSwitch.

For information on the OSPFv2 protocol, specifications, deployments, protocol stack and implementation, refer the standard RFC documents and other pointers described in the "reference" section of this document.

#Design choices

##Current choices for the modules
Centralized Database--OpenvSwitch Database, known as OVSDB.
OSPFv2 Protcol Stack--From the Quagga Routing Protocol Suite.

#Participating modules
Multiple components are involved in supporting OSPFv2.

The below diagram highlights how the different components intercommunicate:

```ditaa
            +------------+    +------------------+      +-------------------+
            | ops-portd  |    |   ops-ospfd      |      | Mgmt Interfaces   |
            |            |    |                  |      | (CLI, REST)       |
            +--+---------+    +--------^---------+      +----------^--------+
               |           Updates|    |Configs       Config|      |Show
               |                  |    |                    |      |
               |                  |    |                    |      |
    +-----------------------------v-----------------------------------------+
    |  +-------v--+  +----------+  +-------------+  +---------------+ OVSDB |
    |  | PORT     |  |  VRF     |  |OSPF_LSA     |  |OSPF_Route     |       |
    |  +----------+  +----------+  +-------------+  +---------------+       |
    |                                                                       |
    | +-------------+    +-------------+  +----------+    +---------------+ |
    | |OSPF_Router  |    |OSPF_Area    |  | Route    |    |OSPF_Interface | |
    | +-------------+    +-------------+  +-+--^--+--+    +---------------+ |
    | +---------------+                     |  |  |                         |
    | |OSPF_Neighbor  |                     |  |  |                         |
    | +---------------+                     |  |  |                         |
    +-----------------------------------------------------------------------+
                                            |  |  +--------------+
                                            |  |                 |
                                         +--v--+-------+      +--v---------+
                                         | ops-zebra   |      |ops-switchd |
                                         |             |      |            |
                                         +------+------+      +------+-----+
                                                |                    |
                                                |                    |
                                                |                    |
                                         +------v------+      +------v-----+
                                         |   Kernel    |      |  ASIC h/w  |
                                         |     netns   |      |            |
                                         +-------------+      +------------+
Figure-1: OSPFv2 related OVSDB tables and their interactions with the daemons and modules.
```

In Figure-1 (above), the large block in the center is the OVSDB server and all daemons (including ospfd) communicate to the OVSDB server. As part of OSPFv2 support on OpenSwitch, several new tables have been added to the OVSDB schema and some existing tables have been modified as well. The major tables and their interactions are depicted by the directional arrows in Figure-1.

The role of each of these components is explained below in more detail:

### ops-portd
The ops-portd daemon is responsible for updating the port related information in the OVSDB PORT table.
Refer to the [ops-portd Component Design](http://git.openswitch.net/cgit/openswitch/ops-portd/tree/DESIGN.md) for more information.

### Management Interfaces
Management Interfaces here refers to all the components through which the device can be configured. This can be in the form of a CLI, REST APIs, and so on.. Refer to the [CLI Component Design](http://git.openswit ch.net/cgit/openswitch/ops-cli/tree/DESIGN.md), the [REST API Component Design](http://git.openswitch.ne t/cgit/openswitch/ops-restd/tree/DESIGN.md) and the [REST API User Guide](http://git.openswitch.net/cgit /openswitch/ops/tree/docs/REST_API_user_guide.md) to understand the usage. All the configurations and the status and statistics reports happen through these management interfaces.

### ops-ospfd
The ops-ospfd daemon runs the OSPFv2 routing protocol. As part of that, it communicates to the OSPFv2 routers in the network. It advertises the routes to the other routers communicating in OSPFv2 and also learns route information from them. 
   
The OSPFv2 learned routes are updated into the "Route" table in the OVSDB database. The ops-ospfd daemon learns the configurations from different  OVSDB tables. The ops-ospfd daemon also updates a few tables as part of the running OSPFv2 protocol, so that the user or network operator can have access to the status and updates from the OSPFv2 protocol through the CLI or REST API-based management applications.

### ops-zebra
The ops-zebra is the RTM (Routing Table Manager) daemon that makes the decision of the best routes among the available routes learned from other routing protocols and other types of routes like connected, static, etc. The ops-zebra daemon learns the routes available from the different protocols and kind from the OVSDB "Route" table.

The zebra daemon updates the "Route" table with the best routes selection. It also installs the routes into the kernel in case of a virtual switch (for example: Docker).

Refer to the ops-zebra component design document for more information on this daemon.

### ops-switchd
As far as routing is concerned, the ops-switchd daemon gets the best routes from the OVSDB "Route" table or the FIB routes and then programs them to the ASIC hardware. This daemon uses the plugins or APIs available from the ASIC provider to program the ASIC hardware.

Refer to the [Openvswitch Component Design](http://git.openswitch.net/cgit/openswitch/ops-openvswitch/tree/DESIGN.md) for more information on this daemon.

### OVSDB
The OVSDB is the central database used in OpenSwitch. All the communications between different modules are facilitated through this database. The following tables are used in OVSDB for OSPFv2 support:
- System
- Route
- Route_Map
- VRF
- Port
- OSPF_Router
- OSPF_Area
- OSPF_Summary_Address
- OSPF_Interface
- OSPF_Vlink
- OSPF_Neighbor
- OSPF_NBMA_Neighbor
- OSPF_Route
- OSPF_LSA

OVSDB Schema
------------
Figure-2 depicts the existing tables which are extended to support the OSPFv2 on OpenSwitch. It also depicts the OSPFv2 related tables those are newly added.

```ditaa
+---------------+                 +---------------+  +---------------+    +---------------+
|               |                 |               |  |               |    |               |
|   Route       |                 |  Route_Map    |  |  Prefix_List  +--->|  Prefix_List  |
|               |                 |               |  |               |    |    _Entry     |
|               |                 |               |  |               |    |               |
+------+--------+                 +---------------+  +---------------+    +---------------+
       |                                 ^              ^
       |                                 |              |
       v                                 |              |
+---------------+                 +------+--------+     |         +---------------+
|               |                 |               |     |         |               |
|   VRF         +---------------->|  OSPF_Router  +-------------->|  OSPF_Route   |
|               |            +----+               |     |         |               |
|               |            |    |               +---------+  +->|               |
+------+--------+            |    +------+--------+     |   |  |  +---------------+
       |                     |           |              |   |  |
       |                     |           |     +--------+   +---------+
       v                     |           v     |               |      |
+---------------+            |    +------------+--+            |  +---v-----------+
|               |            |    |               +------------+  |               |
|   Port        |            |    |  OSPF_Area    +-------------->|  OSPF_LSA     |
|               |<-----+     |    |               |               |               |
|               |      |     |    |               +----------+    |               |
+---------------+      |     |    +------+-------++          |    +---------------+
                       |     |           |       |           |
                       |     |           |       +-----+     |
                       |     |           v             |     |
                       |     |    +---------------+    |     |    +---------------+
                       |     |    |               |    |     +--->| OSPF_Area_    |
                       +----------+  OSPF_        |    |          |   Summary_    |
                             |    |     Interface |    |          |     Addr      |
                             |    |               |    |          |               |
                             |    +------+------+-+    |          +---------------+
                             |           |      |      |
                             |           |      |      +-------------+
                             |           v      +---------+          |
+---------------+            |    +---------------+       |       +--v------------+
| OSPF_NBMA_    |<-----------+    |               |       +------>|               |
| Neighbor_     |<----------------+  OSPF_Neighbor|               |  OSPF_Vlink   |
|   Config      |                 |               |               |               |
|               |                 |               |               |               |
+---------------+                 +---------------+               +---------------+


  +----+
  |    |  OVSDB tables                                                  ------>
  +----+                                                            Reference Pointer

  Figure-2: OSPFv2 related OVSDB schema tables and their inter-relationships
```

Below is the overview of the OSPFv2 related tables and information on what data or entity they model.

#### OSPF_Router table
The OSPF_Router table contains all ospf router instance level configurations, status and statistics. It contains information related to SPF (Shortest path first) parameters, restart related configurations, router related configurations and also references to tables like OSPF_Area, OSPF_LSA, OSPF_Route start here.

#### OSPF_Area table
The OSPF_Area table contains information connected to area related configurations, status, and statistics. It contains information related to area level authentication and area type.  It also has references to other tables such as  OSPF_Vlink, OSPF_Interface, OSPF_Route,  OOSPF_LSA and OSPF_Summary_Addr.

#### OSPF_Summary_Addr table
This OSPF_Summary_Addr table contains information related to route summarization like prefix and related configuration.

#### OSPF_Interface table
The OSPF_Interface table contains information related to interface FSM states and interface statistics. It also has references to tables like OSPF_Neighbor, OSPF_Vlink, OSPF_LSA and Port.

#### OSPF_Neighbor table
The OSPF_Neighbor table contains information connected to neighbor related status and statistics. It has reference to OSPF_NBMA_Neighbor table, in case the neighbor is of type NBMA (Non Broadcast Multiple Access) neighbor.

#### OSPF_NBMA_Neighbor table
The OSPF_NBMA_Neighbor table contains information connected to Non-broadcast multiple access (NBMA) neighbors. It contains the configurations and statuses specific to NBMA neighbors, like poll timer.

#### OSPF_Vlink table
The OSPF_Vlink table contains information connected to virtual link related configurations like peer router id, area id, hello interval, dead interval, retransmit interval, transmit delay and authentication related configuration.

#### OSPF_Route table
The OSPF_Route table contains information connected to OSPFv2 routes. It contains columns like prefix, path type, paths, route information and flags.

#### OSPF_LSA table
The OSPF_LSA table contains information connected related to link state related configurations such as LS age, LS id, lsa type, lsa sequence number, options, flags, checksum, prefix and so on.

## OSPF configuration flows and protocol updates

The below diagram depicts the schema update flow for few OSPFv2 related CLI commands and the OSPFv2 protocol updates, which covers most of the related tables.

```ditaa
            +---------------+                     +---------------+
            |               |                     |               |
        #0  |  OSPF_Router  |          #2         |  OSPF_Area    |
Cmd-1 +---->|               +-------------------->|               |
            |               |  OPS-OSPFD process  |               |
            +---------------+                     +---------------+
                                                         |
                                                         |
                                                         |
                                                         |
                                                         |
                                                         |
                                                      #3 |
                                                         |
                                                         |
                                                         |
                                                         |
                                                         v
            +---------------+                     +---------------+
            |               |                     |               |
         #0 |     Port      |         #1          |  OSPF_        |
Cmd-1a +--->|               +-------------------->|     Interface |
            |               |  OPS-OSPFD process  |               |
            +---------------+                     +---------------+


  +----+
  |    |  OVSDB tables                                  ------>
  +----+                                                Flow

Figure-3: Flow of the configuration changes through schema table objects for cmd-1
Cmd-1 : conf term -->> router ospf -->> network <subnet/mask> area <area-id>
Cmd-1a : conf term -->> inerface <ifname> -->> ip ospf hello-interval <interval>
```

Figure-3 depicts the flow of the configuration changes through the OVSDB schema tables for the commands to enable the ospf protocol on a subnetwork and interface level configuration. The numbers along the flow-arrows are indicative of the order of the flow.

The command (Cmd-1) creates a a corresponding row in the "OSPF_Router" and an entry in the "networks" column. The OPS-OSPFD daemon then runs OSPFv2 protocol on the network configured and populates the corresponding rows in the "OSPF_Area" and "OSPF_Interface" tables.
The command (Cmd-1a) populates OSPFv2 relates columns in the corresponding row of the "Port" table. This configuration may impact the related columns of the corresponding "OSPF_Interface" table through the OPS-OSPFD daemon.


```ditaa
                +---------------+                 +---------------+
                | OSPF_NBMA_    |                 |               |
         #0     | Neighbor_     |    #1           |  OSPF_Neighbor|
Cmd-2 +-------->|   Config      +---------------->|               |
                |               |                 |               |
                +---------------+                 +---------------+


  +----+
  |    |  OVSDB tables                               ------>
  +----+                                             Flow

Figure-4: Flow of the configuration changes through schema table objects for cmd-2
Cmd-2 : conf term -->> router ospf -->> neighbor <nbr-ip>

```

Figure-4 depicts flow of the configuration changes through the OVSDB schema tables for the command to configure a NBMA Neighbor. The numbers along the flow-arrows are indicative of the order of the flow.

This command will create corresponding rows in the "OSPF_NBMA_Neighbor". If may create a corresponding row in the "OSPF_Neighbor" table as well, depending on the validation of the configuration.


```ditaa

    +---------------+
    |               |
    |     Port      |
    |               |
    |               |
    +-------+-----^-+
            |     |
         #3 |     +------+
            v            |
    +---------------+    |          +---------------+
    |               |    |          |               |
    |  OSPF_        |    |          |   OSPF_Area   |
    |     Interface |    |          |               |
    |               |    |          |               |
    +------+--------+    |          +---------------+
           |             |    #2               ^
        #4 |             +-------------+       | #1
           v                           |       |
    +---------------+               +--+-------+----+
    |               |               |               |
    |  OSPF_Neighbor|               |  OSPF_Vlink   |    #0
    |               |               |               |<-------+ Cmd-3
    |               |               |               |
    +---------------+               +---------------+


  +----+
  |    |  OVSDB tables                       +----->
  +----+                                     Flow

Figure-5: Flow of the configuration changes through schema table objects for cmd-3
Cmd-3 : conf term -->> router ospf -->> area <area-id> virtual-link <remote-ip>

```

Figure-5 depicts the flow of the configuration changes through the OVSDB schema tables for the command to configure a Virtual-link in a non backbone area. The numbers along the flow-arrows are indicative of the order of the flow.

This command creates a corresponding row in the "OSPF_Area" table if it does not exist already. It creates a corresponding row in the "Port" table to create "port" for the Vlink. A corresponding row in the "OSPF_Interface" table is created and through neighbor Finite State Machine (FSM) in the OSPFv2 protocol a corresponding row in the "OSPF_Neighbor" table might be created as well.


```ditaa

         Cmd-4
           +
           | #0
           v
    +---------------+               +---------------+
    |               |    #1         |               |
    |  OSPF_Area    +-------------->|  OSPF_Summary |
    |               |               |      _Address |
    |               |               |               |
    +---------------+               +-------+-------+
                                            |
                                            | #2
                                            v
                                    +---------------+
                                    |               |
                                    |  OSPF_LSA     |
                                    |               |
                                    |               |
                                    +---------------+

  +----+
  |    |  OVSDB tables                        +----->
  +----+                                      Flow

Figure-6: Flow of the configuration changes through schema table objects for cmd-4
Cmd-4 : conf term -->> router ospf -->> area <area-id> range <A.B.C.D/M>
```

Figure-6 depicts the flow of the configuration changes through the OVSDB schema tables for the command to configure a area range summarization prefix. The numbers along the flow-arrows are indicative of the order of the flow.

This command creates a corresponding row in the "OSPF_Area" table if it does not exist already. It creates corresponding row in the "OSPF_Summary_Address" table. This may trigger OSPFv2 protocol to create or delete corresponding one or more rows in the "OSPF_LSA" table.


```ditaa

                                    +---------------+
+------------------+                |               |
|                  |       +------->|     Route     |
| OPS-OSPFD        |       |        |               |
|       Process    |       |        +---------------+
|                  |       |
| +--------------+ |       |        +---------------+
| |    SPF       + |-------+        |               |
| | Calculation  + |--------------->|  OSPF_Route   |
| +--------------+ |                |               |
|                  |                +---------------+
|                  |
| +--------------+ |                +---------------+
| |LSA Origin/   | |                |               |
| |  Reception   + |--------------->|  OSPF_LSA     |
| |              | |                |               |
| +--------------+ |                +---------------+
|                  |
|                  |
| +--------------+ |                +---------------+
| |    OSPF      | |                |               |
| |  Neighbor    + |--------------->| OSPF_Neighbor |
| |    FSM       | |                |               |
| |              | |                +---------------+
| +--------------+ |
|                  |
| +--------------+ |                +---------------+
| |    OSPF      | |                |               |
| |  Interface   + |--------------->| OSPF_Interface|
| |    FSM       | |                |               |
| |              | |                +---------------+
| +--------------+ |
|                  |
+------------------+

  +----+
  |    |  OVSDB tables                    +----->
  +----+                                  Flow

Figure-7: Flow of the OSPFv2 protocol updates through schema table objects
```

Figure-7 depicts flow of the OSPFv2 protocol updates through the OVSDB schema tables for different OSPFv2 protocol internal modules.

The SPF calculation module may create, delete or update the rows in the "OSPF_Route" and "Route" tables.

The LSA Generation and Reception update the OSPFv2 protocols Link Sate Data Base, which may create, delete or update the rows in the "OSPF_LSA" table.

The Neighbor FSM module may create, delete or update the rows in the "OSPF_Neighbor" table.

The Neighbor FSM module may create, delete or update the rows in the "OSPF_Interface" table.

## Functionality Support or Compliance

We will be supporting the below list of compliances as part of the "OSPFv2 support on OpenSwitch":
- OSPFv2 RFC 2328, which is backward compatible to RFC 2178.
- Stub Router Advertisement RFC 3137.
- The OSPFv2 Not-So-Stubby Area (NSSA) RFC 3101.

The following features may be supported at a later point in time:
- Non Broadcast Multiple Access (NBMA) Neighbors, which is part of the RFC 2328.
- The OSPFv2 Opaque LSA Option RFC 2370.
- Multiple VRF Support for OSPFv2.
- Route Maps support for OSPFv2.
- OSPFv2 Graceful Restart RFC 3623.
- SNMPv2 MIB Support RFC 4750 for OSPFv2.
- OSPFv2 support on LAG ports.

The following features are not planned for support at this time:
- Fast Hellos or sub-second hellos.
- IP Fast ReRoute Loop Free alternate (LFA FRR) - RFC 5286 support for OSPFv2.

##References
* [OpenSwitch Design](http://www.openswitch.net/documents/dev/ops-openvswitch/DESIGN)
* [OpenSwitch Archtecture](http://www.openswitch.net/documents/user/architecture)
* [ops-portd Component Design](http://git.openswitch.net/cgit/openswitch/ops-portd/tree/DESIGN.md)
* [CLI Component Design](http://git.openswitch.net/cgit/openswitch/ops-cli/tree/DESIGN.md)
* [REST API Component Design](http://git.openswitch.net/cgit/openswitch/ops-restd/tree/DESIGN.md)
* [REST API User Guide](http://git.openswitch.net/cgit/openswitch/ops/tree/docs/REST_API_user_guide.md)
* [OSPFv2 command reference](/documents/dev/ops/docs/OSPFv2_cli)
* [OSPFv2 user guide](/documents/dev/ops/docs/OSPFv2_user_guide)
* [Quagga Documentation](http://www.nongnu.org/quagga/docs.html)
* [OSPFv2 protocol specifications RFC 2328](https://tools.ietf.org/html/rfc2328)
* [OSPFv2 protocol specifications (obsolete) RFC 2178](https://tools.ietf.org/html/rfc2178)
* [OSPFv2 Graceful Restart RFC 3623](https://tools.ietf.org/html/rfc3623)
* [IP Fast Reroute RFC 5286](https://tools.ietf.org/html/rfc5286)
* [OSPFv2 Stub Router Advertisement RFC 3137](https://tools.ietf.org/html/rfc3137)
* [The OSPFv2 Opaque LSA Option RFC 2370](https://tools.ietf.org/html/rfc2370)

#<u>High level design of OSPFv2</u>


#OSPFv2 Introduction
OSPFv2 (Open Shortest Path First version 2) is a routing protocol which is described in RFC2328. OSPFv2 is a Link State based IGP (Interior Gateway Protocol) routing protocol. OSPFv2 is widely used in medium to large sized enterprise networks.

#Scope
The document describes the design of the integration of OSPFv2 routing protocols stack in OpenSwitch.

For information on OSPFv2 protocol, specifications, deployments, protocol stack and implementation, refer the standard RFC documents and other pointers described in the "reference" section of this document.

#Design choices

##Current choices for the modules
Centralised Database - OpenvSwitch Database, popularly known and referred hereafter as OVSDB.
OSPFv2 protcol Stack - From Quagga Routing Protocol Suite.

##Integration specific choices
OVSDB schema is the definitions of the "tables" and "columns" for the database. Actual data entry in the table, is called "row" of the corresponding table.

As per the current design approach, the lookup for a row in a particular table will follow the iterating from top level parent table, down to the table of interest.

## Major deviations from the OSPFv2 original stack
- Enabling the OSPFv2 protocol on the subnetwork or port.
	In OpenSwitch, OSPFv2 protocol can be enabled per port, with restriction of port can be participate in only one ospf area and router instance.
- NBMA Neighbor configuration
	As with above point, it is logical to move the NBMA configuration to interface context.

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


In the above Figure-1, the large block in the center is OVSDB server and all daemons (including ospfd) communicate to the OVSDB server. As part of OSPFv2 support on OpenSwitch, several new tables are added to the OVSDB schema as well as some existing tables have been modified. The major tables and their interactions are depicted by directional arrows in Figure-1.

The role of each of these components is explained below in more detail:

### ops-portd
ops-portd is responsible for updating the port related information in the PORT table of OVSDB.
Refer the [ops-portd Component Design](http://git.openswitch.net/cgit/openswitch/ops-portd/tree/DESIGN.md) for more information on this daemon.

### Management Interfaces
Management Interfaces here refers to all the components through which the device can be configured. This can be in the form of CLI, REST APIs, etc. Refer the [CLI Component Design](http://git.openswitch.net/cgit/openswitch/ops-cli/tree/DESIGN.md), [REST API Component Design](http://git.openswitch.net/cgit/openswitch/ops-restd/tree/DESIGN.md) and [REST API User Guide](http://git.openswitch.net/cgit/openswitch/ops/tree/docs/REST_API_user_guide.md) understand the usage. All the configurations and display of status and statistics happen through these management interfaces.

### ops-ospfd
The ops-ospfd is the daemon which runs the OSPFv2 routing protocol. As part of that it communicates to OSPFv2 routers in the network. It advertises the routes to the other routers talking OSPFv2 and also learns route from them.
The learned routes through OSPFv2, are updated into the "Route" table into the OVSDB database.
The ops-ospfd learns the configurations from different table of the OVSDB. The ops-ospfd also updates few tables as part of the OSPFv2 protocol running, so that the user or network operator can have access to the status and updates from the OSPFv2 protocol through CLI or REST API based management applications.

### ops-zebra
The ops-zebra is RTM (Routing Table Manager) daemon which makes the decision on best routes among the routes learned from all the protocols and kind. The ops-zebra daemon learns the routes available from different protocols and kind from "Route" table of the OVSDB.

The zebra daemon updates the "Route" table with the decision or selection of the best routes. It also installs the routes into kernel in case of virtual switch (for e.g., docker).

Refer the ops-zebra Component Design for more information on this daemon.

### ops-switchd
As far as routing is concerned, ops-switchd gets the routes from the "Route" table of the OVSDB which are the best routes or FIB routes and programs them to the ASIC hardware. This daemon uses the plugins or APIs available from the ASIC provider to program the ASIC hardware.

Refer the [Openvswitch Component Design](http://git.openswitch.net/cgit/openswitch/ops-openvswitch/tree/DESIGN.md) for more information on this daemon.

### OVSDB
OVSDB is the central database used in OpenSwitch. All the communication between different modules are facilitated through this database. The following tables are used in OVSDB for OSPFv2 support:
- System
- Route
- Route_Map
- VRF
- Port
- OSPF_Router
- OSPF_Area
- OSPF_Summary_Address
- OSPF_Interface
- OSPF_Interface_Config
- OSPF_Vlink
- OSPF_Neighbor
- OSPF_NBMA_Neighbor_Config
- OSPF_Route
- OSPF_LSA

OVSDB Schema
------------
The below diagram depicts the existing tables which are extended and / or being used for OSPFv2 support on OpenSwitch. It also depicts the OSPFv2 related tables that are newly added.

```ditaa
XXXXXXXXXXXXXXXXX                 XXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXXXXX
X               X                 X               X  X               X    X               X
X   Route       X                 X  Route_Map    X  X  Prefix_List  +---->  Prefix_List  X
X               X                 X               X  X               X    X    _Entry     X
X               X                 X               X  X               X    X               X
XXXXXXX+XXXXXXXXX                 XXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXXXXX
       |                                 ^              ^
       |                                 |              |
       v                                 |              |
XXXXXXXXXXXXXXXXX                 +------+--------+     |         +---------------+
X               X                 |               |     |         |               |
X   VRF         +---------------> |  OSPF_Router  +--------------->  OSPF_Route   |
X               X                 |               |     |         |               |
X               X                 |               +---------+  +-->               |
XXXXXXX+XXXXXXXXX                 +------+--------+     |   |  |  +---------------+
       |                                 |              |   |  |
       |                                 |     +--------+   +---------+
       v                                 |     |               |      |
XXXXXXXXXXXXXXXXX                 +------v-----+--+            |  +---v-----------+
X               X                 |               +------------+  |               |
X   Port        X                 |  OSPF_Area    +--------------->  OSPF_LSA     |
X               X<-----+          |               |               |               |
X               X      |          |               +----------+    |               |
XXXXXXX+XXXXXXXXX      |          +------+-------++          |    +---------------+
       |               |                 |       |           |
       |               |                 |       +-----+     |
       v               |                 |             |     |
+------+--------+      |          +------v--------+    |     |    +---------------+
|   OSPF_       |      |          |               |    |     +----> OSPF_Area_    |
| Interface_    |      +----------+  OSPF_        |    |          |   Summary_    |
|    Config     |                 |     Interface |    |          |     Addr      |
|               |                 |               |    |          |               |
+------+--------+                 +------+-------++    |          +---------------+
       |                                 |       |     |
       |                                 |       |     +-------------+
       v                                 |       +--------+          |
+------+--------+                 +------v--------+       |       +--v------------+
| OSPF_NBMA_    |                 |               |       +------->               |
| Neighbor_     | <---------------+  OSPF_Neighbor|               |  OSPF_Vlink   |
|   Config      |                 |               |               |               |
|               |                 |               |               |               |
+---------------+                 +---------------+               +---------------+


  +----+                            XXXXXXX
  |    |  Newly added tables        X     X   Existing tables           ------>
  +----+                            XXXXXXX                         Reference Pointer

  Figure-2: OSPFv2 related OVSDB schema tables and their inter-relationships
```

Below is the overview of the OSPFv2 related tables and information of what data or entity they model.

#### OSPF_Router table
The OSPF_Router table contains all ospf router instance level configuration, status and statistics. It contains information related to SPF (Shortest path first) parameters, restart related configurations, router related configurations and also references to tables like OSPF_Area, OSPF_LSA, OSPF_Route and Route_Map.

#### OSPF_Area table
The OSPF_Area table contains information related to area related configurations, status and statistics. It contains information related to area level authentication and area type.  It also has references to other tables like OSPF_Vlink, OSPF_Interface, OSPF_Route,  OOSPF_LSA, OSPF_Summary_Addr and Route_Map.

#### OSPF_Summary_Addr table
This OSPF_Summary_Addr table contains information related to route summarization like prefix, and related configuration.

#### OSPF_Interface table
The OSPF_Interface table contains information related to interface FSM states, interface statistics and also has references to tables like OSPF_Neighbor, OSPF_Vlink, OSPF_LSA and Port. This table is used to model the active OSPF interface.

#### OSPF_Interface_Config table
The OSPF_Interface_Config table contains information related to interface related configurations, authentication type, passive interface flags and also reference to OSPF_NBMA_Neighbor_Config table.

#### OSPF_Neighbor table
The OSPF_Neighbor table contains information related to neighbor status and statistics. It has reference to OSPF_NBMA_Neighbor_Config table, in case the neighbor is of type NBMA (Non Broadcast Multiple Access).

#### OSPF_NBMA_Neighbor_Config table
The OSPF_NBMA_Neighbor_Conf table contains information related to Non-broadcast multiple access (NBMA) neighbors. It contains the configurations and statuses specific to NBMA neighbors, like poll timer.

#### OSPF_Vlink table
The OSPF_Vlink table contains information related to virtual link related configurations like peer router id, area id, hello interval, dead interval, retransmit interval, transmit delay and authentication configuration.

#### OSPF_Route table
The OSPF_Route table contains information related to OSPFv2 routes. It contains columns like prefix, path type, paths, route information and flags.

#### OSPF_LSA table
The OSPF_LSA table contains information related to link state related configurations like LS age, LS id, lsa type, lsa sequence number, options, flags, checksum, prefix etc.

## OSPF configuration flows and protocol updates

The below diagram depicts the schema updation flow for few OSPFv2 related CLI commands and the OSPFv2 protocol updates, which covers most of the related tables.

```ditaa
                                                  +---------------+
                                                  |               |
                                                  |  OSPF_Router  |
                                         +-------->               |
                                         |        |               |
                                         |        +------+--------+
                                         |               |
                                         |             #2|
                                         |               |
                XXXXXXXXXXXXXXXXX        |        +------v--------+
                X               X        |        |               |
                X   Port        X        |        |  OSPF_Area    |
                X               X     #1 |        |               |
                X               X        |        |               |
                XXXXXXX+XXXXXXXXX        |        +------+--------+
                       |                 |               |
                       |                 |            #3 |
                       |                 |               |
                +------v--------+        |        +------v--------+
                |   OSPF_       |        |        |               |
         #0     | Interface_    |        |        |  OSPF_        |
Cmd-1 +--------->    Config     +--------+        |     Interface |
                |               |                 |               |
                +---------------+                 +---------------+


  +----+                            XXXXXXX
  |    |  Newly added tables        X     X   Existing tables           ------>
  +----+                            XXXXXXX                              Flow

Figure-3: Flow of the configuration changes through schema table objects for cmd-1
Cmd-1 : conf term -->> interface <ifname> -->> ip router ospf area <area-id>
```

In above Figure-3, flow of the configuration through the OVSDB schema tables for the command to enable the ospf protocol on an interface is depicted. The numbers along the flow-arrows are indicative of the order of the flow.

This command will create a corresponding row in the "OSPF_Interface_Config". If there is no corresponding row in the "OSPF_Router" and "OSPF_Area" tables, they will be created. It will also create a row in "OSPF_Interface" table as well.


```ditaa
                +---------------+                 +---------------+
                | OSPF_NBMA_    |                 |               |
         #0     | Neighbor_     |    #1           |  OSPF_Neighbor|
Cmd-2 +--------->   Config      +----------------->               |
                |               |                 |               |
                +---------------+                 +---------------+


  +----+                            XXXXXXX
  |    |  Newly added tables        X     X   Existing tables           ------>
  +----+                            XXXXXXX                               Flow

Figure-4: Flow of the configuration changes through schema table objects for cmd-2
Cmd-2 : conf term -->> interface <ifname> -->> ip ospf neighbor <nbr-ip>

```

In above Figure-4, flow of the configuration through the OVSDB schema tables for the command to configure a NBMA Neighbor an interface is depicted. The numbers along the flow-arrows are indicative of the order of the flow.

This command will create corresponding rows in the "OSPF_NBMA_Neighbor_Config". If may create a corresponding row in the "OSPF_Neighbor" table as well, depending on the validation of the configuration.


```ditaa

    +---------------+
    |               |
    |     Port      |
    |               |
    |               |
    +-------+-----^-+
            |     |
         #3 |     +------+
            |            |
    +-------v-------+    |          +---------------+
    |               |    |          |               |
    |  OSPF_        |    |          |   OSPF_Area   |
    |     Interface |    |          |               |
    |               |    |          |               |
    +------+--------+    |          +----------^----+
           |             |    #2               | #1
        #4 |             +-------------+       |
           |                           |       |
    +------v--------+               +--+-------+----+
    |               |               |               |
    |  OSPF_Neighbor|               |  OSPF_Vlink   |    #0
    |               |               |               <--------+ Cmd-3
    |               |               |               |
    +---------------+               +---------------+


  +----+                            XXXXXXX
  |    |  Newly added tables        X     X   Existing tables           +----->
  +----+                            XXXXXXX                               Flow

Figure-5: Flow of the configuration changes through schema table objects for cmd-3
Cmd-3 : conf term -->> router ospf -->> area <area-id> virtual-link <remote-ip>

```

In above Figure-5, flow of the configuration through the OVSDB schema tables for the command to configure a Virtual-link in a non backbone area is depicted. The numbers along the flow-arrows are indicative of the order of the flow.

This command will create a corresponding row in the "OSPF_Area" table if there is not already. It will create a corresponding row in the "Port" table to create "port" for the Vlink. A corresponding row in "OSPF_Interface" table will be created and through neighbor Finite State Machine (FSM) in the OSPFv2 protocol a corresponding row in "OSPF_Neighbor" may be created as well.


```ditaa

         Cmd-4
           +
           | #0
           |
    +------v-----+--+               +---v-----------+
    |               |    #1         |               |
    |  OSPF_Area    +--------------->  OSPF_Summary |
    |               |               |      _Address |
    |               |               |               |
    +---------------+               +-------+-------+
                                            |
                                            | #2
                                            |
                                    +-------v-------+
                                    |               |
                                    |  OSPF_LSA     |
                                    |               |
                                    |               |
                                    +---------------+

  +----+                            XXXXXXX
  |    |  Newly added tables        X     X   Existing tables           +----->
  +----+                            XXXXXXX                               Flow

Figure-6: Flow of the configuration changes through schema table objects for cmd-4
Cmd-4 : conf term -->> router ospf -->> area <area-id> range <A.B.C.D/M>
```

In above Figure-6, flow of the configuration through the OVSDB schema tables for the command to configure a area range summarization prefix is depicted. The numbers along the flow-arrows are indicative of the order of the flow.

This command will create a corresponding row in the "OSPF_Area" table if there is not already. It will create corresponding rows in the "OSPF_Summary_Address" table. This may in turn trigger OSPFv2 protocol to create and / or delete corresponding one or more rows in the "OSPF_LSA" table.


```ditaa

                                    +---------------+
+------------------+                |               |
|                  |       +-------->     Route     |
| OPS-OSPFD        |       |        |               |
|       Process    |       |        +---------------+
|                  |       |
| +--------------+ |       |        +---------------+
| |    SPF       + |-------+        |               |
| | Calculation  + |---------------->  OSPF_Route   |
| +--------------+ |                |               |
|                  |                +---------------+
|                  |
| +--------------+ |                +---------------+
| |LSA Origin/   | |                |               |
| |  Reception   + |---------------->  OSPF_LSA     |
| |              | |                |               |
| +--------------+ |                +---------------+
|                  |
|                  |
| +--------------+ |                +---------------+
| |    OSPF      | |                |               |
| |  Neighbor    + |----------------> OSPF_Neighbor |
| |    FSM       | |                |               |
| |              | |                +---------------+
| +--------------+ |
|                  |
| +--------------+ |                +---------------+
| |    OSPF      | |                |               |
| |  Interface   + |----------------> OSPF_Interface|
| |    FSM       | |                |               |
| |              | |                +---------------+
| +--------------+ |
|                  |
+------------------+

  +----+                            XXXXXXX
  |    |  Newly added tables        X     X   Existing tables           +----->
  +----+                            XXXXXXX                               Flow

Figure-7: Flow of the OSPFv2 protocol updates through schema table objects
```

In above Figure-7, flow of the OSPFv2 protocol updates through the OVSDB schema tables for different OSPFv2 protocol internal modules.

The SPF calculation module can create/delete/update the rows in "OSPF_Route" and "Route" tables.

The LSA Generation and Reception will update the OSPFv2 protocols Link Sate Data Base, which in turn can create/delete/update the rows in "OSPF_LSA" table.

The Neighbor FSM module can create/delete/update the rows in "OSPF_Neighbor" table.

The Neighbor FSM module can create/delete/update the rows in "OSPF_Interface" table.

## Functionality Support or Compliance

We will be supporting below compliances as part of the "OSPFv2 support on OpenSwitch:
- OSPFv2 RFC 2328, which is backward compatible to RFC 2178.
- Stub Router Advertisement RFC 3137.
- The OSPFv2 Not-So-Stubby Area (NSSA) RFC 3101.

The following may be supported at a later point in time:
- Non Broadcast Multiple Access (NBMA) Neighbors, which is part of the RFC 2328.
- The OSPFv2 Opaque LSA Option RFC 2370.
- Multiple VRF Support for OSPFv2.
- Route Maps support for OSPFv2.
- OSPFv2 Graceful Restart RFC 3623.
- SNMPv2 MIB Support RFC 4750 for OSPFv2.

The following are not planned for support at this time:
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
* [The OSPFv2 Not-So-Stubby Area (NSSA) RFC 3101](https://tools.ietf.org/html/rfc3101)
* [OSPFv2 MIB RFC 4750](https://tools.ietf.org/html/rfc4750)

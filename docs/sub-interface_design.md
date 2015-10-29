# High-level sub-interface & loopback interface design

Sub-interfaces are used on L3 router, to support router-on-a-stick configurations, and to allow to separate traffic on a particular VLAN to a separate port, and to selectively apply policies on them. Open vSwitch Database has port and interface tables to manage the physical and logical interfaces configured on the OpenSwitch. A sub-interface is a logical interface allowing layer 3 configurations and layer 2 configurations on a single interface. One interface may be split into multiple logical interfaces, each having different network IP address, and a dot1q encapsulation VLAN number. VLAN will be used to switch the incoming packets and to tag the outgoing packets, while IP address is used to route the packets.

A loopback interface is a virtual interface, supporting IPv4 address configuration, that remains up after you issue the no shutdown command until you disable it with the shutdown command.The loopback interface can be considered stable because once you enable it, it will remain up until you shut it down. This makes loopback interfaces ideal for assigning Layer 3 addresses such as IP addresses when you want a single address as a reference that is independent of the status of any physical interfaces in the networking device.


## Design choices
The OVS schema for interfaces and ports was adopted for maximum compatibility with Open vSwitch. Existing port table and interface table schema are extended to support sub-interfaces and loopback. Alternate approaches are adding a new table for sub-interfaces as they have a mix of port and interface table columns. Current design adheres to the port and interface design. Handling of addition/update/deletion of sub-interface and loopback interface are handled by extending the functionalities of **intfd** and **portd**. There is no new daemon introduced for sub-interface or loopback interface.


## Participating modules
Sub-interfaces are primarily managed by **portd**, **intfd**, and **vswitchd**. Please see the respective component documentation for more details about these daemons.

```
                                 ovsdb                   +--------+
                    +-----------------------------+  +---+ portd  |
                    |                             |  |   |        |
   +--------+       |                             |  |   +--------+
   |        |       |                             |  |   +--------+
   |  cli   +---------->  ***   port tbl  *** <------+---+        |
   |        |       |                 ^           |      | intfd  |
   |        +----------> *** interface|tbl*** <----------+        |
   +--------+       |           ^     |           |      +--------+
                    +-----------|-----|-----------+
                                |     |
                                |     |
                              +-+-----+------+
                              |              |
                              |   vswitchd   |
                              |              |
                              +--------------+

```


### intfd
The [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN) reads information from the port table and the interface table. The intfd determines if an interface should be brought up, based on user configuration and state information. The intfd updates the **hw_intf_config** field to tell **vswitchd** if an interface is to be enabled or disabled in hardware. When the parent interface is configured as administratively down, all its sub-interfaces are brought down. They will be brought up when the parent interface is up as well as the sub-interface is up. If the parent interface is link_down, all its sub-interfaces also will be down.

### portd
The [Port Daemon (portd)](http://www.openswitch.net/documents/dev/ops-portd/DESIGN) reads information from the port table. User configurations like IP address, Dot1q encapsulation VLAN Id etc. are validated by portd. The portd updates the **hw_config** field to notify **vswitchd** when the user configure any of these parameters. When the parent interface is configured as L2 interface by "no routing" command, all its sub-interfaces will be removed.

### vswitchd
The [Virtual Switch Daemon (vswitchd)](http://www.openswitch.net/documents/dev/ops-openvswitch/DESIGN) is the daemon that ultimately drives control to and reports state and statistics from the switching ASIC. It monitors the **hw_intf_config** field and takes appropriate action in the hardware. For the switch image, **vswitchd** calls the BCM plug-in APIs to configure the ASIC and also setup the Linux kernel virtual interfaces. For the host based VSI image, it setup the interfaces in Linux.


## OVSDB-Schema


### Port table
```
Port:interfaces  (cli, rest, etc) - uuid of corresponding interface row entry
Port:name        (cli, rest, etc) - Sub-interface name as "parent_interface"."sub-interface"
Port:trunks      (cli, rest, etc) - The dot1q encapsulation VLAN id.
Port:vlan_mode   (cli, rest, etc) - Always set to “trunk”.
Port:ip4_address (cli, rest, etc) - User configured IP address.
Port:hw_config   (intfd)          - for vswitchd to consume.

```
See the [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN) and the [Port Daemon (portd)](http://www.openswitch.net/documents/dev/ops-portd/DESIGN).



### Interface table
```
Interface:name           (cli, rest, etc) - sub-interface name, identical to port row entry.
Interface:statistics     (vswitchd)       - statistics of the sub-interface.
Interface:user_config    (cli, rest, etc) - administrative state (up/down) of the sub-interface.
Interface:hw_intf_config (intfd)          - for vswitchd to consume the user configurations.
```
See the [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN), and the [Virtual Switch Daemon (vswitchd)](http://www.openswitch.net/documents/dev/ops-openvswitch/DESIGN).
Refer the section OVSDB-Schema in [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN) for other rows and their usage.


## Functionality
### Sub-interfaces
* Creation of sub-interfaces
While creating a sub-interface, a port table entry and an interface table entry are created. Naming convention used for sub-interface is parent_interface.subinterface_number. The port table has interface row, having the uuid of the sub-interface entry. Other fields like ip4_address, trunks, vlan_mode are populated by the configuring daemon like **clid** or **restd**. Interface table has the administrative up/down, statistics etc. The port table entry will be attached to both VRF table and bridge table.

* Handling parent interface config changes
Configuring the parent interface as L2 interface will remove all sub-interfaces created under it. Administratively bringing down the parent interface will bring the state of it down, which will bring down all its sub-interfaces. Common properties like MTU, speed etc. will be copied to the interface table entry of all its sub-interfaces when they are configured on the parent interface.

* Handling parent interface state changes
When the parent interface is down, all its sub-interfaces will be brought down.

###Loopback interfaces
Loopback interfaces are logical interfaces, allowing admin to configure IP addresses. These IP addresses can be advertised by routing protocols, used as router identifiers, as source address, or as a fixed IP address that could be reached if at least one link to the router is operational. The allowed configurations are IP address, and enable/disable.

* Creation of loopback interfaces
For each loopback interface, there will be a port table entry created, which holds the IP4 address, and an interface table entry - where administrative state and statistics are kept.

* Default behaviour
No loopback interface will be created by default. Administrator will have to configure the loopback interface, assign IP address and enable them to be operational.

### Interface Type
The **interface:type** field identifies the interface type. All physical interfaces, those representing true hardware physical interfaces (aka face-plate interfaces), are of the type **system**. There are other interfaces used for internal communication purposes that are of the type **internal**. Interfaces of the type **internal** are not managed or configured directly by users. Sub-interfaces are identified by **vlansubint** type. Loopback interface use the type **loopback**.

## References
* [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN)
* [Virtual Switch Daemon (vswitchd)](http://www.openswitch.net/documents/dev/ops-openvswitch/DESIGN)
* [Port Daemon (portd)](http://www.openswitch.net/documents/dev/ops-portd/DESIGN)

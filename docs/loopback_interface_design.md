# High-level loopback interface design

A loopback interface is a virtual interface, supporting IPv4/IPv6 address configuration, that remains up after you issue the no shutdown command until you disable it with the shutdown command.The loopback interface can be considered stable because once you enable it, it will remain up until you shut it down. This makes loopback interfaces ideal for assigning Layer 3 addresses such as IP addresses when you want a single address as a reference that is independent of the status of any physical interfaces in the networking device.


## Design choices
The OVS schema for interfaces and ports was adopted for maximum compatibility with Open vSwitch. Existing port table and interface table schema are extended to support loopback. Current design adheres to the port and interface design. Handling of addition/update/deletion of loopback interface are handled by extending the functionalities of **intfd** and **portd**. There is no new daemon introduced for loopback interface.


## Participating modules
Loopback interfaces are primarily managed by **portd**, **intfd**, and **vswitchd**. Please see the respective component documentation for more details about these daemons.

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
The [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN) reads information from the port table and the interface table. The intfd determines if an interface should be brought up, based on user configuration and state information. The intfd updates the **hw_intf_config** field to tell **vswitchd** if a loopback interface is to be enabled or disabled.

### portd
The [Port Daemon (portd)](http://www.openswitch.net/documents/dev/ops-portd/DESIGN) reads information from the port table. User configurations like IP address are validated by portd. The portd updates the **hw_config** field to notify **vswitchd** when the user configure any of these parameters.

### vswitchd
The [Virtual Switch Daemon (vswitchd)](http://www.openswitch.net/documents/dev/ops-openvswitch/DESIGN) is the daemon that ultimately drives control to and reports state and statistics from the switching ASIC. It monitors the **hw_intf_config** field and takes appropriate action in the hardware. For the switch image, **vswitchd** calls the BCM plug-in APIs to configure the ASIC and also setup the Linux kernel virtual interfaces. For the host based VSI image, it setup the interfaces in Linux.


## OVSDB-Schema


### Port table
```
Port:interfaces  (cli, rest, etc) - uuid of corresponding interface row entry
Port:name        (cli, rest, etc) - Sub-interface name as "parent_interface"."sub-interface"
Port:ip4_address (cli, rest, etc) - User configured IP address.
Port:ip6_address (cli, rest, etc) - User configured IPv6 address.
Port:hw_config   (intfd)          - for vswitchd to consume.

```
See the [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN) and the [Port Daemon (portd)](http://www.openswitch.net/documents/dev/ops-portd/DESIGN).



### Interface table
```
Interface:name           (cli, rest, etc) - sub-interface name, identical to port row entry.
Interface:statistics     (vswitchd)       - statistics of the sub-interface.
Interface:user_config    (cli, rest, etc) - administrative state (up/down) of the sub-interface.
Interface:hw_intf_config (intfd)          - for vswitchd to consume the user configurations.
Interface:type           (cli, rest, etc) - loopback interfaces are identified by the type `loopback`.
```
See the [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN), and the [Virtual Switch Daemon (vswitchd)](http://www.openswitch.net/documents/dev/ops-openvswitch/DESIGN).
Refer the section OVSDB-Schema in [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN) for other rows and their usage.


###Loopback interfaces
Loopback interfaces are logical interfaces, allowing admin to configure IP addresses. These IP addresses can be advertised by routing protocols, used as router identifiers, as source address, or as a fixed IP address that could be reached if at least one link to the router is operational. The allowed configurations are IP address, and enable/disable.

* Creation of loopback interfaces
For each loopback interface, there will be a port table entry created, which holds the IPv4/IPv6 address, and an interface table entry - where administrative state and statistics are kept.

* Default behaviour
No loopback interface will be created by default. Administrator will have to configure the loopback interface, assign IP address and enable them to be operational.

### Interface Type
The **interface:type** field identifies the interface type. All physical interfaces, those representing true hardware physical interfaces (aka face-plate interfaces), are of the type **system**. There are other interfaces used for internal communication purposes that are of the type **internal**. Interfaces of the type **internal** are not managed or configured directly by users. Sub-interfaces are identified by **vlansubint** type. Loopback interface use the type **loopback**.

## References
* [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN)
* [Virtual Switch Daemon (vswitchd)](http://www.openswitch.net/documents/dev/ops-openvswitch/DESIGN)
* [Port Daemon (portd)](http://www.openswitch.net/documents/dev/ops-portd/DESIGN)

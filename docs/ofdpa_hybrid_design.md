# High level design of OpenFlow Hybrid Switch (OF-DPA) Feature

The OpenFlow Hybrid Switch (OF-DPA) Feature is contained within the ops-switchd daemon.

Code in the ops-switchd repository contains an implementation of an OpenFlow agent. This implementation comes from the Open vSwitch code on which ops-switchd is based. Information about the OpenFlow agent from Open vSwitch can be found in the ovs repository ([openswitch/ovs](http://git.openswitch.net/cgit/openswitch/ovs)).

The OpenNSL plugin in the ops-switchd-opennsl-plugin repository contains code that implements OpenFlow related APIs defined in the ASIC plugin interface. The details of the design is found in DESIGN.md document found in the ops-switchd-opennsl-plugin repository.

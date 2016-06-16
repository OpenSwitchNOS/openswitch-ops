#MSTP Feature

**Table of Contents**

[TOC]

High level design of ops-stpd
==============================

The ops-stpd process manages to avoid bridge loops (multiple paths linking one segment to another, resulting in an infinite loop situation).

Responsibilities
----------------
The ops-stpd process is responsible for managing all MSTP Instances defined by the user.

Design choices
--------------
N/A

Relationships to external OpenSwitch entities
---------------------------------------------
```ditaa`
+-------------+      +-------------+       +------+
|             +------>Interfaces   +       +      +
|             |      +		     +-------+ PEER +
|             |      +-------------+       +------+
| ops-stpd    |
|             |
|             |
|             |
|             |       +--------------+
|             +------->              |
+-------------+       |              |
                      |   database   |
                      |              |
+-------------+       |              |
|             +------->              |
|             |       |              |
|             |       +--------------+
|  switchd    |
|             |       +--------+
|             +------->        |
|             |       | SWITCH |
+-------------+       |        |
                      +--------+

```
The ops-stpd process monitors the MSTP related Schema in the database. As the configuration and state information for the ports and interfaces are changed, ops-stpd examines the data to determine if there are new Instances being defined in the configuration and if state information for interfaces has changed. The ops-stpd process uses this information to configure MSTP Instances and update the MSTP protocol state machines.

The ops-stpd process registers for MSTP protocol packets on all L2 interfaces configured for MSTP, and sends and receives state information to the peer through the interfaces.

When the state information maintained by ops-stpd changes, it updates the information in the database. Some of this information is strictly status, but this also includes hardware configuration, which is used by switchd to configure the switch.

OVSDB-Schema
------------
The following OpenSwitch database schema elements are referenced by ops-stpd:

Configuration Columns are listened by ops-stpd for changes in the configuration.
Status Columns are written into DB by ops-stpd by comparing configuration with priority vectors received from BPDU.

Bridge Table:
	Configuration Column:
		mstp_enable : to determine MSTP enable or disable
	Status Column:
		mstp_instances : References to MSTP Instances
		mstp_common_instance : References to MSTP Common Instance

MSTP_Instance:
	Configuration Columns:
		vlans : VLANS associated to the particular MSTP Instance
		priority : to determine MSTP Instance priority

	Status Columns:
		bridge_identifier : to set the bridge identifier for this instance.
		mstp_instance_ports : Reference to PORTs associated to this Instance.
		hardware_grp_id : to store Hardware Group ID to this instance
		designated_root : Designated root for this instance
		root_path_cost : Path cost to the root for this instance
		root_priority : Priority of the root in this instance
		root_port : Port which is connected to Root.
		remaining_hops : to keep track of the number of remaining hops
		time_since_top_change : To store the time since the topology has changed
		top_change_cnt : to keep track of the number of topology Changes.
		topology_change_disable: this is will be set when topology change happens

MSTP_Common_Instance:
	Configuration Columns:
		vlans : VLANS associated to the particular MSTP Instance
		priority : to determine MSTP Instance priority
		hello_time : Hello time for Common instance
		forward_delay : Forward delay time for Common instance
		max_age : Max Age for Common instance
		tx_hold_count : TX hold count for Common instance
	Status Columns:
		bridge_identifier : to set the bridge identifier for this instance.
		mstp_common_instance_ports : References to ports associated with MSTP Common Instance
		hardware_grp_id : to store Hardware Group ID to this instance
		designated_root : Designated root for this instance
		root_path_cost : Path cost to the root for this instance
		root_priority : Priority of the root in this instance
		root_port : Port which is connected to Root.
		regional_root : To Store the Regional Root for the CST
		cist_path_cost : Path cost for the CIST
		remaining_hops : to keep track of the number of remaining hops
		oper_hello_time : To set the Oper Hello time based on the priority vectors
		oper_forward_delay : To set the Oper Forward Delay based on the priority vectors
		oper_max_age : to set the Max Age based on the priority vectors
		hello_expiry_time : to keep track of Hello Expiry time
		forward_delay_expiry_time : To keep track of Forward delay expiry time
		time_since_top_change : To Keep track of time since topology change
		oper_tx_hold_count : To set the Oper TX hold count based on the priority vectors
		top_change_cnt : to keep track of the count of changes in topology


MSTP_Common_Instance_Port :
	Configuration Columns:
		port_priority : Priority of the port in CIST
		admin_path_cost : Path cost set by admin to the interface
		admin_edge_port_disable : to set the port as admin edge
		bpdus_rx_enable : to enable bpdu rx
		bpdus_tx_enable : to enable bpdu tx
		restricted_port_role_disable : to enable restricted port role
		restricted_port_tcn_disable : to enable restricted port tcn
		bpdu_guard_disable : to enable bpdu guard
		loop_guard_disable : to enable loop guard
		root_guard_disable : to enable root guard
		bpdu_filter_disable : to enable bpdu filter
	Status Columns:
		port : Reference the port row
		port_role : to set the port role for the CIST
		port_state : to set the port state for the CIST
		link_type : to set the link type for the CIST
		oper_edge_port : To check if the port is oper edge
		cist_regional_root_id : To store the Regional Root
		cist_path_cost : to store the path cost to the CIST Root
		port_path_cost : to store the path cost to the Root
		designated_path_cost : to store the path cost to the Designated Root
		designated_bridge : to store the mac address of designated Bridge
		designated_port : to store the port of the Designated root.
		port_hello_time : to store the operational Hello time
		protocol_migration_enable : To enable the protocol migration.
	Statistics Column:
		mstp_statistics: to store MSTP statistics.

MSTP_Instance_Port :
	Configuration Columns:
		port_priority : Priority of the port in CIST
		admin_path_cost : Path cost set by admin to the interface
	Status Columns:
		port : Reference the port row
		port_role : to set the port role for the CIST
		port_state : to set the port state for the CIST
		designated_root : to store the mac address of Designated Root.
		designated_root_priority : to store the priority of the designated root
		designated_cost : to store the cost to the designated root.
		designated_bridge : to store the mac address of designated Bridge
		designated_port : to store the port of the Designated root.
		designated_bridge_priority : to store the priority of th designated bridge

MSTP BPDU Format
----------------
```ditaa
+--------------------------------------+
|           Protocol Identifier        |1-2
+--------------------------------------+
|     Protocol Version Identifier      |3
+--------------------------------------+
|              BPDU Type               |4
+--------------------------------------+
|             CIST Flags               |5
+--------------------------------------+
|    	CIST Root Identifier           |6-13
+--------------------------------------+
|      CIST External Path cost         |14-17
+--------------------------------------+
|    CIST Regional Root Identifier     |18-25
+--------------------------------------+
|       CIST Port Identifier           |26-27
+--------------------------------------+
|           Message Age                |28-29
+--------------------------------------+
|             Max Age                  |30-31
+--------------------------------------+
|            Hello Time                |32-33
+--------------------------------------+
|          Forward Delay               |34-35
+--------------------------------------+
|        Version 1 Length = 0          |36
+--------------------------------------+
|         Version 3 Length             |37-38
+--------------------------------------+
|      MST configuration Identifier    |39-89
+--------------------------------------+
|      CIST Internal Path cost         |90-93
+--------------------------------------+
|       CIST Bridge Identifier         |94-101
+--------------------------------------+
|        CIST Remaining Hops           |102
+--------------------------------------+
| MSTI configuration Messages          |103-39+Version 3 Length
+--------------------------------------+
```
When we configure only CIST and enable a spanning-tree MSTP BPDUs will be sent out with a length of 119 bytes incremented by 16 bytes for each instance.

Internal structure
------------------
The ops-stpd process has three operational threads:
* ovsdb_thread
  This thread processes the typical OVSDB main loop, and handles any changes. Some changes are handled by passing messages to the mstpd_protocol_thread thread.
* mstpd_protocol_thread
  This thread processes messages sent to it by the other two threads. Processing of the messages includes operating the finite state machines.
* mstp_rx_pdu_thread
  This thread waits for MSTP packets on interfaces. When a packet is received, it sends a message (including the packet data) to the mstpd_protocol_thread thread for processing through the state machines.

Event Handling
---------------
The ops-stpd process handles multiple events received from OVSDB updates.
* L2Port Add:
  When a l2port is created in OVSDB, daemon will creata a entry for CIST_port and MSTI_port if exists. Updates the daemon data structures and if MSTP is enabled it triggers the state machines which are relevant. Split/LAG ports does not have any special functionality from ops-stpd perspective.
* L2Port Delete:
  When a l2port is being removed in OVSDB, daemon will remove the respective CIST and MSTI port entries. Clears the daemon data structures for the ports being deleted. Split/LAG ports does not have any special functionality from ops-stpd perspective.
* VLAN Add:
  When a VLAN is being added in OVSDB, daemon will map newly added VLAN into CIST by default. In Daemon restart scenario, daemon will check if the VLAN is already mapped in CIST/MSTI and the add into CIST or ignore if present.
* VLAN Delete:
  When a VLAN is being deleted in OVSDB, daemon will unmap the VLANS from CIST/MSTI wherever it is mapped. When the last VLAN is being deleted from Instance, Instance should be deleted from the daemon.
* Packet Receive:
  The ops-stpd process the MSTP packets from the Peers, and compares with the config related parameters in the DB.

Daemon calculates the priority vectors and takes a decision on the ports which has to be forwarded and blocked.
ops-stpd also updates DB on the state changes/statistics/status parameters in interfaces based on priority vectors.

Once daemon sets port state as Forwarding/Blocking/Learning, switchd plugin shall take care of setting the values into the Hardware.

Daemon Restartablity
--------------------
When a ops-stpd process crashes, daemon cleans up the status and statistics columns in the daemon, tries to restart with the configuration columns present in the DB. This area can be improved by supporting High Availablity.

Other Feature Interactions
--------------------
ops-stpd interacts with port-pecking order feature, which decides whether the control packets can be carried over to the daemon based on the Priority of the protocol which has set the Port State as Blocking/Forwarding. Please refer to [Port Pecking Order Design](http://git.openswitch.net/cgit/openswitch/ops/plain/docs/port_state_pecking_order_design.md)

ops-stpd also interacts with link aggregation daemon to operate on LAGs, to get the bond status and bond speed for the link aggregation formed by Link Aggregation.
Please refer to [Link Aggregation Design](http://git.openswitch.net/cgit/openswitch/ops/tree/docs/link_aggregation_design.md)


Troubleshooting Support
-----------------------
ops-stpd daemon has some support for debugging in case of any issues.
There are two options to troubleshoot ops-stpd daemon
1. diag-dump mstp basic : This will list all the data in daemon.
2. Bash commands: To see the segregated data based on Instances or Ports. Below are the commands
* ovs-appctl -t ops-stpd mstpd/ovsdb/cist
* ovs-appctl -t ops-stpd mstpd/ovsdb/cist_port <port>
* ovs-appctl -t ops-stpd mstpd/ovsdb/msti <msti>
* ovs-appctl -t ops-stpd mstpd/ovsdb/msti_port <msti> <port>
* ovs-appctl -t ops-stpd mstpd/daemon/cist
* ovs-appctl -t ops-stpd mstpd/daemon/cist_port <port>
* ovs-appctl -t ops-stpd mstpd/daemon/msti <msti>
* ovs-appctl -t ops-stpd mstpd/daemon/msti_port <msti> <port>

References
----------
*  [Port Pecking Order Design](http://git.openswitch.net/cgit/openswitch/ops/plain/docs/port_state_pecking_order_design.md)

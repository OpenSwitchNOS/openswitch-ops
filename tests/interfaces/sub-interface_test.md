# Subinterfaces feature Test Cases
<!-- TOC depth:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Subinterfaces feature Test Cases](#subinterfaces-feature-test-cases)
	- [Verify L3 reachability of sub-interface](#verify-l3-reachability-of-sub-interface)
		- [Objective](#objective)
		- [Requirements](#requirements)
		- [Setup](#setup)
			- [Topology Diagram](#topology-diagram)
			- [Test Setup](#test-setup)
		- [Description](#description)
		- [Test Result Criteria](#test-result-criteria)
			- [Test Pass Criteria](#test-pass-criteria)
			- [Test Fail Criteria](#test-fail-criteria)
	- [Verify sub-interface admin state](#verify-sub-interface-admin-state)
		- [Objective](#objective)
		- [Requirements](#requirements)
		- [Setup](#setup)
			- [Topology Diagram](#topology-diagram)
			- [Test Setup](#test-setup)
		- [Description](#description)
		- [Test Result Criteria](#test-result-criteria)
			- [Test Pass Criteria](#test-pass-criteria)
			- [Test Fail Criteria](#test-fail-criteria)
	- [Verify routing on L3 sub-interfaces](#verify-routing-on-l3-sub-interfaces)
		- [Objective](#objective)
		- [Requirements](#requirements)
		- [Setup](#setup)
			- [Topology Diagram](#topology-diagram)
			- [Test Setup](#test-setup)
		- [Description](#description)
		- [Test Result Criteria](#test-result-criteria)
			- [Test Pass Criteria](#test-pass-criteria)
			- [Test Fail Criteria](#test-fail-criteria)
<!-- /TOC -->

##  Verify L3 reachability of sub-interface

### Objective
Verify the reachability of IP address set on sub-interface

### Requirements
The requirements for this test case are:
 - openswitch
 - vlan aware host

### Setup
Connect openswitch interface 1 to eth0 on host

#### Topology Diagram
#### Test Setup
### Description
 - Create vlan interface eth0.100 on host
 - Assign ip 192.168.1.2/24 to eth0.100
 - Run routing command on interface 1 on openswitch
 - Create sub-interface 1.1 on interface 1
 - Set dot1q encapsulation to 100 on 1.1
 - Assign ip 192.168.1.1/24 to 1.1
 - Ping 192.168.1.1 from host
### Test Result Criteria
Ping result

#### Test Pass Criteria
Ping succeeds

#### Test Fail Criteria
Ping fails

##  Verify sub-interface admin state

### Objective
Verify the sub-interface admin state

### Requirements
The requirements for this test case are:
 - openswitch
 - vlan aware host

### Setup
Connect openswitch interface 1 to eth0 on host

#### Topology Diagram

#### Test Setup

### Description
 - Create vlan interface eth0.100 on host
 - Assign ip 192.168.1.2/24 to eth0.100
 - Run routing command on interface 1 on openswitch
 - Create sub-interface 1.1 on interface 1
 - Run no shutdown on 1.1
 - Set dot1q encapsulation to 100 on 1.1
 - Assign ip 192.168.1.1/24 to 1.1
 - Ping 192.168.1.1 from host
 - Run shutdown on 1.1
 - Ping 192.168.1.1 from host

### Test Result Criteria
Ping result

#### Test Pass Criteria
Ping succeeds when sub-interface is enabled
Ping fails when sub-interface is disabled

#### Test Fail Criteria
Ping fails when sub-interface is enabled

##  Verify routing on L3 sub-interfaces

### Objective

Verify inter-vlan routing across L3 sub-interfaces

### Requirements
The requirements for this test case are:

 - ops 1
 - ops 2
 - vlan aware host 1
 - vlan aware host 2

### Setup
connect openswitch 1 interface 1 to ops 2 interface 3
connect host 1 to ops 2 interface 1
connect host 2 to ops 2 interface 2

#### Topology Diagram

#### Test Setup

### Description
 - On ops 1, configure sub-interface 1.100 with IP address  192.168.1.2/4
 - On ops 1, configure sub-interface 1.200 with IP address  182.168.1.2/4
 - On ops 2, Configure interface 3 as trunk
 - On ops 2, configure vlan 100 and vlan 200 on the trunk
 - Add host 1 in vlan 100 on openswtich 2
 - Configure subnet 192.168.1.1/24 on host 1 with 192.168.1.2 as default gateway
 - Add host 2 in vlan 200 on openswitch 2
 - Configure subnet 182.168.1.1/24 on host 2 with 182.168.1.2 as default gateway
 - ping host 2 from host 1

### Test Result Criteria
Ping result

#### Test Pass Criteria
Ping succeeds

#### Test Fail Criteria
Ping fails

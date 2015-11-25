# Subinterfaces Feature Test Cases
## Contents

- [Verify L3 reachability of sub-interface](#verify-l3-reachability-of-sub-interface)
- [Verify sub-interface admin state](#verify-sub-interface-admin-state)
- [Verify L3 sub-interfaces with L2 VLAN](#verify-l3-sub-interfaces-with-l2-vlan)
- [Verify L2 VLANs with L3 sub-interface](#verify-l2-vlans-with-l3-sub-interface)

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
 - Run no shutdown on 1.1
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

##  Verify L3 sub-interfaces with L2 VLAN

### Objective

Verify L3 sub-interfaces with L2 VLAN

### Requirements
The requirements for this test case are:

 - ops 1
 - vlan aware host 1
 - vlan aware host 2
 - vlan aware host 3

### Setup
connect host 1 to ops 1 interface 1
connect host 2 to ops 1 interface 2
connect host 3 to ops 1 interface 3

#### Topology Diagram

#### Test Setup

### Description
 - create vlan 100 on ops 1 with interface 2 and interface 3
 - Create vlan interface eth0.100 on host
 - Assign ip 192.168.1.2/24 to eth0.100
 - Run routing command on interface 1 on openswitch
 - Create sub-interface 1.1 on interface 1
 - Run no shutdown on 1.1
 - Set dot1q encapsulation to 100 on 1.1
 - Assign ip 192.168.1.1/24 to 1.1
 - Ping 192.168.1.1 from host
 - delete vlan 100 on ops 1 with interface 2 and interface 3
 - Ping 192.168.1.1 from host

### Test Result Criteria
Ping result

#### Test Pass Criteria
Ping succeeds

#### Test Fail Criteria
Ping fails

##  Verify L2 VLANs with L3 sub-interface

### Objective

Verify L2 VLANs with L3 sub-interface

### Requirements
The requirements for this test case are:

 - ops 1
 - vlan aware host 1
 - vlan aware host 2
 - vlan aware host 3

### Setup
connect host 1 to ops 1 interface 1
connect host 2 to ops 1 interface 2
connect host 3 to ops 1 interface 3

#### Topology Diagram

#### Test Setup

### Description
 - create vlan 100 on ops 1 with interface 2 and interface 3
 - Create vlan interface eth0.100 on host
 - Assign ip 192.168.1.2/24 to eth0.100
 - Run routing command on interface 1 on openswitch
 - Create sub-interface 1.1 on interface 1
 - Run no shutdown on 1.1
 - Set dot1q encapsulation to 100 on 1.1
 - Assign ip 192.168.1.1/24 to 1.1
 - Ping 192.168.1.1 from host
 - Put host 2 and host in the same sub-net
 - Ping host 2 from host 3 and vice-versa

### Test Result Criteria
Ping result

#### Test Pass Criteria
Ping succeeds

#### Test Fail Criteria
Ping fails

# Subinterfaces Feature Test Cases
## Contents

- [Verify L3 reachability of sub-interface](#verify-l3-reachability-of-sub-interface)
- [Verify sub-interface admin state](#verify-sub-interface-admin-state)
- [Verify L3 sub-interfaces with L2 VLAN](#verify-l3-sub-interfaces-with-l2-vlan)
- [Verify L2 VLANs with L3 sub-interface](#verify-l2-vlans-with-l3-sub-interface)
- [Verify routing on L3 sub-interfaces](#verify-routing-on-l3-sub-interfaces)

##  Verify L3 reachability of sub-interface

### Objective
Verify the reachability of the IP address set on the sub-interface.

### Requirements
The requirements for this test case are:
 - OpenSwitch
 - VLAN aware host

### Setup
Connect OpenSwitch interface 1 to eth0 on the host.

#### Topology diagram
#### Test setup
### Description
1. Create VLAN interface eth0.100 on host.
2. Assign IP 192.168.1.2/24 to eth0.100.
3. Run routing command on interface 1 on OpenSwitch.
4. Create sub-interface 1.1 on interface 1.
5. Run no shutdown on 1.1.
6. Set dot1q encapsulation to 100 on 1.1.
7. Assign IP 192.168.1.1/24 to 1.1.
8. Ping 192.168.1.1 from the host.

### Test Result Criteria
Ping result.

#### Test pass criteria
Ping succeeds.

#### Test fail criteria
Ping fails.

##  Verify sub-interface admin state

### Objective
Verify the sub-interface admin state.

### Requirements
The requirements for this test case are:
 - OpenSwitch
 - VLAN aware host

### Setup
Connect OpenSwitch interface 1 to eth0 on the host.
#### Topology diagram

#### Test setup

### Description
1. Create VLAN interface eth0.100 on the host.
2. Assign IP 192.168.1.2/24 to eth0.100.
3. Run routing command on interface 1 on OpenSwitch.
4. Create sub-interface 1.1 on interface 1. 5. Run no shutdown on 1.1.
5. Run no shutdown on 1.1.
6. Set dot1q encapsulation to 100 on 1.1.
7. Assign IP 192.168.1.1/24 to 1.1.
8. Ping 192.168.1.1 from the host.
9. Run shutdown on 1.1.
10. Ping 192.168.1.1 from the host.

### Test Result Criteria
Ping result.

#### Test pass criteria
Ping succeeds when sub-interface is enabled.
Ping fails when sub-interface is disabled.

#### Test fail criteria
Ping fails when sub-interface is enabled.

##  Verify L3 sub-interfaces with L2 VLAN

### Objective

Verify L3 sub-interfaces with L2 VLAN.

### Requirements
The requirements for this test case are:

 - ops 1
 - VLAN aware host 1
 - VLAN aware host 2
 - VLAN aware host 3

### Setup
1. Connect host 1 to ops 1 interface 1.
2. Connect host 2 to ops 1 interface 2.
3. Connect host 3 to ops 1 interface 3.
#### Topology diagram

#### Test setup

### Description
1. Create VLAN 100 on ops 1 with interface 2 and interface 3.
2. Create VLAN interface eth0.100 on host.
3. Assign IP 192.168.1.2/24 to eth0.100.
4. Run routing command on interface 1 on OpenSwitch.
5. Create sub-interface 1.1 on interface 1.
6. Run no shutdown on 1.1.
7. Set dot1q encapsulation to 100 on 1.1.
8. Assign IP 192.168.1.1/24 to 1.1.
9. Ping 192.168.1.1 from the host.
10. Delete VLAN 100 on ops 1 with interface 2 and interface 3.
11. Ping 192.168.1.1 from the host.

### Test result criteria
Ping result.

#### Test pass criteria
Ping succeeds.

#### test fail criteria
Ping fails.

##  Verify L2 VLANs with L3 sub-interface

### Objective

Verify L2 VLANs with L3 sub-interface.

### Requirements
The requirements for this test case are:

 - OpenSwitch 1
 - VLAN aware host 1
 - VLAN aware host 2
 - VLAN aware host 3

### Setup
1. Connect host 1 to ops 1 interface 1.
2. Connect host 2 to ops 1 interface 2.
3. Connect host 3 to ops 1 interface 3.

#### Topology diagram

#### Test setup

### Description
1. Create VLAN 100 on ops 1 with interface 2 and interface 3.
2. Create VLAN interface eth0.100 on the host.
3. Assign IP 192.168.1.2/24 to eth0.100.
4. Run routing command on interface 1 on OpenSwitch.
5. Create sub-interface 1.1 on interface 1.
6. Run no shutdown on 1.1.
7. Set dot1q encapsulation to 100 on 1.1.
8. Assign IP 192.168.1.1/24 to 1.1.
9. Ping 192.168.1.1 from the host.
10. Put host 2 and host in the same sub-net.
11. Ping host 2 from host 3 and vice-versa.

### Test result criteria
Ping result.

#### Test pass criteria
Ping succeeds.

#### Test fail criteria
Ping fails.

##  Verify routing on L3 sub-interfaces

### Objective

Verify the inter-vlan routing on L3 sub-interfaces.

### Requirements

The requirements for this test case are:

 - Openswitch 1
 - Openswitch 2
 - VLAN aware host 1
 - VLAN aware host 2

### Setup
1. Connect openswitch 1 interface 1 to ops 2 interface 3.
2. Connect host 1 to ops 2 interface 1.
3. Connect host 2 to ops 2 interface 2.

#### Topology diagram

#### Test setup

### Description
1. On Openswitch 1, configure sub-interface 1.100 (Set dot1q encapsulation to 100) with IP address 192.168.1.2/4.
2. On Openswitch 1, configure sub-interface 1.200 (Set dot1q encapsulation to 200) with IP address  182.168.1.2/4.
3. On Openswitch 2, Configure interface 3 as trunk.
4. On ops 2, configure vlan 100 and vlan 200 on the trunck.
5. Add host 1 in vlan 100 on openswtich 2.
6. Configure subnet 192.168.1.1/24 on host 1 with 192.168.1.2 as default gateway.
7. Add host 2 in vlan 200 on openswitch 2.
8. Configure subnet 182.168.1.1/24 on host 2 with 182.168.1.2 as default gateway.
9. ping host 2 from host 1.

### Test result criteria
Ping result.

#### Test pass criteria
Ping succeeds.

#### Test fail criteria
Ping fails.

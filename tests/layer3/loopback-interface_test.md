# Loopback Interface Feature Test Cases

## Contents

- [Verify L3 reachability of loopback interface](#verify-l3-reachability-of-loopback-interface)
- [Verify L3 non-reachability of loopback interface](#verify-l3-non-reachability-of-loopback-interface)


##  Verify L3 reachability of loopback interface

### Objective
Verify the reachability of IP address set on loopback interface.

### Requirements
The requirements for this test case are:
 - OpenSwitch
 - host

### Setup
Connect OpenSwitch interface 1 to eth0 on host

#### Topology diagram
#### Test setup
### Description
1. Assign IP 192.168.1.2/24 to eth0 on the host.
2. Create loopback interface.
3. Assign IP 192.168.1.1/24 to loopback interface 1.
4. Ping 192.168.1.1 from the host.

### Test result criteria
Ping result.

#### Test pass criteria
Ping succeeds.

#### Test fail criteria
Ping fails.

##  Verify L3 non-reachability of loopback interface

### Objective
Verify the non-reachability of the IP address set on the loopback interface.

### Requirements
The requirements for this test case are:
 - OpenSwitch
 - host

### Setup
Connect openswitch interface 1 to eth0 on host.

#### Topology diagram
#### Test setup
### Description
1. Assign IP 192.168.1.2/24 to eth0 on host.
2. Create loopback interface 1.
3. Assign IP 192.168.1.1/24 to loopback interface 1.
4. Ping 192.168.1.1 from host.
5. Remove loopback interface 1.
6. Ping 192.168.1.1 from host.

### Test result criteria
Ping result.

#### Test pass criteria
Ping fails.

#### Test fail criteria
Ping succeeds.

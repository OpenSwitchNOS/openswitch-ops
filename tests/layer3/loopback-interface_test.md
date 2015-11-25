# Loopback Interface Feature Test Cases

## Contents

- [Verify L3 reachability of loopback interface](#verify-l3-reachability-of-loopback-interface)
- [Verify L3 non-reachability of loopback interface](#verify-l3-non-reachability-of-loopback-interface)


##  Verify L3 reachability of loopback interface

### Objective
Verify the reachability of IP address set on loopback interface

### Requirements
The requirements for this test case are:
 - openswitch
 - host

### Setup
Connect openswitch interface 1 to eth0 on host

#### Topology diagram
#### Test setup
### Description
Assign ip 192.168.1.2/24 to eth0 on host
Create loopback interface 1
Assign ip 192.168.1.1/24 to loopback interface 1
Ping 192.168.1.1 from host

### Test result criteria
Ping result

#### Test pass criteria
Ping succeeds

#### Test fail criteria
Ping fails

##  Verify L3 non-reachability of loopback interface

### Objective
Verify the non-reachability of IP address set on loopback interface

### Requirements
The requirements for this test case are:
 - openswitch
 - host

### Setup
Connect openswitch interface 1 to eth0 on host

#### Topology diagram
#### Test setup
### Description
Assign ip 192.168.1.2/24 to eth0 on host
Create loopback interface 1
Assign ip 192.168.1.1/24 to loopback interface 1
Ping 192.168.1.1 from host
Remove loopback interface 1
Ping 192.168.1.1 from host

### Test result criteria
Ping result

#### Test pass criteria
Ping fails

#### Test fail criteria
Ping succeeds

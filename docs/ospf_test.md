#OSPF test cases

## Contents

- [OSPF router id](#test-cases-to-verify-ospf-router-id-related-configurations)
- [OSPF adjacencies](#test-cases-to-verify-ospf-adjacencies)
- [OSPF DR/BDR election](#test-cases-to-verify-ospf-election-process)
- [OSPF learning and advertising of routes](#test-cases-to-verify-ospf-learning-and-advertising-of-routes)
- [OSPF passive interface](#test-cases-to-verify-ospf-passive-interface)
- [OSPF ABR and inter-area](#test-cases-to-verify-ospf-inter-area-and-abr)
- [OSPF authentication](#test-cases-to-verify-ospf-authentication)
- [OSPF area as NSSA](#test-cases-to-verify-area-as-nssa)
- [OSPF area as stubby](#test-cases-to-verify-area-as-stubby)
- [OSPF stub router advertisement](#test-cases-to-verify-stub-router-advertisement)
- [OSPF virtual links](#test-cases-to-verify-virtual-links)
- [OSPF SPF throttling](#test-cases-to-verify-spf-throttling)
- [OSPF filter-list](#test-cases-to-verify-ospf-area-network-filtering)
- [OSPF Opaque LSA](#test-cases-to-verify-opaque-capability)
- [OSPF Zebra best route](#test-cases-to-verify-best-route-selection-by-zebra)


## Test cases to verify OSPF router id related configurations ##
### Objective ###
Verify the global and router level router id configurations.

### Requirements ###
The requirements for this test case are:
 - 2 switches

### Setup ###

#### Topology Diagram ####

```ditaa

 +------------+           +--------------+
 |            |           |              |
 |  Switch 1 1+-----------+1  Switch 2   |
 |            |           |              |
 +------------+           +--------------+
```
### Test case 1.01 : Verifying that the dynamic router id is selected
### Precondition ###
 - The global router id and router context router id are not configured.

### Description ###
When the hello packets are sent out, the router id should be selected from the zebra.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the hello packet had the router id that was allocated dynamically (by zebra).
#### Test Fail Criteria ####
The test case is a failure if the hello packet does not have the router id.

### Test case 1.02 : Verifying that the globally configured router id is selected
### Precondition ###
 - The global router id and router context router id are not configured.

### Description ###
Configure the global router id using the command `router-id <A.B.C.D>` in config context. The hello packets will not contain the router id that was configured in config context. Since changing the router id often is disruptive, quagga uses the router id that is already present.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the hello packet does not have the router id that was configured in config context but has the router id previously assigned by quagga.
#### Test Fail Criteria ####
The test case is a failure if the hello packet does not contain the router id that was configured in config context.

### Test case 1.03 : Verifying that the dynamic router id is selected when global router id is removed
### Precondition ###
 - The global router id is configured and
 - router context router id is not configured.

### Description ###
Remove the global router id using the command `no router-id` in config context. The hello packets should not contain the router id that was previously configured in config context but should contain the router id that was dynamically allocated by zebra.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the hello packet had the router id that was dynamically allocated.
#### Test Fail Criteria ####
The test case is a failure if the hello packet does not have the router id or contain the router id that was configured in config context.

### Test case 1.04 : Verifying that the router id configured in router context is selected
### Precondition ###
 - The global router id is not configured and
 - router context router id is not configured.

### Description ###
Configure the instance level router id using the command `router-id <A.B.C.D>` in router context. The hello packets should contain the router id that was configured in router context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the hello packet had the router id that was configured in router context.
#### Test Fail Criteria ####
The test case is a failure if the hello packet does not have the router id or does not contain the router id that was configured in router context.

### Test case 1.05 : Verifying that the dynamic router id is selected when instance level router id is removed
### Precondition ###
 - The global router id is not configured and
 - router context router id is configured.

### Description ###
Remove the instance level router id using the command `no router-id` in router context. The hello packets should not contain the router id that was previously configured in router context but should contain the router id that was dynamically allocated by zebra.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the hello packet had the router id that was dynamically allocated.
#### Test Fail Criteria ####
The test case is a failure if the hello packet does not have the router id or contain the router id that was configured in router context.

### Test case 1.06 : Verifying that the globally configured router id is selected when instance level router id is removed
### Precondition ###
 - The global router id is configured and
 - router context router id is configured.

### Description ###
Remove the instance level router id using the command `no router-id` in router context. The hello packets should not contain the router id that was previously configured in config context but should contain the router id that was dynamically allocated by zebra.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the hello packet had the router id that was configured in config context.
#### Test Fail Criteria ####
The test case is a failure if the hello packet does not have the router id configured in config context or contain the router id that was configured in router context.

## Test cases to verify ospf adjacencies ##
### Objective ###
Verify the OSPF adjacency related functionality.
### Requirements ###
The requirements for this test case are:
 - 4 switches in vlan 100

### Setup ###

#### Topology Diagram ####

```ditaa
+---------------+             +---------------+          +---------------+         +---------------+
|               |             |               |          |               |         |               |
| Switch 1     1+-------------+1  Switch 2   2+----------+2  Switch 3   1+---------+1   Switch 4   |
|               |             |               |          |               |         |               |
|               |             |               |          |               |         |               |
+---------------+             +---------------+          +---------------+         +---------------+
```

### Test case 2.01 : Test case to verify that the neighbors are discovered
### Precondition ###
 None

### Description ###
The hello packets should be exchanged between the adjacent switches. The "if_statistics" column in  `ovs-vsctl list OSPF_Interface` command output will give the number of hellos sent and received. Also neighbors should be present in the neighbor table. This can be verified using the command `show ip ospf neighbor detail`.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the hello packets - sent and received counters are non zero and `show ip ospf neighbor detail` displays the neighbors.
#### Test Fail Criteria ####
The test case is a failure if the hello packet counters are zero or `show ip ospf neighbor detail` does not display the neighbors.

### Test case 2.02 : Test case to verify that the hello packets are exchanged periodically
### Precondition ###
 - Neighbors are already discovered and adjacency is formed.

### Description ###
The command `show ip ospf interface` will display the hello interval. The hello packets should be exchanged between the adjacent switches for every hello interval. The "if_statistics" column in  `ovs-vsctl list OSPF_Interface` command output will give the number of hellos sent and received. This counter should be incremented for every hello interval.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the hello packets - sent and received counters are non zero and incrementing every hello interval.
#### Test Fail Criteria ####
The test case is a failure if the hello packet counters are zero or is not incrementing every hello interval.

### Test case 2.03 : Test case to verify that neighbor information is updated when ospf is disabled in one of the switches
### Precondition ###
 - Neighbors are already discovered and adjacency is formed.

### Description ###
The command `show ip ospf neighbor detail` will display the neighbor details. When ospf is disabled in switch 2 using the command `no router ospf` in config context, the adjacency between switch 1 and switch 2 and switch 2 and switch 3 should be torn down. This can be verified using the command `show ip ospf neighbor` in switch 1 and switch 2.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the neighbor entry of switch 2 is removed in switch 1 and switch 3.
#### Test Fail Criteria ####
The test case is a failure if the neighbor entry of switch 2 is not removed in switch 1 and switch 3.

### Test case 2.04 : Test case to verify that neighbor information is updated when one of the neighbor goes down
### Precondition ###
 - Neighbors are already discovered and adjacency is formed.

### Description ###
The command `show ip ospf neighbor detail` will display the neighbor details. When switch 2 is rebooted, the adjacency between switch 1 and switch 2 and switch 2 and switch 3 should be torn down. This can be verified using the command `show ip ospf neighbor` in switch 1 and switch 2.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the neighbor entry of switch 2 is removed in switch 1 and switch 3.
#### Test Fail Criteria ####
The test case is a failure if the neighbor entry of switch 2 is not removed in switch 1 and switch 3.

### Test case 2.05 : Test case to verify that neighbor information is updated when dead timer is changed
### Precondition ###
 - Neighbors are already discovered and adjacency is formed.

### Description ###
The command `show ip ospf neighbor detail` will display the neighbor details. Modify the dead timer in switch 2 using the command `ip ospf dead-interval <dead_interval>` in the interface context. The adjacency between switch 1 and switch 2 and switch 2 and switch 3 should be torn down. This can be verified using the command `show ip ospf neighbor` in switch 1 and switch 2.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the neighbor entry of switch 2 is removed in switch 1 and switch 3.
#### Test Fail Criteria ####
The test case is a failure if the neighbor entry of switch 2 is not removed in switch 1 and switch 3.

### Test case 2.06 : Test case to verify that neighbor information is updated when hello timer is changed
### Precondition ###
 - Neighbors are already discovered and adjacency is formed.

### Description ###
The command `show ip ospf neighbor detail` will display the neighbor details. Modify the hello timer in switch 2 using the command `ip ospf hello-interval <hello_interval>` in the interface context. The adjacency between switch 1 and switch 2 and switch 2 and switch 3 should be torn down. This can be verified using the command `show ip ospf neighbor` in switch 1 and switch 2.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the neighbor entry of switch 2 is removed in switch 1 and switch 3.
#### Test Fail Criteria ####
The test case is a failure if the neighbor entry of switch 2 is not removed in switch 1 and switch 3.

### Test case 2.07 : Test case to verify that neighbor information is updated when MTU mismatches
### Precondition ###
 - Neighbors are already discovered and adjacency is formed.

### Description ###
The command `show ip ospf neighbor detail` will display the neighbor details. Modify the mtu value in switch 2 using the command `mtu <mtu-value>` in the interface context. The adjacency between switch 1 and switch 2 and switch 2 and switch 3 should be torn down. This can be verified using the command `show ip ospf neighbor` in switch 1 and switch 2.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the neighbor entry of switch 2 is removed in switch 1 and switch 3.
#### Test Fail Criteria ####
The test case is a failure if the neighbor entry of switch 2 is not removed in switch 1 and switch 3.

### Test case 2.08 : Test case to verify that neighbor information is not updated when MTU mismatches and MTU ignore flag is set
### Precondition ###
 - Neighbors are already discovered and adjacency is formed.
 - Switch 2 is not present in the neighbor table in switch 1 and switch 3
 - MTU in switch 2 mismatch the one in switch 1 and switch 3

### Description ###
The command `show ip ospf neighbor detail` will display the neighbor details. Set the MTU ignore flag to true using the command `ip ospf mtu-ignore`. The adjacency between switch 1 and switch 2 and switch 2 and switch 3 should be formed. This can be verified using the command `show ip ospf neighbor` in switch 1 and switch 2.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the neighbor entry of switch 2 is present in switch 1 and switch 3.
#### Test Fail Criteria ####
The test case is a failure if the neighbor entry of switch 2 is not present in switch 1 and switch 3.

### Test case 2.09 : Test case to verify that neighbor adjacencies are formed when NBMA neighbors are configured
### Precondition ###
 None

### Description ###
Configure the NBMA neighbors in switch 1 and switch 2 using the command `neighbor <neighbor_ip> {poll-interval <poll_value> | priority <priority_value>}` in router context. The command `show ip ospf neighbor detail` will display the neighbor details. The adjacency between switch 1 and switch 2 should be formed. This can be verified using the command `show ip ospf neighbor` in switch 1 and switch 2.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the neighbor entry of switch 2 is present in switch 1 and viceversa.
#### Test Fail Criteria ####
The test case is a failure if the neighbor entry of switch 2 is not present in switch 1 and viceversa.

### Test case 2.10 : Test case to verify that neighbor adjacencies are formed when link is point to point
### Precondition ###
 None

### Description ###
Configure the link between switch 1 and switch 2 as point to point using the command `ip ospf network (broadcast|point-to-point)` in interface context. The command `show ip ospf neighbor detail` will display the neighbor details. The adjacency between switch 1 and switch 2 should be formed. This can be verified using the command `show ip ospf neighbor` in switch 1 and switch 2.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the neighbor entry of switch 2 is present in switch 1 and viceversa.
#### Test Fail Criteria ####
The test case is a failure if the neighbor entry of switch 2 is not present in switch 1 and viceversa.


## Test cases to verify ospf election process ##
### Objective ###
Verify the OSPF election process.
### Requirements ###
The requirements for this test case are:
 - 3 switches in vlan 100

### Setup ###

#### Topology Diagram ####

```ditaa
+---------------+             +---------------+          +---------------+
|               |             |               |          |               |
| Switch 1     1+-------------+1  Switch 2   2+----------+2  Switch 3    |
|               |             |               |          |               |
|               |             |               |          |               |
+---------------+             +---------------+          +---------------+
```

### Test case 3.01 : Test case to verify that the DR and BDR is selected
### Precondition ###
  None

### Description ###
Configure the priority of switch 1 and switch 2 using the command `ip ospf priority <priority_value>` in interface context. The priority value is set such that switch 2 has the higher priority. switch 3 has the default priority.
The `show ip ospf interface` command is used to display the DR, BDR and priority information.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the switch 2 is selected as DR, switch 1 is BDR and switch 3 is other-DR.
#### Test Fail Criteria ####
The test case is a failure if the switch 2 is not selected as DR, switch 1 is not BDR or switch 3 is not other-DR.

### Test case 3.02 : Test case to verify that the BDR is selected as DR when DR goes down
### Precondition ###
 - Switch 1 is DR
 - Switch 2 is BDR

### Description ###
Reboot the switch 1. The switch 2 should become DR now. The `show ip ospf interface` command is used to display the DR, BDR and priority information.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the switch 2 is selected as DR.
#### Test Fail Criteria ####
The test case is a failure if the switch 2 is not selected as DR.

### Test case 3.03 : Test case to verify that the BDR is selected as DR when DR goes down
### Precondition ###
 - Switch 1 is DR
 - Switch 2 is BDR

### Description ###
Configure the priority of switch 3 using the command `ip ospf priority <priority_value>` in interface context. The priority value is set such that switch 3 has the higher priority than switch 2.  The `show ip ospf interface` command is used to display the DR, BDR and priority information.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if the switch 1 is selected as DR and switch 3 is BDR.
#### Test Fail Criteria ####
The test case is a failure if the switch 1 is not selected as DR or switch 3 is not BDR.

## Test cases to verify ospf learning and advertising of routes ##
### Objective ###
Verify the OSPF learning and advertising of routes learned.

### Requirements ###
The requirements for this test case are:
 - 3 switches

### Setup ###

#### Topology Diagram ####

```ditaa
+---------------+             +---------------+          +---------------+
|               |             |               |          |               |
| Switch 1     1+-------------+1  Switch 2   2+----------+2  Switch 3    |
|               |             |               |          |               |
|               |             |               |          |               |
+---------------+             +---------------+          +---------------+
```

### Test case 4.01 : Test case to verify redistribution of static routes
### Precondition ###
 - Neighbors have been discovered and adjacency is formed

### Description ###
Configure the static routes in switch 2 using the command `ip route A.B.C.D/M (<nexthop-ip> | <interface>) {distance}` in config context. Redistribute the routes to the neighbors using the command `redistribute static` in router context.
The `show rib` command in switch 1 is used to the routes that were distributed.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show rib` command in switch 1 contains the routes distributed by switch 2.
#### Test Fail Criteria ####
The test case is a failure if `show rib` command in switch 1 does not contain the routes distributed by switch 2.

### Test case 4.02 : Test case to verify redistribution of connected routes
### Precondition ###
 - Neighbors have been discovered and adjacency is formed

### Description ###
Configure interfaces in switch 2. Redistribute the routes to the neighbors using the command `redistribute connected` in router context.
The `show rib` command in switch 1 is used to the routes that were distributed.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show rib` command in switch 1 contains the routes distributed by switch 2.
#### Test Fail Criteria ####
The test case is a failure if `show rib` command in switch 1 does not contain the routes distributed by switch 2.

### Test case 4.03 : Test case to verify redistribution of bgp routes
### Precondition ###
 - Neighbors have been discovered and adjacency is formed

### Description ###
Enable bgp in switch 2. Redistribute the routes to the neighbors using the command `redistribute bgp` in router context.
The `show rib` command in switch 1 is used to the routes that were distributed.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show rib` command in switch 1 contains the routes distributed by switch 2.
#### Test Fail Criteria ####
The test case is a failure if `show rib` command in switch 1 does not contain the routes distributed by switch 2.

## Test cases to verify ospf passive interface ##
### Objective ###
Verify the OSPF passive interface behaviour.

### Requirements ###
The requirements for this test case are:
 - 3 switches

### Setup ###

#### Topology Diagram ####

```ditaa
+---------------+             +---------------+          +---------------+
|               |             |               |          |               |
| Switch 1     1+-------------+1  Switch 2   2+----------+2  Switch 3    |
|               |             |               |          |               |
|               |             |               |          |               |
+---------------+             +---------------+          +---------------+
```

### Test case 5.01 : Test case to verify passive interface behaviour
### Precondition ###
 - Neighbors have been discovered and adjacency is formed

### Description ###
Configure the interface 2 of switch 2 as passive interface using the command `passive-interface <interface>` in router context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 2 does not display switch 3.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 2 displays switch 3.

### Test case 5.02 : Test case to verify adjacency is restored when passive interface is disabled
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - Interface 2 of switch 2 is set as passive interface

### Description ###
Unconfigure the interface 2 of switch 2 from passive interface using the command `no passive-interface <interface>` in router context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 2 displays switch 3.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 2 does not display switch 3.

### Test case 5.03 : Test case to verify behaviour when passive interface default is set
### Precondition ###
 - Neighbors have been discovered and adjacency is formed

### Description ###
Configure all interfaces of switch 2 as passive using the command `passive-interface default` in router context.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 3 does not display switch 2.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 3 displays switch 2.

## Test cases to verify ospf inter area and ABR ##
### Objective ###
Verify the OSPF inter-area and ABR functionality.

### Requirements ###
The requirements for this test case are:
 - 4 switches

### Setup ###

#### Topology Diagram ####

```ditaa
+---------------+             +---------------+          +---------------+         +---------------+
|               |             |               |          |               |         |               |
| Switch 1     1+-------------+1  Switch 2   2+----------+2  Switch 3   1+---------+1   Switch 4   |
|               |             |               |          |               |         |               |
|               |             |               |          |               |         |               |
+---------------+             +---------------+          +---------------+         +---------------+
```

### Test case 6.01 : Test case to verify ABR
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - Switch 1 has connected routes

### Description ###
Configure the interface 1 of switch 1 and interface 1 of switch 2 in Area 100, interface 2 of switch 3 and interface 2 of switch 2 in Area 0 and interface 1 of switch 3 and interface 1 of switch 4 in Area 200 using the command `network <A.B.C.D/M> area <area-id>` in router context. The Switch 2 and switch 3 will act as ABR.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show rib` in switch 2 and switch 4 displays connected routes in switch 1.
#### Test Fail Criteria ####
The test case is a failure if `show rib` in switch 2 and switch 4 does not display connected routes in switch 1.

### Test case 6.02 : Test case to verify learnt routes are removed in inter-area, when switch in another area goes down
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - Switch 1 has connected routes

### Description ###
Configure the interface 1 of switch 1 and interface 1 of switch 2 in Area 100, interface 2 of switch 3 and interface 2 of switch 2 in Area 0 and interface 1 of switch 3 and interface 1 of switch 4 in Area 200 using the command `network <A.B.C.D/M> area <area-id>` in router context. The Switch 2 and switch 3 will act as ABR. Reboot the switch 1.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show rib` in switch 2 and switch 4 does not display connected routes in switch 1.
#### Test Fail Criteria ####
The test case is a failure if `show rib` in switch 2 and switch 4 displays connected routes in switch 1.

### Test case 6.03 : Test case to verify ABR learns and distributes connected routes
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - Switch 1 has connected routes

### Description ###
Configure the interface 1 of switch 1 and interface 1 of switch 2 in Area 100, interface 2 of switch 3 and interface 2 of switch 2 in Area 0 and interface 1 of switch 3 and interface 1 of switch 4 in Area 200 using the command `network <A.B.C.D/M> area <area-id>` in router context. The Switch 2 and switch 3 will act as ABR.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show rib` in switch 2 and switch 4 displays connected routes in switch 1.
#### Test Fail Criteria ####
The test case is a failure if `show rib` in switch 2 and switch 4 does not display connected routes in switch 1.

### Test case 6.04 : Test case to verify ABR distributes summarized routes
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - Switch 1 has connected routes 10.10.10.1/24 and 10.10.20.1/24

### Description ###
Configure the interface 1 of switch 1 and interface 1 of switch 2 in Area 100, interface 2 of switch 3 and interface 2 of switch 2 in Area 0 and interface 1 of switch 3 and interface 1 of switch 4 in Area 200 using the command `network <A.B.C.D/M> area <area-id>` in router context. The Switch 2 and switch 3 will act as ABR.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show rib` in switch 2 and switch 4 displays connected routes in switch 1 summarized as 10.10.0.0/16.
#### Test Fail Criteria ####
The test case is a failure if `show rib` in switch 2 and switch 4 does not display connected routes in switch 1 summarized as 10.10.0.0/16.

## Test cases to verify ospf authentication ##
### Objective ###
Verify the OSPF authentication related configuration in router and interface context.

### Requirements ###
The requirements for this test case are:
 - 3 switches

### Setup ###

#### Topology Diagram ####

```ditaa
+---------------+             +---------------+          +---------------+
|               |             |               |          |               |
| Switch 1     1+-------------+1  Switch 2   2+----------+2  Switch 3    |
|               |             |               |          |               |
|               |             |               |          |               |
+---------------+             +---------------+          +---------------+
```

### Test case 7.01 : Test case to verify md5 authentication in interface context - adjacency torn
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - No authentication is configured

### Description ###
Configure the md5 authentication in interface 2 of switch 2 using the command `ip ospf authentication {message-digest}` and `ip ospf authentication-key <key>` in interface context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 2 does not display switch 3.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 2 displays switch 3.

### Test case 7.02 : Test case to verify md5 authentication in interface context - adjacency restored
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - Authentication is configured in switch 2 only

### Description ###
Configure the md5 authentication in interface 2 of switch 3 using the command `ip ospf authentication {message-digest}` and `ip ospf authentication-key <key>` in interface context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 2 displays switch 3.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 2 does not display switch 3.

### Test case 7.03 : Test case to verify text authentication in interface context - adjacency torn
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - No authentication is configured

### Description ###
Configure the text based authentication in interface 2 of switch 2 using the command `ip ospf authentication` in interface context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 2 does not display switch 3.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 2 displays switch 3.

### Test case 7.04 : Test case to verify text authentication in interface context - adjacency restored
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - Text based authentication is configured in switch 2 only

### Description ###
Configure the text based authentication in interface 2 of switch 3 using the command `ip ospf authentication` in interface context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 2 displays switch 3.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 2 does not display switch 3.

### Test case 7.05 : Test case to verify md5 authentication in router context - adjacency torn
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - No authentication is configured

### Description ###
Configure the md5 authentication in switch 2 using the command `area  (<area_ip>|<area_id>) authentication [message-digest]` in router context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 2 does not display switch 3 and switch 1.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 2 displays switch 3 or switch 1.

### Test case 7.06 : Test case to verify md5 authentication in interface context - adjacency restored
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - Authentication is configured in switch 2 only

### Description ###
Configure the md5 authentication in switch 3 using the command `area  (<area_ip>|<area_id>) authentication [message-digest]` in router context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 2 displays switch 3 and switch 1.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 2 does not display switch 3 or switch 1.

### Test case 7.07 : Test case to verify text based authentication in router context - adjacency torn
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - No authentication is configured

### Description ###
Configure the text based authentication in switch 2 using the command `area  (<area_ip>|<area_id>) authentication` in router context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 2 does not display switch 3 and switch 1.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 2 displays switch 3 or switch 1.

### Test case 7.08 : Test case to verify text based authentication in interface context - adjacency restored
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - Authentication is configured in switch 2 only

### Description ###
Configure the text based authentication in switch 3 using the command `area  (<area_ip>|<area_id>) authentication` in router context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 2 displays switch 3 and switch 1.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 2 does not display switch 3 or switch 1.

### Test case 7.09 : Test case to verify md5 authentication configured both in interface context and router context - adjacency torn
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - No authentication is configured

### Description ###
Configure the md5 authentication in interface 2 of switch 2 using the command `ip ospf authentication {message-digest}` and `ip ospf authentication-key <key>` in interface context and configure the md5 authentication in switch 2 using the command `area  (<area_ip>|<area_id>) authentication [message-digest]` in router context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 2 does not display switch 3.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 2 displays switch 3.

### Test case 7.10 : Test case to verify md5 authentication configured both in interface context and router context - adjacency restored
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - Authentication is configured in switch 2 only

### Description ###
Configure the md5 authentication in switch 3 using the command `ip ospf authentication {message-digest}` and `ip ospf authentication-key <key>` in interface context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 2 displays switch 3 and switch 1, though the router context authentication is not configured.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 2 does not display switch 3 or switch 1.

### Test case 7.11 : Test case to verify text based authentication configured both in interface context and router context - adjacency torn
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - No authentication is configured

### Description ###
Configure the text based authentication in interface 2 of switch 2 using the command `ip ospf authentication` in interface context and configure the text based authentication in switch 2 using the command `area  (<area_ip>|<area_id>) authentication` in router context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 2 does not display switch 3.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 2 displays switch 3.

### Test case 7.12 : Test case to verify text based authentication configured both in interface context and router context - adjacency restored
### Precondition ###
 - Neighbors have been discovered and adjacency is formed
 - Authentication is configured in switch 2 only

### Description ###
Configure the text based authentication in switch 3 using the command `ip ospf authentication` in interface context.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is successful if `show ip ospf neighbor` in switch 2 displays switch 3 and switch 1, though the router context authentication is not configured.
#### Test Fail Criteria ####
The test case is a failure if `show ip ospf neighbor` in switch 2 does not display switch 3 or switch 1.

##  Test cases to verify area as NSSA
### Objective ###
Verify NSSA (Not so stubby area) area configuration on ABR/ASBR. A not-so-stubby area (NSSA) is a type of stub area that can import autonomous system external routes and send them to other areas, but still cannot receive AS-external routes from other areas. NSSA is an extension of the stub area feature that allows the injection of external routes in a limited fashion into the stub area. A case study simulates an NSSA getting around the Stub Area problem of not being able to import external addresses. It visualizes the following activities: the ASBR imports external addresses with a type 7 LSA, the ABR converts a type 7 LSA to type 5 and floods it to other areas, the ABR acts as an "ASBR" for other areas.
### Requirements ###
The requirements for this test case are:
 - 1 DUT, 2 switches

### Setup ###

#### Topology Diagram ####
Area 1 (DUT [ABR], Switch 1)
Area 0 (Switch 2[ASBR])
```ditaa
                +------------------------------+
                |                              |
                |              DUT             |
                |         (OpenSwitch)         |
                |                              |
                +------------------------------+
                       1                2
                       |                |
                       |                |
                       3                4
                 +-----------+    +-----------+
                 |           |    |           |
                 | Switch 1  |    |  Switch 2 |
                 |           |    |           |
                 +-----------+    +-----------+
```
### Test case 8.01 : Verify area as NSSA
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.

### Description ###
Configure area as NSSA, by executing these commands on DUT and Switch-1 of area 1.
```
switch# configure terminal
switch# router ospf
switch(config-router)# area 1 nssa
```
### Test Result Criteria ###
#### Test Pass Criteria ####
- Configuring area as NSSA, must have following characteristics:-
    1. No Type 5 LSAs are allowed in Area 1.
    2. All external routes are inject to Area 1 as type 7 LSA.
    3. All type 7 LSAs are translated into type 5 LSAs by the NSSA ABR (DUT) and are flooded into the OSPF domain as type 5 LSAs.
- Configuring area as NSSA (Totally stubby), must have following characteristics:-
    1. No type 3 or 4 summary LSAs are allowed in Area 1. This means no inter-area routes are allowed in Area 1.
    2. Type 3 LSA in injected into Area 1 as default route.
- Ping is working on all routes.

#### Test Fail Criteria ####
- The test case is a failure if following occurs:-
    1. Type 5 LSAs are allowed in Area 1.
    2. All external routes are not inject to Area 1 as type 7 LSA.
    3. All type 7 LSAs are not translated into type 5 LSAs by the NSSA ABR (DUT).

### Test case 8.02 : Verify area as NSSA (Totally stubby)
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.

### Description ###
Configure area as NSSA (totally stubby), by executing these commands on DUT (ABR).
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 nssa no-summary
```
### Test Result Criteria ###
#### Test Pass Criteria ####
- Configuring area as NSSA (totally stubby), must have following characteristics:-
    1. No type 3 or 4 summary LSAs are allowed in Area 1. This means no inter-area routes are allowed in Area 1.
    2. Type 3 LSA in injected into Area 1 as default route.
- Ping is working on all routes.

#### Test Fail Criteria ####
- The test case is a failure if following occurs:-
    1. Inter-area routes are allowed in area 1.
    2. ping doesn't work.

## Test cases to verify area as Stubby
### Objective ###
To verify that OSPF non-backbone area can be configured as stub. Stub networks have only a single attached router.Packets on a stub network always have either a source or a destination address belonging to that network. That is, all packets were either originated by a device on the network or are destined for a device on the network. OSPF advertises host routes (routes with a mask of 255.255.255.255) as stub networks. Loopback interfaces are also considered stub networks and are advertised as host routes. An ASBR learning external destinations will advertise those destinations by flooding AS External LSAs throughout the OSPF autonomous system. In many cases, these External LSAs may make up a large percentage of the LSAs in the databases of every router. As in any area, all routers in a stub area must have identical link state databases. To ensure this condition, all stub routers will set a flag (the E-bit) in their Hello packets to zero; they will not accept any Hello from a router in which the E-bit is set to one. As a result, adjacencies will not be established with any router that is not configured as a stub router.
### Requirements ###
The requirements for this test case are:
 - 1 DUT, 2 switches

### Setup ###
#### Topology Diagram ####
Area 1 (DUT [ABR], Switch 1)
Area 0 (Switch 2[ASBR])
```ditaa
                +------------------------------+
                |                              |
                |              DUT             |
                |         (OpenSwitch)         |
                |                              |
                +------------------------------+
                       1                2
                       |                |
                       |                |
                       3                4
                 +-----------+    +-----------+
                 |           |    |           |
                 | Switch 1  |    |  Switch 2 |
                 |           |    |           |
                 +-----------+    +-----------+
```
### Test case 9.01 : Verify area as stubby
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.

### Description ###
Configure area as stub, by executing these commands on DUT and Switch-1 of area 1.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 stub
```
### Test Result Criteria ###
#### Test Pass Criteria ####
- Configuring area as stub, must have following characteristics:-
    1. All external routes must be replaced with default route.
    2. Adjacency between a router in stubby area and router in non-stubby area is not possible.
    3. The Hello packets from STUB network captured on packet capture must have E-Bit set on Flag.

#### Test Fail Criteria ####
- The test case is a failure if following occurs:-
    1. External routes are not replaced as default route.
    2. Hello packets from STUB network have no E bit set.

### Test case 9.02 : Verify area as Totally stubby
#### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.

### Description ###
Configure area as Totally stubby, by executing these commands on DUT (ABR).
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 stub no-summary
```
### Test Result Criteria ###
#### Test Pass Criteria ####
- Configuring area as totally stubby, must have following characteristics:-
    1. All external and inter-area routes must be replaced with default route.
    2. Adjacency between a router in stubby area and router in non-stubby area is not possible.
    3. The Hello packets from STUB network captured on packet capture must have E-Bit set on Flag.

#### Test Fail Criteria ####
- The test case is a failure if following occurs:-
    1. External and inter-area routes are not replaced as default route.
    2. If adjacency between routers in  stubby and non-stubby area is possible.

## Test cases to verify stub router advertisement
### Objective ###
To verify the stub router advertisement, i.e. maximizing the cost metric of the DUT links. Stub routers does not forwards traffic that is not destined for networks directly connected to it. The router becomes a stub router by maximizing the cost metric for the connected links.
### Requirements ###
The requirements for this test case are:
 - 1 DUT, 2 switches

### Setup ###
#### Topology Diagram ####
Area 1 (DUT, Switch 1, Switch 2)
```ditaa
                +------------------------------+
                |                              |
                |              DUT             |
                |         (OpenSwitch)         |
                |                              |
                +------------------------------+
                       1                2
                       |                |
                       |                |
                       3                4
                 +-----------+    +-----------+
                 |           |    |           |
                 | Switch 1  |    |  Switch 2 |
                 |           |    |           |
                 +-----------+    +-----------+
```
### Test case 10.01 : Verify DUT as stub router
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- There should be atleast one network segment not directly connected to DUT.

### Description ###
Configure DUT as stub router
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# max-metric router-lsa
```
### Test Result Criteria ###
#### Test Pass Criteria ####
- For routes to network segment not directly connected to DUT, DUT is not listed as next hop for Switch-1. Verified using `show ip route` command output.

#### Test Fail Criteria ####
- Test case is a failure if, for routes to network segment not directly connected to DUT, DUT is listed as next hop for Switch-1. Verified using `show ip route` command output.

### Test case 10.02 : Verify DUT as stub router on startup
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- There should be atleast one network segment not directly connected to DUT.

### Description ###
Configure router as stub router on start-up
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# max-metric router-lsa on-startup 3000
```
### Test Result Criteria ###
#### Test Pass Criteria ####
- For routes to network segment not directly connected to DUT, DUT is removed as next hop for Switch-1 after 3000 seconds of DUT start up. Verified using `show ip route` command output.

#### Test Fail Criteria ####
- Test case is a failure if, for routes to network segment not directly connected to DUT, DUT is not removed as next hop for Switch-1 after 3000 seconds of DUT start up. Verified using `show ip route` command output.

##  Test cases to verify virtual links
### Objective ###
To verify that on configuring Virtual link at one end, the status of virtual-neighbor will be shown as down. To verify that Virtual link functionality. All areas in an Open Shortest Path First (OSPF) autonomous system must be physically connected to the backbone area (Area 0), in some cases it is not possible. There virtual link(s) are used to connect to the backbone through a non-backbone area. Virtual links can also be used to connect two parts of a partitioned backbone through a non-backbone area.
### Requirements ###
The requirements for this test case are:
 - 1 DUT, 3 switches
 - tcpdump tool or packet sniffers.

### Setup ###
#### Topology Diagram ####
Area 1 (Switch 1, DUT [ABR])
Area 0 (Switch 2, Switch 4)
VLINK (DUT <--> Switch 2)
```ditaa
         +------------------------------+            +----------------+
         |                              |            |                |
         |              DUT             |    VLINK   |     Switch 2   |
         |         (OpenSwitch)         +------------+                |
         |                              |            |                |
         +------------------------------+            +----------------+
                       1                                     2
                       |                                     |
                       |                                     |
                       3                                     4
                 +-----------+                       +----------------+
                 |           |                       |                |
                 | Switch 1  |                       |    Switch 4    |
                 |           |                       |                |
                 +-----------+                       +----------------+
```
### Test case 11.01 : Verify virtual link between DUT and remote ABR
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- The DUT shouldn't be part of backbone area.

### Description ###
Create a virtual link to remote ABR Switch-1 on DUT and vice-versa.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 virtual-link  100.0.1.1
```
### Test Result Criteria ###
#### Test Pass Criteria ####
- Before creating virtual links, DUT and switch-1 will not form adjacency.
- Configuring virtual link on DUT alone will not form adjacency, need to do the same on Switch-1.
- Hello packets must be send unicast in virtual links. Verify using packet capture tools.
- DUT and Switch-1 should form neighbor relation. Verify using `show ip ospf neighbor` command output.
- Switch-2 and Switch-3 should show DUT and Switch-1 routes and ping should work on all routes. Verify using `show ip ospf routes` command output.

#### Test Fail Criteria ####
- Test case will fail if there exist a adjacency between DUT and Switch-1 before creating virtual link.
- Test case will fail if adjacency is not established after creating virtual links on both switches.

### Test case 11.02 : Verify virtual link authentication
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- The DUT shouldn't be part of backbone area.
- Virtual link is created between DUT and switch-1.

### Description ###
Configure virtual link authentication.
```
switch# configure terminal
switch# router ospf
switch(config-router)# area 1 virtual-link  100.0.1.1 message-digest-key  1 md5 openswitch
switch(config-router)# area 1 virtual-link  100.0.1.1 authentication message-digest
```
### Test Result Criteria ###
#### Test Pass Criteria ####
- After configuring authentications the authentication field of OSPF packet header should show MD5 authentication. Verify using packet capture tools.

#### Test Fail Criteria ####
- Test case will fail in OSPF header in packet sent on virtual link doesn't have configured authentication field.

### Test case 11.03 : Verify hello-interval, retransmit-interval, transmit-delay and dead-interval for virtual links
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- The DUT shouldn't be part of backbone area.
- Virtual link is created between DUT and switch-1.

### Description ###
Configure hello-interval, retransmit-interval, transmit-delay and dead-interval for virtual links.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 virtual-link  100.0.1.1 hello-interval 30
switch(config-router)# area 1 virtual-link  100.0.1.1 retransmit-interval 30
switch(config-router)# area 1 virtual-link  100.0.1.1 transmit-delay 30
switch(config-router)# area 1 virtual-link  100.0.1.1 dead-interval 30
```
### Test Result Criteria ###
#### Test Pass Criteria ####
- Configure different hello and dead interval on DUT and remoter ABR, this will cause the hello packets to be dropped. Hello and dead intervals needs to be same for both DUT and peer ABR (Switch-1).

#### Test Fail Criteria ####
- Test case will fail if hello packets are sent and adjacency is formed even when different hello and dead intervals are set on DUT and switch-1.

### Test case 11.04 : Verify deleting virtual links
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- The DUT shouldn't be part of backbone area.
- Virtual link is created between DUT and switch-1.

### Description ###
Delete virtual links with remote ABR.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# no area 1 virtual-link  100.0.1.1
```
### Test Result Criteria ###
#### Test Pass Criteria ####
- Adjacency will cease after deleting virtual link between DUT and switch-1.

#### Test Fail Criteria ####
- Test case will fail if adjacency persists between DUT and Switch-1 even after deleting virtual link.

### Test case 11.05 : Verify virtual links on stubby and totally stubby area
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- The DUT shouldn't be part of backbone area.
- Virtual link is created between DUT and switch-1.

### Description ###
Configure virtual links on stubby and totally stubby area, it wouldn't work.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 stub
switch(config-router)# area 1 virtual-link  100.0.1.1
```
### Test Result Criteria ###
#### Test Pass Criteria ####
- Configuring virtual links on stubby and totally stubby area will throw error.

#### Test Fail Criteria ####
- Test case will fail if configuring virtual link on stubby and totally stubby area succeeds.

## Test cases to verify SPF throttling
### Objective ###
To verify the OSPFv2 SPF throttling. The OSPF Shortest Path First Throttling feature makes it possible to configure SPF scheduling in seconds interval and to potentially delay shortest path first (SPF) calculations during network instability. SPF is scheduled to calculate the Shortest Path Tree (SPT) when there is a change in topology. One SPF run may include multiple topology change events. The current SPF interval will be calculated and will be twice as long as the previous one until the this value reaches the maximum wait time specified.
### Requirements ###
The requirements for this test case are:
 - 1 DUT (ABR), 3 switches

### Setup ###
#### Topology Diagram ####
Area 0 (Switch 3, DUT)
Area 1 (Switch 2, DUT)
Area 2 (Switch 1, DUT)
```ditaa
  +----------+           +------------------------------+          +-------------+
  |          | 1       2 |                              |          |             |
  | Switch 3 +-----------+             DUT              |3        4|   Switch 2  |
  |          |           |         (OpenSwitch)         +----------+             |
  |          |           |                              |          |             |
  +----------+           +------------------------------+          +-------------+
                                       1
                                       |
                                       |
                                       3
                                 +-----------+
                                 |           |
                                 | Switch 1  |
                                 |           |
                                 +-----------+
```
### Test case 12.01 : Verify SPF throttling parameters
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- Adjacency should be established between routers and topology is stable unless changed manually.

### Description ###
Configure SPF throttling parameters
Set the spf throttling parameters as delay=100 milliseconds, initial hold time=100000 milliseconds and max hold time=300000 milliseconds, on DUT.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# timers throttle spf 100 100000 300000
```
Do a topology change manually like deleting a link of DUT for verifying the SPF timers effect.
### Test Result Criteria ###
#### Test Pass Criteria ####
- Verify that the SPF timers are set properly using `show ip ospf` command output.
- Verify that SPF is run at the interval of 100 secs. This can be verified in the logs. The Adjacency formed should remain intact, which can be verified using `show ip ospf neighbor` command output. Again the SPF is run at 200 secs (previous 100 sec x 2).

#### Test Fail Criteria ####
- Test cases will fail if SPF is not calculated within configured values.

## Test cases to verify OSPF area network filtering
### Objective ###
To verify the OSPF area network filtering. Filtering Type-3 summary-LSAs to/from area using prefix lists. These test cases makes sense in ABR only.
### Requirements ###
The requirements for this test case are:
 - 1 DUT (ABR), 2 switches

### Setup ###
#### Topology Diagram ####
Area 1 (Switch 1, DUT)
Area 0 (Switch 2, DUT)
```ditaa
                +------------------------------+
                |                              |
                |              DUT             |
                |         (OpenSwitch)         |
                |                              |
                +------------------------------+
                       1                2
                       |                |
                       |                |
                       3                4
                 +-----------+    +-----------+
                 |           |    |           |
                 | Switch 1  |    |  Switch 2 |
                 |           |    |           |
                 +-----------+    +-----------+
```
### Test case 13.01 : Verify filtering type-3 LSA into the area as per a preconfigured prefix list
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- Adjacency should be established between routers.
- Prefix filter list should be already configured for both ingress and egress.

### Description ###
Configure area to filter type-3 LSA into the area as per a preconfigured prefix list.
The filter list prefix (10.10.0.0/16) is already configure with list name *list1*. These commands will filter any type-3 LSA matching prefix 10.10.0.0/16 from entering the area 1, of which DUT is an ABR.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 filter-list list1 in
```
### Test Result Criteria ###
#### Test Pass Criteria ####
- Verify that the type-3 LSAs matching 10.10.0.0/16 prefix is filtered out from entering area 1 using `show ip ospf database` command output executed on Switch-1.

#### Test Fail Criteria ####
- Test case will fail in any LSA matching 10.10.0.0/16 prefix enters area 1.

### Test case 13.02 : Verify filtering type-3 LSA out of the area as per a preconfigured prefix list
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- Adjacency should be established between routers.
- Prefix filter list should be already configured for both ingress and egress.

### Description ###
Configure area to filter type-3 LSA out of the area as per a preconfigured prefix list.
The filter list prefix (100.10.0.0/16) is already configure with list name *list1*. These commands (executed on DUT) will filter any type-3 LSA matching prefix 100.10.0.0/16 from going out of the area 1, of which DUT is an ABR.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 filter-list list1 out
```
### Test Result Criteria ###
#### Test Pass Criteria ####
- Verify that the type-3 LSAs matching 100.10.0.0/16 prefix is filtered out from entering area 0 using `show ip ospf database` command output, executed on switch-2.

#### Test Fail Criteria ####
- Test case will fail if any type-3 LSA matching 100.10.0.0/16 prefix enters area 0.

## Test cases to verify Opaque capability
### Objective ###
To verify the sending and receiving Opaque LSAs between neighbors. Opaque LSAs are Type 9, 10 and 11 link-state advertisements. These advertisements may be used directly by OSPF or indirectly by some application wishing to distribute information throughout the OSPF domain. The function of the Opaque LSA option is to provide for future extensibility of OSPF.
- Link-state type 9 denotes a link-local scope. Type-9 Opaque LSAs are not flooded beyond the local (sub)network.
- Link-state type 10 denotes an area-local scope. Type-10 Opaque LSAs are not flooded beyond the borders of their associated area.
- Link-state type 11 denotes that the LSA is flooded throughout the Autonomous System (AS). The flooding scope of type-11 LSAs are equivalent to the flooding scope of AS-external (type-5) LSAs. Specifically type-11 Opaque LSAs are
   1. flooded throughout all transit areas.
   2. not flooded into stub areas from the backbone
   3. not originated by routers into their connected stub areas.
As with type-5 LSAs, if a type-11 Opaque LSA is received in a stub area from a neighboring router within the stub area the LSA is rejected.

### Requirements ###
The requirements for this test case are:
 - 1 DUT, 1 switches

### Setup ###
#### Topology Diagram ####
Area 1 (Switch 1, DUT)
Area 0 (Switch 2, DUT)
```ditaa
                +------------------------------+          +-------------+
                |                              |          |             |
                |              DUT             |          |  Switch 2   |
                |         (OpenSwitch)         |3--------4|             |
                |                              |          |             |
                +------------------------------+          +-------------+
                               1
                               |
                               |
                               2
                       +---------------+
                       |               |
                       |   Switch 1    |
                       |               |
                       +---------------+
```
### Test case 14.01 : Verify OSPF Opaque capability on DUT
#### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- Adjacency should be established between routers.

### Description ###
Configure OSPF Opaque capability on DUT, Switch-1 and Switch-2.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# capability opaque
```
### Test Result Criteria ###
#### Test Pass Criteria ####
- Verify that the Opaque-link (type 9) is received by using `show ip ospf database opaque-link` command output on DUT. Also the Number of Opaque LSA counter will be increased which can be verified using `show ip ospf` command output on DUT.
- Verify that the Opaque-area (type 10) is received by using `show ip ospf database opaque-area` command output on DUT. Also the Number of Opaque LSA counter will be increased which can be verified using `show ip ospf` command output on DUT.

#### Test Fail Criteria ####
- Test case will fail if no opaque LSA is received and installed on the DUT.

## Test cases to verify best route selection by zebra
### Objective ###
To verify that always the best route is selected for routing, when multiple protocols have routes to same network segment. When multiple protocol (including static routes) have routes to the same network segment, then zebra ensures that always the best route is selected depending on the distance cost. The lower the cost, more chance there is for the route to be selected.
### Requirements ###
The requirements for this test case are:
 - 1 DUT, 1 switches

### Setup ###
#### Topology Diagram ####
Area 1 (Switch 1, DUT)
```ditaa
                +------------------------------+
                |                              |
                |              DUT             |
                |         (OpenSwitch)         |
                |                              |
                +------------------------------+
                               1
                               |
                               |
                               2
                       +---------------+
                       |               |
                       |   Switch 1    |
                       |               |
                       +---------------+
```
### Test case 15.01 : Verify best route selection by zebra
#### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- Adjacency should be established between routers and Switch-1 should be configured for network 10.10.10.0/24.
- OSPF route for network 10.10.10.0/24 network is installed.

### Description ###
Configure OSPF distance and add static route for network 10.10.10.0/24 (executed on DUT).
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# distance 100
switch(config-router)# exit
switch(config)# ip route 10.10.10.0/24 1 90
switch(config)#
```
The static route is added for interface 1 on DUT with distance 90.
### Test Result Criteria ###
#### Test Pass Criteria ####
- Verify that the static route is selected for routing using `show rib` command output. Selected route for network 10.10.10.0/24 will the route entry prefixed with symbol `*` like below:-
```
10.10.10.0/24,  1 unicast next-hops
	*via  1,  [100/0],  connected
*10.10.10.0/24,  1 unicast next-hops
	*via  1,  [90/0],  static
```

#### Test Fail Criteria ####
- Test case will fail if OSPF route is selected instead of static route.

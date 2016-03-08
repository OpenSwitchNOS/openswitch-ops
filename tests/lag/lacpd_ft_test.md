# LACP Daemon Feature Test Cases

# Contents

## Transferring interface to another LAG with CLI
### Objective
Transferring an interface to another LAG without passing the interface on the
other side of the link cause the link to get in state Out of Sync and not
Collecting/Distributing using CLI interface for configuration
### Requirements
- Virtual Mininet Test Setup
- Script is in tests/test_ft_lacp_aggregation_key.py

### Setup
#### Topology Diagram
```
+--------+                  +--------+
|        1------------------2        |
|   s1   |                  |   s2   |
|        2------------------2        |
+--------+                  +--------+
```

### Test Setup
```
 Switch 1
   LAG 100:
       Interface 1
       Interface 2

 Switch 2
   LAG 100:
       Interface 1
       Interface 2
```

### Description
1. Turn on interfaces 1-4 in both switches
* Create LAG 100 in switch 1 with active state
* Create LAG 100 in switch 2 with active state
* Associate interfaces 1 and 2 to the LAG from both switches
* Wait switches to negotiate LAG state
* Request information from interface 1 in both switches with command
"show lacp interface"
* Validations on switch 1 in interface 1
  * Validate name, it should be lag100
  * Validate local key, it should be 100
  * Validate remote key, it should be 100
  * Validate local state, it should be In Sync and Collecting/Distributing
  * Validate remote state, it should be In Sync and Collecting/Distributing
* Validations on switch 2 in interface 1 for LAG 100:
  * Validate lag name, it should be lag100
  * Validate local key, it should be 100
  * Validate remote key, it should be 100
  * Validate local state, it should be In Sync and Collecting/Distributing
  * Validate remote state, it should be In Sync ad Collecting/Distributing
* Create LAG 200 in switch 1
* Associate interface 1 to lag 200
* Associate interface 3 to lag 200
* Associate interface 4 to lag 100, to keep lag 100 with two interfaces
* Wait switches to negotiate new LAG state
* Get LAG information for interface 1,2,3 and 4 in switch 1
* Get LAG information for interface 1 and 2 in Switch 2
* Validation on switch 1:
  * Validate lag name for interface 1 is lag200
  * Validate local key for interface 1 is 200
  * Validate remote key for interface 1 is 100
  * Validate lag state for interface 1 is Active, Long timeout, Aggregable and
  Out of Sync
  * Validate lag state for interface 2 is Sync and Collecting/Distributing
  * Validate lag state for interfaces 3 and 4 are in default
* Validation for switch 2:
  * Validate lag name is lag100
  * Validate local key for interface 1 is 100
  * Validate remote key for interface 1 is 200
  * Validate lag state is Out of Sync and not Collecting/Distributing for
  interface 1
  * Validate lag state for interface 2 is In Sync and Collecting/Distributing
* Clean configuration


### Test Result Criteria
#### Test Pass Criteria
All validations should be same as describe above
#### Test Fail Criteria
Assert for validation fails

## LACP aggregation key packet validation
### Objective
Capture LACPDUs packets and validate the aggregation key is set correctly for
both switches
### Requirements
- Virtual Mininet Test Setup
- Script is in tests/test_ft_lacp_aggregation_key.py

### Setup
#### Topology Diagram
```
+--------+                  +--------+
|        1------------------2        |
|   s1   |                  |   s2   |
|        2------------------2        |
+--------+                  +--------+
```
### Test Setup
```
 Switch 1
   LAG 100:
       Interface 1
       Interface 2

 Switch 2
   LAG 200:
       Interface 1
       Interface 2
```

### Description
1. Turn on interfaces 1 and 2 in both switches
* Create LAG 100 in switch 1
* Create LAG 200 in switch 2
* Associate interfaces 1 and 2 to lag in both switches
* Get mac address from switch 1 and 2
* Take capture from interface 1 in switch 1
* Get information from packet capture parse in a map with key-value
* Validate key sent from switch 1 to switch 2 is 100
* Validate key sent from switch 2 to switch 1 is 200
* Clean configuration

### Test Result Criteria
#### Test Pass Criteria
* Key sent from switch 1 to switch 2 should be 100
* Key sent from switch 2 to switch 1 should be 200
#### Test Fail Criteria
* Key sent from switch 1 to switch 2 is not 100
* Key sent from switch 2 to switch 1 is not 200

## LAG created with one LAG at the time, configured by CLI
### Objective
Verify only interfaces associated with the same
aggregation key get to Collecting/Distributing state
### Requirements
- Virtual Mininet Test Setup
- Script is in tests/test_ft_lacp_aggregation_key.py

### Setup
#### Topology Diagram
```
+------------+
|            |
|     s1     |
|            |
+-1--2--3--4-+
  |  |  |  |
  |  |  |  |
  |  |  |  |
  |  |  |  |
+-1--2--3--4-+
|            |
|     s2     |
|            |
+------------+
```

### Test Setup
```
Switch 1
    LAG150
      Interface 1
      Interface 2
      Interface 3
      Interface 4
Switch 2
    LAG150
      Interface 1
      Interface 2
    LAG400
      Interface 3
      Interface 4
```
### Description
1. Turn on interfaces 1-4 in switches 1 and 2
* Create LAG 150 in switch 1
* Create LAG 150 in switch 2
* Create LAG 400 in switch 2
* Associate interfaces 1-4 to LAG 150 in switch 1
* Associate interfaces 1 and 2 to LAG 150 in switch 2
* Associate interfaces 3 and 3 to LAG 400 in switch 2
* Wait for switches to negotiate LAG state
* Get information for interface 1-4 in switch 1 using CLI command
"show lacp interface"
* Get information for interface 1-4 in switch 2 using CLI command
"show lacp interface"
* Validations in switch 1
  * Validate interface 1 has state In Sync and Collecting/Distributing
  * Validate interface 2 has state In Sync and Collecting/Distributing
  * Validate interface 3 has state Out of Sync and not Collecting/Distributing
  * Validate interface 4 has state Out of Sync and not Collecting/Distributing
* Validations in switch 2
  * Validate interface 1 has state In Sync and Collecting/Distributing
  * Validate interface 2 has state In Sync and Collecting/Distributing
  * Validate interface 3 has state Out of Sync and not Collecting/Distributing
  * Validate interface 4 has state Out of Sync and not Collecting/Distributing
* Clean configuration
### Test Result Criteria
#### Test Pass Criteria
All validation should apply with the description above
#### Test Fail Criteria
If any validation fails to return the correct value

## LAG with cross links with same aggregation key using CLI
### Objective
Verify LAGs should be formed independent of port IDs as long
as aggregation key is the same, using CLI for configuration
### Requirements
- Virtual Mininet Test Setup
- Script is in tests/test_ft_lacp_aggregation_key.py

### Setup

#### Topology Diagram
```
+--------------------+
|                    |
|         s1         |
|                    |
+-1--2--3----5--6--7-+
  |  |  |    |  |  |
  |  |  |    |  |  |
  |  |  |    |  |  |
  |  |  |    |  |  |
+-1--2--3----6--7--5-+
|                    |
|         s2         |
|                    |
+--------------------+
```
### Test Setup
```
Switch 1
    LAG150
      Interface 1
      Interface 5
    LAG250
      Interface 2
      Interface 6
    LAG350
      Interface 3
      Interface 7
Switch 2
    LAG150
      Interface 1
      Interface 6
    LAG250
      Interface 2
      Interface 7
    LAG350
      Interface 3
      Interface 5
```
### Description
1. Turn on interfaces 1-3 and 5-7 in switch 1 and 2
* Create LAG 150, 250 and 350 in switch 1 and 2
* Associate interface 1 to LAG 150 in switch 1
* Associate interface 5 to LAG 150 in switch 1
* Associate interface 2 to LAG 250 in switch 1
* Associate interface 6 to LAG 250 in switch 1
* Associate interface 3 to LAG 350 in switch 1
* Associate interface 7 to LAG 350 in switch 1
* Associate interface 1 to LAG 150 in switch 2
* Associate interface 6 to LAG 150 in switch 2
* Associate interface 2 to LAG 250 in switch 2
* Associate interface 7 to LAG 250 in switch 2
* Associate interface 3 to LAG 350 in switch 2
* Associate interface 5 to LAG 350 in switch 2
* Waiting for LAG negotiation between switches
* Get information for interfaces 5-7 in both switches with CLI command
"show lacp interfaces"
* Validations on switch 1
  * Validate lag name for interface 5 should be 150
  * Validate lag name for interface 6 should be 250
  * Validate lag name for interface 7 should be 350
  * Validate lag state for interface 5 should be In Sync and
  Collecting/Distributing
  * Validate lag state for interface 6 should be In Sync and
  Collecting/Distributing
  * Validate lag state for interface 7 should be In Sync and
  Collecting/Distributing
* Validations on switch 2
  * Validate lag name for interface 5 should be 350
  * Validate lag name for interface 6 should be 150
  * Validate lag name for interface 7 should be 250
  * Validate lag state for interface 5 should be In Sync and
  Collecting/Distributing
  * Validate lag state for interface 6 should be In Sync and
  Collecting/Distributing
  * Validate lag state for interface 7 should be In Sync and
  Collecting/Distributing
* Clean configuration



### Test Result Criteria
#### Test Pass Criteria
All validations should return what describe above
#### Test Fail Criteria
If any validation return something different that was is expected

## LAG created with different aggregation key configured wit CLI
### Objective
Verify LAGs with different names from switches can get connected as long as all interfaces connected have same aggregation key, using CLI interface for
configuration
### Requirements
- Virtual Mininet Test Setup
- Script is in tests/test_ft_lacp_aggregation_key.py

### Setup

#### Topology Diagram
```
+--------+                  +--------+
|        1------------------2        |
|   s1   |                  |   s2   |
|        2------------------2        |
+--------+                  +--------+
```
### Test Setup
Switch 1
    LAG10
      Interface 1
      Interface 2
Switch 2
    LAG20
      Interfaces 1
      Interface 2

### Description
1. Turn interfaces 1 and 2 in both switches
* Create LAG 10 in switch 1
* Create LAG 20 in switch 2
* Associate interface 1 and 2 to lag 10 in switch 1
* Associate interface 1 and 2 to lag 20 in switch 2
* Wait for LAG negotiations between switches
* Get information from interface 1 and 2 from both switches using CLI command
"show lacp interface"
* Validations in switch 1
  * Validate interface 1 and 2 are In Sync and Collecting/Distributing in local
  state
  * Validate interface 1 and 2 are In Sync and Collecting/Distributing in remote
  state
* Validations in switch 2
  * Validate interface 1 and 2 are In Sync and Collecting/Distributing in local
  state
  * Validate interface 1 and 2 are In Sync and Collecting/Distributing in remote
  state

### Test Result Criteria
#### Test Pass Criteria
All validation should return what describe above
#### Test Fail Criteria
If any validation return a different value than expected

## LACP aggregation key with hosts
### Objective
Verify test cases for aggregation key functionality including hosts
connected to the switches
### Requirements
- Virtual Mininet Test Setup
- Script is in tests/test_ft_lacp_agg_key_hosts.py
### Setup
#### Topology Diagram
```
 +-------+              +-------+
 |       |              |       |
 |  hs1  |              |  hs2  |
 |       |              |       |
 +-------+              +-------+
     |                      |
     |                      |
     |                      |
 +-------+              +-------+
 |  sw1  |              |  sw2  |
 +-------+              +-------+
     |                      |
 LAG |                      | LAG
     |      +-------+       |
     +------+  sw3  +-------+
            +-------+
                |
                |
                |
            +-------+
            |       |
            |  hs3  |
            |       |
            +-------+
```
### Test Setup
```
Switch 1
    LAG10:
      Interface 1
      Interface 2

Switch 2
    LAG20:
      Interface 1
      Interface 2

Switch 3
    LAG310:
        Interface 1
        Interface 2
    LAG320:
        Interface 3
Host1[1] -> [3]Switch1
Host2[1] -> [3]Switch2
Host3[1] -> [4]Switch3
```

### Description
1. Turn on interfaces 1 and 2 in switch 1
* Turn on interfaces 1 and 2 in switch 2
* Turn on interfaces 1-4 in switch 3
* Create LAG 10 in Switch 1
* Create LAG 20 in Switch 2
* Create LAG 310 and 320 in Switch 2
* Configure IP 10.0.10.1 for host 1
* Configure IP 10.0.20.1 for host 2
* Configure IP 10.0.10.2 for host 3, to be able to ping with host 1
* Create Vlan 100 in switch 1
* Create Vlan 200 in switch 2
* Create Vlans 100 and 200 in switch 3
* Associate Vlan 100 to LAG 10 in switch 1
* Associate Vlan 200 to LAG 20 in switch 2
* Associate Vlan 100 to LAG 310 in switch 3
* Associate Vlan 200 to LAG 320 in switch 3
* Associate interface 3 in switch 1 to vlan 100
* Associate interface 4 in switch 3 to vlan 100
* Validate Host 1 and Host 3 can ping each other
* Associate interface 3 in switch 2 to vlan 200
* Associate interface 4 in switch 3 to vlan 200
* Remove IP 10.0.10.2 from host 3
* Configure IP 10.0.20.2 to host 3
* Validate Host 2 and Host 3 can ping each other
* Change interface 2 from Switch 3 to LAG 320
* Get state from interfaces 1 and 2 in switch 1 with CLI command
"show lacp interface"
* Get state from interfaces 2 in switch 2 with CLI command
"show lacp interface"
* Get state from interfaces 1, 2 and 3 in switch 3 with CLI command
"show lacp interface"
* Validate LACP state for interface 2 in switch 3 is Out of Sync and not in
Collecting/Distributing
* Validate LACP state for interface 2 in switch 1 is Out of Sync and not in
Collecting/Distributing
* Validate LACP state for interface 1 in switch 1 is Sync and
Collecting/Distributing
* Validate LACP state for interface 1 in switch 2 is Sync and
Collecting/Distributing
* Validate LACP state for interface 1 in switch 3 is Sync and
Collecting/Distributing
* Validate LACP state for interface 3 in switch 3 is Sync and
Collecting/Distributing
* Validate Host 2 and Host 3 can ping each other
* Change interface 4 in switch 3 to Vlan 100
* Remove IP 10.0.20.2 to host 3
* Configure IP 10.0.10.1 to host 3
* Validate Host 1 and Host 3 can ping each other
### Test Result Criteria
#### Test Pass Criteria
All validation should return what describe above
#### Test Fail Criteria
If any validation return a different value than expected


[LAG] Test Cases
=======

## Contents

* [Dynamic LAG: Create LAGs with different names](#Dynamic-LAG-Create-LAGs-with-different-names)
* [Static LAG: Create LAGs with different names](#Static-LAG-Create-LAGs-with-different-names)
* [Static LAG: Verify interface can be moved to a different LAG](#Static-LAG-Verify-interface-can-be-moved-to-different-LAG)
* [Dynamic LAG: Verify interface can be moved to a different LAG](#Dynamic-LAG-Verify-interface-can-be-moved-to-different-LAG)
* [Static LAG: Create LAG with non-consecutive interfaces](#Static-LAG-Create-LAG-with-non-consecutive-interfaces)
* [Dynamic LAG: Create LAG with non-consecutive interfaces](#Dynamic-LAG-Create-LAG-with-non-consecutive-interfaces)
* [Dynamic LAG: Convert dynamic LAG to static LAG](#Dynamic-LAG-Convert-dynamic-LAG-to-static-LAG)
* [Dynamic LAG: Delete LAG with minimum number of members](#Dynamic-LAG-Delete-LAG-with-minimum-number-of-members)
* [Dynamic LAG: Delete LAG with max number of members](#Dynamic-LAG-Delete-LAG-with-max-number-of-members)
* [Dynamic LAG: Delete non-existent LAGs](#Dynamic-LAG-Delete-non-existent-LAGs)
* [Dynamic LAG: Modify number of LAG members lower limits](#Dynamic-LAG-Modify-number-of-LAG-members-lower-limits)
* [Dynamic LAG: Modify number of LAG members upper limits](#Dynamic-LAG-Modify-number-of-LAG-members-upper-limits)
* [Static LAG: Convert static LAG to dynamic LAG](#Static-LAG-Convert-static-LAG-to-dynamic-LAG)
* [Static LAG: Delete LAG with minimum number of members](#Static-LAG-Delete-LAG-with-minimum-number-of-members)
* [Static LAG: Delete LAG with max number of members](#Static-LAG-Delete-LAG-with-max-number-of-members)
* [Static LAG: Delete non-existent LAGs](#Static-LAG-Delete-non-existent-LAGs)
* [Static LAG: Modify number of LAG members upper limits](#Static-LAG-Modify-number-of-LAG-members-upper-limits)
* [Dynamic LAG: Modify LAG without changing any setting](#Dynamic-LAG-Modify-LAG-without-changing-any-setting)
* [Static LAG: Modify LAG without changing any setting](#Static-LAG-Modify-LAG-without-changing-any-setting)

##  [Dynamic LAG: Create LAGs with different names] ##
### Objective ###
To verify a dynamic LAG cannot be created if the name is too long or has unsupported characters.
### Requirements ###
The requirements for this test case are:
 - 1 Switch running Open Switch
### Setup ###
#### Topology Diagram ####
```ditaa

						+----------+
						|          |
						|  dut01   |
						+----------+

```

#### Test Setup ####
Standalone Switch
### Description ###
This test verify a dynamic LAG can be configured using correct names and can not be configured using a name longer than permited or containing unsupported characters.

Steps:
1)      LAG name with value of 1.
2)      LAG name with value of 2000.
3)      Negative: LAG name with special characters or letters.
4)      Negative: LAG name with value 0,-1, 2001.

### Test Result Criteria ###
#### Test Pass Criteria ####
Test will pass if dynamic LAG can be configured using valid name and cannot be configured using name longer than permitted or containing invalid characters.
Steps that should succeed: 1 and 2
Steps that should fail: 3 and 4

#### Test Fail Criteria ####
Test will fail if dynamic LAG can not be configured using valid name or can be configured using invalid name.


##  [Static LAG: Create LAGs with different names] ##
### Objective ###
To verify a static LAG cannot be created if the name is too long or has unsupported characters.
### Requirements ###
The requirements for this test case are:
 - 1 Switch running Open Switch
### Setup ###
#### Topology Diagram ####
```ditaa

						+----------+
						|          |
						|  dut01   |
						+----------+

```

#### Test Setup ####
Standalone Switch
### Description ###
This test verify a static LAG can be configured using correct names and can not be configured using a name longer than permited or containing unsupported characters.

Steps:
1)      LAG name with value of 1.
2)      LAG name with value of 2000.
3)      Negative: LAG name with special characters or letters.
4)      Negative: LAG name with value 0,-1, 2001.

### Test Result Criteria ###
#### Test Pass Criteria ####
Test will pass if static LAG can be configured using valid name and cannot be configured using name longer than permitted or containing invalid characters.
Steps that should succeed: 1 and 2
Steps that should fail: 3 and 4

#### Test Fail Criteria ####
Test will fail if dynamic LAG can not be configured using valid name or can be configured using invalid name.



##  [Static LAG: Verify interface can be moved to a different LAG] 

### Objective ###
To move an interface associated with an static LAG to another static LAG

### Requirements ###
The requirements for this test case are:

 - 1 Switch running Open Switch
 
### Setup ###

#### Topology Diagram ####
```ditaa

						+----------+
						|          |
						|  dut01   |
						+----------+

```
#### Test Setup ####
### Description ###
This test verifies that an interface can be moved from one static LAG to another static LAG

Steps:
1- Configure LAG 1
2- Add interface to LAG 1
3- Configure LAG 2
4- Add interface to LAG 2

### Test Result Criteria ###
#### Test Pass Criteria ####
Interface is on LAG 1 after step 2, and is on LAG 2 after step 4

#### Test Fail Criteria ####
Interface is not on LAG 1 after step 2, or is not on LAG 2 after step 4



##  [Dynamic LAG: Verify interface can be moved to a different LAG] 

### Objective ###
To move an interface associated with an dynamic LAG to another dynamic LAG

### Requirements ###
The requirements for this test case are:

 - 1 Switch running Open Switch
 
### Setup ###

#### Topology Diagram ####
```ditaa

						+----------+
						|          |
						|  dut01   |
						+----------+

```
#### Test Setup ####
### Description ###
This test verifies that an interface can be moved from one dynamic LAG to another dynamic LAG

Steps:
1- Configure LAG 1
2- Add interface to LAG 1
3- Configure LAG 2
4- Add interface to LAG 2

### Test Result Criteria ###
#### Test Pass Criteria ####
Interface is on LAG 1 after step 2, and is on LAG 2 after step 4

#### Test Fail Criteria ####
Interface is not on LAG 1 after step 2, or is not on LAG 2 after step 4



##  [Static LAG: Create LAG with non-consecutive interfaces] 

### Objective ###
To move an interface associated with a static LAG to another static LAG

### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 Workstations
 
### Setup ###

#### Topology Diagram ####
```ditaa

						+-----------+
						|workstation|
						|    01     |
						+-----------+
						      |
						+----------+
						|          |
						|  dut01   |
						+----------+
						    ||         LAG 1
						+----------+
						|          |
						|  dut02   |
						+----------+
						     |
						+-----------+
						|workstation|
						|    02     |
						+-----------+
```
#### Test Setup ####
### Description ###
This test verifies that a static LAG can be configured using non consecutive interfaces

Steps:
1- Configure LAG 1
2- Add non consecutive interfaces to LAG 1 (example: 1 and 3)
3- Configure workstations
4- Ping between workstations

### Test Result Criteria ###
#### Test Pass Criteria ####
Ping between workstation is successful

#### Test Fail Criteria ####
Ping doesn't reach the other side


##  [Dynamic LAG: Create LAG with non-consecutive interfaces] 

### Objective ###
To move an interface associated with a dynamic LAG to another dynamic LAG

### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 Workstations
 
### Setup ###

#### Topology Diagram ####
```ditaa

						+-----------+
						|workstation|
						|    01     |
						+-----------+
						      |
						+----------+
						|          |
						|  dut01   |
						+----------+
						    ||         LAG 1
						+----------+
						|          |
						|  dut02   |
						+----------+
						     |
						+-----------+
						|workstation|
						|    02     |
						+-----------+
```
#### Test Setup ####
### Description ###
This test verifies that a dynamic LAG can be configured using non consecutive interfaces

Steps:
1- Configure LAG 1
2- Add non consecutive interfaces to LAG 1 (example: 1 and 3)
3- Configure workstations
4- Ping between workstations

### Test Result Criteria ###
#### Test Pass Criteria ####
Ping between workstation is successful

#### Test Fail Criteria ####
Ping doesn't reach the other side

##  [Dynamic LAG: Convert dynamic LAG to static LAG] ##
### Objective ###
To verify a dynamic LAG can be converted to a dynamic LAG and pass traffic.
### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |         
         |         
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |     
       |   |     LAG 1
       |   |     
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |       
         |      
 +-------+---------+
 |                 |
 |  Workstation 1  |
 |                 |
 +-----------------+
```
#### Test Setup ####

 1. Workstations have a static IP address each on the same range

### Description ###
This test verifies that a dynamic LAG formed between an active and a passive member can be transitioned to a static LAG retaining connectivity of clients employing the LAG to communicate.

Steps:
 1. Configure active LAG on switch 1 and add the 2 interfaces connected to switch 2.
 2. Configure passive LAG on switch 2 and add the 2 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations connectivity.
 5. Change LAGs on both switches to static.
 6. Test workstations connectivity.

### Test Result Criteria ###
#### Test Pass Criteria ####

 1. LAGs are converted from dynamic to static.
 2. Workstations can communicate after change in LAGs.

#### Test Fail Criteria ####

 1. LAGs cannot be converted from dynamic to static.
 2. Workstations cannot communicate.

##  [Dynamic LAG: Delete LAG with minimum number of members] ##
### Objective ###
To verify a dynamic LAG of 2 members or less can be deleted.
### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |         
         |         
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |     
       |   |     LAG 1
       |   |     
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |       
         |      
 +-------+---------+
 |                 |
 |  Workstation 1  |
 |                 |
 +-----------------+
```
#### Test Setup ####

 1. Workstations have a static IP address each on the same range

### Description ###
This test verifies that a dynamic LAG formed between an active and a passive member can be deleted when it has 2, 1 or 0 members.

Steps:
 1. Configure active LAG on switch 1 and add the 2 interfaces connected to switch 2.
 2. Configure passive LAG on switch 2 and add the 2 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations connectivity.
 5. Delete LAGS and test connectivity is broken.
 6. Re-create the LAGs with 1 interface and test connectivity is re-established.
 8. Delete LAGS and test connectivity is broken.
 9. Re-create the LAGs with no interfaces and re-delete them.

### Test Result Criteria ###
#### Test Pass Criteria ####

 1. LAGs can be recreated and deleted without errors.
 2. Workstations can communicate when a LAG is created with at least 1 interface.
 3. Workstations cannot communicate when LAGs are deleted or the LAG has no interfaces associated.

#### Test Fail Criteria ####

 1. LAGs cannot be created or deleted or there are errors when doing so.
 2. Workstations cannot communicate when a LAG is created with at least 1 interface.
 3. Workstations can communicate after deleting a LAG or when the LAG has not interfaces associated.

##  [Dynamic LAG: Delete LAG with max number of members] ##
### Objective ###
To verify a dynamic LAG of 8 members can be deleted.
### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |         
         |         
+--------+--------+
|                 |
|    Switch 1     |
|                 |
+-+-+-+-+-+-+-+-+-+
  | | | | | | | |  
  | | | | | | | |    LAG 1
  | | | | | | | |  
+-+-+-+-+-+-+-+-+-+
|                 |
|    Switch 2     |
|                 |
+-------+---------+
        |          
        |          
+-------+---------+
|                 |
|  Workstation 1  |
|                 |
+-----------------+
```
#### Test Setup ####

 1. Workstations have a static IP address each on the same range

### Description ###
This test verifies that a dynamic LAG formed between an active and a passive member can be deleted when it has 8 members.

Steps:
 1. Configure active LAG on switch 1 and add the 8 interfaces connected to switch 2.
 2. Configure passive LAG on switch 2 and add the 8 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations connectivity.
 5. Delete LAGS and test connectivity is broken.

### Test Result Criteria ###
#### Test Pass Criteria ####

 1. LAGs can be created and deleted without errors.
 2. Workstations can communicate when LAGs are created.
 3. Workstations cannot communicate when LAGs are deleted.

#### Test Fail Criteria ####

 1. LAGs cannot be created or deleted or there are errors when doing so.
 2. Workstations cannot communicate when the LAGs are created.
 3. Workstations can communicate after deleting the LAGs.

##  [Dynamic LAG: Delete non-existent LAGs] ##
### Objective ###
To verify attempting to delete a non-existent LAG will not affect created LAGs.
### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |         
         |         
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |     
       |   |     LAG 1
       |   |     
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |       
         |      
 +-------+---------+
 |                 |
 |  Workstation 1  |
 |                 |
 +-----------------+
```
#### Test Setup ####

 1. Workstations have a static IP address each on the same range

### Description ###
Tests that a previously configured dynamic Link Aggregation does not stop forwarding traffic when attempting to delete several non-existent Link Aggregations with different names that may not be supported.

Steps:
 1. Configure active LAG on switch 1 and add the 2 interfaces connected to switch 2.
 2. Configure passive LAG on switch 2 and add the 2 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations connectivity.
 5. Attempt to delete LAGs with the following names on each switch while verifying the created LAG is not changed on each switch: XX, 0, -1, 2000, 2001, @%&$#(), 60000, 600, 2
 6. Test workstations connectivity.

### Test Result Criteria ###
#### Test Pass Criteria ####

 1. Non-existent LAGs cannot be deleted (an error is displayed).
 2. Workstations can communicate.
 3. Existing LAGs don't see their configuration altered after attempting to delete the non-existent LAGs.

#### Test Fail Criteria ####

 1. Deleting a non-existent LAG isn't met with an error.
 2. Workstations cannot communicate.
 3. Existing LAGs have their configuration modified after attempting to delete the non-existent LAGs.

##  [Dynamic LAG: Modify number of LAG members lower limits] ##
### Objective ###
To verify it is possible to modify a LAG’s lower limits.
### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
+-----------------+ 
|                 | 
|  Workstation 1  | 
|                 | 
+--------+--------+ 
         |          
         |          
   +-----+------+   
   |            |   
   |  Switch 1  |   
   |            |   
   +-+---+---+--+   
     |   |   |      
     |   |   |      LAG 1
     |   |   |      
   +-+---+---+--+   
   |            |   
   |  Switch 2  |   
   |            |   
   +-----+------+   
         |          
         |          
 +-------+---------+
 |                 |
 |  Workstation 1  |
 |                 |
 +-----------------+
```
#### Test Setup ####

 1. Workstations have a static IP address each on the same range

### Description ###
Tests that a previously configured dynamic Link Aggregation can be modified to have between 0 and 2 members.

Steps:
 1. Configure active LAG on switch 1 and add the 3 interfaces connected to switch 2.
 2. Configure passive LAG on switch 2 and add the 3 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations connectivity.
 5. Remove 1 interface of each LAG and test connectivity between workstations.
 6. Add back the interface and test connectivity between workstations.
 7. Remove all interfaces from LAGs and test connectivity doesn't work.
 8. Add all interfaces back to LAGs and test connectivity is restored.
 9. Remove 2 interfaces from each LAG and test connectivity still works.
 10. Remove the 2 interfaces back and test connectivity.

### Test Result Criteria ###
#### Test Pass Criteria ####

 1. Number of interfaces on the LAGs are modified
 2. Workstations can communicate as long as LAGs have at least 1 interface.

#### Test Fail Criteria ####

 1. Number of interfaces on the LAGs cannot be modified.
 2. Workstations cannot communicate with at least 1 interface on each LAG or they can communicate when there are no interfaces on the LAGs.

##  [Dynamic LAG: Modify number of LAG members upper limits] ##
### Objective ###
To verify it is possible to modify a LAG’s upper limits.
### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |         
         |         
+--------+--------+
|                 |
|    Switch 1     |
|                 |
+-+-+-+-+-+-+-+-+-+
  | | | | | | | |  
  | | | | | | | |    LAG 1
  | | | | | | | |  
+-+-+-+-+-+-+-+-+-+
|                 |
|    Switch 2     |
|                 |
+-------+---------+
        |          
        |          
+-------+---------+
|                 |
|  Workstation 1  |
|                 |
+-----------------+
```
#### Test Setup ####

 1. Workstations have a static IP address each on the same range

### Description ###
Tests that a previously configured dynamic Link Aggregation can be modified to have between 7 and 8 members.

Steps:
 1. Configure active LAG on switch 1 and add the 8 interfaces connected to switch 2.
 2. Configure passive LAG on switch 2 and add the 8 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations connectivity.
 5. Remove 1 interface of each LAG and test connectivity between workstations.
 6. Add back the interface and test connectivity between workstations.

### Test Result Criteria ###
#### Test Pass Criteria ####

 1. Number of interfaces on the LAGs are modified
 2. Workstations can communicate.

#### Test Fail Criteria ####

 1. Number of interfaces on the LAGs cannot be modified.
 2. Workstations cannot communicate.

##  [Static LAG: Convert static LAG to dynamic LAG] ##
### Objective ###
To verify a dynamic LAG can be converted to a static LAG and pass traffic.
### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |         
         |         
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |     
       |   |     LAG 1
       |   |     
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |       
         |      
 +-------+---------+
 |                 |
 |  Workstation 1  |
 |                 |
 +-----------------+
```
#### Test Setup ####

 1. Workstations have a static IP address each on the same range

### Description ###
This test verifies that a static LAG formed 2 switches can be transitioned to a dynamic LAG with 1 member active and the other passive. Retaining connectivity of clients employing the LAG to communicate.

Steps:
 1. Configure static LAG on switch 1 and add the 2 interfaces connected to switch 2.
 2. Configure static LAG on switch 2 and add the 2 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations connectivity.
 5. Change LAGs on both switches to dynamic (1 active, the other passive).
 6. Test workstations connectivity.

### Test Result Criteria ###
#### Test Pass Criteria ####

 1. LAGs are converted from static to dynamic.
 2. Workstations can communicate after change in LAGs.

#### Test Fail Criteria ####

 1. LAGs cannot be converted from static to dynamic.
 2. Workstations cannot communicate.

##  [Static LAG: Delete LAG with minimum number of members] ##
### Objective ###
To verify a static LAG of 2 members or less can be deleted.
### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |         
         |         
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |     
       |   |     LAG 1
       |   |     
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |       
         |      
 +-------+---------+
 |                 |
 |  Workstation 1  |
 |                 |
 +-----------------+
```
#### Test Setup ####

 1. Workstations have a static IP address each on the same range

### Description ###
Tests that a previously configured static Link Aggregation of 2, 1 or 0 members can be deleted.

Steps:
 1. Configure static LAG on switch 1 and add the 2 interfaces connected to switch 2.
 2. Configure static LAG on switch 2 and add the 2 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations connectivity.
 5. Delete LAGS and test connectivity is broken.
 6. Re-create the LAGs with 1 interface and test connectivity is re-established.
 8. Delete LAGS and test connectivity is broken.
 9. Re-create the LAGs with no interfaces and re-delete them.

### Test Result Criteria ###
#### Test Pass Criteria ####

 1. LAGs can be recreated and deleted without errors.
 2. Workstations can communicate when a LAG is created with at least 1 interface.
 3. Workstations cannot communicate when LAGs are deleted or the LAG has no interfaces associated.

#### Test Fail Criteria ####

 1. LAGs cannot be created or deleted or there are errors when doing so.
 2. Workstations cannot communicate when a LAG is created with at least 1 interface.
 3. Workstations can communicate after deleting a LAG or when the LAG has not interfaces associated.

##  [Static LAG: Delete LAG with max number of members] ##
### Objective ###
To verify a static LAG of 8 members can be deleted.
### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |         
         |         
+--------+--------+
|                 |
|    Switch 1     |
|                 |
+-+-+-+-+-+-+-+-+-+
  | | | | | | | |  
  | | | | | | | |    LAG 1
  | | | | | | | |  
+-+-+-+-+-+-+-+-+-+
|                 |
|    Switch 2     |
|                 |
+-------+---------+
        |          
        |          
+-------+---------+
|                 |
|  Workstation 1  |
|                 |
+-----------------+
```
#### Test Setup ####

 1. Workstations have a static IP address each on the same range

### Description ###
Tests that a previously configured static Link Aggregation of 8 members can be deleted.

Steps:
 1. Configure active LAG on switch 1 and add the 8 interfaces connected to switch 2.
 2. Configure passive LAG on switch 2 and add the 8 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations connectivity.
 5. Delete LAGS and test connectivity is broken.

### Test Result Criteria ###
#### Test Pass Criteria ####

 1. LAGs can be created and deleted without errors.
 2. Workstations can communicate when LAGs are created.
 3. Workstations cannot communicate when LAGs are deleted.

#### Test Fail Criteria ####

 1. LAGs cannot be created or deleted or there are errors when doing so.
 2. Workstations cannot communicate when the LAGs are created.
 3. Workstations can communicate after deleting the LAGs.

##  [Static LAG: Delete non-existent LAGs] ##
### Objective ###
To verify attempting to delete a non-existent LAG will not affect created LAGs.
### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |         
         |         
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |     
       |   |     LAG 1
       |   |     
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |       
         |      
 +-------+---------+
 |                 |
 |  Workstation 1  |
 |                 |
 +-----------------+
```
#### Test Setup ####

 1. Workstations have a static IP address each on the same range

### Description ###
Tests that a previously configured static Link Aggregation does not stop forwarding traffic when attempting to delete several non-existent Link Aggregations with different names that may not be supported.

Steps:
 1. Configure static LAG on switch 1 and add the 2 interfaces connected to switch 2.
 2. Configure static LAG on switch 2 and add the 2 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations connectivity.
 5. Attempt to delete LAGs with the following names on each switch while verifying the created LAG is not changed on each switch: XX, 0, -1, 2000, 2001, @%&$#(), 60000, 600, 2
 6. Test workstations connectivity.

### Test Result Criteria ###
#### Test Pass Criteria ####

 1. Non-existent LAGs cannot be deleted (an error is displayed).
 2. Workstations can communicate.
 3. Existing LAGs don't see their configuration altered after attempting to delete the non-existent LAGs.

#### Test Fail Criteria ####

 1. Deleting a non-existent LAG isn't met with an error.
 2. Workstations cannot communicate.
 3. Existing LAGs have their configuration modified after attempting to delete the non-existent LAGs.

## [Static LAG: Modify number of LAG members upper limits] ##
### Objective ###
To verify it is possible to modify a LAG’s upper limits.
### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |         
         |         
+--------+--------+
|                 |
|    Switch 1     |
|                 |
+-+-+-+-+-+-+-+-+-+
  | | | | | | | |  
  | | | | | | | |    LAG 1
  | | | | | | | |  
+-+-+-+-+-+-+-+-+-+
|                 |
|    Switch 2     |
|                 |
+-------+---------+
        |          
        |          
+-------+---------+
|                 |
|  Workstation 1  |
|                 |
+-----------------+
```
#### Test Setup ####

 1. Workstations have a static IP address each on the same range

### Description ###
Tests that a previously configured static Link Aggregation can be modified to have between 7 and 8 members.

Steps:
 1. Configure static LAG on switch 1 and add the 8 interfaces connected to switch 2.
 2. Configure static LAG on switch 2 and add the 8 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations connectivity.
 5. Remove 1 interface of each LAG and test connectivity between workstations.
 6. Add back the interface and test connectivity between workstations.

### Test Result Criteria ###
#### Test Pass Criteria ####

 1. Number of interfaces on the LAGs are modified
 2. Workstations can communicate.

#### Test Fail Criteria ####

 1. Number of interfaces on the LAGs cannot be modified.
 2. Workstations cannot communicate.

##  [Dynamic LAG: Modify LAG without changing any setting] ##
### Objective ###
To verify when reapplying a dynamic LAG configuration the LAG doesn't change and continues to pass traffic.
### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
+-----------------+ 
|                 | 
|  Workstation 1  | 
|                 | 
+--------+--------+ 
         |          
         |          
   +-----+------+   
   |            |   
   |  Switch 1  |   
   |            |   
   +-+---+---+--+   
     |   |   |      
     |   |   |      LAG 1
     |   |   |      
   +-+---+---+--+   
   |            |   
   |  Switch 2  |   
   |            |   
   +-----+------+   
         |          
         |          
 +-------+---------+
 |                 |
 |  Workstation 1  |
 |                 |
 +-----------------+
```
#### Test Setup ####

 1. Workstations have a static IP address each on the same range

### Description ###
Tests that a previously configured dynamic Link Aggregation does not stop forwarding traffic when the link is reconfigured with the same initial settings.

Steps:
 1. Configure dynamic LAG on switch 1 and add the 3 interfaces connected to switch 2.
 2. Configure dynamic LAG on switch 2 and add the 3 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations connectivity.
 5. Re-apply LAG configuration and test connectivity again.

### Test Result Criteria ###
#### Test Pass Criteria ####

 1. Traffic flow between hosts is not stopped after applying dynamic LAG configuration and current configuration is not modified.

#### Test Fail Criteria ####

 1. Traffic between hosts stops crossing the static LAG link or configuration changes, interfaces reset or any other unexpected behavior.

 ##  [Static LAG: Modify LAG without changing any setting] ##
### Objective ###
To verify when reapplying a static LAG configuration the LAG doesn't change and continues to pass traffic.
### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
+-----------------+ 
|                 | 
|  Workstation 1  | 
|                 | 
+--------+--------+ 
         |          
         |          
   +-----+------+   
   |            |   
   |  Switch 1  |   
   |            |   
   +-+---+---+--+   
     |   |   |      
     |   |   |      LAG 1
     |   |   |      
   +-+---+---+--+   
   |            |   
   |  Switch 2  |   
   |            |   
   +-----+------+   
         |          
         |          
 +-------+---------+
 |                 |
 |  Workstation 1  |
 |                 |
 +-----------------+
```
#### Test Setup ####

 1. Workstations have a static IP address each on the same range

### Description ###
Tests that a previously configured static Link Aggregation does not stop forwarding traffic when the link is reconfigured with the same initial settings.

Steps:
 1. Configure static LAG on switch 1 and add the 3 interfaces connected to switch 2.
 2. Configure dynamic LAG on switch 2 and add the 3 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations connectivity.
 5. Re-apply LAG configuration and test connectivity again.

### Test Result Criteria ###
#### Test Pass Criteria ####

 1. Traffic flow between hosts is not stopped after applying static LAG configuration and current configuration is not modified.

#### Test Fail Criteria ####

 1. Traffic between hosts stops crossing the static LAG link or configuration changes, interfaces reset or any other unexpected behavior.


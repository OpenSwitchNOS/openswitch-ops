
Vlans Test Cases
=======

 [TOC]

## vlan_Id_Validation ##
### **Objective**  ##
Verify that a VID out of the 802.1Q range or reserved VID cannot be set and also verifies that a VID which already exists cannot be set again.
### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS
### Setup ###

#### Topology Diagram ####
```ditaa

	+-------+
	|       |
	|  DUT  |
	|       |
	+-------+

```
#### Test Setup ####
- 1 DUT in standalone

### Description ###
DUT must be running OpenSwitch OS to execute this test, should be by default configured and in the login or bash-shell context. 
### Test Result Criteria ###

#### Test Pass Criteria ####
Vlan out of range and repeated not configured
#### Test Fail Criteria ####
Vlan out of range or repeated were configured 

##  vlan_state_transition ##
### Objective ###
Verify the status of the Vlan change from up to down correctly. The status of a vlan is changed from down to up when a port is added to the vlan and the vlan has been brought up with the respective command.
### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS
### Setup ###

#### Topology Diagram ####
```ditaa

	+-------+
	|       |
	|  DUT  |
	|       |
	+-------+

```
#### Test Setup ####
- 1 DUT in standalone

### Description ###
DUT must be running OpenSwitch OS to execute this test, should be by default configured and in the login or bash-shell context. 
### Test Result Criteria ###
#### Test Pass Criteria ####
Vlans status is correctly verifyed and validated in every scenario of configuration
#### Test Fail Criteria ####
If vlan status is wrong showed in one of the scenarios

##  vlan_state_reason_transition ##
### Objective ###
With several vlans configured, bring one vlan up and confirm its state, witch one port assigned to it verify its Reason to ok, then issue the command to set the vlan down and confirm its state. Only one vlan should see a change in its state.

### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS
 
### Setup ###

#### Topology Diagram ####
```ditaa

	+-------+
	|       |
	|  DUT  |
	|       |
	+-------+

```
#### Test Setup ####
- 1 DUT in standalone
### Description ###
DUT must be running OpenSwitch OS to execute this test, should be by default configured and in the login or bash-shell context. 
### Test Result Criteria ###
#### Test Pass Criteria ####
Just one of the vlans get the configuration performed in reason and status
#### Test Fail Criteria ####
If more than one vlan was configured with same options or the vlan configured was incorrect configuration 

##  vlan_removed_from_end_of_table ##
### Objective ###
Verify the functionality of deleting a VLAN and reasigned port to another vlan. The Vlan will be deleted from the end of the VLAN list table. No traffic should pass through other vlans.

### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS
 - Ubuntu or CentOS for workStations with nmap installed
 
### Setup ###

#### Topology Diagram ####                  
```ditaa

    +-------+     +---------+     +-------+
    |       |     |         |     |       |
    |wrkSton+----->   DUT   <-----+wrkSton|
    |       |     |         |     |       |
    +-------+     +----^----+     +-------+
                       |                   
                       |                   
                  +---+ --+               
                  |       |               
                  |wrkSton|               
                  |       |               
                  +-------+

```               
#### Test Setup ####
- 1 DUT
- 3 workStations
### Description ###
DUT must be running OpenSwitch OS to execute this test, should be by default configured and in the login or bash-shell context. In the other hand workStations must have nmap installed.
### Test Result Criteria ###
#### Test Pass Criteria ####
Vlan is correctly deleted without affecting the other ones, and traffic is correctly sent.
#### Test Fail Criteria ####
Other vlan were affected with traffic sent and or target vlan was not correctly deleted.

##  vlan_removed_from_middle_of_table ##
### Objective ###
Verify the functionality of deleting a VLAN and reasigned port to another vlan. The Vlan will be deleted from middle of the VLAN list or the VLAN not with the highest or lowest VID. No traffic should pass through other vlans.

### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS
 - Ubuntu or CentOS for workStations with nmap installed
 
### Setup ###

#### Topology Diagram ####
```ditaa

    +-------+     +---------+     +-------+
    |       |     |         |     |       |
    |wrkSton+----->   DUT   <-----+wrkSton|
    |       |     |         |     |       |
    +-------+     +----^----+     +-------+
                       |                   
                       |                   
                  +---+ --+               
                  |       |               
                  |wrkSton|               
                  |       |               
                  +-------+

```    
#### Test Setup ####
- 1 DUT in standalone
- 3 workStations
### Description ###
DUT must be running OpenSwitch OS to execute this test, should be by default configured and in the login or bash-shell context. In the other hand workStations must have nmap installed.
### Test Result Criteria ###
#### Test Pass Criteria ####
Vlan is correctly deleted without affecting the other ones, and traffic is correctly sent.
#### Test Fail Criteria ####
Other vlan were affected with traffic sent and or target vlan was not correctly deleted.

##  vlan_initial_state##
### Objective ###
Verify the initial state of vlans when they are created.
### Requirements ###
The requirements for this test case are:

 - Single switch with OpenSwitch OS
### Setup ###
DUT must be running OpenSwitch OS and started from a clean setup.
#### Topology Diagram ####
```ditaa

	+-------+
	|       |
	|  DUT  |
	|       |
	+-------+

```
#### Test Setup ####
Standalone switch
### Description ###
When vlans are created they initially show a status of down.
### Test Result Criteria ###
#### Test Pass Criteria ####
Vlan 30 is created and shows up with a status of down in the 'show vlan' output
#### Test Fail Criteria ####
Vlan status is other than down

##  vlan_admin_down ##
### Objective ###
 Verify state of a vlan with ports ports assigned and  administratively shut down.
### Requirements ###
The requirements for this test case are:

 - Single switch with OpenSwitch OS
### Setup ###
DUT must be running OpenSwitch OS and started from a clean setup.
#### Topology Diagram ####
```ditaa

	+-------+
	|       |
	|  DUT  |
	|       |
	+-------+

```
#### Test Setup ####
Standalone switch
### Description ###
The state and reason values of a vlan is down and admin_down if ports have been assigned to the respective vlan but vlan has not been set to up.
### Test Result Criteria ###
#### Test Pass Criteria ####
Vlan 30 is created with ports assigned to it and shows up with a status of down and reason of admin_down in the 'show vlan' output.
#### Test Fail Criteria ####
Vlan status or reason value is other than down and admin_down.

##  vlan_description##
### Objective ###
Verify that a VLAN string name has a limit to the amount of characters it can accept and VLAN name string can be changed correctly.
### Requirements ###
The requirements for this test case are:

 - Single switch with OpenSwitch OS
### Setup ###
DUT must be running OpenSwitch OS and started from a clean setup.
#### Topology Diagram ####
```ditaa

	+-------+
	|       |
	|  DUT  |
	|       |
	+-------+

```
#### Test Setup ####
Standalone switch
### Description ###
a. Add new Vlan's to the switch and add a description.
b. Rename the new Vlan with another description.

### Test Result Criteria ###

#### Test Pass Criteria ####
Up to 250 alphanumeric characters to name the VLAN can be used and it can be changed.
#### Test Fail Criteria ####
No more than 250 alphanumeric characters accepted for VLAN's name.

##  vlan_no_port_member ##
### Objective ###
 Create three different vlans and set admin state 'up' for one of them. Verify the state is down and no_member_port in the reason value for one of them.
### Requirements ###
The requirements for this test case are:

 - Single switch with OpenSwitch OS
### Setup ###
DUT must be running OpenSwitch OS and started from a clean setup.
#### Topology Diagram ####
```ditaa

	+-------+
	|       |
	|  DUT  |
	|       |
	+-------+

```
#### Test Setup ####
Standalone switch
### Description ###
The state and reason value of a vlan with no ports and "no shutdown" should be down and no_member_port .
### Test Result Criteria ###
#### Test Pass Criteria ####
Vlan 30,40 and 50 are created. Only one vlan shows up with a status and reason of down and no_member_port as per the 'show vlan' output.
#### Test Fail Criteria ####
Vlan status or reason is other than down and no_member_port.

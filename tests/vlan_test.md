
VLAN Test Cases
=
##Contents


* [test_ft_vlan_id_validation](#testftvlanidvalidation)
* [test_ft_vlan_state_transition](#testftvlanstatetransition)
* [test_ft_vlan_state_reason_transition](#testftvlanstatereasontransition)
* [test_ft_vlan_removed_from_end_of_table](#testftvlanremovedfromendoftable)
* [test_ft_vlan_removed_from_middle_of_table](#testftvlanremovedfrommiddleoftable)
* [test_ft_vlan_tagged_frames_access_port](#testftvlantaggedframesaccessport)
* [test_ft_vlan_untagged_frames_on_trunk_port](#testftvlanuntaggedframesontrunkport)
* [test_ft_vlan_delete_existing_non_existing_vlan](#testftvlandeleteexistingnonexistingvlan)
* [test_ft_vlan_initial_state](#testftvlaninitialstate)
* [test_ft_vlan_admin_down](#testftvlanadmindown)
* [test_ft_vlan_trunk](#testftvlantrunk)
* [test_ft_vlan_no_member_port](#testftvlannomemberport)


## test_ft_vlan_id_validation ##
### **Objective**  ##
Verify that a VID out of the 802.1Q range or reserved VID cannot be set and also verifies that a VID which already exists cannot not be set again.
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

##  test_ft_vlan_state_transition ##
### Objective ###
Verify the status of the VLAN change from up to down correctly. The status of a VLAN is changed from down to up when a port is added to the VLAN and the VLAN has been brought up with the respective command.
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
Vlans status is correctly verifyed in every scenario
#### Test Fail Criteria ####
If vlan status is wrong showed in one of the scenarios

##  test_ft_vlan_state_reason_transition ##
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
Just one of the vlans get the configuration perfomed
#### Test Fail Criteria ####
If more than one vlan was configured with same options

##  test_ft_vlan_removed_from_end_of_table ##
### Objective ###
Verify the functionality of deleting a VLAN and reasigned port to another vlan. The Vlan will be deleted from the end of the VLAN list table. No traffic should pass through other vlans.

### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS
 - WorkStations must have nmap installed

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
Vlans is correctly delete it without affecting the others
#### Test Fail Criteria ####
If other vlans are affected

##  test_ft_vlan_removed_from_middle_of_table ##
### Objective ###
Verify the functionality of deleting a VLAN and reasigned port to another vlan. The Vlan will be deleted from the middle of the VLAN list or the VLAN not with the highest or lowest VID. No traffic should pass through other vlans.

### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS
 - Ubuntu workStations with nmap installed

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
VLAN is correctly deleted without affecting the other ones, and traffic is correctly sent.
#### Test Fail Criteria ####
If other vlans are affected

##  test_ft_vlan_tagged_frames_access_port ##
### Objective ###
Verify a switch port ability to handle tagged frames received on an access port.

### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS

### Setup ###

#### Topology Diagram ####
```ditaa

    +-------+     +---------+     +-------+
    |       |     |         |     |       |
    |wrkSton+----->   DUT   <-----+wrkSton|
    |       |     |         |     |       |
    +-------+     +----^----+     +-------+

```
#### Test Setup ####
- 1 DUT in standalone
- 2 workStations
### Description ###
DUT must be running OpenSwitch OS to execute this test, should be by default configured and in the login or bash-shell context.
### Test Result Criteria ###
#### Test Pass Criteria ####
Vlan forward traffic correctly and drop it if necessary
#### Test Fail Criteria ####
Vlan is not forwarding traffic propertly

##  test_ft_vlan_untagged_frames_on_trunk_port ##
### Objective ###
Verify a switch port ability to handle untagged frames received on trunk port.

### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS

### Setup ###

#### Topology Diagram ####
```ditaa

    +-------+     +---------+     +-------+
    |       |     |         |     |       |
    |wrkSton+----->   DUT   <-----+wrkSton|
    |       |     |         |     |       |
    +-------+     +----^----+     +-------+

```
#### Test Setup ####
- 1 DUT in standalone
- 2 workStations
### Description ###
DUT must be running OpenSwitch OS to execute this test, should be by default configured and in the login or bash-shell context.
### Test Result Criteria ###
#### Test Pass Criteria ####
Vlan forward traffic correctly and drop it if necessary
#### Test Fail Criteria ####
Vlan is not forwarding traffic propertly

##  test_ft_vlan_delete_existing_non_existing_vlan ##
### Objective ###
Verify the functionality of deleting an existent and non existent VLAN with ports/no ports configured within the VLAN

### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS
 - WorkStations must have nmap installed
### Setup ###

#### Topology Diagram ####
```ditaa

    +-------+     +---------+     +-------+
    |       |     |         |     |       |
    |wrkSton+----->   DUT   <-----+wrkSton|
    |       |     |         |     |       |
    +-------+     +----^----+     +-------+

```
#### Test Setup ####
- 1 DUT in standalone
- 2 workStations
### Description ###
DUT must be running OpenSwitch OS to execute this test, should be by default configured and in the login or bash-shell context.
### Test Result Criteria ###
#### Test Pass Criteria ####
Vlans is correctly delete it with ports member and no ports
#### Test Fail Criteria ####
If vlan is not correctly deleted

## test_ft_vlan_initial_state ##
### Objective ###
Verify the initial state of VLANs when they are created.
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
When VLANs are created they initially show a status of down.
### Test Result Criteria ###
#### Test Pass Criteria ####
VLAN 30 is created and shows up with a status of down in the 'show vlan' output
#### Test Fail Criteria ####
VLAN status is other than down

## test_ft_vlan_admin_down ##
### Objective ###
 Verify state of a VLAN with ports ports assigned and  administratively shut down.
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
The state and reason values of a VLAN is down and admin_down if ports have been assigned to the respective VLAN but VLAN has not been set to up.
### Test Result Criteria ###
#### Test Pass Criteria ####
VLAN 30 is created with ports assigned to it and shows up with a status of down and reason of admin_down in the 'show vlan' output.
#### Test Fail Criteria ####
VLAN status or reason value is other than down and admin_down.

##  test_ft_vlan_trunk ##
### Objective ###
Verify trunk link can carry multiple vlan traffic.
### Requirements ###
The requirements for this test case are:

 - 2 Switches with OpenSwitch OS
 - 4 Workstations
### Setup ###
DUT must be running OpenSwitch OS and started from a clean setup.
#### Topology Diagram ####
```ditaa

 +-----------+     +----------+
 |  DUT1     |     |   DUT2   |
 |           +-----+          |
 +-----------+     +----------+
    |     |           |      |
    |     |           |      |
 +----+ +-----+     +----+ +----+
 |Wrks| |Wrks |     |Wrks| |Wrks|
 +----+ +-----+     +----+ +----+

```
#### Test Setup ####
Configure trunking between the two DUTs.
Assign ports to vlans on both DUTs.

### Description ###
A trunk link is used to connect switches and it should be able to carry traffic from multiple VLANs.

### Test Result Criteria ###

#### Test Pass Criteria ####
Connectivity exists in all Vlans in the system.
#### Test Fail Criteria ####
Connectivity Failed.

##  test_ft_vlan_no_member_port ##
### Objective ###
 Create three different VLANs and set admin state 'up' for one of them. Verify the state is down and no_member_port in the reason value for one of them.
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
The state and reason value of a VLAN with no ports and "no shutdown" should be down and no_member_port .
### Test Result Criteria ###
#### Test Pass Criteria ####
VLAN 30,40 and 50 are created. Only one VLAN shows up with a status and reason of down and no_member_port as per the 'show vlan' output.
#### Test Fail Criteria ####
VLAN status or reason is other than down and no_member_port.

# VLAN Test Cases

##Contents


[test_ft_vlan_id_validation](#testftvlanidvalidation)
[test_ft_vlan_state_transition](#testftvlanstatetransition)
[test_ft_vlan_state_reason_transition](#testftvlanstatereasontransition)
[test_ft_vlan_removed_from_end_of_table](#testftvlanremovedfromendoftable)
[test_ft_vlan_removed_from_middle_of_table](#testftvlanremovedfrommiddleoftable)
[test_ft_vlan_tagged_frames_access_port](#testftvlantaggedframesaccessport)
[test_ft_vlan_untagged_frames_on_trunk_port](#testftvlanuntaggedframesontrunkport)
[test_ft_vlan_delete_existing_non_existing_vlan](#testftvlandeleteexistingnonexistingvlan)
[test_ft_vlan_initial_state](#testftvlaninitialstate)
[test_ft_vlan_admin_down](#testftvlanadmindown)
[test_ft_vlan_trunk](#testftvlantrunk)
[test_ft_vlan_no_member_port](#testftvlannomemberport)


## test_ft_vlan_id_validation
### **Objective**
Verify that a VID out of the 802.1Q range or reserved VID cannot be set. Also, confirm that a VID that already exists cannot not be set again.
### Requirements
The OpenSwitch OS is required for this test.
### Setup

#### Topology diagram
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test setup
The test setup consists of one DUT in standalone mode.

### Description
The DUT must be running the OpenSwitch OS to execute this test. The DUT must also be configured by default and be in the login or bash-shell context.
### Test result criteria

#### Test pass criteria
A VID out of the 802.1Q range or a VID already in use was not applied to the configuration.
#### Test fail criteria
A VID out of the 802.1Q range or a VID already in use was applied to the configuration.

##  test_ft_vlan_state_transition
### Objective
Verify that the status of the VLAN changes from up to down correctly. The status of a VLAN is changed from down to up when a port is added to the VLAN and the VLAN has been brought up with the 'no shutdown' command.
### Requirements
The OpenSwitch OS is required for this test.
### Setup

#### Topology diagram
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test setup
The test setup consists of one DUT in standalone mode.

### Description
The DUT must be running the OpenSwitch OS to execute this test. The DUT must also be configured by default and be in the login or bash-shell context.
### Test result criteria
#### Test pass criteria
The VLAN's status is correctly verified in every scenario.
#### Test fail criteria
If the VLAN status is wrong, it is displayed in one of the scenarios.

##  test_ft_vlan_state_reason_transition
### Objective
With several VLANs configured, bring up one VLAN and confirm its state, assigned one port to the same vlan and verify its Reason value is 'ok'. Then issue the command to set the VLAN to down and confirm its state. Only one VLAN should see a change in its state..

### Requirements
The OpenSwitch OS is required for this test.

### Setup

#### Topology diagram
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test setup
The test setup consists of one DUT in standalone mode.
### Description
The DUT must be running the OpenSwitch OS to execute this test. The DUT must also be configured by default and be in the login or bash-shell context.
### Test result criteria
#### Test pass criteria
Only one of the VLANs have the configuration performed.
#### Test fail criteria
More than one VLAN is configured with the same options.

##  test_ft_vlan_removed_from_end_of_table
### Objective
To verify the functionality of deleting a VLAN and reassigning the port to another VLAN.

### Requirements
The requirements for this test case are:

 - OpenSwitch OS
 - WorkStations must have nmap installed

### Setup

#### Topology diagram
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
#### Test setup
- 1 DUT
- 3 workStations
### Description
The DUT must be:

-Running the OpenSwitch OS
-Configured by default
-Using the login or bash-shell context
-Running with workstations that have 'nmap' installed.
### Test result criteria
#### Test pass criteria
The VLAN is deleted from the end of the VLAN table and no traffic passes through other VLANs.
#### Test fail criteria
This test fails if other VLANs are affected by the deletion.

##  test_ft_vlan_removed_from_middle_of_table
### Objective
To verify the functionality of deleting a VLAN from the middle of the VLAN list and reassigning the port to another VLAN. The VLAN is deleted from the middle of the VLAN list or the VLAN that does not have the highest or the lowest VID. No traffic passes through the other VLANs.

### Requirements
The requirements for this test case are:

 - OpenSwitch OS
 - Ubuntu workStations with nmap installed

### Setup

#### Topology diagram
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
#### Test setup
- 1 DUT in standalone mode.
- 3 workStations.
### Description
The DUT must be:

-Running the OpenSwitch OS
-Configured by default
-Using the login or bash-shell context
-Running with workstations that have 'nmap' installed.
### Test result criteria
#### Test pass criteria
The VLAN is deleted without affecting the other VLANS and the traffic is sent correctly.
#### Test fail criteria
This test fails if other VLANs are affected by the deletion.

##  test_ft_vlan_tagged_frames_access_port
### Objective
To confirm that a switch port has the ability to handle tagged frames received on an access port.

### Requirements
The OpenSwitch OS is required for this test.

### Setup

#### Topology diagram
```ditaa

    +-------+     +---------+     +-------+
    |       |     |         |     |       |
    |wrkSton+----->   DUT   <-----+wrkSton|
    |       |     |         |     |       |
    +-------+     +----^----+     +-------+

```
#### Test setup
- 1 DUT in standalone mode.
- 2 workStations.
### Description
The DUT must be running the OpenSwitch OS to execute this test. The DUT must also be configured by default and be in the login or bash-shell context.
### Test result criteria
#### Test pass criteria
The VLAN forwards traffic correctly or drops it if necessary.
#### Test fail criteria
Tagged frames are not discarded on a access port.

##  test_ft_vlan_untagged_frames_on_trunk_port
### Objective
To confirm a switch port's ability to handle untagged frames that are received on trunk ports.

### Requirements
The OpenSwitch OS is required for this test.

### Setup

#### Topology diagram
```ditaa

    +-------+     +---------+     +-------+
    |       |     |         |     |       |
    |wrkSton+----->   DUT   <-----+wrkSton|
    |       |     |         |     |       |
    +-------+     +----^----+     +-------+

```
#### Test setup
- 1 DUT in standalone mode
- 2 workStations
### Description
The DUT must be running the OpenSwitch OS to execute this test. The DUT must also be configured by default and be in the login or bash-shell context.
### Test result criteria
#### Test pass criteria
The VLAN forwards traffic correctly or drops it if necessary.
#### Test fail criteria
Untagged frames are not dropped on the trunk port.

##  test_ft_vlan_delete_existing_non_existing_vlan
### Objective
Verify the functionality of deleting an existing and nonexistent VLAN with ports or no ports configured within it.

### Requirements
The requirements for this test case are:

 - OpenSwitch OS
 - WorkStations must have nmap installed
### Setup

#### Topology diagram
```ditaa

    +-------+     +---------+     +-------+
    |       |     |         |     |       |
    |wrkSton+----->   DUT   <-----+wrkSton|
    |       |     |         |     |       |
    +-------+     +----^----+     +-------+

```
#### Test setup
- 1 DUT in standalone mode
- 2 workStations
### Description
The DUT must be running the OpenSwitch OS to execute this test. The DUT must also be configured by default and be in the login or bash-shell context.
### Test result criteria
#### Test pass criteria
Vlans is correctly delete it with ports member and no ports.
#### Test fail criteria
The VLAN is not deleted from the configuration.

## test_ft_vlan_initial_state
### Objective
Verify that the initially created VLANs are in a down state.
### Requirements
A single switch with the OpenSwitch OS is required for this test.
### Setup
The DUT must be running the OpenSwitch OS and started from a clean setup.
#### Topology diagram
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test setup
This test setup requires a standalone switch.
### Description
When VLANs are created they initially show a status of down.
### Test result criteria
#### Test pass criteria
A VLAN is created and is displayed with a status of "down" in the 'show vlan' output
#### Test fail criteria
A VLAN is created and is displayed with a status other than "down" in the 'show vlan' output

## test_ft_vlan_admin_down
### Objective
 Confirm the state of a VLAN that has ports assigned but is shut down administratively.
### Requirements
A single switch with the OpenSwitch OS is required for this test.
### Setup
The DUT must be running the OpenSwitch OS and started from a clean setup.
#### Topology diagram
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test setup
This test setup requires a standalone switch.
### Description
The VLAN state value is down and the reason value is admin_down if the ports have been assigned to the respective VLAN, but the VLAN has not been set to "up".
### Test result criteria
#### Test pass criteria
A VLAN is created with ports assigned to it and displays a Status value of "up" and a Reason value of 'admin_down' in the 'show vlan' output.
#### Test fail criteria
This test fails with a status other than down or a reason other than admin_down.

##  test_ft_vlan_trunk
### Objective
Verify that a trunk link can carry traffic from multiple VLANs.
### Requirements
The requirements for this test case are:

 - 2 Switches with OpenSwitch OS
 - 4 Workstations
### Setup
The DUT must be running the OpenSwitch OS and started from a clean setup.
#### Topology diagram
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
#### Test setup
1. Configure the trunking between two DUTs.
2. Assign the ports to VLANs on both DUTs.

### Description
A trunk link is used to connect switches and it must be able to carry traffic from multiple VLANs.

### Test result criteria

#### Test pass criteria
This test is successful if connectivity exists for all VLANs in the system.
#### Test fail criteria
This test is unsuccessful if the connectivity fails.

##  test_ft_vlan_no_member_port
### Objective
To create three different VLANs and set the admin state to 'up' for one of them. Verify the the state is down and no_member_port in the reason value for one of the VLANs.
### Requirements
A single switch with the OpenSwitch OS is required for this test.
### Setup
The DUT must be running the OpenSwitch OS and started from a clean setup.
#### Topology diagram
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test setup
This test setup requires a standalone switch.
### Description
A VLAN with no ports and "no shutdown" must report a state value of "down" and a reason value of "no_member_port".
### Test result criteria
#### Test pass criteria
Three VLANs are created. Only one VLAN displays the status value as "up" and reason value as "no_member_port" in the 'show vlan' output.
#### Test fail criteria
The VLAN status is other than "down" or the reason value is other than "no_member_port".

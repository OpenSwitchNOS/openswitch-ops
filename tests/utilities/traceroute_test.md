# Traceroute Feature Test Cases
=
[TOC]

## Verify traceroute between 2 switches configured with IPv4 address ##
### Objective ###
To traces a packet between 2 switches and traceroute is successful.
### Requirements ###
The requirements for this test case are:
 - Docker version 1.7 or above.
 - Accton AS5712 switch docker instance.
 - A topology with a single link between two switches, switch 1 and switch 2 are configured with IPv4 address.

### Setup ###
#### Topology Diagram ####

     +----------------+                                        +--------------------+
     |                |                                        |                    |
     | AS5712 switch  |<-------------------------------------->|  AS5712 switch     |
     |                |int1                                int1|                    |
     |                |                                        |                    |
     +----------------+                                        +--------------------+

#### Test Setup ####

### Test case 1.01: traceroute from switch1 to switch2 and vice versa ###
### Description ###
Verify traceroute from switch1 to switch2 and vice versa is successful.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to successfully traceroute.
#### Test Fail Criteria ####
Traceroute doesn't reach the other side, destination Unreachable.

### Test case 1.02: traceroute from switch1 to switch2 with multiple Parameters ###
### Description ###
Verify traceroute from switch1 to switch2 with multiple Parameters is successful.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to successfully traceroute.
#### Test Fail Criteria ####
Traceroute doesn't reach the other side, destination Unreachable.

### Test case 1.03: traceroute from switch1 to switch2 with ip-option loose source route ###
### Description ###
Verify traceroute from switch1 to switch2 with ip-option loose source route is successful.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to successfully traceroute and loose source route output is displayed.
#### Test Fail Criteria ####
Traceroute doesn't reach the other side, destination Unreachable.


## Verify traceroute6 between 2 switches configured with IPv6 address ##
### Objective ###
To traces a packet between 2 switches and traceroute6 is successful.
### Requirements ###
The requirements for this test case are:
 - Docker version 1.7 or above.
 - Accton AS5712 switch docker instance.
 - A topology with a single link between two switches, switch 1 and switch 2 are configured with IPv6 address.

### Setup ###
#### Topology Diagram ####

     +----------------+                                        +--------------------+
     |                |                                        |                    |
     | AS5712 switch  |<-------------------------------------->|  AS5712 switch     |
     |                |int1                                int1|                    |
     |                |                                        |                    |
     +----------------+                                        +--------------------+

#### Test Setup ####

### Test case 1.01: traceroute6 from switch1 to switch2 and vice versa ###
### Description ###
Verify traceroute6 from switch1 to switch2 and vice versa is successful.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to successfully traceroute6.
#### Test Fail Criteria ####
Traceroute6 doesn't reach the other side, destination Unreachable.

### Test case 1.02: traceroute6 from switch1 to switch2 with multiple Parameters ###
### Description ###
Verify traceroute6 from switch1 to switch2 with multiple Parameters is successful.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to successfully traceroute6.
#### Test Fail Criteria ####
Traceroute6 doesn't reach the other side, destination Unreachable.

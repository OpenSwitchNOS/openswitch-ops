# Ping Feature Test Cases
=
[TOC]

## Verify Connectivity between 2 switches configured with IPv4 address ##
### Objective ###
To verify connectivity between 2 switches is successfully established and ping is successful.
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

### Test case 1.01: ping from switch1 to switch2 and vice versa ###
### Description ###
Verify ping from switch1 to switch2 and vice versa is successful.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to successfully ping and packet loss observed is 0%.
#### Test Fail Criteria ####
Ping doesn't reach the other side, packet loss is 100%.

### Test case 1.02: ping from switch1 to switch2 with multiple Parameters ###
### Description ###
Verify ping from switch1 to switch2 with multiple Parameters is successful.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to successfully ping and packet loss observed is 0%.
#### Test Fail Criteria ####
Ping doesn't reach the other side, packet loss is 100%.

### Test case 1.03: ping from switch1 to switch2 with ip-option record-route ###
### Description ###
Verify ping from switch1 to switch2 with ip-option record-route is successful.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to successfully ping and record-route output is displayed.
#### Test Fail Criteria ####
Ping doesn't reach the other side, packet loss is 100%.

### Test case 1.04: ping from switch1 to switch2 with ip-option include-timestamp ###
### Description ###
Verify ping from switch1 to switch2 with ip-option include-timestamp is successful.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to successfully ping and roundtrip time is displayed.
#### Test Fail Criteria ####
Ping doesn't reach the other side, packet loss is 100%.

### Test case 1.05: ping from switch2 to switch1 with ip-option include-timestamp-and-address ###
### Description ###
Verify ping from switch1 to switch2 with ip-option include-timestamp-and-address is successful.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to successfully ping and roundtrip time to a particular host as well as address is displayed.
#### Test Fail Criteria ####
Ping doesn't reach the other side, packet loss is 100%.

## Verify Connectivity between 2 switches configured with IPv6 address ##
### Objective ###
To verify connectivity between 2 switches is successfully established and ping6 is successful.
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

### Test case 1.01: ping from switch1 to switch2 and vice versa ###
### Description ###
Verify ping from switch1 to switch2 and vice versa is successful.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to successfully ping and packet loss observed is 0%.
#### Test Fail Criteria ####
Ping doesn't reach the other side, packet loss is 100%.

### Test case 1.02: ping from switch1 to switch2 with multiple Parameters ###
### Description ###
Verify ping from switch1 to switch2 with multiple Parameters is successful.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to successfully ping and packet loss observed is 0%.
#### Test Fail Criteria ####
Ping doesn't reach the other side, packet loss is 100%.

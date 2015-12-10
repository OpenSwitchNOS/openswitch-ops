# SFTP Feature Test Cases

[TOC]

## Verify SFTP server configuration ##
### Objective ###
To verify enable/disable of the SFTP server.
### Requirements ###
The requirements for this test case are:
 - Docker version 1.7 or above.
 - Accton AS5712 switch docker instance.
 - A topology with a single link between two switches, switch 1 and switch 2 are configured with IPv4 address/IPv6 address.

### Setup ###
#### Topology Diagram ####

     +----------------+                                        +--------------------+
     |                |                                        |                    |
     | AS5712 switch  |<-------------------------------------->|  AS5712 switch     |
     |                |int1                                int1|                    |
     |                |                                        |                    |
     +----------------+                                        +--------------------+

#### Test Setup ####

### Test case 1.01: SFTP copy without SFTP server service###
### Description ###
Verify SFTP copy is not working when SFTP server service is not enabled.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is unable to perform the SFTP copy.
#### Test Fail Criteria ####
User is able to perform the SFTP copy.

### Test case 1.02: Enabling SFTP server ###
### Description ###
Enable the SFTP server on switch1 using appropriate CLI.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to start a SFTP server
#### Test Fail Criteria ####
User is unable to initiate a SFTP server

### Test case 1.03: Verify the SFTP server status ###
### Description ###
Verify the SFTP server status using the show command.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to check for the current SFTP server status as either enable/disable.
#### Test Fail Criteria ####
User is unable to execute the show command

## Verify SFTP client ##
### Objective ###
To verify Interactive/Non-Interactive mode of the SFTP client.
### Requirements ###
The requirements for this test case are:
 - Docker version 1.7 or above.
 - Accton AS5712 switch docker instance.
 - A topology with a single link between two switches, switch 1 and switch 2 are configured with IPv4 address/IPv6 address.

### Setup ###
#### Topology Diagram ####

     +----------------+                                        +--------------------+
     |                |                                        |                    |
     | AS5712 switch  |<-------------------------------------->|  AS5712 switch     |
     |                |int1                                int1|                    |
     |                |                                        |                    |
     +----------------+                                        +--------------------+

#### Test Setup ####

### Test case 1.04:  SFTP client in a Interactive mode ###
### Description ###
Verify SFTP client working in the interactive mode
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to enter the interactive mode and perform get/put.
#### Test Fail Criteria ####
User is unable to enter the interactive mode

### Test case 1.05: SFTP client in a Non-Interactive mode ###
### Description ###
Verify switch1 working as an SFTP client is able to perform a secure copy
from switch2 which is providing SFTP server service.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to perform secure copy from switch2.
#### Test Fail Criteria ####
User is unable to perform secure copy from switch2.

### Test case 1.06: SFTP copy on a non mgmt interface ###
### Description ###
Verify SFTP copy is not working on a non mgmt interface.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is unable to perform the SFTP copy.
#### Test Fail Criteria ####
User is able to perform the SFTP copy.

### Test case 1.07: SFTP copy from multiple vty sessions###
### Description ###
Verify SFTP copy from a number of vty sessions
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to perform the SFTP copy from different vty sessions.
#### Test Fail Criteria ####
User is unable to perform the SFTP copy from different vty sessions.
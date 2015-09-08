
<!--  See the https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet for additional information about markdown text.
Here are a few suggestions in regards to style and grammar:
* Use active voice. With active voice, the subject is the doer of the action. Tell the reader what
to do by using the imperative mood, for example, Press Enter to view the next screen. See https://en.wikipedia.org/wiki/Active_voice for more information about the active voice. 
* Use present tense. See https://en.wikipedia.org/wiki/Present_tense for more information about using the present tense. 
* The subject is the test case. Explain the actions as if the "test case" is doing them. For example, "Test case configures the IPv4 address on one of the switch interfaces". Avoid the use of first (I) or second person. Explain the instructions in context of the test case doing them. 
* See https://en.wikipedia.org/wiki/Wikipedia%3aManual_of_Style for an online style guide.
 --> 
Feature Test Cases
=======

<!--Provide the name of the grouping of commands, for example, LLDP commands-->
	
	- Test to verify login with local authentication.
	- Test to verify login with radius authentication.
	- Test to verify fallback to local authentication.
	- Test to verify secondary radius server authentication.
	- Test to verify SSH authentication method. 

##  Test to verify login with local authentication ##
### Objective ###
 Test cases to configure local authentication. And login with local credentials. 
### Requirements ###
The requirements for this test case are:
<!-- list as bulleted items of the equipment needed, software versions required, etc. -->
 - Docker version 1.7 or above.
 
 - Accton 5712 switch docker instance.
### Setup ###
#### Topology Diagram ####
              +------------------+              
              |                  |
              |  AS5712 switch   |
              |                  |
              +------------------+ 

#### Test Setup ####
AS5712 switch instance.
### Test case 1.01 : Test to verify local authentication ###
### Description ###
Test to verify whether local authentication is success when authentication is configured to local.
### Test Result Criteria ###
#### Test Pass Criteria ####
User should be able to login with local credentials
#### Test Fail Criteria ####
User not able to login with local password.
### Test case 1.02 : Test to verify local authentication with wrong password ###
### Description ###
Test to verify whether local authentication is a failure when given wrong credentials.
### Test Result Criteria ###
#### Test Pass Criteria ####
User should be not login with wrong credentials.
#### Test Fail Criteria ####
User successfully logged in with wrong credentials.

##  Test to verify login with radius authentication ##
### Objective ###
 Test cases to configure radius server and reachable. And login with credentials  configured in radius server. 
### Requirements ###
The requirements for this test case are:
<!-- list as bulleted items of the equipment needed, software versions required, etc. -->

- Docker version 1.7 or above.
 
- Accton 5712 switch docker instance.

- Host instance with radius server installed. (This test took freeradius server as reference)
### Setup ###
#### Topology Diagram ####



     +----------------+                                        +--------------------+
     |                |                                        |                    |
     | AS5712 switch  |<-------------------------------------->|  Host with         |
     |                |eth0                               eth1 |  radius server     |
     |                |                                        |                    |
     +----------------+                                        +--------------------+

#### Test Setup ####
AS5712 switch instance and host with radius server.
### Test case 2.01 : Test to verify radius authentication ###
### Description ###
Test to verify whether radius authentication is success with credentials configured on radius server.
### Test Result Criteria ###
#### Test Pass Criteria ####
User should be able to login with radius server credentials.
#### Test Fail Criteria ####
User not able to login with radius server credentials.
### Test case 2.02 : Test to verify radius authentication with wrong credentials ###
### Description ###
Test to verify whether radius authentication is failure with wrong credentials compared to the credentials configured on radius server.
### Test Result Criteria ###
#### Test Pass Criteria ####
User should be not able to login with wrong radius server credentials.
#### Test Fail Criteria ####
User able to login with wrong radius server credentials.

##  Test to verify fallback to local authentication.##
### Objective ###
 Test cases to configure radius server and not-reachable. And authentication fallback to local.  
### Requirements ###
The requirements for this test case are:
<!-- list as bulleted items of the equipment needed, software versions required, etc. -->

- Docker version 1.7 or above.

- Accton 5712 switch docker instance.
 
- Host instance with radius server installed. (This test took freeradius server as reference)
### Setup ###
#### Topology Diagram ####

     +----------------+                                        +--------------------+
     |                |                                        |                    |
     | AS5712 switch  |<-------------------------------------->|  Host with         |
     |                |eth0                               eth1 |  radius server     |
     |                |                                        |                    |
     +----------------+                                        +--------------------+

#### Test Setup ####
AS5712 switch instance and host with radius server.
### Test case 3.01 : Test to verify fallback to local authentication###
### Description ###
Test to verify whether authentication is success with local credentials when radius server is not reachable.  
### Test Result Criteria ###
#### Test Pass Criteria ####
User should be able to login with local credentials.
#### Test Fail Criteria ####
User not able to login with local credentials.

##  Test to verify secondary radius server authentication.##
### Objective ###
 Test cases to configure two radius server and first radius server not-reachable. And authentication should happen through secondary radius server.  
### Requirements ###
The requirements for this test case are:

- Docker version 1.7 or above.

- Accton 5712 switch docker instance.

- Two host instance with radius server installed. (This test took freeradius server as reference)
### Setup ###
#### Topology Diagram ####

     +---------------------+           +----------------------+        +----------------------+
     |   HOST              |       int 1                      |int 2   |       HOST           |
     | Radius server       |<----+---->|     AS5712           |<--+--->|     Radius server    |
     |                    h1-eth0      |                      |    h2-eth0                    |
     |                     |           |                      |        |                      |
     +--------------------->           +----------------------+        +----------------------+
#### Test Setup ####
AS5712 switch instance and two host with radius server.
### Test case 3.01 : Test to verify fallback to local authentication###
### Description ###
Test to verify whether authentication is success with secondary radius server credentials when first radius server is not reachable.  
### Test Result Criteria ###
#### Test Pass Criteria ####
User should be able to login with secondary radius server credentials.
#### Test Fail Criteria ####
User not able to login with secondary radius server credentials.

##  Test to verify SSH authentication method.##
### Objective ###
 In this test case we configure ssh authentication method to be either password authentication or public key authentication. 
### Requirements ###
The requirements for this test case are:

- Accton 5712 switch docker instance.

### Setup ###
#### Topology Diagram ####

     +----------------+
     |                |
     | AS5712 switch  |
     |                |
     +----------------+

#### Test Setup ####
AS5712 switch instance.
### Test case 4.01 : Test to verify ssh public key authentication###
### Description ###
Test to verify whether ssh public key authentication method is enabled in OVDSDB or not.  
### Test Result Criteria ###
#### Test Pass Criteria ####
SSH public key authentication is enabled and respective ssh config files are modified accordingly.
#### Test Fail Criteria ####
SSH public key authentication is not enabled and respective ssh config files are not modified accordingly.

### Test case 4.02 : Test to verify ssh password authentication###
### Description ###
Test to verify whether ssh password authentication method is enabled in OVDSDB or not.  
### Test Result Criteria ###
#### Test Pass Criteria ####
SSH password authentication is enabled and respective ssh config files are modified accordingly.
#### Test Fail Criteria ####
SSH password authentication is not enabled and respective ssh config files are not modified accordingly.
### Test case 4.03 : Test to verify disabling ssh public key authentication###
### Description ###
Test to verify whether ssh public key authentication method is disabled in OVDSDB or not.  
### Test Result Criteria ###
#### Test Pass Criteria ####
SSH public key authentication is disabled and respective ssh config files are modified accordingly.
#### Test Fail Criteria ####
SSH public key authentication is not disabled and respective ssh config files are not modified accordingly.

### Test case 4.04 : Test to verify disabling ssh password authentication###
### Description ###
Test to verify whether ssh password authentication method is disabled in OVDSDB or not.  
### Test Result Criteria ###
#### Test Pass Criteria ####
SSH password authentication is disabled and respective ssh config files are modified accordingly.
#### Test Fail Criteria ####
SSH password authentication is not disabled and respective ssh config files are not modified accordingly.

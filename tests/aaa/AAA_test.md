
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
	- Test to verify login with RADIUS server authentication.
	- Test to verify fallback to local authentication.
	- Test to verify secondary RADIUS server authentication.
	- Test to verify SSH authentication method. 

##  Test to verify login with local authentication ##
### Objective ###
 Test cases to configure local authentication. And login with local credentials. 
### Requirements ###
The requirements for this test case are:
<!-- list as bulleted items of the equipment needed, software versions required, etc. -->
 - Docker version 1.7 or above.
 
 - Accton AS5712 switch docker instance.
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
Test to verify whether local authentication is successful when with local credentials.
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

##  Test to verify login with RADIUS server authentication ##
### Objective ###
 Test cases to configure RADIUS server and reachable. Login with credentials configured on the RADIUS server.
### Requirements ###
The requirements for this test case are:
<!-- list as bulleted items of the equipment needed, software versions required, etc. -->

- Docker version 1.7 or above.
 
- Accton 5712 switch docker instance.

- Host instance with RADIUS server installed. (This test took freeradius server as reference)
### Setup ###
#### Topology Diagram ####



     +----------------+                                        +--------------------+
     |                |                                        |                    |
     | AS5712 switch  |<-------------------------------------->|  Host with         |
     |                |eth0                               eth1 |  RADIUS server     |
     |                |                                        |                    |
     +----------------+                                        +--------------------+

#### Test Setup ####
AS5712 switch instance and host with RADIUS server.
### Test case 2.01 : Test to verify RADIUS authentication ###
### Description ###
Test to verify whether RADIUS authentication is success with credentials configured on RADIUS server.
### Test Result Criteria ###
#### Test Pass Criteria ####
User should be able to login with RADIUS server credentials.
#### Test Fail Criteria ####
User not able to login with RADIUS server credentials.
### Test case 2.02 : Test to verify RADIUS authentication with wrong credentials ###
### Description ###
Test to verify whether RADIUS authentication is failure with wrong credentials compared to the credentials configured on RADIUS server.
### Test Result Criteria ###
#### Test Pass Criteria ####
User should be not able to login with wrong RADIUS server credentials.
#### Test Fail Criteria ####
User able to login with wrong RADIUS server credentials.

##  Test to verify fallback to local authentication.##
### Objective ###
Test case to configure RADIUS server and make it not-reachable, then authentication fallback to local.  
### Requirements ###
The requirements for this test case are:
<!-- list as bulleted items of the equipment needed, software versions required, etc. -->

- Docker version 1.7 or above.

- Accton 5712 switch docker instance.
 
- Host instance with RADIUS server installed. (This test took freeradius server as reference)
### Setup ###
#### Topology Diagram ####

     +----------------+                                        +--------------------+
     |                |                                        |                    |
     | AS5712 switch  |<-------------------------------------->|  Host with         |
     |                |eth0                               eth1 |  RADIUS server     |
     |                |                                        |                    |
     +----------------+                                        +--------------------+

#### Test Setup ####
AS5712 switch instance and host with RADIUS server.
### Test case 3.01 : Test to verify fallback to local authentication###
### Description ###
Test to verify whether authentication is success with local credentials when RADIUS server is not reachable.  
### Test Result Criteria ###
#### Test Pass Criteria ####
User should be able to login with local credentials.
#### Test Fail Criteria ####
User not able to login with local credentials.

##  Test to verify secondary RADIUS server authentication.##
### Objective ###
 Test case to configure two RADIUS server and make first RADIUS server not-reachable. Then authentication should happen through secondary RADIUS server.  
### Requirements ###
The requirements for this test case are:

- Docker version 1.7 or above.

- Accton 5712 switch docker instance.

- Two host instance with RADIUS server installed. (This test took freeradius server as reference)
### Setup ###
#### Topology Diagram ####

     +---------------------+           +----------------------+        +----------------------+
     |   HOST              |           |                      |eth0    |       HOST           |
     | RADIUS server       |<----+---->|     AS5712           |<--+--->|     RADIUS server    |
     |                    h1-eth0  eth0|                      |    h2-eth0                    |
     |                     |           |                      |        |                      |
     +--------------------->           +----------------------+        +----------------------+
#### Test Setup ####
AS5712 switch instance and two host with RADIUS server.
### Test case 3.01 : Test to verify fallback to local authentication###
### Description ###
Test to verify whether authentication is success with secondary RADIUS server credentials when first RADIUS server is not reachable.  
### Test Result Criteria ###
#### Test Pass Criteria ####
User should be able to login with secondary RADIUS server credentials.
#### Test Fail Criteria ####
User not able to login with secondary RADIUS server credentials.

##  Test to verify SSH authentication method.##
### Objective ###
 In this test case we configure ssh authentication method to be either password authentication or public key authentication. Then check if user authentication is successful. 
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
Test to verify whether ssh public key authentication method is successful or not.  
### Test Result Criteria ###
#### Test Pass Criteria ####
SSH public key authentication is enabled and respective ssh config files are modified accordingly. User whose public key is copied to by auto provisioning feature can login automatically.
#### Test Fail Criteria ####
SSH public key authentication is not enabled and respective ssh config files are not modified accordingly and login fails.

### Test case 4.02 : Test to verify ssh password authentication###
### Description ###
Test to verify whether ssh password authentication method is successful or not. Password is prompted and user need to authenticate with valid passowrd.
### Test Result Criteria ###
#### Test Pass Criteria ####
SSH password authentication is enabled and respective ssh config files are modified accordingly. Login is successful with the password given by the user.
#### Test Fail Criteria ####
SSH password authentication is not enabled and respective ssh config files are not modified accordingly and login fails.

[Standard REST API] Test Cases
==============================

[TOC]

##  Standard REST API PUT, GET Methods for URI "/rest/v1/system" ##
### Objective ###
The objective of the test case is to configure the system through Standard REST API PUT Method.
### Requirements ###
The requirements for this test case are:
- OpenSwitch.
- Ubuntu Workstation.
### Setup ###
#### Topology Diagram ####
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
### Description ###
The test case is to configure the system through Standard REST API PUT Method.

> **STEPS:**

> - Connect the OpenSwitch to Ubuntu workstation as shown in the topology diagram.
> - Configure the IPV4 address on the switch management interfaces.
> - Configure the IPV4 address on the Ubuntu workstation.
> - Configure the system through Standard REST API PUT Method for the URI "/rest/v1/system".
> - Validate the system configuration with HTTP return code for the URI "/rest/v1/system".
> - Execute Standard REST API GET Method for URI "/rest/v1/system".
> - Validate the GET Method HTTP return code for "/rest/v1/system" and respective values.

### Test Result Criteria ###
#### Test Pass Criteria ####
- The first test passes, if the standard REST API PUT method returns HTTP code 200 OK for the URI "/rest/v1/system".
- The second test passes, if the standard REST API GET method returns HTTP code 200 OK for the URI "/rest/v1/system" and the returned data is identical to the date used for the PUT.
#### Test Fail Criteria ####
- The first test fails, if the standard REST API PUT Method does not return HTTP code 200 for the URI "/rest/v1/system".
- The second test fails, if the standard REST API GET Method does not return HTTP code 200 for the URI "/rest/v1/system" or the returned data is not identical to the data used for PUT.

##  Standard REST API GET Method for URI "/rest/v1/system/subsystems". ##
### Objective ###
The objective of the test case is to validate the subsystem through Standard REST API GET Method.
### Requirements ###
The requirements for this test case are:
- OpenSwitch.
- Ubuntu Workstation.
### Setup ###
#### Topology Diagram ####
+---------------+                 +---------------+
|               |       	  |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
### Description ###
The test case is to validate the subsystem through Standard REST API GET Method.

> **STEPS:**

> - Connect the OpenSwitch to Ubuntu workstation as shown in the topology diagram.
> - Configure the IPV4 address on the switch management interfaces.
> - Configure the IPV4 address on the Ubuntu workstation.
> - Execute Standard REST API GET Method for URI "/rest/v1/system/subsystems".
> - Validate the GET Method HTTP return code for "/rest/v1/system/subsystems" and respective values.

### Test Result Criteria ###
#### Test Pass Criteria ####
- The test case is passes, if the standard REST API GET Method returns HTTP code 200 for the URI "/rest/v1/system/subsystems" and the returned data is identical.
#### Test Fail Criteria ####
- The test case is fails, if the standard REST API GET Method not returns HTTP code 200 for the URI "/rest/v1/system/subsystems".

##  Standard REST API PUT, GET, DELETE Methods for URI "/rest/v1/system/interfaces/{id}". ##
### Objective ###
The objective of the test case is to validate the "/rest/v1/system/interfaces/{id}" through Standard REST API GET Method.
### Requirements ###
The requirements for this test case are:
- OpenSwitch.
- Ubuntu Workstation.
### Setup ###
#### Topology Diagram ####
+---------------+      		  +---------------+
|               |       	  |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
### Description ###
The objective of the test case is to validate the "/rest/v1/system/interfaces/{id}" through Standard REST API GET Method.

> **STEPS:**

> - Connect the OpenSwitch to Ubuntu workstation as shown in the topology diagram.
> - Configure the IPV4 address on the switch management interfaces.
> - Configure the IPV4 address on the Ubuntu workstation.
> - Configure the "/rest/v1/system/interfaces/{id}" through Standard REST API PUT Method.
> - Validate the "/rest/v1/system/interfaces/{id}" configuration with HTTP return code.
> - Execute Standard REST API GET Method for URI "/rest/v1/system/interfaces/{id}".
> - Validate the GET Method HTTP return code for "/rest/v1/system/interfaces/{id}" and respective values.
> - Execute Standard REST API DELETE Method for URI "/rest/v1/system/interfaces/{id}".
> - Validate the DELETE Method HTTP return code for "/rest/v1/system/interfaces/{id}".
> - Execute Standard REST API GET Method for URI "/rest/v1/system/interfaces/{id}".
> - Validate the GET Method HTTP return code for "/rest/v1/system/interfaces/{id}".

### Test Result Criteria ###
#### Test Pass Criteria ####
- The first test passes, if the standard REST API PUT method returns HTTP code 200 OK for the URI "/rest/v1/system/interfaces/{id}".
- The second test passes, if the standard REST API GET method returns HTTP code 200 OK for the URI "/rest/v1/system/interfaces/{id}" and the returned data is identical to the date used for the PUT.
- The third case is passes, if the standard REST API DELETE Method returns HTTP code 204 for the URI "/rest/v1/system/interfaces/{id}".
- The fourth test passes, if the standard REST API GET method not returns HTTP code 200 OK for the URI "/rest/v1/system/interfaces/{id}".
#### Test Fail Criteria ####
- The first test fails, if the standard REST API PUT Method does not return HTTP code 200 for the URI "/rest/v1/system/interfaces/{id}".
- The second test fails, if the standard REST API GET Method does not return HTTP code 200 for the URI "/rest/v1/system/interfaces/{id}" or the returned data is not identical to the data used for PUT.
- The test case is fails, if the standard REST API DELETE Method not returns HTTP code 204 for the URI "/rest/v1/system/interfaces/{id}".
- The fourth test fails, if the standard REST API GET method returns HTTP code 200 OK for the URI "/rest/v1/system/interfaces/{id}".

##  Standard REST API GET Method for URI "/rest/v1/system/vrfs". ##
### Objective ###
The objective of the test case is to validate the "/rest/v1/system/vrfs" through Standard REST API GET Method.
### Requirements ###
The requirements for this test case are:
- OpenSwitch.
- Ubuntu Workstation.
### Setup ###
#### Topology Diagram ####
+---------------+      		  +---------------+
|               |      		  |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
### Description ###
The objective of the test case is to validate the "/rest/v1/system/vrfs" through Standard REST API GET Method.

> **STEPS:**

> - Connect the OpenSwitch to Ubuntu workstation as shown in the topology diagram.
> - Configure the IPV4 address on the switch management interfaces.
> - Configure the IPV4 address on the Ubuntu workstation.
> - Execute Standard REST API GET Method for URI "/rest/v1/system/vrfs".
> - Validate the GET Method HTTP return code for "/rest/v1/system/vrfs" and respective values.

### Test Result Criteria ###
#### Test Pass Criteria ####
- The test case is passes, if the standard REST API GET Method returns HTTP code 200 for the URI "/rest/v1/system/vrfs" and the returned data is identical.
#### Test Fail Criteria ####
- The test case is fails, if the standard REST API GET Method not returns HTTP code 200 for the URI "/rest/v1/system/vrfs".

##  Standard REST API GET Method for URI "/rest/v1/system/route_maps/{id}". ##
### Objective ###
The objective of the test case is to validate the "/rest/v1/system/route_maps/{id}" through Standard REST API GET Method.
### Requirements ###
The requirements for this test case are:
- OpenSwitch.
- Ubuntu Workstation.
### Setup ###
#### Topology Diagram ####
+---------------+      		  +---------------+
|               |      		  |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
### Description ###
The objective of the test case is to validate the "/rest/v1/system/route_maps/{id}" through Standard REST API GET Method.

> **STEPS:**

> - Connect the OpenSwitch to Ubuntu workstation as shown in the topology diagram.
> - Configure the IPV4 address on the switch management interfaces.
> - Configure the IPV4 address on the Ubuntu workstation.
> - Execute Standard REST API GET Method for URI "/rest/v1/system/route_maps/{id}".
> - Validate the GET Method HTTP return code for "/rest/v1/system/route_maps/{id}" and respective values.

### Test Result Criteria ###
#### Test Pass Criteria ####
- The test case is passes, if the standard REST API GET Method returns HTTP code 200 for the URI "/rest/v1/system/route_maps/{id}" and the returned data is identical.
#### Test Fail Criteria ####
- The test case is fails, if the standard REST API GET Method not returns HTTP code 200 for the URI "/rest/v1/system/route_maps/{id}".

##  Standard REST API GET Method for URI "/rest/v1/system/interfaces". ##
### Objective ###
The objective of the test case is to validate the "/rest/v1/system/interfaces" through Standard REST API GET Method.
### Requirements ###
The requirements for this test case are:
- OpenSwitch.
- Ubuntu Workstation.
### Setup ###
#### Topology Diagram ####
+---------------+      		  +---------------+
|               |     		  |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
### Description ###
The objective of the test case is to validate the "/rest/v1/system/interfaces" through Standard REST API GET Method.

> **STEPS:**

> - Connect the OpenSwitch to Ubuntu workstation as shown in the topology diagram.
> - Configure the IPV4 address on the switch management interfaces.
> - Configure the IPV4 address on the Ubuntu workstation.
> - Execute Standard REST API GET Method for URI "/rest/v1/system/interfaces".
> - Validate the GET Method HTTP return code for "/rest/v1/system/interfaces" and respective values.

### Test Result Criteria ###
#### Test Pass Criteria ####
- The test case is passes, if the standard REST API GET Method returns HTTP code 200 for the URI "/rest/v1/system/interfaces" and the returned data is identical.
#### Test Fail Criteria ####
- The test case is fails, if the standard REST API GET Method not returns HTTP code 200 for the URI "/rest/v1/system/interfaces".

##  Standard REST API PUT Method with invalid data for URIs. ##
### Objective ###
The objective of the test case is to configure REST API PUT Method with invalid data for URIs.
### Requirements ###
The requirements for this test case are:
- OpenSwitch.
- Ubuntu Workstation.
### Setup ###
#### Topology Diagram ####
+---------------+      		  +---------------+
|               |     		  |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
### Description ###
The test case is to configure REST API PUT Method with invalid data for URIs.

> **STEPS:**

> - Connect the OpenSwitch to Ubuntu workstation as shown in the topology diagram.
> - Configure the IPV4 address on the switch management interfaces.
> - Configure the IPV4 address on the Ubuntu workstation.
> - Configure the standard REST API PUT Method with invalid data for URIs mentioned.
> - Validate that standard REST API PUT Method fails to configure with invalid data for all URIs.

### Test Result Criteria ###
#### Test Pass Criteria ####
- The test case is passes, if the standard REST API PUT Method with invalid data fails to return HTTP code 200 OK for the URIs.
#### Test Fail Criteria ####
- The test case is fails, if the standard REST API PUT Method with invalid data passes to return HTTP code 200 OK for the URIs.

## REST API login authentication ##
### Objective ###
The objective for the test case is to check login and authentication.
### Requirements ###
The requirements for this test case are:
- OpenSwitch.
- Ubuntu Workstation.
### Setup ###
#### Topology Diagram ####
+---------------+      		  +---------------+
|               |     		  |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
### Description ###
The test case is to check login and authentication.

> **STEPS:**

> - Connect the OpenSwitch to Ubuntu workstation as shown in the topology diagram.
> - Configure the IPV4 address on the switch management interfaces.
> - Configure the IPV4 address on the Ubuntu workstation.
> - Execute Standard REST API POST Method for URI "/login" with valid credentials.
> - Validate the GET Method HTTP return code for URI "/login"  - 1st test case.
> - Execute Standard REST API POST Method for URI "/login" with invalid credentials.
> - Validate the GET Method HTTP failed return code for URI "/login" - 2nd test case.

### Test Result Criteria ###
#### Test Pass Criteria ####
- The first test passes if the standard REST API GET method returns HTTP code 200 OK for the URI "/login".
- The second test passes if the standard REST API GET method returns HTTP code 401 UNAUTHORIZED for the URI "/login".
#### Test Fail Criteria ####
- The first test fails if the standard REST API GET Method does not return HTTP code 200 for the URI "/login".
- The second test fails if the standard REST API GET Method does not return HTTP code 401 for the URI "/login".

## REST API startup config verify ##
### Objective ###
The objective for the test case is to verify REST API startup config.
### Requirements ###
The requirements for this test case are:
- OpenSwitch.
- Ubuntu Workstation.
### Setup ###
#### Topology Diagram ####
+---------------+      		  +---------------+
|               |      		  |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
### Description ###
verify REST API startup config.

> **STEPS:**

> - Connect the OpenSwitch to Ubuntu workstation as shown in the topology diagram.
> - Configure the IPV4 address on the switch management interfaces.
> - Configure the IPV4 address on the Ubuntu workstation.
> - Execute Standard REST API PUT Method for URI "/rest/v1/system" - 1st test case.
> - Execute Standard REST API GET Method for URI "/rest/v1/system" - 2nd test case.

### Test Result Criteria ###
#### Test Pass Criteria ####
- The first test passes if the standard REST API PUT method returns HTTP code 200 OK for the URI "/rest/v1/system".
- The second test passes if the standard REST API GET method returns HTTP code 200 OK for the URI "/rest/v1/system" and the returned data is identical to the date used for the PUT.
#### Test Fail Criteria ####
- The first test fails, if the standard REST API PUT Method does not return HTTP code 200 for the URI "/rest/v1/system".
- The second test fails, if the standard REST API GET Method does not return HTTP code 200 for the URI "/rest/v1/system" or the returned data is not identical to the data used for PUT.

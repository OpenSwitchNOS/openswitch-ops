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
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
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
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
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
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
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
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
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
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
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
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
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
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
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
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
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
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
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

Ports Resource: REST Test Cases
=============================

[TOC]

## Query Port ##

### Objective ###
The test case verify:

- Query all ports
- Query an specific port.
- Query an non-existent port.

###  Requirements ###

Port "Port1" must exist

### Setup ###

#### Topology Diagram ####
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

#### Test Setup ####

** Switch 1 ** has a Port with name Port1 with the following configuration data

```
{
"configuration": {
"name": "Port1",
"interfaces": ["/rest/v1/system/interfaces/1"],
"trunks": [413],
"ip4_address_secondary": ["192.168.0.1"],
"lacp": "active",
"bond_mode": "l2-src-dst-hash",
"tag": 654,
"vlan_mode": "trunk",
"ip6_address": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
"external_ids": {"extid1key": "extid1value"},
"bond_options": {"key1": "value1"},
"mac": "01:23:45:67:89:ab",
"other_config": {"cfg-1key": "cfg1val"},
"bond_active_slave": "null",
"ip6_address_secondary": ["01:23:45:67:89:ab"],
"vlan_options": {"opt1key": "opt2val"},
"ip4_address": "192.168.0.1",
"admin": "up"
}
}
```

### Description ###

1. Verify if port is at port list

- Execute GET request over /rest/v1/system/ports
- Verify if the HTTP response is 200 OK.
- Verify if the returned port list has at least one element
- Verify if the URI /rest/v1/system/ports/Port1 is on response data

2. Verify if a specific port exists

- Execute GET request over rest/v1/system/ports/Port1
- Verify if the HTTP response is 200 OK
- Verify if the response data is not empty
- Verify if the response data has the keys: "configuration", "status" and "statistics"
- Verify if the configuration data is equal to the Port1 configuration data

3. Verify if a non-existent port exists
- Execute GET request over rest/v1/system/ports/Port2
- Verify if the HTTP response is 404 NOT FOUND

### Test Result Criteria ###
#### Test Pass Criteria ####

The test is considered passed when querying a the post list:

- The HTTP response is 200 OK
- The port list has at least one port
- There is a URI "rest/v1/system/ports/Port1" in port list returned from rest/v1/system/ports URI

The test is considered passed when querying Port1:

- When doing a GET request over "rest/v1/system/ports/Port1" the HTTP response is 200 OK
- The response data is not empty
- The response data contains the following keys: "configuration", "status" and "statistics"
- The port configuration data is equal to the Port1 (pre-set port)

The test case is considered passed when querying a non-existent Port:

- The HTTP response is 404 NOT FOUND

#### Test Fail Criteria ####

The test is considered failed when querying a the post list:

- The HTTP response is not equal to 200 OK
- When doing a GET request to "rest/v1/system/ports" the port "Port1" is at the Ports URI list

The test is considered failed when querying Port1:

- When doing a GET request over "rest/v1/system/ports/Port1" the HTTP response is not equalt to 404 NOT FOUND

The test case is considered failed when querying a non-existent Port:

- The HTTP response is not equal to 404 NOT FOUND

## Create a Port ##

### Objective ###

The test case verify:
- Create a port
- Create port with the same name that another
- Port data validation: Ranges, Types, Allowed Values, Malformed JSON, Missing Attributes


###  Requirements ###

Bridge "bridge_normal" must exists.

### Setup ###

#### Topology Diagram ####
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

#### Test Setup ####

### Description ###

#### Create Port ####

1. Execute a POST request over /rest/v1/system/ports with the following data and verify if the HTTP response is 201 CREATED

```
{
"configuration": {
"name": "Port1",
"interfaces": ["/rest/v1/system/interfaces/1"],
"trunks": [413],
"ip4_address_secondary": ["192.168.0.1"],
"lacp": "active",
"bond_mode": "l2-src-dst-hash",
"tag": 654,
"vlan_mode": "trunk",
"ip6_address": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
"external_ids": {"extid1key": "extid1value"},
"bond_options": {"key1": "value1"},
"mac": "01:23:45:67:89:ab",
"other_config": {"cfg-1key": "cfg1val"},
"bond_active_slave": "null",
"ip6_address_secondary": ["01:23:45:67:89:ab"],
"vlan_options": {"opt1key": "opt2val"},
"ip4_address": "192.168.0.1",
"admin": "up"
},
"referenced_by": [{"uri":"/rest/v1/system/bridges/bridge_normal"}]
}
```

2. Execute a GET request over /rest/v1/system/ports/Port1 and verify if the response is 200 OK
3. Verify if the configuration response data from the step 2 is the same that the configuration data from step 1

#### Create an existent Port ####
Verify that the HTTP response is BAD_REQUEST when creating a existing port with name "Port1".

1. Execute a POST request over /rest/v1/system/ports, with the name "Port1"
```
"name": "Port1"
```
2. Verify if the HTTP response is 400 BAD REQUEST

#### Data validation ####

##### Data Types Validation #####

###### Invalid string type ######

1. Set the "ip4_address" value to:
```
"ip4_address": 192
```
2. Execute a POST request over /rest/v1/system/ports with the Port data changed
3. Verify if the HTTP response is 400 BAD REQUEST

###### Valid string type ######

1. Set the "ip4_address" value to:
```
"ip4_address": "192.168.0.1"
```
2. Execute a POST request over /rest/v1/system/ports with the Port data changed
3. Verify if the HTTP response is 201 CREATED

###### Invalid integer type ######

1. Set the "tag" value to:
```
"tag": "675"
```
2. Execute a POST request over /rest/v1/system/ports with the Port data changed
3. Verify if the HTTP response is 400 BAD REQUEST

###### Valid integer type ######

1. Set the "tag" value to:
```
"tag": 675
```
2. Execute a POST request over /rest/v1/system/ports with the Port data changed
2. Verify if the HTTP response is 201 CREATED

###### Invalid array type ######

1. Set the "trunks" value to:
```
"trunks": "654,675"
```
2. Execute a POST request over /rest/v1/system/ports with the Port data changed
3. Verify if the HTTP response is 400 BAD REQUEST

###### Valid array type ######

1. Set the "trunks" value to:
```
"trunks": [654,675]
```
2. Execute a POST request over /rest/v1/system/ports with the Port data changed
3. Verify if the HTTP response is 201 CREATED

##### Ranges Validation #####


###### Invalid range for string type ######

1. Set the "ip4_address" value to:
```
"ip4_address": "175.167.134.123/248"
```
2. Execute a POST request over /rest/v1/system/ports with the Port data changed
3. Verify if the HTTP response is 400 BAD REQUEST

###### Valid range for string type ######

1. Set the "ip4_address" value to:
```
"ip4_address": "175.167.134.123/24"
```
2. Execute a POST request over /rest/v1/system/ports with the Port data changed
3. Verify if the HTTP response is 201 CREATED

###### Invalid range for integer type ######

1. Set the "tag" value to:
```
"tag": 4095
```
2. Execute a POST request over /rest/v1/system/ports with the Port data changed
3. Verify if the HTTP response is 400 BAD REQUEST

###### Valid range for integer type ######

1. Set the "tag" value to:
```
"tag": 675
```
2. Execute a POST request over /rest/v1/system/ports with the Port data changed
3. Verify if the HTTP response is 201 CREATED

###### Invalid range for array type ######

1. Change the "interfaces" value to:
```
"interfaces": [ "/rest/v1/system/interfaces/1",
"/rest/v1/system/interfaces/2",
"/rest/v1/system/interfaces/3",
"/rest/v1/system/interfaces/4",
"/rest/v1/system/interfaces/5",
"/rest/v1/system/interfaces/6",
"/rest/v1/system/interfaces/7",
"/rest/v1/system/interfaces/8",
"/rest/v1/system/interfaces/9",
"/rest/v1/system/interfaces/10" ]
```
2. Execute a POST request over /rest/v1/system/ports with the Port data changed:
3. Verify if the HTTP response is 400 BAD REQUEST

###### Valid range for array type ######

1. Change the "interfaces" value to:
```
"interfaces": ["/rest/v1/system/interfaces/1"]
```
2. Execute a POST request over /rest/v1/system/ports with the Port data changed
3. Verify if the HTTP response is 201 CREATED

##### Allowed Data Values Validation #####


###### Invalid data value ######

1. Change the "vlan_mode" value to:
```
"vlan_mode": "invalid_value"
```
2. Execute a POST request over /rest/v1/system/ports with the Port data changed
3. Verify if the HTTP response is 400 BAD REQUEST

###### Valid data value ######

1. Change the "vlan_mode" value to:
```
"vlan_mode": "access"
```
2. Execute a POST request over /rest/v1/system/ports with the Port data changed
3. Verify if the HTTP response is 201 CREATED

##### Missing attribute Validation #####

1. Execute a POST request over /rest/v1/system/ports without "vlan_mode" attribute
2. Verify if the HTTP Response is 400 BAD REQUEST
3. Execute a POST request over /rest/v1/system/ports with all attributes
4. Verify if the HTTP Response is 201 CREATED

##### Unknown Attribute Validation #####

1.  Execute a POST request over /rest/v1/system/ports with an unknown attribute:
```
"unknown_attribute": "unknown_value"
```
2. Verify if the HTTP Response is 400 BAD REQUEST
3. Execute a POST request over /rest/v1/system/ports with all allowed attributes
4. Verify if the HTTP Response is 201 CREATED

##### Malformed Json Validation #####

1. Execute a POST request over /rest/v1/system/ports with a semi-colon at the end of the json data
2. Verify if the HTTP Response is 400 BAD REQUEST
3. Execute a POST request over /rest/v1/system/ports without the semi-colon at the end of the json data
4. Verify if the HTTP Response is 201 CREATED


### Test Result Criteria ###
#### Test Pass Criteria ####

The test is considered passed when creating a new port

- The HTTP response is 200 OK
- When executing a GET request over /rest/v1/system/ports/Port1 the HTTP response is 200 OK
- When the configuration data posted is the same that the retrieved port

The test is considered passed when creating a port with the same that another port

- The HTTP response is 400 BAD REQUEST

The test is considered passed when creating a new port with a valid string type

- The HTTP response is 201 CREATED

The test is considered passed when creating a new port with an invalid string type

- The HTTP response is 400 BAD REQUEST

The test is considered passed when creating a new port with a valid integer type

- The HTTP response is 201 CREATED

The test is considered passed when creating a new port with an invalid array type

- The HTTP response is 400 BAD REQUEST

The test is considered passed when creating a new port with valid array type

- The HTTP response is 201 CREATED

The test is considered passed when creating a new port with an invalid value on attribute

- The HTTP response is 400 BAD REQUEST

The test is considered passed when creating a new port with a valid value on attribute

- The HTTP response is 201 CREATED

The test is considered passed when creating a new port with a missing attribute

- The HTTP response is 400 BAD REQUEST

The test is considered passed when creating a new port with with all attributes

- The HTTP response is 201 CREATED

The test is considered passed when creating a new port with an unknown attribute

- The HTTP response is 400 BAD REQUEST

The test is considered passed when creating a new port with all allowed attributes

- The HTTP response is 201 CREATED

The test is considered passed when creating a new port with malformed json data

- The HTTP response is 400 BAD REQUEST

The test is considered passed when creating a new port with well-formed json data

- The HTTP response is 201 CREATED

#### Test Fail Criteria ####

The test is considered failed when creating a new port

- The HTTP response is not equal to 200 OK
- When executing a GET request over /rest/v1/system/ports/Port1 the HTTP response is not equal to 200 OK
- When the configuration data posted is not the same that the retrieved port

The test is considered failed when creating a port with the same that another port

- The HTTP response is not equal 400 BAD REQUEST

The test is considered failed when creating a new port with a valid string type

- The HTTP response is not equal 201 CREATED

The test is considered failed when creating a new port with an invalid string type

- The HTTP response is not equal 400 BAD REQUEST

The test is considered failed when creating a new port with a valid integer type

- The HTTP response is not equal 201 CREATED

The test is considered failed when creating a new port with an invalid array type

- The HTTP response is not equal 400 BAD REQUEST

The test is considered failed when creating a new port with valid array type

- The HTTP response is not equal 201 CREATED

The test is considered failed when creating a new port with an invalid value on attribute

- The HTTP response is not equal 400 BAD REQUEST

The test is considered failed when creating a new port with a valid value on attribute

- The HTTP response is not equal 201 CREATED

The test is considered failed when creating a new port with a missing attribute

- The HTTP response is not equal 400 BAD REQUEST

The test is considered failed when creating a new port with with all attributes

- The HTTP response is not equal 201 CREATED

The test is considered failed when creating a new port with an unknown attribute

- The HTTP response is not equal 400 BAD REQUEST

The test is considered failed when creating a new port with all allowed attributes

- The HTTP response is not equal 201 CREATED

The test is considered failed when creating a new port with malformed json data

- The HTTP response is not equal 400 BAD REQUEST

The test is considered failed when creating a new port with well-formed json data

- The HTTP response is not equal 201 CREATED


## Update a Port ##

### Objective ###

The test case verify:
- Modify a port
- Try to modify the name of the port
- Port data validation: Ranges, Types, Allowed Values, Malformed JSON, Missing Attributes

###  Requirements ###

Port "Port1" must exist

### Setup ###

#### Topology Diagram ####
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

#### Test Setup ####

** Switch 1 ** has a Port with name Port1 with the following configuration data

```
{
"configuration": {
"name": "Port1",
"interfaces": ["/rest/v1/system/interfaces/1"],
"trunks": [413],
"ip4_address_secondary": ["192.168.0.1"],
"lacp": "active",
"bond_mode": "l2-src-dst-hash",
"tag": 654,
"vlan_mode": "trunk",
"ip6_address": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
"external_ids": {"extid1key": "extid1value"},
"bond_options": {"key1": "value1"},
"mac": "01:23:45:67:89:ab",
"other_config": {"cfg-1key": "cfg1val"},
"bond_active_slave": "null",
"ip6_address_secondary": ["01:23:45:67:89:ab"],
"vlan_options": {"opt1key": "opt2val"},
"ip4_address": "192.168.0.1",
"admin": "up"
}
}
```

### Description ###

#### Update Port ####

1. Execute a PUT request over /rest/v1/system/ports/Port1 with the following data and verify if the HTTP response is 200 OK

```
{
"configuration": {
"name": "Port1",
"interfaces": ["/rest/v1/system/interfaces/1", "/rest/v1/system/interfaces/2"],
"trunks": [400],
"ip4_address_secondary": ["192.168.0.2"],
"lacp": "passive",
"bond_mode": "l3-src-dst-hash",
"tag": 600,
"vlan_mode": "access",
"ip6_address": "2001:0db8:85a3:0000:0000:8a2e:0370:8225",
"external_ids": {"extid2key": "extid2value"},
"bond_options": {"key2": "value2"},
"mac": "01:23:45:63:90:ab",
"other_config": {"cfg-2key": "cfg2val"},
"bond_active_slave": "slave1",
"ip6_address_secondary": ["2001:0db8:85a3:0000:0000:8a2e:0370:7224"],
"vlan_options": {"opt1key": "opt3val"},
"ip4_address": "192.168.0.2",
"admin": "up"
},
"referenced_by": [{"uri":"/rest/v1/system/bridges/bridge_normal"}]
}
```

2. Execute a GET request over /rest/v1/system/ports/Port1 and verify if the response is 200 OK
3. Verify if the configuration response data from the step 2 is the same that the configuration data from step 1

#### Update Port name ####

1. Set the name of the port to "Port2"
```
"name": "Port2"
```
2. Execute a PUT request over /rest/v1/system/ports/Port1
3. Verify if the HTTP response is 200 OK
4. Execute a GET request over /rest/v1/system/ports/Port1 and verify if the response is 200 OK
5. Verify if the port is still named "Port1"

#### Data validation ####

##### Data Types Validation #####

###### Invalid string type ######

1. Set the "ip4_address" value to:
```
"ip4_address": 192
```
2. Execute a PUT request over /rest/v1/system/ports/Port1 with the Port data changed
3. Verify if the HTTP response is 400 BAD REQUEST

###### Valid string type ######

1. Set the "ip4_address" value to:
```
"ip4_address": "192.168.0.1"
```
2. Execute a PUT request over /rest/v1/system/ports/Port1 with the Port data changed
3. Verify if the HTTP response is 200 OK

###### Invalid integer type ######

1. Set the "tag" value to:
```
"tag": "675"
```
2. Execute a PUT request over /rest/v1/system/ports/Port1 with the Port data changed
3. Verify if the HTTP response is 400 BAD REQUEST

###### Valid integer type ######

1. Set the "tag" value to:
```
"tag": 675
```
2. Execute a PUT request over /rest/v1/system/ports/Port1 with the Port data changed
2. Verify if the HTTP response is 200 OK

###### Invalid array type ######

1. Set the "trunks" value to:
```
"trunks": "654,675"
```
2. Execute a PUT request over /rest/v1/system/ports/Port1 with the Port data changed
3. Verify if the HTTP response is 400 BAD REQUEST

###### Valid array type ######

1. Set the "trunks" value to:
```
"trunks": [654,675]
```
2. Execute a PUT request over /rest/v1/system/ports/Port1 with the Port data changed
3. Verify if the HTTP response is 200 OK

##### Ranges Validation #####


###### Invalid range for string type ######

1. Set the "ip4_address" value to:
```
"ip4_address": "175.167.134.123/248"
```
2. Execute a PUT request over /rest/v1/system/ports/Port1 with the Port data changed
3. Verify if the HTTP response is 400 BAD REQUEST

###### Valid range for string type ######

1. Set the "ip4_address" value to:
```
"ip4_address": "175.167.134.123/24"
```
2. Execute a PUT request over /rest/v1/system/ports/Port1 with the Port data changed
3. Verify if the HTTP response is 200 OK

###### Invalid range for integer type ######

1. Set the "tag" value to:
```
"tag": 4095
```
2. Execute a PUT request over /rest/v1/system/ports/Port1 with the Port data changed
3. Verify if the HTTP response is 400 BAD REQUEST

###### Valid range for integer type ######

1. Set the "tag" value to:
```
"tag": 675
```
2. Execute a PUT request over /rest/v1/system/ports/Port1 with the Port data changed
3. Verify if the HTTP response is 200 OK

###### Invalid range for array type ######

1. Change the "interfaces" value to:
```
"interfaces": [ "/rest/v1/system/interfaces/1",
"/rest/v1/system/interfaces/2",
"/rest/v1/system/interfaces/3",
"/rest/v1/system/interfaces/4",
"/rest/v1/system/interfaces/5",
"/rest/v1/system/interfaces/6",
"/rest/v1/system/interfaces/7",
"/rest/v1/system/interfaces/8",
"/rest/v1/system/interfaces/9",
"/rest/v1/system/interfaces/10" ]
```
2. Execute a PUT request over /rest/v1/system/ports/Port1 with the Port data changed
3. Verify if the HTTP response is 400 BAD REQUEST

###### Valid range for array type ######

1. Change the "interfaces" value to:
```
"interfaces": ["/rest/v1/system/interfaces/1"]
```
2. Execute a PUT request over /rest/v1/system/ports/Port1 with the Port data changed
3. Verify if the HTTP response is 200 OK

##### Allowed Data Values Validation #####


###### Invalid data value ######

1. Change the "vlan_mode" value to:
```
"vlan_mode": "invalid_value"
```
2. Execute a PUT request over /rest/v1/system/ports/Port1 with the Port data changed
3. Verify if the HTTP response is 400 BAD REQUEST

###### Valid data value ######

1. Change the "vlan_mode" value to:
```
"vlan_mode": "access"
```
2. Execute a PUT request over /rest/v1/system/ports/Port1 with the Port data changed
3. Verify if the HTTP response is 200 OK

##### Missing attribute Validation #####

1. Execute a PUT request over /rest/v1/system/ports/Port1 without "vlan_mode" attribute
2. Verify if the HTTP Response is 400 BAD REQUEST
3. Execute a PUT request over /rest/v1/system/ports/Port1 with all attributes:
4. Verify if the HTTP Response is 200 OK

##### Unknown Attribute Validation #####

1.  Execute a PUT request over /rest/v1/system/ports/Port1 with an unknown attribute:
```
"unknown_attribute": "unknown_value"
```
2. Verify if the HTTP Response is 400 BAD REQUEST
3. Execute a PUT request over /rest/v1/system/ports/Port1 with all allowed attributes
4. Verify if the HTTP Response is 200 OK

##### Malformed Json Validation #####

1. Execute a PUT request over /rest/v1/system/ports/Port1 with a semi-colon at the end of the json data
2. Verify if the HTTP Response is 400 BAD REQUEST
3. Execute a PUT request over /rest/v1/system/ports/Port1 without the semi-colon at the end of the json data
4. Verify if the HTTP Response is 200 OK

### Test Result Criteria ###
#### Test Pass Criteria ####

The test is considered passed when updating a port

- The HTTP response is 200 OK
- When executing a GET request over /rest/v1/system/ports/Port1 the HTTP response is 200 OK
- When the configuration data posted is the same that the retrieved port

The test is considered passed when updating a port with the same that another port

- The HTTP response is 400 BAD REQUEST

The test is considered passed when updating a port with a valid string type

- The HTTP response is 200 OK

The test is considered passed when updating a port with an invalid string type

- The HTTP response is 400 BAD REQUEST

The test is considered passed when updating a port with a valid integer type

- The HTTP response is 200 OK

The test is considered passed when updating a port with an invalid array type

- The HTTP response is 400 BAD REQUEST

The test is considered passed when updating a port with valid array type

- The HTTP response is 200 OK

The test is considered passed when updating a port with an invalid value on attribute

- The HTTP response is 400 BAD REQUEST

The test is considered passed when updating a port with a valid value on attribute

- The HTTP response is 200 OK

The test is considered passed when updating a port with a missing attribute

- The HTTP response is 400 BAD REQUEST

The test is considered passed when updating a port with with all attributes

- The HTTP response is 200 OK

The test is considered passed when updating a port with an unknown attribute

- The HTTP response is 400 BAD REQUEST

The test is considered passed when updating a port with all allowed attributes

- The HTTP response is 200 OK

The test is considered passed when updating a port with malformed json data

- The HTTP response is 400 BAD REQUEST

The test is considered passed when updating a port with well-formed json data

- The HTTP response is 200 OK

#### Test Fail Criteria ####

The test is considered failed when updating a port

- The HTTP response is not equal to 200 OK
- When executing a GET request over /rest/v1/system/ports/Port1 the HTTP response is not equal to 200 OK
- When the configuration data posted is not the same that the retrieved port

The test is considered failed when updating a port with the same that another port

- The HTTP response is not equal 400 BAD REQUEST

The test is considered failed when updating a port with a valid string type

- The HTTP response is not equal 200 OK

The test is considered failed when updating a port with an invalid string type

- The HTTP response is not equal 400 BAD REQUEST

The test is considered failed when updating a port with a valid integer type

- The HTTP response is not equal 200 OK

The test is considered failed when updating a port with an invalid array type

- The HTTP response is not equal 400 BAD REQUEST

The test is considered failed when updating a port with valid array type

- The HTTP response is not equal 200 OK

The test is considered failed when updating a port with an invalid value on attribute

- The HTTP response is not equal 400 BAD REQUEST

The test is considered failed when updating a port with a valid value on attribute

- The HTTP response is not equal 200 OK

The test is considered failed when updating a port with a missing attribute

- The HTTP response is not equal 400 BAD REQUEST

The test is considered failed when updating a port with with all attributes

- The HTTP response is not equal 200 OK

The test is considered failed when updating a port with an unknown attribute

- The HTTP response is not equal 400 BAD REQUEST

The test is considered failed when updating a port with all allowed attributes

- The HTTP response is not equal 200 OK

The test is considered failed when updating a port with malformed json data

- The HTTP response is not equal 400 BAD REQUEST

The test is considered failed when updating a port with well-formed json data

- The HTTP response is not equal 200 OK


## Delete a Port ##

### Objective ###

The tests cases verifies if an existent port is deleted.

### Requirements ###

Port "Port1" must exist

### Setup ###
#### Topology Diagram ####
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

#### Test Setup ####

** Switch 1 ** has a Port with name Port1 with the following configuration data

```
{
"configuration": {
"name": "Port1",
"interfaces": ["/rest/v1/system/interfaces/1"],
"trunks": [413],
"ip4_address_secondary": ["192.168.0.1"],
"lacp": "active",
"bond_mode": "l2-src-dst-hash",
"tag": 654,
"vlan_mode": "trunk",
"ip6_address": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
"external_ids": {"extid1key": "extid1value"},
"bond_options": {"key1": "value1"},
"mac": "01:23:45:67:89:ab",
"other_config": {"cfg-1key": "cfg1val"},
"bond_active_slave": "null",
"ip6_address_secondary": ["01:23:45:67:89:ab"],
"vlan_options": {"opt1key": "opt2val"},
"ip4_address": "192.168.0.1",
"admin": "up"
}
}
```

### Description ###

1. Execute DELETE request over /rest/v1/system/ports/Port1 and verify if the HTTP response is 204 NOT CONTENT
2. Execute GET request over /rest/v1/system/ports and verify if port is being deleted from Port list.
3. Execute GET request over /rest/v1/ports/system/Port1 and verify if the HTTP response is 404 NOT FOUND.
4. Execute a DELETE request over /rest/v1/system/ports/Port2 and the HTTP response is 404 NOT FOUND

### Test Result Criteria ###

#### Test Pass Criteria ####

The test is considered passed when deleting an existent Port:

- The HTTP response is 204 NOT CONTENT
- There is not URI "/rest/v1/system/ports/Port1" in port list returned from /rest/v1/system/ports URI
- When doing a GET request over "/rest/v1/system/ports/Port1" the HTTP response is 404 NOT FOUND

The test case is considered passed when deleting a non-existent Port:

- The HTTP response is 404 NOT FOUND

#### Test Fail Criteria ####

The test case is considered failed when deleting an existent Port:

- The HTTP response is not equal to 204 NOT CONTENT
- When doing a GET request to "/rest/v1/system/ports" the port "Port1" is at the Ports URI list
- When doing a GET request over "/rest/v1/system/ports/Port1" the HTTP response is not equalt to 404 NOT FOUND

The test case is considered failed when deleting a non-existent Port:

- The HTTP response is not equal to 404 NOT FOUND
System Resource: REST Test Cases
=============================

## Query System OPTIONS ##

### Objective ###
The tests case queries System's available OPTIONS and verifies they are the expected ones. 

### Requirements ###
System resource must exist

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

1. Execute OPTIONS request over /rest/v1/system
2. Verify that 'allow' options in header correspond to ["DELETE", "GET", "OPTIONS", "POST", "PUT"]
3. Verify that 'access-control-allow-methods' options in header corresponds to ["DELETE", "GET", "OPTIONS", "POST", "PUT"]

### Test Result Criteria ###
#### Test Pass Criteria ####

The test is considered passed when: 

- 'allow' options correspond to ["DELETE", "GET", "OPTIONS", "POST", "PUT"]
- 'access-control-allow-methods' options correspond to ["DELETE", "GET", "OPTIONS", "POST", "PUT"]

#### Test Fail Criteria ####

The test case is considered failed when:

- 'allow' options does not correspond to ["DELETE", "GET", "OPTIONS", "POST", "PUT"]
- 'access-control-allow-methods' options does not correspond to ["DELETE", "GET", "OPTIONS", "POST", "PUT"]


## Query System resource ##

### Objective ###
The test case queries System resource and verifies that well-formed data is returned. 

### Requirements ###
System resource must exist

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

1. Execute GET request over /rest/v1/system and verify returned data

### Test Result Criteria ###
#### Test Pass Criteria ####

The test is considered passed when: 

- A well-formed, non-empty JSON is returned by the GET request

#### Test Fail Criteria ####

The test case is considered failed when:

- The response JSON is malformed
- The response JSON is empty


## Modify System resource ##

### Objective ###
The tests case modifies the resource System and verifies modification was executed. 

### Requirements ###
System resource must exist

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

1. Execute GET request over /rest/v1/system to obtain initial data
2. In the initial data from GET, set the configuration attributes to the following values:

    - 'hostname' to 'test'
    - 'dns_servers' to "8.8.8.8"
    - 'asset_tag_number' to "tag"
    - 'other_config' to {"key1": "value1"}
    - 'external_ids' to {"id1": "value1"}

3. Execute PUT request over /rest/v1/system with the modified data
4. Execute a new GET request to obtain post-PUT data
5. Verify post-PUT data matches PUT request data

### Test Result Criteria ###
#### Test Pass Criteria ####

The test is considered passed when: 

- PUT request data matches data returned in GET request executed post-PUT 

#### Test Fail Criteria ####

The test case is considered failed when:

- PUT request data does not match data returned in GET request executed post-PUT 










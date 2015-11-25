# Loopback Interface feature Test Cases
<!-- TOC depth:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Loopback Interface feature Test Cases](#loopback-interface-feature-test-cases)
	- [Verify L3 reachability of Loopback interface  ##](#verify-l3-reachability-of-loopback-interface-)
		- [Objective ###](#objective-)
		- [Requirements ###](#requirements-)
		- [Setup ###](#setup-)
			- [Topology Diagram ####](#topology-diagram-)
			- [Test Setup ####](#test-setup-)
		- [Description ###](#description-)
		- [Test Result Criteria ###](#test-result-criteria-)
			- [Test Pass Criteria ####](#test-pass-criteria-)
			- [Test Fail Criteria ####](#test-fail-criteria-)
<!-- /TOC -->

##  Verify L3 reachability of Loopback interface  ##

### Objective ###
Verify the reachability of IP address set on sub-interface

### Requirements ###
The requirements for this test case are:
 - openswitch
 - host

### Setup ###
Connect openswitch interface 1 to eth0 on host

#### Topology Diagram ####

#### Test Setup ####

### Description ###
 - Assign ip 192.168.1.2/24 to eth0 on host
 - Create loopback interface 1
 - Assign ip 192.168.1.1/24 to loopback interface 1
 - Ping 192.168.1.1 from host

### Test Result Criteria ###
Ping result

#### Test Pass Criteria ####
Ping succeeds

#### Test Fail Criteria ####
Ping fails


<!--  See the https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet for additional information about markdown text.
Here are a few suggestions in regards to style and grammar:
* Use active voice. With active voice, the subject is the doer of the action. Tell the reader what
to do by using the imperative mood, for example, Press Enter to view the next screen. See https://en.wikipedia.org/wiki/Active_voice for more information about the active voice. 
* Use present tense. See https://en.wikipedia.org/wiki/Present_tense for more information about using the present tense. 
* The subject is the test case. Explain the actions as if the "test case" is doing them. For example, "Test case configures the IPv4 address on one of the switch interfaces". Avoid the use of first (I) or second person. Explain the instructions in context of the test case doing them. 
* See https://en.wikipedia.org/wiki/Wikipedia%3aManual_of_Style for an online style guide.
 -->

#Log-rotate Test Cases


<!--Provide the name of the grouping of commands, for example, LLDP commands-->
##Contents
[TOC]
##  1.0 Test cases to verify log-rotate configuration ##

### Objective ###
The Objective of these test cases is to configure various log-rotate parameters and to verify the expected behavior for valid and error scenarios.

### Requirements ###
The requirements for this test case are:

 - TFTP Server (tftpd-hpa)

### Setup ###
#### Topology Diagram ####
<pre>





                                                           +-------------------+
              +------------------+                         | Linux workstation |
              |                  |eth0                eth0 |+-----------------+|
              |  AS5712 switch   |<----+         +-------->||TFTP Server      ||
              |                  |     |         |         |+-----------------+|
              +------------------+     |         |         +-------------------+
                                       |         |
                                       v         v
                                 +---------------------+
                                 | port 1      port 2  |
                                 |                     |
                                 |      Switch         |
                                 |                     |
                                 +---------------------+</pre>

###1.01 To verify default configuration of log-rotate ###

#### Description ####
With no logrotate configuration in DB, display log-rotate configuration with the ‘show’ command.

Command : 'root# show logrotate'

#### Test Result Criteria ####
#### Test Pass Criteria ####
The default values should be displayed.
```bash
    Logrotate configurations :
    Period            : daily
    Maxsize           : 10MB
```

#### Test Fail Criteria ####
If default values are not displayed or if the values are different, then the test case fails.


###1.02 To verify OVSDB is updated properly for period configuration ###

#### Description ####
Configure the logrotate period and check that the database is updated properly

Command: `root# logrotate period hourly`

Values in OVSDB shall be verified with the following command,
```bash
Show logrotate
Ovs-vsctl list Open-vSwitch
```

#### Test Result Criteria ####
#### Test Pass Criteria ####
Configured period value should be updated in OVSDB. 

#### Test Fail Criteria ####
Test case fails if configured value is not found in OVSDB or updated with incorrect value.

### 1.03 To verify period configuration cli is updated in show running config ###
#### Description ####
Configure logrotate period with a value different from default value.

Command:

`root# logrotate period hourly`

Command to verify:

'show running-config'

#### Test Result Criteria ####
#### Test Pass Criteria ####
Configured period value should be updated in OVDDB and command should be updated in running config.
#### Test Fail Criteria ####
Test case fails, if configured cli is not part of 'show running config'

### 1.04 To verify OVSDB is updated properly for maxsize configuration ###
#### Description ####
Configure logrotate maxsize and check OVSDB is updated properly

Command:

'root# logrotate maxsize 20'

Values in OVSDB shall be verified with the following command,

```bash
Show logrotate
Ovs-vsctl list Open-vSwitch
```

#### Test Result Criteria ####
#### Test Pass Criteria ####
Configured maxsize value should be updated in OVSDB.

#### Test Fail Criteria ####
Test case fails if configured value is not found in OVSDB or updated with incorrect value.

### 1.05 To verify maxsize configuration cli is updated in show running config ###
#### Description ####
Configure logrotate maxsize with a value different from default value.

Command:

`root# logrotate period maxsize 20'

Command to verify:

`show running-config`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Configured maxsize value should be updated in OVDDB and command should be updated in running config.
#### Test Fail Criteria ####
Test case fails, if configured cli is not part of 'show running config'

### 1.06 To verify logrotate maxsize cli for wrong values ###
#### Description ####
Enter wrong values for logrotate maxsize.

Command:

`root# logrotate maxsize 250`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Testcase result is success if proper error messages are thrown.

#### Test Fail Criteria ####
Testcase result is fail if user is able to configure.


### 1.07 To verify OVSDB is updated properly for target configuration ###
#### Description ####
Configure logrotate target and check OVSDB is updated properly

Command:

`root# logrotate target tftp://1.1.1.1`

Values in OVSDB shall be verified with the following command,

```bash
Show logrotate
Ovs-vsctl list Open-vSwitch
Show running-config
```
#### Test Result Criteria ####
#### Test Pass Criteria ####
Configured target value should be updated in OVSDB and command should be updated in running config.

#### Test Fail Criteria ####
Test case fails if configured value is not found in OVSDB or updated with incorrect value.
Test case also fails if cli is not part of show running config

### 1.08 To verify logrotate target cli for invalid or not supported protocol ###
#### Description ####
Configure logrotate target with invalid or not supported protocol.

Command:

`root# logrotate target scp://1.1.1.1`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Test case result is success if configuration fails saying "Only TFTP protocol is supported".
#### Test Fail Criteria ####
Test case fails, if user could successfully configure.


### 1.09 To verify logrotate target cli for invalid IPv4 address ###
#### Description ####
Configure logrotate target with invalid IPv4 address.

Command:

`root# logrotate target tftp://1.1`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Test case result is success if configuration fails saying "Invalid IPv4 or IPv6 address".
#### Test Fail Criteria ####
Test case fails, if user could successfully configure.


### 1.10 To verify logrotate target cli for broadcast IPv4 address ###
#### Description ####
Configure logrotate target with broadcast IPv4 address.

Command:

`root# logrotate target tftp://255.255.255.255`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Test case result is success if configuration fails saying "IPv4: broadcast, multicast and loopback addresses are not allowed".
#### Test Fail Criteria ####
Test case fails, if user could successfully configure.


### 1.11 To verify logrotate target cli for multicast IPv4 address ###
#### Description ####
Configure logrotate target with multicast IPv4 address.

Command:

`root# logrotate target tftp://224.10.0.1`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Test case result is success if configuration fails saying "IPv4: broadcast, multicast and loopback addresses are not allowed".
#### Test Fail Criteria ####
Test case fails, if user could successfully configure.


### 1.12 To verify logrotate target cli for loopback IPv4 address ###
#### Description ####
Configure logrotate target with loopback IPv4 address.

Command:

`root# logrotate target tftp://127.0.0.1`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Test case result is success if configuration fails saying "IPv4: broadcast, multicast and loopback addresses are not allowed".
#### Test Fail Criteria ####
Test case fails, if user could successfully configure.


### 1.13 To verify logrotate target cli for invalid IPv6 address ###
#### Description ####
Configure logrotate target with invalid IPv6 address.

Command:

`root# logrotate target tftp://22:22`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Test case result is success if configuration fails saying "Invalid IPv4 or IPv6 address".
#### Test Fail Criteria ####
Test case fails, if user could successfully configure.


### 1.14 To verify logrotate target cli for multicast IPv6 address ###
#### Description ####
Configure logrotate target with multicast IPv6 address.

Command:

`root# logrotate target tftp://ff02::1:3`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Test case result is success if configuration fails saying "IPv6: Multicast and loopback addresses are not allowed".
#### Test Fail Criteria ####
Test case fails, if user could successfully configure.


### 1.15 To verify logrotate target cli for loopback IPv6 address ###
#### Description ####
Configure logrotate target with loopback IPv6 address.

Command:

`root# logrotate target tftp://::1`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Test case result is success if configuration fails saying "IPv6: Multicast and loopback addresses are not allowed".
#### Test Fail Criteria ####
Test case fails, if user could successfully configure.

##  2.0 Test case to verify log-rotation and remote transfer ##

### Objective ###
The objective of these test cases is to verify log-rotation in the local host and to verify the transfer of rotated logs to remote host.

### Requirements ###
The requirements for this test case are:

 - TFTP Server (tftpd-hpa)

### Setup ###
#### Topology Diagram ####

                                                           +-------------------+
              +------------------+                         | Linux workstation |
              |                  |eth0                eth0 |+-----------------+|
              |  AS5712 switch   |<----+         +-------->||TFTP Server      ||
              |                  |     |         |         |+-----------------+|
              +------------------+     |         |         +-------------------+
                                       |         |
                                       v         v
                                 +---------------------+
                                 | port 1      port 2  |
                                 |                     |
                                 |      Switch         |
                                 |                     |
                                 +---------------------+</pre>


#### Test Setup ####
### 2.01 To verify log-rotate for period with default configuration  ###
#### Description ####
With default config, change the date to simulate daily log-rotate locally.

Command:

`date --set='2015-06-26 12:21:42'`

Command to verify:

`ls –lhrt /var/log/`


#### Test Result Criteria ####
#### Test Pass Criteria ####
Test case result is success, if log files are rotated ,compressed and stored locally in /var/log/ with appropriate time extension with hourly granularity
#### Test Fail Criteria ####
Test case fails, if any one of the above condition (rotation,compression and file with appropriate time extension) is not met

### 2.02 To verify log-rotate for period with non-default configuration ###
#### Description ####
Change the period config to 'hourly' and change the date to simulate hourly log-rotate locally.

Command:

`date --set='2015-06-26 12:21:42'`

Command to verify:

`ls –lhrt /var/log/`

#### Test Result Criteria ####
<!--    Explain the criteria that clearly identifies under whch conditions would the test be considered as pass or fail. Also if the test case can exit with any other result, explain that result and similarly the relevant criteria. -->
#### Test Pass Criteria ####
Test case result is success, if log files are rotated ,compressed and stored locally in /var/log/ with appropriate time extension with hourly granularity
#### Test Fail Criteria ####
Test case fails, if any one of the above condition (rotation,compression and file with appropriate time extension) is not met

### 2.03 To verify log-rotate for period with remote host ###
#### Description ####
Repeat test 2.02 for remote transfer by configuring logrotate target.

Command:
```bash
root# logrotate target tftp://172.17.42.1
date --set='2015-06-26 12:21:42
```
Command to verify:
```bash
ls –lhrt /var/log/ (in local host)
ls (in remote host tftp path)
```

#### Test Result Criteria ####
#### Test Pass Criteria ####
Testcase result is success if log files are rotated ,compressed and stored locally in /var/log/ with appropriate time extension with hourly granularity and also transferred to remote host.
#### Test Fail Criteria ####
Test case fails, if any one of the above condition (rotation, compression, file with appropriate time extension and remote transfer) is not met.

### 2.04 To verify log-rotate maxsize with default configuration ###
#### Description ####
With default config, copy a file of size greater than 10MB to /var/log/messages and change the date to simulate hourly logrotate locally.

Command:

`date --set='2015-06-26 12:21:42'`

Command to verify:

`ls –lhrt /var/log/`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Test case result is success, if log files are rotated ,compressed and stored locally in /var/log/ with appropriate time extension with hourly granularity
#### Test Fail Criteria ####
Test case fails, if any one of the above condition (rotation,compression and file with appropriate time extension) is not met.

### 2.05 To verify log-rotate maxsize with non-default configuration ###
#### Description ####
Change the logrotate maxsize to 20 MB, copy a file of size greater than 20MB to /var/log/messages and change the date to simulate hourly logrotate locally.

Command:

`date --set='2015-06-26 12:21:42'`

Command to verify:

`ls –lhrt /var/log/`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Test case result is success, if log files are rotated ,compressed and stored locally in /var/log/ with appropriate time extension with hourly granularity.
#### Test Fail Criteria ####
Test case fails, if any one of the above condition (rotation,compression and file with appropriate time extension) is not met.


### 2.06 To verify log-rotate maxsize with remote host ###
#### Description ####
Repeat test 2.05 for remote transfer by configuring logrotate target.

Command:
```bash
root# logrotate target tftp://172.17.42.1
date --set='2015-06-26 12:21:42'
```
Command to verify:
```bash
ls –lhrt /var/log/ (in local host)
ls (in remote host tftp path)
```

#### Test Result Criteria ####
#### Test Pass Criteria ####
Testcase result is success if log files are rotated ,compressed and stored locally in /var/log/ with appropriate time extension with hourly granularity and also transferred to remote host.
#### Test Fail Criteria ####
Test case fails, if any one of the above condition (rotation, compression, file with appropriate time extension and remote transfer) is not met.

### 2.07 To verify log-rotate remote transfer with non-reachable IPv4 address ###
#### Description ####
Enter a non-reachable IP in logrotate target.

Command:

`root# logrotate target tftp://1.1.1.1`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Test case result is success if log_rotate script timeout after some time without waiting indefinitely.
#### Test Fail Criteria ####
Test case fails, if log_rotate script waits indefinitely.

### 2.08 To verify log-rotate remote transfer with IPv6 address ###
#### Description ####
Repeat test 2.05 for remote transfer with valid IPv6 address in logrotate target.

Command:

`root# logrotate target tftp://2001:db8:0:1::128`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Testcase result is success if log files are rotated ,compressed and stored locally in /var/log/ with appropriate time extension with hourly granularity and also transferred to remote host.
#### Test Fail Criteria ####
Test case fails, if any one of the above condition (rotation, compression, file with appropriate time extension and remote transfer) is not met.


### 2.09 To verify log-rotate remote transfer with non-reachable IPv6 address ###
#### Description ####
Enter a non-reachable IPv6 in logrotate target.

Command:

`root# logrotate target tftp://2001:db8:0:1::fe`

#### Test Result Criteria ####
#### Test Pass Criteria ####
Test case result is success if log_rotate script timeout after some time without waiting indefinitely.
#### Test Fail Criteria ####
Test case fails, if log_rotate script waits indefinitely.
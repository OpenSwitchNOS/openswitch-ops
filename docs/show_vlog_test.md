# Component Test Cases for Show VLOG

## Contents
- [1.Positive Test Cases](#1-positive-test-cases)
    - [1.1 List the supported features for show vlog](#list-the
        -supported-features-for-show-vlog)
    - [1.2 Running show vlog feature](#running-show-vlog-feature)
    - [1.3 Running show vlog](#running-show-vlog)
    - [1.4 Basic vlog Configuration for feature](#basic-vlog
        -configuration-for-feature)
    - [1.5 Basic vlog Configuration for daemon](#basic-vlog-configuration
        -for-daemon)
- [2.Negative Test Cases](#2-negative-test-cases)
    - [2.1 Show vlog for invalid daemon](#show-vlog-for-invalid-daemon)
    - [2.2 Show vlog for invalid feature](#show-vlog-for-invalid-feature)
    - [2.3 Show vlog for invalid subcommand](#show-vlog-for-invalid-subcommand)
    - [2.4 Vlog configuration for invalid feature](#vlog-configuratin-for
        -invalid-feature)
    - [2.5 Vlog configuration for invalid daemon](#vlog-configuration-for
        -invalid-daemon)
    - [2.6 Vlog configuration for invalid destination](#vlog-configuration-for
        -invalid-destination)
    - [2.7 Vlog configuration for invalid log level](#vlog-configuration-for
        -invalid-log-level)

# 1.Positive Test Cases
## 1.1 List the supported features for show vlog

### Objective
"show vlog list" command is able to display list of supported features and descriptions.

### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology Diagram

```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```

#### Test Setup
Standalone Switch
### Description
step:
- Run "show vlog list" on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
"show vlog list" command gives list of supported features with their description.

#### Test fail criteria
"show vlog list" command gives "show vlog list failed".

## 1.2 Running show vlog feature
### Objective
Capture the vlog severity level of syslog and file destinations for feature.

### Requirements
Ensure that feature related daemon are running. Feature related daemon are available in ops_featuremapping.yaml file

### Setup
####  Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test setup
### Description
Capture vlog log level for feature using 'show vlog feature <feature_name>'

### Test result criteria
#### Test pass criteria
`show vlog feature <feature_name>` diaplays log-level of syslog and file for feature.
#### Test fail criteria
vtysh crash or show vlog feature failed.

## 1.3  Running show vlog
### Objective
`show vlog` command to display the list of features with their log levels of file and syslog destinations.

## Requirements.
Ensure that features related daemons are running. Features related daemons are available in ops_featuremapping.yaml file

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test setup
### Description
Caapture the log levels of supported features.
### Test result criteria
#### Test pass criteria
'show vlog' command displays the features corresponding daemons log levels on the console.
#### Test fail criteria
 vtysh crash or show vlog failed.

## Basic vlog Configuration for feature
### Objective
Configure the log level and destination for feature.

### Requirements
Ensure that feature related daemon are running .Feature related daemon are available in ops_featuremapping.yaml

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test setup
### Description
Configure the basic log level for feature using command `vlog feature <feature_name> syslog dbg`
on console.

### Test result criteria
#### Test pass criteria
User cant see configuration changes on configuration node .using `show vlog feature <feature_name>` to obtain configuration changes on Enable mode.
#### Test fail criteria
vtysh crash or vlog configuration failed.

## 1.5 Basic vlog Configuration for daemon
### Objective
Configure the log level of syslog and file destinations for daemon.

### Requirement
Ensure that daemon running on switch.
### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test setup
### Description
Using `vlog daemon <daemon_name> file info` on configuration mode to configure the log level of syslog or file destination for daemon .

### Test result criteria
#### Test pass criteria
User cant see configuration changes on configuration node .using `show vlog daemon <daemon_name>` to obtain configuration changes on Enable mode.
#### Test fail criteria
vtysh crash or vlog configuration failed.

# 2.Negative Test Cases
## 2.1 Show vlog for invalid daemon.
### Objective
This test case verifies the behaviour of `show vlog daemon <daemon_name>` CLI command.
when we pass Invalid daemon_name as parameter to CLI.

### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test setup
### Description
Passing Invalid daemon_name as argument to `show vlog daemon <daemon_name>` CLI command.

### Test result criteria
#### Test pass criteria
`show vlog daemon daemon_name` CLI Command results "show vlog for invalid daemon failed".
#### Test fail criteria
vtysh crash or Improper message.

## 2.2 Show vlog for invalid feature
### Objective
This test case verifies the behaviour of `show vlog feature <feature_name>` CLI command.
when we pass Invalid feature_name  as paramter  to CLI.

### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test setup
### Description
Passing Invalid feature name as argument to `show vlog feature <feature_name> CLI command.

### Test result criteria
#### Test pass criteria
`show vlog feature <feature_name>` CLI Command results "show vlog for invalid feature failed".
#### Test fail criteria
vtysh crash or Improper message.

## 2.3 Show vlog for invalid subcommand
### Objective
This test case verifies the behviour of `show vlog <name>` CLI command.
when we pass Invalid subcommand as parameter to CLI.

### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test setup
### Description
Passing Invalid subcommand as argument to `show vlog <name>` CLI command.

### Test result criteria
#### Test pass criteria
`show vlog <name>` CLI command results "show vlog for invalid subcommand failed"
#### Test fail criteria
vtysh crash or Improper message.


## 2.4  Vlog configuration for invalid feature
### Objective
This test case verifies the behaviour of `vlog feature <feature_name> syslog dbg` when we pass the feature name is invalid.

### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test setup
### Description
Passing Invalid feature_name as argument to configure the log level of file and syslog destination using `vlog feature <feature_name> <destination> <log-level>` CLI command on configuration mode.

### Test result criteria
#### Test pass criteria
`vlog feature <feature_name> syslog dbg` displays "config vlog for invalid feature failed".

#### Test fail criteria
vtysh crash or Improper message.

##2.5 Vlog configuration for invalid daemon
### Objective
This test case verifies the behaviour of `vlog daemon <daemon_name> file warn` when we pass the Invalid daemon_name passed as paramter to CLI on configuration mode.

### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test setup
### Description
Passing Invalid daemon_name as argument to `vlog daemon <daemon_name> <destination> <log-level>`

### Test result criteria
#### Test pass criteria
`vlog daemon <daemon_name> file warn ` results "config vlog for invalid daemon failed".

#### Test fail criteria
vtysh crash or Improper message.

##2.6 Vlog configuration for invalid destination
### Objective
This test case verifies the behaviour of `vlog feature lacp <destination_name> dbg` .when the destimation as invalid destination to CLI.
### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test setup
### Description
Passig Invalid destination_name as argument to `vlog (feature|daemon) <name> <destination_name> <log-level>` CLI command.
### Test result criteria
#### Test pass criteria
`vlog (daemon | feature) <name> <destination_name> <log-level>` results "config vlog for invalid destination failed".

#### Test fail criteria
vtysh crash or Improper message.

##2.7 Vlog configuration for invalid Log level
### Objective
This test case verifies the behaviour of `vlog (daemon | feature) <name> <destination> <log-level_name>`.when we pass the invalid log level_name as parametr  to CLI.
### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test setup
### Description
Passig Invalid log level_name as argument to `vlog (feature|daemon) <name> <destination> <log-level_name>` CLI command.
### Test result criteria
#### Test pass criteria
`vlog (daemon | feature) <name> <destination> <log-level_name>` results "config vlog for invalid dlog level failed".

#### Test fail criteria
vtysh crash or Improper message.

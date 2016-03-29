# Syslog Remote Configuration Test Cases

## Contents
- [Logging CLI Configuration](#logging-cli-configuration)
- [Logging Configuration displayed in show running-config](#logging-configuration-displayed-in-show-running-config)
- [Syslog messages are received in remote syslog servers](#syslog-messages-are-received-in-remote-syslog-servers)

##  Logging CLI Configuration

### Objective
Objective of this test case is to verify that the logging cli configurations results in proper update of the rsyslog remote configuration file.

### Requirements
A switch running OpenSwitch is required for this test case.

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
Standalone switch

### Description
*Steps*
1. Get into configuration terminal of the switch.
2. Execute the command `logging 10.0.0.2 udp 514 severity info`.
3. Get into the bash shell.
4. Verify that the file `/etc/rsyslog.remote.conf` contains the line `info.* @10.0.0.2:514`.

### Test Result Criteria
#### Test Pass Criteria
Logging configuration is correctly stored in the `/etc/rsyslog.remote.conf` file.

#### Test Fail Criteria
Logging configuration is not found in `/etc/rsyslog.remote.conf` file.

##  Logging Configuration displayed in show running-config
### Objective
Objective of this test case is to verify that the logging cli configurations changes are displayed in show running-config

### Requirements
A switch running OpenSwitch is required for this test case.

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
Standalone switch

### Description
*Steps*
1. Get into configuration terminal of the switch
2. Execute the command `logging 10.0.0.2 udp 514 severity info`.
3. Execute `end` to go back to vtysh shell.
4. Execute `show running`.
5. Verify that the changes are reflected in the show running output.

### Test Result Criteria
#### Test Pass Criteria
Logging configuration are visible in the show running-config output.

#### Test Fail Criteria
Logging configuration not found in the show running-config output.

##  Syslog messages are received in remote syslog servers
### Objective
Objective of this test case is to verify that the syslog message are received in the remote syslog server.

### Requirements
1. A switch running OpenSwitch is required for this test case.
2. A Host running syslog server

### Setup
#### Topology Diagram
```ditaa
 +----------+        +--------+
 |          |        |        |
 |  Switch  <-------->  Host  |
 |          |        |        |
 +----------+        +--------+

```
#### Test Setup
Standalone switch

### Description
*Steps*
1. Get into configuration terminal of the switch
2. Execute the command `logging 10.0.0.2 udp 514 severity info` .
3. Verify that the syslog messages of severity info and above are received on the host machine.

### Test Result Criteria
#### Test Pass Criteria
Syslog messages of severity info and above are received on the host machine

#### Test Fail Criteria
Syslog messages are not received on the host machine.

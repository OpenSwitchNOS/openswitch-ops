# Show Core Dump Test Case

## Contents
- [1. Negative Test Cases](#1-negative-test-cases)
	- [1.1 Daemon Core Dump Configuration File Missing](#11-daemon-core-dump-configuration-file-missing)
	- [1.2 Empty Daemon Core Dump Configuration File](#12-empty-daemon-core-dump-configuration-file)
	- [1.3 Corrupted Daemon Core Dump Configuration File](#13-corrupted-daemon-core-dump-configuration-file)
	- [1.4 No Kernel Core Dump Configuration File](#14-no-kernel-core-dump-configuration-file)
	- [1.5 Empty Kernel Core Dump Configuration File](#15-empty-kernel-core-dump-configuration-file)
	- [1.6 Corrupted Kernel Core Dump Configuration File](#16-corrupted-kernel-core-dump-configuration-file)
	- [1.7 Invalid Input Parameter to Cli](#17-invalid-input-parameter-to-cli)
- [2. Positive Test Cases](#2-positive-test-cases)
	- [2.1 No Core Dumps Present.](#21-no-core-dumps-present)
	- [2.2 Daemon Core Dumps Displayed.](#22-daemon-core-dumps-displayed)
	- [2.3 Kernel Core Dumps Present](#23-kernel-core-dumps-present)
	- [2.4 Display both Kernel and Daemon Core Dumps.](#24-display-both-kernel-and-daemon-core-dumps)
- [3. Destructive Tests](#3-destructive-tests)
	- [3.1 Core Dump with Corrupted Core File Names](#31-core-dump-with-corrupted-core-file-names)


# 1. Negative Test Cases
##  1.1 Daemon Core Dump Configuration File Missing

### Objective
This test case verifies the behavior of `show core-dump` in the absence of daemon core dump configuration file.

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
*Steps*
1. Remove the daemon core dump configuration file `/etc/ops_corefile.conf`
2. Execute "show core-dump".

### Test Result Criteria
#### Test Pass Criteria
show core-dump should display error `Unable to read daemon core dump config file`.

#### Test Fail Criteria
Improper error message or crash.

## 1.2 Empty Daemon Core Dump Configuration File

### Objective
This test case verifies the behavior of show core-dump when there is no information present in the configuration file.

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
*Steps*
1. Empty the core dump configuration file `/etc/ops_corefile.conf`
2. Run `show core-dump` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
show core-dump should display error `Invalid daemon core dump config file`.

#### Test Fail Criteria
Improper error message or crash.


## 1.3 Corrupted Daemon Core Dump Configuration File

### Objective
This test case verifies the behavior of show core-dump when the daemon core dump configuration file is corrupted.

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
*Steps*
1. Remove the corepath entry from core dump configuration file `/etc/ops_corefile.conf`
2. Add some junk characters around the configuration file
3. Run `show core-dump` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
show core-dump should display error `Invalid daemon core dump config file`.

#### Test Fail Criteria
Improper error message or crash.


## 1.4 No Kernel Core Dump Configuration File

### Objective
This test case verifies the behavior of show core-dump when the kernel core dump configuration file is missing.

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
*Steps*
1. Remove the kernel core dump configuration file `/etc/kdump.conf`
2. Run `show core-dump` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
show core-dump should display error `Unable to read kernel core dump config file`.

#### Test Fail Criteria
Improper error message or crash.


## 1.5 Empty Kernel Core Dump Configuration File

### Objective
This test case verifies the behavior of show core-dump when the kernel core dump configuration file is empty.

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
*Steps*
1. Remove the contents of kernel core dump configuration file `/etc/kdump.conf`
2. Run `show core-dump` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
show core-dump should display error `Invalid kernel core dump config file`.

#### Test Fail Criteria
Improper error message or crash.


## 1.6 Corrupted Kernel Core Dump Configuration File

### Objective
This test case verifies the behavior of show core-dump when the kernel core dump configuration file is corrupted.

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
*Steps*
1. Remove the configuration named 'path' from core dump configuration file `/etc/kdump.conf`
2. Add junk entries across the configuration file
3. Run `show core-dump` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
show core-dump should display error `Invalid kernel core dump config file`.

#### Test Fail Criteria
Improper error message or crash.


## 1.7 Invalid Input Parameter to Cli

### Objective
This test case verifies the behavior of show core-dump invalid parameters are passed to it

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
*Steps*
1. Run `show core-dump 2314!@#$!@#$jkj` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
show core-dump should display error `Unknown command`.

#### Test Fail Criteria
Improper error message or crash.


# 2. Positive Test Cases
## 2.1 No Core Dumps Present.
### Objective
Verify the behavior of `show core-dump` when no core dump is present in the system

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

*Steps*
1. Delete all the core dump files(daemon as well as kernel) from the system .
2. Run "show core-dump" on vtysh shell.

### Test Result Criteria
#### Test Pass Criteria
 "show core-dump" should display `No core dumps are present`

#### Test Fail Criteria
 Improper message or crash.


## 2.2 Daemon Core Dumps Displayed.
### Objective
Verifies that the `show core-dump` displays daemon core dumps correctly

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
*Steps*
1. Generate the core dumps if no core dump is already present. To generate a core dump kill any process with is PID. Execute "kill -11 <PID>".  Otherwise just create a file under the core dump folder with the format <DaemonName>/<DaemonName>.1.YYYYMMDD.HHMMSS.core.tar.gz to similate a core dump
2. Execute "show core-dump".

### Test Result Criteria
#### Test Pass Criteria
Newly Added core dump should be displayed.

#### Test Fail Criteria
Newly Added core dump is not displayed or crash.


## 2.3 Kernel Core Dumps Present
### Objective
Verifies that `show core-dump` displays kernel core dump

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
*Steps*
1. Generate the kernel core dumps if no core dump is already present. To generate a kernel core dump run `echo c > /proc/sysrq-trigger`.  Otherwise create a dummy core dump file in the location mentioned in the kernel core dump configuration file.  This dummy core dump file should be named as vmcore.YYYYMMDD.HHMMSS.tar.gz
2. Execute "show core-dump".

### Test Result Criteria
#### Test Pass Criteria
 `show core-dump` displays the kernel core dump along with timestamp specified.

#### Test Fail Criteria
 `show core-dump` does not display the kernel core dump or errors out.


## 2.4 Display both Kernel and Daemon Core Dumps.
### Objective
Verifies that the `show core-dump` displays both kernel as well as daemon core dumps.

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
*Steps*
1. Generate the core dumps if no core dump is already present. To generate a core dump kill any process with is PID. Execute "kill -11 <PID>".  Otherwise just create a file under the core dump folder with the format <DaemonName>/<DaemonName>.1.YYYYMMDD.HHMMSS.core.tar.gz to similate a core dump
2. Generate the kernel core dumps if no core dump is already present. To generate a kernel core dump run `echo c > /proc/sysrq-trigger`.  Otherwise create a dummy core dump file in the location mentioned in the kernel core dump configuration file.  This dummy core dump file should be named as vmcore.YYYYMMDD.HHMMSS.tar.gz
3. Execute `show core-dump`


### Test Result Criteria
#### Test Pass Criteria
 Displays both the kernel and daemon core dumps

#### Test Fail Criteria
 Kernel or daemon core dump missing in the display.

# 3. Destructive Tests
## 3.1 Core Dump with Corrupted Core File Names
### Objective
Verifies that `show core-dump` handles corrupted core dump files without crashing.

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
*Steps*
1. Generate daemon core dump and change the name of core file to random string.
2. Run "show core-dump" on vtysh shell.

### Test Result Criteria
#### Test Pass Criteria
 "show core-dump" should not display those core dumps.

#### Test Fail Criteria
 Crashing or displaying junk information.

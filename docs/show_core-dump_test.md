#show core-sump test document	

##contents

##  1.1 Display core-dumps when present

### Objective
This test case verifies that core-dumps are listed when the user executes "show core-dump".

### Requirements
The requirements for this test case are:
 - Switch running openswitch
 - Core-dumps should be present in the switch

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
Step:
 - Generate the core dumps if no core-dump is already present. To generate a core dump kill any process with is PID. Execute "kill -11 <PID>".
 - Execute "show core-dump".

### Test Result Criteria
#### Test Pass Criteria
show core-dump successfully lists all the core-dumps that are present in the switch.

#### Test Fail Criteria
Show core-dump fails to display core dumps .  show core-dump displays the following error in this Case
`No core Dump Present`


## 1.2 Display "No Core Dump Present" if core-dumps are not present.

### Objective
This test case verifies that show core-dump does not display any core dump if they are not present on the switch.

### Requirements
The requirements for this test case are:
 - Switch running openswitch
 - Core-dumps should not be present in the switch.

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
Step:
 - Erase all the core dump present
 - Run `show core-dump` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
 Show core-dump does not display any core dump. show core-dump displays the following in this Case
`No core Dump Present`

#### Test Fail Criteria
 Show core-dump displays any core dump.



## 1.3 Empty core folder.

### Objective
This test case verifies that show core-dump does not display any core dump if they are not present on the switch. Folder is present but there are no coredumps.

### Requirements
The requirements for this test case are:
 - Switch running openswitch
 - Core-dumps should not be present in the switch.

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
Step:
 - Erase all the core dump present but keep the folder
 - Run `show core-dump` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
 Show core-dump does not display any core dump. show core-dump displays the following in this Case
`No core Dump Present`

#### Test Fail Criteria
 Show core-dump displays any core dump.




## 2. Negative Tests
## 2.1 Core Dump should be displayed after renaming.
### Objective
Rename the core dump file with some junk characters, changing the format and after the renaming that file should not be displayed.

### Requirements
The requirements for this test case are:
 - Switch running openswitch
 - Renamed core dump file.

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
1. Generate the core-dumps if no core-dump is already present. To generate a core dump kill any process with is PID. Execute "kill -11 <PID>".
2. Execute "show core-dump".
3. Rename any one of the files displayed in the earlier step.
4. "show core-dump" should not display the renamed file.


### Test Result Criteria
#### Test Pass Criteria
 "show core-dump" should not display the renamed core dump file.

#### Test Fail Criteria
 "show core-dump" displays the renamed files.


## 2.2 Renaming the core-dump file keeping the format intact.
### Objective
Rename the daemon file keeping the file naming convention intact. The file should be displayed.

### Requirements
The requirements for this test case are:
 - Switch running openswitch
 - Renamed core dump file.

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
1. Generate the core-dumps if no core-dump is already present. To generate a core dump kill any process with is PID. Execute "kill -11 <PID>".
2. Execute "show core-dump".
3. Rename any one of the files displayed in the earlier step keeping the naming format intact.
4. "show core-dump" displays the renamed file.


### Test Result Criteria
#### Test Pass Criteria
 "show core-dump" displays the renamed core dump file.

#### Test Fail Criteria
 "show core-dump" does not display the renamed file.


## 2.3 Giving extra token after the command "show core-dump".
### Objective
The cli should not take extra token after the command "show core-dump.

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
1. Execute "show core-dump $%#&%"


### Test Result Criteria
#### Test Pass Criteria
 The command throws an error.

#### Test Fail Criteria
 The command successfully runs.

## 2.4 Rename the daemon folder name.
### Objective
 The core file should get displayed.

### Requirements
 The requirements for this test case are:
  - Switch running openswitch
  - Renamed core dump folder

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
 1. Execute "show core-dump".


### Test Result Criteria
#### Test Pass Criteria
  The core file gets displayed.

#### Test Fail Criteria
  The core file does not get displayed..

## 3. Destructive Tests
## 3.1 Renaming the core dump folder exceeding the max value
### Objective
core dumps will not be displayed.

### Requirements
The requirements for this test case are:
 - Switch running openswitch
 - Renamed core dump folder

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
1. rename the core-dump folder to max limit.
2. Run "show core-dump" on vtysh shell.

### Test Result Criteria
#### Test Pass Criteria
 "show core-dump" should not display any core dumps.

#### Test Fail Criteria
 "show core-dump" displays the files.


## 3.2 Renaming the core dump file exceeding the max value
### Objective
core dumps will not be displayed.

### Requirements
The requirements for this test case are:
 - Switch running openswitch
 - Renamed core dump

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
1. rename the core-dump folder to max limit.
2. Run "show core-dump" on vtysh shell.

### Test Result Criteria
#### Test Pass Criteria
 "show core-dump" should not display any core dumps.

#### Test Fail Criteria
 "show core-dump" displays the files.


## 3.3 Core-dump folder without read permission
### Objective
core dumps will not be displayed.

### Requirements
The requirements for this test case are:
 - Switch running openswitch
 - change the folder permissions

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
1. change the core dump folder permissions.
2. Run "show core-dump" on vtysh shell.

### Test Result Criteria
#### Test Pass Criteria
 "show core-dump" should not display any core dumps.

#### Test Fail Criteria
 "show core-dump" displays the files.

## 3.4 Core-dump file without read permission
### Objective
core dumps will not be displayed.

### Requirements
The requirements for this test case are:
 - Switch running openswitch
 - change the file permissions

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
1. change the core dump file permissions.
2. Run "show core-dump" on vtysh shell.

### Test Result Criteria
#### Test Pass Criteria
 "show core-dump" should not display any core dumps.

#### Test Fail Criteria
 "show core-dump" displays the files.


## 3.5 Delete the core dump folder and files should stop getting displayed.
### Objective
  core dumps will not be displayed after the folder is deleted.

### Requirements
  The requirements for this test case are:
   - Switch running openswitch
   - core-dump with a core-dump file inside it.

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
  1. Execute "show core-dump".
  2. Delete the folder containing core-dump.

### Test Result Criteria
#### Test Pass Criteria
   "show core-dump" should not display the core-dumps in the folder which just got deleted..

#### Test Fail Criteria
   "show core-dump" displays the files.

  

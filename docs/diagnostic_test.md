
# Component Test Cases for Diagnostic

## Contents

- [Component Test Cases for Diagnostic](#component-test-cases-for-diagnostic)
    - [Contents](#contents)
    - [List supported feature for diag dump](#list-supported-feature-for-diag-dump)
        - [Objective](#objective)
        - [Requirements](#requirements)
        - [Setup](#setup)
            - [Topology Diagram](#topology-diagram)
            - [Test Setup](#test-setup)
        - [Description](#description)
        - [Test Result Criteria](#test-result-criteria)
            - [Test Pass Criteria](#test-pass-criteria)
            - [Test Fail Criteria](#test-fail-criteria)
    - [Basic diag dump on console](#basic-diag-dump-on-console)
        - [Objective](#objective)
        - [Requirements](#requirements)
        - [Setup](#setup)
            - [Topology Diagram](#topology-diagram)
            - [Test Setup](#test-setup)
        - [Description](#description)
        - [Test Result Criteria](#test-result-criteria)
            - [Test Pass Criteria](#test-pass-criteria)
            - [Test Fail Criteria](#test-fail-criteria)
    - [Basic diag dump to given file](#basic-diag-dump-to-given-file)
        - [Objective](#objective)
        - [Requirements](#requirements)
        - [Setup](#setup)
            - [Topology Diagram](#topology-diagram)
            - [Test Setup](#test-setup)
        - [Description](#description)
        - [Test Result Criteria](#test-result-criteria)
            - [Test Pass Criteria](#test-pass-criteria)
            - [Test Fail Criteria](#test-fail-criteria)
    - [References](#references)

## List supported feature for diag dump.

### Objective
"diag-dump list" command is able to display list of supported featues on console.

### Requirements
Switch running openswitch

### Setup
#### Topology Diagram
```ditta
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
- Run 'diag-dump list' on vtysh shell.

### Test Result Criteria


#### Test Pass Criteria
"diag-dump list" command gives list of supported daemon with their description.

#### Test Fail Criteria
"diag-dump list" command blocks for long time or vtysh crashing.

## Basic diag dump on console

### Objective
Capture basic diag dump on stdout of vtysh .

### Requirements
Switch running openswitch
### Setup
#### Topology Diagram
```ditta
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test Setup
Standalone Switch
### Description
Capture basic diag dump on console  using command 'diag-dump <feature name> basic' .
### Test Result Criteria
#### Test Pass Criteria
User can see output with last line as "Diagnostic dump captured for all daemons" .

#### Test Fail Criteria
No output on console or exit of vtysh process or missing of
"Diagnostic dump captured for all daemons" confirms to failure of test case.

## Basic diag dump to given file
### Objective
Capture basic diag dump to given file .

### Requirements
Ensure that feature related daemon are running .Feature related daemon are available in ops_diagdump.yaml file.
### Setup
#### Topology Diagram
```ditta
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test Setup
### Description
Capture basic diag dump into give file using command 'diag-dump <feature name> basic <filename>'.
### Test Result Criteria
#### Test Pass Criteria
User can't see output on vtysh and vtysh is free for next command.
Output file contains the diag dump output with string "Diagnostic dump captured for all daemons".
#### Test Fail Criteria
vtysh crash or showing output on console confirms failure of test case.

## References
* [Reference 1] 'diagnostic_test.md'

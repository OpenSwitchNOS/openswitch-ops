# Component Test Cases for Diagnostic Dump Feature

## Contents

- [Component Test Cases for Diagnostic Dump Feature](#component-test-cases-for-diagnostic-dump-feature)
	- [Contents](#contents)
	- [List supported feature for diag dump](#list-supported-feature-for-diag-dump)
	- [Basic diag dump on console](#basic-diag-dump-on-console)
	- [Basic diag dump to given file](#basic-diag-dump-to-given-file)
	- [Basic diag dump to given file and check file](#basic-diag-dump-to-given-file-and-check-file)
	- [Basic diag dump to given file and check file size](#basic-diag-dump-to-given-file-and-check-file-size)
	- [Basic diag dump for a unsupported daemon](#basic-diag-dump-for-a-unsupported-daemon)
	- [Basic diag dump for a unknown daemon](#basic-diag-dump-for-a-unknown-daemon)
	- [Basic diag dump without config  file](#basic-diag-dump-without-config-file)
	- [Basic diag dump with empty config  file](#basic-diag-dump-with-empty-config-file)
	- [References](#references)


## List supported feature for diag dump

### Objective
"diag-dump list" command is able to display list of supported features on console.

### Requirements
Switch running openswitch

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
Standalone Switch
### Description
Step:
- Run 'diag-dump list' on vtysh shell.

### Test result criteria
#### Test pass criteria
"diag-dump list" command gives list of supported features with their description.

#### Test fail criteria
"diag-dump list" command blocks for long time or vtysh crashing.

## Basic diag dump on console

### Objective
Capture basic diag dump on vtysh console.

### Requirements
Switch running openswitch
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
Standalone Switch
### Description
Capture basic diag dump on console  using command 'diag-dump <feature name> basic' .
### Test result criteria
#### Test pass criteria
User can see output with last line as "Diagnostic dump captured for feature" .

#### Test fail criteria
No output on console or exit of vtysh process or missing of
"Diagnostic dump captured for feature" confirms to failure of test case.

## Basic diag dump to given file
### Objective
Capture basic diag dump to given file .

### Requirements
Ensure that feature related daemon are running. Feature related daemon are available in ops_featuremapping.yaml file.
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
Capture basic diag dump into give file using command 'diag-dump <feature name> basic <filename>'.
### Test result criteria
#### Test pass criteria
User can't see output on vtysh and vtysh is free for next command.
Output file contains the diag dump output with string "Diagnostic dump captured for feature".
#### Test fail criteria
vtysh crash or showing output on console confirms failure of test case.



## Basic diag dump to given file and check file
### Objective
Capture basic diag dump to given file and check existance of file.

### Requirements
Ensure that feature related daemon are running .Feature related daemon are available in ops_featuremapping.yaml file.
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
Capture basic diag dump into give file using command 'diag-dump <feature name> basic <filename>'. Then check the file in path /tmp/ops-diag/<filename>

### Test result criteria
#### Test pass criteria
User can't see output on vtysh and vtysh is free for next command.
Output file contains the diag dump output with string "Diagnostic dump captured for feature".
User can verify the created file at location /tmp/ops-diag/<filename>.
#### Test fail criteria
vtysh crash or showing output on console confirms failure of test case . Absence of file /tmp/ops-diag/<file> confirms failure of testcase.


## Basic diag dump to given file and check file size
### Objective
Capture basic diag dump to given file and check the file size .

### Requirements
Ensure that feature related daemon are running .Feature related daemon are available in ops_featuremapping.yaml file.
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
Capture basic diag dump into give file using command 'diag-dump <feature name> basic <filename>'.
### Test result criteria
#### Test pass criteria
User can't see output on vtysh and vtysh is free for next command.
Output file contains the diag dump output with string "Diagnostic dump captured for feature" and file is created at /tmp/ops-diag/<filename> . This file contains valid data for corresponding feature.
#### Test fail criteria
vtysh crash or showing output on console confirms failure of test case. Empty file /tmp/ops-diag/<filename> also confirms failure of testcase.



## Basic diag dump for a unsupported daemon
### Objective
Capture basic diag dump for daemon which doesnot support diag feature.

### Requirements
Ensure that feature related daemon are running .Feature related daemon are available in ops_featuremapping.yaml file.
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
Capture basic diag dump into give file using command 'diag-dump <feature name> basic '.
Then check output on console.

### Test result criteria
#### Test pass criteria
User can see some error and vtysh is free for next command.
#### Test fail criteria
vtysh crash or vtysh blocked for indefenite time causes failure of this testcase.



## Basic diag dump for a unknown daemon
### Objective
Capture basic diag dump for daemon which doesnot exist .

### Requirements
Ensure that feature related daemon are not running on switch . Feature related daemon are available in ops_featuremapping.yaml file.
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
Capture basic diag dump into give file using command 'diag-dump <feature name> basic '.
Then check output on console.

### Test result criteria
#### Test pass criteria
User can see some error and vtysh is free for next command.
#### Test fail criteria
vtysh crash or vtysh blocked for indefenite time causes failure of this testcase.



## Basic diag dump without config  file
### Objective
Capture basic diag dump for daemon or list out the feature availbe on cli without config file.

### Requirements
Ensure to delete the config ops_featuremapping.yaml file.
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
Capture 'diag-dump list' and try 'diag-dump <feature name> basic ' . Without config file it will not show any feature list and 'diag-dump <feature name> basic ' will not accept any feature name.

Capture basic diag dump into give file using command 'diag-dump <feature name> basic '.
Then check output on console.

### Test result criteria
#### Test pass criteria
User can see some error/warning message and vtysh is free for next command. As there is no feature daemon mapping file so it will not accept any option for command 'diag-dump <feature name> basic '.
#### Test fail criteria
vtysh crash or vtysh blocked for indefenite time causes failure of this testcase.




## Basic diag dump with empty config  file
### Objective
Capture basic diag dump for daemon or list out the feature availbe on cli with empty  config file.

### Requirements
Remove all conent of the config ops_featuremapping.yaml file.
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
Capture 'diag-dump list' and try 'diag-dump <feature name> basic ' . With empty config file it will not show any feature list and 'diag-dump <feature name> basic ' will not accept any feature name.

Capture basic diag dump into give file using command 'diag-dump <feature name> basic '.
Then check output on console.

### Test result criteria
#### Test pass criteria
User can see some error/warning message and vtysh is free for next command. As there is no feature daemon mapping file so it will not accept any option for command 'diag-dump <feature name> basic '.
#### Test fail criteria
vtysh crash or vtysh blocked for indefinite time causes failure of this testcase.


## References
* [Reference 1] 'diagnostic_test.md'

# Diagnostic Dump

## Contents




- [Diagnostic Dump](#diagnostic-dump)
	- [Contents](#contents)
	- [Overview](#overview)
	- [How to use the feature](#how-to-use-the-feature)
		- [Setting up the basic configuration](#setting-up-the-basic-configuration)
		- [list diagnostic supported features](#list-diagnostic-supported-features)
		- [basic diagnostic on console](#basic-diagnostic-on-console)
		- [basic diagnostic to file](#basic-diagnostic-to-file)
		- [Troubleshooting the configuration](#troubleshooting-the-configuration)
			- [Condition](#condition)
			- [Cause](#cause)
			- [Remedy](#remedy)


## Overview
Diagnostic dump command is used to collect internal diagnostic information from single or multiple daemon mapped to a single feature.


## How to use the feature
1. First configure ops_diagdump.yaml file.
2. To show supported feature list run the cli 'diag-dump list' .
2. To show basic diagnostic information on console run 'diag-dump <feature> basic' .
3. To dump basic diagnostic information to a file run 'diag-dump <feature> basic  <file path>' .



### Setting up the basic configuration

 Write or update ops_diagdump.yaml file for daemon and feature mapping. yaml file path is  /etc/openswitch/supportability/ops_diagdump.yaml .

### List diagnostic supported features
Execute cli command "diag-dump list" and get the list of supported features with description on console.

### Basic diagnostic on console
Execute "diag-dump <feature> basic" to get basic diagnostic information on console.

### Basic diagnostic to file
Execute "diag-dump <feature> basic <filename>" to get basic diagnostic information in a file.

### Troubleshooting the configuration

#### Condition
'diag-dump' cli command results in the following error
'Failed to capture diagnostic information'


#### Cause
1.ops_diagdump.yaml file is not present in right path  (/etc/openswitch/supportability/ops_diagdump.yaml )
2.user may not have read permission.
3.incorrect content of yaml file .


#### Remedy
1.Please ensure the yaml file is present in its path
(/etc/openswitch/supportability/ops_diagdump.yaml )
2.Verify the content of yaml file using yaml lint tool.
3.Verify the structure of the configuration is valid.
4.Ensure the user has read permission for yaml file.

# show events Infrastructure

## Contents

- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
    - [Setting up the basic configuration](#setting-up-the-basic-configuration)
    - [Verifying the configuration](#verifying-the-configuration)
    - [Troubleshooting the configuration](#troubleshooting-the-configuration)
        - [Cause](#cause)
        - [Remedy](#remedy)


## Overview
show events is used to run events of  all supported features.This CLI helps to system administors/developers/support/lab with information useful for generation of event logs in switch.
This CLI allows system administrators/support/lab to more easily obtain events  on problem that occur and provides solution to problem.

## How to use the CLI
	To run the events for supported features/daemons in the switch ,run the cli command `show events`.

### Setting up the basic configuration

Show events Infrastructure loads its configuration from the showevent configuration yaml file located in (/etc/openswitch/supportability/ops_events.yaml).
This file contains the default configuration for show events.

### Verifying the configuration

 Execute the cli command `show events` and verify the features as configured.

### Troubleshooting the configuration

#### Cause
This Error could appear in the following two cases.
1. ops_events.yaml configuration file is missing in its path.
2. ops_events.yaml configuration file is wrongly configured.

#### Remedy
1.Please ensure that the ops_events.yaml file is present in path(/etc/openswitch/supportability/ops_events.yaml).
2.Verify the configuration file (ops_events.yaml) to be a valid yaml file, using yaml tools.

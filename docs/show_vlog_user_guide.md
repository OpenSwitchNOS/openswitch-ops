# Show Vlog User Guide

## Contents

- [Overview](#overview)
- [Show vlog to display vlogs](#show-vlog-to-display-vlogs)
	- [filter vlogs based on daemon name](#filter-vlogs-based-on-daemon-name)
	- [filter vlogs based on severity](#filter-vlogs-based-on-severity)
- [Using the show vlog config command to access feature/daemon information](#using-the-show-vlog-command-to-access-feature-daemon-information)
    - [List the vlog supported features](#list-vlog-supported-features)
    - [Severity log level  of feature](#severity-log-level-of-feature)
    - [Severity log levels of supported features](#severit-log-levels-of-supported-features)
    - [Severity log level of daemon](#log-level-severity-of-daemon)
    - [Configure logging level of features and daemons](#configure-logging-level-of-features-and-daemons)
    - [Troubleshooting the configuration](#troubleshooting-the-configuration)
         - [Condition](#condition)
         - [Configuration file is missing in its path](#configuration-file-is-missing-in-its-path)
         - [File is not properly configured](#file-is-not-properly-configured)
    - [Feature to daemon mapping](#feature-to-daemon-mapping)
	- [References](#references)

## Overview
The `show vlog` used as logging infrastructure in most of ops daemons.By using `show vlog` to display vlog messages of ops daemons.The `show vlog config` CLI command is used to display list of features and corresponding daemons log levels of syslog and file destinations. This CLI is useful to generate switch feature vlog configuration log levels for administrators, developers, support and lab staff.

## Show vlog to display vlogs
The `show vlog` CLI is used to display vlog messages of ops daemons.There are various ways to filter the vlog messages. In the following section to filter vlog messages using commands.

### Filter vlogs based on daemon name

The `show vlog daemon <daemon_name>` CLI is used to filter the vlog messages based on daemon-name/word.This CLI displays only vlog messages of specified daemon-name/word

### Filter vlogs based on severity
The `show vlog severity <emer/err/warn/info/debug>` CLI is used to filter the vlog messages of severity level and above.
This CLI displays vlog messages of specified severity level and above.

## Using the show vlog command to access feature/daemon information

There are various ways to get access to supported feature information using the `show vlog config` command as shown in the following sections.

### List vlog supported features
Execute the CLI `show vlog config list` command to get the list of supported features with descriptions on the console.

### Severity log level  of feature
Execute the CLI `show vlog config feature <feature_name>` command to capture specific feature log levels of file and syslog destinations on the console.

### Severity log levels of supported features
Execute the CLI `show vlog config` command to get the list of supported features and corresponding daemons log levels of file and syslog destinations on the console.

### Severity log level of daemon
Execute the CLI `show vlog config daemon <daemon_name>` command to capture the daemon log levels of file and syslog destinations on the console.

### Configure feature logging level and destination
Configure the switch using
`vlog (feature|daemon) <name> <syslog/file/all> <emer/err/warn/info/dbg>` on configuration mode.
Execute the CLI `show vlog config (feature|daemon) <name>` to obtain the corresponding feature/daemon log level changes of file and syslog destinations on the console.

### Troubleshooting the configuration

#### Condition
The `show vlog config` command results in the following error
'Failed to capture vlog information <feature/daemon>'

#### Configuration file is missing in its path
If the error `ops_featuremapping.yaml configuration file is missing in its path` appears, ensure that the `ops_featuremapping.yaml` file is present in the `/etc/openswitch/supportability/ops_featuremapping.yaml` path.

#### File is not properly configured
If the error `ops_featuremapping.yaml configuration file is wrongly configured` appears,
use the yaml tools to confirm that the configuration file (ops_featuremapping.yaml) is valid.

### Feature to daemon mapping
The `/etc/openswitch/supportability/ops_featuremapping.yaml` file contains `feature to daemon mapping` configurations.

### References
* References `showvlog_user_guide.md`

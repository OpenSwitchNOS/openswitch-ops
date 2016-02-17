# Infrastructure for show vlog command

## Contents

- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
	- [Setting up the basic configuration](#setting-up-the-basic-configuration)
	- [Verifying the configuration](#verifying-the-configuration)
	- [Troubleshooting the configuration](#troubleshooting-the-configuration)
		- [Configuration file is missing in its path](#configuration-file-is-missing-in-its-path)
		- [File is not properly configured](#file-is-not-properly-configured)

#Overview

The `show vlog` command is used to display list of features/daemons and severity log levels.This CLI is useful to generate switch feature vlog configuration log levels for administrators, developers, support and lab staff.To obtain the loglevel configuration of feature for destinations SYSLOG and FILE using the CLI.

## How to use the CLI

To access vlog list for supported features or daemons in the switch, run the CLI `show vlog` command.

### Setting up the basic configuration

The `show vlog` command infrastructure loads its configuration from the "showvlog configuration yaml" file located in (/etc/openswitch/supportability/ops_featuremapping.yaml).This file contains the default configuration for the `show vlog` command.


### Verifying the configuration

Execute the CLI `show vlog` command and verify that the features are configured.

### Troubleshooting the configuration

#### Configuration file is missing in its path.

If the error `ops_featuremapping.yaml configuration file is missing in its path` appears ,ensure
that the `ops_featuremapping.yaml` file is present in the (/etc/openswitch/supportability/ops_featuremapping.yaml) path.

#### File is not properly configured

If the error `ops_featuremapping.yaml configuration file is wrongly configured` appears, use the yaml tools to confirm that the configuration file (ops_featuremapping.yaml) is valid.
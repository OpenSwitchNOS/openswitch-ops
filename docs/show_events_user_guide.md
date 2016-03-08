## Contents

- [Infrastructure for the show events command](#infrastructure-for-the-show-events-command)
	- [Contents](#contents)
	- [Overview](#overview)
	- [How to use the CLI](#how-to-use-the-cli)
		- [Setting up the basic configuration](#setting-up-the-basic-configuration)
		- [Verifying the configuration](#verifying-the-configuration)
			- [Log Filter Options](#log-filter-options)
		- [Reverse List Option](#reverse-list-option)
		- [Troubleshooting the configuration](#troubleshooting-the-configuration)
			- [Configuration file is missing in its path.](#configuration-file-is-missing-in-its-path)
			- [File is not properly configured](#file-is-not-properly-configured)

## Overview

The `show events` command is used to display events for all of the supported features. This CLI is useful to generate switch event logs for administrators, developers, support, and lab staff. Problem events and solutions are also easily obtainable using the CLI.

## How to use the CLI

	To access events for supported features or daemons in the switch, run the CLI `show events`command.

### Setting up the basic configuration

The `show events` command infrastructure loads its configuration from the "showevent configuration yaml" file located in (/etc/openswitch/supportability/ops_events.yaml). This file contains the default configuration for the `show events` command.

### Verifying the configuration

 Execute the CLI `show events` command and verify that the features are configured.

#### Log Filter Options

`show events` command provide log filter options to show the logs of interest only. The following filters are supported:

 * event-id
 * severity
 * category

These filter keywords can be used along with the `show events` command to filter logs accordingly.

For example,

To filter according to event ID of 1002
`show events event-id 1002`

To filter according to severity level of emergency,
`show events severity emer`

The following are the severity keywords supported in CLI:
 * emer
 * alert
 * crit
 * error
 * warn
 * notice
 * info
 * debug

To filter according to interested log category:
`show events category LLDP`

Also a combination of all these filters can be used together.

For example:
`show events event-id 1003 category LLDP severity emer`

#### Reverse List Option

The show events output usually displays from oldest to latest in order.
We can make use of `reverse` keyword to list logs from latest to oldest order.
This option can be used along with any of the log filters as well.

For example:
`show events reverse`
`show events event-id 1003 category LLDP severity emer reverse`

### Troubleshooting the configuration

#### Configuration file is missing in its path.

If the error `ops_events.yaml configuration file is missing in its path` appears, ensure that the `ops_events.yaml` file is present in the (/etc/openswitch/supportability/ops_events.yaml) path.

#### File is not properly configured

If the error `ops_events.yaml configuration file is wrongly configured` appears, use the yaml tools to confirm that the configuration file (ops_events.yaml) is valid.

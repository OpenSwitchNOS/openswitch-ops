# Infrastructure for the show events command

## Contents

- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
	- [Show events to display event logs](#show-events-to-display-event-logs)
		- [Filter event logs based on category](#filter-event-logs-based-on-category)
		- [Filter event logs based on event-id](#filter-event-logs-based-on-event-id)
		- [Filter event logs based on severity](#filter-event-logs-based-on-severity)
    - [Setting up the basic configuration](#setting-up-the-basic-configuration)
    - [Verifying the configuration](#verifying-the-configuration)
    - [Troubleshooting the configuration](#troubleshooting-the-configuration)
        - [Configuration file is missing in its path](#Configuration file is missing in its path)
        - [File is not properly configured](#File is not properly configured)


## Overview

The `show events` command is used to display events for all of the supported features. This CLI is useful to generate switch event logs for administrators, developers, support, and lab staff. Problem events and solutions are also easily obtainable using the CLI.

## How to use the feature
### Show events to display event logs
To access events for supported features or daemons in the switch, run the CLI `show events`command.

#### Filter event logs based on category
The `show events category <WORD>` CLI is used to filter the  event log messages based on category .This CLI displays only  event log messages of specified category.

#### Filter event logs based on event-id
The `show events event-id <1001-999999>` CLI is used to filter the  event log messages based on event-id .This CLI displays only  event log messages of specified event-id's.

#### Filter event logs based on severity
The `show events severity` CLI is used to filter the  event log messages based on severity level.This CLI displays only  event log messages of specified severity and ab.

### Setting up the basic configuration

The `show events` command infrastructure loads its configuration from the "show event configuration yaml" file located in (/etc/openswitch/supportability/ops_events.yaml). This file contains the default configuration for the `show events` command.

### Verifying the configuration

 Execute the CLI `show events` command and verify that the features are configured.

### Troubleshooting the configuration

#### Configuration file is missing in its path.

If the error `ops_events.yaml configuration file is missing in its path` appears, ensure that the `ops_events.yaml` file is present in the (/etc/openswitch/supportability/ops_events.yaml) path.

#### File is not properly configured

If the error `ops_events.yaml configuration file is wrongly configured` appears, use the yaml tools to confirm that the configuration file (ops_events.yaml) is valid.

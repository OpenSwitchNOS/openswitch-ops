# Show Tech Infrastructure

## Contents


- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
    - [Setting up the basic configuration](#setting-up-the-basic-configuration)
    - [Verifying the configuration](#verifying-the-configuration)
    - [Troubleshooting the configuration](#troubleshooting-the-configuration)
        - [Condition](#condition)
        - [Cause](#cause)
        - [Remedy](#remedy)
- [CLI](#cli)
- [Related features](#related-features)


## Overview
Show Tech Infrastructure is used to collect the summary of switch or feature specific information.  This Infrastructure will run a collection of show commands and produces the output in text format.  The collection of show commands per feature are present in the show tech configuration file, accordingly show tech will those commands for the given feature.  The output of the show tech command is mainly useful to analyze the system/feature behavior. Tools could be developed to parse these output in order to arrive at meaningful conclusion and aid in problem troubleshooting.

## How to use the feature

1. To collect the switch wide show tech information, run the cli command `show tech`
2. To collect a feature specific show tech information, run the cli command `show tech FEATURE-NAME`
3. To collect a sub feature specific show tech information, run the cli command `show tech FEATURE-NAME SUB-FEATURE-NAME`
4. To know the list of features and sub features supported by show tech, run the cli command `show tech list`

### Setting up the basic configuration

Show Tech Infrastructure loads its configuration from the showtech configuration yaml file located in (/etc/openswitch/supportability/ops_showtech.yaml).
This file contains the default configuration for show tech.

### Verifying the configuration

 Execute the cli command `show tech list` and verify the features and subfeatures are listed as configured

### Troubleshooting the configuration

#### Condition
`show tech` cli commands results in the following error.

`Failed to obtain Show Tech Configuration`

#### Cause
This Error could appear in the following two cases
1. ops_showtech.yaml configuration file is missing in its path
2. ops_showtech.yaml configuration file is wrongly configured.

#### Remedy
1.Please ensure that the ops_showtech.yaml file is present in its path (/etc/openswitch/supportability/ops_showtech.yaml).
2.Verify the configuration file (ops_showtech.yaml) to be a valid yaml file, using yaml lint tools.
3.Verify that the structure of the configuration is valid.  Refer [here](/documents/user/show-tech_design#show-tech-configuration-yaml-file) for structure information and example.

## CLI

Click [here](/documents/user/show-tech_cli#commands-summary) for the CLI commands related to the named feature.

## Related features
-

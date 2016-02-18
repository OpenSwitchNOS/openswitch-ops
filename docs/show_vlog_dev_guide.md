# Show Vlog Infrastructure Developer Guide

## Contents

- [Overview](#overview)
- [How to map feature to daemon in to show vlog ](#how-to-map-feature-to-daemon-in-to-show-vlog)
- [Sample YAML file](#sample-yaml-file)
- [Testing](#testing)
	- [Running CT test for show vlog](#running-ct-test-for-show-vlog)
- [References](#references)


## Overview
The show vlog config CLI is used as logging infrastructure in most of ops daemons.
This CLI captures the log levels of file and syslog destinations for supported
features.

## How to map feature to daemon in to show vlog
Define a singleton function in `src/ops-supportability/src/featuremapping/feature_mapping.c`
that mapping the features and daemons in yaml file.

The syntax of the Initial routine of feature to daemon mapping should be as follows:
```
struct feature* get_feature_mapping(void)
```

## Sample YAML File
Add a new enty for a daemon on the switch or add the following entry in the ops-supportability repo.
`/etc/openswitch/supportability/ops_featuremapping.yaml`.

	```ditta
     -
       feature_name: "lldp"
       feature_desc: "Link Layer Discovery Protocol"
       daemon:
         - "ops-lldpd"

     -
       feature_name: "lacp"
       feature_desc: "Link Aggregation Control Protocol"
       daemon:
         - "ops-lacpd"
     -
       feature_name: "fand"
       feature_desc: "System Fan"
       daemon:
          - "ops-fand"
```

## Testing

Once the configuration file is modified, test the following four CLI commands and verify the output.

| Command | Expectation|
|:--------|:-----------|
| **show vlog config** | Runs show vlog config for supported features.Ensure that your newly added feature commands run successfully as part of the show vlog config output |
| **show vlog config list** | List the supported features and description.Ensure that it lists your newly added feature name and description |
| **show vlog config feature <feature_name>** | Runs show vlog config for the newly added feature and verifies the ouput |
| **show vlog config daemon <daemon_name>** | Runs show vlog config for daemon directly |

### Running CT test for show vlog
Run the following CT test to verify that the show vlog infrastructure is properly working with the configuration changes.

`make devenv_ct_test src/ops-supportability/test/show_vlog_test.py`

## References

* [Reference 1 ] `show_vlog_design.md`
* [Reference 2 ] `show_vlog_cli.md`
* [Reference 3 ] `show_vlog_test.md`
* [Reference 4 ] `show_vlog_user_guide.md`
* [Reference 5 ] `show_vlog_dev_guide.md`

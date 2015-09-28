# Autoprovisioning

[toc]

## Overview ##
Autoprovisioning (a.k.a Zero Touch Provisioning - ZTP)  is a feature which enables automatic provisioning of switch when it is deployed. Using a DHCP option advertised by DHCP server in the setup, the switch downloads a provisioning script and executes it. The provisioning script can do many things like adding new management users, downloading ssh keys, installing a server certificate etc. This feature is mainly used to download ssh keys and add user ids to the switch, to enable key based authentication of management users.

## How to use the feature ##
###Setting up the basic configuration

The feature is enabled by default and cannot be turned off through CLI. To disable autoprovisioning feature, one should configure the DHCP server to NOT send option 239 in DHCP reply/ack messages.


###Verifying the configuration

N/A

###Troubleshooting the configuration

#### Condition
Autoprovisioning not performed
#### Cause
1.DHCP option 239 not configured on the DHCP server

Verify whether DHCP server is correctly configured

2.Provisioning script does not contain the line "OPS-PROVISIONING"

Please verify the provisioning script.
## CLI ##
Click [Autoprovision CLI-TBL](https://openswitch.net/cli_feature_name.html#cli_command_anchor) for the CLI commands related to the named feature.

## Related features ##
None


# Management Interface
#Table of Contents
------------------
[TOC]

## Overview ##
The primary goal of the management module is to facilitate the management of device. It provides the following:

	•	Device access and configuration

	•	Event collection for monitoring, analysis, and correlation

	•	Device and user authentication, authorization, and accounting

	•	Device time synchronization

	•	Device image downloading


The device is configured or monitored through the management interface. All management traffic like
ssh to the device, tftp, etc goes through the management interface.

## Prerequisites ##
- The physical interface that should act as management interface should be specified in the hardware description file "image.manifest".
- Install the Dhclient in the switch for the management interface to function properly in dhcp mode.

## How to use the feature ##

###Setting up the basic configuration

 Configure the mode in which the management interface is going to operate. Select one of the following options:
- DHCP mode -- DHCP Client automatically populates all the management interface parameters.
- Static mode -- User manually configures the management interface parameters.

###Setting up the optional configuration

 1. Configure the IPv4 or the IPv6 configuration depending on the requirement.
 2. Configure that secondary nameserver if fallback is required.

###Verifying the configuration

 1. Verify the configured values using the `show interface mgmt` command.
 2. Verify the configuration using the `show running-config` command.

###Troubleshooting the configuration
Troubleshoot the device only through the management interface. if there is any problem with the management interface configuration, you may not be able to access the device over the network. Try accessing it over the serial console.
#### Scenario 1
##### Condition
The values configured are not displayed with the show command.
##### Cause
The configured values will not appear in the show command if the configuration fails at the management interface daemon.
Check the syslog for the error message.
Check for any error in the daemon using the command `systemctl status mgmt-intf -l`.
##### Remedy
Restart the management interface daemon using the command `systemctl restart mgmt-intf`.
#### Scenario 2
##### Condition
Values configured in the CLI are not configured in the interface.
##### Cause
The management interface daemon could have crashed.
Check the syslog for the error message.
Check if the daemon is still int running state using the command `systemctl status mgmt-intf -l`.
##### Remedy
Restart the management interface daemon using the command `systemctl restart mgmt-intf`.
#### Scenario 3
##### Condition
Mode is dhcp, but no DHCP attributes are populated.
##### Cause
dhclient might be down.
Check the syslog for the error message and status of the dhclient using the command `systemctl status dhclient@eth0.service -l`.
##### Remedy
Restart the management interface daemon using the command `systemctl restart mgmt-intf`.

## CLI ##
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here-TBL](https://openswitch.net/cli_feature_name.html#cli_command_anchor) for the CLI commands related to the named feature.
## Related features ##
None.

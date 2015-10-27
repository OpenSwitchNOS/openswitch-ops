#Loopback interface
<!-- TOC depth:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Loopback interface](#loopback-interface)
	- [Overview ##](#overview-)
	- [How to use the feature ##](#how-to-use-the-feature-)
		- [Setting up the basic configuration](#setting-up-the-basic-configuration)
		- [Setting up the optional configuration](#setting-up-the-optional-configuration)
		- [Verifying the configuration](#verifying-the-configuration)
		- [Troubleshooting the configuration](#troubleshooting-the-configuration)
			- [Condition](#condition)
			- [Cause](#cause)
			- [Remedy](#remedy)
	- [CLI ##](#cli-)
<!-- /TOC -->

## Overview ##
A loopback interface is a virtual interface, supporting IPv4 and IPv6 address configuration, that remains up until you disable it. Unlike subinterfaces, loopback interfaces are independent of the state of any physical interface.E.g Router ID for routing protocols like OSPF.

The loopback interface can be considered stable because once you enable it, it will remain up until you shut it down. This makes loopback interfaces ideal for assigning Layer 3 addresses such as IP addresses when you want a single address as a reference that is independent of the status of any physical interfaces in the networking device.

Max limit of loopback interfaces is 1024.

## How to use the feature ##

###Setting up the basic configuration

 1. Create a loopback interface
 2. Set IPv4 address
 3. Enable

###Setting up the optional configuration

 1. None

###Verifying the configuration

 1. Display configured loopback interfaces

###Troubleshooting the configuration

#### Condition
Unable to ping Loopback interface from external entity
#### Cause
Overlapping IP address set on loopback interface
#### Remedy
Check var log messages from Linux shell or external log messages server
## CLI ##
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [CLI-TBL](https://openswitch.net/cli_feature_name.html#cli_command_anchor) for the CLI commands related to the loopback interfaces feature.

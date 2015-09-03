<!--  See the https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet for additional information about markdown text.
Here are a few suggestions in regards to style and grammar:
* Use active voice. With active voice, the subject is the doer of the action. Tell the reader what
to do by using the imperative mood, for example, Press Enter to view the next screen. See https://en.wikipedia.org/wiki/Active_voice for more information about the active voice. 
* Use present tense. See https://en.wikipedia.org/wiki/Present_tense for more information about using the present tense. 
* Avoid the use of I or third person. Address your instructions to the user. In text, refer to the reader as you (second person) rather than as the user (third person). The exception to not using the third-person is when the documentation is for an administrator. In that case, *the user* is someone the reader interacts with, for example, teach your users how to back up their laptop. 
* See https://en.wikipedia.org/wiki/Wikipedia%3aManual_of_Style for an online style guide.
Note regarding anchors:
--StackEdit automatically creates an anchor tag based off of each heading.  Spaces and other nonconforming characters are substituted by other characters in the anchor when the file is converted to HTML. 
 --> 
 
Management Interface
=======
<!--Provide the title of the feature-->

 - Overview
 - Prerequisites
 - How to use the feature
 - CLI
 - Related features
 
## Overview ##
 <!--Provide an overview here. This overview should give the reader an introduction of when, where and why they would use the feature. -->
The primary goal of the management module is to facilitate the management of device. It provides the following:

	•	Device access and configuration
	
	•	Event collection for monitoring, analysis, and correlation
	
	•	Device and user authentication, authorization, and accounting
	
	•	Device time synchronization
	
	•	Download image to device
	

The device is configured or monitored through the management interface. All management traffic like ssh to the device, tftp, etc goes through the management interface.  
 
## Prerequisites ##
<!--Change heading for conceptual or reference info, such as Prerequisites. -->
- The physical interface that should act as management interface should be specified in the hardware description file "image.manifest".
- Dhclient should be installed in the switch for the management interface to function properly in the dhcp mode.
## How to use the feature ##

###Setting up the basic configuration

 1. Configure the mode in which the management interface is going to operate.
 2. If the mode is dhcp, then dhcp client will populate all the management interface parameters.
 3. If the mode is static, configure the management interface parameters.
 

###Setting up the optional configuration

 1. Configure the IPv4 or/and IPv6 configuration depending on the requirement.
 2. Configure secondary nameserver if fallback is required.

###Verifying the configuration

 1. Verify the configured values using show command.
 2. Verify the configuration using show running-config command.

###Troubleshooting the configuration
The device is troubleshooted through the management interface only. So if there is any problem with the management interface configuration, device may not accessible over the network and it should be accessed over the serial console for further troubleshooting.
#### Scenario 1
#### Condition 
Values configured are not displayed in the show command.
#### Cause 
The configured values will not appear in the show command if the configuration fails at the management interface daemon.
Check the syslog for the error message.
Check for any error in the daemon using the command "systemctl status mgmt-intf -l".
#### Remedy  
Restart the management interface daemon using the command "systemctl restart mgmt-intf".
#### Scenario 2
#### Condition  
Values configured in CLI are not configured on the interface.
#### Cause 
The management interface daemon could have crashed.
Check the syslog for the error message.
Check if the daemon is still int running state using the command "systemctl status mgmt-intf -l".
#### Remedy  
Restart the management interface daemon using the command "systemctl restart mgmt-intf".
#### Scenario 3
#### Condition  
Mode is dhcp, but no DHCP attributes are populated.
#### Cause 
dhclient might be down.
Check the syslog for the error message and status of the dhclient using the command "systemctl status dhclient@eth0.service -l".
#### Remedy  
Restart the management interface daemon using the command "systemctl restart mgmt-intf".

## CLI ##
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here-TBL](https://openswitch.net/cli_feature_name.html#cli_command_anchor) for the CLI commands related to the named feature.  
## Related features ##
None.

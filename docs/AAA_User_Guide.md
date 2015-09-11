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

AAA Feature
=======

- Overview
- How to use the feature
- CLI
- Related features

## Overview ##
 <!--Provide an overview here. This overview should give the reader an introduction of when, where and why they would use the feature. -->
This feature is used for authenticating the users who access the switch management interface via console, SSH or REST. It supports the following:

	- Local or RADIUS authentication.
	- Configure RADIUS servers (maximum up-to 64 RADIUS servers).
	- Configure SSH authentication method.

This feature currently supports authentication of the user based on user name and password.

## How to use the feature ##
### Scenario 1 ###
###Setting up the basic configuration

 1. Create user on the switch and configure a password.
 2. Configure the authentication mode: local or RADIUS.
 3. Configure RADIUS servers.

###Setting up the optional configuration
 1. Change the default value of shared secret used for communication between the switch and RADIUS server.
 2. Change the default value of the port used for communication with RADIUS server.
 3. Change the default value of number of connection retries.
 4. Change the default value of connection timeout.

###Verifying the configuration

 1. Verify the configuration using show command
 2. Verify the configuration using show running-config command for non default values.

###Troubleshooting the configuration
### Case 1
#### Condition
When local authentication configured, but unable to login with local password.
#### Possible causes

- AAA daemon status: Run the command "ps -ef | grep aaautilspamcfg".
- PAM configuration files: Check the presence of common-*-access files in the path "/etc/pam.d/".
- Verify that user has entered the correct password.

#### Remedy
- Verify if daemon is running, if crashed restart it by "service aaautils.service start".
- If pam configuration files are removed, copy PAM configuration files from another switch from the path "/etc/pam.d/".
- Verify /var/log/auth.log for more information.

### Case 2
#### Condition
When RADIUS authentication configured, but unable to login with RADIUS server password.
#### Possible causes
- AAA daemon status: Run the command "ps -ef | grep aaautilspamcfg".
- Verify if RADIUS server stopped or not reachable.
- Difference in the configuration of RADIUS servers on the switch, verify by "show radius-server" and the RADIUS server running on the host.
- Verify that user has entered the correct password.
#### Remedy
- Verify if daemon is running, if crashed restart it by "service aaautils.service start".
- If pam configuration files are removed, copy PAM configuration files from another switch from the path "/etc/pam.d/".
- Restart RADIUS server: service <RADIUS server> start.
- Verify /var/log/auth.log for more information.

### Scenario 2 ###
###Setting up the basic configuration
 1. Enable RADIUS authentication.
 2. Enable fallback to local authentication.
 3. Configure RADIUS server.
###Setting up the optional configuration
 1. Change the default value of shared secret used for communication between the switch and RADIUS server.
 2. Change the default value of the port used for communication with RADIUS server.
 3. Change the default value of number of connection retries.
 4. Change the default value of connection timeout.
###Verifying the configuration

 1. Verify using show commands.
 2. Verify using show running-config command.

###Troubleshooting the configuration
#### Condition
When RADIUS server is unreachable, user couldn't login with local credentials even though fallback to local is enabled.
#### Possible causes
- AAA daemon status: Run the command "ps -ef | grep aaautilspamcfg".
- PAM configuration files: Check the presence of common-*-access files in the path /etc/pam.d/
- Verify that user has entered the correct password.
#### Remedy
- Verify if daemon is running, if crashed restart it by "service aaautils.service start".
- If pam configuration files are removed, copy PAM configuration files from another switch from the path "/etc/pam.d/".

### Scenario 3 ###
###Setting up the basic configuration
 1. Create a user on the switch.
 2. Enable ssh password or public key authentication method
###Setting up the optional configuration
N/A
###Verifying the configuration

 1. Verify using show commands.
 2. Verify using show running-config command.

###Troubleshooting the configuration
### Case 1
#### Condition
SSH password authentication is enabled, but user is not able to login with the password.
#### Possible causes
- AAA daemon status: Run the command "ps -ef | grep aaautilspamcfg".
- SSH configuration file: Check the presence of "sshd_config" file in path "/etc/ssh/".
- Verify that user has entered the correct password.
#### Remedy
- Verify if daemon is running, if crashed restart it by "service aaautils.service start".
- If ssh configuration file is removed, copy SSH configuration file from another switch from path "/etc/sshd/".
- Verify /var/log/auth.log for more information.
### Case 2
#### Condition
SSH public key authentication is enabled, but user is not able to login.
#### Possible causes
- AAA daemon status: Run the command "ps -ef | grep aaautilspamcfg".
- SSH configuration file: Check the presence of "sshd_config" file in path "/etc/ssh/".
- Users public key is not present on the switch "/users/<user>/.ssh/id_rsa.pub".
#### Remedy
- Verify if daemon is running, if crashed restart it by "service aaautils.service start".
- If ssh configuration file is removed, copy SSH configuration file from another switch from path "/etc/sshd/".
- Copy public key manually to switch in the path "/home/<user>/.ssh/id_rsa.pub".
- Verify /var/log/auth.log for more information.
## CLI ##
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here](https://openswitch.net/cli_feature_name.html#cli_command_anchor) for the CLI commands related to the named feature - TBD
## Related features ##
<!-- Enter content into this section to describe features that may need to be considered in relation to this particular feature, under what conditions and why.  Provide a hyperlink to each related feature.  Sample text is included below as a potential example or starting point-->

Auto provisioning script is used to get ssh public keys, for more information on auto provisioning refer to : TBD Link -  [Auto Provisioning](https://openswitch.net./tbd/other_filefeatures/related_feature1.html#first_anchor)
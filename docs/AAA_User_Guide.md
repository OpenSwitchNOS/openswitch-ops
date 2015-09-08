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
This feature come into picture when user wants to login to the switch. This login can be either console login or SSH login. This feature provides

	- Local or radius authentication. 
	- Configure radius servers (maximum up-to 64 radius servers).
	- Configure SSH authentication method.
	 
 Authentication provides a way of identifying a user, typically by having the user enter a valid user name and valid password before access is granted. The process of authentication is based on each user having a unique set of criteria for gaining access. The AAA server compares a user's authentication credentials with other user credentials stored in a database. If the credentials match, the user is granted access to the network. If the credentials are at variance, authentication fails and network access is denied, it is based on PAP authentication protocol.

## How to use the feature ##
### Scenario 1 ###
###Setting up the basic configuration

 1. Create user on the switch and configure a password.
 2. Configure local/radius authentication.
 3. Configure radius servers.

###Setting up the optional configuration
 1. Admin can select his own shared secret between radius client(switch) and radius server.  
 2. Admin can select authentication port number for each radius server.
 3. Admin can select number of retries to radius servers.
 4. Admin can select timeout between each retry to radius server.

###Verifying the configuration

 1. Verify the configuration using show command
 2. Verify the configuration using show running-config command for non default values.

###Troubleshooting the configuration
### Case 1
#### Condition 
When local authentication configured, but unable to login with local password. 
#### Cause 
AAA daemon would have crashed, or pam configuration files are removed. User would have entered wrong password.
#### Remedy  
Verify if daemon is running, if crashed restart it.
If pam configuration files are removed, copy similar switch configuration files or power cycle the switch or load with a fresh image. Cross verify password. Verify auth.log for more information.

### Case 2 
#### Condition 
When radius authentication configured, but unable to login with radius server password. 
#### Cause 
AAA daemon would have crashed, or pam configuration files are removed.
Radius server would have been stopped or not reachable, difference in the configuration of radius server in the switch and the radius server running host. User would have entered wrong password.
#### Remedy  
Verify if daemon is running, if crashed restart it. If pam configuration files are removed, copy similar switch configuration files or power cycle the switch or load with a fresh image. Cross verify if radius server is reachable, if yes check if radius server is running and listening to requests. Verify radius server configuration on the switch and on the host. Verify auth.log for more information.

### Scenario 2 ###
###Setting up the basic configuration
 1. Enable radius authentication.
 2. Enable fallback to local authentication.
 3. Configure radius server.
###Setting up the optional configuration
N/A
###Verifying the configuration

 1. Verify using show commands.
 2. Verify using show running-config command 

###Troubleshooting the configuration
#### Condition 
When radius server is unreachable, user couldn't login with local credentials even though fallback to local is enabled.  
#### Cause 
User giving wrong local credentials. AAA daemon would have crashed, or pam configuration files are removed. 
#### Remedy  
Verify if daemon is running, if crashed restart it. If pam configuration files are removed, copy similar switch configuration files or power cycle the switch or load with a fresh image. Cross verify local credentials are correct or not. Verify auth.log for more information.

### Scenario 3 ###
###Setting up the basic configuration
 1. Enable ssh password or public key authentication method
 2. Create a user on the switch.
###Setting up the optional configuration
N/A
###Verifying the configuration

 1. Verify using show commands.
 2. Verify using show running-config command 

###Troubleshooting the configuration
### Case 1
#### Condition 
SSH password authentication is enabled, but user is not able to login with the password.
#### Cause 
User giving wrong credentials. AAA daemon would have crashed, or ssh configuration file is removed. 
#### Remedy  
Verify if daemon is running, if crashed restart it. If ssh configuration file is removed, copy similar switch ssh configuration file or power cycle the switch or load with a fresh image. Cross verify credentials are correct or not. Verify auth.log for more information.
### Case 2
#### Condition 
SSH public key authentication is enabled, but user is not able to login.
#### Cause 
User giving wrong credentials. AAA daemon would have crashed, or ssh configuration file is removed. Users public key is not present on the switch. 
#### Remedy  
Verify if daemon is running, if crashed restart it. If ssh configuration file is removed, copy similar switch ssh configuration file or power cycle the switch or load with a fresh image. Copy publick key manually or power cycle the switch. Verify auth.log for more information.
## CLI ##
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here](https://openswitch.net/cli_feature_name.html#cli_command_anchor) for the CLI commands related to the named feature.  
## Related features ##
(<!-- Enter content into this section to describe features that may need to be considered in relation to this particular feature, under what conditions and why.  Provide a hyperlink to each related feature.  Sample text is included below as a potential example or starting point.  -->
When configuring the switch for FEATURE_NAME, it might also be necessary to configure [RELATED_FEATURE1](https://openswitch.net./tbd/other_filefeatures/related_feature1.html#first_anchor) so that....


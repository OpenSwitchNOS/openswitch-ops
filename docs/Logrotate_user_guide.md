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
 
Log-rotate
=======
<!--Provide the title of the feature-->

 [TOC]

    Overview
    How to use the feature
    Setting up the basic configuration
    Setting up the optional configuration
    Verifying the configuration
 
## Overview ##
 <!--Provide an overview here. This overview should give the reader an introduction of when, where and why they would use the feature. -->
Logrotate as a feature, rotates and compresses the log files either based on period or based on size or based on both period and size (whichever condition triggers first). Rotated log files shall be stored locally or transferred to the remote destination.

## How to use the feature ##

With no initial configuration , logrotate shall be executed as a hourly cron job from /etc/cron.hourly with the following default configuration,

    h1# show logrotate 
    Logrotate configurations : 
    Period            : daily
    Maxsize           : 10MB

All rotated logs shall be stored locally

As per the above configuration,  default behavior is that log-rotate shall rotate log files daily. Log-rotation shall also be triggered with in a day if size of the file exceeds maximum size of 10 MB . Out of the period and size, which ever condition occurs first shall trigger log rotation.

###Setting up the basic configuration

User shall change the default threshold values for both period and size using the following CLIs,

 1. logrotate period (hourly| daily| weekly | monthly )
 2. logrotate maxsize <1-200>
  

###Setting up the optional configuration

User shall choose to send the rotated log files to remote host using the following CLI,

 1. logrotate target  { tftp://A.B.C.D | tftp://X:X::X:X }

 Only TFTP protocol is supported for remote transfer.
 Both IPv4 and IPv6 host addresses are supported.

###Verifying the configuration

Log-rotate configuration parameters shall be verified with the following command,

 1.show logrotate

    h1# show logrotate 
    Logrotate configurations : 
    Period            : weekly
    Maxsize           : 20MB
    Target            : tftp://2001:db8:0:1::128

Log-rotate configuration CLIs shall be verfied with the *show running-config* command

###Troubleshooting the configuration

#### Condition 1
<!-- Type the symptoms for the issue. -->

Log-rotation is not happening regardless of 'period' value.

#### Cause 
<!-- Type the cause for the issue. -->

Log-rotate will not happen for empty files (i.e if file size is zero)
#### Remedy  
<!--Type the solution. -->
Log-rotate will happen when file size becomes non-zero.

#### Condition 2
<!-- Type the symptoms for the issue. -->

Rotated log files are not transferred to remote host

#### Cause 
<!-- Type the cause for the issue. -->
1. Remote host may not be reachable
2. Tftp server in the remote host may not have sufficient privileges for file creation

#### Remedy  
<!--Type the solution. -->
1. Check and ensure that remote host is reachable.
2. Make sure that tftp server is configured with required file creation permission.
	1. For example in tftpd-hpa server, change the configuration file in '/etc/default/tftpd-hpa' to include '-c' in TFTP_OPTIONS. (ex., TFTP_OPTIONS="--secure -c")

#### Condition 3
<!-- Type the symptoms for the issue. -->

Log-rotation is not happening when size of the log file exceeds the configured 'maxsize' value.

#### Cause 
<!-- Type the cause for the issue. -->
Log-rotate being a hourly cron job, will check the size of the file once in a hour on first minute of every hour of the day. So log-rotation will not happen in the mean time.

#### Remedy  
<!--Type the solution. -->
No remedy as this is an expected behavior as per design.

## CLI ##
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here](https://openswitch.net/cli_feature_name
.html#cli_command_anchor) for the CLI commands related to the named feature.  

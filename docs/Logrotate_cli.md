
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
Log-rotate commands 
=======

<!--Provide the name of the grouping of commands, for example, LLDP commands-->

 [TOC]

    Configuration commands:
       logrotate period
       logrotate maxsize
       logrotate target

    Display commands:
       show logrotate

## Log-rotate Configuration Commands ##
<!-- Change logrotate -->
###  logrotate period ###
#### Syntax ####
<!--For example,    myprogramstart [option] <process_name> -->
    logrotate period ( hourly | weekly | monthly )
    no logrotate period ( hourly | weekly | monthly )
#### Description ####

   To configure log rotation based on time. Possible values are 'hourly', weekly' or  'monthly'. When time difference between the last rotation of a file and current time   exceeds the configured value, log rotation shall be triggered for that particular file.    To reset to the default value, use the 'no' form of the command.
#### Authority ####

    All users
#### Parameters ####

    'hourly'   Rotates log files every hour.
    'monthly'  Rotates log files every month.
    'weekly'   Rotates log files every week.

   If not specified, default value is 'daily'.
#### Examples ####

    switch(config)# logrotate period weekly
### logrotate maxsize ###
   
#### Syntax ####

   logrotate maxsize *filesize*

   no logrotate maxsize *filesize*
#### Description ####
<!--Provide a description of the command. -->
   To configure log rotation based on log file size. Log file size shall be checked once in a hour. When size of the log file exceeds the configured value, rotation shall be triggered for that particular log file. To reset to the default value, use the 'no' form of the command.   
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
   All user
#### Parameters ####
<!--Provide for the parameters for the command.-->
   *filesize*

   Specifies log rotate maximum file size in Mega Bytes (MB). The range is from 1 to 200 MB. If not specified, default value is 10MB
#### Examples ####
<!--    myprogramstart -s process_xyz-->
    switch(config)# logrotate maxsize 20

### logrotate target ###
   
#### Syntax ####

   logrotate target *URI*

   no logrotate target *URI*
#### Description ####
<!--Provide a description of the command. -->
   To configure remote host URI. If configured rotated log files shall be sent to the remote URI using 'tftp' protocol. If not specified, rotated and compressed log files shall be found locally in the path /var/log/. To disable sending to the remote host, use 'no' form of the command.
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
   All user
#### Parameters ####
<!--Provide for the parameters for the command.-->
   *URI*

   Specifies URI (Universal Resource Identifier) of the remote host. Possilbe values are     'tftp://A.B.C.D' or 'tftp://X:X::X:X'. Both IPv4 and IPv6 addresess are supported

#### Examples ####
<!--    myprogramstart -s process_xyz-->
    switch(config)# logrotate target tftp://192.168.1.132
    switch(config)# logrotate target tftp://2001:db8:0:1::128

##Display Commands ##
### show logrotate ###
<!--Change the value of the anchor tag above, so this command can be directly linked. -->
#### Syntax ####
<!--For example,    myprogramstart [option] <process_name> -->
     show logrotate
#### Description ####
<!--Provide a description of the command. -->
   Displays logrotate configuration parameters.
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
     All users
#### Parameters ####
<!--Provide for the parameters for the command.-->
#### Examples ####
<!--    myprogramstart -s process_xyz-->
    h1# show logrotate 
    Logrotate configurations : 
    Period            : weekly
    Maxsize           : 20MB
    Target            : tftp://2001:db8:0:1::128



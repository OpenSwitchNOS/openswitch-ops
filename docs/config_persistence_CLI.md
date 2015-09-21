#CLI support for Config Persistence
## Contents##
- [1. Copy commands](#1.-copy-commands)
    - [1.1 Copy startup configuration to running configuration](#1.1-copy-startup-configuration-
to-running-configuration)
    - [1.2 Copy running configuration to startup configuration](#1.2-copy-running-configuration-
to-startup-configuration)
- [2. Show commands](#2.-show-commands)
    - [2.1 Show startup configuration](#2.1-show-startup-configuration)

## 1. Copy commands ##
###1.1 Copy startup configuration to running configuration
#### Syntax ####
copy startup-config running-config

#### Description ####
<!--Provide a description of the command. -->
This command is used to copy the content of startup configuration to current system running configuration.
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
Admin
#### Parameters ####
<!--Provide for the parameters for the command.-->
None

#### Examples ####
```bash
as5712 # copy startup-config running-config
```

###1.2 Copy running configuration to startup configuration
#### Syntax ####
<!--For example,    myprogramstart [option] <process_name> -->
copy running-config startup-config

#### Description ####
<!--Provide a description of the command. -->
This command is used to copy the content of current system running configuration to startup configuration.
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
Admin
#### Parameters ####
<!--Provide for the parameters for the command.-->
None

#### Examples ####
```bash
as5712 # copy running-config startup-config
```

##2. Show Commands ##
<!-- Change LLDP -->
###2.1 Show startup configuration
#### Syntax ####
<!--For example,    myprogramstart [option] <process_name> -->
show startup-config

#### Description ####
<!--Provide a description of the command. -->
To display the saved startup configuration in JSON format

#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
Admin
#### Parameters ####
<!--Provide for the parameters for the command.-->
None

#### Examples ####
```bash
as5712 # show startup-config
```

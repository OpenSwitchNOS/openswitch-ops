# Autoprovisioning

- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
    - [Setting up the basic configuration](#setting-up-the-basic-configuration)
    - [Verifying the configuration](#verifying-the-configuration)
    - [Writing autoprovisioning script](#writing-autoprovisioning-script)
        - [API](#api)
        - [Example](#example)
            - [VTYSH](#vtysh)
            - [WGET](#wget)
            - [LOGGER](#logger)
        - [Sample script file](#sample-script-file)
    - [Troubleshooting the configuration](#troubleshooting-the-configuration)
        - [Condition](#condition)
        - [Cause](#cause)
- [CLI](#cli)
- [Related features](#related-features)

## Overview ##
Autoprovisioning (a.k.a Zero Touch Provisioning - ZTP)  is a feature that enables automatic provisioning of switch when it is deployed. Using a DHCP option advertised by DHCP server in the setup, the switch downloads a provisioning script and executes it. The provisioning script can do many things, such as new management users, downloading `ssh` keys, installing a server certificate, etc. This feature is mainly used to download `ssh` keys and add user ids to the switch enabling key based authentication of management users.

## How to use the feature ##
###Setting up the basic configuration

The feature is enabled by default and cannot be turned off through CLI. To disable the autoprovisioning feature, configure the DHCP server to NOT send option 239 in the DHCP reply/ack messages.


###Verifying the configuration

Not applicable.

###Writing autoprovisioning script
- Shell, Perl or Python scripts are supported as auto-provisioning script.
- It is assumed that the first line of the script contains entries like `#!/bin/sh` to distinguish between a shell, perl and python scripts.
- The provisioning script must contain a line `OPS-PROVISIONING` as a comment. This is for a very rudimentary validation that we got a valid provisioning script.
- The script is executed on the linux shell prompt of the switch.

#### API
In the script the following executables can be used to configure CLI commands in the switch(VTYSH), to download other files from outside the switch(WGET) and to log the appropriate ZTP messages(LOGGER).
```
VTYSH=/usr/bin/vtysh
WGET=/usr/bin/wget
LOGGER=/usr/bin/logger
```

#### Example
##### VTYSH
- Use $VTYSH to configure CLI commands.
- Now suppose we want to configure the following configuration:
```
vlan 2
    no shutdown
interface 3
    no shutdown
    no routing
    vlan trunk native 1
    vlan trunk allowed 2
```
- In the switch’s linux shell prompt execute the below command:
```
root@switch:~# $VTYSH -c "configure terminal" -c "vlan 2" -c "no shutdown"  -c "interface 3" -c "no shutdown" -c "no routing" -c "vlan trunk allowed 2" -c "exit"
```
- Since autoprovisioning script will get executed on the shell prompt so automating a script to read the CLI configuration from a separately downloaded config file and run the CLI commands like above is fairly easy task.

##### WGET
- Use WGET to download config file/SSH keys:
- Shell commands like wget can be used to download any type of file into switch.
```
$WGET <Link to config/SSH key file> -O <File-name>
```

##### LOGGER
- Logging events:
```
$LOGGER -i "MESSAGE that needs to be documented"
```

#### Sample script file
```
#!/bin/sh

# OPS-PROVISIONING
# Sample auto-provisioning script for Openswitch.

# executable files used by this script
VTYSH=/bin/vtysh
WGET=/usr/bin/wget
LOGGER=/usr/bin/logger

<---- Complete the script to read configuration file and apply on switch using VTYSH and/or download SSH key files and save in it ---->
```

###Troubleshooting the configuration

#### Condition
Autoprovisioning is not performed.
#### Cause
- The DHCP option 239 not configured on the DHCP server.

Verify whether DHCP server is correctly configured.

- Provisioning script does not contain the line `OPS-PROVISIONING`.

Please verify the provisioning script.
## CLI ##
Click [ here](/documents/user/autoprovision_CLI) for the CLI commands related to the named feature.

## Related features ##
None.

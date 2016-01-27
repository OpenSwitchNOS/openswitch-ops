# NTP

[TOC]

## Overview  ##
We are supporting the NTP Client functionality on the switch.
The switch will synchronize its time with a NTP server using the NTP protocol over a (WAN or LAN) UDP Network.

## Prerequisites  ##
An NTP server (either local or remote) will be needed to which the switch can synchronize its time with.

## Limitations ##
1. We are supporting the NTP Client functionality alone.
2. A maximum of 8 servers can be configured to synchronize from.

## Defaults ##
NTP is enabled by default and cannot be disabled.
NTP authentication is disabled by default.
Default NTP version used is 3.

## Limitations ##
Currently only IPV4 is supported.

## Configuring NTP Client ##
Configure the terminal to change the vtysh context to config context with the following commands:
```
switch# configure terminal
switch(config)#
```

### Enabling NTP ###
NTP is enabled by default and cannot be disabled.

### Adding a server ###
Add a NTP server with the following command:
```
switch(config)# ntp server <FQDN/IPV4 address> [key _key-id_] [version _version-no_] [prefer]
```
—Server name can be max 57 characters long.
—IPV4 address, if mentioned, needs to be of a valid format.
—Default version is 3. (Only 3 or 4 are acceptable values).

### Configuring NTP Authentication ###
The switch can be configured to authenticate the NTP server to which it will synchronize.
The NTP server should have been previously configured with some authentication keys.
One of this key will be mentioned while adding this server on the switch.
When NTP authentication is enabled, the switch will synchronize to the NTP server only if the switch has an authentication key specified as a trusted-key.
Without this, NTP packets will be dropped due to authentication check failure.
```
switch(config)# ntp authentication enable
```

NTP authentication can be disabled using the corresponding _no_ command.
```
switch(config)# no ntp authentication enable
```

### Verifying the configuration ###
#### Viewing NTP global information
The `show ntp status` command displays global NTP configuration.
```
switch# show ntp status
```

## CLI ##
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here](/documents/user/ntp_cli) for the CLI commands related to the NTP feature.
## Related features  ##
None

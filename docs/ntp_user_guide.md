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
3. Currently only IPV4 is supported.
4. Currently only default VRF is supported.

## Defaults ##
1. NTP is enabled by default and cannot be disabled.
2. NTP authentication is disabled by default.
3. Default NTP version used is 3.

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
- Server name can be a maximum of 57 characters long.
- IPV4 address, if mentioned, needs to be of a valid format.
- Default version is 3. (Only 3 or 4 are acceptable values).
### Deleting a server ###
A previously added NTP server can be deleted using the following command:
```
switch(config)# no ntp server <FQDN/IPV4 address>
```

### Enabling NTP Authentication ###
The switch can be configured to authenticate the NTP server to which it will synchronize.
The NTP server should have been previously configured with some authentication keys.
One of these keys will be mentioned while adding this server on the switch.
When NTP authentication is enabled, the switch will synchronize to the NTP server only if the switch has an authentication key specified as a trusted-key.
Without this, NTP packets will be dropped due to authentication check failure.
```
switch(config)# ntp authentication enable
```
### Disabling NTP Authentication ###
NTP authentication can be disabled using the corresponding _no_ command.
```
switch(config)# no ntp authentication enable
```

### Adding NTP Authentication-Key ###
When NTP authentication is enabled on the switch, the incoming NTP packets are authenticated using an authentication key.
This key needs to be marked as "trusted" as well & must be same key previously configured on the NTP server.
```
switch(config)# ntp authentication-key <_key-id_> md5 <_password_>
```
- _key-id_ should lie between [1-65534].
- _password_ should be an alphanumeric string which 8-16 characters long.
### Deleting NTP Authentication-Key ###
A previously configured authentication-key can be deleted by using the following command:
```
switch(config)# no ntp authentication-key <_key-id_>
```

### Adding NTP Trusted-Key ###
A previously configured authentication-key can be marked as a "trusted key" using the following command:
```
switch(config)# ntp trusted-key <_key-id_>
```
### Deleting NTP Trusted-Key ###
A previously configured trusted-key can be unmarked as "trusted" using the following command:
```
switch(config)# no ntp trusted-key <_key-id_>
```

## Verifying the configuration ###
### Viewing NTP global information
The `show ntp status` command displays global NTP configuration.
```
switch# show ntp status
NTP has been enabled
NTP Authentication has been enabled
Uptime: 2 hrs
```
In case the switch has synchronized its time with a NTP server, then those details too will be displayed herein -
```
switch# show ntp status
NTP has been enabled
NTP Authentication has been enabled
Uptime: 2 hrs
Synchronized to NTP Server 10.93.55.11 at stratum 4
Poll interval = 1024 seconds
Time accuracy is within 1.676 seconds
Reference time: Wed Jan 27 2016 19:01:48.647
```

### Viewing NTP servers
The `show ntp associations` command will display the configured servers.
The server to which the switch has synced to will be marked with a `*` in the beginning.
```
switch# show ntp associations
----------------------------------------------------------------------------------------------------------------------
  ID             NAME           REMOTE  VER  KEYID           REF-ID  ST  T  LAST  POLL  REACH    DELAY  OFFSET  JITTER
----------------------------------------------------------------------------------------------------------------------
*  1      10.93.55.11      10.93.55.11    4      -     16.77.112.61   4  U   728  1024    377    1.779   2.512   3.537
   2    17.253.38.253    17.253.38.253    4      -           .INIT.  16  -     -  1024      0    0.000   0.000   0.000
   3    198.55.111.50    198.55.111.50    4      -           .INIT.  16  -     -  1024      0    0.000   0.000   0.000
----------------------------------------------------------------------------------------------------------------------
```

### Viewing NTP authentication keys
The `show ntp authentication-keys` command will display the configured auth-keys.
```
switch# show ntp authentication-keys
---------------------------
Auth-key       MD5 password
---------------------------
       2     aNicePassword2
       3      aNewPassword3
---------------------------
```

### Viewing NTP trusted keys
The `show ntp trusted-keys` command will display the configured auth-keys.
```
switch# show ntp trusted-keys
------------
Trusted-keys
------------
2
------------
```

### Viewing NTP statistics
The `show ntp statistics` command will display the configured auth-keys.
```
switch# show ntp statistics
             Rx-pkts    224513
     Cur Ver Rx-pkts    146
     Old Ver Rx-pkts    0
          Error pkts    0
    Auth-failed pkts    0
       Declined pkts    0
     Restricted pkts    0
   Rate-limited pkts    0
            KOD pkts    0
```

## Troubleshooting NTP
Depending on the NTP server that the switch is trying to synchronize time from, it can take a while before the transaction is a success.
Time taken for synchronization can vary from 64-1024 seconds

`show ntp statistics` should show increase in Rx packets for some activity to proceed.
Also increase in pkt drops suggests erroneous configurations/conditions.
For example:
          Rx-pkts - Total NTP pkts received
  Cur Ver Rx-pkts - Number of NTP pkts that match the current NTP version
  Old Ver Rx-pkts - Number of NTP pkts that match the previous NTP version
       Error pkts - Pkts dropped due to all other error reasons
 Auth-failed pkts - Pkts dropped due to auth-failure
    Declined pkts - Pkts denied access for any reason
  Restricted pkts - Pkts dropped due to NTP access control
Rate-limited pkts - Number of packets discarded due to rate limitation
         KOD pkts - Number of Kiss of Death packets

When the switch successfully synchronizes to a server, the corresponding status is displayed as part of `show ntp status`

Also the REF-ID field in the output for `show ntp associations` carries suggestive values.
For the list of values that it can take, refer to -
http://doc.ntp.org/4.2.6p5/refclock.html

For general debuggability of NTPd, refer to -
http://doc.ntp.org/4.2.6p5/debug.html


## CLI ##
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here](/documents/user/ntp_cli) for the CLI commands related to the NTP feature.
## Related features  ##
None

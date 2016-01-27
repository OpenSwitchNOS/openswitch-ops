# NTP

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Limitations](#limitations)
- [Defaults](#defaults)
- [Configuring an NTP client](#configuring-an-ntp-client)
	- [Enabling NTP](#enabling-ntp)
	- [Adding a server](#adding-a-server)
	- [Deleting a server](#deleting-a-server)
	- [Enabling NTP authentication](#enabling-ntp-authentication)
	- [Disabling NTP authentication](#disabling-ntp-authentication)
	- [Adding an NTP authentication key](#adding-an-ntp-authentication-key)
	- [Deleting an NTP authentication key](#deleting-an-ntp-authentication-key)
	- [Adding an NTP trusted key](#adding-an-ntp-trusted-key)
	- [Deleting an NTP trusted key](#deleting-an-ntp-trusted-key)
- [Verifying the configuration](#verifying-the-configuration)
	- [Viewing NTP global information](#viewing-ntp-global-information)
	- [Viewing NTP servers](#viewing-ntp-servers)
	- [Viewing NTP authentication keys](#viewing-ntp-authentication-keys)
	- [Viewing NTP trusted keys](#viewing-ntp-trusted-keys)
	- [Viewing NTP statistics](#viewing-ntp-statistics)
- [Troubleshooting NTP](#troubleshooting-ntp)
	- [Scenario 1](#scenario-1)
	- [Generic tips for troubleshooting](#generic-tips-for-troubleshooting)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
The NTP Client functionality is supported on the switch.
The switch synchronizes its time with a NTP server using the NTP protocol over a (WAN or LAN) UDP network.

## Prerequisites
An NTP server (either local or remote) is needed with which the switch can synchronize its time.

## Limitations
1. Only the NTP Client functionality alone is supported.
2. A maximum of eight servers can be configured from which to synchronize.
3. Currently only IPV4 is supported.
4. Currently only default VRF is supported.

## Defaults
1. NTP is enabled by default and cannot be disabled.
2. NTP authentication is disabled by default.
3. The default NTP version used is 3.

## Configuring an NTP client
Configure the terminal to change the CLI context to config context with the following commands:
```
switch# configure terminal
switch(config)#
```

### Enabling NTP
NTP is enabled by default and cannot be disabled.

### Adding a server
Add a NTP server with the following command:
```
switch(config)# ntp server <FQDN/IPV4 address> [key _key-id_] [version _version-no_] [prefer]
```
- The server name can be a maximum of 57 characters long.
- The IPv4 address, if included, needs to be of a valid format.
- Default version is 3. (Only versions 3 or 4 are acceptable values.)

### Deleting a server
A previously added NTP server can be deleted using the following command:
```
switch(config)# no ntp server <FQDN/IPV4 address>
```

### Enabling NTP authentication
The switch can be configured to authenticate the NTP server to which it will synchronize.
The NTP server should already be configured with some authentication keys.
One of these keys will be used when adding the server on the switch.
When NTP authentication is enabled, the switch synchronizes to the NTP server only if the switch has an authentication key specified as a trusted-key.
Without this, NTP packets are dropped due to authentication check failure.
```
switch(config)# ntp authentication enable
```
### Disabling NTP authentication
NTP authentication can be disabled using the corresponding `no` command.
```
switch(config)# no ntp authentication enable
```

### Adding an NTP authentication key
When NTP authentication is enabled on the switch, the incoming NTP packets are authenticated using an authentication key.
This key needs to be marked as "trusted", and must be the same key previously configured on the NTP server.
```
switch(config)# ntp authentication-key <_key-id_> md5 <_password_>
```
- _key-id_ should be between 1 to 65534.
- _password_ should be an alphanumeric string between 8 to 16 characters long.

### Deleting an NTP authentication key
A previously configured authentication key can be deleted by using the following command:
```
switch(config)# no ntp authentication-key <_key-id_>
```

### Adding an NTP trusted key
A previously configured authentication key can be marked as a "trusted key" using the following command:
```
switch(config)# ntp trusted key <_key-id_>
```
### Deleting an NTP trusted key
A previously configured trusted key can be unmarked as "trusted" using the following command:
```
switch(config)# no ntp trusted-key <key-id>
```

## Verifying the configuration
### Viewing NTP global information
The `show ntp status` command displays global NTP configuration.
```
switch# show ntp status
NTP has been enabled
NTP Authentication has been enabled
Uptime: 2 hrs
```
In case the switch has synchronized its time with an NTP server, then those details are also displayed:
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
The `show ntp associations` command displays the configured servers.
The server to which the switch has synced is marked with a `*` in the beginning.
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
The `show ntp authentication-keys` command displays the configured authentication keys.
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
The `show ntp trusted-keys` command displays the configured trusted authorization keys.
```
switch# show ntp trusted-keys
------------
Trusted-keys
------------
2
------------
```

### Viewing NTP statistics
The `show ntp statistics` command displays the NTP statistics.
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
### Scenario 1
NTP association is stuck in the `.INIT.` state:
```
switch# show ntp associations
----------------------------------------------------------------------------------------------------------------------
  ID             NAME           REMOTE  VER  KEYID           REF-ID  ST  T  LAST  POLL  REACH    DELAY  OFFSET  JITTER
----------------------------------------------------------------------------------------------------------------------
   2    17.253.38.253    17.253.38.253    4      -           .INIT.  16  -     -  1024      0    0.000   0.000   0.000
   3    198.55.111.50    198.55.111.50    4     33           .INIT.  16  -     -  1024      0    0.000   0.000   0.000
----------------------------------------------------------------------------------------------------------------------
```
If authentication is not enabled:
    - reverify if the server is reachable (Rx packets are incrementing in `show ntp statistics` output)
    - reverify if the version mentioned for the server is supported by the server

If authentication is enabled:
    - reverify if the server is reachable (Rx packets are incrementing in `show ntp statistics` output)
    - reverify if the version mentioned for the server is supported by the server
    - reverify if the key mentioned is the one that has been previously configured on the server
    - reverify if the password mentioned while configuring the authentication-key matches too
    - reverify if this key has been marked as "trusted".

### Generic tips for troubleshooting
Depending on the NTP server from which the switch is trying to synchronize time, it can take awhile before the transaction is successful.
Time taken for synchronization can vary from 64 to 1024 seconds.

The `show ntp statistics` command should show increase in Rx packets for some activity to proceed.
An increase in packet drops suggests erroneous configurations or conditions.
For example:
          Rx-pkts - Total NTP packets received.
  Cur Ver Rx-pkts - Number of NTP packets that match the current NTP version.
  Old Ver Rx-pkts - Number of NTP packets that match the previous NTP version.
       Error pkts - Packets dropped due to all other error reasons.
 Auth-failed pkts - Packets dropped due to authentication failure.
    Declined pkts - Packets denied access for any reason.
  Restricted pkts - Packets dropped due to NTP access control.
Rate-limited pkts - Number of packets discarded due to rate limitation.
         KOD pkts - Number of Kiss of Death packets.

When the switch successfully synchronizes to a server, the corresponding status is displayed as part of `show ntp status`.

The REF-ID field in the output for `show ntp associations` carries suggestive values.
For the list of values that it can take, refer to -
http://doc.ntp.org/4.2.6p5/refclock.html

For general debugging information of NTP, refer to -
http://doc.ntp.org/4.2.6p5/debug.html


## CLI
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here](/documents/user/ntp_cli) for the CLI commands related to the NTP feature.
## Related features
None

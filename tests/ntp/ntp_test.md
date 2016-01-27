NTP Feature test cases
========

## Contents

- [NTP configuration without authentication](#ntp configuration without authentication)


## NTP configuration without authentication

### Objective
The test case checks if the switch is configured as an ntp client and is successfully configured with ntp server.


#### Requirements
- Virtual mininet test setup with a workstation which can host as an NTP server
- **FT file**: ops/tests/ntp/test_ft_ntp_noauth.py


#### Setup
##### Topology diagram
```
   +------------+
   |            |
   |  Switch    |
   |            |
   +------------+
         |
         |
   +-----------+
   |           |
   |   Host    |
   |           |
   +-----------+
```


####Test Setup

#####NTP server setup

1. NTP server should be configured with following parameters in the /etc/ntp.conf file

```
restrict default nomodify notrap noquery
restrict ::1
restrict 127.0.0.1
driftfile /var/lib/ntp/ntp.drift
logfile /var/log/ntp.log
broadcastdelay  0.008
keys /etc/ntp.keys
trustedkey 12
server 10.93.55.11 prefer
fudge   127.127.1.0 stratum 10
fudge   127.127.1.0 stratum 10

```

2. The /etc/ntp.keys file in the NTP server should have the appropriate key which can be used for authntication
for example,

```
10 MD5 NtpPassword
```

3. Start the ntpd service and verify the service is running on the server

```
# ntpd -c /etc/ntp.conf

# ps -ef

UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 03:39 ?        00:00:00 /bin/bash
root        16     0  0 03:39 ?        00:00:00 /bin/bash --rcfile /shared/minin
root        23     0  1 03:39 ?        00:00:00 /bin/bash
root        38     1  1 03:39 ?        00:00:00 ntpd -c /etc/ntp.conf
root        40    23  0 03:39 ?        00:00:00 ps -ef
```

4. Verify that the NTP server provided in the ntp.conf file is configured properly

```
# ntpq -p
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*10.93.55.11     16.77.112.61     4 u    -   64    1    4.152    2.758   0.000

```


##### NTP Client setup

1. Configure switch as a NTP client and add NTP server IP address as a preferred IP address

```
configure terminal
ntp server 198.55.111.50
ntp server <ntp_server_ip> prefer
ntp server 17.253.38.253 version 4

```


### Test result criteria

#### Test pass criteria

The test case is considered passing if the NTP server configured for the client has an appropriate REF-ID
Confirm that the preferred server is configured properly without any errors in REF-ID

```

switch# show ntp associations
----------------------------------------------------------------------------------------------------------------------
  ID             NAME           REMOTE  VER  KEYID           REF-ID  ST  T  LAST  POLL  REACH    DELAY  OFFSET  JITTER
----------------------------------------------------------------------------------------------------------------------
*  1       172.17.0.4       172.17.0.4    3      -      10.93.55.11   5  -     7    64      1    0.404   0.164   0.000
   2    198.55.111.50    198.55.111.50    4      -           .INIT.  16  -     -    64      0    0.000   0.000   0.000
   3    17.253.38.253    17.253.38.253    3      -           .INIT.  16  -     -    64      0    0.000   0.000   0.000
----------------------------------------------------------------------------------------------------------------------

```

#### Test fail criteria

If the REF-ID status is .NKEY., .INIT., .TIME.,.RATE. or .AUTH., there is an issue with connecting to NTP server.


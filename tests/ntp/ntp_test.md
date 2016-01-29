# NTP Feature Test Cases

## Contents

- [NTP configuration without authentication](#ntp-configuration-without-authentication)
	- [Objective](#objective)
		- [Requirements](#requirements)
		- [Setup](#setup)
			- [Topology diagram](#topology-diagram)
		- [Test setup](#test-setup)
			- [NTP server setup](#ntp-server-setup)
			- [NTP client setup](#ntp-client-setup)
	- [Test result criteria](#test-result-criteria)
		- [Test pass criteria](#test-pass-criteria)
		- [Test fail criteria](#test-fail-criteria)

- [NTP configuration with authentication](#ntp-configuration-with-authentication)
	- [Objective](#objective)
		- [Requirements](#requirements)
		- [Setup](#setup)
			- [Topology diagram](#topology-diagram)
		- [Test setup](#test-setup)
			- [NTP server setup](#ntp-server-setup)
			- [NTP client setup](#ntp-client-setup)
	- [Test result criteria](#test-result-criteria)
		- [Test pass criteria](#test-pass-criteria)
		- [Test fail criteria](#test-fail-criteria)

## NTP configuration without authentication

### Objective
The test case checks if the switch is configured as a Network Time Protocol (NTP) client and if the switch is successfully configured with NTP server.


#### Requirements
- Virtual Mininet test setup with a workstation that can host as an NTP server
- **FT file**: `ops/tests/ntp/test_ft_ntp_noauth.py`


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


#### Test setup

##### NTP server setup

1. The NTP server should be configured with the following parameters in the `/etc/ntp.conf` file.

 ```
keys /etc/ntp.keys
trustedkey <key-id>
server <server_ip> prefer
 ```

2. The `/etc/ntp.keys` file in the NTP server should have the appropriate key that can be used for authentication.
For example:

 ```
<key-id> MD5 MyNtpPassword

 ```

3. Start the NTPD service and verify the service is running on the server.

 ```
 # ntpd -c /etc/ntp.conf

 ```
  
4. Verify that the NTP server provided in the ntp.conf file is configured properly.

 ```
  # ntpq -p

       remote           refid      st t when poll reach   delay   offset  jitter
  ==============================================================================
  *<server_ip>     <valid ref-id>   4 u    -   64    1    4.152    2.758   0.000

 ```


##### NTP client setup

Configure the switch as an NTP client and add the NTP server's IP address as a preferred IP address.

  ```
  configure terminal
  ntp server <ntp_server_ip>
  ntp server <ntp_server_ip> prefer
  ntp server <ntp_server_ip> version 4
  ```


### Test result criteria

#### Test pass criteria

- The test case is considered passing if the NTP server configured for the client has an appropriate REF-ID.
- One more way to confirm the server configuration is to check the ntp status and check if the clock is synchronized
with the ntp server

Example output:

```
 
switch# show ntp associations
----------------------------------------------------------------------------------------------------------------------
  ID             NAME           REMOTE  VER  KEYID           REF-ID  ST  T  LAST  POLL  REACH    DELAY  OFFSET  JITTER
----------------------------------------------------------------------------------------------------------------------
*  1       172.17.0.4       172.17.0.4    3      -      10.93.55.11   5  -     7    64      1    0.404   0.164   0.000
   2    198.55.111.50    198.55.111.50    4      -           .INIT.  16  -     -    64      0    0.000   0.000   0.000
   3    17.253.38.253    17.253.38.253    3      -           .INIT.  16  -     -    64      0    0.000   0.000   0.000
----------------------------------------------------------------------------------------------------------------------


switch# show ntp status

NTP has been enabled
NTP Authentication has been enabled
Synchronized to NTP Server 172.17.0.4 at stratum 5
Poll interval = 64 seconds
Time accuracy is within 0.016 seconds
Reference time: Thu Jan 27 2016 20:32:55.639
```

#### Test fail criteria

If the REF-ID status is .NKEY., .INIT., .TIME.,.RATE. or .AUTH., there is an issue with connecting to the NTP server.




## NTP configuration with authentication

### Objective

The test case checks if the switch is configured as a Network Time Protocol (NTP) client and if the switch is successfully configured with NTP server with authentication.



#### Setup
##### Topology diagram
```
   +------------+    +-----------+
   |            |    |           |
   |  Switch    |----|   Host1   | 
   |            |    |   (auth)  | 
   +------------+    +-----------+
         |
         |
   +-----------+
   |           |
   |   Host2   |
   |           |
   +-----------+
```


#### Test setup

##### NTP server setup

We have setup two NTP servers using Host1 and Host2.

1. The NTP servers should be configured with the following parameters in the `/etc/ntp.conf` file.

 ```
authenticate yes
keys /etc/ntp.keys
trustedkey <key-id>
server <server_ip> prefer
 ```

2. The `/etc/ntp.keys` file in the NTP server should have the appropriate key that can be used for authentication.
For example:

 ```
<key-id> MD5 MyNtpPassword
 ```

3. Start the NTPD service and verify the service is running on the server.

 ```
  # ntpd -c /etc/ntp.conf

 ```
  
4. Verify that the NTP server provided in the ntp.conf file is configured properly.

 ```
  # ntpq -p

       remote           refid      st t when poll reach   delay   offset  jitter
  ==============================================================================
  *<server_ip>     <valid ref-id>   4 u    -   64    1    4.152    2.758   0.000

 ```


##### NTP client setup

Configure the switch as an NTP client and add both the NTP server's IP address as a preferred IP address.

  ```
  configure terminal
  ntp authentication-key <key-id> md5 <myNtpPassword>
  ntp trusted-key <key-id>
  ntp authentication enable
  ntp server <ntp_server_ip1> version 4
  ntp server <ntp_server_ip2> prefer
  ntp server <ntp_server_ip3> prefer key-id <key-id> 
  ```


### Test result criteria

#### Test pass criteria

1. The test case is considered passing if the NTP server configured for the client has an appropriate REF-ID.
Confirm that the preferred server is configured properly without any errors in the REF-ID column.

2. One more way to confirm the working configuration is to check the ntp status and check if the clock is synchronized
with the ntp server

Example output:

```
 
switch# show ntp associations
----------------------------------------------------------------------------------------------------------------------
  ID             NAME           REMOTE  VER  KEYID           REF-ID  ST  T  LAST  POLL  REACH    DELAY  OFFSET  JITTER
----------------------------------------------------------------------------------------------------------------------
* 1       172.17.0.2       172.17.0.2    3     55   15.203.224.212   3  -     -    64      0    0.000   0.000   0.000
  2       172.17.0.3       172.17.0.3    3      -   15.203.224.212  16  -    66    64      7    0.126   0.029   0.016
----------------------------------------------------------------------------------------------------------------------

switch# show ntp status

NTP has been enabled
NTP Authentication has been enabled
Synchronized to NTP Server 172.17.0.2 at stratum 3
Poll interval = 64 seconds
Time accuracy is within 0.016 seconds
Reference time: Thu Jan 28 2016 20:32:55.639

```

#### Test fail criteria

If the REF-ID status is .NKEY., .INIT., .TIME.,.RATE. or .AUTH., there is an issue with connecting to the NTP server.

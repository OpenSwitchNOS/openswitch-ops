# Copy Core Dump CLI Guide

## Contents
- [Copy Core Dump CLI Guide](#copy-core-dump-cli-guide)
	- [Contents](#contents)
		- [copy coredump to tftp, destination file unspecified](#copy-coredump-to-tftp-destination-file-unspecified)
		- [copy daemon coredump to destination tftp server, destination file specified](#copy-daemon-coredump-to-destination-tftp-server-destination-file-specified)
		- [copy core dump using sftp , destination file unspecified](#copy-core-dump-using-sftp-destination-file-unspecified)
		- [copy core dump using sftp , destination file specified](#copy-core-dump-using-sftp-destination-file-specified)
		- [copy coredump help string](#copy-coredump-help-string)

### copy coredump to tftp, destination file unspecified

#### Syntax
```
copy core-dump  <DAEMONNAME>  tftp  <tftp server ipiv4 address /host name>
```

#### Description
This cli copy daemon coredump  to destination tftp server .  It saves
destination file name same as source file name .

#### Authority
All users.

#### Parameters
daemon name
tftp server address

#### Examples
```
switch# copy core-dump ops-fand  tftp 172.17.0.1
Verbose mode on.
mode set to octet
putting /tmp/core/ops-fand/ops-fand.1.20160321.032825.11.core.tar.gz to 172.17.0.1:ops-fand.1.20160321.032825.11.core.tar.gz [octet]
Sent 447468 bytes in 0.1 seconds [35797440 bits/sec]
switch#
```

If there are no core dumps to present, the following information appears:
<daemon> don't have core file
```
switch# copy core-dump ops-abc  tftp 172.17.0.1
ops-abc don't have core file
switch#
```

### copy daemon coredump to destination tftp server, destination file specified

#### Syntax
```
copy core-dump <DAEMONNAME> tftp <tftp server ipv4 address / hostname > <FILENAME>
```

#### Description
This cli copy daemon coredump to daestination tftp server. It saves destination
file as given name .

#### Authority
All users.

#### Parameters
daemon name
tftp server address
destination file name

#### Examples

```
switch# copy core-dump ops-fand  tftp   172.17.0.1    ops-fand.core.tar.gz
Verbose mode on.
mode set to octet
putting /tmp/core/ops-fand/ops-fand.1.20160321.032825.11.core.tar.gz to 172.17.0.1:ops-fand.core.tar.gz [octet]
Sent 447468 bytes in 0.1 seconds [35797440 bits/sec]

```

If there are no core dumps to present, the following information appears:

```
switch# copy core-dump ops-abc  tftp 172.17.0.1 abc.tar.gz
ops-abc don't have core file
switch#
```

### copy core dump using sftp , destination file unspecified

#### Syntax
```
copy core-dump <DAEMONNAME>  sftp <USERNAME> <sshd server ipv address / host name >
```

#### Description
This cli copy daemon coredump  to destination sftp server .  It saves
destination file name same as source file name .

#### Authority
All users.

#### Parameters
daemon name
user name
sshd server address

#### Examples

```
switch# copy core-dump ops-fand  sftp naiksat  172.17.0.1
The authenticity of host '172.17.0.1 (172.17.0.1)' can't be established.
ECDSA key fingerprint is SHA256:uWeyXm2j6VkDfCitlyz/P+xGgZW9YYw5GnDOsEgVHeU.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '172.17.0.1' (ECDSA) to the list of known hosts.
naiksat@172.17.0.1's password:
Connected to 172.17.0.1.
sftp> put /tmp/core/ops-fand/ops-fand.1.20160321.032825.11.core.tar.gz ops-fand.1.20160321.032825.11.core.tar.gz
Uploading /tmp/core/ops-fand/ops-fand.1.20160321.032825.11.core.tar.gz to /users/naiksat/ops-fand.1.20160321.032825.11.core.tar.gz
/tmp/core/ops-fand/ops-fand.1.20160321.032825.11.core.tar.gz                                                                                                       100%  437KB 437.0KB/s   00:00
switch#
```

If there are no core dumps to present, the following information appears:

```
switch# copy core-dump ops-abc  sftp naiksat 172.17.0.1
ops-abc don't have core file
switch#
```

### copy core dump using sftp , destination file specified

#### Syntax
```
copy core-dump <DAEMONNAME>  sftp <USERNAME> <sshd server ipv address / host name >  <FILENAME>

```

#### Description
This cli copy daemon coredump  to destination tftp server .  It saves
destination file name same as given name .

#### Authority
All users.

#### Parameters
daemon name
user name
sshd server address
destination file name

#### Examples

```
switch# copy core-dump ops-fand  sftp naiksat  172.17.0.1    ops-fand.core.tar.gz
naiksat@172.17.0.1's password:
Connected to 172.17.0.1.
sftp> put /tmp/core/ops-fand/ops-fand.1.20160321.032825.11.core.tar.gz ops-fand.core.tar.gz
Uploading /tmp/core/ops-fand/ops-fand.1.20160321.032825.11.core.tar.gz to /users/naiksat/ops-fand.core.tar.gz
/tmp/core/ops-fand/ops-fand.1.20160321.032825.11.core.tar.gz                                                                                                       100%  437KB 437.0KB/s   00:00
switch# copy core-dump ops-fand  tftp   172.17.0.1    ops-fand.core.tar.gz
Verbose mode on.
mode set to octet
putting /tmp/core/ops-fand/ops-fand.1.20160321.032825.11.core.tar.gz to 172.17.0.1:ops-fand.core.tar.gz [octet]
Sent 447468 bytes in 0.1 seconds [35797440 bits/sec]
switch#
```

If there are no core dumps to present, the following information appears:

```
switch# copy core-dump ops-abc  tftp 172.17.0.1
ops-abc don't have core file
switch#
```


### copy coredump help string
```
 bash-4.3# vtysh
switch# copy
  core-dump       Copy core dump present in the system
  running-config  Copy from current system running configuration
  sftp            Copy data from an SFTP server
  startup-config  Copy from startup configuration
switch# copy core-dump
  DAEMON_NAME  Name of the Daemon
switch# copy core-dump ops-fand
  sftp  Copy data to sftp server
  tftp  Copy data to tftp server
switch# copy core-dump ops-fand tftp
  A.B.C.D  Specify the host IP of the remote system (IPv4)
  WORD     Specify the host name of the remote system
switch# copy core-dump ops-fand tftp 172.17.0.1
  <cr>
  [FILE_NAME]  Name of the destination file
switch# copy core-dump ops-fand tftp 172.17.0.1 abc.tar.gz
  <cr>
switch# copy core-dump ops-fand
  sftp  Copy data to sftp server
  tftp  Copy data to tftp server
switch# copy core-dump ops-fand sftp
  USERNAME  User name of sshd server
switch# copy core-dump ops-fand sftp naiksat
  A.B.C.D  Specify the host IP of the remote system (IPv4)
  WORD     Specify the host name of the remote system
switch# copy core-dump ops-fand sftp naiksat 172.17.0.1
  <cr>
  [FILE_NAME]  Name of the destination file
switch# copy core-dump ops-fand sftp naiksat 172.17.0.1  abc.tar.gz
  <cr>
switch# copy core-dump ops-fand sftp naiksat 172.17.0.1  abc.tar.gz
```

# Copy Core Dump CLI Guide

## Contents

- [Copy Core Dump CLI Guide](#copy-core-dump-cli-guide)
	- [Contents](#contents)
		- [copy one instance of coredump to tftp](#copy-one-instance-of-coredump-to-tftp)
		- [copy all instance of corefile for a daemon](#copy-all-instance-of-corefile-for-a-daemon)
		- [copy kernel corefile to tftp server](#copy-kernel-corefile-to-tftp-server)
		- [copy one instnace of daemon corefile to sshd server](#copy-one-instnace-of-daemon-corefile-to-sshd-server)
		- [copy all instance of corefile for a daemon to sshd server](#copy-all-instance-of-corefile-for-a-daemon-to-sshd-server)
		- [Copy kernel corefile to sshd srver](#copy-kernel-corefile-to-sshd-srver)
		- [copy coredump help string](#copy-coredump-help-string)

### copy one instance of daemon coredump to tftp

#### Syntax
```
copy core-dump  <DAEMONNAME> instance-id <INSTANCE ID>  tftp  <TFTP SERVER IPIV4 ADDRESS /HOST NAME> [FILENAME]
```

#### Description
This cli copy only one instance of daemon coredump file to destination tftp server .  Destination filename is optional parameter . CLI keep destination file name same as source file name if user has not provided the destination filename .

#### Authority
root and netop users can copy corefile to any external tftp server from the switch.

#### Parameters
daemon name
instance id
tftp server address
destination file name


#### Examples
```
switch# show  core-dump
======================================================================================
Daemon Name         | Instance ID | Crash Reason                  | Timestamp
======================================================================================
ops-vland             439           Aborted                        2016-04-26 18:05:28
ops-vland             410           Aborted                        2016-04-26 18:08:59
======================================================================================
Total number of core dumps : 2
======================================================================================
switch#
switch# copy core-dump ops-vland instance-id 439  tftp 10.0.12.161 ops-vland.xz
copying ...
Sent 109188 bytes in 0.1 seconds
switch#
```

If there are no core dumps present with given instance, then following information appears:
No coredump found for daemon <daemon name>
```
switch# copy core-dump ops-vland instance-id 567  tftp 10.0.12.161 ops-vland.xz
No coredump found for daemon ops-vland with instance 567
switch#
```

### copy all instance of corefile for a daemon

#### Syntax
```
copy core-dump <DAEMONNAME>  tftp <tftp server ipv4 address / hostname >
```

#### Description
This cli copy all instance of corefile for a daemon to destination tftp server.

#### Authority
root and netop users can copy corefile to any external tftp/sssh server from the switch.

#### Parameters
daemon name
tftp server address

#### Examples

```
switch# show  core-dump
======================================================================================
Daemon Name         | Instance ID | Crash Reason                  | Timestamp
======================================================================================
ops-vland             439           Aborted                        2016-04-26 18:05:28
ops-vland             410           Aborted                        2016-04-26 18:08:59
======================================================================================
Total number of core dumps : 2
======================================================================================
switch#
switch# copy core-dump ops-vland tftp 10.0.12.161
copying ...
Sent 109188 bytes in 0.1 seconds
copying ...
Sent 109044 bytes in 0.0 seconds
switch#
```

If there are no core dumps files present, then following information appears:

```
switch# copy core-dump ops-lldpd  tftp 10.0.12.161
No coredump found for daemon ops-lldpd
switch#
```


### Copy kernel corefile to tftp server

#### Syntax
```
copy core-dump kernel tftp  <TFTP SERVER IPV4 ADDRESS / HOST NAME > [FILENAME]

```

#### Description
This cli copy daemon coredump  to destination sftp server . User can specify the destiation filename by specifying in CLI .

#### Authority
root and netop users can copy corefile to any external tftp/sssh server from the switch.

#### Parameters
daemon name
user name
tftp  server address

#### Examples

```
switch# show core-dump
======================================================================================
Daemon Name         | Instance ID | Crash Reason                  | Timestamp
======================================================================================
ops-vland             439           Aborted                        2016-04-26 18:05:28
ops-vland             410           Aborted                        2016-04-26 18:08:59
kernel                                                             2016-04-26 18:04:20
======================================================================================
Total number of core dumps : 3
======================================================================================
switch#
switch#
switch# copy core-dump kernel
sftp  tftp
switch# copy core-dump kernel
  sftp  Copy coredump to sftp server
  tftp  Copy coredump to tftp server
switch# copy core-dump kernel tftp
  A.B.C.D  Specify server IP
  WORD     Specify server name
switch# copy core-dump kernel tftp 10.0.12.161
  <cr>
  [FILENAME]  Specify destination file name

switch# copy core-dump kernel tftp   10.0.12.161
copying ...
Sent 30955484 bytes in 19.6 seconds
switch#

```

If there are no kernel corefile ,then following information appears:
No coredump found for kernel

```
switch#  copy core-dump kernel tftp 10.0.12.161
No coredump found for kernel
switch#
```

### copy one instnace of daemon corefile to sshd server

#### Syntax
```
copy core-dump <DAEMONNAME> instance-id <INSTANCE ID> sftp <USERNAME> <SSHD SERVER IPV4/HOST NAME> [FILENAME]
```

#### Description
This cli copy daemon coredump  to destination sshd server . Use can specify the destination filename. destination filename is optional parameter . If uses has not specified file name then it saves as original name .

#### Authority
root and netop users can copy corefile to any external tftp/sssh server from the switch.

#### Parameters
daemon name
user name
sshd server address
destination file name

#### Examples

```
switch#copy core-dump ops-vland instance-id 410 sftp naiksat 10.0.12.161 ops-vland.xz
copying ...
naiksat@10.0.12.161's password:
Connected to 10.0.12.161.
sftp> put /var/diagnostics/coredump/core.ops-vland.0.a6f6c4b58aa5467ba57d7f9492afa10f.410.1461694139000000.xz ops-vland.xz
Uploading /var/diagnostics/coredump/core.ops-vland.0.a6f6c4b58aa5467ba57d7f9492afa10f.410.1461694139000000.xz to /users/naiksat/ops-vland.xz
/var/diagnostics/coredump/core.ops-vland.0.a6 100%  106KB 106.5KB/s   00:00
switch#
```

If there are no core dumps to present, the following information appears:

```
copy core-dump ops-vland instance-id 410 sftp naiksat 10.0.12.161 ops-vland.xz
No coredump found for daemon ops-vland with instance 410
```

### copy all instance of corefile for a daemon to sshd server

#### Syntax
```
copy core-dump < DAEMON NAME>  sftp <USERNAME> <SSHD SERVER ADDRESS>  [DESTINATION FILE NAME]
```

#### Description
This cli copy all instance of daemon coredump  to destination sshd server . User can specify destination file name .
If uses has not specified file name then it saves as original name .

#### Authority
root and netop users can copy corefile to any external tftp/sssh server from the switch.

#### Parameters
daemon name
user name
sshd server address
destination file name

#### Examples

```
switch# copy core-dump ops-switchd sftp naiksat 10.0.12.161
copying ...
The authenticity of host '10.0.12.161 (10.0.12.161)' can't be established.
ECDSA key fingerprint is SHA256:uWeyXm2j6VkDfCitlyz/P+xGgZW9YYw5GnDOsEgVHeU.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.0.12.161' (ECDSA) to the list of known hosts.
naiksat@10.0.12.161's password:
Connected to 10.0.12.161.
sftp> put /var/diagnostics/coredump/core.ops-switchd.0.1bddabce7ee5468884cc012b1d7c2ab0.361.1461694266000000.xz core.ops-switchd.0.1bddabce7ee5468884cc012b1d7c2ab0.361.1461694266000000.xz
Uploading /var/diagnostics/coredump/core.ops-switchd.0.1bddabce7ee5468884cc012b1d7c2ab0.361.1461694266000000.xz to /users/naiksat/core.ops-switchd.0.1bddabce7ee5468884cc012b1d7c2ab0.361.1461694266000000.xz
/var/diagnostics/coredump/core.ops-switchd.0. 100% 4531KB   4.4MB/s   00:00
switch#

```

If there are no core dumps to present, the following information appears:

```
switch# copy core-dump ops-fand  sftp naiksat 10.0.12.161
No coredump found for daemon ops-fand
switch#

```

### copy kernel corefile to sshd srver

#### Syntax
```
copy core-dump kernel sftp <USERNAME>  <SSHD SERVER IP>  [ DESTINATION FILE NAME ]
```
#### Description
This cli copy kernel corefile  to destination sshd server . User can specify destination file name .
If uses has not specified file name then it saves as original name .

#### Authority
root and netop users can copy corefile to any external ssh server from the switch.

#### Parameters
daemon name
user name
sshd server address
destination file name

#### Examples

```
switch# copy core-dump kernel sftp naiksat 10.0.12.161 kernelcore.tar.gz
copying ...
naiksat@10.0.12.161's password:
Connected to 10.0.12.161.
sftp> put /var/diagnostics/coredump/kernel-core/vmcore.20160426.180420.tar.gz
kernelcore.tar.gz
Uploading /var/diagnostics/coredump/kernel-core/vmcore.20160426.180420.tar.gz to
/users/naiksat/kernelcore.tar.gz
/var/diagnostics/coredump/kernel-core/vmcore. 100%   44MB  43.5MB/s   00:01
switch#
```

If there are no core dumps to present, the following information appears:
No coredump found for kernel
```
switch# copy core-dump kernel sftp naiksat 10.0.12.161 kernelcore.tar.gz
No coredump found for kernel
switch#
```

### copy coredump help string
```
switch# copy
  core-dump       Copy daemon or kernel coredump
  running-config  Copy from current system running configuration
  sftp            Copy data from an SFTP server
  startup-config  Copy from startup configuration
switch# copy core-dump
  DAEMON_NAME  Specify daemon-name
  kernel       Copy kernel coredump
switch# copy core-dump ops-fand
  instance-id  Coredump instance ID
  sftp         Copy coredump to sftp server
  tftp         Copy coredump to tftp server
switch# copy core-dump ops-fand instance-id
  INSTANCE_ID  Specify coredump instance ID
switch# copy core-dump ops-fand instance-id 123
  sftp  Copy coredump to sftp server
  tftp  Copy coredump to tftp server
switch# copy core-dump ops-fand instance-id 123 tftp
  A.B.C.D  Specify server IP
  WORD     Specify server name
switch# copy core-dump ops-fand instance-id 123 tftp 1.2.3.4
  <cr>
  [FILE_NAME]  Specify destination file name
switch# copy core-dump ops-fand instance-id 123 tftp 1.2.3.4 abc.xz
  <cr>
switch# copy core-dump ops-fand instance-id 123 tftp 1.2.3.4 ops-fand.xz
  <cr>
switch# copy core-dump ops-fand
  instance-id  Coredump instance ID
  sftp         Copy coredump to sftp server
  tftp         Copy coredump to tftp server
switch# copy core-dump ops-fand tftp
  A.B.C.D  Specify server IP
  WORD     Specify server name
switch# copy core-dump ops-fand tftp 1.2.3.4
  <cr>
switch# copy core-dump kernel
  sftp  Copy coredump to sftp server
  tftp  Copy coredump to tftp server
switch# copy core-dump kernel tftp
  A.B.C.D  Specify server IP
  WORD     Specify server name
switch# copy core-dump kernel tftp 1.2.3.4
  <cr>
  [FILENAME]  Specify destination file name
switch# copy core-dump kernel tftp 1.2.3.4 kernel.tar.gz
  <cr>
switch# copy core-dump ops-fand
  instance-id  Coredump instance ID
  sftp         Copy coredump to sftp server
  tftp         Copy coredump to tftp server
switch# copy core-dump ops-fand instance-id 123
  sftp  Copy coredump to sftp server
  tftp  Copy coredump to tftp server
switch# copy core-dump ops-fand instance-id 123 sftp
  USERNAME  Specify user name of sshd server
switch# copy core-dump ops-fand instance-id 123 sftp naiksat
  A.B.C.D  Specify server IP
  WORD     Specify server name
switch#
switch# copy core-dump ops-fand instance-id 123 sftp naiksat 1.2.3.4
  <cr>
  [FILE_NAME]  Specify destination file name
switch# copy core-dump ops-fand instance-id 123 sftp naiksat 1.2.3.4 ops-fand.tar.gz

switch# copy core-dump ops-fand
  instance-id  Coredump instance ID
  sftp         Copy coredump to sftp server
  tftp         Copy coredump to tftp server
switch# copy core-dump ops-fand
  instance-id  Coredump instance ID
  sftp         Copy coredump to sftp server
  tftp         Copy coredump to tftp server
switch# copy core-dump ops-fand
  instance-id  Coredump instance ID
  sftp         Copy coredump to sftp server
  tftp         Copy coredump to tftp server
switch# copy core-dump ops-fand sftp
  USERNAME  Specify user name of sshd server
switch# copy core-dump ops-fand sftp naiksat
  A.B.C.D  Specify server IP
  WORD     Specify server name
switch# copy core-dump ops-fand sftp naiksat 1.2.3.4
  <cr>
switch# copy core-dump
  DAEMON_NAME  Specify daemon-name
  kernel       Copy kernel coredump
switch# copy core-dump kernel
  sftp  Copy coredump to sftp server
  tftp  Copy coredump to tftp server
switch# copy core-dump kernel sftp
  USERNAME  Specify user name of sshd server
switch# copy core-dump kernel sftp naiksat
  A.B.C.D  Specify server IP
  WORD     Specify server name
switch# copy core-dump kernel sftp naiksat 1.2.3.4
  <cr>
  [FILENAME]  Specify destination file name
switch# copy core-dump kernel sftp naiksat 1.2.3.4 kernel.tar.gz
  <cr>

```

## References
* [ Copy core-dump commands ]  copy_core-dump_cli_guide.md
* [ Copy core-dump userguide ] copy_core-dump_user_guide.md
* [ Copy core-dump design  ]  copy_core-dump_design_doc.md

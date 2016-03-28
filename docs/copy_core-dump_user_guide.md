# Copy Core Dump User Guide

## Contents

- [Copy Core Dump User Guide](#copy-core-dump-user-guide)
	- [Contents](#contents)
	- [Overview](#overview)
	- [How to use the feature](#how-to-use-the-feature)
		- [Examples](#examples)
			- [tftp without destination file name](#tftp-without-destination-file-name)
			- [tftp with destination file name](#tftp-with-destination-file-name)
			- [sftp without destination file name](#sftp-without-destination-file-name)
			- [sftp with destination file name](#sftp-with-destination-file-name)



## Overview
This command copy daemon corefile to tftp/ssh server .

## How to use the feature
Execute the cli command
1) "copy core-dump <daemon name/kernel> tftp <ipv4/ hostname> [FILENAME]".
2) "copy core-dump <daemon name/kernel> sftp <user name>  <ipv4/hostname> [FILENAME]".

### Examples
#### tftp without destination file name
```
switch# copy core-dump ops-fand  tftp 172.17.0.1
Verbose mode on.
mode set to octet
putting /tmp/core/ops-fand/ops-fand.1.20160321.032825.11.core.tar.gz to 172.17.0.1:ops-fand.1.20160321.032825.11.core.tar.gz [octet]
Sent 447468 bytes in 0.1 seconds [35797440 bits/sec]
switch#
```


#### tftp with destination file name
```
switch# copy core-dump ops-fand  tftp   172.17.0.1    ops-fand.core.tar.gz
Verbose mode on.
mode set to octet
putting /tmp/core/ops-fand/ops-fand.1.20160321.032825.11.core.tar.gz to 172.17.0.1:ops-fand.core.tar.gz [octet]
Sent 447468 bytes in 0.1 seconds [35797440 bits/sec]
```


#### sftp without destination file name
````
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


````

#### sftp with destination file name
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

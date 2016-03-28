#Copy Core Dump Design Document

##Contents
- [Copy Core Dump Design Document](#copy-core-dump-design-document)
	- [Contents](#contents)
		- [High level design of show core dump](#high-level-design-of-show-core-dump)
		- [Design choices](#design-choices)
		- [Block diagram](#block-diagram)
		- [Example  copy daemon coredump](#example-copy-daemon-coredump)
		- [References](#references)


### High level design of show core dump
The copy core dump command copy daemon core file to tftp/sshd server.

### Design choices
- User can copy core files with or without specifying destination file name .
- Maximum length of User name , hostname , destination file , daemon name is limited to 50.
- Acceptable characters for user name are "a-zA-Z0-9_-"  .
- Acceptable characters for host name are "A-Za-z0-9_.:-" .
- Acceptable characters for file name are "A-Za-z0-9_.-" .
- Acceptable characters for daemon name are "A-Za-z0-9_.-" .
- Usernmae or host name can't use "@" . It is used as separator between user and host while running ssh.
- Using one cli to copy core file kernel and daemon . We use "kernel" key word to copy kernel core file.


### Block diagram

```ditaa

  CLI Command
 +---------------+        +--------------+
 |copy core-dump | Read   |  Core Dump   |
 |               | -----> |  Location    |
 +---------------+        +--------------+
        |
        | copy
        v
 +---------------+
 | tftp          |
 | sftp server   |
 +---------------+

```

### Example  copy daemon coredump

```
bash-4.3# vtysh
switch# copy core-dump ops-fand tftp 172.17.0.1
Verbose mode on.
mode set to octet
putting /tmp/core/ops-fand/ops-fand.1.20160321.032825.11.core.tar.gz to 172.17.0.1:ops-fand.1.20160321.032825.11.core.tar.gz [octet]
Sent 447468 bytes in 0.0 seconds [inf bits/sec]
switch#

```


If there are no core dumps present, the following information appears:

```
<daemon name> don't have core file
```
```
copy core-dump ops-lldpd  tftp 172.17.0.1
ops-lldpd don't have core file
```
### References
copy_core-dump_design_doc.md

# SFTP Design

## Contents
   - [High level design of SFTP](#high-level-design-of-sftp)
   - [Design choices](#design-choices)
   - [Internal structure](#internal-structure)
       - [OVSDB Schema](#ovsdb-schema)
   - [References](#references)

## High level design of SFTP
The SFTP (Secure File Transfer Protocol) command is a very common method for transferring a file or executing a command in a secure mode. SFTP makes use of encrypted SSH session for it's operation. It provides an alternative to TFTP (Trivial File Transfer Protocol) for transferring sensitive information to and from the switch. Files transferred using SFTP are encryted and require authentication, thus providing greater security to the switch.

SFTP server :
It can be enabled/disabled by the user through CLI. The CLI daemon updates the modified configuration status of SFTP server into the OVSDB. The ops-aaa-utils daemon which is running the SSH daemon picks up the modified status from the OVSDB and accordingly it updates the /etc/ssh/sshd_config file.

SFTP client :
Client parameters are obtained from the user through CLI. Information entered by the user is passed on to a SFTP cli handler which maps these information to the open source SFTP client options and invokes the openSSH SFTP utility. The handler sends the response obtained from the openSSH back to the user. The end to end operation is performed in a single thread context as part of CLI Daemon.
No OVSDB interaction or any other module interaction is involved.

## Design choices

The open source `SFTP` application used is taken from the openSSH 6.8p1 package. SFTP runs on top of SSH daemon and as openSSH 6.8 is the package currently used by SSH daemon, we are leveraging the same.

## Internal structure

```ditaa
SFTP client

+--------+           +-------------------+             +-----------------+
|        +----------->                   +------------->                 |
|  CLI   |           |  SFTP cli handler |             |   openSSH 6.8   |
|        <-----------+                   <-------------+    (client)     |
+--------+           +-------------------+             +-----------------+

```

```ditaa
SFTP server

+----------------+           +----------------------+             +-----------------+
|   CLI          +----------->                      |             |                 |
|  daemon        |           |       OVSDB          +------------->   AAA Daemon    |
|                <-----------+                      |             |                 |
+----------------+           +----------------------+             +-------+---------+
                                                                          |
                                                                          |
                                                                    +-----V----+     +----------+
                                                                    |   SSHd   |     |   open   |
                                                                    |   Config +----->  SSH 6.8 |
                                                                    |   file   |     | (server) |
                                                                    +----------+     +----------+

```

### OVSDB Schema
#### System table
```
System:other_config
Key:
sftp_server_enable
Value:
true, false
```

## References
openSSH 6.8 Package (http://olex.openlogic.com/packages/openssh/6.8)

Linux SFTP Man page (http://linux.die.net/man/1/sftp)

SFTP RFC (https://tools.ietf.org/html/rfc913)

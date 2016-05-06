# Custom login banners
## Contents
- [Responsibilities](#responsibilities)
- [Design choices](#design-choices)
- [User roles](#user-roles)
- [Participating modules](#participating-modules)
- [OVSDB-schema](#ovsdb-schema)
- [References](#references)

## Responsibilities
The banner feature displays messages to a user authenticating themselves to a management interface of a switch. One message is displayed before the user enters their login and the other is displayed upon succesful authentication. These messages are customizable.

## Design choices
- The banner feature leverages the existing banner functionality in OpenSSH server for SSH connections.
- ops-cli and RESTD publish banner changes to OVSDB.
- OpenSSH server reads the pre-authentication banner from /etc/issue.net and the post authentication banner from /etc/motd.
- The AAA daemon subscribes to the System table and updates these files on disk whenever either banner has changed.

## User roles
There are currently 2 users in OpenSwitch, admin and netop.
The roles of these users are:
- admin: managment of the actual switch hardware, admins are only allowed to upgrade the firmware
- netop: management of virtual switch instance
Users in group ops\_netop are able to change the banner through the command line interface. No other users are permitted to change the banner. This design is based partly on the fact that the admin user in OpenSwitch should not have access to vtysh. The design philosophy in OpenSwitch is that only ops\_netop users should be capable of making changes to OVSDB.

## Participating modules

``` ditaa
     +---------------------+   +---------------------+
     |                     |   |                     |
     |       ops+cli       |   |       RESTD         |
     |                     |   |                     |
     |                     |   |                     |
     +----+----------------+   +-----+-----------+---+
          |                          |           |
          |                          +           |
publishes |                  subscribes          | publishes
          |                          +           |
          |        +-----------------v---+       |
          |        |                     |       |
          |        |       OVSDB         |       |
          +-------->                     <-------+
                   |                     |
                   +---------^-----------+
                             |
                             | subscribes
                             |
                   +---------+-----------+
                   |                     |
                   |        AAA          |
                   |                     |
                   |                     |
                   +---------+-----------+
                             | updates
                             |
                   +---------v------------+
                   |                      |
                   |     filesystem       |
                   |                      |
                   |                      |
                   +---------^------------+
                             | reads
                             |
                   +---------+------------+
                   |                      |
                   |        SSHD          |
                   |                      |
                   |                      |
                   +----------------------+

```

## OVSDB-schema
System:other\_config
Keys:
banner
banner\_exec

## References
* [Banner Commands](http://www.openswitch.net/documents/user/banner_cli)
* [Feature Test Cases for Banner](http://www.openswitch.net/documents/user/banner_test)

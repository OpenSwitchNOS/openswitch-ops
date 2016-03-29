# High level design of remote syslog feature
Remote syslog feature is used to configure syslog servers to which syslog messages are forwarded.  This feature is configured either through CLI or REST api.  The configurations are stored in the OVSDB table *syslog_remote*.   The daemon *ops-supportability* is responsible to monitor this OVSDB table and reconfigure the rsyslog daemon accordingly.

## Contents

- [Design choices](#design-choices)
- [Participating modules](#participating-modules)
- [OVSDB-Schema](#ovsdb-schema)
- [References](#references)

## Design choices
* Maximum of 4 remote syslog servers are supported.
* Support only one configuration per remote syslog server.
* Only TCP and UDP transport protocols are supported to establish connection with remote syslog server.
* Default UDP protocol used is 514
* Default TPC protocol used is 1470
* Supports syslog server connection only via data ports.

## Participating modules

``` ditaa
+-----+        +-----------+
| CLI +-------->           |
+-----+        |   OVSDB   |
          +---->           |               +-------------+
          |    +---+-------+    restarts   |             |
+------+  |        |         +------------->   rsyslog   |
| REST +--+        |         |             |   daemon    |
+------+           |         |             |             |
                   |         |             +------^------+
                   |         |                    |
  +----------------v----+    |                    |
  |                     +----+             +------+--------+
  |  ops-supportability |       updates    | rsyslog       |
  |  daemon             +------------------> configuration |
  |                     |                  +---------------+
  +---------------------+
```

CLI/REST remote syslog configuration updates the syslog_remote table in OVSDB.  The Daemon *ops-supportability* which has subscribed to the changes to this table, will receive the notification.  When a change in this table is detected *ops-supportability* daemon will generate the appropriate rsyslog configuration file(/etc/rsyslog.remote.conf).  It verifies whether there is any change with respect to the old rsyslog configuration, if changes are found, it will restart the rsyslog server for the new configuration to take effect.

## OVSDB-Schema
Remote syslog server configuration are stored in syslog_remote table.  This table contains the following columns
```ditaa
=================================================================
Column        |  Purpose
==============|==================================================
remote_host   | FQDN or host name or IPv4 address or IPv6 address
              | of the remote syslog server
--------------|--------------------------------------------------
transport     | Transport layer protocol used to forward messages
              | to the server.  Default is UDP
--------------|--------------------------------------------------
port_number   | Port number on which syslog server is listening.
              | Default is 514 for UDP and 1470 for TCP.
--------------|--------------------------------------------------
severity      | Filter syslog messages with severity.  Only
              | messages with severity higher than or equal to
              | the specified value will be sent to the remote
              | server.  Default is "debug"
=================================================================              
```


## References

* [User Guide](documents/user/syslog_remote_user_guide)
* [CLI Guide](documents/user/syslog_remote_cli)

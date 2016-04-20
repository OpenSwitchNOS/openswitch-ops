#Show Vlog Commands

## Contents


- [Display commands](#display-commands)
	 - [Commands summary](#commands-summary)
      - [Syntax](#syntax)
      - [Description](#description)
      - [Authority](#authority)
      - [Examples](#examples)
      - [References](#references)


##Display commands
###Commands summary
| Command | Usage |
|:------- |:------|
| **show vlog** | Displays vlog messages of ops daemons|
| **show vlog daemon (daemon_name)** | Displays vlog messages of corresponding ops-daemon only|
| **show vlog severity (severity_level)** | Displays vlog messages of corresponding severity level and above|
| **show vlog config list** | Displays list of supported features and descriptions|
| **show vlog config feature (feature_Name)** | Displays feature configuration log level of syslog and file Destinations|
| **show vlog config daemon (daemon_Name)**| Displays daemon configuration log level of syslog and file Destinations|
| **show vlog config** | Displays list of supported features corresponding daemons logging levels of file and console destinations|
| **show vlog daemon (daemon_name) severity (severity_level)** | Display vlogs for specified ops-daemon with severity level and above|
| **show vlog severity (severity_level) daemon (daemon_name)** | Display vlogs for specified severity level and above with ops-daemon only|


### Show vlog
#### Syntax
`show vlog`
#### Description
Runs the `show vlog` command to displays vlog messages of ops daemons.
#### Authority
All users

### Show vlog daemon
#### Syntax
`show vlog daemon <daemon_name>`
#### Description
Runs the `show vlog daemon <daemon_name>` command to displays only corresponding ops-daemon vlog messages.
#### Authority
All users

### Show vlog severity
#### Syntax
`show vlog severity <emer/err/warn/info/debug>`
#### Description
Runs the `show vlog severity <emer/err/warn/info/debug>` command to displays  corresponding severity level and above vlog messages.
#### Authority
All users

### Show vlog config list
#### Syntax
`show vlog config list`
#### Description
Runs the `show vlog config list` command list all vlog supported features and description.
#### Authority
All users

### Show vlog config feature
#### Syntax
`show vlog config feature <feature_name>`
#### Description
Runs the `show vlog config feature <feature_name>` command for feature configuration log levels of file and syslog destinations.
#### Authority
All users

### Show vlog config daemon
#### Syntax
`show vlog config daemon <daemon_name>`
#### Description
Runs the `show vlog config daemon <daemon_name>` command for ops-daemon configuration log levels of file and syslog destinations.

### Show vlog config
#### Syntax
`show vlog config`
#### Description
Runs the `show vlog config` command list all supported features and coresponding daemons logging levels of file and syslog destinations.
#### Authority
All users

### Show vlog daemon (daemon_name) severity (severity_level)
#### Syntax
`show vlog daemon <daemon_name> severity <severity_level>`
#### Description
This CLI command to display vlogs for specified ops-daemon only with severity and above.
#### Authority
All users


#### Examples
```
switch# show vlog

---------------------------------------------------
show vlog
-----------------------------------------------------
ovsdb-server            |ovs|00001|ovsdb_server|INFO|ovsdb-server (Open vSwitch) 2.5.0
ops-arpmgrd             |ovs|00001|arpmgrd|INFO|ops-arpmgrd (OpenSwitch arpmgrd) 2.5.0
ops-arpmgrd             |ovs|00002|reconnect|INFO|unix:/var/run/openvswitch/db.sock: connecting...
ops-arpmgrd             |ovs|00003|reconnect|INFO|unix:/var/run/openvswitch/db.sock: connected
ops-arpmgrd             |ovs|00004|ovsdb_idl|INFO|DEBUG first row is missing from table class System
ops-intfd               |ovs|00001|ops_intfd|INFO|ops-intfd (OpenSwitch Interface Daemon) started
.......


switch# show vlog daemon ops-lldpd

---------------------------------------------------
show vlog
----------------------------------------------------
ovs|00001|lldpd_ovsdb_if|INFO|ops-lldpd (OPENSWITCH LLDPD Daemon) started

switch# show vlog severity warn

---------------------------------------------------
show vlog
-----------------------------------------------------
ops-sysd            |ovs|00005|ovsdb_if|ERR|Failed to commit the transaction. rc = 7
ops-pmd             |ovs|00007|timeval|WARN|Unreasonably long 2802ms poll interval (168ms user, 29ms system)
ops-pmd             |ovs|00008|timeval|WARN|faults: 590 minor, 0 major
ops-pmd             |ovs|00009|timeval|WARN|context switches: 637 voluntary, 70 involuntary
ops-sysd            |ovs|00006|ovsdb_if|ERR|Failed to commit the transaction. rc = 7
ops-intfd           |ovs|00007|intfd_ovsdb_if|WARN|value for speeds not set in h/w description file
......

switch# show vlog config list

================================================
Features          Description
================================================
lldp              Link Layer Discovery Protocol
lacp              Link Aggregation Control Protocol
fan               System Fan

switch# show vlog config feature lldp
========================================
Feature               Syslog     File
========================================
lldp                   DBG       WARN

switch# show vlog config daemon ops-fand

======================================
Daemon              Syslog     File
======================================
ops-fand             DBG       WARN

switch# show vlog config

=================================================
Feature         Daemon          Syslog     File
=================================================
lldp            ops-lldpd        DBG        DBG

                ops-portd       INFO       INFO

lacp            ops-lacpd        OFF        OFF

                ops-ledd         DBG       EMER

fan             ops-fand        INFO       INFO


switch# configure t
switch(config)# vlog feature lacp syslog dbg
switch(config)# vlog daemon ops-lldpd file warn
switch(config)# end
switch# show vlog feature lacp

========================================
Feature               Syslog     File
========================================
lacp                   DBG       INFO

switch# show vlog daemon ops-lldpd

======================================
Daemon              Syslog     File
======================================
ops-lldpd            DBG       WARN

switch# configure t
switch(config)# vlog feature lacp file dbg
switch(config)# vlog daemon ops-lldpd syslog info
switch(config)# vlog feature fand all dbg
switch(config)# end

switch# show vlog config feature lacp

========================================
Feature               Syslog     File
========================================
lacp                   OFF        DBG

switch# show vlog config daemon ops-lldpd

======================================
Daemon              Syslog     File
======================================
ops-lldpd           INFO        DBG

switch# show vlog config feature fan

========================================
Feature               Syslog     File
========================================
fan                   DBG        DBG
```


switch# show vlog severity debug daemon ops-pmd

---------------------------------------------------
show vlog
-----------------------------------------------------
ovs|00006|ops_pmd|INFO|ops-pmd (OpenSwitch pmd) 0.02


##References
* [Reference 1] `show_vlog_cli.md`

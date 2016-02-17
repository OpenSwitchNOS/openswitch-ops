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
| **show vlog daemon (daemon_name/word)** | Displays vlog messages of corresponding daemon only|
| **show vlog severity (severity_level)** | Displays vlog messages of corresponding severity level|
| **show vlog config list** | Displays list of supported features and descriptions|
| **show vlog config feature (feature_Name)** | Displays feature configuration log level of syslog and file Destinations|
| **show vlog config daemon (daemon_Name)**| Displays daemon configuration log level of syslog and file Destinations|
| **show vlog config** | Displays list of supported features corresponding daemons logging levels of file and console destinations|

### Show vlog
#### Syntax
`show vlog`
#### Description
Runs the `show vlog` command to displays vlog messages of ops daemons.
#### Authority
All users

### Show vlog daemon
#### Syntax
`show vlog daemon <word>`
#### Description
Runs the `show vlog daemon <word>` command to displays only corresponding daemon vlog messages.
#### Authority
All users

### Show vlog severity
#### Syntax
`show vlog severity <word>`
#### Description
Runs the `show vlog daemon <word>` command to displays only corresponding severity level vlog messages.
#### Authority
All users

### Show vlog config list
#### Syntax
`show vlog config list`
#### Description
Runs the `show vlog config list` command list all the supported features and description.
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
Runs the `show vlog config daemon <daemon_name>` command for daemon configuration log levels of file and syslog destinations.

### Show vlog config
#### Syntax
`show vlog config`
#### Description
Runs the `show vlog config` command for list of supported features coresponding daemons logging levels of file and syslog destinations.
#### Authority
All users

#### Examples
```
switch# show vlog

---------------------------------------------------
show vlog
-----------------------------------------------------
ovs|00001|ovsdb_server|INFO|ovsdb-server (Open vSwitch) 2.3.90
ovs|00001|arpmgrd|INFO|ops-arpmgrd (OpenSwitch arpmgrd) 2.3.90
ovs|00002|reconnect|INFO|unix:/var/run/openvswitch/db.sock: connecting...
ovs|00003|reconnect|INFO|unix:/var/run/openvswitch/db.sock: connected
ovs|00001|reconnect|INFO|unix:/var/run/openvswitch/db.sock: connecting...
ovs|00002|reconnect|INFO|unix:/var/run/openvswitch/db.sock: connected
ovs|00001|lacpd|INFO|ops-lacpd (OpenSwitch Link Aggregation Daemon) started
.......

switch# show vlog  daemon lldpd

---------------------------------------------------
show vlog
-----------------------------------------------------
ovs|00002|reconnect|INFO|unix:/var/run/openvswitch/db.sock: connecting...
ovs|00003|reconnect|INFO|unix:/var/run/openvswitch/db.sock: connected
ovs|00004|lldpd_ovsdb_if|INFO|System is now configured (cur_cfg=1).
ovs|00005|lldpd_ovsdb_if|INFO|Configured lldp_tlv_sys_name_enable=1
ovs|00006|lldpd_ovsdb_if|INFO|Configured lldp_tlv_sys_desc_enable=1
ovs|00007|lldpd_ovsdb_if|INFO|Configured lldp_tlv_sys_cap_enable=1
ovs|00008|lldpd_ovsdb_if|INFO|Configured lldp_tlv_mgmt_addr_enable=1
ovs|00009|lldpd_ovsdb_if|INFO|Configured lldp_tlv_port_desc_enable=1
......
ovs|00014|lldpd_ovsdb_if|INFO|lldp disabled
ovs|00015|lldpd_ovsdb_if|INFO|ops-lldpd (OPENSWITCH lldpd) 0.1.0-R0.1-10-g4f0b17d-dirty

switch# show vlog severity info

---------------------------------------------------
show vlog
-----------------------------------------------------
ovs|  1  | reconnect | INFO | unix:/var/run/openvswitch/db.sock: connecting...
ovs|  3  | reconnect | INFO | unix:/var/run/openvswitch/db.sock: connected
ovs|  5  | cfgd | INFO | No rows found in the config table
......

switch# show vlog config list
================================================
Features          Description
================================================
lldp              Link Layer Discovery Protocol
lacp              Link Aggregation Control Protocol
fand              System Fan

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

fand            ops-fand        INFO       INFO

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
switch# show vlog config feature fand
========================================
Feature               Syslog     File
========================================
fand                   DBG        DBG
```
##References
* [Reference 1] `show_vlog_cli.md`

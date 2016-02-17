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
| **show vlog config list** | Displays list of supported features and descriptions|
| **show vlog config feature (feature_Name)** | Displays feature configuration log level of syslog and file Destinations|
| **show vlog config daemon (daemon_Name)**| Displays daemon configuration log level of syslog and file Destinations|
| **show vlog config** | Displays list of supported features corresponding daemons logging levels of file and console destinations|

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

### Show vlog
#### Syntax
`show vlog`
#### Description
Runs the `show vlog config` command for list of supported features coresponding daemons logging levels of file and syslog destinations.
#### Authority
All users

#### Examples
```
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

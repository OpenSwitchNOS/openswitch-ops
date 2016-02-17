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
| **show vlog list** | Displays all supported features and descriptions|
| **show vlog feature (feature_Name)** | Displays Feature configuration log level for syslog and file Destinations|
| **show vlog daemon (daemon_Name)**| Displays Daemon configuration log level for syslog and file Destinations|
| **show vlog** | Displays all supported features logging levels for file and console destinations|

### Show vlog list
#### Syntax
`show vlog list`
#### Description
Runs the `show vlog list` command list all the supported features and descriptions.
#### Authority
All users

### Show vlog feature
#### Syntax
`show vlog feature <feature_name>`
#### Description
Runs the `show vlog feature <feature_name>` command for feature configuration log levels for file and syslog destinations.
#### Authority
All users

### Show vlog daemon
#### Syntax
`show vlog daemon <daemon_name>`
#### Description
Runs the `show vlog daemon <daemon_name>` command for daemon configuration log levels for file and
syslog destinations.

### Show vlog
#### Syntax
`show vlog`
#### Description
Runs the `show vlog` command for all supported features logging levels for file and syslog destinations.
#### Authority
All users

#### Examples
```
switch# show vlog list
================================================
Features          Description
================================================
lldp              Link Layer Discovery Protocol
lacp              Link Aggregation Control Protocol
fand              System Fan

switch# show vlog feature lldp
========================================
Feature               Syslog     File
========================================
lldp                   DBG       WARN

switch# show vlog daemon ops-fand
======================================
Daemon              Syslog     File
======================================
ops-fand             DBG       WARN

switch# show vlog
=================================================
Feature         Daemon          Syslog     File
=================================================
lldp            ops-lldpd        DBG       WARN

lacp            ops-lacpd       EMER       INFO

fand            ops-fand         DBG       WARN

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
switch(config)# vlog feature lldp any info
switch(config)# vlog daemon ops-lacpd syslog any
switch(config)# vlog daemon ops-lacpd any any
switch(config)# vlog feature fand any any
switch(config)# end
switch# show vlog feature lldp
========================================
Feature               Syslog     File
========================================
lldp                  INFO       INFO

switch# show vlog daemon ops-lacpd
======================================
Daemon              Syslog     File
======================================
ops-lacpd            DBG        DBG

switch# show vlog feature fand
========================================
Feature               Syslog     File
========================================
fand                   DBG        DBG
```
##References
* [Reference 1] `show_vlog_cli.md`

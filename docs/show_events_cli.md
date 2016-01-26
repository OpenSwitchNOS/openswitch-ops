# Show events Command
## Contents

- [Contents](#contents)
- [Configuration Commands](#configuration-commands)
- [Display Commands](#display-commands)
	-[Commands Summary](#commands-summary)
    -[show events](#show events)
     - [Syntax](#syntax)
     - [Description](#description)
     - [Authority](#authority)
     - [Examples](#examples)

## Configuration Commands

switch# configure terminal
eg:
switch(config)# lldp enable
switch(config)# no lldp enable
switch(config)# lldp timer 125

## Display Commands
### Commands Summary
| Command | Usage|
|:--------|:--------|
| **show events**| Runs show events for all supported features|

### Show events
#### Syntax
`show events`
#### Description
Runs show events command for all the supported features.
#### Authority
All users
#### Examples
switch# configure t
switch(config)# lldp enable
switch(config)# no lldp enable
switch(config)# lldp timer 100
switch(config)# end
switch# show events

---------------------------------------------------
show event logs
---------------------------------------------------
2016-01-26:09:13:31.287757|6|ops-evt|1002|LOG_INFO|LLDP Disabled
2016-01-26:09:14:25.097368|6|ops-evt|1001|LOG_INFO|LLDP Enabled
2016-01-26:09:14:36.989378|6|ops-evt|1002|LOG_INFO|LLDP Disabled
2016-01-26:09:14:48.545033|6|ops-evt|1003|LOG_INFO|Configured LLDP tx-timer with 100
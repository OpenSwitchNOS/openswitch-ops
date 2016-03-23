# Show Events Command
## Contents

- [Configuration commands](#configuration-commands)
- [Display commands](#display-commands)
  - [Commands summary](#commands-summary)
  - [Show events](#show events)
     - [Syntax](#syntax)
     - [Description](#description)
     - [Authority](#authority)
     - [Examples](#examples)

## Configuration commands

`switch# configure terminal`

For example:

`switch(config)# lldp enable`

`switch(config)# no lldp enable`

`switch(config)# lldp timer 125`

## Display commands
### Commands summary
| Command | Usage|
|:--------|:--------|
| **show events**| Displays events for all supported features|
| **show events category** | Displays events based on event category|
| **show events event-id** | Displays events based on event ID|
| **show events reverse** | Displays reverse list the event logs|
| **show vlog severity** | Displays event logs of specified severity and above|

### Show events
#### Syntax
`show events`
#### Description
Runs the `show events` command to displays all event logs for supported features.
#### Authority
All users

### Show events category
#### Syntax
`show events category`
#### Description
Runs the `show events category` command to displays events based on event category.
#### Authority
All users

### Show events event-id
#### Syntax
`show events event-id`
#### Description
Runs the `show events event-id` command to displays events based on event-id.
#### Authority
All users

### Show events reverse
#### Syntax
`show events reverse`
#### Description
Runs the `show events reverse` command to displays reverse list the event logs.
#### Authority
All users

### Show events severity
#### Syntax
`show events severity`
#### Description
Runs the `show events severity` command to displays event logs based on specific severity and above.
#### Authority
All users

#### Examples
```
switch# configure t
switch(config)# lldp enable
switch(config)# no lldp enable
switch(config)# lldp timer 100
switch(config)# lldp management-address 10.0.0.1
switch(config)# end
switch# show events

---------------------------------------------------
show event logs
---------------------------------------------------
2016-03-22:14:16:04.945278|ops-lldpd|1002|LOG_INFO|LLDP Disabled
2016-03-22:17:54:51.906801|ops-lldpd|1001|LOG_INFO|LLDP Enabled
2016-03-22:17:54:57.573014|ops-lldpd|1003|LOG_INFO|Configured LLDP tx-timer with 100
2016-03-22:17:55:23.053182|ops-lldpd|1007|LOG_INFO|Configured LLDP Management pattern 10.0.0.1


switch# show events category LLDP

---------------------------------------------------
show event logs
---------------------------------------------------
2016-03-22:14:16:04.945278|ops-lldpd|1002|LOG_INFO|LLDP Disabled
2016-03-22:17:54:51.906801|ops-lldpd|1001|LOG_INFO|LLDP Enabled
2016-03-22:17:54:57.573014|ops-lldpd|1003|LOG_INFO|Configured LLDP tx-timer with 100
2016-03-22:17:55:23.053182|ops-lldpd|1007|LOG_INFO|Configured LLDP Management pattern 10.0.0.1

switch# show events event-id 1002

---------------------------------------------------
show event logs
---------------------------------------------------
2016-03-22:14:16:04.945278|ops-lldpd|1002|LOG_INFO|LLDP Disabled


switch# show events event-id 1001-1003,1007

---------------------------------------------------
show event logs
---------------------------------------------------
2016-03-22:17:54:51.906801|ops-lldpd|1001|LOG_INFO|LLDP Enabled
2016-03-22:17:54:57.573014|ops-lldpd|1003|LOG_INFO|Configured LLDP tx-timer with 100
2016-03-22:17:55:23.053182|ops-lldpd|1007|LOG_INFO|Configured LLDP Management pattern 10.0.0.1
2016-03-22:19:57:52.200040|ops-lldpd|1002|LOG_INFO|LLDP Disabled

switch# show events reverse

---------------------------------------------------
show event logs
---------------------------------------------------
2016-03-22:19:57:52.200040|ops-lldpd|1002|LOG_INFO|LLDP Disabled
2016-03-22:19:57:52.157195|ops-lldpd|1007|LOG_INFO|Configured LLDP Management pattern 10.0.0.1
2016-03-22:17:54:57.573014|ops-lldpd|1003|LOG_INFO|Configured LLDP tx-timer with 100
2016-03-22:17:54:51.906801|ops-lldpd|1001|LOG_INFO|LLDP Enabled


switch# show events severity info

---------------------------------------------------
show event logs
---------------------------------------------------
2016-03-22:17:54:51.906801|ops-lldpd|1001|LOG_INFO|LLDP Enabled
2016-03-22:17:54:57.573014|ops-lldpd|1003|LOG_INFO|Configured LLDP tx-timer with 100
2016-03-22:17:55:23.053182|ops-lldpd|1007|LOG_INFO|Configured LLDP Management pattern 10.0.0.1
2016-03-22:19:57:52.200040|ops-lldpd|1002|LOG_INFO|LLDP Disabled
```
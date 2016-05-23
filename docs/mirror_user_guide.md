# Port Mirroring User Guide
<!-- Version 0.1 -->

## Contents

- [Terminology used in this document](#terminology)
- [Overview](#overview)


## Terminology

##### Ports, Interfaces & LAGs
In this document the terms 'port' and 'interface' are used interchangably - a single logical interface which may represent one or more physical ports.  Note 'interface' is the keyword representing a port/interface when configuring the switch.
A collection of ports acting as a single logical interface is termed a 'LAG' - Link Aggregation Group, therefore an 'interface' can be an individual port, or a LAG.

In summary, you use the keyword interface to configure a switch port.  An interface can be a single port, or a multi-port LAG.

##### VLANs
Currently (release xxx) VLANs are not supported as source or destination interfaces.

##### Mirror Session
A given configuration of ports & associated commands in a Mirror is termed a 'Session'.





## Overview

##### Introduction

The Port Mirroring feature allows the replication of selected network traffic passing through the switch on one or more ports to another port for purposes such as monitoring.

Port Mirroring allows traffic replication independent of originating port VLAN or VRF membership.

A Mirror Session is used to create the desired mirroring configuration.  Up to 4 active Mirror Sessions can exist, while there is no fixed limit on the number of inactive sessions.

##### Mirror Port types

A valid Mirror Session is comprised of a single output, or 'destination' port and zero or more input, or 'source' ports.

The destination port, or interface, is the recipient of all mirrored traffic.  This port must be capable enough to receive the expected combined data rate of all configured source ports.


An added source port can be configured to mirror only received traffic on that port, only transmitted traffic, or traffic in both directions.

##### Mirror Port restrictions

Mirror Sessions are subject to a few Port Configuration rules under different conditions:

* 1: For a port to be eligible for addition to a mirror, it must not be a Layer3/route-only port.
* 2: A port cannot be added as both a source and destination within a given Mirror Session.

Once a Mirror Session is activated, the following rules also apply:

* 3: A Mirror Session's configured destination port must not be a source or destination in any other active Mirror Session
* 4: A Mirror Session's source ports must not be a destination in any other active Mirror Session

Notes:
* An active source port in one Mirror Session may be a source port in another active Mirror Session, assuming it also does not violate rules 2 & 4.
* At activation time, if the configuration of the Mirror Session violates rules 3 & 4 it will remain shutdown.
* It is permissible to configure multiple Mirror Sessions that violate rules 3 & 4 provided the sessions remain shutdown, i.e. you can configure multiple Mirror Sessions whose destination ports are the same/destination ports are sources in other mirrors, but only one of those overlapping sessions may be active at any given time. However rule 2 still applies in all cases, shutdown or not.



### Configuring Mirroring

#### Session creation

**Step 1: Enter configuration context**
```ditaa
# configure terminal
```

**Step 2: If necessary, activate ports to be added to the mirror, e.g.:**
```ditaa
(config)# interface 1
(config-if)# no shutdown
(config-if)# interface 2
(config-if)# no shutdown
(config-if)# interface 3
(config-if)# no shutdown
(config-if)# exit
```

**Step 3: Create a new mirror session (e.g. 'mirror_3')**
```ditaa
(config)# mirror session mirror_3
```

Note, if you specify the name of an existing mirror session you will be placed in the context of that existing mirror with no warning and you will affect it's configuration with any changes made.

At this point you can see the Mirror Session listed alongside existing Mirror Sessions via the 'show mirror' command.
```ditaa
(config-mirror)# do show mirror

name                                                            status
--------------------------------------------------------------- --------------
mirror_1                                                        active
mirror_2                                                        shutdown
mirror_3                                                        shutdown
```


#### Port addition

**Step 4: Add a destination port to the new Mirror Session**
```ditaa
(config-mirror)# destination interface 1
```
Note at this stage it is legal, though possibly not very useful, to activate the mirror.  A Mirror Session with no source ports can be active, waiting for the addition of it's first source port.

**Step 5: Add a port as a source of inbound/received traffic only**
```ditaa
(config-mirror)# source interface 2 rx
```
**Step 6: Add a port as a source of outbound/transmitted traffic only**
```ditaa
(config-mirror)# source interface 3 tx
```
**Step 7: Add a port as a source of traffic in both directions**
```ditaa
(config-mirror)# source interface 4 both
```



#### Mirror activation

Note that as with other switch configuration items, a mirror when created has an implicit 'shutdown' command configured even though it is not explicitly added. The 'no' form of the shutdown command removes that state and initiates activation.

```ditaa
(config-mirror)# no shutdown
```

Recheck the status of the mirror to ensure successful activation.
```ditaa
(config-mirror)# do show mirror
(config)#

name                                                            status
--------------------------------------------------------------- --------------
mirror_1                                                        active
mirror_2                                                        shutdown
mirror_3                                                        active
```
If the new session indicates it is still shutdown, consult the troubleshooting section in this guide on how to determine the problem.

You can also check the details of the mirror session to verify the ports are configured as added by specifying the mirror name with the show command:
```ditaa
(config-mirror)# do show mirror mirror_3
 Mirror Session: mirror_3
 Status: active
 Source: interface 4 both
 Source: interface 2 rx
 Source: interface 3 tx
 Destination: interface 1
 Output Packets: 0
 Output Bytes: 0
```

To leave the Mirror Session's context, use the 'exit' command.
```ditaa
(config-mirror)# exit
```

#### Limitations
* There is no limit to the number of Mirror Sessions that can be created.
* There is a limit of 4 active Sessions.
* There is a limit of one destination port per session
* There is no limit to the number of source ports per session


### Mirror Session modification

It is permissible to modify the port membership of a Mirror Session while active.  The following describes expected behavior when performing such modifications.

The mirror port rules described above still apply during port addition/modification operations on an active mirror.

**Option 1: Destination port removal/modification**

Removal:
If the output/destination port of a mirror is removed while active, this is accepted and results in immediate shutdown.
```ditaa
(config)# mirror session mirror_3
(config-mirror)# no destination interface
```
Modification:
You can also specify a different output/destination port without first removing the existing one:
```ditaa
(config)# mirror session mirror_3
(config-mirror)# destination interface 5
```
Assuming the new destination port abides by all of the rules, modification of the destination port causes immediate switchover of mirrored traffic to the new destination port.  Mirror Session remains active.


**Option 2: Source port removal/modification**
As mentioned previously, a source port can be mirrored in one of 3 different forms.  Inbound only (rx), outbound only (tx) or both inbound & outbound (both).

Unlike destination removal where you do not need to specify the port, since there can be multiple source ports you must specify the port name.  Optionally you can specify a direction - rx or tx.

If no direction is specified, the specified port is completely removed as a source in all directions regardless of the direction it was originally added, including 'both'.
```ditaa
(config)# mirror session mirror_3
(config-mirror)# no source interface 2
```
This is the simplest way to remove a source port entirely.
To remove a source port added with 'both', also use the directionless form. 'both' is not a valid option for removal.

A direction may be specified to remove mirroring in that particular direction if already added.  If the switch is not mirroring in the direction specified, whether explicitly or via 'both', there is no change.
```ditaa
(config)# mirror session mirror_3
(config-mirror)# no source interface 2 rx
```
Regarding an existing 'both' source port, and direction specific removal:
If a source port was originally added with 'both', removing direction 'rx' will remove mirroring from just that direction but leave the mirroring active in the 'tx' direction.  Conversely, removing direction 'tx' will leave mirroring active in the 'rx' direction.
In other words, for a 'both' source port, you can later restrict mirroring from that source port in a particular direction by removing mirroring in the opposite direction.


As an alternative to source port modification via the 'no' form of the 'source interface' command, you can re-specify a port's source mirroring preferences which will replace that port's current configuration.
For example if port 3 was already mirroring 'both', specifying a direction of 'rx' will result in the removal of mirroring in the 'tx' direction for that port and vice versa.
```ditaa
(config)# mirror session mirror_3
(config-mirror)# source interface 2 tx
```

**Option 3: Mirror Session disabling/deactivation**
To disable an active mirror, 'restore' the shutdown command removed during activation.
This results in the cessation of source port traffic being replicated to the destination port, the configuration is preserved.
```ditaa
(config)# mirror session mirror_3
(config-mirror)# shutdown
```

**Option 4: Mirror Session Removal**
This can be performed whether active or shutdown.  If the session is active, the mirroring of traffic ceases immediately.  Mirror Session configuration is deleted.
```ditaa
(config)# no mirror session mirror_3
```


### Displaying Mirror Session details

**What Mirror Sessions are configured / what is their state?**
```ditaa
(config)# show mirror

name                                                            status
--------------------------------------------------------------- --------------
mirror_1                                                        active
mirror_2                                                        shutdown
mirror_3                                                        active
```
Under normal operating conditions the status column will indicate a Mirror status of either 'active' or 'shutdown'.
In exceptional circumstances, mirror activation may fail and the status column will display an error.  This is indicative of severe system instability and a reboot is recommended.  If opening a support case please report the specific error message seen:
* Internal error
* Driver error
* Unknown error


**What is a Mirror Session's port membership / traffic statistics**
```ditaa
(config)# show mirror <mirror_name>

 Mirror Session: xyz
 Status: active
 Source: interface 4 both
 Source: interface 2 rx
 Source: interface 3 tx
 Destination: interface 1
 Output Packets: 143658
 Output Bytes: 1207498
```

### Troubleshooting Scenarios

**I am not seeing expected data on my capture device**

There are a number of factors that can lead to a Mirror Session not operating as expected.

Firstly verify physical connectivity for the source & destination ports you want to have in the Mirror Session.

Next ensure the link light is lit on the ports in question, and your capture device is configured correctly.

Lastly, check the details of the mirror session to ensure the desired ports are added & the session status is 'active'

```ditaa
(config)# show mirror <mirror_name>
```
If the expected ports are not present add them using the 'source interface' and/or 'destination interface' commands described in the 'Existing Mirror Session modification' section.


**I am seeing too much / not enough data on a configured source port**

Ensure that the source port you added is configured for the correct direction.  A source port can mirror traffic in one of three 'directions' on a port:
* Received traffic only ('rx')
* Transmitted traffic only ('tx')
* Both received & transmitted traffic ('both')

If the port is not added in the correct direction, modify the mirror by readding the port in the desired direction.

Or, remove the port entirely via the 'no source interface <interface>' command if mirroring is no longer necessary on that port.

If the session is not activated, do so using the 'no shutdown' command in mirror context.

# Mirroring User Guide
<!-- Version 0.1 -->

## Contents

- [Terminology used in this document](#terminology)
- [Overview](#overview)


## Terminology

##### Interfaces & LAGs
A collection of physical Interfaces acting as a single logical Interface is termed a 'LAG' - Link Aggregation Group. From a configuration standpoint, once the LAG is created, it is then considered an Interface unto itself.


##### VLANs
Currently, VLANs are not supported as source or destination Interfaces.

##### Mirror Session
A given configuration of Interfaces & associated commands in a Mirror is termed a 'Session'.





## Overview

##### Introduction

The Mirroring feature allows the replication of selected network traffic passing through the switch on one or more Interfaces to another Interface for purposes such as monitoring.

Mirroring allows traffic replication independent of originating Interface VLAN or VRF membership.

A Mirror Session is used to create the desired mirroring configuration.  Up to 4 active Mirror Sessions can exist, while there is no fixed limit on the number of inactive sessions.

##### Mirror Interface types

A valid Mirror Session is comprised of a single output, or 'destination' Interface and zero or more input, or 'source' Interfaces.

The destination Interface is the recipient of all mirrored traffic.  This Interface must be capable enough to receive the expected combined data rate of all configured source Interfaces.


Each source Interface can be individually configured to mirror only received traffic on that Interface, only transmitted traffic, or traffic in both directions.

##### Mirror Interface restrictions

Mirror Sessions are subject to a few Interface Configuration rules under different conditions:

1: For an Interface to be eligible as a mirror destination, it must not be a Layer3/route-only Interface nor participate in any form of Spanning Tree protocol.
2: An Interface cannot be added as both a source and destination within a given Mirror Session.

Once a Mirror Session is activated, the following rules also apply:

3: A Mirror Session's configured destination Interface must not be a source or destination in any other active Mirror Session
4: Any of a Mirror Session's source Interfaces must not be a destination in any other active Mirror Session

Notes:
* An active source Interface in one Mirror Session may be a source Interface in another active Mirror Session, assuming it also does not violate rules 2 & 4.
* When attempting to activate a mirror session (no shutdown), if the configuration of the Mirror Session violates rules 3 & 4 it will remain shutdown.
* It is permissible to configure multiple Mirror Sessions that violate rules 3 & 4 provided the sessions remain shutdown, e.g. multiple mirror sessions can be created with the same destination that would use the same monitor device, but only one session can use the device at a time.



### Configuring Mirroring

#### Session creation

**Step 1: Enter configuration context**
```ditaa
# configure terminal
```

**Step 2: If necessary, activate Interfaces to be added to the mirror, e.g.:**
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

Note, if you specify the name of an existing mirror session you will be placed in the context of that existing mirror and any changes will take effect immediately.

At this point you can see all Mirror Session and their status via the 'show mirror' command.
```ditaa
(config-mirror)# do show mirror

name                                                            status
--------------------------------------------------------------- --------------
mirror_1                                                        active
mirror_2                                                        shutdown
mirror_3                                                        shutdown
```


#### Interface addition

**Step 4: Add a destination Interface to the new Mirror Session**
```ditaa
(config-mirror)# destination interface 1
```
Note at this stage it is legal, though possibly not very useful, to activate the mirror.  A Mirror Session with no source Interfaces can be active, waiting for the addition of it's first source Interface.

**Step 5: Add an Interface as a source of inbound/received traffic only**
```ditaa
(config-mirror)# source interface 2 rx
```
**Step 6: Add an Interface as a source of outbound/transmitted traffic only**
```ditaa
(config-mirror)# source interface 3 tx
```
**Step 7: Add an Interface as a source of traffic in both directions**
```ditaa
(config-mirror)# source interface 4 both
```



#### Mirror activation

A mirror session when created is initially shutdown. Use the 'no' form of the shutdown command to change that state and initiate activation.

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

You can also check the details of the mirror session to verify the Interfaces are configured as added by specifying the mirror name with the show command:
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
* There is a limit of one destination Interface per session
* There is no limit to the number of source Interface per session


### Mirror Session modification

It is permissible to modify the Interface membership of a Mirror Session while active.  The following describes expected behavior when performing such modifications.

The mirror Interface rules described above still apply during Interface addition/modification operations on an active mirror.

**Option 1: Destination Interface removal/modification**

Removal:
If the output/destination Interface of a mirror is removed while active, this is accepted and results in immediate shutdown.
```ditaa
(config)# mirror session mirror_3
(config-mirror)# no destination interface
```
Modification:
You can also specify a different output/destination Interface without first removing the existing one:
```ditaa
(config)# mirror session mirror_3
(config-mirror)# destination interface 5
```
Assuming the new destination Interface abides by all of the rules, modification of the destination Interface causes immediate switchover of mirrored traffic to the new destination while the Mirror Session remains active.


**Option 2: Source Interface removal/modification**

To stop mirroring from a source Interface, use the 'no' form of the source Interface command:

```ditaa
(config)# mirror session mirror_3
(config-mirror)# no source interface 2
```

This ceases mirroring from that Interface completely regardless of the direction it was originally added with.

To change the direction of traffic mirrored on an existing source Interface, reenter the **source interface* command again with the new direction.

For example if Interface 3 was already mirroring 'both', specifying a direction of 'rx' will result in the removal of mirroring in the 'tx' direction for that Interface and vice versa.
```ditaa
(config)# mirror session mirror_3
(config-mirror)# source interface 2 tx
```

**Option 3: Mirror Session disabling/deactivation**
To disable an active mirror, 'restore' the shutdown command removed during activation.
This results in the cessation of source Interface traffic being replicated to the destination Interface, the configuration is preserved.
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
In exceptional circumstances, mirror activation may fail and the status column will display an error.  This is indicative of severe system instability and a reboot is recommended.  If opening a support case please reInterface the specific error message seen:
* Internal error
* Driver error
* Unknown error


**What is a Mirror Session's Interface membership / traffic statistics**
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

First run 'show interface' to verify each Interface are configured to be active (i.e. no shutdown) and link is established.

Next, check the details of the mirror session to ensure the desired Interfaces are added and the session status is 'active'

```ditaa
(config)# show mirror <mirror_name>
```
If the expected Interfaces are not present add them using the 'source interface' and/or 'destination interface' commands described in the 'Existing Mirror Session modification' section.


**I am seeing too much / not enough data on a configured source Interface**

Ensure that the source Interface you added is configured for the correct direction.  A source Interface can mirror traffic in one of three 'directions' on an Interface:
* Received traffic only ('rx')
* Transmitted traffic only ('tx')
* Both received & transmitted traffic ('both')

If the Interface is not added in the correct direction, modify the mirror session to specify the desired direction.

If mirroring is no longer necessary on that Interface, remove the Interface entirely via the 'no source interface <interface>' command.

Check that the total amount of source traffic does not exceed the capacity of the destination Interface.

If the session is not activated, do so using the 'no shutdown' command in mirror context.

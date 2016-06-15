# Port Mirroring User Guide


## Contents
	- [Overview](#overview)
		- [Mirror sessions](#mirror-sessions)
		- [Mirror rules](#mirror-rules)
		- [Creating a new mirror session](#creating-a-new-mirror-session)
		- [Editing an existing mirror session](#editing-an-existing-mirror-session)
			- [Removing the destination interface](#removing-the-destination-interface)
			- [Modifying the destination interface](#modifying-the-destination-interface)
			- [Modifying a source interface](#modifying-a-source-interface)
			- [Removing a source interface](#removing-a-source-interface)
			- [Deactivating a mirror session](#deactivating-a-mirror-session)
			- [Removing a mirror session](#removing-a-mirror-session)
		- [Displaying mirror session status](#displaying-mirror-session-status)
			- [Displaying a list of all configured mirror sessions](#displaying-a-list-of-all-configured-mirror-sessions)
			- [Displaying detailed mirror session information](#displaying-detailed-mirror-session-information)
		- [Troubleshooting](#troubleshooting)
			- [No data is being mirrored](#no-data-is-being-mirrored)
			- [Too much or not enough data is seen on the destination interface](#too-much-or-not-enough-data-is-seen-on-the-destination-interface)

## Overview
The port mirroring feature enables traffic on one or more switch interfaces to be replicated on another interface for purposes such as monitoring.

### Mirror sessions
A mirror session defines the settings for the replication of data between one or more source interfaces and a destination interface.

A maximum of four mirror sessions can be active at the same time on the switch. There is no limit on the number of inactive sessions that can be defined.

Each mirror session has a single output, or *destination* interface, and zero or more input, or *source* interfaces. The destination interface is the recipient of all mirrored traffic, and must able to support  the combined data rate of all source interfaces. Source interfaces can be configured to mirror received traffic, transmitted traffic, or all traffic. Source and destination interfaces do not need to reside in the same subnet, VLAN, VRF, or LAG.

A LAG can be specified as either a source or destination interface. The switch internally handles the mirroring of the traffic appropriately across all the LAG member interfaces.

Mirroring is VRF agnostic. That is, a network administrator may choose to specify source interfaces from different VRFs in the same mirror session and have a single destination for the mirrored traffic.

### Mirror rules

The following rules apply when creating a mirror session:

1. Layer 3 (routed) interfaces cannot be used as a source or destination in a mirror session.
2. An interface cannot be both a source and destination in the same mirror session.
3. The destination interface in an **active** mirror session cannot be the source or destination in another **active** mirror session.
4. The source interface in an **active** mirror session cannot be the destination in another **active** mirror session.
5. The destination interface cannot have an IP address.
6. The destination interface cannot have the spanning tree protocol enabled on it.

Note:
- If you try to activate a mirror session that violates rules 3 or 4 it will remain shutdown.
- The same interface can be the source in more than one mirror session as long as it does not violate rule 2 or 4.
- You can configure multiple session that violate rules 3 or 4 as long as they are not active at the same time.


### Creating a new mirror session

1. Change to configuration mode.
```
switch# configure terminal
```

2. Enable one or more interfaces to be added to the mirror session. In the following example, interface 1, 2, and 3 are enabled.
```
switch# (config)# interface 1
switch# (config-if)# no shutdown
switch# (config-if)# interface 2
switch# (config-if)# no shutdown
switch# (config-if)# interface 3
switch# (config-if)# no shutdown
switch# (config-if)# interface 4
switch# (config-if)# no shutdown
switch# (config-if)# exit
```

3. Create a new mirror session. In the following example, the session is called **mirror_3**.
```
switch# (config)# mirror session mirror_3
```

4. Set interface 1 as the destination.
```
switch# (config-mirror)# destination interface 1
```

5. Add source interface. In the following example, interface 2 will only mirror incoming traffic.
```
switch# (config-mirror)# source interface 2 rx
```

6. Add source interface. In the following example, interface 3 will only mirror outgoing traffic.
```
switch# (config-mirror)# source interface 3 tx
```

7. Add source interface. In the following example, interface 4 will mirror all traffic.
```
switch# (config-mirror)# source interface 4 both
```

8. Activate the mirror.
```
switch# (config-mirror)# no shutdown
```

9. View mirror status to verify activation.
```
  switch# (config-mirror)# do show mirror

  name                                                            status
  --------------------------------------------------------------- --------------
  mirror_3                                                        active
```

10. View detailed mirror status to verify all interfaces.
```
switch# (config-mirror)# do show mirror mirror_3
 Mirror Session: mirror_3
 Status: active
 Source: interface 4 both
 Source: interface 2 rx
 Source: interface 3 tx
 Destination: interface 1
 Output Packets: 143658
 Output Bytes: 1207498
```


### Editing an existing mirror session

Mirror sessions can be modified while active.

#### Removing the destination interface
Removing the destination interface from an active mirror results in immediate shutdown. For example:
```
switch# (config)# mirror session mirror_3
switch# (config-mirror)# no destination interface
switch# (config-mirror)# do show mirror

name                                                            status
--------------------------------------------------------------- --------------
mirror_3                                                        shutdown
```

#### Modifying the destination interface
A destination interface can be modified without removing the existing definition. The mirror session remains active and traffic is immediately sent to the new interface.
```
switch# (config)# mirror session mirror_3
switch# (config-mirror)# destination interface 5
switch# (config-mirror)# do show mirror mirror_3
 Mirror Session: mirror_3
 Status: active
 Source: interface 4 both
 Source: interface 2 rx
 Source: interface 3 tx
 Destination: interface 5
 Output Packets: 143658
 Output Bytes: 1207498
```

#### Modifying a source interface
To change the settings for a source port, re-issue the source command with the new settings. For example, if interface 3 is set to mirror both types of traffic, the following command changes it to only mirror transmitted traffic.
```
switch# (config)# mirror session mirror_3
switch# (config-mirror)# source interface 3 tx
```

#### Removing a source interface
The following example removes source interface 2 from the mirror_3 session.
```
switch# (config)# mirror session mirror_3
switch# (config-mirror)# no source interface 2
```

#### Deactivating a mirror session
```
(config)# mirror session mirror_3
(config-mirror)# shutdown
```

#### Removing a mirror session
This can be performed on both active and shutdown sessions.  If the session is active, mirroring of traffic stops immediately.
```
switch(config)# no mirror session mirror_3
```


### Displaying mirror session status

#### Displaying a list of all configured mirror sessions
```
swtich (config)# show mirror

name                                                            status
--------------------------------------------------------------- --------------
mirror_1                                                        active
mirror_2                                                        shutdown
mirror_3                                                        active
```


#### Displaying detailed mirror session information
```
switch(config)# show mirror <mirror_3>

 Mirror Session: xyz
 Status: active
 Source: interface 4 both
 Source: interface 2 rx
 Source: interface 3 tx
 Destination: interface 1
 Output Packets: 143658
 Output Bytes: 1207498
```

### Troubleshooting

#### No data is being mirrored

- Verify physical connectivity of the source and destination interfaces.
- Display details of the mirror session to ensure the desired ports are added and the session status is **active**.

#### Too much or not enough data is seen on the destination interface
Ensure that the source port you added is configured for the correct direction: receive, transmit, or both.

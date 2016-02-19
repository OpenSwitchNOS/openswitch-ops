Mirror Commands
======

## Contents

- [Mirror Session Configuration Commands](mirror_cli.md#mirror-session-configuration-commands)
  - [destination](mirror_cli.md#destination)
  - [shutdown](mirror_cli.md#shutdown)
  - [source](mirror_cli.md#source)
- [Mirror Show Commands](mirror_cli.md#display-commands)
  - [show mirror](mirror_cli.md#show-qos-cos-map)

Mirroring is the ability of a switch to transmit a copy of a packet out another port.  This allows network administrators to seamlessly inspect traffic flowing through the switch.

Mirroring is configured and controlled from a Mirror Session in the configuration context.

**NOTE:**  OpenSwitch 0.3 only supports mirroring traffic from one or more ports out another port.


## Mirror Session Configuration Commands

#### Syntax
```
mirror session <NAME>
no mirror session <NAME>
```

To create or edit an existing the Mirror Session context, enter **mirror session &lt;NAME&gt;**.

The following commands are available in the Mirror Session context:
- [destination](#destination)
- [shutdown](#shutdown)
- [source](#source)

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* |  Up to 64 letters, numbers, or underscores


#### Examples
```
switch# configure terminal
switch(config)# mirror session Port_1_Mirror
switch(config-mirror)#
```


## destination

#### Syntax
```
destination interface <INTERFACE>
no destination interface
```

#### Description
The **destination interface** command assigns the specified Ethernet interface or LAGG where all mirror traffic for this session will be transmitted.  Only one destination interface is allowed per session.

The **no destination** command will cease the use of the interface.

Changing the destination interface will cause a temporary suspension mirroring traffic from the source(s) during the reconfiguration.

##### Special Requirements for Destination Interfaces

To be qualified as a mirror session destination, the interface must:
- Not already be a source or destination in any other active mirror session
- Not participating in any form of Spanning Tree protocol
- Routing disabled
- No IP addresses configured on the destination
- When the destination is an Ethernet LAGG and members are added or removed while the mirror session is active, the session must be restarted for the change to be recognized

To clearly distinguish mirror traffic, it is best if the interface is either the sole member of a vlan or not a member of any vlan.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *INTERFACE* |  Ethernet interface or LAGG

#### Examples
```
switch# configure terminal
switch(config)# mirror session Mirror_3
switch(config-mirror)# destination interface 10
```

## shutdown

#### Syntax
```
shutdown
no shutdown
```

#### Description
By default a newly created mirror session is inactive.  To activate mirroring of traffic from the source(s) to the destination enter the **no shutdown** command.

The **shutdown** command will stop mirroring of traffic from the source to the destination.

**NOTE**:  Please refer to product documentation for the allowed number of simultaneous active mirror sessions.

#### Authority
All configuration users.

#### Examples
```
switch# configure terminal
switch(config)# qos schedule-profile Mirror_3
switch(config-mirror)# destination interface 10
switch(config-mirror)# source interface 20
switch(config-mirror)# no shutdown
```

## source

#### Syntax
```
source interface <INTERFACE> {both|rx|tx}
no source interface <INTERFACE>
```

#### Description
The **source interface** command assigns the specified Ethernet interface or LAGG where all mirror traffic for this session will be transmitted.  The parameter specifies which direction of traffic on the source port is mirrored:
- **both** - traffic received and transmitted
- **rx** only received traffic
- **tx** only transmitted traffic

More than one source interface can be configured in a mirror session, each with their own direction.

The direction of a source interface can be changed at any time by reentering the command.  This may  cause a temporary suspension mirroring traffic from all source(s) during the reconfiguration.

The **no destination <INTERFACE>** command will cease mirror traffic from the interface.

##### Special Requirements for Mirror Source Interfaces

To be qualified as a mirror session source, the interface must:
- Not already be a source or destination in any mirror session
- When the source is an Ethernet LAGG and members are added or removed while the mirror session is active, the session must be restarted for the change to be recognized

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *INTERFACE* |  Ethernet interface or LAGG

#### Examples
```
switch# configure terminal
switch(config)# mirror session Mirror_3
switch(config-mirror)# source interface 5 both
```


## Display Commands
The following commands show configuration and status information.

### show mirror

#### Syntax
```
show mirror [<NAME>]
```

#### Description
Without a 'name' parameter, this command will display the list of mirror sessions and their status.

With a 'name' parameter, this command will display the details of that mirror session.

#### Authority
All users.

#### Parameters
The optional 'NAME' parameter will display the details of that mirror session.

#### Examples
```
switch# show mirror
 name                                                            status
 --------------------------------------------------------------- --------------
 My_Session_1                                                    active
 Other_Session_2                                                 shutdown

switch# show mirror My_Session_1
 Mirror Session: My_Session_1
 Status: active
 Source: interface 2 both
 Source: interface 3 rx
 Destination: interface 1
 Output Packets: 123456789
 Output Bytes: 8912345678
```

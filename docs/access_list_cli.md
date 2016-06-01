# Access Control List (ACL) Commands

## Contents

- [Overview](#overview)
  - [Logging](#logging)
- [Configuration commands](#configuration-commands)
  - [access-list ip](#access-list-ip)
  - [permit/deny](#permitdeny)
  - [apply access-list](#apply-access-list)
  - [access-list log-timer](#access-list-log-timer)
- [Display commands](#display-commands)
  - [show access-list](#show-access-list)
  - [show access-list hitcounts](#show-access-list-hitcounts)

## Overview

Access control lists (ACLs) enable you to filter incoming traffic on an
interface based on a variety of criteria. An ACL is composed of one or more
access control entries (ACEs). Each ACE is a rule which defines the type of
traffic to match and the action to take (permit or deny the traffic), when a
match is found. Incoming traffic is evaluated against each ACE according to
their position in the list (determined by their sequence number). If incoming
traffic does not match any ACE, it is denied by default. Therefore, an empty
ACL will deny all incoming traffic.

### Logging

When you enable logging for an ACE, statistics for packets that match the deny
conditions of the ACE are logged. For example, if you define an ACE entry to
deny all packets from source address 209.157.22.26, statistics for packets that
are explicitly denied by the ACL entry are logged in the syslog buffer and in
SNMP traps sent by the switch.

The first time an ACL denies a packet, a syslog entry and SNMP trap are
generated, and a five-minute timer is started. The timer keeps track of all
packets explicitly denied by the ACL. After five minutes, a syslog entry is
generated for each ACE indicating the number of packets denied by the ACE
during this period.

If the ACL does not explicitly deny a packet during the five minute interval,
the timer stops. The timer restarts when the ACL explicitly denies a packet.

## Configuration commands

### access-list ip

#### Syntax

```
access-list ip <acl-name>
no access-list ip <acl-name>
```

#### Description

Changes to access control list (ACL) mode for the specified IPv4 ACL. If the
ACL does not exist, it is created.

Use the `no` form of this command to remove an ACL.

#### Command mode

Configuration mode (config).

#### Authority

Admin.

#### Parameters

| Parameter  | Status   | Syntax | Description              |
|:-----------|:---------|:------:|:-------------------------|
| *acl-name* | Required | String | The name of an IPv4 ACL. |

#### Example

###### Creating an access list called My_ACL

```
switch(config)# access-list ip My_ACL
```

### permit/deny

#### Syntax

```
[<sequence-number>] <action> <protocol-1> <source-ip> <destination-ip> [count] [log]

[<sequence-number>] <action> <protocol-2>
                    <source-ip>      [<condition> <port> | port <port-range>]
                    <destination-ip> [<condition> <port> | port <port-range>]
                    [count] [log]

<sequence-number> comment <comment-text>

no <sequence-number>
```

#### Description

Adds an access control list entry (ACE) to an ACL. ACEs are identified by a
sequence number, which determines the order in which ACEs are evaluated in an
ACL. ACEs with a lower sequence number are evaluated first.

Use the `no` form of this command to remove an ACE.

#### Command mode

Configuration mode (config).

#### Authority

Admin.

#### Parameters

| Name                | Status   | Syntax       | Description |
|---------------------|----------|--------------|-------------|
| *action*            | Required | Literal      | Specify **permit** to allow all traffic matching this ACE. Specify **deny** to drop all traffic matching this ACE. |
| *sequence-number*   | Optional | 1-4294967295 | Sequence number for this ACE. If no sequence number is specified, a sequence number is assigned equal to the highest ACE currently in the list plus 10.|
| *protocol-1*        | Required | String       | IP protocol to match. Specify **any** (to match traffic from any IP protocol). To match traffic from a specific protocol, specify the protocol name: **ah**, **gre**, **esp**, **icmp**, **igmp**, **pim**, or its IP protocol number. |
| *protocol-2*        | Required | String       | IP protocol to match. Specify the protocol name: **sctp**, **tcp**, or **udp**. |
| *source-ip*         | Required | String       | Source IP address to match. Specify **any** (to match traffic from any address). To match traffic from a specific address, specify the IPv4 address (A.B.C.D), and subnet mask in dotted-decimal or CIDR format: M.M.M.M or /MM. For example: 192.168.5.0/255.255.255.0 or 192.168.5.0/24.
| *destination-ip*    | Required | String       | Destination IP address to match. Specify **any** (to match traffic destined for any address). To match traffic destined for a specific address, specify the IPv4 address (A.B.C.D), and subnet mask in dotted-decimal or CIDR format: M.M.M.M or /MM. For example:  192.168.5.0/255.255.255.0 or 192.168.5.0/24.
| *condition*         | Optional | String       | Determines how traffic is checked for a match against the port number: **eq**=equal to, **gt**=greater than, **lt**=less than, **neg**=not equal to
| *port*              | Optional | String       | IP port number to match.
| *port-range*        | Optional | 0-65535      | Starting port number and ending port number. |
| **count**           | Optional | Literal      | Keep count of the number of packets matching this ACE. |
| **log**             | Optional | Literal      | Keep a log of the number of packets matching this ACE. |

#### Examples

###### Creating an ACL with three ACEs

- ACE 10: Permits UDP traffic from any address that is being sent to 172.16.1.0/24.
- ACE 20: Permits TCP traffic from 172.16.2.0/16, that is on port 1024 or higher and is being sent to any address.
- ACE 30: Denies all traffic on any protocol with any source or destination address. Enables counting to track all packets that are denied.

```
switch(config)# access-list ip My_ACL
switch(config-acl)# 10 permit udp any 172.16.1.0/24
switch(config-acl)# 20 permit tcp 172.16.2.0/16 gt 1023 any
switch(config-acl)# 30 deny any any any count
switch(config-acl)# exit
```

###### Adding a comment to an existing ACE

```
switch(config)# access-list ip My_ACL
switch(config-acl)# 20 comment Permit all TCP ephemeral ports
switch(config-acl)# do show access-list
switch(config-acl)# exit
```

###### Adding an ACE to an existing ACL

```
switch(config)# access-list ip My_ACL
switch(config-acl)# 25 permit icmp 172.16.2.0/16 any
switch(config-acl)# exit
```

###### Replacing an ACE in an existing ACL

```
switch(config)# access-list ip My_ACL
switch(config-acl)# 25 permit icmp 172.17.1.0/16 any
switch(config-acl)# exit
```

###### Removing an ACE from an ACL

```
switch(config)# access-list ip My_ACL
switch(config-acl)# no 25
switch(config-acl)# exit
```

###### Removing an ACL

```
switch(config)# no access-list ip My_ACL
```

### apply access-list

#### Syntax

```
apply access-list ip <acl-name> in
no apply access-list ip <acl-name> in
```

#### Description

Applies an ACL.

- When run in the interface context, it applies the specified ACL to the interface.
- When run in the VLAN context, it applies the specified ACL to the VLAN.

Only one direction (e.g. inbound) and type (e.g. IPv4) of ACL may be applied to
an interface or VLAN at a time.

#### Command mode

Configuration mode (config).

Interface mode (config-if).

#### Authority

Admin.

#### Parameters

| Name       | Status   | Syntax  | Description |
|------------|----------|---------|-------------|
| *acl-name* | Required | String  | Name of the ACL to apply. |

#### Examples

###### Applying **My\_ACL** to interfaces 1 and 2

```
switch(config)# interface 1
switch(config-if)# apply access-list ip My_ACL in
switch(config-if)# exit
switch(config)# interface 2
switch(config-if)# apply access-list ip My_ACL in
switch(config-if)# exit
switch(config)#
```

###### Replacing **My\_ACL** with **My\_Replacement\_ACL** on interface 1

```
switch(config)# interface 1
switch(config-if)# apply access-list ip My_Replacement_ACL in
switch(config-if)# exit
switch(config)#
```

###### Removing **My\_Replacement\_ACL** from interface 1

```
switch(config)# interface 1
switch(config-if)# no apply access-list ip My_Replacement_ACL in
switch(config-if)# exit
switch(config)#
```

### access-list log-timer

#### Syntax

```
access-list log-timer (default | <time>)
```

#### Description

Set the log timer frequency for all ACEs that have the `log` option enabled.

The first packet that matches an entry with the `log` keyword within an ACL log
timer window (configured with `access-list log-timer`) will have its header
contents extracted and sent to the configured logging destination (console,
syslog server, etc.). Each time the ACL log timer expires, a summary of all
ACEs with `log` configured will be sent to the logging destination.

#### Command mode

Configuration mode (config).

#### Authority

Admin.

#### Parameters

| Name        | Status | Syntax  | Description |
|-------------|--------|---------|-------------|
| **default** | Choice | Literal | Sets the log timer to its default value (300 seconds). |
| *time*      | Choice | 30-300  | Log time in seconds. |

#### Examples

###### Setting the ACL log timer to 120 seconds.

```
switch(config)# access-list log-timer 120
```

###### Resetting the ACL log timer to the default value.

```
switch(config)# access-list log-timer default
```

## Display commands

### show access-list

#### Syntax

```
show access-list [(interface | vlan) <id> [in]] [ip] [<acl-name>] [config]
```

#### Description

Displays all configured ACLs and their ACEs.

#### Authority

Admin.

#### Parameters

| Name          | Status   | Syntax  | Description |
|---------------|----------|---------|-------------|
| **interface** | Optional | Literal | Display ACLs applied to the specified interface. |
| **vlan**      | Optional | Literal | Display ACLs applied to the specified VLAN ID. |
| *id*          | Optional | String  | The name or ID of an interface or VLAN. |
| **in**        | Optional | String  | Limit display to ingress ACLs. |
| **ip**        | Optional | Literal | Limit display to IPv4 ACLs. |
| *acl-name*    | Optional | String  | Display the ACL matching this name. |
| **config**    | Optional | String  | Display output as CLI commands. |

#### Examples

Displaying all configured ACLs.

```
switch# show access-list
Type       Name
  Sequence Comment
           Action                          L3 Protocol
           Source IP Address               Source L4 Port(s)
           Destination IP Address          Destination L4 Port(s)
           Additional Parameters
-------------------------------------------------------------------------------
IPv4       My_ACL
        10 permit                          udp
           any
           172.16.1.0/24
        20 Permit all TCP ephemeral ports
           permit                          tcp
           172.16.2.0/16                    >  1023
           any
        30 deny                            any
           any
           any
           Hit-counts: enabled
-------------------------------------------------------------------------------
```

Displaying the CLI commands needed to create an ACL and its ACEs

```
switch# show access-list config
access-list ip My_ACL
    10 permit udp any 172.16.1.0/24
    20 permit tcp 172.16.2.0/16 gt 1023 any
    30 deny any any any count
```

### show access-list hitcounts

#### Syntax

```
show access-list hitcounts ip <acl-name> [(interface | vlan) <id> [in]]
clear access-list hitcounts (all | ip <acl-name> (interface | vlan) <id> [in])
```

#### Description

Display or clear hit counts for ACEs that have `count` enabled. If an ACE does
not have `count` enabled, the hit count is shown as `-`.

#### Authority

Admin.

#### Parameters

| Name          | Status   | Syntax  | Description |
|---------------|----------|---------|-------------|
| *all*         | Choice | Keyword | Operate on all ACLs. |
| **ip**        | Choice | Keyword | Operate on an IPv4 ACL. |
| *acl-name*    | Required | String  | Operate on a named ACL. |
| **interface** | Choice | Keyword | Specify the interface the ACL is applied to. |
| **vlan**      | Choice | Keyword | Specify the VLAN the ACL is applied to. |
| *id*          | Optional | String  | Interface name or VLAN ID. |
| **in**        | Optional | Keyword | Display information for ACLs applied to ingress traffic. |

#### Examples

###### Displaying hit counts for ACL a specific ACL

```
switch# show access-list hitcounts ip My_ACL interface 1
Statistics for ACL My_ACL (ipv4):
Interface 1 (in):
           Hit Count  Configuration
                   -  10 permit udp any 172.16.1.0/24
                   -  20 permit tcp 172.16.2.0/16 gt 1023 any
                   0  30 deny any any any count
```

###### Clearing hit counts for a specific ACL.

```
switch# clear access-list hitcounts ip My_ACL interface 1
```

###### Clearing hit counts for all configured ACLs.

```
switch# clear access-list hitcounts all
```

# Access Control List (ACL) Commands

## Contents

- [Configuration Context](#configuration-context)
  - [Creation, Modification, and Deletion](#creation-modification-and-deletion)
- [Global Context](#global-context)
  - [Display](#display)
- [Interface Configuration Context](#interface-configuration-context)
  - [Application, Replacement, and Removal](#application-replacement-and-removal)

## Configuration Context

### Creation, Modification, and Deletion

#### Syntax

```
    [no] access-list ip <acl-name>

        [no] <sequence-number>
             {permit|deny}
             {any|ah|gre|esp|icmp|igmp|pim|<ip-protocol-num>}
             {any|<source-ip-address>[/<source-subnet-mask>]}
             {any|<destination-ip-address>[/<destination-subnet-mask>]}

        [no] <sequence-number>
             {permit|deny}
             {sctp|tcp|udp}
             {any|<source-ip-address>[/<source-subnet-mask>]}
             [{eq|gt|lt|neq} <port>|range <min-port> <max-port>]
             {any|<destination-ip-address>[/<destination-subnet-mask>]}
             [{eq|gt|lt|neq} <port>|range <min-port> <max-port>]
```

#### Description

Creates an Access Control List (ACL) comprised of one or more Access Control
Entries (ACEs) ordered and prioritized by sequence numbers.

The `no` keyword can be used to delete either an ACL or an individual ACE.

An applied ACL will continue to process a packet until either the last ACE in
the list has been evaluated or the packet matches an ACE. If no ACEs are
matched, the packet will be denied (each ACL has an implicit default-deny ACE).

Note that an ACL must be applied via the `apply` command (at interface context)
before it will have an effect on traffic. If an ACL with no user-created
entries is applied, it will deny all traffic on the applied interface
(since only the implicit default-deny ACE will be present).

Entering an existing *acl-name* value will cause the existing ACL to be
modified, with any new *sequence-number* value creating an additional ACE, and
any existing *sequence-number* value replacing the existing ACE with the same
sequence number.

#### Authority

Admin.

#### Parameters

| Name                      | Status   | Syntax                     | Description |
|---------------------------|----------|------------------------    |-------------|
| *acl-name*                | Required | String                     | The name of this Access Control List (ACL). |
| *sequence-number*         | Required | Integer (1-4294967295)     | A sequence number for this Access List Entry (ACE). |
| *permit*, *deny*          | Required | Keyword                    | Permit or deny matching traffic. |
| *ip-protocol*             | Required | Keyword or Integer (1-255) | An IP Protocol number or name. |
| *source-ip-address*       | Required | IP Address or Keyword      | The source IP host, network address, or `any`. |
| *destination-ip-address*  | Required | IP Address or Keyword      | The destination IP host, network address, or `any`. |
| *eq*, *gt*, *lt*, *neq*   | Optional | Keyword                    | Match packets whose layer 4 port is equal to, greater than, less than, or not equal to the specified value. |
| *port*                    | Optional | Integer (0-65535)          | A single port qualified by an operator. |
| *range*                   | Optional | Keyword                    | Match ports starting and ending at the specified ports. |
| *min-port*, *max-port*    | Optional | Integer (0-65535)          | The start and end (inclusive) of a port range. |

#### Examples

Create an ACL and a few entries

```
switch(config)# access-list ip My_ACL
switch(config-acl)# 10 permit udp any 172.16.1.0/24
switch(config-acl)# 20 permit tcp 172.16.2.0/16 gt 1023 any
switch(config-acl)# 30 deny any any any
switch(config-acl)# exit
```

Add an entry to an existing ACL

```
switch(config)# access-list ip My_ACL
switch(config-acl)# 25 permit icmp 172.16.2.0/16 any
switch(config-acl)# exit
```

Remove an entry from an ACL

```
switch(config)# access-list ip My_ACL
switch(config-acl)# no 25
switch(config-acl)# exit
```

Remove an ACL

```
switch(config)# no access-list ip My_ACL
```

## Global Context

### Display

#### Syntax

```
    show access-list
```

#### Description

Displays configured access lists (ACLs) and their entries.

#### Authority

Admin.

#### Parameters

#### Examples

Display ACLs configured in above examples.

```
    switch# show access-list
    Type Name
              Seq Action Proto
                  Source IP          Port(s)
                  Destination IP     Port(s)
    -------------------------------------------------------------------------------
    ip   My_ACL
               10 permit udp
                  any
                  172.16.1.0/24
               20 permit tcp
                  172.16.2.0/16      gt    1023
                  any
               30 deny   any
                  any
                  any
```

## Interface Configuration Context

### Application, Replacement, and Removal

#### Syntax

```
    [no] apply access-list ip <acl-name> in
```

#### Description

Apply an Access Control List (ACL) to the current interface context.

Only one Ingress IPv4 ACL may be applied to an interface at a time, thus using
the `apply` command on an interface with an already-applied Ingress IPv4 ACL
will replace the currently applied ACL.

#### Authority

Admin.

#### Parameters

| Name       | Status   | Syntax | Description |
|------------|----------|--------|-------------|
| *acl-name* | Required | String | The name of Access Control List (ACL) to apply. |

#### Examples

Apply *My_ACL* on interfaces 1 and 2

```
    switch(config)# interface 1
    switch(config-if)# apply access-list ip My_ACL in
    switch(config-if)# exit
    switch(config)# interface 2
    switch(config-if)# apply access-list ip My_ACL in
    switch(config-if)# exit
    switch(config)#
```

Replace *My_ACL* with *My_Replacement_ACL* on interface 1
(following the above examples *My_ACL* remains applied to interface 2)

```
    switch(config)# interface 1
    switch(config-if)# apply access-list ip My_Replacement_ACL in
    switch(config-if)# exit
    switch(config)#
```

Apply no ACL on interface 1
(following the above examples *My_ACL* remains applied to interface 2)

```
    switch(config)# interface 1
    switch(config-if)# no apply access-list ip My_Replacement_ACL in
    switch(config-if)# exit
    switch(config)#
```

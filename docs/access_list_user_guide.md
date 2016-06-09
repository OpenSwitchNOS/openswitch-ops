Access control lists (ACLs)

 [TOC]

## Overview ##
ACLs can be used to help improve network performance and restrict network usage
by creating policies to eliminate unwanted IP traffic by filtering packets
where they enter the switch on layer 2 and layer 3 interfaces.

An access control list is an ordered list of one or more access control list
entries (ACEs) prioritized by sequence number. An incoming packet will be
matched sequentially against each entry in an ACL.  When a match is made, the
action of that ACE is taken and the packet is not compared against any more
ACEs in the list.


For ACL filtering to take effect, configure an ACL and then assign in the
inbound direction on either a layer 2 or layer 3 interface.

Please Note:
Every ACL will be configured with a 'deny any any any' entry as the last entry
in the list.  This entry is known as the implicit deny entry.  An ACL with no
user configured entries that is applied to an interface will be programmed in
hardware with the implicit deny entry.


## How to use the feature ##

###Setting up the basic configuration
Prior to applying an ACL to an interface, verify that traffic is flowing as
expected through unit.


Create an ACL

    switch(config)# access-list ip My_ACL


Add one or more entries to the list.

    switch(config-acl)# 10 permit udp any 172.16.1.0/24
    switch(config-acl)# 20 permit tcp 172.16.2.0/16 gt 1023 any
    switch(config-acl)# 30 deny any any any count
    switch(config-acl)# exit


Apply the ACL to an interface.

    switch(config)# interface 1
    switch(config-if)# apply access-list ip My_ACL in
    switch(config-if)# exit


Delete an ACL

    switch(config)# no access-list ip My_ACL


Configure the ACL logging timer.

    access-list log-timer 30


###Verifying the configuration

Use the following show commands to display the ACL configuration.


    show access-list [{interface} <id> [in]] [ip] [<acl-name>] [commands] [configuration]


The following refer to the above basic configuration example.

Show the ACL applied to interface 1:



    show access-list interface 1 in
    Direction
    Type       Name
      Sequence Comment
           Action                          L3 Protocol
           Source IP Address               Source L4 Port(s)
           Destination IP Address          Destination L4 Port(s)
           Additional Parameters
    -------------------------------------------------------------------------------
    Inbound
    IPv4       My_ACL
        10 permit                          udp
           any
           172.16.1.0/255.255.255.0
        20 permit                          tcp
           172.16.2.0/255.255.0.0           >  1023
           any
        30 deny                            any
           any
           any
           Hit-counts: enabled
    -------------------------------------------------------------------------------

Show all active ACLs configured on the system:


    show access-list
    Type       Name
      Sequence Comment
           Action                          L3 Protocol
           Source IP Address               Source L4 Port(s)
           Destination IP Address          Destination L4 Port(s)
           Additional Parameters
    -------------------------------------------------------------------------------
    IPv4       100
        10 permit                          tcp
           1.1.1.1/255.255.255.0
           2.2.2.2/255.255.255.0            >  1024
        20 permit                          udp
           1.1.1.1/255.255.255.0
           2.2.2.2/255.255.255.0            >  1024
    -------------------------------------------------------------------------------
    IPv4       My_ACL
        10 permit                          udp
           any
           172.16.1.0/255.255.255.0
        20 permit                          tcp
           172.16.2.0/255.255.0.0           >  1023
           any
        30 deny                            any
           any
           any
           Hit-counts: enabled
    -------------------------------------------------------------------------------


Show all ACLs configured by the user:


    show access-list configuration
    Type       Name
      Sequence Comment
           Action                          L3 Protocol
           Source IP Address               Source L4 Port(s)
           Destination IP Address          Destination L4 Port(s)
           Additional Parameters
    -------------------------------------------------------------------------------
    IPv4       100
        10 permit                          tcp
           1.1.1.1/255.255.255.0
           2.2.2.2/255.255.255.0            >  1024
        20 permit                          udp
           1.1.1.1/255.255.255.0
           2.2.2.2/255.255.255.0            >  1024
    -------------------------------------------------------------------------------
    IPv4       My_ACL
        10 permit                          udp
           any
           172.16.1.0/255.255.255.0
        20 permit                          tcp
           172.16.2.0/255.255.0.0           >  1023
           any
        30 deny                            any
           any
           any
           Hit-counts: enabled
    -------------------------------------------------------------------------------

Show the ACLs in command line format:

    show access-list commands
    access-list ip 100
        10 permit tcp 1.1.1.1/255.255.255.0 2.2.2.2/255.255.255.0 gt 1024
        20 permit udp 1.1.1.1/255.255.255.0 2.2.2.2/255.255.255.0 gt 1024
    access-list ip My_ACL
        10 permit udp any 172.16.1.0/255.255.255.0
        20 permit tcp 172.16.2.0/255.255.0.0 gt 1023 any
        30 deny any any any count
    interface 1
        apply access-list ip My_ACL in


Active configuration versus user-specified configuration.

The output from the 'show access-list' command will display the active
configuration of the product.  The active configuration displays the ACLs that
have been programmed in hardware.

The output from the 'show access-list' command with the 'configuration' option
will display the ACLs that have been configured by the user.  The output of this
command may not be the same as what has been programmed in hardware or what is
active on the box.  Unsupported command parameters may have been configured,
or unsupported applications specified.  To determine if there is a discrepancy
between what has been configured and what is active, run either the command
'show access-list commands' or 'show access-list commands configuration'.  If
the active ACLs and configured ACLs are not the same a warning message will be
displayed.

```
Warning: user-specified access-list apply does not match active configuration
```

If the warning message is displayed, the user may make additional changes until
the error message is no longer displayed when 'show access-list commands' or
'show access-list commands configuration' is entered, or run the command
'reset access-list'.  This will change the user specified configuration to match
the active configuration.


    switch# show access-list commands configuration
    access-list ip 100
        10 permit tcp 1.1.1.1/255.255.255.0 2.2.2.2/255.255.255.0 gt 1024
        20 permit udp 1.1.1.1/255.255.255.0 2.2.2.2/255.255.255.0 gt 1024
    access-list ip My_ACL
        10 permit udp any 172.16.1.0/255.255.255.0
        20 permit tcp 172.16.2.0/255.255.0.0 gt 1023 any
        30 deny any any any count
    interface 1
        apply access-list ip My_ACL in
    vlan 1
        apply access-list ip 100 in /* unsupported command */
    % Warning: user-specified access-list apply does not match active configuration
    switch(config)# reset access-list
    switch# show access-list commands configuration
    access-list ip 100
        10 permit tcp 1.1.1.1/255.255.255.0 2.2.2.2/255.255.255.0 gt 1024
        20 permit udp 1.1.1.1/255.255.255.0 2.2.2.2/255.255.255.0 gt 1024
    access-list ip My_ACL
        10 permit udp any 172.16.1.0/255.255.255.0
        20 permit tcp 172.16.2.0/255.255.0.0 gt 1023 any
        30 deny any any any count
    interface 1
        apply access-list ip My_ACL in


### Displaying ACL hitcounts
Hitcounts are available for ACEs that are created with the 'count' keyword
specified as in entry 30 in the example ACL My_ACL.  The ACL must be applied
to an interface and actively configured for the hitcounts to be valid.

    switch# show access-list hitcounts ip My_ACL interface 1 in
    Statistics for ACL My_ACL (ipv4):
    Interface 1 (in):
               Hit Count  Configuration
                       -  10 permit udp any 172.16.1.0/255.255.255.0
                       -  20 permit tcp 172.16.2.0/255.255.0.0 gt 1023 any
                    2045  30 deny any any any count

Please notice in the above output that only entry 30 displays a numerical
hitcount.  It is only this ACE that contains the 'count' keyword.




###Troubleshooting the configuration

#### Condition 1
IP traffic that was not explicitly denied is blocked.
#### Cause
The implicit deny entry is blocking the traffic.
#### Remedy
Add an ACE to explicitly permit the traffic.

#### Condition 2
An ACL with no entries is applied to an interface, all IP traffic is blocked.
#### Cause
The implicit deny entry is blocking the traffic.
#### Remedy
Add an ACE to explicitly permit the traffic.

#### Condition 3
An ACL is applied and is not blocking traffic
#### Cause
The ACL has been configured but is not active
#### Remedy
Run the command 'show access-list commands'.  If a warning message is displayed,
issue the 'reset access-list' command.  Re-run 'show access-list commands' to
verify the warning message is no longer displayed.

#### Condition 4
ACL not behaving as expected, permitted traffic is denied and/or denied traffic
is permitted.
#### Cause
Misconfigured ACL
#### Remedy
Enable the 'count' keyword on the troublesome ACEs.  While sending traffic run
the ACL hitcount show commands and monitor the counts of the ACEs.

## CLI ##
For the detailed list of ACL configuration commands Please see the
[Access Control List CLI Guide](http://openswitch.net/documents/user/access_list_cli).

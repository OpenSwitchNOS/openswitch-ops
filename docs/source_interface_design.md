# Source Interface Selection Design

## Contents
   - [High level design of source interface selection](#high-level-design-of-source-interface-selection)
   - [Internal structure](#internal-structure)
   - [OVSDB schema](#ovsdb-schema)
       - [System table](#system-table)
   - [References](#references)

## High level design of source interface selection
Note: As of now the CLI infrastructure is ready, but the end-to-end functionality of the source interface selection is not implemented. Protocol daemon for the specified protocols needs to implement this functionality.

When a host creates an IP packet, it must select some source address.  It gives the receiver the information needed to deliver a reply.If the source is selected incorrectly, in the best case, the backward path may appear different to the forward one which is harmful for performance. The source interface selection is used to set the IP address of an interface or IP address-defined interface as the source interface for the TFTP protocol or all the specified protocols like telnet, TFTP, radius, sflow and so on.

The source interface selection configuration can be do by the user through CLI. The CLI daemon updates the source interface selection configuration into the OVSDB. The protocol daemon gets the source interface selection details from the OVSDB and sets the appropriate protocol source interface of the specified protocol.


## Internal structure

```ditaa
Source Interface Selection

+----------------+           +----------------------+             +-----------------+
|   CLI          +----------->                      |             |                 |
|  daemon        |           |       OVSDB          +------------->   Protocol      |
|                <-----------+                      |             |   daemon        |
+----------------+           +----------------------+             +-----------------+
```

## OVSDB schema
### System table
```
System:other_config
Keys:
tftp_source
Value: source interface or IP address for tftp client
protocols_source
Value: source interface or IP address for all the protocols that support it.
```

## References
* Click [here](ops/docs/source_interface_user_guide.md) for source interface selection user guide.
* Click [here](ops/docs/source_interface_cli.md) for source interface selection CLI guide.

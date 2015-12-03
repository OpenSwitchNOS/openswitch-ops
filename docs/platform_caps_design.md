## Contents
  * [High level design of Platform Capabilties and
  * Capacities](#high-level-design-of-platform-capabilities-and-capacities)
    * [Design choices](#design-choices)
    * [Participating modules](#participating-modules)
  * [OVSDB-Schema](#ovsdb-schema)
  * [References](#references)

# High level design of Platform Capabilties and Capacities
Porting openswitch to a new hardware platform requires communicating hardware-specific capabilities and limits from the platform-dependent modules to the platform-independent modules. Modules in switchd and sysd determine the properties of switching ASIC and platform and populate SubSystem and System tables. User interfaces, daemons, and applications query the System table to determine which features are enabled and their limits, and act accordingly.

## Design choices

### Location of data
Other design considerations include putting capabilities and capacities in tables appropriate for the respective features and modules. The risk in doing so is that information of this type is spread across ovsdb and could be overlooked, which could lead to duplicate or inconsistent feature capability/capacity data. Consolidating the data into the System table provides a single source of truth in the database, with a well-known location and well-known keys.

### Allowable values
Several ideas were discussed in [IRC Discussions](#references)
* Lists for capabilities would allow consolidation of multiple related capabilities undera single key. e.g. acls_capable: in_ipv4, out_ipv4, in_mac, etc.
  * This would require an extra level of parsing, but allow a more compact representation in the database.
* Enums for capabilities - Allows for more fine-grained communication of capabilities but allowing more values than just true/false.
* Bitmaps for capabilities - Use an integer bitmap to represent related capabilities.

## Participating modules
```ditaa
+---------+   +---------+  +------+
|         |   | {s}     |  |      |
| daemons <--->         <--> apps |
+---------+   |         |  +------+
              |  ovsdb  <------+
              +----^----+      |
                   |           |
          +--------+----+   +--v-----------+
          | ops-switchd |   |   ops-sysd   |
          +--------^----+   +--+-----------+
                   |           |
          +--------v----+   +--v-----------+
          |   ASIC      |   |   Hardware   |
          +-------------+   +--------------+
```

During module initialization, switchd populates the capabilities and capacities columns in the OVSDB Subsystem table. The sysd module acts as an arbiter to summarize the data from multiple subsystems into the System table capacities and capabilities columns. Applications and daemons read the system-wide values from the System table.

## OVSDB-Schema
The specific keys and their meanings are documented in vswitch.xml.

### Capabilities
Capabilities can have a key that is present or not present. If a key is present, the value can be true or false.

Key Status     | Value   |  Meaning
---------------|---------|-----------------
Not present    | n/a     | feature is not supported
present        | true    | feature is supported and enabled
present        | false   | feature is supported but not enabled

### Capacities
Capacities can have a key that is present or not present. If a key is present, the value can be zero or greater than zero.

Key Status     | Value   |  Meaning
---------------|---------|-----------------
Not present    | n/a     | feature is not supported
present        | >0      | feature is supported and enabled, with limit specified by value
present        | 0       | feature is supported but not enabled

### Subsystem Table
```
Subsystem:capabilities
Keys: string
Values: boolean

Subsystem:capacities
Keys: string
Values: integer
```
### System Table
```
System:capabilities
Keys: string
Values: boolean

System:capacities
Keys: string
Values: integer
```

# References
[IRC Discussions] (http://eavesdrop.openswitch.net/meetings/platform_capabilities_and_capacities/2015/)

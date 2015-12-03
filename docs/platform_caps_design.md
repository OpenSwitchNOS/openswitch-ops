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
Discuss any design choices that were made.

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
* [Reference 1](http://www.openswitch.net/docs/redest1)

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

### Subsystem Table
```
Subsystem:capabilities
Keys: string
Values: string

Subsystem:capacities
Keys: string
Values: integer
```
### System Table
```
System:capabilities
Keys: string
Values: string

System:capacities
Keys: string
Values: integer
```

# References
* [Reference 1](http://www.openswitch.net/docs/redest1)

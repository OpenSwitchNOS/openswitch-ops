# Show Tech Infrastructure

## Contents
- [High level design of show tech infra](#high-level-design-of-show-tech-infra)
  - [Reponsibilities](#reponsibilities)
  - [Design choices](#design-choices)
  - [Block Diagram](#block-diagram)
  - [OVSDB-Schema](#ovsdb-schema)
  - [Show Tech Configuration Yaml File](#show-tech-configuration-yaml-file)
  - [Internal structure](#internal-structure)
    - [Source modules](#source-modules)
    - [Data structures](#data-structures)

# High level design of show tech infrastructure
   Show Tech Infrastructure helps to execute multiple show commands grouped under various feature and produce the output of those commands.  This helps the support and development engineers to analysis the system behaviour.

## Reponsibilities
The Show tech Infrastructure is responsible to execute multiple show commands grouped under different features and thus provide the overview of system or feature behaviour. This Infra consist of show tech configuration parser and cli component. Show Tech configuration parser is built as a library component, hence it could be imported by various daemon to get access to the show tech infra.

## Design choices
show tech infra could have been merged with the ops-cli. However, keeping these separate will help us to export the show tech infra as a module to other daemons and python scrips to perform more show tech analysis.


## Block Diagram
```ditaa
+-------------------+  Imports as     +-----------------------+
|                   |  library        |        ops-cli        |
|  Show Tech Infra  +---------------> |     (vtysh Daemon)    |
|     (Library)     |                 |                       |
|                   |                 |                       |
| +---------------+ |                 |    cli_showtech       |
| | Config Parser | |                 |          +            |
| +---------------+ |                 |          |            |
+-------------------+                 |          v            |
          ^                           |    show commands      |
          |                           |                       |
          |                           |                       |
          |                           +-----------------------+
          |
          |
  +-------+--------+
  | Show Tech      |
  | Configuration  |
  | File ( YAML)   |
  +----------------+

```

## OVSDB-Schema
ovsdb schema is not used for this feature.


##  Show Tech Configuration Yaml File

List of Show Tech Features and the corresponding commands to be executed under various features are specified in /etc/openswitch/supportability/ops_showtech.yaml configuration file.

The Yaml file is structured with the following elements

- feature
  * feature_name
  * feature_desc
  * cli_cmds
   * "command1"
   * "command2"
   * ...
  * sub_feature **(Optional)**
   * sub_feature_name
   * sub_feature_desc
   * cli_cmds
     * "command1"
     * "command2"
     * ..


Sample Yaml File with Two Feature Definition is shown below

```ditaa

---
  feature:
  -
    feature_desc: "Show Tech Basic"
    feature_name: basic
    cli_cmds:
      - "show version"
      - "show system"
      - "show vlan"
  feature:
  -
    feature_desc: "Link Layer Discovery Protocol"
    feature_name: lldp
    sub_feature:
      -
        sub_feature_desc: "LLDP Configuration"
        sub_feature_name: configuration
        cli_cmds:
          - "show lldp configuration"
    sub_feature:
      -
        sub_feature_desc: "LLDP Statistics"
        sub_feature_name: statistics
        cli_cmds:
          - "show lldp statistics"
    sub_feature:
      -
        sub_feature_desc: "LLDP Neighbor Info"
        sub_feature_name: neighbor-info
        cli_cmds:
          - "show lldp neighbor-info"


```


## Internal structure


### Source modules
```ditaa
  showtech.c
  showtech.h
```

### Data structures

Show tech Configuration Information from the configuration file (ops_showtech.yaml) is parsed and stored in linked list datastructure.
We mainly perform two operation on this datastructure.

1. Addition of New element O(1)
2. Search for a Element O(N)

We also have to preserve the order of the elements as they are defined in yaml configuration file.  Hence we are using simple linked list.

```ditaa
 struct clicmds
 {
  char* command;
  struct clicmds* next;
};

struct ovscolm
{
  char* name;
  struct ovscolm* next;
};

struct ovstable
{
  char* tablename;
  struct ovscolm* p_colmname;
  struct ovstable* next;
};

struct sub_feature
{
  char* name;
  char* desc;
  char no_sta_support;
  char support_stb;
  struct clicmds* p_clicmds;
  struct ovstable* p_ovstable;
  struct sub_feature* next;
};

struct feature
{
  char* name;
  char* desc;
  struct sub_feature* p_subfeature;
  struct feature* next;
};


+------------------+
| +------------------+
| | +------------------+
+-+ |  Features(1..N)  |
  +-+     +            |
    +------------------+
          |
          |
          |
          |      +---------------------+
          |      | +---------------------+
          +----> | | +---------------------+
                 +-+ |  SubFeatures(0..N)  |
                   +-+                     |
                     +--------+------------+
                              |
                              |
                              |         +---------------------+
                              |         | +---------------------+
                              +---------> | +---------------------+
                                        +-+ |  CliCommands(1..N)  |
                                          +-+                     |
                                            +---------------------+

```

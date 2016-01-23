# High level design of Diagnostic Dump
Primary goal of diagnostic module is to capture internal diagnostic information from  feature or daemon .


## Contents

- [Responsibilities](#responsibilities)
- [Design choices](#design-choices)
- [Participating modules](#participating-modules)
- [OVSDB-Schema](#ovsdb-schema)
- [Diagnostic Dump Configuration Yaml File](#diagnostic-dump-configuration-yaml-file)
- [Internal structure](#internal-structure)
	- [Source modules](#source-modules)
	- [Data structures](#data-structures)
- [References](#references)

##Responsibilities

Diagnostic infrastructure is responsible for capturing information from one or more daemon for a feature.

## Design choices
-One feature can be mapped with multiple daemon and one daemon can be mapped with multiple feature.
-User can change mapping of feature to daemon at runtime .
-Basic diagnostic is dumped to console , file using cli .

## Participating modules

``` ditaa
  +---------------+                   +-----------------------+
  |               |                   |                       |
  | Config Parser |  ---------------> |        diag-dump      |
  |               |                   |(vtysh unixctl client) |
  +---------------+                   |                       |
          ^                           +-----------------------+
          |                                       | ^
          |                                unixctl| |unixctl reply
          |                     diag-dump request | |
          |                                       v |
  +-------+--------+                   +-----------------------+
  | Diag dump      |                   |                       |
  | Configuration  |                   |    daemon             |
  | File ( YAML)   |                   |                       |
  +----------------+                   +-----------------------+


```


## OVSDB-Schema
ovsdb schema is not used for this feature.


##  Diagnostic Dump Configuration Yaml File

List of diag-dump features and corresponding mapped daemons are  specified in /etc/openswitch/supportability/ops_diagdump.yaml configuration file.

The Yaml file is structured with the following elements


  -
    feature_name: "feature1"
    feature_desc: "Description1"
    daemon:
      - "daemon1"
      - "daemon2"
      - "daemon3"

  -
    feature_name: "feature2"
    feature_desc: "Description2"
    daemon:
      - "daemon4"
      - "daemon5"
      - "daemon6"



Sample Yaml File with Two Feature Definition is shown below
```ditaa
  -
    feature_name: "lldp"
    feature_desc: "Link Layer Discovery Protocol"
    daemon:
      - "ops-lldpd"

  -
    feature_name: "lacp"
    feature_desc: "Link Aggregation Control Protocol"
    daemon:
      - "ops-lacpd"

```


## Internal structure


### Source modules
```ditaa
	diag_dump_vty.c
  diag_dump_vty.h
```

### Data structures

Diagnostic dump cli parses information from the configuration file (ops_diagdump.yaml) and stores in following data structures.

```


struct daemon {
   char* name;
   struct daemon* next;
};

struct feature {
   char* name;
   char* desc;
   struct daemon*   p_daemon;
   struct feature*   next;
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
                 +-+ |  Daemons(0..N)      |
                   +-+                     |
                     +--------+------------+


```


## References

* [Reference 1](http://www.openswitch.net)

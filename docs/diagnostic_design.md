# High level design of Diagnostic Dump
Primary goal of diagnostic module is to capture internal diagnostic information about features from related daemons.


## Contents

- [High level design of Diagnostic Dump](#high-level-design-of-diagnostic-dump)
	- [Contents](#contents)
	- [Responsibilities](#responsibilities)
	- [Design Choices](#design-choices)
	- [Participating Modules](#participating-modules)
	- [OVSDB-Schema](#ovsdb-schema)
	- [Diagnostic Dump Configuration Yaml File](#diagnostic-dump-configuration-yaml-file)
	- [Internal Structure](#internal-structure)
		- [Source Modules](#source-modules)
		- [Data Structures](#data-structures)
	- [API Detail](#api-detail)
		- [API Description](#api-description)
		- [Sample Code](#sample-code)
			- [BB Script](#bb-script)
			- [Header File](#header-file)
			- [Init Function](#init-function)
			- [Handler Function Definition](#handler-function-definition)
			- [Example For lldpd Daemon](#example-for-lldpd-daemon)
	- [References](#references)


##Responsibilities

Diagnostic infrastructure is responsible for capturing information from one or more daemon for a feature.

## Design Choices
-One feature can be mapped with multiple daemon and one daemon can be mapped with multiple feature.
-User can change mapping of feature to daemon at runtime .
-Basic diagnostic is dumped to console or file using CLI .
-CLI can't be blocked for more than 30 sec . If daemon doesn't reply to vtysh then timer handler in vtysh will release vtysh for next command.

## Participating Modules

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
Diag-dump uses a feature to daemon mapping file whose absolute path is /etc/openswitch/supportability/ops_diagdump.yaml

This Yaml file is structured with the following elements


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


## Internal Structure


### Source Modules
```ditaa
    diag_dump_vty.c
    diag_dump_vty.h
```

### Data Structures

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
## API Detail

Daemon initialisation function is required to register diagnostic dump basic handler function.
"INIT_DIAG_DUMP_BASIC" macro takes function name as argument and this function is callback handler for basic diag-dump.

###API Description

This macro registers it argument callback handler .
Callback function arguments are double pointer to buffer and character pointer to feature name.
Callback handler dynamically allocates memory as per requirement and populates required data in buffer.
This macro checks and send data inside buffer as reply to vtysh and free dynamically allocated memory.

```ditta
Syntax:
INIT_DIAG_DUMP_BASIC(basic_diag_handler_cb)
```

### Sample Code
#### BB Script
Add dependancy "DEPENDS = ops-supportability" in bbscript of respective daemon.
#### Header File
include diag_dump.h in .c file.
```ditta
#include  <diag_dump.h>
```
#### Init Function
Inside initialisation function invoke this macro with handler function.
INIT_DIAG_DUMP_BASIC(lldpd_diag_dump_basic_cb);

#### Handler Function Definition

```ditta
static void lldpd_diag_dump_basic_cb(const char *feature , char **buf)
{
    if (!buf && !*buf)
        return;
    *buf =  xcalloc(1,BUF_LEN);
    if (*buf) {
        /* populate data in buffer */
        lldpd_dump(*buf,BUF_LEN);
        VLOG_INFO("basic diag-dump data populated for feature %s",feature);
    } else{
        VLOG_INFO("Memory allocation failed for feature %s",feature);
    }
    return ;
}

```
#### Example For lldpd Daemon

```ditta
yocto/openswitch/meta-distro-openswitch/recipes-ops/l2/ops-lldpd.bb
DEPENDS = "ops-utils ops-config-yaml ops-ovsdb libevent openssl ops-supportability"



src/ops-lldpd/src/daemon/lldpd_ovsdb_if.c

#include  <diag_dump.h>

ovsdb_init(){
...
INIT_DIAG_DUMP_BASIC(lldpd_diag_dump_basic_cb);
...
}

/*
 * Function       : lldpd_diag_dump_basic_cb
 * Responsibility : callback handler function for diagnostic dump basic
 *                  it allocates memory as per requirement and populates data.
 *                  INIT_DIAG_DUMP_BASIC will free allocated memory.
 * Parameters     : feature name string,buffer pointer
 * Returns        : void
 */

static void lldpd_diag_dump_basic_cb(const char *feature , char **buf)
{
    if (!buf && !*buf)
        return;
    *buf =  xcalloc(1,BUF_LEN);
    if (*buf) {
        /* populate basic diagnostic data to buffer  */
        lldpd_dump(*buf,BUF_LEN);
        VLOG_INFO("basic diag-dump data populated for feature %s",feature);
    } else{
        VLOG_INFO("Memory allocation failed for feature %s",feature);
    }
    return ;
}



```

## References

* [Reference 1] 'diagnostic_design.md'

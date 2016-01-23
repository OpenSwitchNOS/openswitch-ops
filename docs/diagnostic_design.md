# High level design of Diagnostic Dump
Primary goal of diagnostic module is to capture internal diagnostic information about features from related daemons.


## Contents

- [High level design of Diagnostic Dump](#high-level-design-of-diagnostic-dump)
    - [Contents](#contents)
    - [Responsibilities](#responsibilities)
    - [Design choices](#design-choices)
    - [Participating modules](#participating-modules)
    - [OVSDB-Schema](#ovsdb-schema)
    - [Diagnostic Dump Configuration Yaml File](#diagnostic-dump-configuration-yaml-file)
    - [Internal structure](#internal-structure)
        - [Source modules](#source-modules)
        - [Data structures](#data-structures)
    - [API Detail](#api-detail)
        - [API Description](#api-description)
        - [Sample code:](#sample-code)
    - [References](#references)

##Responsibilities

Diagnostic infrastructure is responsible for capturing information from one or more daemon for a feature.

## Design choices
-One feature can be mapped with multiple daemon and one daemon can be mapped with multiple feature.
-User can change mapping of feature to daemon at runtime .
-Basic diagnostic is dumped to console or file using CLI .
-CLI can't be blocked for more than 30 sec . If daemon doesn't reply to vtysh then timer handler in vtysh will release vtysh for next command.

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
## API Detail

Daemon initiliazation function is required to register diagnostic dump handler function.
Inside this hanler function argv[1] contains the string of diagnostic type. i.e. either "basic" or "advanced".
Using if else condition it will populate corresponding data in buffer and finally send the response.


###API Description

unixctl_command_register registers a unixctl command with the given 'name'.  'usage' describes the
arguments to the command; it is used only for presentation to the user in "list-commands" output.
'cb' is called when the command is received.  It is passed an array
containing the command name and arguments, plus a copy of 'aux'.  Normally
'cb' should reply by calling unixctl_command_reply() or
unixctl_command_reply_error() before it returns, but if the command cannot
be handled immediately then it can defer the reply until later.  A given
connection can only process a single request at a time, so a reply must be
made eventually to avoid blocking that connection.

Syntax:
void  unixctl_command_register(const char *name, const char *usage,
                          int min_args, int max_args,
                          unixctl_cb_func *cb, void *aux)




unixctl_command_reply replies to the active unixctl connection 'conn'.  'result' is sent to the
client indicating the command was processed successfully.  Only one call to
unixctl_command_reply() or unixctl_command_reply_error() may be made per
request.

Syntax:
void  unixctl_command_reply(struct unixctl_conn *conn, const char *result);


unixctl_command_reply_error replies to the active unixctl connection 'conn'. 'error' is sent to the
client indicating an error occurred processing the command.  Only one call to
unixctl_command_reply() or unixctl_command_reply_error() may be made per request.

Syntax:
void  unixctl_command_reply_error(struct unixctl_conn *conn, const char *error);


###Sample code:

```ditta
/* register handler function in init  routine */
unixctl_command_register("dumpdiag", "", 1, 1,
                             lldp_unixctl_diag_dump, NULL);

/*
 * Function       : lldp_unixctl_diag_dump
 * Responsibility : callback handler function unixctl and send data in reply
 * Parameters     : unixctl_conn, argc,argv[]
 * Returns        : void
 */


static void
lldp_unixctl_diag_dump(struct unixctl_conn *conn, int argc ,
                   const char *argv[], void *aux OVS_UNUSED)
{
    /*
    Allocate buffer
    Check argv[] as "basic" or "advanced"
    populate data in buffer
    send unixctl reply
    */

    char *buf = xcalloc(1, BUF_LEN);
    if (buf){
        if(!strcmp(argv[1],DIAG_BASIC)){
            /*populate data for basic diagnostics */
            lldpd_dump(buf,BUF_LEN);
        } else if (!strcmp(argv[1],DIAG_ADVANCED)){
            strncpy(buf,"Advanced diagnostic is not supported",BUF_LEN);
        } else {
            snprintf(buf,BUF_LEN,
                    "Unknown option in diagnostic is not supported,%s %s",
                    "unknown option",argv[1]);
        }

        unixctl_command_reply(conn, buf);
        free(buf);
    } else {
        unixctl_command_reply_error(conn, "lldpd failed to allocate memory");
    }
    return;
}                               /* lldp_unixctl_diag_dump*/


#define BUF_LEN 4000
#define REM_BUF_LEN (buflen - 1 - strlen(buf))
static void
lldpd_dump(char* buf, int buflen)
{
    struct shash_node *sh_node;
    int first_row_done = 0;

    /*
     * Loop through all the current interfaces and figure out how many
     * have config changes that need action.
     */
    SHASH_FOR_EACH(sh_node, &all_interfaces) {

        struct interface_data *itf = sh_node->data;

        if (itf->hw && first_row_done == 0) {
            if (itf->hw->h_cfg->g_protocols[0].enabled)
                strcpy(buf, "\nLLDP : ENABLED\n\n");
            else
                strcpy(buf, "\nLLDP : DISABLED\n\n");
            strncat(buf, "    intf name\t|   OVSDB interface\t|"
                "   LLDPD Interface\t|    LLDP Status\t|  Link State\n",
                REM_BUF_LEN);
            strncat(buf,
                "==============================================="
                "===============================================\n",
                REM_BUF_LEN);
            first_row_done++;
        }

        strncat(buf, itf->name, REM_BUF_LEN);
        if (itf->ifrow)
            strncat(buf, "\t\t|    Yes", REM_BUF_LEN);
        else
            strncat(buf, "\t\t|    No\t", REM_BUF_LEN);
        if (itf->hw) {
            strncat(buf, "\t\t|    Yes", REM_BUF_LEN);
            if (itf->hw->h_enable_dir == HARDWARE_ENABLE_DIR_OFF)
                strncat(buf, "\t\t|    off", REM_BUF_LEN);
            if (itf->hw->h_enable_dir == HARDWARE_ENABLE_DIR_TX)
                strncat(buf, "\t\t|    tx", REM_BUF_LEN);
            if (itf->hw->h_enable_dir == HARDWARE_ENABLE_DIR_RX)
                strncat(buf, "\t\t|    rx", REM_BUF_LEN);
            if (itf->hw->h_enable_dir == HARDWARE_ENABLE_DIR_RXTX)
                strncat(buf, "\t\t|    rxtx", REM_BUF_LEN);
        } else
            strncat(buf, "\t\t|No\t\t|", REM_BUF_LEN);

        if (itf->hw) {
            if (itf->hw->h_link_state == INTERFACE_LINK_STATE_UP)
                strncat(buf, "\t\t|    up", REM_BUF_LEN);
            else
                strncat(buf, "\t\t|    down", REM_BUF_LEN);
        }

        strncat(buf, "\n", REM_BUF_LEN);
    }
}


```

## References

* [Reference 1] 'diagnostic_design.md'

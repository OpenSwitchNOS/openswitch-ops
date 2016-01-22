# High Level Design of Event logging Infra

Event logging Infrastructure helps us to log important events occuring in the system.  This helps the customer as well as the support team to understand the system behaviour better.

## Contents
- [Responsibilities](#responsibilities)
- [Design choice](#design-choice)
- [Block Diagram](#block-diagram)
- [OVSDB-Schema](#ovsdb-schema)
- [Event logging Configuration Yaml File](#event-logging-configuration-yaml-file)
- [Event Initialization](#event-initialization)
- [Event Logging](#event-logging)
- [Configure rsyslog](#configure-rsyslog)
- [Data structures](#data-structures)


## Responsibilities
The Event logging Infrastructure is responsible to store and manage Event logs from different Features/Daemons.

## Design choice
Event log infrastructure is a part of supportability library.  Event Definitions are present in the event log configuration yaml file.
Information about the events of the corresponding modules are read from this yaml file and kept in the datastructure.  Later this information is referred while logging the events.

For Event Logging we are using sd_journal_send api and log it directly to the systemd journal.  Later the event logs are copied from journal to a seperate eventlog file for easy access.

## Block Diagram

```ditaa
event_log_init(event_category)

 +--------------+      +-------------+
 | (libyaml)    |store |  evt_table  |
 | parsing yaml +------+             |
 +------+-------+table +------^---+--+
        ^                     |   |
        |                     |   |
        |                     |   |
 +------+-------+             |   |
 | Event yaml   |             |   |log_EVent(event_name,key->Value)
 |    File      |         +---+---v--------+
 +--------------+         | sd_journal_send|
                          |                |
                          +------+---------+
                                 |
  CLI command                    v
 +--------------+        +-------+------+
 | show events  |        |   journal    |
 |              | <------+              |
 +--------------+        +-------+------+
                                 | forwarded
                                 |   to
                          +------v-------+
                          |    rsyslog   |
                          |              |
                          +-------+------+
                                  | rsyslog.conf
                                  |
                           +------v-------+
                           |   event.log  |
                           |              |
                           +--------------+

```

## OVSDB-Schema
ovsdb schema is not used for this feature.


## Event logging Configuration Yaml File

List of Event log Categories are defined in yaml file.

eg: Event_Groups:
  event_category: LLDP
  event category: FAN
  event category: OSPF
  event category: BGP

Event_Definition:
event_name: A unique name for the event.
event_category: event_category is already added into event category list.
evt_ID: first 2 digits belongs to event category and last 3 for its events.
severity: LOG_EMER, LOG_ALER, LOG_CRIT, LOG_ERR, LOG_WARN, LOG_NOTICE, LOG_INFO
Keys: The variables that need to be populated during run time.
event_description: The event description string.

Define your feature specific events as per the below format in event.yaml file.

Yaml file should be under /etc/supportability/event.yaml

Sample Yaml File with Two daemon events Definition is shown below.

---

   categories:
   -
       event_category: LLDP_EVENTS
       description: 'Events related to LLDP_A'
   -
       event category: LLDP_A
       description: 'Events related to LLDP_A'
   -
       event category: LLDP_B
       description: 'Events related to LLDP_B'
   -
       event category: FAN_EVENT
       description: 'Events related to FAN'

event_definitions:
  -
   event_name: LLDP_A
     event_category: LLDP
     event_ID : 01001
     severity: LOG_INFO
     keys: X, Y
     event_description: 'LLDP {X} ADDED ON {Y}'
  -
   event_name: LLDP_B
     event_category: LLDP
     event_ID : 01002
     severity: LOG_INFO
     keys: x,y
     event_description: 'LLDP neighbor added on {x} with {y}'
  -
   event_name: FAN_EVENT
     event_category: FAN
     event_ID : 02001
     severity: LOG_EMER
     keys: key1,key2
     event_description: 'High temperature detected'

## Event Initialization
    API Prototype: int event_log_init("event_category")

Each Feature should call event_log_init() API during it's init or just before logging an event.
- Initialize feature or event category specific events for the daemon.
- returns 0 on sucess , -1 on failure.
- an argument of event_log_init API is event_category.The category of events which needs to be initialized for the daemon.

Example:
  (a) event_log_init("LLDP")
  (b) event_log_init("FAN")
  (c) event_log_init("OSPF")


## Event Logging
  API Prototype: `int log_event(char *event_name, char *key-value1, char *key-value2,...)`

Log an event using log_event () API.
-  Log the specified feature event.
-  returns 0 on success , -1 on failure.
-  arguments are passed in log_event API are event_name- unique event name as defined in YAML file,
   Key, Value - This should be specified as KV("Key", format-specifier, Value)
   Example:KV("lldp_neighbour", "%d", test)

Example:
  (a)log_event("LLDP_A", KV("X", "%d", value_of_X), KV("Y", "%s", "testing" ))
  (b)log_event("FAN_EVENT", NULL)

## Configure rsyslog

    rsyslog.conf is configured file to store logs in separate file event.log.


## Data structures

Event log Configuration file event.yaml is parsed and stored in the following data structure.
```
typedef struct{
    int event_id;
    char event_name[64];
    char severity[24];
    int num_of_keys;
    char event_description[240];
    }event;

event ev_table[1024];
```

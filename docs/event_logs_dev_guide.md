# Event Log Infrastructure Developer Guide

## Contents

- [Overview](#overview)
- [How to define event log in YAML file](#how-to-define-event-log-in-yaml-file)
- [Sample yaml File](#sample-yaml-file)
- [API usage](#api-usage)
- [show events CLI](#show-events-cli)

## Overview
Event Logging provides system administrators/support/lab with information useful for diagnostics and
auditing. This facilitates localization and allows system administrators/support/lab to more easily
obtain information on problem that occur and provide an appropriate solution to problem.

Event Logging infrastructure in Openswitch makes use of Linux JournalD. The structured event logs would be stored in the Journal.


## How to define event log in YAML file
Event Log infrastructure makes use of a YAML file to define events and their corresponding categories.

The event yaml file is placed in ops-supportability repo under the path "ops-supportability/conf/ops_events.yaml"

The structure of this file is as shown below


Categories:
     - event_category:
       description:
       category_rank:

event_definitions:
      - event_name:
        event_category:
        event_ID :
        severity:
        keys:
        event_description:

## Sample yaml File

```ditaa

categories:
      - event_category: LLDP_EVENTS
        description: 'Events related to LLDP_A'
	    category_rank: 001

      - event category: LLDP_A
        description: 'Events related to LLDP_A'
	    category_rank: 002

      - event category: LLDP_B
        description: 'Events related to LLDP_B'
	    category_rank: 003

      - event category: FAN_EVENT
        description: 'Events related to FAN'
	    category_rank: 004

event_definitions:

      - event_name: LLDP_A
        event_category: LLDP
        event_ID : 001001
        severity: LOG_INFO
        keys: X, Y
        event_description: 'LLDP {X} ADDED ON {Y}'

      - event_name: LLDP_B
        event_category: LLDP
        event_ID : 001002
        severity: LOG_INFO
        keys: x,y
        event_description: 'LLDP neighbor added on {x} with {y}'

      - event_name: FAN_EVENT
        event_category: FAN
        event_ID : 002001
        severity: LOG_EMER
        keys: key1,key2
        event_description: 'High temperature detected'
```

## API usage

Every daemon which defined their event category of interest & events in YAML file are supposed to call event_log_init(category_name) during initialization. This will enable that daemon to log all the events in that category using log_events(event_name, key-values,...) API.

The following are the syntax of the API's:

int event_log_init("event_category");

- Initialize feature or event category specific events for the daemon.

- returns 0 on success , -1 on failure.

- an argument of event_log_init API is event_category.The category of events which needs to be initialized for the daemon.

Example:
 (a) event_log_init("LLDP")
 (b) event_log_init("FAN")
 (c) event_log_init("OSPF")


Events can be logged using:
```
int log_event(char *event_name, char *key-value1, char *key-value2,...)
```
- arguments are passed in log_event API are event_name- unique event name as defined in YAML
file,
 Key, Value - This should be specified as KV("Key", format-specifier, Value)

Example:KV("lldp_neighbour", "%d", test)

(a)log_event("LLDP_A", KV("X", "%d", value_of_X), KV("Y", "%s", "testing" ))
(b)log_event("FAN_EVENT", NULL)


## show events CLI

The logged events could be viewed from the vtysh shell by invoking the command "show events".

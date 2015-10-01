High level design of REST API
============================

The feature is a combination of REST API documentation rendering engine and the corresponding REST API service engine that serves the supported API functionalities.

Design choices
--------------
The feature aims to serve the needs of DevOps to set and change configurations on a switch as well as to retrieve status and statistics information of the switch. It also serves as a building block for the web UI of the switch. It mainly exposes operations on OVSDB through REST API. The resources serviced by the API is therefore based on the schema of the OVSDB.

Participating modules
---------------------
The feature is essentially composed out of two modules, restd (REST daemon) and restapi (REST API rendering). The restapi module is configured in a way that points to the same host and the same port as the entry point for all the documented REST API operations.

           URL path
               +
               |
   +-----------+------------+
   +                        +
 /api                /rest/v1/system
   +                        +
   |                        |
   |                        |
   v                        v
REST API                REST API
rendering               servicing

The URL path name space is used to direct web requests to appropriate module for processing accordingly to the diagram above.

During switch image build time, REST API servicing module generates and installs the REST API documentation file in JSON format for REST API rendering module to use at runtime.

OVSDB-Schema
------------
An extended schema file based on the original OVSDB schema file is created with two additional groups of tags to indicate how this feature should expose each resource through the REST API.

1. "category": ["configuration" | "status" | "statistics"]
Indicate for each column of a table whether the attribute is a configuration (readable and writable), status (read-only) or statistics (mostly counters that change frequently). For those columns of the table that are not marked with any one of the category tags, they are not exposed in REST API.

2. "relationship": ["1:m" | "m:1" | "reference"]
Indicate for those columns pointing to other tables whether the relationship between the table cited at the column and the current table is child ("1:m"), parent ("m:1") or reference. The REST API utilizes this information to construct resource structure among the tables in the schema file.

The two groups of tags can be used simultaneously when the column refers to some other table. For the columns that are tagged with "relationship", the "category" tag can be either "configuration" (read-write) or "status" (read-only).

A sanitizing Python script is run to strip the extended schema file of the two groups of tags added, so that other modules depending on the original OVSDB schema can operate as usual.

References
----------
* [REST API user guide](http://www.openswitch.net/docs/REST_API_user_guide.md)
* [REST API rendering component design](http://www.openswitch.net/docs/REST_API_design.md)
* [REST daemon component design](http://www.openswitch.net/docs/REST_daemon_design.md)

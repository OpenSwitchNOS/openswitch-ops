# High Level Design of REST API

## Contents

- [Introduction](#introduction)
- [Design choices](#design-choices)
- [Participating modules](#participating-modules)
- [OVSDB schema](#ovsdb-schema)
- [HTTPS support](#https-support)
- [Logs support](#logs-support)
- [References](#references)

## Introduction
The feature is a combination of the REST API documentation rendering engine and the corresponding REST API service engine that serves the supported API functionalities.

## Design choices

This feature sets and changes switch configurations, as well as retrieves status and statistics information of the switch. It also serves as a building block for the web UI of the switch.

Its main function exposes operations on OVSDB through the REST API. The resources serviced by the API are therefore based on the schema of the OVSDB.

## Participating modules

This feature has two modules:
- REST daemon (restd) -- Serves REST API requests.
- REST API rendering (restapi) -- Configured so that it points to the same host and the same port as the entry point for all of the documented REST API operations.

```ditaa
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

```

The URL path name space is used to direct web requests to the appropriate module for processing according to the diagram above.

During the switch image build time, the REST API servicing module generates and installs the REST API documentation file in JSON format, for the REST API rendering module to use at runtime.

## OVSDB schema

The new OVSDB schema is an extended schema file based on the original OVSDB schema file. The new schema is marked with two additional groups of tags, which indicate how this feature exposes each resource through the REST API:

- The "category": ["configuration" | "status" | "statistics"] tags
indicate for each column of a table, whether the attribute is categorized as configuration (readable and writable), status (read-only), or statistics (mostly counters that change frequently). For those columns of the table that are not marked with any one of the category tags, they are not exposed in the REST API.

- The "relationship": ["1:m" | "m:1" | "reference"] tags
indicate for those columns pointing to other tables, whether the relationship between the table cited at the column and the current table is child ("1:m"), parent ("m:1"), or reference. The REST API utilizes this information to construct a resource structure among the tables in the schema file.

The two groups of tags can be used simultaneously when the column refers to another table. For the columns that are tagged with "relationship", the "category" tag can be either "configuration" (read-write) or "status" (read-only).

A sanitizing Python script is run to strip the extended schema file of the two groups of tags added, so that other modules that are aware of only the original OVSDB schema can operate as usual.

## HTTPS support

The REST API runs only on the HTTPS protocol. The HTTPS protocol provides authentication of the REST server, and additionally provides encryption of exchanged data between the REST server and the client. Authentication/encryption is done by security protocols like SSL/TLS within the HTTP connection.

The REST server requires SSL certificate to run in HTTPS mode. A self-signed SSL certificate and private key files are pre-installed at "/etc/ssl/certs/server.crt" and "/etc/ssl/certs/server-private.key" respectively on the server. Steps to obtain a self-signed certificate are standard. The self-signed SSL certificate is mainly for development purposes and testing. For proper authentication, a user may have to purchase a SSL certificate for a specific hostname from a trusted Certificate Authority (CA), for example Symantec.

Once the SSL certificate is enrolled with a trusted CA, the certificate file and private key file are copied into predefined locations, "/etc/ssl/certs/server.crt" and "/etc/ssl/certs/server-private.key", on the REST server using scp. The client uses the CA certificate to verify the server authenticity when establishing an HTTPS connection.
Following is a sample client side code snippet that is compatible with Python 2.7.9 and retrieves ports information from a REST server:
```ditaa
import ssl
import httplib

sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
sslcontext.verify_mode = ssl.CERT_REQUIRED
sslcontext.check_hostname = True
sslcontext.load_verify_locations("/etc/ssl/certs/server.crt")
url = '/rest/v1/system/ports'
conn = httplib.HTTPSConnection("172.17.0.3", 443, context=sslcontext)
conn.request('GET', url, None, headers=_headers)
response = conn.getresponse()

```

Following is an example URL with HTTPS to query ports on the system from a web browser. HTTPS uses the default port 443 if not specified.
```https://172.17.0.3/rest/v1/system/ports```

## Logs Support
### Design
REST APIs for logs provides an interface to query the systemd journal. The API internally calls the Journalctl linux command to read the systemd journal. Journalctl command was chosen as it has several filtering options and is an easy tool for accessing all the systemd/kernel logs. It also provides the output in JSON pretty format which is required for REST. The REST server does not modify the output from the journalctl command as it is already in JSON format.

### Log API definitions
- ```GET https://10.10.0.1/rest/v1/logs```
Returns complete system journal output in json. This may be a huge output depending on how long the system is running. Hence, it is recommended to use filtering options to retrieve the logs that are of interest.

-  ```GET https://10.10.0.1/rest/v1/logs?priority=<0-7>```
Returns log output filtered by the given log priority level. Priority levels are similar to syslog levels 0-7. All logs with input level or a lower level (important) levels will be returned.

- ```GET https://10.10.0.1/rest/v1/logs?since=”yyyy-mm-dd
hh:mm:ss”;until=”yyyy-mm-dd hh:mm:ss”```
Returns output filtered by the given time window.
Instead of specific time, user can also give relative words like “yesterday”, “1 day ago”, “2 hours ago” etc;
```GET https://10.10.0.1/rest/v1/logs?since="2 hours ago"```
Returns log messages generated in the past 2 hour time window.


- ```GET https://10.10.0.1/rest/v1/logs?after-cursor=”cursor_string”```
Returns log output after a specified location in the log journal as indicated by the cursor. Cursor is maintained by the systemd journald service.  For e.g. If the user wants to retrieve the logs since the last request, the user will have to provide the valid cursor value returned in the previous request at the bottom of the output e.g. cursor: s=66e980e3c7bc46bea313de741ce481bc;i=8598c;b=78537df4874046d5ae9f251193b9f0bc;m=285fc88ec04;t=52bd96c4fa130;x=2f797c4c0bb5eafc

- ```GET https://10.10.0.1/rest/v1/logs?cursor=”cursor_string”```
Returns logs from the location specified by the passed cursor in the log output. Cursor is shown as the last entry in the output.

- ```GET https://10.10.0.1/rest/v1/logs?offset=<int>;limit=<int>```
As the log output can be huge, pagination is required to see the output in chunks. In order to retrieve the logs in pages, user may use the offset and limit parameters.  `Offset` is the starting point to obtain the results and the limit defines the number of logs returned in a page. Pagination parameters ```offset``` and ```limit``` can be used along with other filtering parameters.
For example ```GET https://10.10.0.1/rest/v1/logs?priority=<0-7>;offset=<int>;limit=<int>```


- ```Get https://10.10.0.1/rest/v1/logs?<field>=<value>```
Returns the output based on the fields in the system journal. The following fields are supported:
    |Field       | Description                                                             |
    ----------   |--------------------------------------------------------------------------
    |MESSAGE     | Exact log message that is expected in string format.
    |MESSAGE_ID  | A 128-bit message identifier ID for recognizing certain message types. All openswitch events are stored with this message ID 50c0fa81c2a545ec982a54293f1b1945 in the system journal. Use this MESSAGE_ID in string format to query all the events.
    |PRIORITY     | A priority value between 0 ("emerg") and 7 ("debug").
    |SYSLOG_IDENTIFIER | Identifier string is the module generating the log message. Use this field to filter logs by a specific module.
    |_PID | Process ID of the process that is generating the log entry.
    |_UID | User ID of the process that is generating the log entry.
    |_GID | Group ID of the process that is generating the log entry.
   Following is an example of the log API response.
```{

	"__CURSOR" : "s=66e980e3c7bc46bea313de741ce481bc;i=9d56f;b=78537df4874046d5ae9f251193b9f0bc;m=294bd70c2b9;t=52be82d3777e5;x=97f095510c616684",
	"__REALTIME_TIMESTAMP" : "1455651074570213",
	"__MONOTONIC_TIMESTAMP" : "2837856699065",
	"_BOOT_ID" : "78537df4874046d5ae9f251193b9f0bc",
	"_TRANSPORT" : "syslog",
	"PRIORITY" : "5",
	"SYSLOG_FACILITY" : "3",
	"SYSLOG_IDENTIFIER" : "ops-switchd",
	"_PID" : "193",
	"_UID" : "0",
	"_GID" : "0",
	"_COMM" : "ops-switchd",
	"_EXE" : "/usr/sbin/ops-switchd",
	"_CMDLINE" : "/usr/sbin/ops-switchd --no-chdir --pidfile --detach -vSYSLOG:INFO",
	"_CAP_EFFECTIVE" : "3fffffffff",
	"_SYSTEMD_CGROUP" : "/system.slice/switchd.service",
	"_SYSTEMD_UNIT" : "switchd.service",
	"_SYSTEMD_SLICE" : "system.slice",
	"_MACHINE_ID" : "1547d722b8f04e1d8c4993c9664d625c",
	"_HOSTNAME" : "switch",
	"MESSAGE" : "ovs|383379|ovsdb_idl|INFO|DEBUG first row is missing from table class Neighbor",
	"_SOURCE_REALTIME_TIMESTAMP" : "1455651074569511"
}
```

## References

* [REST API user guide](/documents/user/REST_API_user_guide)
* [REST API rendering component design](/documents/user/REST_API_design)

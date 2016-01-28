# High Level Design of REST API

## Contents

- [Introduction](#introduction)
- [Design choices](#design-choices)
- [Participating modules](#participating-modules)
- [OVSDB schema](#ovsdb-schema)
- [HTTPS support](#https-support)
- [Events](#events)
    - [WebSockets](#websockets)
    - [Subscriptions](#subscriptions)
    - [Notifications](#notifications)
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

Following is an example URL with HTTPS to query ports on the system from a web browser:
`https://172.17.0.3/rest/v1/system/ports`

HTTPS uses the default port 443 if not specified.


## Events
Clients can subscribe to events to be notified about changes within the database. The REST daemon is the entry point for subscribing to events. Clients can subscribe to specific row and column changes, or all changes to a table. The REST daemon receives notifications from the OVSDB indicating changes. The changes, if subscribed to, are notified to the clients.

```ditaa
    +------------+
    |            |
    |            |
    |  Client 1  |
    |            |   /ws    +----------------+       +----------------+
    |            +----------+                |       |                |
    +------------+          |                |       |                |
                            |     restd      +-------+     OVSDB      |
    +------------+   /ws    |                |       |                |
    |            +----------+                |       |                |
    |            |          +----------------+       +----------------+
    |  Client N  |
    |            |
    |            |
    +------------+
```

### WebSockets
The REST daemon exposes a WebSocket interface via the underlying Tornado web framework for subscribing and receiving event notifications and is accessible at the `/ws` path, where `ws` denotes WebSocket. Clients subscribe to specific events through the WebSocket. The REST daemon records the event subscriptions associated with the client by the established WebSocket connection. When the REST daemon receives notification of changes from the OVSDB, the REST daemon informs the clients through the WebSocket.

The REST daemon maintains a reference to the WebSocket upon connection establishment. OVSDB changes trigger pushes to the client using the WebSocket. Reference to the WebSocket, along with the associated events, are removed upon WebSocket disconnect.

WebSocket messages are formatted in JSON with the following fields:

- **type**: Type can be either a `request` or a `response`.
- **data**: Contains the application data.
- **status**: Status in response to the request. Can be either `successful` or `error`.
- **info**: Contains information about the failed request.

**Example of a request:**

```
{
    "type": "request",
    "data": {
        "event": {
            ...
        }
    }
}
```

**Example of an error response:**

```
{
    "type": "response",
    "status": "error",
    "info": "Unsupported application type"
}
```

### Subscriptions
The client subscribes by sending a JSON indicating the resource URI or table name, and fields to subscribe to. More than one subscriptions in an event request is permitted. To subscribe to a specific row, the `resource` field should contain the full URI, such as: `/system/vrfs/vrf_default/bgp_routers/1` and the `type` needs to be set to `row`. If the `fields` array is empty, changes to all columns are registered; otherwise, only specific columns are registered to. Each event must have an `event_id` field that is unique to this subscriber. To subscribe to a table, the `resource` field should include name of the table and the `type` should be set to `table`, as shown in the second element of the `event` key below. For table events, any change will trigger a notification and does not utilize `fields`.

**Subscription JSON**

```
{
    "type": "request",
    "data": {
        "event": {
            "subscriptions": [{
                "event_id": "1",
                "type": "row",
                "resource": "/rest/v1/system/vrfs/vrf_default/bgp_routers/1",
                "fields": ["router_id", "timers"]
            }, {
                "event_id": "2",
                "type": "table",
                "resource": "VRF"
            }]
        }
    }
}
```

Upon receiving the subscription request, the REST daemon attempts to register the client. All subscriptions must be successful. If the request fails due to invalid `resource` or `fields`, the daemon responds with the errors and an event `status` of `unsuccessful`. The `errors` field contains the error messages associated with the `event_id`. If the request is successful, the response includes a `successful` status without the `errors` field.

**Subscription failure response JSON**

```
{
    "type": "response",
    "status": "successful",
    "data": {
        "event": {
            "status": "unsuccessful",
            "errors": [{
                "event_id": "1",
                "messages": [
                    "Invalid column router_idx",
                    "Invalid column timersx"
                ]
            }, {
                "event_id": "2",
                "messages": [
                    "Invalid resource URI"
                ]
            }]
        }
    }
}
```

**Subscription success response JSON**

```
{
    "type": "response",
    "status": "successful",
    "data": {
        "event": {
            "status": "successful"
        }
    }
}
```

### Notifications
When changes in the database are detected, the REST daemon notifies the corresponding clients that subscribed. The notification is pushed to the client in JSON format, which includes the URI and the fields affected. Notifications do not require a response.

If an update occurred on the row, the `change` field is set to `updated` and the `details` field includes the names of the columns changed. If the row is deleted, the `change` field is set to `deleted` and  excludes the `details` field. The notification includes the new value as `value`. Currently, table changes including rows added, updated, and deleted, are all represented as `change` of `updated`.

**Notification JSON**

```
{
    "type": "request",
    "data": {
        "event": {
            "notifications": [{
                "event_id": "1",
                "change": "updated",
                "details": ["router_id"]
            }, {
                "event_id": "2",
                "change": "updated"
            }]
        }
    }
}
```

## References

* [REST API user guide](/documents/user/REST_API_user_guide)
* [REST API rendering component design](/documents/user/REST_API_design)

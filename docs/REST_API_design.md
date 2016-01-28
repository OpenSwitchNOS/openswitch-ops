# High Level Design of REST API

## Contents

- [Introduction](#introduction)
- [Design choices](#design-choices)
- [Participating modules](#participating-modules)
- [OVSDB schema](#ovsdb-schema)
- [HTTPS support](#https-support)
- [Events](#events)
    - [WebSockets](#websockets)
    - [REST Event Subscriptions](#rest-event-subscriptions)
    - [REST Event Notifications](#rest-event-notifications)
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
Clients can subscribe to events to be notified about changes within the database. The REST daemon is the entry point for subscribing to events. Clients can subscribe to specific rows or table changes through REST APIs. The REST daemon receives notifications from the OVSDB indicating changes and are notified to the clients.

```ditaa
    +------------+
    |            |
    |            |
    |  Client 1  |
    |            |  WebSocket  +----------------+       +----------------+
    |            +-------------+                |       |                |
    +------------+             |                |       |                |
                               |     restd      +-------+     OVSDB      |
    +------------+  WebSocket  |                |       |                |
    |            +-------------+                |       |                |
    |            |             +----------------+       +----------------+
    |  Client N  |
    |            |
    |            |
    +------------+
```

### WebSockets
The REST daemon exposes a WebSocket interface via the underlying Tornado web framework for receiving event notifications and is accessible at the `/rest/v1/ws/events` path. When the REST daemon receives notification of changes from the OVSDB, the REST daemon informs the clients through the WebSocket. The WebSocket connection is authenticated upon the initial HTTP handshake before upgrading to WebSockets.

The REST daemon maintains a reference to the WebSocket upon connection establishment and adds a new `REST_Event_Subscriber` resource into the OVSDB. The new subscriber resource is assigned an auto-generated random value for the `name`, and `ws` is set for the subscriber `type`. The REST daemon returns the URI to the subscriber resource created to the WebSocket client upon connection establishment, for example:

```
{
    "rest_event_subscriber": {
        "resource_uri": "/rest/v1/system/rest_event_subscribers/3562910982"
    }
}
```

OVSDB changes trigger pushes to the client using the WebSocket identified by its `name`. Reference to the WebSocket, along with the associated subscriber and event resources, are removed upon WebSocket disconnect.

### REST Event Subscriptions
Clients subscribe to events through REST APIs. Sending a POST request to, for example, `/rest/v1/system/rest_event_subscribers/3562910982/rest_event_subscriptions`, will create a new `REST_Event_Subscription` resource and subscribe the client to the event. The event subscription request includes a `resource_uri` to subscribe to. The client can subscribe to a specific resource or a collection of resources. For example, to subscribe to a specific resource for changes, the client can subscribe to the `/rest/v1/system/vrfs/vrf_default` URI, and  the `/rest/v1/system/vrfs` URI for a collection of `VRF` changes. Subscribing to a resource will monitor for modifications and deletion. Subscriptions for URIs without an explicit parent will subscribe to the complete collection. Subscribing to a collection that has a parent will monitor a collection of resources that are children of that parent, and will only monitor for additions and deletions. For example, subscribing to `/rest/v1/system/vrfs/vrf_default/bgp_routers` will monitor `BGP_Router` resources that are children of the `vrf_default` resource.

**Example: Subscription JSON**

```
{
    "configuration": {
        "resource_uri": "/rest/v1/system/vrfs/vrf_default"
    }
}
```

The `resource_uri` field will be validated and will result in a `400` error response, such as `Invalid resource URI` if the resource does not exist. Upon a successful subscription, the initial values for the subscribed URIs are sent as notifications to the client.

The POST request for an event subscription results in the URI of the new resource in the response, which includes the index of the event relative to the subscriber. For example, the first event subscription for subscriber `3562910982` will result in a response with the following JSON data:

```
{
    "event_subscription": {
        "resource_uri": "/rest/v1/system/rest_event_subscribers/3562910982/rest_event_subscriptions/0"
    }
}
```

A second IDL is used to monitor for specific changes, on an as-needed basis, to increase the performance by avoiding the need to subscribe to every resource and attributes. The second IDL will only be used for event subscriptions.

### REST Event Notifications
When changes in the database are detected, the REST daemon notifies the corresponding clients that subscribed. The notification is pushed to the client in JSON format, which includes the URI and the attributes updated. Notifications do not require a response.

The notification message contains the `notifications` field and includes URIs for resources that are `added`, `modified`, and `deleted`. When a resource that belongs to a monitored parent is added, the `added` field contains a list of changes that include the `subscription_uri` of the subscription, `resource_uri` of the resource added, and the initial `values`.

When a resource is modified, the `modified` field contains a list of changes that includes the `subscription_uri` of the subscription, `resource_uri` of the resource modified, and the `new_values` of attributes that were updated.

When a resource is deleted, the `deleted` field contains a list of changes that includes the `subscription_uri` of the subscription and the `resource_uri` of the resource deleted.

**Notification JSON**

```
{
    "notifications": {
        "added": [{
            "subscription_uri": "/rest/v1/system/rest_event_subscribers/3562910982/rest_event_subscriptions/1",
            "resource_uri": "/rest/v1/system/vrfs/vrf_default/bgp_routers/1/bgp_neighbors/2.2.2.2",
            "values": {
                "remote_as": 2,
                ...
            }
        }],
        "modified": [{
            "subscription_uri": "/rest/v1/system/rest_event_subscribers/3562910982/rest_event_subscriptions/0",
            "resource_uri": "/rest/v1/system/vrfs/vrf_default/bgp_routers/1",
            "new_values": {
                "router_id": "1.1.1.1",
                "maximum_paths": 5,
            }
        }],
        "deleted": [{
            "subscription_uri": "/rest/v1/system/rest_event_subscribers/3562910982/rest_event_subscriptions/2",
            "resource_uri": "/rest/v1/system/vrfs/vrf_default/bgp_routers/1/bgp_neighbors/3.3.3.3"
        }]
    }
}
```

## References

* [REST API user guide](/documents/user/REST_API_user_guide)
* [REST API rendering component design](/documents/user/REST_API_design)

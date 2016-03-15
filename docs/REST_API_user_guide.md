# REST API

## Contents

- [Overview](#overview)
- [How to use this feature](#how-to-use-this-feature)
  - [Setting up the basic configuration](#setting-up-the-basic-configuration)
  - [Troubleshooting the configuration](#troubleshooting-the-configuration)
    - [Condition](#condition)
    - [Cause](#cause)
  - [Entry point](#entry-point)
- [CLI](#cli)
- [Related features](#related-features)
- [WebSockets](#websockets)
- [Events](#events)
  - [Subscribing](#subscribing)
  - [Notification](#notification)
  - [Events over websockets](#events-over-websockets)

## Overview ##
The REST_API provides a management interface to interact with a switch. You can utilize the API to retrieve status and statistics information of the switch, as well as to set and change the configuration of the switch. Switch configurations, statuses, and statistics can also be subscribed to for event notifications of changes.

This feature provides two major functionalities:

- REST API service engine -- Processes REST API operation requests.

- REST API documentation rendering engine -- Presents a web interface documenting the supported REST API. You can interact with the REST API service engine running on the same switch through this web interface.

## How to use this feature

### Setting up the basic configuration

This feature is included in the switch image build and is enabled by default. This feature cannot be turned off through CLI. You do not need to do anything other than basic network connectivity to the switch to use this feature.

### Troubleshooting the configuration

#### Condition
Error in accessing the URIs supported by the REST API.

#### Cause
- Switch network connectivity issue
- REST daemon fails to start or has crashed

#### Remedy
- Ping the switch at the given IP address after making sure that the IP address is configured for the management interface of the switch.
- Make sure that the REST daemon is running.

### Entry point

The URL for accessing REST API documentation rendered on the switch is:

`http://management_interface_ip_address-or-switch_name:8091/api/index.html`

The default port is `8091`. When HTTPS is used, the corresponding default port is `443`.

To access details about the supported REST API without running a switch image, see the following website for information:

`http://api.openswitch.net/rest/dist/index.html`

## CLI
This feature is an alternative to the CLI mechanism as a management interface. It has no CLIs of its own.

## Related features
The configuration daemon and API modules utilize configuration read and write capabilities provided by this feature in the form of Python libraries.

## WebSockets
REST supports handling of websockets for a persistent connection between clients and the switch. Currently, only [events](#events) is supported over websockets. A websocket connection can be established at the `ws://management_interface_ip_address-or-switch_name:8091/ws` URI.

### Requests
To send a request over a websocket to the switch, the payload must be in JSON format and follow the specified syntax. The syntax of the requests contain the `type` and `data` fields. The `type` field indicates the type of the message, which contains the value `request`. The `data` field contains the application's JSON data. For example, the `data` field includes JSON data for the `event` field to include the event application data, as shown below:

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

### Responses
The syntax of the responses contain the `type`, `status`, and `data` fields. The `type` field contains the value `response`. The `status` field is either `successful` or `unsuccessful`. The `data` field contains the application's response in JSON format, as shown below:

```
{
    "type": "response",
    "status": "successful",
    "data": {
        "event": {
            ...
        }
    }
}
```

If a websocket request results in an `unsuccessful` status, the message also contains an `info` field, which provides more information about the error encountered.

## Events
The REST implementation supports event notifications for changes that the clients subscribe to. Clients may subscribe to be notified about switch configurations, statuses, and statistics changes. The events implementation uses websockets.

### Subscribing
To subscribe to a switch configuration, status, or statistic, the client must send a request that includes the `event_id`, `resource`, `type`, and `fields` keys in the JSON formatted request. The `event_id` is a unique identifier associated with the event for this subscriber. The `event_id` is not unique across different subscribers/clients. The `resource` field indicates a table name or a URI for a specific resource. The `type` field indicates the type of resource the event is subscribing to, which is either `table` or `row`. If the `type` is `row`, the `fields` key contains a list of columns to subscribe for changes. If the `type` is `table`, the `fields` key is not used since it tracks all changes related to the table.

Events are added to the `subscriptions` field. More than one event can be added to the request to subscribe to multiple switch configurations, statistics, and statuses.

**Example of a subscription request**
```
{
    "subscriptions": [
        {
            "event_id": "1",
            "resource": "Port",
            "type": "table"
        }
    ]
}
```

The subscription request may fail in the following cases:

- The `type` field indicates a `table` and the `resource` field contains an invalid table name.
- The `type` field indicates a `row` and the `resource` field contains an invalid resource URI.
- The `type` field indicates a `row` and the `resource` is valid, but the `fields` key contains an invalid configuration, statistic, or status name as defined in the schema.

If a subscription request fails, the response contains a `status` of `unsuccessful` and contains an `errors` field indicating the errors. Failures for each event can be identified by the `event_id` in the response. For each failed event subscription, the `messages` field contains the errors, as shown below:

**Example of an unsuccessful subscription response**
```
{
    "status": "unsuccessful",
    "errors": [
        {
            "event_id": "2",
            "messages": [
                "Invalid column invalid_column"
            ]
        }
    ]
}
```

Upon an event subscription error, no events are stored.

### Notification
When the REST daemon detects configuration, statistic, and status changes, it will identify if there are any event subscriptions associated and notify the clients. The notifications are sent in JSON format with the `event_id`, `change`, and `details` fields. The `event_id` helps the client to identify the associated event the notification is for. The `change` field indicates if a table is `updated`, or if a row is `updated` or `deleted`. If a row is updated, it will include the `details` field indicating the specific changes that triggered the notification.

**Example of a notification**
```
{
    "notifications": [
        {
            "event_id": "1",
            "change": "updated"
        },
        {
            "event_id": "2",
            "change": "updated",
            "details": [
                "trunks"
            ]
        }
    ]
}
```

### Events over websockets
All events subscribed to over websockets are cleared upon websocket disconnect. The events associated with the websocket is not persisted and the client will need to re-establish the websocket connection and resubscribe.

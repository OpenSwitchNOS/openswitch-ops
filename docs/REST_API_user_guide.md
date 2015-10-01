# REST API
#Table of contents

 [TOC]

## Overview ##
REST_API is a feature that provides a management interface to interact with a switch. You can utilize the API to retrieve status and statistics information of the switch, as well as to set and change the configuration of the switch.

The feature provides two major functionalities. One is REST API service engine, which processes REST API operation requests. The other is REST API documentation rendering engine, which presents a web interface documenting the supported REST API. You can interact with the REST API service engine running on the same switch through this web interface.

## How to use the feature ##

###Setting up the basic configuration

The feature is included in switch image build and is enabled by default. The feature cannot be turned off through CLI. You do not need to do anything other than basic network connectivity to the switch to use the feature.

###Verifying the configuration

Not applicable.

###Troubleshooting the configuration

#### Condition
Error in accessing the URIs supported by the REST API.
#### Cause
- Network connectivity issue to the switch
- REST daemon fails to start or has crashed
#### Remedy
- Make sure that the IP address is configured for the management interface of the switch and you can ping the switch at the given IP address.
- Make sure that the REST daemon is running.

### Entry point

The URL for accessing REST API documentation rendered on the switch is:
> http://management_interface_ip_address-or-switch_name:8091/api/index.html

The default port is 8091. When https is used, the corresponding default port is 18091.

You can explore the rendered REST API documentation for the details about all the URIs and their corresponding parameters supported by the REST API service engine. To access details about supported REST API without running a switch image, please refer to the following website for information:
> http://api.openswitch.net/rest/dist/index.html

## CLI ##
The feature is an alternative to CLI mechanism as a management interface. It has no CLIs of its own.

## Related features ##
Configuration daemon and API modules utilize configuration read and write capabilities provided by the feature in the form of Python libraries.

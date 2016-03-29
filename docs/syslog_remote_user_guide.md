# Remote syslog feature

## Contents
- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
	- [Setting up the basic configuration](#setting-up-the-basic-configuration)
	- [Verifying the configuration](#verifying-the-configuration)
	- [Troubleshooting the configuration](#troubleshooting-the-configuration)
		- [Condition](#condition)
		- [Cause](#cause)
		- [Remedy](#remedy)
- [CLI](#cli)

## Overview
Remote syslog feature enables switch to forward syslog messages to remote syslog server.


## How to use the feature

### Setting up the basic configuration
```
 logging <IPv4-address> | <IPv6-address> | <hostname> [udp [<port>] | tcp [<port>]] [severity <level>]
```

Example:
```
 switch(config)#logging 10.0.10.9 tcp 4242 severity err
```

### Verifying the configuration

 1. Run the remote syslog server at the specified address, transport and port.
 2. Run show running configuration in the switch to verify the configuration.
 3. Check the remote syslog server if it is receiving the messages as configured.


### Troubleshooting the configuration

#### Condition
Syslog messages are not received on the remote syslog server.

#### Cause
Following are the possible cause for this problem.

* Remote syslog server is not running.
* Remote syslog server is not reachable from the switch.
* Remote syslog server has improper configuration.

#### Remedy
* Confirm that the remote syslog server is running.
* Test the reachability of the remote syslog server from the switch.  Could use ping to check this.
* Make sure that the remote syslog server is configured to receive remote syslog messages.

## CLI
Click [here](documents/user/syslog_remote_cli) for CLI commands related to syslog remote configuration.

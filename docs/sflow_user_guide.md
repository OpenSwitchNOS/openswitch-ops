# sFlow

## Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Limitations](#limitations)
- [Defaults](#defaults)
- [Configuring sFlow](#configuring-sFlow)
	- [Minimum configuration](#minimum-configuration)
	- [Enabling sFlow](#enabling-sflow)
	- [Configuring collectors](#configuring-collectors)
	- [Configuring sampling rate](#configuring-sampling-rate)
	- [Configuring polling interval](#configuring-polling-interval)
	- [Configuring agent interface](#configuring-agent-interface)
	- [Configuring header size](#configuring-header-size)
	- [Configuring max datagram size](#configuring-max-datagram-size)
	- [Enable sFlow per interface](#enabling-sflow-per-interface)
- [Verifying the configuration](#verifying-the-configuration)
	- [Viewing sFlow global configuration](#viewing-sflow-global-configuration)
	- [Viewing sFlow interface configuration](#viewing-sflow-interface-configuration)
- [CLI](#cli)
- [Related features](#related-features)
- [Disclaimer](#disclaimer)

## Overview
sFlow is a standard that enables the network device to sample packets flowing through
the device and send the sampled packets to an external collector. The sFlow collector
analyzes the sampled packets to understand the network data flow pattern etc. The network
device also periodically sends interface statistics to the collector. sFlow agent in
OpenSwitch can sample traffic from all physical and bond interfaces in the system.

## Prerequisites
An sFlow collector is required to be present in the network that is reachable from
the network switch.

## Limitations
- A maximum of three sFlow collectors can be configured.
- Currently only default VRF is supported.

## Defaults
- sFlow is disabled by default.
- sFlow collector port is default to 6343.
- sFlow agent interface address family is default to IPv4.
- sFlow sampling rate is default to 4096.
- sFlow polling interval is default to 30 seconds.
- sFlow header size is default to 128 bytes.
- sFlow max datagram size is default to 1400 bytes.

## Minimum configuration
The following needs to be set for sFlow to work.

- Atleast one sFlow collector.
- sFlow sampling rate.
- Enable sFlow.

Configure the terminal to change the CLI context to config context with the following commands:
```
switch# configure terminal
switch(config)#
```

### Enabling sFlow
Enable global sFlow with the following command:
```
switch(config)# sflow enable
```
sFlow is enabled on all the interfaces in the switch.

Disable global sFlow with the following command:
```
switch(config)# no sflow enable
```
sFlow is disabled on all the interfaces in the switch.

### Configuring collectors
Configure up to a maximum of three collectors with the following command:
```
switch(config)# sflow collector <IP> [port <port>] [vrf <vrf-name>]
```
- IP can be the IPv4 or IPv6 address of the collector.
- port can be any valid UDP port that the collector is listening on. Default is 6343.
- vrf-name can be any of the configured VRFs in the system. Default is vrf_default.

Unconfiguring a configured collector can be done with the command:
```
switch(config)# no sflow collector <IP> [port <port>] [vrf <vrf-name>]
```

### Configuring sampling rate
sFlow global sampling rate can be configured using the command:
```
switch(config)# sflow sampling <rate>
```
- rate at which packets should be sampled and sent to collector. Default is 4096.
  For example `sflow sampling 1024` means one in 1024 packets will be
  sampled from all the interfaces in the switch.

Unconfiguring the sampling rate can done with the command:
```
switch(config)# no sflow sampling <rate> [<interface-speed>]
```

### Configuring polling interval
sFlow interface counter statistics are periodically send to the collector. The interval
can be configured with the following command:
```
switch(config)# sflow polling <interval>
```
- interval is in seconds and the default is 30.

sFlow polling interval is unconfigured using:
```
switch(config)# no sflow polling <interval>
```

### Configuring agent interface
sFlow agent interface is configured with the command:
```
switch(config)# sflow agent-interface <ifname> [ipv4|ipv6]
```
- ifname is the name of the interface whose IP address will be used as the agent
  IP in the sFlow datagrams. If not specified, system will pick the IP address from one
  of the interfaces in the switch in a priority order (TBD). By default the IPv4 address
  of the agent-interface is used, but can be changed by specifying ipv6 or ipv4.

### Configuring header size
sFlow header size is configured with the command:
```
switch(config)# sflow header-size <size>
```
- size is the number of bytes of a sampled packet to send to the collector.
  Default is 128 bytes and the range can be from 64 to 256 bytes.

sFlow header size can be unconfigured with:
```
switch(config)# no sflow header-size <size>
```

### Configuring max datagram size
sFlow max datagram size can be configured with:
```
switch(config)# sflow max-datagram-size <size>
```
- size is the maximum number of bytes that will be sent in one sFlow UDP datagram.
  Default is 1400 bytes.

sFlow max datagram size can be unconfigured with:
```
switch(config)# no sflow max-datagram-size <size>
```

### Enable sFlow per interface
Configure the terminal to change the CLI context to the interface config context
with the following commands:
```
switch(config)# interface <interface-name>
```
Enable sFlow on the interface by:
```
switch(config-if)# sflow enable
```

Disable sFlow on the interface by:
```
switch(config-if)# no sflow enable
```

## Verifying the configuration
The current sFlow configuration can be viewed from the main CLI context.
### Viewing sFlow global configuration
The global sFlow configuration can be viewed using:
```
switch# show sflow
```
This displays the current sFlow configuration and the sample statistics.

### Viewing sFlow interface configuration
sFlow configuration on an interface can be viewed using:
```
switch# show sflow <interface-name>
```
This displays the current sFlow configuration and the sample statistics on that interface.


## CLI

Click [here](/documents/user/sflow_cli) for the CLI commands related to the sFlow feature.

## Related features
None

## Disclaimer
sFlow datagrams are not encrypted and may expose sensitive information contained in the sFlow sample.

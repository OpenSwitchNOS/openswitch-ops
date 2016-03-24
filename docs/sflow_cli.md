sFlow Commands
==============
## Contents
- [sFlow Configuration Commands](#sflow-configuration-commands)
    - [Enable sFlow](#enable-sflow-globally)
    - [Disable sFlow](#disable-sflow-globally)
    - [Set sFlow sampling rate](#set-sflow-sampling-rate)
    - [Remove sFlow sampling rate](#remove-sflow-sampling-rate)
    - [Set sFlow polling interval](#set-sflow-polling-interval)
    - [Remove sFlow polling interval](#remove-sflow-polling-interval)
    - [Set sFlow collector ip address](#set-sflow-collector-ip-address)
    - [Remove sFlow collector ip address](#remove-sflow-collector-ip-address)
    - [Set sFlow agent interface name and family](#set-sflow-agent-interface-name-and-family)
    - [Remove sFlow agent interface name and family](#remove-sflow-agent-interface-name-and-family)
    - [Set sFlow header size](#set-sflow-header-size)
    - [Remove sFlow header size](#remove-sflow-header-size)
    - [Set sFlow max datagram size](#set-sflow-max-datagram-size)
    - [Remove sFlow max datagram size](#remove-sflow-max-datagram-size)
    - [Enable sFlow on the interface](#enable-sflow-on-the-interface)
    - [Disable sFlow on the interface](#disable-sflow-on-the-interface)

- [sFlow Show Commands](#sflow-show-commands-)
    - [Show sFlow configuration](#show-sflow-configuration)
    - [Show sFlow configuration(interface)](#show-sflow-configuration-interface)

## sFlow configuration commands

### Global context commands
#### Enable sFlow globally
#### Syntax
`sflow enable`
#### Description
This command enables sflow globally. By default sflow is disabled.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# sflow enable
```
#### Disable sFlow globally
#### Syntax
`no sflow enable`
#### Description
This command disables sflow globally. By default sflow is disabled.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no sflow enable
```
### Set sFlow sampling rate
#### Syntax
`sflow sampling <rate>`
#### Description
This command sets a global sampling rate for sflow. The default sampling rate is 4096. One in 4096 packets are sampled.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *rate* | required | 1-1000000000 | Adds sampling rate |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# sflow sampling 1000
```
### Remove sFlow sampling rate
#### Syntax
`no sflow sampling`
#### Description
This command removes the current sampling rate for sflow and sets it back to default of 4096 globally. A sampling rate of 4096 means that one in 4096 packets are sampled.
#### Authority
All users.
#### Parameters
No Parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no sflow sampling
```
### Set sFlow polling interval
#### Syntax
`sflow polling <interval>`
#### Description
This command sets a polling interval. The default polling interval is 30 seconds. If the polling interval is zero, it means that polling is disabled.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interval* | required | 0-3600 | Adds interval for polling |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# sflow polling 10
```
### Remove sFlow polling interval
#### Syntax
`no sflow polling`
#### Description
This command removes a polling interval. Default polling interval is 30 seconds. If the polling interval is zero, it means that polling is disabled.
#### Authority
All users.
#### Parameters
No Parameters
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no sflow polling
```
### Set sFlow collector ip address
#### Syntax
`sflow collector <IP> [port <port>] [vrf <data/management>]`
#### Description
This command sets a collector IP (IPv4 or IPv6) and adds a port and a VRF as an option. The port defaults to 6343. VRF is the vrf on which collector can be reached. Default to data vrf. A maximum of three collectors can be configured. Supplies port address to reach the collector. Supplies the name of the VRF to reach collector.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *IP* | required | A.B.C.D / X:X::X:X | Collector IPv4 / IPv6 address |
| *port* | optional | 0-65535 | Gives port to reach collector |
| *vrf* | optional | String | Adds name of VRF to reach collector |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# sflow collector 10.0.0.1 port 6343 vrf vrf1
```
### Remove sFlow collector ip address
#### Syntax
`no sflow collector <IP> [port <port>] [vrf <data/management>]`
#### Description
This command removes a collector IP address (if present) that may be associated with a port and a VRF. Supplies port address to reach the collector. Supplies the name of the VRF to reach collector.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *IP* | required | A.B.C.D / X:X::X:X | Collector IPv4 / IPv6 address |
| *port* | optional | 0-65535 | Gives port to reach collector |
| *vrf* | optional | String | Adds name of VRF to reach collector |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no sflow collector 10.0.0.1 port 6343 vrf vrf2
```
### Set sFlow agent interface name and family
#### Syntax
`sflow agent-interface <interface-name> [<ipv4/ipv6>]`
#### Description
This command sets the name of the interface whose IP address is used as the agent IP in the sFlow datagrams.
If not specified, the system picks the IP address from one of the interfaces in a priority order (to be determined). It also sets the family type(IPv4 or IPv6) for the agent interface which is an optional parameter and set to IPv4 by default.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface-name* | required | System defined | Name of the interface. System defined. |
| *address-family* | optional | ipv4|ipv6 | IPv4 / IPv6 address family |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# sflow agent-interface 1 ipv4
```
### Remove sFlow agent interface name and family
#### Syntax
`no sflow agent-interface`
#### Description
This command removes an agent-interface and family if set. If not specified, system will pick the IP address from one of the interfaces in a priority order (to be determined). The agent address family defaults to IPv4.
#### Authority
All users.
#### Parameters
No Parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no sflow agent-interface
```

### Set sFlow header size
#### Syntax
`sflow header-size <size>`
#### Description
This command sets the header size. The default value for this is 128.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *size* | required | 64-256 | Sets size of header |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# sflow header-size 64
```
### Remove sFlow header size
#### Syntax
`no sflow header-size`
#### Description
This command removes the set header size and sets it back to the default of 128.
#### Authority
All users.
#### Parameters
No Parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no sflow header-size
```
### Set sFlow max datagram size
#### Syntax
`sflow max-datagram-size <size>`
#### Description
This command sets the maximum number of bytes that are send in one sFlow datagram. The default value is 1400 bytes.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *size* | required | 1-9000 | Sets max size of datagram |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# sflow max-datagram-size 1000
```
### Remove sFlow max datagram size
#### Syntax
`no sflow max-datagram-size`
#### Description
This command removes the set number of bytes that are send in one sFlow datagram. This command resets the number of bytes to the default of 1400.
#### Authority
All users.
#### Parameters
No Parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no sflow max-datagram-size
```
### Interface context commands
#### Enable sFlow on the interface
#### Syntax
`sflow enable`
#### Description
This command enables sFlow on the interface. It is used in interface context.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# sflow enable
```
#### Disable sFlow on the interface
#### Syntax
`no sflow enable`
#### Description
This command disables sFlow on the interface. It is used in interface context.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no sflow enable
```

## sFlow display commands
### Show sFlow configuration
#### Syntax
`show sflow`
#### Description
This command displays sflow configuration and sample statistics.
#### Authority
All users.
#### Parameters
no parameters
#### Examples
```
ops-as5712# show sflow
 sFlow Configuration
 -----------------------------------------
 sFlow                         enabled
 Collector IP/Port/Vrf         10.0.0.1/6343/vrf_default
                               10.0.0.2/6343/vrf_default
 Agent Interface               1
 Agent Address Family          ipv4
 Sampling Rate                 1024
 Polling Interval              30
 Header Size                   128
 Max Datagram Size             1400
 Number of Samples             0
 ```

### Show sFlow configuration interface
#### Syntax
`show sflow <interface>`
#### Description
This command displays sflow configuration and sample statistics for an interface.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface* | required | System defined | Name of the interface. System defined. |
#### Examples
```
ops-as5712# show sflow 1
 sFlow configuration - Interface 1
 -----------------------------------------
 sFlow                         enabled
 Sampling Rate                 1024
 Number of Samples             0

```

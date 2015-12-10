SFLOW Commands
======
## Contents
- [SFLOW Configuration Commands](#sflow-configuration-commands)
    - [Enable SFLOW](#enable-sflow)
    - [Disable SFLOW](#disable-sflow)
    - [Set SFLOW sampling rate](#set-sflow-sampling)
    - [Remove SFLOW sampling rate](#remove-sflow-sampling)
    - [Set SFLOW polling interval](#set-sflow-polling-interval)
    - [Remove SFLOW polling interval](#remove-sflow-polling-interval)
    - [Set SFLOW collector ip address](#set-sflow-collector-ip-address)
    - [Remove SFLOW collector ip address](#remove-sflow-collector-ip-address)
    - [Set SFLOW agent interface name](#set-sflow-agent-interface-name)
    - [Remove SFLOW agent interface name](#remove-sflow-agent-interface-name)
    - [Set SFLOW agent address family](#set-sflow-agent-address-family)
    - [Remove SFLOW agent address family](#remove-sflow-agent-address-family)
    - [Set SFLOW header size](#set-sflow-header-size)
    - [Remove SFLOW header size](#remove-sflow-header-size)
    - [Set SFLOW max datagram size](#set-sflow-max-datagram-size)
    - [Remove SFLOW max datagram size](#remove-sflow-max-datagram-size)
    - [Enable SFLOW on the interface](#enable-sflow-on-the-interface)
    - [Disable SFLOW on the interface](#disable-sflow-on-the-interface)

- [SFLOW Show Commands](#sflow-show-commands-)
    - [Show SFLOW configuration](#show-sflow-configuration)
    - [Show SFLOW configuration(interface)](#show-sflow-configuration-interface)

## SFLOW Configuration Commands

### Global context commands
#### Enable SFLOW globally
#### Syntax
sflow enable
#### Description
This command enables sflow globally.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# sflow enable
```
#### Disable SFLOW globally
#### Syntax
no sflow enable
#### Description
This command disables sflow globally.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no sflow enable
```
### Set SFLOW sampling rate
#### Syntax
sflow sampling <rate>
#### Description
This command sets a global sampling rate for sflow. The default sampling rate is 1024.
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
### Remove SFLOW sampling rate
#### Syntax
no sflow sampling
#### Description
This command removes the current sampling rate for sflow and sets it back to default of 1024 globally.
#### Authority
All users.
#### Parameters
No Parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no sflow sampling
```
### Set SFLOW polling interval
#### Syntax
sflow polling <interval>
#### Description
This command sets a polling interval. Default polling interval is 30 seconds.
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
### Remove SFLOW polling interval
#### Syntax
no sflow polling <interval>
#### Description
This command removes a polling interval. Default polling interval is 30 seconds.
#### Authority
All users.
#### Parameters
No Parameters
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no sflow polling
```
### Set SFLOW collector ip address
#### Syntax
sflow collector <IP> [port <port>] [vrf <data/management>]
#### Description
This command sets a collector IP (IPv4 or IPv6) adding a port and vrf as an option.Port defaults to 6343.VRF is the vrf on which collector can be reached. Default to data vrf.A maximum of three collectors can be configured.
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
### Remove SFLOW collector ip address
#### Syntax
no sflow collector <IP> [port <port>] [vrf <data/management>]
#### Description
This command removes a collector IP address if present which may be associated with a port and vrf.
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
ops-as5712(config)# no sflow collector 10.0.0.1 port 6343 vrf vrf1
```
### Set SFLOW agent interface name
#### Syntax
sflow agent-interface <interface-name>
#### Description
This command sets the name of the interface whose IP address will be used as the agent IP in the sflow datagrams. If not specified, system will pick the IP address from one of the interfaces in a priority order (to be determined).
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface-name* | required | System defined | Name of the interface. System defined. |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# sflow agent-interface 1
```
### Remove SFLOW agent interface name
#### Syntax
no sflow agent-interface
#### Description
This command removes an agent-interface if set.If not specified, system will pick the IP address from one of the interfaces in a priority order (to be determined).
#### Authority
All users.
#### Parameters
No Parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no sflow agent-interface
```
### Set SFLOW agent address family
#### Syntax
sflow agent-address-family <ipv4/ipv6>
#### Description
This command uses the IPv4/IPv6 address family from the sflow agent-interface.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *IP* | required | IPv4, IPv6 | IPv4 / IPv6 address family|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# sflow agent-address-family ipv4
```
### Remove SFLOW agent address family
#### Syntax
no sflow agent-address-family <ipv4/ipv6>
#### Description
This command removes an IPv4/IPv6 address family from the sflow agent-interface.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *IP* | required | IPv4, IPv6 | IPv4 / IPv6 address family |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no sflow agent-address-family ipv4
```
### Set SFLOW header size
#### Syntax
sflow header-size <size>
#### Description
This command sets the header size.The default value for this is 128.
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
### Remove SFLOW header size
#### Syntax
no sflow header-size
#### Description
This command removes the set header size and sets it back to default of 128.
#### Authority
All users.
#### Parameters
No Parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no sflow header-size
```
### Set SFLOW max datagram size
#### Syntax
sflow max-datagram-size <size>
#### Description
This command sets the maximum number of bytes that will be send in one sflow datagram.Default value is 1400 bytes.
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
### Remove SFLOW max datagram size
#### Syntax
no sflow max-datagram-size
#### Description
This command removes the set number of bytes to be send in one sflow datagram. Resets it to default of 1400.
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
#### Enable SFLOW on the interface
#### Syntax
sflow enable
#### Description
This command enables sflow on the interface. Its to be used in interface context.
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
#### Disable SFLOW on the interface
#### Syntax
no sflow enable
#### Description
This command disables sflow on the interface. Its to be used in interface context.
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

## SFLOW display commands
### Show SFLOW configuration
#### Syntax
show sflow
#### Description
This command displays sflow configuration and sample statistics.
#### Authority
All users.
#### Parameters
no parameters
#### Examples
```
ops-as5712# show sflow
 SFLOW configuration
 --------------------------------------------------------------------
 sflow                                  enabled
 collector_ip : port : vrf              10.0.0.1 : 6343 : vrf_default
                                        10.0.0.2 : 6343 : vrf_default
 agent_interface                        1
 agent_address_family                   IPv4
 sampling_rate : interface_speed        1024 : 10G
                                        2048 : 100G
 polling interval                       30
 header_size                            64
 max_datagram_size                      1400
 <sample-stats-TBD>
 ```

### Show SFLOW configuration interface
#### Syntax
show sflow <interface>
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
 SFLOW configuration : interface 1
 --------------------------------------------------------------------
 sflow                                  enabled
 sampling_rate                          1024
 <interface-sample-stats-TBD>
```

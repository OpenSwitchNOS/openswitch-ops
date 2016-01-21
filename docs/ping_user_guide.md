# Ping

## Contents
- [Overview](#overview)
	- [Syntax](#syntax)
	- [Explanation of parameters](#explanation-of-parameters)
- [How to use the feature](#how-to-use-the-feature)
	- [Ping examples for IPv4 addresses](#ping-examples-for-ipv4-addresses)
	- [Ping6 examples for IPv6 addresses](#ping6-examples-for-ipv6-addresses)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
The ping (Packet InterNet Groper) command is a very common method for troubleshooting the accessibility of devices.
It uses Internet Control Message Protocol (ICMP) echo requests and ICMP echo replies to determine if another device is alive.
It also measures the amount of time it takes to receive a reply from the specified destination.
The ping command is mostly used to verify connectivity between your switch and a host or port. The reply packet tells you if the host received the ping and the amount of time it took to return the packet.

### Syntax
`ping <ipv4-address | hostname> [repetitions <1-10000>] [timeout <1-60>] [interval <1-60>] [datagram-size <100-65399>] [data-fill <WORD>][ip-option (include-timestamp |include-timestamp-and-address |record-route)][tos <0-255>]`

`ping6 <ipv6-address | hostname> [repetitions <1-10000>] [interval <1-60>] [datagram-size <100-65468>] [data-fill <WORD>]`

### Explanation of parameters

* Ipv4-address - Target IPv4 address of the destination node being pinged.

* Hostname - Hostname of the destination node being pinged.

* Repetitions <1-10000> - Number of ping packets sent to the destination address. The default value is 5.

* Timeout <1-60> - Timeout interval in seconds, the ECHO REPLY must be received before this time interval expires for the Ping to be successful. The default value is 2 seconds.

* Interval <1-60> - Interval seconds between sending each packet. The default value is 1 second.

* Datagram-size - Size of packet sent to the destination. The default value is 100 bytes.

* Data-fill -  Hexadecimal pattern to be filled in the packet. Only first 16 characters are considered for data-fill.

* Ip-options - This prompt offers more selection of any one option from the list below.

 *   Include-timestamp - Timestamp option is used to measure roundtrip time to particular hosts.
 *   Include-timestamp-and-address - Displays roundtrip time to particular hosts as well as address.
 *   Record-route - Displays the address(es) of the hops the packet goes through.

*   TOS <0-255> - Specifies the Type of Service (TOS). The requested TOS is placed in each probe. It is the Internet service quality selection.

## How to use the feature

### Ping examples for IPv4 addresses
#### Ping IPv4-address
##### Success case
    Send an IP Ping request to the device that has IP address 10.10.10.1
    switch# ping 10.0.3.1
    PING 10.0.3.1 (10.0.3.1): 100 data bytes
    108 bytes from 10.0.3.1: icmp_seq=0 ttl=64 time=0.063 ms
    108 bytes from 10.0.3.1: icmp_seq=1 ttl=64 time=0.023 ms
    108 bytes from 10.0.3.1: icmp_seq=2 ttl=64 time=0.050 ms
    108 bytes from 10.0.3.1: icmp_seq=3 ttl=64 time=0.044 ms
    108 bytes from 10.0.3.1: icmp_seq=4 ttl=64 time=0.056 ms
    --- 10.0.3.1 ping statistics ---
    5 packets transmitted, 5 packets received, 0% packet loss
    round-trip min/avg/max/stddev = 0.023/0.047/0.063/0.000 ms

##### Failure case
    switch# ping 1.1.1.1
    ping: sending packet: Network is unreachable
    PING 1.1.1.1 (1.1.1.1): 100 data bytes

#### Hostname
    ping hostname
    Domain name of the host to ping.

#### Repetitions
    ping <ipv4-address | hostname> repetitions <1-10000>
    Number of packets to send <1-10000>.
    Range: < 1 to 10000 >

#### Timeout
    ping <ipv4-address | hostname> timeout <1-60>
    Ping timeout in seconds <1-60>.
    Range: <1 to 60>

#### Interval
    ping <ipv4-address | hostname> interval <1-60>
    Seconds between sending each packet <1-60>.
    Range: <1 to 60>

#### Data-fill
    ping <ipv4-address | hostname> data-fill WORD
    Ping data fill string, example 'ab'
    Maximum pattern length is 16 hexadecimal characters.

#### Datagram-size
    ping <ipv4-address | hostname> datagram-size <100-65399>
    Range: <100 to 65399>

### Ping6 examples for IPv6 addresses
#### Ping IPv6-address
##### Success case
    Send an IPv6 Ping request to the device that has IPv6 address 2030::1(Success case)
    switch# ping6 2030::1
    PING 2030::1 (2030::1): 100 data bytes
    108 bytes from switch: icmp_seq=0 ttl=64 time=0.091 ms
    108 bytes from switch: icmp_seq=1 ttl=64 time=0.073 ms
    108 bytes from switch: icmp_seq=2 ttl=64 time=0.089 ms
    108 bytes from switch: icmp_seq=3 ttl=64 time=0.068 ms
    108 bytes from switch: icmp_seq=4 ttl=64 time=0.089 ms
    --- 2030::1 ping statistics ---
    5 packets transmitted, 5 packets received, 0% packet loss
    round-trip min/avg/max/stddev = 0.068/0.082/0.091/0.000 ms

##### Failure case
    switch# ping6 3030::1
    ping6: sending packet: Network is unreachable
    PING 3030::1 (3030::1): 100 data bytes

#### Hostname
    ping6 hostname
    Domain name of the host to ping.

#### Repetitions
    ping6 <ipv6-address | hostname> repetitions <1-10000>
    Number of packets to send <1-10000>.
    Range: <1 to 10000>

#### Interval
    ping6 <ipv6-address | hostname> interval <1-60>
    Seconds between sending each packet <1-60>.
    Range: <1 to 60>

#### Data-fill
    ping6 <ipv6-address | hostname> data-fill WORD
    Ping data fill string, example 'ab'
    Maximum pattern length is 16 hexadecimal characters.

#### Datagram-size
    ping6 <ipv6-address | hostname> datagram-size <100-65468>
    Range: <100 to 65468>
## CLI
Click [here](http://www.openswitch.net/documents/user/ping_cli) for more information about the CLI commands related to the ping feature.

## Related features
* [Traceroute User Guide](http://www.openswitch.net/documents/user/traceroute_user_guide)
* [Traceroute CLI Guide](http://www.openswitch.net/documents/user/traceroute_cli)

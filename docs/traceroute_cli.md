Traceroute Utility
======
## Contents

- [Traceroute Options](##traceroute-options)
	- [IPv4 address](#ipv4-address)
	- [Hostname](#hostname)
	- [Set Destination port](#set-destination-port)
	- [Set Maximum TTL](#set-maximum-ttl)
	- [Set Minimum TTL](#set-minimum-ttl)
    - [Set Probes](#set-probes)
	- [Set Timeout](#set-timeout)
	- [Set Ip-option Loose source route](#set-ip-option-loose-source-route)

- [Traceroute6 Options](##traceroute6-options)
	- [IPv6 address](#ipv6-address)
	- [Hostname](#hostname)
	- [Set Destination port](#set-destination-port)
	- [Set Maximum TTL](#set-maximum-ttl)
    - [Set Probes](#set-probes)
	- [Set Timeout](#set-timeout)

##traceroute options
### IPv4 address
#### Syntax
`traceroute <IPv4-address>`
#### Description
This command is used to traceroute the specified IPv4 address.
#### Authority
Root user.
#### Parameters
| Parameter | Syntax | Description
| *IPv4-address* | A.B.C.D | IPv4 address to traceroute.
#### Examples
```
switch# traceroute 10.168.1.146
traceroute to 10.168.1.146 (10.168.1.146) , 30 hops max
1 10.57.191.129 2 ms 3 ms 3 ms
2 10.57.232.1 4 ms 2 ms 3 ms
3 10.168.1.146 4 ms 3 ms 3 ms
```

### Hostname
#### Syntax
`traceroute <hostname>`
#### Description
This command is used to traceroute the specified Hostname.
#### Authority
Root user.
#### Parameters
| Parameter | Syntax | Description
| *hostname* | string | Hostname to traceroute. Length must be less than 256 characters.
#### Examples
```
switch# traceroute localhost
traceroute to localhost (127.0.0.1), 30 hops max

  1   127.0.0.1  0.018ms  0.006ms  0.003ms
```

### Set Maximum TTL
#### Syntax
`traceroute ( <IPv4-address> | <hostname> ) maxttl <number>`
#### Description
This command sets the Minimum number of hops used in outgoing probe packets. The default value is 30
#### Authority
Root user.
#### Parameters
| Parameter | Syntax | Description
| *maxttl* | <1-255> | Select Maximum number of hops used in outgoing probe packets between 1 to 255.
#### Examples
```
switch# switch# traceroute 10.168.1.146 maxttl 30
traceroute to 10.168.1.146 (10.168.1.146) , 30 hops max
1 10.57.191.129 2 ms 3 ms 3 ms
2 10.57.232.1 4 ms 2 ms 3 ms
3 10.168.1.146 4 ms 3 ms 3 ms
```

### Set Minimum TTL
#### Syntax
`traceroute ( <IPv4-address> | <hostname> ) minttl <number>`
#### Description
This command sets the Minimum number of hops used in outgoing probe packets. The default value is 1
#### Authority
Root user.
#### Parameters
| Parameter | Syntax | Description
| *minttl* | <1-255> | Select Minimum number of hops used in outgoing probe packets between 1 to 255.
#### Examples
```
switch# traceroute 10.168.1.146 minttl 1
traceroute to 10.168.1.146 (10.168.1.146) , 30 hops max
1 10.57.191.129 2 ms 3 ms 3 ms
2 10.57.232.1 4 ms 2 ms 3 ms
3 10.168.1.146 4 ms 3 ms 3 ms
```

### Set Destination port
#### Syntax
`traceroute ( <IPv4-address> | <hostname> ) dstportdstport <number>`
#### Description
This command sets the destination port. The default value is dstport 33434
#### Authority
Root user.
#### Parameters
| Parameter | Syntax | Description
| *dstport* | <1-34000> | Select the destination port number.
#### Examples
```
switch# traceroute 10.168.1.146 dstport 33434
traceroute to 10.168.1.146 (10.168.1.146) , 30 hops max
1 10.57.191.129 2 ms 3 ms 3 ms
2 10.57.232.1 4 ms 2 ms 3 ms
3 10.168.1.146 4 ms 3 ms 3 ms
```

### Set probes
#### Syntax
`traceroute ( <IPv4-address> | <hostname> ) probes <number>`
#### Description
This command sets Number of probe queries to send out for each hop. The default value is 3
#### Authority
Root user.
#### Parameters
| Parameter | Syntax | Description
| *probes* | <1-5> | Select Number of probe queries to send out for each hop between 1 to 5.
#### Examples
```
switch# traceroute 10.168.1.146 probes 3
traceroute to 10.168.1.146 (10.168.1.146) , 30 hops max
1 10.57.191.129 2 ms 3 ms 3 ms
2 10.57.232.1 4 ms 2 ms 3 ms
3 10.168.1.146 4 ms 3 ms 3 ms
```

### Set Timeout
#### Syntax
`traceroute ( <IPv4-address> | <hostname> ) timeout <time>`
#### Description
This command sets the Time in seconds to wait for a response to a probe. The default value is 3 seconds
#### Authority
Root user.
#### Parameters
| Parameter | Syntax | Description
| *timeout* | <1-120> | Select Time in seconds to wait for a response to a probe between 1 and 120.
#### Examples
```
switch# traceroute 10.168.1.146 timeout 5
traceroute to 10.168.1.146 (10.168.1.146) , 30 hops max
1 10.57.191.129 2 ms 3 ms 3 ms
2 10.57.232.1 4 ms 2 ms 3 ms
3 10.168.1.146 4 ms 3 ms 3 ms
```

### Set Ip-option Loose source route
#### Syntax
`traceroute ( <IPv4-address> | <hostname> ) ip-option loosesourceroute <IPv4-Address> `
#### Description
This command is used to set the the intermediate loose source route addresse.
#### Authority
Root user.
#### Parameters
No parameters.
#### Examples
```
switch# traceroute 10.168.1.146 ip-option loosesourceroute10.57.191.1291.1.1.5
traceroute to 10.168.1.146 (10.168.1.146) , 30 hops max
1 10.57.191.129 2 ms 3 ms 3 ms
2 10.57.232.1 4 ms 2 ms 3 ms
3 10.168.1.146 4 ms 3 ms 3 ms
 ```

##traceroute6 options :

### IPv6 address
#### Syntax
`traceroute6 <IPv6-address>`
#### Description
This command is used to traceroute the specified IPv6 address.
#### Authority
Root user.
#### Parameters
| Parameter | Syntax | Description
| *IPv6-address* | X:X::X:X | IPv6 address to traceroute6.
#### Examples
```
switch# traceroute6 0:0::0:1
traceroute to 0:0::0:1 (::1) from ::1, 30 hops max, 24 byte packets
 1  localhost (::1)  0.117 ms  0.032 ms  0.021 ms
```

### Hostname
#### Syntax
`traceroute6 <hostname>`
#### Description
This command is used to traceroute the specified Hostname.
#### Authority
Root user.
#### Parameters
| Parameter | Syntax | Description
| *hostname* | string | Hostname to traceroute. Length must be less than 256 characters.
#### Examples
```
switch# traceroute6 localhost
traceroute to localhost (::1) from ::1, 30 hops max, 24 byte packets
 1  localhost (::1)  0.189 ms  0.089 ms  0.025 ms
```

### Set Maximum TTL
#### Syntax
`traceroute6 ( <IPv6-address> | <hostname> ) maxttl <number>`
#### Description
This command sets the Minimum number of hops used in outgoing probe packets. The default value is 30
#### Authority
Root user.
#### Parameters
| Parameter | Syntax | Description
| *maxttl* | <1-255> | Select Maximum number of hops used in outgoing probe packets between 1 to 255.
#### Examples
```
switch# traceroute6 0:0::0:1 maxttl 30
traceroute to 0:0::0:1 (::1) from ::1, 30 hops max, 24 byte packets
 1  localhost (::1)  0.117 ms  0.032 ms  0.021 ms
```

### Set Destination port
#### Syntax
`traceroute6 ( <IPv6-address> | <hostname> ) dstportdstport <number>`
#### Description
This command sets the destination port. The default value is dstport 33434.
#### Authority
Root user.
#### Parameters
| Parameter | Syntax | Description
| *dstport* | <1-34000> | Select the destination port number.
#### Examples
```
switch# traceroute6 0:0::0:1 dsrport 33434
traceroute to 0:0::0:1 (::1) from ::1, 30 hops max, 24 byte packets
 1  localhost (::1)  0.117 ms  0.032 ms  0.021 ms```
```

### Set probes
#### Syntax
`traceroute6 ( <IPv6-address> | <hostname> ) probes <number>`
#### Description
This command sets Number of probe queries to send out for each hop. The default value is 3
#### Authority
Root user.
#### Parameters
| Parameter | Syntax | Description
| *probes* | <1-5> | Select Number of probe queries to send out for each hop between 1 to 5.
#### Examples
```
switch# traceroute6 0:0::0:1 probes 3
traceroute to 0:0::0:1 (::1) from ::1, 30 hops max, 24 byte packets
 1  localhost (::1)  0.117 ms  0.032 ms  0.021 ms
```

### Set Timeout
#### Syntax
`traceroute6 ( <IPv6-address> | <hostname> ) timeout <time>`
#### Description
This command sets the Time in seconds to wait for a response to a probe. The default value is 3 seconds
#### Authority
Root user.
#### Parameters
| Parameter | Syntax | Description
| *timeout* | <1-120> | Select Time in seconds to wait for a response to a probe. between 1 and 120.
#### Examples
```
switch# traceroute6 0:0::0:1 timeout 3
traceroute to 0:0::0:1 (::1) from ::1, 30 hops max, 24 byte packets
 1  localhost (::1)  0.117 ms  0.032 ms  0.021 ms
```

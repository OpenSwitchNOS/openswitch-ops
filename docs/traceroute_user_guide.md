# Traceroute
======
##contents
   - [Overview](#overview)
   - [How to use the feature](#how-to-use-the-feature)
   - [Related features](#related-features)

##Overview

Traceroute is a computer network diagnostic tool for displaying the route (path), and measuring transit delays of packets
across an Internet Protocol (IP) network.
It sends a sequence of User Datagram Protocol (UDP) packets addressed to a destination host; ICMP Echo Request or TCP SYN packets can also be used.
The time-to-live (TTL) value, also known as hop limit, is used in determining the intermediate routers being traversed towards the destination.


###Syntax
`traceroute ( <IP-ADDR | hostname > ) [dstport <1-34000> ][ maxttl <1-255>][minttl <1-255>] [probes <1-5>][timeout <1-120>][ip-option loosesourceroute <IP-ADDR>]`

`traceroute6 <IP-ADDR | hostname > [dstport <1-34000> ][ maxttl <1-255>][probes <1-5>][timeout <1-120>]`

####Explanation of parameters

•	IP-ADDR - Network IP address of the device to which to send traceroute.

•	Hostname - Domain name of the device to which to send traceroute.

•	Maxttl <1-255> - Maximum number of hops used in outgoing probe packets. The default value is 30.

•	Minttl <1-255> - Minimum number of hops used in outgoing probe packets. The default value is 1.

•	Timeout <1-120> - Time (in seconds) to wait for a response to a probe. The default value is 3 seconds.

•	Probes <1-5> - Number of probe queries to send out for each hop. The default value is 3.

•	Ip-option - Tells traceroute to add an IP source routing option to the outgoing packet.

•	Loosesourceroute <IP-ADDR> - Tells the network to route the packet through the specified gateway.

##How to use the feature

###Examples

####Traceroute ip-address
    Send an IP traceroute UDP packets to the device that has IP address 10.168.1.146:
    switch# traceroute 10.168.1.146
    traceroute to 10.168.1.146 (10.168.1.146) , 30 hops max
    1 10.57.191.129 2 ms 3 ms 3 ms
    2 10.57.232.1 4 ms 2 ms 3 ms
    3 10.168.1.146 4 ms 3 ms 3 ms

####Hostname
    traceroute hostname
    Domain name of the host to traceroute.

####Destination port
    traceroute dstport <1-34000>.
    Destination port number.
    Range: <1 to 34000>

####Maximum TTL
    traceroute maxttl <1-255>
    Maximum number of hops used in outgoing probe packets.
    Range: <1 to 255>

####Minimum TTL
    traceroute minttl <1-255>
    Minimum number of hops used in outgoing probe packets.
    Range: <1 to 255>

####Timeout
    traceroute timeout <1-120>
    Time (in seconds) to wait for a response to a probe <1-120>.
    Range: < 1 to 120 >

####Probes
    traceroute probes <1-5>
    Number of probe queries to send out for each hop <1-5>.
    Range: < 1 to 120 >


## Related features
Ping

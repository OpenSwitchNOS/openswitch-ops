# Control Plane Policing

##Contents
   - [Overview](#overview)
   - [Monitoring control plane policing](#monitoring-control-plane-policing)

## Overview
Control plane policing (CoPP) in OpenSwitch is needed for protecting the CPU against DoS attacks and prioritizing traffic classes to CPU. In OpenSwitch, CoPP supports default packet classes which are rate limited and put in the respective queues as defined below.

```ditaa
For Broadcom based platforms:
+--------------+-----------+---------------------------------+
|  Priority    | CPU Queue | Description                     |
+--------------+-----------+---------------------------------+
| Critical     |    Q10    | xSTP                            |
+--------------+-----------+---------------------------------+
| Important    |    Q9     | OSPF,BGP                        |
+--------------+-----------+---------------------------------+
| LLDP/LACP    |    Q8     | LLDP, LACP                      |
+--------------+-----------+---------------------------------+
| MANAGEMENT   |    Q7     | Currently, inband management    |
|              |           | traffic is not supported.       |
+--------------+-----------+---------------------------------+
| Unknown IP   |    Q6     | Unknown destination IP/IPv6     |
+--------------+-----------+---------------------------------+
| SW-PATH      |    Q5     | Unicast ARP, Unicast ICMP,      |
|              |           | ICMP, ICMPv6, IP options        |
+--------------+-----------+---------------------------------+
| NORMAL       |    Q4     | Broadcast ARP, ICMP, DHCP,      |
|              |           | Broadcast/Multicast             |
+--------------+-----------+---------------------------------+
| sFlow        |    Q3     | Sampled sFlow traffic           |
+--------------+-----------+---------------------------------+
| Snooping     |    Q2     |                                 |
+--------------+-----------+---------------------------------+
| Default      |    Q1     | Unclasssified packets           |
+--------------+-----------+---------------------------------+
| ACL Logging  |    Q0     | ACL logging                     |
+--------------+-----------+---------------------------------+

+---------------+--------------------------------+---------+-----------------+
| Packet Class  |  Description                   |  Queue  | Rate Limit (PPS)|
+---------------+--------------------------------+---------------------------+
| ACL_LOGGING   |  ACL Logging                   |   Q0    |         5       |
+---------------+--------------------------------+---------+-----------------+
| ARP_BC        |  Broadcast ARP Packets         |   Q4    |      1000       |
+---------------+--------------------------------+---------+-----------------+
| ARP_UC        |  Unicast ARPs                  |   Q5    |      1000       |
+---------------+--------------------------------+---------+-----------------+
| BGP           |  BGP packets                   |   Q9    |      5000       |
+---------------+--------------------------------+---------+-----------------+
| DHCP          |  DHCP packets                  |   Q4    |       500       |
+---------------+--------------------------------+---------+-----------------+
| DHCPV6        |  IPv6 DHCP packets             |   Q4    |       500       |
+---------------+--------------------------------+---------+-----------------+
| ICMP_BC       |  IPv4 broadcast/multicast ICMP |   Q4    |      1000       |
|               |  packets                       |         |                 |
+---------------+--------------------------------+---------+-----------------+
| ICMP_UC       |  IPv4 unicast ICMP packets     |   Q5    |      1000       |
+---------------+--------------------------------+---------+-----------------+
| ICMPV6_MC     |  IPv6 multicast ICMP packets   |   Q4    |      1000       |
+---------------+--------------------------------+---------+-----------------+
| ICMPV6_UC     |  IPv6 unicast ICMP             |   Q5    |      1000       |
+---------------+--------------------------------+---------+-----------------+
| IPOPTIONV4    |  Packets with IPv4 options     |   Q5    |       250       |
+---------------+--------------------------------+---------+-----------------+
| IPOPTIONV6    |  Packets with IPv6 options     |   Q5    |       250       |
+---------------+--------------------------------+---------+-----------------+
| LACP          |  LACP packets                  |   Q8    |      1000       |
+---------------+--------------------------------+---------+-----------------+
| LLDP          |  LLDP packets                  |   Q8    |       500       |
+---------------+--------------------------------+---------+-----------------+
| OSPF_MC       |  Multicast OSPF packets        |   Q9    |      5000       |
+---------------+--------------------------------+---------+-----------------+
| OSPF_UC       |  Unicast OSPF packets          |   Q9    |      5000       |
+---------------+--------------------------------+---------+-----------------+
| sFlow         |  Sampled sFlow packets         |   Q3    |      5000       |
+---------------+--------------------------------+---------+-----------------+
| STP           |  STP packets                   |   Q10   |      1000       |
+---------------+--------------------------------+---------+-----------------+
|UNKNOWN_IP_DEST|  Unknown IPv4 or Ipv6          |   Q6    |      2500       |
|               |  destination/Glean packets     |         |                 |
+---------------+--------------------------------+---------+-----------------+
|UNCLASSIFIED   |  Unclassified packets          |   Q1    |      5000       |
+------------------------------------------------+---------+-----------------+

```

These defaults are programmed during switch initialization and are always enabled. Currently, provision to configure these classes is not present.

## Monitoring control plane policing

To monitor accepted/dropped packet stats for each of the CoPP packet classes, following CLIs are provided:

``` ditaa
switch# show copp statistics icmpv4-unicast
        Control Plane Packet: ICMPv4 UNICAST packets

          rate (pps):                  1000
          burst size (pkts):           1000
          local priority:                 5

          packets passed:                 7        bytes passed:              786
          packets dropped:                0        bytes dropped:               0

switch# show copp statistics
        Control Plane Packets Total Statistics

          total_packets_passed:        6967        total_bytes_passed:      650274
          total_packets_dropped:          0        total_bytes_dropped:          0


        Control Plane Packet: BGP packets

          rate (pps):                     0
          burst size (pkts):              0
          local_priority:                 0

          packets_passed:                 0        bytes_passed:                 0
          packets_dropped:                0        bytes_dropped:                0


        Control Plane Packet: LLDP packets

          rate (pps):                     0
          burst size (pkts):              0
          local_priority:                 0

          packets_passed:                 0        bytes_passed:                 0
          packets_dropped:                0        bytes_dropped:                0

          ...
```

This CLI can be used:
1) To monitor the traffic distribution to CPU.
2) To be able to identify potential DoS attacks.
3) To troubleshoot any packet losses seen in control plane due to packets dropped.

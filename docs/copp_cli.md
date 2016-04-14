# COPP

## Contents
- [Display commands](#display-commands)
        - [show copp statistics](#show-copp-statistics)

## Display commands

### show copp statistics

##### Syntax
Under privileged mode.

`show copp statistics [protocol-name]`

#### Description
Displays the control plane policed statistics for a particular protocol or for all protocols. The statistics displayed for all protocols also displays the total packets and bytes that were control plane policed.

#### Authority
Operator.

##### Parameters

| Parameter | Status   | Syntax         | Description                                                   |
|:-----------|:----------|:----------------:|:-----------------------------------------------------------------|
| **protocol-name** | Optional| Literal  | Select the required protocol for which copp statistcis need to be displayed. |

##### Example
```
switch# sh copp statistics acl-logging
        Control Plane Packet: ACL LOGGING packets

          rate (pps):                     0
          burst size (pkts):              0
          local_priority:                 0

          packets_passed:                 0        bytes_passed:                 0
          packets_dropped:                0        bytes_dropped:                0


switch# sh copp statistics
        Control Plane Packets Total Statistics

          total_packets_passed:           0        total_bytes_passed:           0
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

```

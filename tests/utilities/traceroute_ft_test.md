Traceroute Feature Test Cases
========

## Contents
   - [Verify the Traceroute between 2 switches configured with an IPv4 address](#verify-the-traceroute-between-2-switches-configured-with-an-ipv4-address)
   - [Verify the Traceroute between 2 switches configured with an IPv6 address](#verify-the-traceroute-between-2-switches-configured-with-an-ipv6-address)

## Verify the Traceroute between 2 switches configured with an IPv4 address
### Objective
Successfully traces the path between two switches.
### Requirements
The requirements for this test case are:
 - Docker version 1.7 or above.
 - Accton AS5712 switch docker instance.
 - A topology with a single link between two switches, switch 1 and switch 2 are configured with an IPv4 address.

### Setup
#### Topology diagram

```ditaa
     +----------------+                                        +--------------------+
     |                |                                        |                    |
     | AS5712 switch  |<-------------------------------------->|  AS5712 switch     |
     |                |int1                                int1|                    |
     |                |                                        |                    |
     +----------------+                                        +--------------------+
```

#### Test setup

### Test case 1.01
Use the Traceroute diagnostic tool to measure the transmit packet delays from switch1 to switch2.
### Description
Successfully traces the path from switch1 to switch2.
### Test result criteria
#### Test pass criteria
This test is effective if the transmit packet delays between switch1 to switch2 are measured successfully.
#### Test fail criteria
The trace does not reach the destination.

### Test case 1.02
Use the Traceroute diagnostic tool to measure the transmit packet delays from switch2 to switch1.
### Description
Successfully traces the path from switch2 to switch1.
### Test result criteria
#### Test pass criteria
This test is effective if if the transmit packet delays between switch2 to switch1 are measured successfully.
#### Test fail criteria
The trace does not reach the destination.

### Test case 1.03
Use the Traceroute diagnostic tool to measure the transmit packet delays from switch1 to switch2 with the maxttl parameter
### Description
Successfully traces the path from switch1 to switch2 with the maxttl parameter.
### Test result criteria
#### Test pass criteria
This test is effective if the transmit packet delays between switch1 to switch2 with the maxttl parameter are measured successfully.
#### Test fail criteria
The trace does not reach the destination.

### Test case 1.04
Use the Traceroute diagnostic tool to measure the transmit packet delays from switch1 to switch2 with the minttl parameter.
### Description
Successfully traces the path from switch1 to switch2 with the minttl.
### Test result criteria
#### Test pass criteria
This test is effective if the transmit packet delays between switch1 to switch2 with the minttl parameter are measured successfully.
#### Test fail criteria
The trace does not reach the destination.

### Test case 1.05
Use the Traceroute diagnostic tool to measure the transmit packet delays from switch1 to switch2 with the dstport parameter.
### Description
Successfully traces the path from switch1 to switch2 with the dstport.
### Test result criteria
#### Test pass criteria
This test is effective if the transmit packet delays between switch1 to switch2 with the dstport parameter are measured successfully.
#### Test fail criteria
The trace does not reach the destination.

### Test case 1.06
Use the Traceroute diagnostic tool to measure the transmit packet delays from switch1 to switch2 with the probes parameter.
### Description
Successfully traces the path from switch1 to switch2 with the probes parameter.
### Test result criteria
#### Test pass criteria
This test is effective if the transmit packet delays between switch1 to switch2 with the probes parameter are measured successfully.
#### Test fail criteria
The trace does not reach the destination.

### Test case 1.07
Use the Traceroute diagnostic tool to measure the transmit packet delays from switch1 to switch2 with the timeout parameter.
### Description
Successfully traces the path from switch1 to switch2 with the timeout parameter.
### Test result criteria
#### Test pass criteria
This test is effective if the transmit packet delays between switch1 to switch2 with the timeout parameter are measured successfully.
#### Test fail criteria
The trace does not reach the destination.

### Test case 1.08
Use the Traceroute diagnostic tool to measure the transmit packet delays from switch1 to switch2 with the ip-option loose route parameter.
### Description
Successfully traces the path from switch1 to switch2 with the ip-option loose route parameter.
### Test result criteria
#### Test pass criteria
This test is effective if the transmit packet delays between switch1 to switch2 with the ip-option loose route parameter are measured successfully.
#### Test fail criteria
The trace does not reach the destination.

## Verify the Traceroute between 2 switches configured with an IPv6 address
### Objective
To successfully trace the path between two switches.
### Requirements
The requirements for this test case are:
 - Docker version 1.7 or above.
 - Accton AS5712 switch docker instance.
 - A topology with a single link between two switches, switch 1 and switch 2 are configured with an IPv6 address.

### Setup
#### Topology diagram

```ditaa
     +----------------+                                        +--------------------+
     |                |                                        |                    |
     | AS5712 switch  |<-------------------------------------->|  AS5712 switch     |
     |                |int1                                int1|                    |
     |                |                                        |                    |
     +----------------+                                        +--------------------+
```

#### Test setup
### Test case 2.01
Use Traceroute6 to measure the transmit packet delays from switch1 to switch2.
### Description
To successfully trace the path from switch1 to switch2.
### Test result criteria
#### Test pass criteria
This test is effective if the transmit packet delays between switch1 to switch2 using Traceroute6 are measured successfully.
#### Test fail criteria
Traceroute6 does not reach the destination.

### Test case 2.02
Use Traceroute6 to measure the transmit packet delays from switch2 to switch1.
### Description
To successfully trace the path from switch2 to switch1.
### Test result criteria
#### Test pass criteria
This test is effective if the transmit packet delays between switch2 to switch1 using Traceroute6 are measured successfully.
#### Test fail criteria
Traceroute6 does not reach the destination.

### Test case 2.03
Use Traceroute6 to measure the transmit packet delays from switch1 to switch2 with the maxttl parameter.
### Description
To successfully trace the path from switch1 to switch2 with the maxttl parameter.
### Test result criteria
#### Test pass criteria
This test is effective if the transmit packet delays between switch1 to switch2 with the maxttl parameter using Traceroute6 are measured successfully.
#### Test fail criteria
Traceroute6 does not reach the destination.

### Test case 2.04
Use Traceroute6 to measure the transmit packet delays from switch1 to switch2 with the dstport parameter.
### Description
To successfully trace the path from switch1 to switch2 with the dstport parameter.
### Test result criteria
#### Test pass criteria
This test is effective if the transmit packet delays between switch1 to switch2 with the dstport parameter using Traceroute6 are measured successfully.
#### Test fail criteria
Traceroute6 does not reach the destination.

### Test case 2.05
Use Traceroute6 to measure the transmit packet delays from switch1 to switch2 with the probes parameter.
### Description
To successfully trace the path from switch1 to switch2 with the probes parameter.
### Test result criteria
#### Test pass criteria
This test is effective if the transmit packet delays between switch1 to switch2 with the probes parameter using Traceroute6 are measured successfully.
#### Test fail criteria
Traceroute6 does not reach the destination.

### Test case 2.06
Use Traceroute6 to measure the transmit packet delays from switch1 to switch2 with the timeout parameter.
### Description
To successfully trace the path from switch1 to switch2 with the timeout parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if the transmit packet delays between switch1 to switch2 with the timeout parameter using Traceroute6 are measured successfully.
Traceroute6 does not reach the destination.
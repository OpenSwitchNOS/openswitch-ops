Traceroute Feature Test Cases
========

## Contents
   - [Verify the Traceroute between 2 switches configured with an IPv4 address](#verify-the-traceroute-between-2-switches-configured-with-an-IPv4-address)
   - [Verify the Traceroute between 2 switches configured with an IPv6 address](#verify-the-traceroute-between-2-switches-configured-with-an-IPv6-address)

## Verify the Traceroute between 2 switches configured with an IPv4 address
### Objective
Traces the path between 2 switches is successfully.
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
Traceroute from switch1 to switch2.
### Description
Traces the path from switch1 to switch2 is successful.
### Test result criteria
#### Test pass criteria
This test is effective if traceroute from switch1 to switch2 is successful and reached the destination.
#### Test fail criteria
Traceroute does not reach the destination.

### Test case 1.02
Traceroute from switch2 to switch1.
### Description
Traces the path from switch1 to switch2 is successful.
### Test result criteria
#### Test pass criteria
This test is effective if traceroute from switch2 to switch1 is successful and reached the destination.
#### Test fail criteria
Traceroute does not reach the destination.

### Test case 1.03
Traceroute from switch1 to switch2 with the maxttl parameter.
### Description
Traces the path from switch1 to switch2 with the maxttl parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if traceroute from switch1 to switch2 with the maxttl parameter is successful and reached the destination.
#### Test fail criteria
Traceroute does not reach the destination.

### Test case 1.04
Traceroute from switch1 to switch2 with the minttl parameter.
### Description
Traces the path from switch1 to switch2 with the minttl parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if traceroute from switch1 to switch2 with the minttl parameter is successful and reached the destination.
#### Test fail criteria
Traceroute does not reach the destination.

### Test case 1.05
Traceroute from switch1 to switch2 with the dstport parameter.
### Description
Traces the path from switch1 to switch2 with the dstport parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if traceroute from switch1 to switch2 with the dstport parameter is successful and reached the destination.
#### Test fail criteria
Traceroute does not reach the destination.

### Test case 1.06
Traceroute from switch1 to switch2 with the probes parameter.
### Description
Traces the path from switch1 to switch2 with the probes parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if traceroute from switch1 to switch2 with the probes parameter is successful and reached the destination.
#### Test fail criteria
Traceroute does not reach the destination.

### Test case 1.07
Traceroute from switch1 to switch2 with the timeout parameter.
### Description
Traces the path from switch1 to switch2 with the timeout parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if traceroute from switch1 to switch2 with the timeout parameter is successful and reached the destination.
#### Test fail criteria
Traceroute does not reach the destination.

### Test case 1.08
Traceroute from switch1 to switch2 with the ip-option loose route.
### Description
Traces the path from switch1 to switch2 with the ip-option loose route is successful.
### Test result criteria
#### Test pass criteria
This test is effective if traceroute from switch1 to switch2 with the ip-option loose route is successful and reached the destination.
#### Test fail criteria
Traceroute does not reach the destination.

## Verify the Traceroute between 2 switches configured with an IPv6 address
### Objective
Traces the path between 2 switches is successfully.
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
Traceroute6 from switch1 to switch2.
### Description
Traces the path from switch1 to switch2 is successful.
### Test result criteria
#### Test pass criteria
This test is effective if traceroute6 from switch1 to switch2 is successful and reached the destination.
#### Test fail criteria
Traceroute6 does not reach the destination.

### Test case 2.02
Traceroute6 from switch2 to switch1.
### Description
Traces the path from switch1 to switch2 is successful.
### Test result criteria
#### Test pass criteria
This test is effective if traceroute6 from switch2 to switch1 is successful and reached the destination.
#### Test fail criteria
Traceroute6 does not reach the destination.

### Test case 2.03
Traceroute6 from switch1 to switch2 with the maxttl parameter.
### Description
Traces the path from switch1 to switch2 with the maxttl parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if traceroute6 from switch1 to switch2 with the maxttl parameter is successful and reached the destination.
#### Test fail criteria
Traceroute6 does not reach the destination.

### Test case 2.04
Traceroute6 from switch1 to switch2 with the dstport parameter.
### Description
Traces the path from switch1 to switch2 with the dstport parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if traceroute6 from switch1 to switch2 with the dstport parameter is successful and reached the destination.
#### Test fail criteria
Traceroute6 does not reach the destination.

### Test case 2.05
Traceroute6 from switch1 to switch2 with the probes parameter.
### Description
Traces the path from switch1 to switch2 with the probes parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if traceroute6 from switch1 to switch2 with the probes parameter is successful and reached the destination.
#### Test fail criteria
Traceroute6 does not reach the destination.

### Test case 2.06
Traceroute6 from switch1 to switch2 with the timeout parameter.
### Description
Traces the path from switch1 to switch2 with the timeout parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if traceroute6 from switch1 to switch2 with the timeout parameter is successful and reached the destination.
#### Test fail criteria
Traceroute6 does not reach the destination.
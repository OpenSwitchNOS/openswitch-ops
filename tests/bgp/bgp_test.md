BGP Test Cases
==============

[TOC]

##  Basic Route Advertisement ##
### Objective ###
The test case verifies BGP route advertisement by emulating two BGP peers and verifying the received route from the peer.
### Requirements ###

- Physical/Virtual Switches

### Setup ###
#### Topology Diagram ####

```ditta
    +----------------+         +----------------+
    |                |         |                |
    |                |         |                |
    |    Switch 1    +---------+    Switch 2    |
    |                |         |                |
    |                |         |                |
    +----------------+         +----------------+
```

#### Test Setup ####
**Switch 1** is configured with:

    !
    interface 1
        no shutdown
        ip address 9.0.0.1/8
    !
    router bgp 1
        bgp router-id 9.0.0.1
        network 11.0.0.0/8
        neighbor 9.0.0.2 remote-as 2

**Switch 2** is configured with:

    !
    interface 1
        no shutdown
        ip address 9.0.0.2/8
    !
    router bgp 2
        bgp router-id 9.0.0.2
        network 12.0.0.0/8
        neighbor 9.0.0.1 remote-as 1

### Description ###
1. Configure switches 1 and 2 with **9.0.0.1/8** and **9.0.0.2/8**, respectively, in **vtysh** with the following commands:

    ***Switch 1***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 9.0.0.1/8
    ```

    ***Switch 2***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 9.0.0.2/8
    ```

2. Verify BGP processes are running on the switches by verifying a non-null value after executing "pgrep -f bgpd" on the switches.
3. Apply BGP configurations in **vtysh** for each switch with the following commands:

    ***Switch 1***

    ```
    configure terminal
    router bgp 1
    bgp router-id 9.0.0.1
    network 11.0.0.0/8
    neighbor 9.0.0.2 remote-as 2
    ```

    ***Switch 2***

    ```
    configure terminal
    router bgp 2
    bgp router-id 9.0.0.2
    network 12.0.0.0/8
    neighbor 9.0.0.1 remote-as 1
    ```

4. Verify all BGP configurations by comparing the expected values against the output of **show running-config**.
5. Verify the network advertised from switch 2 is in the output of **show ip bgp** on switch 1.
6. Verify the network advertised from switch 1 is in the output of **show ip bgp** on switch 2.

### Test Result Criteria ###
#### Test Pass Criteria ####
The test case is considered passing if the advertised routes of each peer exists in the output of the **show ip bgp** command. The network and next hop must match the information as configured on the peer.

**Expected Switch 1 Routes**

```
Local router-id 9.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       0.0.0.0                  0      0  32768  i
*> 12.0.0.0/8       9.0.0.2                  0      0      0 2 i
```

**Expected Switch 2 Routes**

```
Local router-id 9.0.0.2
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       9.0.0.1                  0      0      0 1 i
*> 12.0.0.0/8       0.0.0.0                  0      0  32768  i
```

#### Test Fail Criteria ####
The test case is considered failing in the following cases:

- The advertised routes from the peers are not present in the output from the **show ip bgp** command and fails during verification.
- The BGP daemon is not running on at least one of the switches and fails during verification.
- The BGP configurations are not applied successfully and fails during verification.





##  Neighbor Password ##
### Objective ###
The test case verifies the **neighbor password** and **no neighbor password** commands by verifying the BGP connection state after setting an incorrect password, correct password, and removing the password.

### Requirements ###

- Physical/Virtual Switches

### Setup ###
#### Topology Diagram ####

```ditta
    +----------------+         +----------------+
    |                |         |                |
    |                |         |                |
    |    Switch 1    +---------+    Switch 2    |
    |                |         |                |
    |                |         |                |
    +----------------+         +----------------+
```

#### Test Setup ####
**Switch 1** is configured with:

    !
    interface 1
        no shutdown
        ip address 9.0.0.1/8
    !
    router bgp 1
        bgp router-id 9.0.0.1
        network 11.0.0.0/8
        neighbor 9.0.0.2 remote-as 2
        neighbor 9.0.0.2 password 1234

**Switch 2** is configured with:

    !
    interface 1
        no shutdown
        ip address 9.0.0.2/8
    !
    router bgp 2
        bgp router-id 9.0.0.2
        network 12.0.0.0/8
        neighbor 9.0.0.1 remote-as 1
        neighbor 9.0.0.1 password 1234

### Description ###
1. Configure switches 1 and 2 with **9.0.0.1/8** and **9.0.0.2/8**, respectively, in **vtysh** with the following commands:

    ***Switch 1***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 9.0.0.1/8
    ```

    ***Switch 2***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 9.0.0.2/8
    ```

2. Verify BGP processes are running on the switches by verifying a non-null value after executing "pgrep -f bgpd" on the switches.
3. Apply BGP configurations in **vtysh** for each switch with the following commands:

    ***Switch 1***

    ```
    configure terminal
    router bgp 1
    bgp router-id 9.0.0.1
    network 11.0.0.0/8
    neighbor 9.0.0.2 remote-as 2
    neighbor 9.0.0.2 password 1234
    ```

    ***Switch 2***

    ```
    configure terminal
    router bgp 2
    bgp router-id 9.0.0.2
    network 12.0.0.0/8
    neighbor 9.0.0.1 remote-as 1
    neighbor 9.0.0.1 password 1234
    ```

4. Verify the **neighbor password** configuration is applied succesfully by checking the route from switch 2 is received on switch 1 and the route from switch 1 is received on switch 2 via the **show ip bgp** command.
5. Apply an incorrect password of **12** on switch 1 by issuing the following commands in **vtysh**:

    **Switch 1**

    ```
    configure terminal
    router bgp 1
    neighbor 9.0.0.2 password 12
    ```

6. Verify the network advertised from switch 2 in the output of **show ip bgp** on switch 1 is no longer present.
7. Reconfigure the correct password **1234** to reestablish a connection for verification of the **no neighbor password** command:

    **Switch 1**

    ```
    configure terminal
    router bgp 1
    neighbor 9.0.0.2 password 1234
    ```

8. Verify the **neighbor password** configuration is applied succesfully by checking the route from switch 2 is received on switch 1 and the route from switch 1 is received on switch 2 via the **show ip bgp** command.
9. Apply the **no neighbor password** command on both switches:

    **Switch 1**

    ```
    configure terminal
    router bgp 1
    no neighbor 9.0.0.2 password
    ```

    **Switch 2**

    ```
    configure terminal
    router bgp 2
    no neighbor 9.0.0.1 password
    ```

10. Verify the connection is no longer established via the **show ip bgp** command. Switch 1 should not show a route from switch 2 and switch 2 should not show a route from switch 1.

### Test Result Criteria ###
#### Test Pass Criteria ####

**Matching Password Pass Criteria**

The test case is considered passing if the advertised routes of each peer exists in the output of the **show ip bgp** command after a matching password is configured on both switches. The network and next-hop, as returned from the **show ip bgp** command, must match the information as configured on the peer.

**Expected Switch 1 Routes**

```
Local router-id 9.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       0.0.0.0                  0      0  32768  i
*> 12.0.0.0/8       9.0.0.2                  0      0      0 2 i
```

**Expected Switch 2 Routes**

```
Local router-id 9.0.0.2
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       9.0.0.1                  0      0      0 1 i
*> 12.0.0.0/8       0.0.0.0                  0      0  32768  i
```

**Incorrect Password Pass Criteria**

The test case is considered passing if the advertised routes are no longer in the output of the **show ip bgp** command.

**Expected Switch 1 Routes**

```
Local router-id 9.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       0.0.0.0                  0      0  32768  i
```

**Expected Switch 2 Routes**

```
Local router-id 9.0.0.2
   Network          Next Hop            Metric LocPrf Weight Path
*> 12.0.0.0/8       0.0.0.0                  0      0  32768  i
```

**No Password Pass Criteria**

The test case is considered passing if the established connection is no longer connected and the routes are no longer in the output of the **show ip bgp** command.

#### Test Fail Criteria ####
The test case is considered failing in the following cases:

- The advertised routes from the peer are not present in the output from the **show ip bgp** command and fails during verification when the correct password is configured.
- The BGP daemon is not running on at least one of the switches and fails during verification.
- The advertised routes from the peer are still present in the output from the **show ip bgp** command after setting the incorrect password or when the password is removed on switch 1.





##  Neighbor Remove Private AS ##
### Objective ###
The test case verifies the **neighbor remove-private-AS** and **no remove-private-AS** commands by verifying the Autonomous System (AS) number of the route received.

### Requirements ###

- Physical/Virtual Switches

### Setup ###
#### Topology Diagram ####

```ditta
    +----------------+         +----------------+         +----------------+
    |                |         |                |         |                |
    |                |         |                |         |                |
    |    Switch 1    +---------+    Switch 2    +---------+    Switch 3    |
    |                |         |                |         |                |
    |                |         |                |         |                |
    +----------------+         +----------------+         +----------------+

```

#### Test Setup ####
**Switch 1** is configured with:

    !
    interface 1
        no shutdown
        ip address 9.0.0.1/8
    !
    router bgp 1
        bgp router-id 9.0.0.1
        network 11.0.0.0/8
        neighbor 9.0.0.2 remote-as 2

**Switch 2** is configured with:

    !
    interface 1
        no shutdown
        ip address 9.0.0.2/8
    interface 2
        no shutdown
        ip address 29.0.0.4/8
    !
    router bgp 2
        bgp router-id 9.0.0.2
        network 12.0.0.0/8
        neighbor 29.0.0.3 remote-as 65000
        neighbor 9.0.0.1 remote-as 1
        neighbor 9.0.0.1 remove-private-AS

**Switch 3** is configured with:

    !
    interface 1
        no shutdown
        ip address 29.0.0.3/8
    !
    router bgp 65000
        bgp router-id 29.0.0.3
        network 13.0.0.0/8
        neighbor 29.0.0.4 remote-as 2

### Description ###

The command **neighbor remove-private-AS** removes the AS number from the received routes as it advertises it to another peer. This test case removes the AS number (65000) from the route received from switch 3, which is advertised to switch 1. The test case verifies the AS number on switch 1 for the routes received from switch 2.

1. Configure interfaces and IP addresses for switches 1, 2, and 3 in **vtysh** with the following commands:

    ***Switch 1***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 9.0.0.1/8
    ```

    ***Switch 2***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 9.0.0.2/8
    interface 2
    no shutdown
    ip address 29.0.0.4/8
    ```

    ***Switch 3***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 29.0.0.3/8
    ```

2. Verify BGP processes are running on the switches by verifying a non-null value after executing "pgrep -f bgpd" on the switches.
3. Apply BGP configurations in **vtysh** for each switch with the following commands:

    ***Switch 1***

    ```
    configure terminal
    router bgp 1
    bgp router-id 9.0.0.1
    network 11.0.0.0/8
    neighbor 9.0.0.2 remote-as 2
    ```

    ***Switch 2***

    ```
    configure terminal
    router bgp 2
    bgp router-id 9.0.0.2
    network 12.0.0.0/8
    neighbor 29.0.0.3 remote-as 65000
    neighbor 9.0.0.1 remote-as 1
    neighbor 9.0.0.1 remove-private-AS
    ```

    ***Switch 3***

    ```
    configure terminal
    router bgp 65000
    bgp router-id 29.0.0.3
    network 13.0.0.0/8
    neighbor 29.0.0.4 remote-as 2
    ```

4. Verify the **neighbor remove-private-AS** configuration is applied succesfully by checking the routes from switch 2 is received on switch 1 sans the AS number 65000 for network 13.0.0.0 via the **show ip bgp** command.
5. Unconfigure the **remove-private-AS** on switch 2 by issuing the following commands in **vtysh**:

    **Switch 2**

    ```
    configure terminal
    router bgp 2
    no neighbor 9.0.0.1 remove-private-AS
    ```

6. Reconfigure the neighbor information of switch 2 on switch 1 to refresh the routes in **vtysh**:

    **Switch 1**

    ```
    configure terminal
    router bgp 1
    no neighbor 9.0.0.2
    neighbor 9.0.0.2 remote-as 2
    ```

7. Verify the **no neighbor remove-private-AS** configuration is applied succesfully by checking the routes from switch 2 is received on switch 1 including the AS number 65000 for network 13.0.0.0 via the **show ip bgp** command.

### Test Result Criteria ###
#### Test Pass Criteria ####

The test case is considered passing, for the **neighbor remove-private-AS** command, if the advertised route from switch 2 to switch 1 for network 13.0.0.0 of switch 3 is received and does not include AS number 65000 via the **show ip bgp**.

**Expected Switch 1 Routes**

```
Local router-id 9.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       0.0.0.0                  0      0  32768  i
*> 12.0.0.0/8       9.0.0.2                  0      0  32768 2 i
*> 13.0.0.0/8       9.0.0.2                  0      0  32768 2 i
```



The test case is considered passing, for the **no neighbor remove-private-AS** command, if the advertised route from switch 2 to switch 1 for network 13.0.0.0 of switch 3 is received and includes AS number 65000 via the **show ip bgp**.

**Expected Switch 1 Routes**

```
Local router-id 9.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       0.0.0.0                  0      0  32768  i
*  12.0.0.0/8       9.0.0.2                  0      0      0 2 i
*  13.0.0.0/8       9.0.0.2                  0      0      0 2 65000 i
```

#### Test Fail Criteria ####
The test case is considered failing in the following cases:

- The advertised routes from the peers are not present in the output from the **show ip bgp** command.
- The BGP daemon is not running on at least one of the switches and fails during verification.
- The advertised routes from switch 2 includes AS number for switch 3 in the output from the **show ip bgp** command on switch 1 after setting **neighbor remove-private-AS**.
- The advertised routes from switch 2 does not include AS number for switch 3 in the output from the **show ip bgp** command on switch 1 after setting **no neighbor remove-private-AS**.





##  Neighbor Remote AS ##
### Objective ###
The test case verifies the **neighbor remote-as** and **no neighbor remote-as** commands by verifying the received routes after configuring and removing the neighbor configurations.

### Requirements ###

- Physical/Virtual Switches

### Setup ###
#### Topology Diagram ####

```ditta
    +----------------+         +----------------+
    |                |         |                |
    |                |         |                |
    |    Switch 1    +---------+    Switch 2    |
    |                |         |                |
    |                |         |                |
    +----------------+         +----------------+
```

#### Test Setup ####
**Switch 1** is configured with:

    !
    interface 1
        no shutdown
        ip address 9.0.0.1/8
    !
    router bgp 1
        bgp router-id 9.0.0.1
        network 11.0.0.0/8
        neighbor 9.0.0.2 remote-as 2

**Switch 2** is configured with:

    !
    interface 1
        no shutdown
        ip address 9.0.0.2/8
    !
    router bgp 2
        bgp router-id 9.0.0.2
        network 12.0.0.0/8
        neighbor 9.0.0.1 remote-as 1

### Description ###
1. Configure switches 1 and 2 with **9.0.0.1/8** and **9.0.0.2/8**, respectively, in **vtysh** with the following commands:

    ***Switch 1***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 9.0.0.1/8
    ```

    ***Switch 2***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 9.0.0.2/8
    ```

2. Verify BGP processes are running on the switches by verifying a non-null value after executing "pgrep -f bgpd" on the switches.
3. Apply BGP configurations in **vtysh** for each switch with the following commands:

    ***Switch 1***

    ```
    configure terminal
    router bgp 1
    bgp router-id 9.0.0.1
    network 11.0.0.0/8
    neighbor 9.0.0.2 remote-as 2
    ```

    ***Switch 2***

    ```
    configure terminal
    router bgp 2
    bgp router-id 9.0.0.2
    network 12.0.0.0/8
    neighbor 9.0.0.1 remote-as 1
    ```

4. Verify the **neighbor remote-as** configuration is applied succesfully by checking the route from switch 2 is received on switch 1 and the route from switch 1 is received on switch 2 via the **show ip bgp** command.
5. Remove the neighbor configuration on switch 1 by issuing the following commands in **vtysh**:

    **Switch 1**

    ```
    configure terminal
    router bgp 1
    no neighbor 9.0.0.2
    ```

6. Verify the network advertised from switch 2 in the output of **show ip bgp** of switch 1 is no longer present.

### Test Result Criteria ###
#### Test Pass Criteria ####

The test case is considered passing, for the **neighbor remote-as** command, if the advertised routes of each peer exists in the output of the **show ip bgp** command on both switches. The network and next-hop, as returned from the **show ip bgp** command, must match the information as configured on the peer.

**Expected Switch 1 Routes**

```
Local router-id 9.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       0.0.0.0                  0      0  32768  i
*> 12.0.0.0/8       9.0.0.2                  0      0      0 2 i
```

**Expected Switch 2 Routes**

```
Local router-id 9.0.0.2
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       9.0.0.1                  0      0      0 1 i
*> 12.0.0.0/8       0.0.0.0                  0      0  32768  i
```

The test case is considered passing, for the **no neighbor remote-as** command, if the advertised routes are no longer in the output of the **show ip bgp** command.

**Expected Switch 1 Routes**

```
Local router-id 9.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       0.0.0.0                  0      0  32768  i
```

**Expected Switch 2 Routes**

```
Local router-id 9.0.0.2
   Network          Next Hop            Metric LocPrf Weight Path
*> 12.0.0.0/8       0.0.0.0                  0      0  32768  i
```

#### Test Fail Criteria ####
The test case is considered failing in the following cases:

- The advertised routes from the peer are not present in the output from the **show ip bgp** command and fails during verification when the neighbor configurations are applied.
- The BGP daemon is not running on at least one of the switches and fails during verification.
- The advertised routes from the peer are still present in the output from the **show ip bgp** command after applying the **no neighbor remote-as** command.





##  Neighbor Peer-Group ##
### Objective ###
The test case verifies the **neighbor peer-group** and **no neighbor peer-group** commands by verifying the received routes after configuring and removing the peer-group configurations.

### Requirements ###

- Physical/Virtual Switches

### Setup ###
#### Topology Diagram ####

```ditta
    +----------------+         +----------------+
    |                |         |                |
    |                |         |                |
    |    Switch 1    +---------+    Switch 2    |
    |                |         |                |
    |                |         |                |
    +----------------+         +----------------+
```

#### Test Setup ####
**Switch 1** is configured with:

    !
    interface 1
        no shutdown
        ip address 9.0.0.1/8
    !
    router bgp 1
        bgp router-id 9.0.0.1
        network 11.0.0.0/8
        neighbor extern-peer-group peer-group
        neighbor extern-peer-group remote-as 2
        neighbor 9.0.0.2 peer-group extern-peer-group

**Switch 2** is configured with:

    !
    interface 1
        no shutdown
        ip address 9.0.0.2/8
    !
    router bgp 2
        bgp router-id 9.0.0.2
        network 12.0.0.0/8
        neighbor extern-peer-group peer-group
        neighbor extern-peer-group remote-as 1
        neighbor 9.0.0.1 peer-group extern-peer-group

### Description ###
The test case verifies the **neighbor peer-group** command by creating a peer-group, configuring the remote-as information, assigning a neighbor to the peer-group and verifying routes are exchanged successfully.

1. Configure switches 1 and 2 with **9.0.0.1/8** and **9.0.0.2/8**, respectively, in **vtysh** with the following commands:

    ***Switch 1***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 9.0.0.1/8
    ```

    ***Switch 2***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 9.0.0.2/8
    ```

2. Verify BGP processes are running on the switches by verifying a non-null value after executing "pgrep -f bgpd" on the switches.
3. Apply BGP configurations in **vtysh** for each switch with the following commands:

    ***Switch 1***

    ```
    configure terminal
    router bgp 1
    bgp router-id 9.0.0.1
    network 11.0.0.0/8
    neighbor extern-peer-group peer-group
    neighbor extern-peer-group remote-as 2
    neighbor 9.0.0.2 peer-group extern-peer-group
    ```

    ***Switch 2***

    ```
    configure terminal
    router bgp 2
    bgp router-id 9.0.0.2
    network 12.0.0.0/8
    neighbor extern-peer-group peer-group
    neighbor extern-peer-group remote-as 1
    neighbor 9.0.0.1 peer-group extern-peer-group
    ```

4. Verify all BGP configurations by comparing the expected values against the output of **show running-config**.
5. Verify the **neighbor peer-group** configuration is applied succesfully by checking the route from switch 2 is received on switch 1 and the route from switch 1 is received on switch 2 via the **show ip bgp** command.
6. Remove the neighbor peer-group configuration on switch 1 by issuing the following commands in **vtysh**:

    **Switch 1**

    ```
    configure terminal
    router bgp 1
    no neighbor 9.0.0.2 peer-group extern-peer-group
    ```

7. Verify the network advertised from switch 2 in the output of **show ip bgp** of switch 1 is no longer present.

### Test Result Criteria ###
#### Test Pass Criteria ####

The test case is considered passing, for the **neighbor peer-group** command, if the advertised routes of each peer exists in the output of the **show ip bgp** command on both switches. The network and next-hop must match the information as configured on the peer.

**Expected Switch 1 Routes**

```
Local router-id 9.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       0.0.0.0                  0      0  32768  i
*> 12.0.0.0/8       9.0.0.2                  0      0      0 2 i
```

**Expected Switch 2 Routes**

```
Local router-id 9.0.0.2
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       9.0.0.1                  0      0      0 1 i
*> 12.0.0.0/8       0.0.0.0                  0      0  32768  i
```

The test case is considered passing, for the **no neighbor peer-group** command, if the advertised routes are no longer in the output of the **show ip bgp** command.

**Expected Switch 1 Routes**

```
Local router-id 9.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       0.0.0.0                  0      0  32768  i
```

**Expected Switch 2 Routes**

```
Local router-id 9.0.0.2
   Network          Next Hop            Metric LocPrf Weight Path
*> 12.0.0.0/8       0.0.0.0                  0      0  32768  i
```

#### Test Fail Criteria ####
The test case is considered failing in the following cases:

- The advertised routes from the peers are not present in the output from the **show ip bgp** command and fails during verification when the neighbor peer-group configurations are applied.
- The BGP daemon is not running on at least one of the switches and fails during verification.
- The advertised routes from the peer are still present in the output from the **show ip bgp** command after applying the **no neighbor peer-group** command.





##  IP Prefix-List and Route-Map ##
### Objective ###
The test case verifies the **ip prefix-list**, **route-map**, **route-map set**, **route-map match**, **neighbor route-map**, **no route-map set**, and **no route-map match** commands by verifying the received routes and configurations after applying and removing the configurations.

### Requirements ###

- Physical/Virtual Switches

### Setup ###
#### Topology Diagram ####

```ditta
    +----------------+         +----------------+
    |                |         |                |
    |                |         |                |
    |    Switch 1    +---------+    Switch 2    |
    |                |         |                |
    |                |         |                |
    +----------------+         +----------------+
```

#### Test Setup ####
**Switch 1** is configured with:

    !
    interface 1
        no shutdown
        ip address 8.0.0.1/8
    !
    ip prefix-list BGP1_OUT seq 5 deny 9.0.0.0/8
    ip prefix-list BGP1_OUT seq 10 permit 10.0.0.0/8
    !
    route-map BGP1_OUT permit 5
        match ip address prefix-list BGP1_OUT
        set metric 1000
        set community 1:5003 additive
    !
    router bgp 1
        bgp router-id 8.0.0.1
        network 9.0.0.0/8
        network 10.0.0.0/8
        neighbor 8.0.0.2 remote-as 2
        neighbor 8.0.0.2 route-map BGP1_OUT out

**Switch 2** is configured with:

    !
    interface 1
        no shutdown
        ip address 8.0.0.2/8
    !
    router bgp 2
        bgp router-id 8.0.0.2
        network 11.0.0.0/8
        neighbor 8.0.0.1 remote-as 1

### Description ###
The test case verifies the **ip prefix-list** command by configuring a **route-map**, applying the route-map to a neighbor via the **neighbor route-map** command, and verifying routes are filtered and exchanged successfully between the two switches. The test case also verifies **route-map set**, **route-map match**, **no route-map set**, and **no route-map match** commands.

1. Configure switches 1 and 2 with **8.0.0.1/8** and **8.0.0.2/8**, respectively, in **vtysh** with the following commands:

    ***Switch 1***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 8.0.0.1/8
    ```

    ***Switch 2***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 8.0.0.2/8
    ```

2. Verify BGP processes are running on the switches by verifying a non-null value after executing "pgrep -f bgpd" on the switches.
3. Create the IP prefix-lists on switch 1 to prohibit network 9.0.0.0/8 and permit network 10.0.0.0/8 with the following commands:

    ***Switch 1***

    ```
    configure terminal
    ip prefix-list BGP1_OUT seq 5 deny 9.0.0.0/8
    ip prefix-list BGP1_OUT seq 10 permit 10.0.0.0/8
    ```

4. Create the route-map on switch 1, assign the prefix-list to the route-map using the **match** command, and apply **set** configurations:

    ***Switch 1***

    ```
    configure terminal
    route-map BGP1_OUT permit 5
    match ip address prefix-list BGP1_OUT
    set metric 1000
    set community 1:5003 additive
    ```

5. Apply BGP configurations on each switch. The route-map configuration is applied to a neighbor, which will filter outgoing advertised routes.

    ***Switch 1***

    ```
    configure terminal
    router bgp 1
    bgp router-id 8.0.0.1
    network 9.0.0.0/8
    network 10.0.0.0/8
    neighbor 8.0.0.2 remote-as 2
    neighbor 8.0.0.2 route-map BGP1_OUT out
    ```

    ***Switch 2***

    ```
    configure terminal
    router bgp 2
    bgp router-id 8.0.0.2
    network 11.0.0.0/8
    neighbor 8.0.0.1 remote-as 1
    ```

6. Verify all BGP configurations by comparing the expected values against the output of **show running-config**.
7. Verify the **neighbor route-map** configuration is applied succesfully by checking the network 9.0.0.0/8 from switch 1 is not received and the network 10.0.0.0/8 is received on switch 2 via the **show ip bgp** command.
8. Verify the metric value, as configured on switch 1, is reflected in the received route on switch 2 via the **show ip bgp** command.
9. Remove the **set metric** and **set community** configurations on switch 1 by issuing the following commands in **vtysh**:

    **Switch 1**

    ```
    configure terminal
    route-map BGP1_OUT permit 5
    no set metric
    no set community
    ```

10. Refresh the routes by removing the neighbor configuration on switch 2 by issuing the following commands in **vtysh**:

    **Switch 2**

    ```
    configure terminal
    router bgp 2
    no neighbor 8.0.0.1
    ```

11. Verify the network advertised from switch 1 in the output of **show ip bgp** on switch 2 is no longer present.
12. Reconfigure the neighbor on switch 2 with the following commands:

    **Switch 2**

    ```
    configure terminal
    router bgp 2
    neighbor 8.0.0.1 remote-as 1
    ```

13. Verify the network advertised from switch 1 in the output of **show ip bgp** on switch 2 is present.
14. Verify the metric value is 0 in the output of **show ip bgp** on switch 2.
15. Verify **no route-map match** by removing the applied prefix-list from the route-map configuration with the following commands:

    **Switch 1**

    ```
    configure terminal
    route-map BGP1_OUT permit 5
    no match ip address prefix-list BGP1_OUT
    ```

16. Refresh the routes by repeating steps **10-13**.
17. Verify the network 9.0.0.0/8 is present in the output of **show ip bgp** on switch 2.

### Test Result Criteria ###
#### Test Pass Criteria ####

The test case is considered passing if the advertised routes from switch 1 do not include network 9.0.0.0/8 in the output of the **show ip bgp** command on switch 2. The **ip prefix-list**, **route-map**, and **neighbor route-map** commands prohibit network 9.0.0.0/8 from being advertised out from switch 1 towards switch 2.

**Expected Switch 1 Routes**

```
Local router-id 8.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 9.0.0.0          0.0.0.0                  0         32768 i
*> 10.0.0.0         0.0.0.0                  0         32768 i
*> 11.0.0.0         8.0.0.2                  0             0 2 i
```

**Expected Switch 2 Routes**

```
Local router-id 8.0.0.2
   Network          Next Hop            Metric LocPrf Weight Path
*> 10.0.0.0         8.0.0.1               1000             0 1 i
*> 11.0.0.0         0.0.0.0                  0         32768 i
```

The test case is considered passing, for the **no route-map match** command, if all advertised routes from switch 1 exists in the output of the **show ip bgp** command on switch 2.

**Expected Switch 2 Routes**

```
Local router-id 8.0.0.2
   Network          Next Hop            Metric LocPrf Weight Path
*> 9.0.0.0          8.0.0.1                  0             0 1 i
*> 10.0.0.0         8.0.0.1                  0             0 1 i
*> 11.0.0.0         0.0.0.0                  0         32768 i
```

#### Test Fail Criteria ####
The test case is considered failing in the following cases:

- The advertised routes from the peers are not present in the output from the **show ip bgp** command.
- The BGP daemon is not running on at least one of the switches and fails during verification.
- The prohibited network 9.0.0.0/8 from switch 1 exists in the output of the **show ip bgp** command on switch 2 prior to the removal of the **route-map match** configuration.
- The set metric value is not 1000 for the routes from switch 1 prior to the removal of the **route-map set** configuration.
- The network 9.0.0.0/8 is not present in the output of the **show ip bgp** command on switch 2 after the **no route-map match** command was executed.





##  IP Prefix-List, Route-Map, and Peer-Group with Hosts PING  ##
### Objective ###
The test case verifies the ability to ping between hosts on different networks after applying the **ip prefix-list**, **route-map**, **neighbor peer-group**, and **neighbor route-map** commands.

### Requirements ###

- Physical/Virtual Switches

### Setup ###
#### Topology Diagram ####

```ditta
    +----------------+         +----------------+
    |                |         |                |
    |                |         |                |
    |    Switch 1    +---------+    Switch 2    |
    |                |         |                |
    |                |         |                |
    +--------+-------+         +--------+-------+
             |                          |
             |                          |
             |                          |
    +--------+-------+         +--------+-------+
    |                |         |                |
    |                |         |                |
    |     Host 1     |         |     Host 2     |
    |                |         |                |
    |                |         |                |
    +----------------+         +----------------+
```

#### Test Setup ####
**Switch 1** is configured with:

    !
    interface 1
        no shutdown
        ip address 11.0.1.254/24
        interface 2
        no shutdown
        ip address 9.0.0.1/8
    !
    ip prefix-list BGP1_IN seq 5 deny 10.0.0.0/8
    ip prefix-list BGP1_IN seq 10 permit 11.0.0.0/8
    !
    route-map BGP1_IN permit 5
        description BGP1 Testing
        match ip address prefix-list BGP1_IN
    !
    router bgp 1
        bgp router-id 9.0.0.1
        network 10.0.0.0/8
        network 11.0.0.0/8
        neighbor extern-peer-group peer-group
        neighbor 9.0.0.2 remote-as 2
        neighbor 9.0.0.2 route-map BGP1_IN out
        neighbor 9.0.0.2 peer-group extern-peer-group
        neighbor extern-peer-group remote-as 2

**Switch 2** is configured with:

    !
    interface 1
        no shutdown
        ip address 12.0.1.254/24
    !
    interface 2
        no shutdown
        ip address 9.0.0.2/8
    !
    ip prefix-list BGP2_IN seq 5 deny 13.0.0.0/8
    ip prefix-list BGP2_IN seq 10 permit 11.0.0.0/8
    !
    route-map BGP2_IN permit 5
        description BGP2 Testing
        match ip address prefix-list BGP2_IN
    !
    router bgp 2
        bgp router-id 9.0.0.2
        network 12.0.0.0/8
        neighbor extern-peer-group peer-group
        neighbor 9.0.0.1 remote-as 1
        neighbor 9.0.0.1 route-map BGP2_IN in
        neighbor 9.0.0.1 peer-group extern-peer-group
        neighbor extern-peer-group remote-as 1

### Description ###
The test case verifies the **ip prefix-list** command by configuring a **route-map**, applying the route-map to a neighbor via the **neighbor route-map** command, and verifying routes are filtered and exchanged successfully between the two switches after assigning the neighbor to a **peer-group**. The test case verifies both hosts can send and receive PINGs through the routes.

1. Configure the interfaces between the two switches with **9.0.0.1/8** and **9.0.0.2/8**, on switches 1 and 2, respectively, in **vtysh** with the following commands:

    ***Switch 1***

    ```
    configure terminal
    interface 2
    no shutdown
    ip address 9.0.0.1/8
    ```

    ***Switch 2***

    ```
    configure terminal
    interface 2
    no shutdown
    ip address 9.0.0.2/8
    ```

2. Configure the interfaces between the switches and the connected hosts with **11.0.1.254/24** and **12.0.1.254/24**, on switches 1 and 2, respectively, in **vtysh** with the following commands:

    ***Switch 1***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 11.0.1.254/24
    ```

    ***Switch 2***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 12.0.1.254/24
    ```

3. Configure the IP addresses **11.0.1.1/8** and **12.0.1.1/8** on hosts 1 and 2, respectively.
4. Verify BGP processes are running on the switches by verifying a non-null value after executing "pgrep -f bgpd" on the switches.
5. Verify the hosts are not able to PING.
6. Apply BGP configurations in **vtysh** for each switch with the following commands:

    ***Switch 1***

    ```
    configure terminal
    ip prefix-list BGP1_IN seq 5 deny 10.0.0.0/8
    ip prefix-list BGP1_IN seq 10 permit 11.0.0.0/8
    route-map BGP1_IN permit 5
    description BGP1 Testing
    match ip address prefix-list BGP1_IN
    exit
    router bgp 1
    bgp router-id 9.0.0.1
    network 10.0.0.0/8
    network 11.0.0.0/8
    neighbor extern-peer-group peer-group
    neighbor 9.0.0.2 remote-as 2
    neighbor 9.0.0.2 route-map BGP1_IN out
    neighbor 9.0.0.2 peer-group extern-peer-group
    neighbor extern-peer-group remote-as 2
    ```

    ***Switch 2***

    ```
    configure terminal
    ip prefix-list BGP2_IN seq 5 deny 13.0.0.0/8
    ip prefix-list BGP2_IN seq 10 permit 11.0.0.0/8
    route-map BGP2_IN permit 5
    description BGP2 Testing
    match ip address prefix-list BGP2_IN
    exit
    router bgp 2
    bgp router-id 9.0.0.2
    network 12.0.0.0/8
    neighbor extern-peer-group peer-group
    neighbor 9.0.0.1 remote-as 1
    neighbor 9.0.0.1 route-map BGP2_IN in
    neighbor 9.0.0.1 peer-group extern-peer-group
    neighbor extern-peer-group remote-as 1
    ```

7. Verify all BGP configurations by comparing the expected values against the output of **show running-config**.
8. Verify the **neighbor route-map** configuration is applied succesfully by checking the network 10.0.0.0/8 from switch 1 is not received and the network 11.0.0.0/8 is received on switch 2 via the **show ip bgp** command.
9. Verify hosts are able to PING after routes are advertised.

### Test Result Criteria ###
#### Test Pass Criteria ####

The test case is considered passing if the advertised routes from switch 1 do not include network 10.0.0.0/8 in the output of the **show ip bgp** command on switch 2 and if the hosts are able to ping. The **ip prefix-list**, **route-map**, and **neighbor route-map** commands prohibit network 10.0.0.0/8 from being advertised out from switch 1 towards switch 2.

**Expected Switch 1 Routes**

```
Local router-id 9.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 10.0.0.0/8       0.0.0.0                  0      0  32768  i
*> 11.0.0.0/8       0.0.0.0                  0      0  32768  i
*> 12.0.0.0/8       9.0.0.2                  0      0      0 2 i
```

**Expected Switch 2 Routes**

```
Local router-id 9.0.0.2
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       9.0.0.1                  0      0      0 1 i
*> 12.0.0.0/8       0.0.0.0                  0      0  32768  i
```

#### Test Fail Criteria ####
The test case is considered failing in the following cases:

- The advertised routes from the peer are not present in the output from the **show ip bgp** command.
- The output of the **show running-config** do not match with the input configuration.
- The BGP daemon is not running on at least one of the switches and fails during verification.
- The prohibited network 10.0.0.0/8 from switch 1 exists in the output of the **show ip bgp** command on switch 2.
- The hosts are not able to PING after BGP routes are advertised.

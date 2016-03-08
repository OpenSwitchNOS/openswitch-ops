# DHCP Relay Feature Test Cases

## Contents

- [Verify the basic DHCP relay functionality](#verify-the-basic-dhcp-relay-functionality)
- [Failure cases](#failure-cases)
    - [Verify the DHCP relay functionality is inactive when DHCP relay is disabled](#verify-the-dhcp-relay-functionality-is-inactive-when-dhcp-relay-is-disabled)
    - [Verify the DHCP relay functionality is inactive when server is unreachable](#verify-the-dhcp-relay-functionality-is-inactive-when-server-is-unreachable)
    - [Verify the DHCP relay functionality is inactive when client is unreachable](#verify-the-dhcp-relay-functionality-is-inactive-when-server-is-unreachable)

## Verify the basic DHCP relay functionality
### Objective
The purpose of this test is to test the functionality of the DHCP relay when client and server connected through a intermediate switch.

### Requirements
The requirements for this test case are:
 - Three (3) switches
 - One (1) workstation

### Setup
#### Topology diagram

```ditaa
+----------------+        +---------------+      +----------------+       +----------------+
|                |        |               |      |                |       |                |
|                |        |               |      |                |       |                |
|                |        |               |      |                |       |                |
| DHCP Client    |        |  Switch2      |      |  Switch3       |       |  DHCP Server   |
|                +--------+               +------+                +-------+                |
|                |        |               |      |                |       |                |
|                |        |               |      |                |       |                |
+----------------+        +---------------+      +----------------+       +----------------+
```

### Description
Configure IPv4 address on switch2, switch3, DHCP server. Add static routes and check connectivity from client to relay.
Configure server IPv4 address as helper addresses on DHCP relay agent(switch3).
Configure the DHCP Server to assign IPv4 address to the client.
Verify that the DHCP client has started and the DHCP relay agent relays DHCP Packet to Client/Server.
Verify that the DHCP client has received IPv4 address.
### Test result criteria
#### Test pass criteria
The DHCP client has recieved IPv4 address.
#### Test fail criteria
This test fails if IPv4 address is not received by the DHCP client.

## Failure cases
### Objective
The purpose of this test is to possible failure cases and corner cases when using DHCP relay.

### Requirements
The requirements for this test case are:
 - Three (3) switches
 - One (1) workstation

### Setup
#### Topology diagram

```ditaa
+----------------+        +---------------+      +----------------+       +----------------+
|                |        |               |      |                |       |                |
|                |        |               |      |                |       |                |
|                |        |               |      |                |       |                |
| DHCP Client    |        |  Switch2      |      |  Switch3       |       |  DHCP Server   |
|                +--------+               +------+                +-------+                |
|                |        |               |      |                |       |                |
|                |        |               |      |                |       |                |
+----------------+        +---------------+      +----------------+       +----------------+
```

### Verify the DHCP relay functionality is inactive when DHCP relay is disabled
### Description
Configure IPv4 address on Switch2, DHCP relay, DHCP server. Add static routes and check connectivity from client to relay.
Configure server IPv4 address as helper addresses on DHCP relay agent.
Disable DHCP relay globally on switch3 using `no dhcp-relay` command.
Configure the DHCP Server to assign IPv4 address to the client.
Verify that the DHCP client has started.
Verify that the DHCP client has not received IPv4 address.
### Test result criteria
#### Test pass criteria
The DHCP client has not recieved IPv4 address.
#### Test fail criteria
This test fails if IPv4 address is received by the DHCP client.

### Verify the DHCP relay functionality is inactive when server is unreachable
### Description
Configure IPv4 address on Switch2, DHCP relay, DHCP server. Add static routes and check connectivity from client to relay.
Change the interface state to down, connecting the server and relay using appropriate cli command.
Configure server IPv4 address as helper addresses on DHCP relay agent.
Configure the DHCP Server to assign IPv4 address to the client.
Verify that the DHCP client has started.
Verify that the DHCP client has not received IPv4 address.
### Test result criteria
#### Test pass criteria
The DHCP client has not recieved IPv4 address.
#### Test fail criteria
This test fails if IPv4 address is received by the DHCP client.

### Verify the DHCP relay functionality is inactive when client is unreachable
### Description
Configure IPv4 address on Switch2, DHCP relay, DHCP server. Add static routes and check connectivity from client to relay.
Change the interface state to down, connecting the DHCP client and relay using appropriate cli command.
Configure server IPv4 address as helper addresses on DHCP relay agent.
Configure the DHCP Server to assign IPv4 address to the client.
Verify that the DHCP client has started.
Verify that the DHCP client has not received IPv4 address.
### Test result criteria
#### Test pass criteria
The DHCP client has not recieved IPv4 address.
#### Test fail criteria
This test fails if IPv4 address is received by the DHCP client.

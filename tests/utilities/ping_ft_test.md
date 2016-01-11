Ping Feature Test Cases
========

## Contents
   - [Verify the basic Ping](#verify-the-basic-ping)
   - [Verify the Ping with the optional parameters](#verify-the-ping-with-the-optional-parameters)
   - [Verify the Ping with the extended option parameters](#verify-the-ping-with-the-extended-option-parameters)
   - [Verify the basic Ping6](#verify-the-basic-ping6)
   - [Verify the Ping6 with the optional parameters](#verify-the-ping6-with-the-optional-parameters)
   - [Verify the Ping failure cases](#verify-the-ping-failure-cases)
   - [Verify the Ping6 failure cases](#verify-the-ping6-failure-cases)

## Verify the basic Ping
### Objective
Verify the basic ping from the switch2 configured with an IPv4 address to host1
### Requirements
The requirements for this test case are:
 - RTL
 - 2 switch
 - 1 workstation

### Setup
#### Topology diagram
    ```ditaa
                +---------+            +----------+          +-----------+
                |         |            |          |          |           |
                |         |            |          |          |           |
                | Host1   +------------+ Switch1  +----------+ Switch2   |
                |         |            |          |          |           |
                |         |            |          |          |           |
                +---------+            +----------+          +-----------+
    ```
#### Test setup

### Test case 1.01
Test case checks that the ping is successful from switch2 to host1 with the host1 IPv4 address.
### Description
From switch2 CLI, execute command `ping <destinationIP>`.
Where destination IP is an IPv4 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping from switch2 to host1 is successful and CLI output shows a zero packet loss.
#### Test fail criteria
Switch2 CLI output shows host unreachable or packet loss is more than 0%.

## Verify the Ping with the optional parameters
### Objective
Verify the ping with the optional parameters from the switch2 configured with an IPv4 address to host1
### Requirements
The requirements for this test case are:
 - RTL
 - 2 switch
 - 1 workstation

### Setup
#### Topology diagram
    ```ditaa
                +---------+            +----------+          +-----------+
                |         |            |          |          |           |
                |         |            |          |          |           |
                | Host1   +------------+ Switch1  +----------+ Switch2   |
                |         |            |          |          |           |
                |         |            |          |          |           |
                +---------+            +----------+          +-----------+
    ```
#### Test setup

### Test case 2.01
Test case checks that the ping is successful from switch2 to host1 with the data-fill parameter.
### Description
From switch2 CLI, execute command `ping <destinationIP> data-fill <character>`.
Where destination IP is an IPv4 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping from switch2 to host1 with the data-fill parameter is successful and CLI output shows a zero packet loss.
#### Test fail criteria
Switch2 CLI should display an invalid input response as unknown command.

### Test case 2.02
Test case checks that the ping is successful from switch2 to host1 with the datagram-size parameter.
### Description
From switch2 CLI, execute command `ping <destinationIP> datagram-size <size>`.
Where destination IP is an IPv4 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping from switch2 to host1 with the datagram-size parameter is successful and CLI output shows a zero packet loss.
Also, verify that the packet with `<size>` bytes is sent to the destination.
#### Test fail criteria
Switch2 CLI should display an invalid input response as unknown command.

### Test case 2.03
Test case checks that the ping is successful from switch2 to host1 with the interval parameter.
### Description
From switch2 CLI, execute command `ping <destinationIP> interval <time>`.
Where destination IP is an IPv4 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping from switch2 to host1 with the interval parameter is successful and CLI output shows a zero packet loss.
#### Test fail criteria
Switch2 CLI should display an invalid input response as unknown command.

### Test case 2.04
Test case checks that the ping is successful from switch2 to host1 with the repetition parameter.
### Description
From switch2 CLI, execute command `ping <destinationIP> repetition <count>`.
Where destination IP is an IPv4 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping from switch2 to host1 with the repetition parameter is successful and CLI output shows a zero packet loss.
Also, verify that `<count>` number of packets are sent to the destination.
#### Test fail criteria
Switch2 CLI should display an invalid input response as unknown command.

### Test case 2.05
Test case checks that the ping is successful from switch2 to host1 with the timeout parameter.
### Description
From switch2 CLI, execute command `ping <destinationIP> timeout <time_out>`.
Where destination IP is an IPv4 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping from switch2 to host1 with the timeout parameter is successful and CLI output shows a zero packet loss.
#### Test fail criteria
Switch2 CLI should display an invalid input response as unknown command.

### Test case 2.06
Test case checks that the ping is successful from switch2 to host1 with the TOS parameter.
### Description
From switch2 CLI, execute command `ping <destinationIP> tos <number>`.
Where destination IP is an IPv4 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping from switch2 to host1 with the TOS parameter is successful and CLI output shows a zero packet loss.
#### Test fail criteria
Switch2 CLI should display an invalid input response as unknown command.

## Verify the Ping with the extended option parameters
### Objective
Verify the ping with the extended option parameters from the switch2 configured with an IPv4 address to host1
### Requirements
The requirements for this test case are:
 - RTL
 - 2 switch
 - 1 workstation

## Setup
#### Topology diagram
    ```ditaa
                +---------+            +----------+          +-----------+
                |         |            |          |          |           |
                |         |            |          |          |           |
                | Host1   +------------+ Switch1  +----------+ Switch2   |
                |         |            |          |          |           |
                |         |            |          |          |           |
                +---------+            +----------+          +-----------+
    ```
#### Test setup

### Test case 3.01
Test case checks that the ping is successful from switch2 to host1 with the ip-option record-route parameter.
### Description
From switch2 CLI, execute command `ping <destinationIP> ip-option record-route`.
Where destination IP is an IPv4 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping from switch2 to host1 with the ip-option record-route parameter is successful and CLI output shows a zero packet loss.
#### Test fail criteria
Switch2 CLI output shows network unreachable or packet loss is more than 0%.

### Test case 3.02
Test case checks that the ping is successful from switch2 to host1 with the ip-option include-timestamp parameter.
### Description
From switch2 CLI, execute command `ping <destinationIP> ip-option include-timestamp`.
Where destination IP is an IPv4 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping from switch2 to host1 with the ip-option include-timestamp parameter is successful and CLI output shows a zero packet loss.
#### Test fail criteria
Switch2 CLI output shows network unreachable or packet loss is more than 0%.

### Test case 3.03
Test case checks that the ping is successful from switch2 to host1 with the ip-option include-timestamp-and-address parameter.
### Description
From switch2 CLI, execute command `ping <destinationIP> ip-option include-timestamp-and-address`.
Where destination IP is an IPv4 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping from switch2 to host1 with the ip-option include-timestamp-and-address parameter is successful and CLI output shows a zero packet loss.
#### Test fail criteria
Switch2 CLI output shows network unreachable or packet loss is more than 0%.

## Verify the basic Ping6
### Objective
Verify the basic ping6 from the switch2 configured with an IPv6 address to host1.
### Requirements
The requirements for this test case are:
 - RTL
 - 2 switch
 - 1 workstation

### Setup
#### Topology diagram
    ```ditaa
                +---------+            +----------+          +-----------+
                |         |            |          |          |           |
                |         |            |          |          |           |
                | Host1   +------------+ Switch1  +----------+ Switch2   |
                |         |            |          |          |           |
                |         |            |          |          |           |
                +---------+            +----------+          +-----------+
    ```
#### Test setup

### Test case 4.01
Test case checks that the ping6 is successful from switch2 to host1 with the host1 IPv6 address.
### Description
From switch2 CLI, execute command `ping6 <destinationIP>`.
Where destination IP is an IPv6 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping6 from switch2 to host1 is successful and CLI output shows a zero packet loss.
#### Test fail criteria
Switch2 CLI output shows network unreachable or packet loss is more than 0%.

## Verify the Ping6 with the optional parameters
### Objective
Verify the ping6 with the optional parameters from the switch2 configured with an IPv6 address to host1.
### Requirements
The requirements for this test case are:
 - RTL
 - 2 switch
 - 1 workstation

### Setup
#### Topology diagram
    ```ditaa
                +---------+            +----------+          +-----------+
                |         |            |          |          |           |
                |         |            |          |          |           |
                | Host1   +------------+ Switch1  +----------+ Switch2   |
                |         |            |          |          |           |
                |         |            |          |          |           |
                +---------+            +----------+          +-----------+
    ```
#### Test setup

### Test case 5.01
Test case checks that the ping6 is successful from switch2 to host1 with the data-fill parameter.
### Description
From switch2 CLI, execute command `ping6 <destinationIP> data-fill <character>`.
Where destination IP is an IPv6 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping6 from switch2 to host1 with the data-fill parameter is successful and CLI output shows a zero packet loss.
#### Test fail criteria
Switch2 CLI should display an invalid input response as unknown command.

### Test case 5.02
Test case checks that the ping6 is successful from switch2 to host1 with the datagram-size parameter.
### Description
From switch2 CLI, execute command `ping6 <destinationIP> datagram-size <size>`.
Where destination IP is a IPv6 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping6 from switch2 to host1 with the datagram-size parameter is successful and CLI output shows a zero packet loss.
Also, verify that the packet with `<size>` bytes is sent to the destination.
#### Test fail criteria
Switch2 CLI should display an invalid input response as unknown command.

### Test case 5.03
Test case checks that the ping6 is successful from switch2 to host1 with the interval parameter.
### Description
From switch2 CLI, execute command `ping6 <destinationIP> interval <time>`.
Where destination IP is an IPv6 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping6 from switch2 to host1 with the interval parameter is successful and CLI output shows a zero packet loss.
#### Test fail criteria
Switch2 CLI should display an invalid input response as unknown Command.

### Test case 5.04
Test case checks that the ping6 is successful from switch2 to host1 with the repetition parameter.
### Description
From switch2 CLI, execute command `ping6 <destinationIP> repetition <count>`.
Where destination IP is an IPv6 address configured on host1.
### Test result criteria
#### Test pass criteria
Ping6 from switch2 to host1 with the repetition parameter is successful and CLI output shows a zero packet loss.
Also, verify that `<count>` number of packets are sent to the destination.
#### Test fail criteria
Switch2 CLI should display an invalid input response as unknown command.

## Verify the Ping failure cases
### Objective
Verify the different ping failure cases
### Requirements
The requirements for this test case are:
 - RTL
 - 1 switch

### Setup
#### Topology diagram
     ```ditaa
                +-------+
                |       |
                |switch2|
                |       |
                +-------+
     ```
#### Test setup

### Test case 6.01
Test case checks that the ping fails from switch2 to a unreachable IPv4 address.
### Description
From switch2 CLI, execute command `ping <destinationIP>`.
Where destination IP is an unreachable IPv4 address.
### Test result criteria
#### Test pass criteria
Switch2 CLI output displays Network is unreachable.
#### Test fail criteria
Ping is successful and packet loss is 0%.

### Test case 6.02
Test case checks that the ping fails from switch2 to a wrong IPv4 address which has the same subnet mask as configured on switch2.
### Description
From switch1 CLI, execute command `ping <destinationIP>`.
Where destination IP is a wrong IPv4 address which has the same subnet mask as configured on switch2.
### Test result criteria
#### Test pass criteria
Switch2 CLI output displays Destination Host Unreachable.
#### Test fail criteria
Ping is successful and packet loss is 0%.

### Test case 6.03
Test case checks that the ping fails from switch2 to a unknown host.
### Description
From switch2 CLI, execute command `ping <hostname>`.
Where hostname is a unknown host name.
### Test result criteria
#### Test pass criteria
Switch2 CLI output displays unknown host.
#### Test fail criteria
Ping is successful and packet loss is 0%.

## Verify the Ping6 failure cases
### Objective
Verify the different ping6 failure cases
### Requirements
The requirements for this test case are:
 - RTL
 - 1 switch

### Setup
#### Topology diagram
     ```ditaa
                +-------+
                |       |
                |switch2|
                |       |
                +-------+
     ```
#### Test setup

### Test case 7.01
Test case checks that the ping6 fails from switch2 to a unreachable IPv6 address.
### Description
From switch2 CLI, execute command `ping6 <destinationIP>`.
Where destination IP is an unreachable IPv6 address.
### Test result criteria
#### Test pass criteria
Switch2 CLI output displays Network is unreachable.
#### Test fail criteria
Ping6 is successful and packet loss is 0%.

### Test case 7.02
Test case checks that the ping6 fails from switch1 to a unknown host.
### Description
From DUT CLI, execute command `ping6 <hostname>`.
Where hostname is a unknown host name.
### Test result criteria
#### Test pass criteria
Switch2 CLI output displays unknown host.
#### Test fail criteria
Ping6 is successful and packet loss is 0%.

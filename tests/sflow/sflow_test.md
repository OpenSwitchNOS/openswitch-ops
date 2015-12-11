Sflow Feature Test Cases
========================


## Contents

- [Global sflow enable and disable](#global-sflow-enable-and-disable)
- [Multiple sflow collectors](#multiple-sflow-collectors)

## Global sflow enable and disable
### Objective
This test verifies global sflow enable/disable functionality on the switch.
### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/sflow/test_sflow_ft_enable_disable.py`
### Setup
#### Topology diagram
```ditaa
           200.0.0.1/24
+-------------------------------+
|          interface 3          |
|                               |
|                               |
|            Switch             |
|                               |
|                               |
| interface 1        interface 2|
+-------------------------------+
   |10.10.10.1/24        |10.10.11.1/24
   |                     |
   |                     |
   |                     |
   |                     |                     +-------------------+
   |                     |                     |                   |
   |                     |       10.10.11.2/24 |                   |
   |                     +---------------------+     sflowtool     |
   |                                           |                   |
   |10.10.10.2/24                              |                   |
+---------------+                              +-------------------+
|               |
|               |
|     Host1     |
|               |
|               |
+---------------+
```
### Description
This test is used to ensure that sflow feature works on OpenSwitch.

1. Connect Host1 to the switch and configure an IP address.
```
ip addr add 10.10.10.2/24 dev eth1
```
2. Connect another host which has sflowtool (sflow collector) to the switch. Configure IP address on it.
```
ip addr add 10.10.11.2/24 dev eth1
```
3. Configure the interfaces on the switch which are connected to these two hosts.
   Also configure another interface which will be used during sflow configuration.
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# ip address 10.10.10.1/24
ops-as5712(config-if)# no shut
ops-as5712(config-if)# exit
ops-as5712(config)# interface 2
ops-as5712(config-if)# ip address 10.10.11.1/24
ops-as5712(config-if)# no shut
ops-as5712(config-if)# exit
ops-as5712(config)# interface 3
ops-as5712(config-if)# ip address 200.0.0.1/24
ops-as5712(config-if)# no shut
ops-as5712(config-if)# exit
```
4. Enable global sflow configuration on the switch.
```
ops-as5712# configure terminal
ops-as5712(config)# sflow enable
```
5. Configure the collector's IP address (attached to interface 2 of the switch).
   Set the agent-interface (interface 3), polling at 15 seconds and sampling rate at 25 (1 in 25 packets will be sampled)
```
ops-as5712# configure terminal
ops-as5712(config)# sflow collector 10.10.11.2
ops-as5712(config)# sflow agent-interface 3
ops-as5712(config)# sflow polling 15
ops-as5712(config)# sflow sampling 25
```
6. Ping 100 packets between Host1 and the switch. sflowtool should be able to see FLOW packets as well as CNTR packets from the switch.
```
ping 10.10.10.1 -c 100 -i 0.01
```
7. Disable global sflow configuration on the switch.
```
ops-as5712# configure terminal
ops-as5712(config)# no sflow enable
```
8. Repeat the ping step and check if the sflowtool is still able to get sflow packets from switch.
### Test result criteria
#### Test pass criteria
1. When sflow is enabled, the sflowtool is able to see sflow packets which are sent from the switch.
   The agent IP address in the FLOW and CNTR packets match the IP address of the agent interface configured (interface 3 in above configuration).
2. When sflow is disabled, sflowtool does not see any sflow packets from the switch.
#### Test fail criteria
1. On enable, sflowtool does not receive any sflow packets from the switch.
2. On disable, sflowtool is able to receive sflow packets from the switch.

## Multiple sflow collectors
### Objective
This test verifies multiple sflow collector configuration on the switch.
### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/sflow/test_sflow_ft_multiple_collectors.py`
### Setup
#### Topology diagram
```ditaa
                        +------------------------------+
                        |                              |
                        |                              |
                        |10.10.12.1/24                 |10.10.12.2/24
+-------------------------------+              +-------------------+
|                   interface 3 |              |                   |
|                               |              |                   |
|                               |              |   sflowtool-2     |
|            Switch             |              |                   |
|                               |              |                   |
|                               |              +-------------------+
| interface 1        interface 2|
+-------------------------------+
   |10.10.10.1/24        |10.10.11.1/24
   |                     |
   |                     |
   |                     |
   |                     |                     +-------------------+
   |                     |                     |                   |
   |                     |       10.10.11.2/24 |                   |
   |                     +---------------------+    sflwotool-1    |
   |                                           |                   |
   |10.10.10.2/24                              |                   |
+---------------+                              +-------------------+
|               |
|               |
|     Host1     |
|               |
|               |
+---------------+
```
### Description
This test is used to ensure that sflow feature on OpenSwitch works with multiple collectors.

1. Connect Host1 to the switch and configure an IP address.
```
ip addr add 10.10.10.2/24 dev eth1
```
2. Connect the first sflow collector, sflowtool-1 to the switch. Configure IP address on it.
```
ip addr add 10.10.11.2/24 dev eth1
```
3. Connect the second sflow collector, sflowtool-2 to the switch. Configure IP address on it.
```
ip addr add 10.10.12.2/24 dev eth1
```
3. Configure the interfaces on the switch which are connected to these hosts.
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# ip address 10.10.10.1/24
ops-as5712(config-if)# no shut
ops-as5712(config-if)# exit
ops-as5712(config)# interface 2
ops-as5712(config-if)# ip address 10.10.11.1/24
ops-as5712(config-if)# no shut
ops-as5712(config-if)# exit
ops-as5712(config)# interface 3
ops-as5712(config-if)# ip address 10.10.12.1/24
ops-as5712(config-if)# no shut
ops-as5712(config-if)# exit
```
4. Enable global sflow configuration on the switch.
```
ops-as5712# configure terminal
ops-as5712(config)# sflow enable
```
5. Configure both the sflow collectors' IP addresses.
   Set the agent-interface (interface 3), polling at 15 seconds and sampling rate at 25 (1 in 25 packets will be sampled)
```
ops-as5712# configure terminal
ops-as5712(config)# sflow collector 10.10.11.2
ops-as5712(config)# sflow collector 10.10.12.2
ops-as5712(config)# sflow agent-interface 3
ops-as5712(config)# sflow polling 15
ops-as5712(config)# sflow sampling 25
```
6. Ping 100 packets between Host1 and the switch. sflowtool-1 and sflowtool-2 should be able to see FLOW packets & CNTR packets from the switch.
```
ping 10.10.10.1 -c 100 -i 0.01
```
### Test result criteria
#### Test pass criteria
When sflow is enabled, both sflow collectors receive sflow packets from the switch.
#### Test fail criteria
Any one or both collectors dont receive sflow packets from the switch.

sFlow Feature Test Cases
========================

## Contents

- [Global sFlow functionality](#global-sflow-functionality)
- [Multiple sFlow collectors](#multiple-sflow-collectors)
- [Sampling different types of packets](#sampling-different-types-of-packets)
- [Runtime configuration changes](#runtime-configuration-changes)
- [Changing agent interface](#changing-agent-interface)

## Global sFlow functionality
### Objective
This test verifies the global sFlow functionality on the switch.
### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/sflow/test_sflow_ft_functionality.py`
### Setup
#### Topology diagram
```ditaa
                    +----------------+
                    |                |
                    |                |
                    |   sflowtool    |
                    |                |
                    +-+--------------+
                      |
                      |
         +------------+--+
         |               |
         |               |
         |    Switch     |
         |               |
         |               |
         |               |
         +-+----------+--+
           |          |
           |          |
+----------+--+     +-+------------+
|             |     |              |
|             |     |              |
|  Host-1     |     |  Host-2      |
|             |     |              |
+-------------+     +--------------+
```
### Description
This test is used to ensure that the global sFlow feature works on OpenSwitch.

1. Connect Host-1 to the switch. Configure IP address and route.
    ```
    ip addr add 10.10.10.2/24 dev eth1
    ip route add 10.10.11.0/24 via 10.10.10.1
    ```

2. Connect Host-2 to the switch. Configure IP address and route.
    ```
    ip addr add 10.10.11.2/24 dev eth1
    ip route add 10.10.10.0/24 via 10.10.11.1
    ```

3. Connect another host which has sflowtool (the sFlow collector) to the switch. Configure an IP address on it.
    ```
    ip addr add 10.10.12.2/24 dev eth1
    ```

4. Configure the interfaces on the switch that are connected to these hosts.
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
    ops-as5712(config)#
    ```

5. Enable the global sFlow feature on the switch.
    ```
    ops-as5712(config)# sflow enable
    ```

6. Configure the collector IP address (attached to interface 2 of the switch).
   Set the agent-interface (interface 3) and the sampling rate at 20 (One in 20 packets are sampled)
    ```
    ops-as5712(config)# sflow collector 10.10.12.2
    ops-as5712(config)# sflow agent-interface 3
    ops-as5712(config)# sflow sampling 20
    ```

7. Ping between Host-1 and the switch (CPU destined traffic). The sflowtool is able to see FLOW packets from the switch.
    ```
    ping 10.10.10.1 -c 200 -i 0.1
    ```

8. Ping between Host-1 and Host-2 (Layer-3 traffic). The sflowtool is able to see FLOW packets from the switch.
    ```
    ping 10.10.11.2 -c 200 -i 0.1
    ```

9. Disable the global sFlow feature on the switch.
    ```
    ops-as5712(config)# no sflow enable
    ```

10. Ping again and check if the sflowtool does not receive the sFlow packets from the switch.

11. Enable sFlow again to test Layer-2 traffic.
    ```
    ops-as5712(config)# sflow enable
    ```

12. Add a new Layer-2 VLAN to the switch. Configure the interfaces connected to the hosts to become a part of this VLAN in access mode.
    ```
    ops-as5712(config)# vlan 10
    ops-as5712(config-vlan)# no shut
    ops-as5712(config-vlan)# exit
    ops-as5712(config)# interface 1
    ops-as5712(config-if)# no routing
    ops-as5712(config-if)# vlan access 10
    ops-as5712(config-if)# exit
    ops-as5712(config)# interface 2
    ops-as5712(config-if)# no routing
    ops-as5712(config-if)# vlan access 10
    ops-as5712(config-if)# exit
    ```

13. Reconfigure IP address on Host-2 to be on the same subnet as Host-1.
    ```
    ip addr del 10.10.11.2/24 dev eth1
    ip addr add 10.10.10.3/24 dev eth1
    ```

13. Ping between the hosts (Layer-2 traffic). The sflowtool is able to see FLOW packets from the switch.
    ```
    ping 10.10.11.2 -c 200 -i 0.1
    ```

### Test result criteria
#### Test pass criteria
- When sFlow is enabled, the sflowtool is able to see the sFlow packets that are sent from the switch.
- When sFlow is disabled, the sflowtool does not see any sFlow packets from the switch.
#### Test fail criteria
- When enabled, the sflowtool does not receive any sFlow packets from the switch.
- When disabled, the sflowtool is still able to receive the sFlow packets from the switch.

## Multiple sFlow collectors
### Objective
This test verifies that the multiple sFlow collector configuration works on the switch.
### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/sflow/test_sflow_ft_multiple_collectors.py`
### Setup
#### Topology diagram
```ditaa
+----------------+      +----------------+
|                |      |                |
|                |      |                |
|  sflowtool-3   |      |  sflowtool-2   |
|                |      |                |
+--------------+-+      +-+--------------+
               |          |
               |          |
             +-+----------+--+
             |               |
             |               |
             |    Switch     |
             |               |
             |               |
             |               |
             +-+----------+--+
               |          |
               |          |
       +-------+--+     +-+--------------+
       |          |     |                |
       |          |     |                |
       | Host     |     |  sflowtool-1   |
       |          |     |                |
       +----------+     +----------------+
```
### Description
This test is used to ensure that the sFlow feature on OpenSwitch works with multiple collectors.

1. Connect Host to the switch interface 1 and configure an IP address.
    ```
    ip addr add 10.10.10.2/24 dev eth1
    ```

2. Connect the sFlow collectors sflowtool-1,2 and 3 to the switch interfaces 2,3 and 4 respectively. Configure IP addresses on them.
    ```
    ip addr add 10.10.11.2/24 dev eth1
    ip addr add 10.10.12.2/24 dev eth1
    ip addr add 10.10.13.2/24 dev eth1
    ```

3. Configure the interfaces on the switch that are connected to the host and the sFlow collectors.
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
    ops-as5712(config)# interface 4
    ops-as5712(config-if)# ip address 10.10.13.1/24
    ops-as5712(config-if)# no shut
    ops-as5712(config-if)# exit
    ops-as5712(config)#
    ```

4. Enable the global sFlow feature on the switch.
    ```
    ops-as5712(config)# sflow enable
    ```

5. Configure the IP address of all three sFlow collectors.
   Set the agent-interface (interface 4) and the sampling rate at 20 (One in 20 packets are sampled)
    ```
    ops-as5712(config)# sflow collector 10.10.11.2
    ops-as5712(config)# sflow collector 10.10.12.2
    ops-as5712(config)# sflow collector 10.10.13.2
    ops-as5712(config)# sflow agent-interface 4
    ops-as5712(config)# sflow sampling 20
    ```

6. Ping between the Host and the switch. All the sFlow collectors should be able to see the FLOW packets from the switch.
    ```
    ping 10.10.10.1 -c 200 -i 0.1
    ```

### Test result criteria
#### Test pass criteria
- When sflow is enabled, all the sFlow collectors receive sFlow packets from the switch.
#### Test fail criteria
- When sFlow is enabled, none of the sFlow collectors receive sFlow packets from the switch.

## Sampling different types of packets
### Objective
This test verifies that the sFlow feature can sample different types of packets.
### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/sflow/test_sflow_ft_different_packets.py`
### Setup
#### Topology diagram
```ditaa
                    +----------------+
                    |                |
                    |                |
                    |   sflowtool    |
                    |                |
                    +-+--------------+
                      |
                      |
         +------------+--+
         |               |
         |               |
         |    Switch     |
         |               |
         |               |
         |               |
         +-+----------+--+
           |          |
           |          |
+----------+--+     +-+------------+
|             |     |              |
|             |     |              |
|  Host-1     |     |  Host-2      |
|             |     |              |
+-------------+     +--------------+
```
### Description
This test is used to ensure that the sFlow feature on OpenSwitch can sample different types of packets.

1. Connect Host-1 to the switch (interface 1). Configure IP and IPv6 addresses and routes.
    ```
    ip addr add 10.10.10.2/24 dev eth1
    ip route add 10.10.11.0/24 via 10.10.10.1
    ip addr add 2000::2/120 dev eth1
    ip route add 2002::0/120 via 2000::1
    ```

2. Connect Host-2 to the switch (interface 2). Configure IP and IPv6 addresses and routes.
    ```
    ip addr add 10.10.11.2/24 dev eth1
    ip route add 10.10.10.0/24 via 10.10.11.1
    ip addr add 2002::2/120 dev eth1
    ip route add 2000::0/120 via 2002::1
    ```

3. Connect the sflowtool (sFlow collector) to switch (interface 3). Configure an IP address on it.
    ```
    ip addr add 10.10.12.2/24 dev eth1
    ```

4. Configure the interfaces that are connected to the hosts and the sFlow collector on the switch.
    ```
    ops-as5712# configure terminal
    ops-as5712(config)# interface 1
    ops-as5712(config-if)# ip address 10.10.10.1/24
    ops-as5712(config-if)# ipv6 address 2000::1/120
    ops-as5712(config-if)# no shut
    ops-as5712(config-if)# exit
    ops-as5712(config)# interface 2
    ops-as5712(config-if)# ip address 10.10.11.1/24
    ops-as5712(config-if)# ipv6 address 2002::1/120
    ops-as5712(config-if)# no shut
    ops-as5712(config-if)# exit
    ops-as5712(config)# interface 3
    ops-as5712(config-if)# ip address 10.10.12.1/24
    ops-as5712(config-if)# no shut
    ops-as5712(config-if)# exit
    ops-as5712(config)#
    ```

5. Enable the global sFlow feature on the switch.
    ```
    ops-as5712(config)# sflow enable
    ```

6. Configure the sFlow collector IP address.
   Set the agent-interface (interface 3), polling interval at 15 seconds and sampling rate to 25 (one in 25 packets are sampled)
    ```
    ops-as5712(config)# sflow collector 10.10.12.2
    ops-as5712(config)# sflow agent-interface 3
    ops-as5712(config)# sflow polling 15
    ops-as5712(config)# sflow sampling 25
    ```

7. Ping between Host-1 and the switch. The sflowtool is able to see these CPU destined packets from the switch.
    ```
    ping 10.10.10.1 -c 100 -i 0.01
    ```

8. Ping (IPv4 and IPv6) between Host-1 and Host-2. The sflowtool is able to see these routed packets from the switch.
    ```
    ping 10.10.11.2 -c 100 -i 0.01
    ping6 2000::2 -c 100 -i 0.01
    ```

9. Ping jumbo packets between the hosts. The sflowtool is able to see these jumbo packets from the switch.
    ```
    ping 10.10.11.2 -M do -s 8972 -c 100 -i 0.01
    ```

10. Ping to a broadcast address from Host-1. The sFlow collector is able to see these broadcast packets from the switch.
    ```
    ping -b 10.10.10.255 -c 100 -i 0.01
    ```

11. Use the iperf tool and generate multicast traffic from Host-1. The sFlow collector is able to see these multicast packets from the switch.
    ```
    iperf -c 226.94.1.1 -u -T 32 -t 10 -i 1
    ```

12. Add a new Layer-2 VLAN to the switch. Configure the interfaces connected to the hosts to become a part of this VLAN in access mode.
    ```
    ops-as5712(config)# vlan 10
    ops-as5712(config-vlan)# no shut
    ops-as5712(config-vlan)# exit
    ops-as5712(config)# interface 1
    ops-as5712(config-if)# no routing
    ops-as5712(config-if)# vlan access 10
    ops-as5712(config-if)# exit
    ops-as5712(config)# interface 2
    ops-as5712(config-if)# no routing
    ops-as5712(config-if)# vlan access 10
    ops-as5712(config-if)# exit
    ```

13. Ping (IPv4 and IPv6) between the hosts. The sFlow collector is able to see these switched untagged packets from the switch.
    ```
    ping 10.10.11.2 -c 100 -i 0.01
    ping6 2000::2 -c 100 -i 0.01
    ```

14. Configure the interfaces to trunk VLAN mode on the switch to check if the tagged packets are also being sampled.
    ```
    ops-as5712(config)# interface 1
    ops-as5712(config-if)# no routing
    ops-as5712(config-if)# vlan trunk allowed 10
    ops-as5712(config-if)# exit
    ops-as5712(config)# interface 2
    ops-as5712(config-if)# no routing
    ops-as5712(config-if)# vlan trunk allowed 10
    ops-as5712(config-if)# exit
    ```

15. Configure a VLAN interface on Host-1 and configure an IP address on it.
    ```
    ip link add link eth1 name eth1.10 type vlan id 10
    ip addr add 100.10.10.2/24 dev eth1
    ```

16. Similarly, configure a VLAN interface on Host-2 and configure an IP address on it.
    ```
    ip link add link eth1 name eth1.10 type vlan id 10
    ip addr add 100.10.10.3/24 dev eth1
    ```

17. Ping between the hosts. The sFlow collector is able to see these tagged packets (with the correct VLAN ID) as FLOW packets from the switch.
    ```
    ping 100.10.10.3 -c 100 -i 0.01
    ```

### Test result criteria
#### Test pass criteria
- When sflow is enabled, all types of packets are sampled and sent to the sFlow collector.
#### Test fail criteria
- When sFlow is enabled, none of the packet types are seen in the sFlow collector.

## Runtime configuration changes
### Objective
This test verifies the runtime changes to the sFlow configuration on the switch.
### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/sflow/test_sflow_ft_runtime_config.py`
### Setup
#### Topology diagram
```ditaa
         +------------+--+
         |               |
         |               |
         |    Switch     |
         |               |
         |               |
         |               |
         +-+----------+--+
           |          |
           |          |
+----------+--+     +-+------------+
|             |     |              |
|             |     |              |
|  Host       |     | sflowtool    |
|             |     |              |
+-------------+     +--------------+

```
### Description
This test is used to ensure that the sFlow feature in OpenSwitch is able to react to runtime configuration changes.

1. Connect the Host to the switch and configure an IP address on it.
    ```
    ip addr add 10.10.10.2/24 dev eth1
    ```

2. Connect another host that has sflowtool (the sFlow collector) to the switch. Configure an IP address on it.
    ```
    ip addr add 10.10.11.2/24 dev eth1
    ```

3. Configure the interfaces which are connected to these two hosts.
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
    ```

4. Enable the global sFlow configuration on the switch.
    ```
    ops-as5712(config)# sflow enable
    ```

5. Configure the collector's IP address (attached to interface 2 of the switch). Set the agent-interface (interface 2).
    ```
    ops-as5712(config)# sflow collector 10.10.11.2
    ops-as5712(config)# sflow agent-interface 2
    ```

6. Set the sampling rate to 20 (One in 20 packets are sampled).
    ```
    ops-as5712(config)# sflow sampling 20
    ```

7. Ping between the Host and the switch. The sflowtool is able to see at least 60% of FLOW packets (taking into account randomness) from the switch.
    ```
    ping 10.10.10.1 -c 200 -i 0.1
    ```

8. Change the sampling rate to 10 (One in 10 packets are sampled).
    ```
    ops-as5712(config)# sflow sampling 10
    ```

9. Ping between the Host and the switch. The sflowtool is able to see twice the number of FLOW packets compared to previous result.
    ```
    ping 10.10.10.1 -c 200 -i 0.1
    ```

10. Set the polling interval to 15 seconds. The sflowtool is able to see at least 3 CNTR packets from the switch in 1 minute.
    ```
    ops-as5712(config)# sflow polling 15
    ```

11. Change the polling interval to 10 seconds. The sflowtool is able to see at least 5 CNTR packets from the switch in 1 minute.
    ```
    ops-as5712(config)# sflow polling 10
    ```

12. Set the header size to 128 bytes and ping from the host to the switch. The sflowtool is able to see FLOW packets with headers containing 128 bytes.
    ```
    ops-as5712(config)# sflow header-size 128
    ```

13. Change the header size to 256 bytes and ping from the host to the switch. The sflowtool is able to see FLOW packets with headers containing 256 bytes.
    ```
    ops-as5712(config)# sflow header-size 256
    ```

14. Set the max datagram size to 500 bytes and ping from the host to the switch. The sflowtool is able to see sFlow datagrams of 500 bytes.
    ```
    ops-as5712(config)# sflow max-datagram-size 500
    ```

15. Change the max datagram size to 1000 bytes and ping from the host to the switch. The sflowtool is able to see sFlow datagrams of 1000 bytes.
    ```
    ops-as5712(config)# sflow max-datagram-size 1000
    ```

### Test result criteria
#### Test pass criteria
- The sFlow feature is able to react dynamically to changing configurations.
#### Test fail criteria
- The sFlow feature does not react to dynamic changes in the sFlow configuration.

## Changing agent interface
### Objective
This test verifies that the configured agent interface is used by the sFlow packets.
### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/sflow/test_sflow_ft_agent_interface.py`
### Setup
#### Topology diagram
```ditaa
                    +----------------+
                    |                |
                    |                |
                    |   sflowtool    |
                    |                |
                    +-+--------------+
                      |
                      |
         +------------+--+
         |               |
         |               |
         |    Switch     |
         |               |
         |               |
         |               |
         +-+-------------+
           |
           |
+----------+--+
|             |
|             |
|  Host-1     |
|             |
+-------------+
```
### Description
This test is used to ensure that the agent interface configured is used by the OpenSwitch.

1. Connect Host-1 to the switch. Configure IP address and route.
    ```
    ip addr add 10.10.10.2/24 dev eth1
    ip route add 10.10.11.0/24 via 10.10.10.1
    ```

2. Connect another host which has sflowtool (the sFlow collector) to the switch. Configure an IP address on it.
    ```
    ip addr add 10.10.11.2/24 dev eth1
    ```

3. Configure the interfaces on the switch that are connected to these hosts.
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

4. Enable the global sFlow feature on the switch.
    ```
    ops-as5712(config)# sflow enable
    ```

5. Configure the collector IP address (attached to interface 2 of the switch).
   Set the agent-interface (interface 1) and the sampling rate at 20 (One in 20 packets are sampled)
    ```
    ops-as5712(config)# sflow collector 10.10.11.2
    ops-as5712(config)# sflow agent-interface 1
    ops-as5712(config)# sflow sampling 20
    ```

6. Ping between Host-1 and the switch. The sflowtool is able to see FLOW packets from the switch with the agent address 10.10.10.1 (IP address of interface 1).
    ```
    ping 10.10.10.1 -c 200 -i 0.1
    ```

7. Change the agent-interface to use interface 3.
    ```
    ops-as5712(config)# sflow agent-interface 3
    ```

8. Ping between Host-1 and the switch. The sflowtool is able to see FLOW packets from the switch with the new agent address as 10.10.12.1 (IP address of interface 3).
    ```
    ping 10.10.10.1 -c 200 -i 0.1
    ```

9. Remove the agent interface configuration.
   ```
   ops-as5712(config)# no sflow agent-interface
   ```

10. Ping between Host-1 and the switch. The sFlow datagram will use one of the IP addresses configured on the switch. The sflowtool is able to see FLOW packets with an agent IP address that is available on the switch.
    ```
    ping 10.10.10.1 -c 200 -i 0.1
    ```

### Test result criteria
#### Test pass criteria
- When sFlow is enabled, the agent IP address in the FLOW packets match the configured agent interface's IP address.
- When agent interface configuration is removed, the agent IP address in the FLOW packets must be one of the IP addresses on the switch.
#### Test fail criteria
- When sFlow is enabled, the agent IP address in the FLOW packets does not match the configured agent interface's IP address.
- When agent interface configuration is removed, the agent IP address in the FLOW packets does not match any of the IP addresses on the switch.

## Changing polling interval
### Objective
This test verifies that the configured polling interval is used by the sFlow packets.
### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/sflow/test_sflow_ft_agent_interface.py`
### Setup
#### Topology diagram
```ditaa
                    +----------------+
                    |                |
                    |                |
                    |   sflowtool    |
                    |                |
                    +-+--------------+
                      |
                      |
         +------------+--+
         |               |
         |               |
         |    Switch     |
         |               |
         |               |
         |               |
         +-+-------------+
           |
           |
+----------+--+
|             |
|             |
|  Host-1     |
|             |
+-------------+
```
### Description
This test is used to ensure that the polling interval configured is used by the OpenSwitch.

1. Connect Host-1 to the switch. Configure IP address and route.
    ```
    ip addr add 10.10.10.2/24 dev eth1
    ip route add 10.10.11.0/24 via 10.10.10.1
    ```

2. Connect another host which has sflowtool (the sFlow collector) to the switch. Configure an IP address on it.
    ```
    ip addr add 10.10.11.2/24 dev eth1
    ```

3. Configure the interfaces on the switch that are connected to these hosts.
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
    ```

4. Enable the global sFlow feature on the switch.
    ```
    ops-as5712(config)# sflow enable
    ```

5. Configure the collector IP address (attached to interface 2 of the switch).
   Set the agent-interface (interface 1) and the sampling rate at 20 (One in 20 packets are sampled)
   Set the polling interval to 10 seconds.
   ```
    ops-as5712(config)# sflow collector 10.10.11.2
    ops-as5712(config)# sflow agent-interface 1
    ops-as5712(config)# sflow sampling 20
    ops-as5712(config)# sflow polling 10
    ```

6. Ping between Host-1 and the switch. The sflowtool is able to see CNTR packets from the switch with the agent address 10.10.10.1 (IP address of interface 1) and atleast 2 if_index.
    ```
    ping 10.10.10.1 -c 200 -i 0.1
    ```

7. Change the polling interval to default(30 seconds).
    ```
    ops-as5712(config)# no sflow polling
    ```

8. Ping between Host-1 and the switch. The sflowtool is able to see CNTR packets from the switch with agent address 10.10.10.1(IP address of inte    rface 1) and atleast 2 if_index.
    ```
    ping 10.10.10.1 -c 200 -i 0.1
    ```

9. Check if number of counter packets with polling rate of 10 is greater than twice of the number with polling rate as 30 seconds.

### Test result criteria
#### Test pass criteria
- At least 2 interfaces must be present in the counter packets in both polling intervals.
- CNTR packets for 10 second polling interval must be greater than twice the number of counter packets with 30 second polling interval.
#### Test fail criteria
- When sFlow is enabled, the polling interval set does not match the polling interval in sflow show cli.
- The CNTR packets for polling interval 10 is less than twice the CNTR packets for polling interval 30.
- The CNTR packet has less than 2 interfaces.

#LACP
## Contents
[TOC]

## Overview <a id="lacpoverview"></a> ##
LACP is one method of bundling several physical interfaces to form one logical interface. LACP exchanges are made between actors and partners. An **actor** is the local interface in an LACP exchange. A **partner** is the remote interface in an LACP exchange. LACP is defined in IEEE 802.3ad, Aggregation of Multiple Link Segments.

- In **dynamic mode**, local LAGs are aware of partner switchs' LAGs. Interfaces configured as dynamic LAGs are designated as active or passive.
— **Active** interfaces initiate LACP negotiations by sending LACP PDUs when forming a channel with an interface on the remote switch.
— **Passive** interfaces participate in LACP negotiations initiated by remote switch, but not allowed to initiate such negotiations.

- In **static mode**, switches create LAGs without awareness of their partner switch's LAGs. Packets may drop when  LAG static aggregate configurations differ between switches. The switch aggregates static links without LACP negotiation.

## Prerequisites <a id="lacppre"></a> ##
All the DUT interfaces (at least the interfaces that are connected to other devices) must be administratively up.

## Configuring LACP<a id="lacpconf"></a> ##
###Creating and adding interfaces to LAG <a id="lacpconfbasic"></a> ###
1. Configure the terminal to change the vtysh context to config context with the following commands:
```
ops-as5712# configure terminal
ops-as5712(config)#
```

2. Create LAG with the following command:
```
ops-as5712(config)# interface lag 100
ops-as5712(config-lag-if)#
```
After creating the LAG, CLI drops to LAG interface context and allows user to configure LAG specific parameters.

3. Add interfaces to LAG.
Maximum 8 physical interfaces can be added to a LAG. Configure the terminal to change the context to interface context and then add interface to LAG.
```
ops-as5712(config)# interface 1
ops-as5712(config-if)# lag 100
ops-as5712(config-if)#
```

###Removing interfaces and deleting LAG <a id="lacpconfbasic2"></a> ###
1. Configure the terminal to change the vtysh context to config context with the following commands:
```
ops-as5712# configure terminal
ops-as5712(config)#
```

2. Delete LAG with the following command:
```
ops-as5712(config)# no interface lag 100
```
After deleting the LAG, the interfaces associated with the LAG behaves as L3 interfaces.

3. Remove interfaces from LAG.
```
ops-as5712(config)# interface 1
ops-as5712(config-if)# no lag 100
ops-as5712(config-if)#
```

###Setting up LACP global parameters<a id="lacpconfglobal"></a> ###

1. Setting the LACP **system priority**.
```
ops-as5712(config)# lacp system-priority 100
ops-as5712(config)#
```
The `no lacp system-priority` commands reverts the LACP system-priority to its default value of 65534.
```
ops-as5712(config)# no lacp system-priority
ops-as5712(config)#
```
In LACP negotiations, link status decisions are made by the system with the numerically lower priority.

###Setting up LAG parameters<a id="lacplagconf"></a> ###

1. Setting the **LACP mode**.
LACP mode takes values **active**, **passive** and **off**.  Default is **off**
Following commands sets lacp mode to active, passive and off respectively.
```
ops-as5712(config-lag-if)# lacp mode active
ops-as5712(config-lag-if)# lacp mode passive
ops-as5712(config-lag-if)# no lacp mode {active / passive}
```
2. Setting the **hash** type.
LACP hash type takes value **l2-src-dst** or **l3-src-dst** to control the selection of a interface from a group of aggregate interfaces with which to transmit a frame.
Default hash type is **l3-src-dst**.
```
ops-as5712(config-lag-if)# hash l2-src-dst
no form of 'hash l2-src-dst' sets the hash type to l3-src-dst.
ops-as5712(config-lag-if)# no hash l2-src-dst
```

3.  Setting the **LACP rate**.
LACP rate takes values **slow** and **fast**. By default **slow** is used.
When configured to be **fast** LACP heartbeats are requested at a rate of once per second causing connectivity issues to be detected more quickly. In **slow** mode, heartbeats are requested at a rate of once every 30 seconds.

```
ops-as5712(config-lag-if)# lacp rate fast
no form of 'lacp rate fast' sets the rate to slow.
ops-as5712(config-lag-if)# no lacp rate fast
```

###Setting up interface LACP parameters<a id="lacpintfconf"></a> ###

1. Setting the **LACP port-id**.
LACP port-id is used in LACP negotiations to identify individual ports participating in aggregation.
LACP port-id takes values in the range of 1 to 65535.
```
ops-as5712(config-if)# lacp port-id 100
```

2. Setting the **LACP port-priority**.
LACP port-id is used in LACP negotiations. In LACP negotiations interfaces with numerically lower priorities are preferred for aggregation.
LACP port-priority takes values in the range of 1 to 65535.
```
ops-as5712(config-if)# lacp port-priority 100
```

3. Setting the **LACP port-priority**.
LACP port-id is used in LACP negotiations. In LACP negotiations interfaces with numerically lower priorities are preferred for aggregation.
LACP port-priority takes values in the range of 1 to 65535.
```
ops-as5712(config-if)# lacp port-priority 100
```

###Verifying the configuration <a id="lacpdisplayconf"></a> ###
#####Viewing LACP global information
The `show lacp configuration` command displays global LACP configuration information.
```
ops-as5712# show lacp configuration
System-id       : 70:72:cf:ef:fc:d9
System-priority : 65534
```

#####Viewing LACP aggregate information
The `show lacp aggregates` command displays information about all LACP aggregates.

```
ops-as5712# show lacp aggregates
Aggregate-name          : lag100
Aggregated-interfaces   :
Heartbeat rate          : slow
Fallback                : false
Hash                    : l3-src-dst
Aggregate mode          : off

>Aggregate-name         : lag200
Aggregated-interfaces   :
Heartbeat rate          : slow
Fallback                : false
Hash                    : l3-src-dst
Aggregate mode          : off
```
The `show lacp aggregates [lag-name]` command displays information about specified LAG.

```
ops-as5712# show lacp aggregates lag100
Aggregate-name          : lag100
Aggregated-interfaces   :
Heartbeat rate          : slow
Fallback                : false
Hash                    : l3-src-dst
Aggregate mode          : off
```

#####Viewing LACP interface details
The `show lacp interfaces` command displays LACP interface configuration.

```
ops-as5712# show lacp interfaces
State abbreviations :
A - Active        P - Passive      F - Aggregable I - Individual
S - Short-timeout L - Long-timeout N - InSync     O - OutofSync
C - Collecting    D - Distributing
X - State m/c expired              E - Default neighbor state
.
Actor details of all interfaces:
\-------------------------------------------
Intf-name    Key    Priority   State
\-------------------------------------------
Aggregate-name : lag100
1                   500
Aggregate-name : lag200
3
4
2
.
Partner details of all interfaces:
\-------------------------------------------------
Intf-name    Partner  Key    Priority   State
             port-id
\-------------------------------------------------
Aggregate-name : lag100
1                            500
Aggregate-name : lag200
3
4
2
```

## CLI <a id="lacpcli"></a> ##
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here](https://openswitch.net/cli_feat.html#cli_command_anchor) for the CLI commands related to the LACP feature.
## Related features <a id="lacprelated"></a> ##
When configuring the switch for LACP, it might also be necessary to configure [Physical Interface](https://openswitch.net./tbd/other_filefeatures/related_feature1.html#first_anchor) .

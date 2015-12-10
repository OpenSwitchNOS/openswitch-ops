# Source Interface Selection

## Contents

- [Overview](#overview)
- [Configuring the source-interface](#configuring-the-source-interface)
- [Verifying the configuration](#verifying-the-configuration)
	- [Viewing source-interface information](#viewing-source-interface-information)
	- [Viewing snapshot of active configurations](#viewing-snapshot-of-active-configurations)
- [Related features](#related-features)

## Overview

Source Interface Selection is used to set the IP address of an interface or IP address defined interafce as the source interface for tftp protocol or all the specified protocols.

Syntax:
ip source-interface <protocol-ID | all>  <interface <id>| address<ip-address>>

[no] ip source-interface <protocol-ID | all>
show  ip source-interface [tftp]


Explanation of Parameters:

protocol-ID : Which specifies the  different software applications like telnet, tftp, radius, sflow etc. we can specify different source ips for different apps by using protocol-ID

all : To specify same source ip for all applications.

address : To set the IP address of an interface as the source IP.

interface : To set an interface as the source interface.

Examples:
## Configuring the source-interface

1.Configuring a source-interface IP address to TFTP protocol

ops-as5712(config)# ip source-interface tftp address 1.1.1.1

2.Configuring a source-interface IP address to all the specified protocols

ops-as5712(config)# ip source-interface all address 1.1.1.1

3. Configuring a source-interface to TFTP protocol

ops-as5712(config)# ip source-interface tftp interface 1

4. Configuring a source-interface to all the specified protocols

ops-as5712(config)# ip source-interface all interface 1

5.Unconfiguring a source-interface to TFTP protocol

ops-as5712(config)# no ip source-interface tftp

6.Unconfiguring a source-interface to all the specified protocols

ops-as5712(config)# no ip source-interface all

## Verifying the configuration
### Viewing source-interface information

1.Verifying source-interface to TFTP protocol

ops-as5712# show ip source-interface tftp

Source-interface Configuration Information

Protocol        Source Interface
--------        ----------------
tftp            1.1.1.1

2.Verifying source-interface to all the specified protocols

ops-as5712# show ip source-interface

Source-interface Configuration Information

Protocol        Source Interface
--------        ----------------
tftp            1.1.1.1

3.Verifying Unconfig source-interface to TFTP protocol

ops-as5712# show ip source-interface tftp

Source-interface Configuration Information

Protocol        Source Interface
--------        ----------------
tftp

4.Verifying Unconfig source-interface to all the specified protocols

ops-as5712# show ip source-interface

Source-interface Configuration Information

Protocol        Source Interface
--------        ----------------
tftp


### Viewing snapshot of active configurations.
ops-as5712# show ip source-interface

Source-interface Configuration Information

3rotocol        Source Interface
--------        ----------------
tftp            1.1.1.1


ops-as5712# show running-config interface
Current configuration:
!
!
!
interface 1
    no shutdown
    ip address 1.1.1.1/24
source interface
    1.1.1.1

## Related features
No related features.
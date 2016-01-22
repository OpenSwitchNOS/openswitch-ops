# Show Tech Commands
## Contents

- [Configuration Commands](#configuration-commands)
- [Display Commands](#display-commands)
    - [Commands Summary](#commands-summary)
    - [Show Tech](#show-tech)
        - [Syntax](#syntax)
        - [Description](#description)
        - [Authority](#authority)
        - [Examples](#examples)
    - [Show Tech List](#show-tech-list)
        - [Syntax](#syntax)
        - [Description](#description)
        - [Authority](#authority)
        - [Parameters](#parameters)
        - [Examples](#examples)
    - [Show Tech Feature](#show-tech-feature)
        - [Syntax](#syntax)
        - [Description](#description)
        - [Authority](#authority)
        - [Parameters](#parameters)
        - [Examples](#examples)
    - [Help Text](#help-text)
        - [Example](#example)

## Configuration Commands
We don't have any configuration command as part of Show Tech.
##Display Commands
### Commands Summary
| Command | Usage |
|:--------|:----------|
| **show tech** | Runs show tech for all supported features |
| **show tech list**| Lists all the supported show tech features |
| **show tech FEATURE**| Runs show tech for the feature specified |
| **show tech FEATURE SUBFEATURE**|Runs show tech for the sub feature specified|


### Show Tech
#### Syntax
`show tech`
#### Description
Runs show tech command for all the supported features.
#### Authority
All users
#### Examples

```
ops-as5712# show tech
===========================
Feature system begins
===========================

------------------------------
command : show version
------------------------------

Quagga 0.99.24.1 (switch).
Copyright 1996-2005 Kunihiro Ishiguro, et al.
configured with:
    --build=x86_64-linux --host=x86_64-openswitch-linux --target=x86_64-openswitch-linux --prefix=/usr --exec_prefix=/usr --bindir=/usr/bin --sbindir=/usr/sbin --libexecdir=/usr/lib/ops-cli --datadir=/usr/share --sysconfdir=/etc --sharedstatedir=/com --localstatedir=/var --libdir=/usr/lib --includedir=/usr/include --oldincludedir=/usr/include --infodir=/usr/share/info --mandir=/usr/share/man --disable-silent-rules --disable-dependency-tracking --with-libtool-sysroot=/ws/ramakdin/ops-vsi/build/tmp/sysroots/genericx86-64 --enable-user=root --enable-group=root --enable-ovsdb --enable-vtysh

------------------------------
command : show system
------------------------------

OpenSwitch Version  : 0.3.0 (Build: developer_image)
Product Name        : OpenSwitch

Vendor              : OpenSwitch
Platform            : Generic-x86-64
Manufacturer        : OpenSwitch
Manufacturer Date   : 09/01/2015 00:00:01

Serial Number       : X8664001            Label Revision      : L01
```

Output is truncated for readability

### Show Tech List
#### Syntax
`show tech list`
#### Description
This command lists all the supported show tech features and sub-features.
#### Authority
All users
#### Parameters
None
#### Examples

```
ops-as5712# show tech list
Show Tech Supported Features List

------------------------------------------------------------
Feature  SubFeature        Desc
------------------------------------------------------------
system                      Show Tech system

lldp                       Link Layer Discovery Protocol

         configuration     LLDP Configuration

         statistics        LLDP Statistics

         neighbor-info     LLDP Neighbor Info

```

### Show Tech Feature
#### Syntax
`show tech FEATURE [SUBFEATURE]`
#### Description
This command runs the show tech for the feature or subfeature specified.
#### Authority
All users
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| **FEATURE** | Required | Feature Name (String) | Feature name as displayed in the show tech list |
| **SUBFEATURE** | Optional | Sub Feature Name (String) | Sub Feature name as displayed in the show tech list |
#### Examples

```
ops-as5712# show tech system
switch# show tech system
====================================================
Feature system begins
====================================================

---------------------------------
Command : show version
---------------------------------
Quagga 0.99.24.1 (switch).
Copyright 1996-2005 Kunihiro Ishiguro, et al.
configured with:
    --build=x86_64-linux --host=x86_64-openswitch-linux --target=x86_64-openswitch-linux --prefix=/usr --exec_prefix=/usr --bindir=/usr/bin --sbindir=/usr/sbin --libexecdir=/usr/lib/ops-cli --datadir=/usr/share --sysconfdir=/etc --sharedstatedir=/com --localstatedir=/var --libdir=/usr/lib --includedir=/usr/include --oldincludedir=/usr/include --infodir=/usr/share/info --mandir=/usr/share/man --disable-silent-rules --disable-dependency-tracking --with-libtool-sysroot=/ws/ramakdin/ops-vsi/build/tmp/sysroots/genericx86-64 --enable-user=root --enable-group=root --enable-ovsdb --enable-vtysh
---------------------------------
Command : show system
---------------------------------
OpenSwitch Version  : 0.3.0 (Build: developer_image)
Product Name        : OpenSwitch

Vendor              : OpenSwitch
Platform            : Generic-x86-64
Manufacturer        : OpenSwitch
Manufacturer Date   : 09/01/2015 00:00:01

Serial Number       : X8664001            Label Revision      : L01

ONIE Version        : 2014.08.00.05       DIAG Version        : 1.0.0.0
Base MAC Address    : 70:72:cf:07:d2:e3   Number of MACs      : 74
Interface Count     : 78                  Max Interface Speed : 40000 Mbps


switch# show tech lldp configuration
====================================================
Feature lldp begins
====================================================

= = = = = = = = = = = = = = = = = = = = = = = = = = =
Sub Feature configuration begins
= = = = = = = = = = = = = = = = = = = = = = = = = = =

---------------------------------
Command : show lldp configuration
---------------------------------
LLDP Global Configuration:

LLDP Enabled :No
LLDP Transmit Interval :30
LLDP Hold time Multiplier :4

TLVs advertised:
Management Address
Port description
Port VLAN-ID
Port Protocol VLAN-ID
Port VLAN Name
Port Protocol-ID

```

### Help Text
| Command | Help Text |
|:--------|:----------|
| **show tech** | Run show tech for all supported features |
| **show tech list**| List all the supported show tech features |
| **show tech FEATURE**| Run show tech for the feature specified |
| **show tech FEATURE SUBFEATURE**|Run show tech for the sub feature specified|

#### Example

```
switch# show tech ?
  <cr>
  FEATURE  Run show tech for the feature specified
  list     List all the supported show tech features

switch# show tech system  ?
  <cr>
  [SUBFEATURE]  Run show tech for the sub feature specified

switch# show tech lldp configuration ?
  <cr>

switch# show ?
  (other commands are ommited for simplicity)
  tech              Run show tech for all supported features
```

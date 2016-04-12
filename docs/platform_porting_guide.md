#Platform

## Contents

- [Contents](#contents)
- [Overview](#overview)
- [ADD CONFIGURATION FOR A DEVICE](#add-configuration-for-a-device)
- [HARDWARE DESCRIPTION FILES](#hardware-description-files)
- [SUPPORT NEW CONNECTOR TYPE](support-new-connector-type)
- [ADDING A BINARY TO OPENSWITCH](#adding-a-binary-to-openswitch)
- [OPENSWITCH PLUGIN FOR PLATFORM OR ASIC](#openwitch-plugin-for-platform-or-asic)

## Overview
This document can be used by platform vendors to port a new platform to OpenSwitch.

### ADD CONFIGURATION FOR A DEVICE:
Before building OpenSwitch the target platform needs to be configured. This is done by “make configure platform_name” . To add a new platform to the ops-build:
Create platform target (meta-platform-openswitch-<platform-name>) corresponding to the new platform. This code belongs to:
a)	repository “openswitch/ops-build”
b)	In the OpenSwitch sandbox look here: $ <work_dir>/yocto/openswitch

References:
In the OpenSwitch sandbox, refer:
1)	[yocto/openswitch/meta-platform-openswitch-as6712](http://git.openswitch.net/cgit/openswitch/ops-build/tree/yocto/openswitch/meta-platform-openswitch-as6712?id=6eb61667d36816a9a94aeb04f67b1c8efd58 "meta-platform-openswitch-as6712")
2)	https://review.openswitch.net/#/c/1766/ this commit has changes made to add AS6712

### HARDWARE DESCRIPTION FILES
To add the hardware description file support for the new platform add files in [openswitch/ops-config-yaml](http://git.openswitch.net/cgit/openswitch/ops-config-yaml/) in the directory vendor_name/platform_name

References:
In the OpenSwitch sandbox, refer repository [openswitch/ops-config-yaml](http://git.openswitch.net/cgit/openswitch/ops-config-yaml/) :
1) [Accton/AS6712-32X](http://git.openswitch.net/cgit/openswitch/ops-hw-config/tree/Accton/AS6712-32X)
3) [README.md](http://git.openswitch.net/cgit/openswitch/ops-hw-config/tree/README.md)




### SUPPORT NEW CONNECTOR TYPE
OpenSwitch supports different connectors. For e.g. CR4, SR4 , etc.
To add a new connector type modify corresponding:
1. Changes to header files.
2. Handle conditions (parsing functions and if & switch cases) for the new connector.
To add support for new connector types refer the following repositories:
1. [openswitch/ops-intfd](http://git.openswitch.net/cgit/openswitch/ops-intfd/)
    a.	intfd.h
    b.	intfd_ovsdb_if.c
    c.	intfd_utils.c
2. [openswitch/ops-openvswitch](http://git.openswitch.net/cgit/openswitch/ops-openvswitch/)
    a.	openswitch-idl.h
3. [openswitch/ops-pmd](http://git.openswitch.net/cgit/openswitch/ops-pmd/)
    a.	plug.h
    b.	pmd.h
    c.	plug.c
    d.	pm_detect.c

Note that the above file list is just a reference and the changes are not limited to the files in the list.

### ADDING A BINARY TO OPENSWITCH
If the new platform needs to add  binary for proprietary code from vendor then it can be included by listing the location of the file in a bit bake file.

For e.g. for the AS6712 or AS5712 platforms, OpenSwitch uses platform specific binaries for the platform. To use the point to a custom binary file locally:
1) In the file:  yocto/openswitch/meta-distro-openswitch/recipes-asic/opennsl/opennsl-cdp_3.0.0.2.bb :
Change the SRC_URI path to the local path of the tarball file. For e.g. for AS6712:
SRC_URI = "file:///home/username/download/opennsl-3.0.0.2-cdp-as6712.tar.bz2 \ "
2) make (build OpenSwitch)


### OPENSWITCH PLUGIN FOR PLATFORM OR ASIC

The OpenSwitch switchd plugin is the platform specific driver that calls into ASIC SDKs. Every ASIC platform would need to implement its own plugin layer. The plugin is a dynamically loaded library during runtime using lib “ldl”. ops-switchd looks for the following location for the plugins:
usr/lib/openvswitch/plugins/

The platform independent switchd calls into switchd plugin using standard interfaces which are defined in two different layers, the netdev layer and the ofproto layer.
Netdev layer: This layer is responsible for configuring physical layer configurations into ASIC which correspond to the Interface Table in OVSDB, such as speed, mtu, duplex, admin state. The layer also reports back transmit and receive statistics of the interface from the hardware. There are multiple netdev classes defined in the plugin, with each class representing a different type of interface:

1) system:  Physical front panel ports in the platform
2) internal: Internal logical interfaces such as bridge interface and Switch Virtua Interfaces (SVI)  for inter VLAN routing
3) loopback: Layer 3 loopback interfaces
4) subinterface: Layer 3 subinterfaces to divide a physical interface into multiple virtual interfaces using dot1q VLAN tagging.
Functions, with different implementations if needed, are registered for each of the classes.
The opennsl plugin implantation for this layer is a good reference:
https://git.openswitch.net/cgit/openswitch/ops-switchd-opennsl-plugin/tree/src/netdev-bcmsdk.c
Ofproto layer: This layer is responsible for configuring all logical layer configurations into ASIC   which correspond to the Port Table in OVSDB, such as LAG, VLAN, IP addresses, neighbors, routes.
bundle_set is the interface that is called for any Port Table changes. Other functions to support layer 3 configurations are also registered by the ofproto layer.
The opennsl plugin implantation for this layer is a good reference:
https://git.openswitch.net/cgit/openswitch/ops-switchd-opennsl-plugin/tree/src/ofproto-bcm-provider.c

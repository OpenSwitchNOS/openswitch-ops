Pluggable Modules
=================

 [TOC]
 
## Overview ##
Pluggable modules, including SFP, SFP+ and QSFP+ transceiver modules allow a network designer to select from several physical transports instead of having a fixed copper or optical transceivers. Direct Attach Copper cables (DACs) may be used toi connect two SFP+ (or QSFP+) ports without dedicated transceivers over relatively short distances, while optical transceivers may support distances of multiple kilometers.

SFP modules support speeds up to 1Gb, while SFP+ modules support 10Gb line rate.

QSFP+ modules include 40Gb DAC modules, 40Gb optical transceivers, and 10Gb 4X transceiver (which splits the four lanes of the QSFP+ module into individual interfaces).

## External references ##
[Small Formfactor Pluggable](https://en.wikipedia.org/wiki/Small_form-factor_pluggable_transceiver "Wikipedia")
[Direct Attach](https://en.wikipedia.org/wiki/10_Gigabit_Ethernet#SFP.2B_Direct_Attach "Wikipedia")
[Quad Small Formfactor Pluggable](https://en.wikipedia.org/wiki/QSFP "Wikipedia")

## How to use the feature ##

###Setting up the basic configuration

 1. Refer to switch manufacturer documentation to determine available receptical types and supported module variants.
 1. Insert the module(s) in the recepticals, and attach cables between module in switch and module in server, switch, or other network device.
 1. Configure interfaces for operation.

Note that for QSFP modules that split a connector into multiple separate interfaces, additional configuration is required. There is no industry standard defined for detecting split QSFP modules, so you must configure the interface to identify the QSFP as split. 

###Verifying the configuration

 1. Display the pluggable module information using the '''show interface transceiver''' command.

###Troubleshooting

#### Condition 
The SFP, SFP+, or QSFP+ is not detected.
##### Cause 
The module may not be properly seated in the receptical.
###### Remedy  
Check that the module is inserted with the correct orientation, and established good mechanical interlock with the receptical.
##### Cause
The module is not inserted in the correct slot.
###### Remedy
Verify that the module is inserted in the correct receptical.
#### Condition
The interface will not establish link.
##### Cause
The interface is not configured properly.
###### Remedy
Refer to interface documentation.
##### Cause
The module is not present or is not fully inserted.
###### Remedy
Verify that the module is present and properly inserted in the receptical.
##### Cause
The cable (optical or copper) is not attached to the module.
###### Remedy
Attach the cable.
##### Cause
The remote end of the cable or module is not properly connected to the remote device.
###### Remedy
Attach cable and module to remote device.
##### Cause
The remote device is not configured to establish link.
###### Remedy
Configure remote device to enable interface.
##### Cause
The remote module is not the same variant (incompatible technologies).
###### Remedy
Only use compatible module types at either end of a network connection.

## CLI ##
Click [here](https://openswitch.net/cli_feature_name.html#cli_command_anchor) for the CLI commands related to interfaces and pluggable modules.

## Related features ##
See also, [Interface](https://openswitch.net/interface_user_guide.html) for information on configuring physical interfaces.

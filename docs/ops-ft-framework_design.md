Test Framework - opstestfw Library Design
=================

## Introduction
This document will discuss the design of the opstestfw library modules.  This framework is used to develop component and feature level tests for the OpenSwitch project.

The opstestfw library module is comprised of core objects that are discussed in the "Framework Objects" section below.  This will discuss what the core objects are and how they are inter-related to each other.  Another core aspect of this module is the concept of topology.  This is described in the "Topology" section below.  

Another important aspect of the opstestfw library module is the concept of "Helper Libraries" and how they relate to the objects.  THis is duscussed in the "Helper Library" section.

## Framework Objects
The framework has some core object.  This section will describe their key function and describe how to use them.  It is important to know the hierarchy of the objects to be successful with working with them.

### The testEnviron Object
This object is the first object created in the test suite.  This object will do the following...

 - Create the logging structure for the suite. By default, this will create a log structure in /tmp/opsTest-results.  Each test run will have an individual date stamp directory under the main results directory.
 - Figure out topology specifications and instantiate the topology object.
 - The topology object is a member of this class.

 As mentioned in the Pytest setup_class section, the testEnviron object needs to be defined in the setup_class method.

### The Topology Object
The topology object is instantiated and is stored within the testEnviron object.  This is actually created in setup_class.

The topology code will build and map the topology.  This will also create all device objects and enable those objects to create interactive connects wit the devices.  One of the most important tasks the Topology object performs is the create and populate the linkPortMapping dictionary for each device.

### Device Objects
The device objects are stored within the topology objects.  The device object contains connection information and objects for the device.  This objects has methods to interact with the device and error check the transaction with the device.  The device object also contains the linkPortMapping dictionary that maps a physical port to a logical link for the device.  If you wanted to get the port of a switch that is connected over lnk01, you would reference it as dut01Obj.ilnkPortMapping['lnk01'].

The device object is the object that will be passed into the helper library functions.  The device object enables the helper libraries to interact with the device.

### The returnStruct Object
The helper libraries and many object methods will return the returnStruct object to the calling process.  Helper libraries or class methods will create this object and return it to the calling routine.
The returnStruct object provides consistency in library returns and gives  standard methods for pulling values out of the return structure.  
Arguments to this class are: returnCode, buffer, and data (data can be either a value or a dictionary).  Methods to retrieve data…

 - returnCode()  gets he returnCode for the library called.
 - buffer() returns the raw buffer if one is given to the object on creation.
 - dataKeys() gives top level dictionary keys of the data stored
 - valueGet(key=)  If no key is given, just returns data.  If a key is
   given, will return the value for the key in the dictionary
   retValueString()  method to return a JSON string of the returnCode,
   buffer and data
   printValueString()  same as retValueString, but prints the JSON string


## Topology
Each test case must have a "topoDict" dictionary defined.  This dictionary describes the way the topology is configured.  Below is an example topology.
```
topoDict = {"topoTarget": "dut01",
			"topoDevices": "dut01 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,lnk02:dut01:wrkston02",
            "topoFilters": "dut01:system-category:switch,dut02:system-category:switch"}

```
The names used in the dictionary values should follow this notation..

 - **Switches**:  These should be named "dut0x",  If I have a two switch topology I would call these switches logically dut01 and dut02.
 - **Workstations / Hosts**:  These should be named "wrkston0x".  If I have three workstations in the topology, these should be referred to as wrkston01, wrkston02, and wrkston03.
 - **Links**:  Links aer connections between two entities and should be named in the following way, lnk0x.  If I have three links in my topology they should be named lnk01, lnk02, and lnk03 respectively.

Below is a description of the topoDict key / value pairs.

 - **topoTarget**:  This is identifying in the topology (switches) that will install the build under test.  If I have three switches in the topology, the value would look like "dut01 dut02 dut03".
 - **topoDevices**:  This identifies all the logical devices in the topology.  If I have two switches and three workstations in my topology the value of this would look like "dut01 dut02 wrkston01 wrkston02 wrkston03".
 - **topoLinks**:  This defines the links for the topology and specifies the entities that the link interconnects.  The link definition is delimited by the ":" character.  The notation of a link definition statement is linkname:device1:device2.  Multiple links are delimited by the "," character.  If I had 3 links defined the statement might look like "lnk01:dut01:wrkston01,lnk02:dut01:wrkston02,lnk03:dut01:dut02".  This example states that "lnk01" is a connection between dut01 and wrkston01, "lnk02" is a connection between dut01 and wrkston02, and "lnk03" is a connection between dut01 and dut02.
 - **topoFilters**:  This gives base definition of what each device is.  This is in the form of  "device":"attribute":"value".  The one attribute that is currently accepted today is "system-category" and the value of this is either switch or workstation.
 - **topoLinkFilter**:  This is a filter on the link that can add requirements to a specific link.  For example, if we want to make sure a port is connected to a specific port on the switch you would add it in the following notation <lnkName>:<device>:interface:<interfaceName>
"topoLinkFilter": "lnk01:dut01:interface:eth0" - this makes sure that lnk01 port on dut01 is over eth0.  This topology key is optional.



## Helper / Utiilty Libraries
Helper and utility libraries are used for performing certain functions like enabling an interface, configure or unconfigure a feature.  Currently the framework packages up these libraries in the opstestfw.host package for any host specific libraies and the opstestfw.switch.CLI package for switch CLI libraries.

## Supporting Documentation
Please refer to the "Writing a Feature Test Case" document that describes the core pieces of the test case.  This document will help get you started on creating automated test cases for OpenSwitch.
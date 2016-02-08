Web User Interface
==================
OpenSwitch Web User Interface (UI)

# Overview
The OpenSwitch web UI provides an easy-to-see visual representation displaying the state of the switch.  Easy to use view and configuration screens help the user understand and configure complex features.

# Accesing Web UI
To access the web UI, bring up a browser (Chrome preferred) and enter the IP address of the switch management interface.

# Screens


##Login
When accessing the switch web UI, the first screen that appears is the login screen.  The login is tied to a user account that has been added to the switch via the CLI `useradd` command.

##Overview
The Overview screen displays important information and statistics about the switch.

###System
The system panel includes the product name, serial number, vendor, version, and base MAC address.

###Hardware
The hardware panel shows the status of the power suupplies, temperatures and fans.

###Features
The features panel includes a list of switch features and their current state (enabled or disabled).  Also included is a list of the total number of VLANs configured on the switch, number of interefaces and MTU.

###Traffic
The trafic panel displays the ports with the top utilization (transmite or receive).  The list automatically sorts, moving the port with the top utliization percentage to the top.  Clicking the graph icon at the top of the gauge takes you to the Interfaces Monitor screen, displaying details for the top interface.

###Logs
The logs panel displays the last system log messages.

##Interfaces

##VLANs

##LAGs

##Logs

##Quick Guides

##Links

###REST API
The Swagger UI link opens a new window/tab in the browser and displays the Swagger UI:  http://api.openswitch.net/rest/dist/index.html

###OpenSwitch.net
The OpenSwitch.net link opens a new window/tab in the browser and displays the OpenSwitch web site:  http://openswitch.net

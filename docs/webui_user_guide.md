OpenSwitch Web User Interface (UI)
==================

#Contents
- [Overview](#overview)
- [Accesing Web UI](#accesing-web-ui)
- [Screens](#screens)
	- [Login](#login)
	- [Overview](#overview)
		- [System](#system)
		- [General](#general)
		- [Hardware](#hardware)
		- [Top Interface Utilization](#topinterfaceutilization)
		- [Logs](#logs)
	- [Interfaces](#interfaces)
	- [LAGs](#lags)
		- [Add LAG](#addlag)
			- [ID & Interfaces](#id&interfaces)
			- [Attributes](#attributes) 
		- [Remove LAG](#removelag)
		- [Edit LAG](#editlag)
	- [ECMP](#ecmp)
		- [Edit ECMP](#editecmp)
	- [Log](#log)
	- [Quick Guides](#quick-guides)
	- [Links](#links)
		- [REST API](#rest-api)
		- [OpenSwitch.net](#openswitchnet)


# Overview
The OpenSwitch web UI provides an easy-to-see visual representation displaying the state of the switch. Easy to use view and configuration screens help the user to understand and configure complex features.

# Accesing Web UI
To access the web UI, bring up a web browser (Google Chrome preferred) and enter the IP address of the switch management interface.

# Screens


## Login
When accessing the switch web UI, the first screen that appears is the login screen. The login is tied to a user account that has been added to the switch via the CLI `useradd` command.

## Overview
The Overview screen displays important information and statistics about the switch.

### System
The system panel includes information about the switch, such as:
- the product name
- serial number
- vendor
- version
- ONIE Version
- base MAC address

### General
The features panel includes:
- a listing of the switch features and their current state (enabled or disabled)
- number of VLANs configured on the switch
- number of interfaces on the switch
- the maximum transmission unit (MTU)
- the Max Interface Speed

### Hardware
The hardware panel shows the status of:
- the power supplies
- temperatures
- fans

### Top Interface Utilization
The Top Interface Utilization panel displays the ports with the top utilization (transmit or receive). The list automatically sorts, moving the port with the top utliization percentage to the top. Clicking the graph icon at the top of the gauge takes you to the Interfaces Monitor screen, displaying details for the top interface.

### Log
The log panel displays the last system log messages.

## Interfaces
The interface screen displays the box graphic of the switch, interface table with details, edit and search options. The details option is a check-box which is checked by default. There is a total count on the top left corner of the table which gives us number of rows in the table, it dynamically updates when a search is done giving us the number of results found with the search input.


On clicking any row in the interface table / click on any port on the box graphic should shoot out interface details panel if details option is checked. This interface details panel has three tabs: general, statistics, and LLDP.

The general tab has information about the interface configuration. All port statistics are present in the statistics tab. Finally, LLDP neighbor information and statistics are provided under LLDP tab. The information in the interface details panel can be used to help understand the interface configuration and health as well as provided troubleshooting information via the LLDP “map” of directly connected devices.

There is a close (X) icon on the top right corner which is used to close the interface details panel.

The edit icon is enabled once a row/ port on the box graphic is selected. Clicking the enabled edit icon should shoot out an edit panel with present state of admin state, auto negotiation, duplex and flow control of the interface, which can be configured. There is a close (X) icon on the top right corner of the edit panel and there is an “OK” button in the footer of the panel.

If an interfaces can be split, you can see the split children and split parent details in the interface details panel. When editing a split parent interface, an additional option is available which is split/ un-split under the edit panel which is set to un-split by default. If split parent interface is configured split from here, then the table updates to show all the split interfaces of that parent. This split parent cannot be configured until it’s un-split.

## LAGs
The Link Aggregation (LAG) screen displays the LAG table with details, edit, add, delete and search options. The details panel will be displayed when selecting a LAG in the list, when the detail check-box which is checked (default). There is a total count on the top left corner of the table.  When using the search box a count of the number found will be displayed in parenthses next to the total count.

### Add LAG
A new LAG can be added by clicking on the plus sign (+).  This will bring up a LAG add panel with 2 tabs of configuration:  "ID & Interfaces" and "Attributes".  

#### ID & Interfaces
The ID & Interfaces tab has an input box for the LAG ID to be created. The list of available LAG ID ranges is shown. There are two icons plus (+) and minus (-) which increment and decrement the LAG ID.  There are two list of interfaces - available and those currently part of that LAG.  The boxes next to "Available" and the LAG name will select and deselect everything in the list.  When selecting an interface from the available list, it can be added by clicking on the greater-than sign (>).  An interface can be removed from the LAG by selecting it and clicking on the less-than sign (<).

#### Attributes
LAG Attributes includes the following configuration options:  Aggregation Mode, Rate, Fallback and Hash. 
Aggregation Mode can be Active, Passive, or Off.  Fallback is true or false, Options for Hash are L3 Src/Dst, L2 Src/Dst, L2 VID Src/Dst, and L4 Src/Dst.

### Remove LAG
The currently selected LAG can be removed by clicking on the minus sign (-).

### Edit LAG
To change the information of an existing LAG, select the LAG and click on the wrench icon.  This will bring up the same dialog as Add LAG.


## ECMP
The ECMP screen shows ECMP (Equal Cost Multi-Path) status and various load balancing configurations:

- **Status:** Determines whether ECMP is enabled in the system. Default is true

- **Source IP:** Determines whether the source IP participates in the ECMP hash calculation. Default is true.

- **Source Port:**  Determines whether the source TCP/UDP port participates in the ECMP hash calculation. Default is true.

- **Destination IP:** Determines whether the destination IP participates in the ECMP hash calculation. Default is true.

- **Destination Port:** Determines whether the destination TCP/UDP port participates in the ECMP hash calculation. Default is true.

- **Resilience Hashing:** Determines whether the ECMP hashing preserves traffic flows when the ECMP group membership changes. Default is true.

### Edit ECMP
The ECMP configuration can be edited by clicking on the wrench icon.


## Log
The Log screen displays a table of the switch logs.  By default the only the critical logs from the last hour are displayed.  The fields being displayed are Time, Severity, Identifier, Category, and Message.  

There are drop-down lists for severity (Critical Only, Critical & Warning, and All) and for time (Last Hour, Last 24 Hours, and Last 7 Days).  When selecting an option in the drop-down list it will make a request to the switch to pull the latest logs matching the selected criteria.

In the upper right corner is a search box.  This will filter the list of logs to those matching the search criteria.  All fields are used when searching.

If the length of the message field is too big to fit, the entire message will be displayed when you mouse over the message field.

## Quick Guides
Quick Guides provide online help for some of the web UI features.

## Links

### REST API
The Swagger UI link opens a new window/tab in the browser and displays the Swagger UI:  [http://api.openswitch.net/rest/dist/index.html](http://api.openswitch.net/rest/dist/index.html)

### OpenSwitch.net
The OpenSwitch.net link opens a new window/tab in the browser and displays the OpenSwitch website:
[http://openswitch.net](http://openswitch.net)

## User
At the bottom left corner of the screen the currently logged in user is shown.  When you click on the user name a pop-up menu with two options is displayed:  Logout and Change Password

### Logout
This will logout the current user and return to the login page.

### Change Password
The Change Password prompts the user for Old Password, New Password and Confirm New Password.  


<!--  See the https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet for additional information about markdown text.
Here are a few suggestions in regards to style and grammar:
* Use active voice. With active voice, the subject is the doer of the action. Tell the reader what
to do by using the imperative mood, for example, Press Enter to view the next screen. See https://en.wikipedia.org/wiki/Active_voice for more information about the active voice. 
* Use present tense. See https://en.wikipedia.org/wiki/Present_tense for more information about using the present tense. 
* The subject is the test case. Explain the actions as if the "test case" is doing them. For example, "Test case configures the IPv4 address on one of the switch interfaces". Avoid the use of first (I) or second person. Explain the instructions in context of the test case doing them. 
* See https://en.wikipedia.org/wiki/Wikipedia%3aManual_of_Style for an online style guide.
 --> 
Management Interface Feature Test Cases
=======

<!--Provide the name of the grouping of commands, for example, LLDP commands-->

 - Test cases to verify Management interface configuration in IPV4 DHCP mode
 - Test case to verify Management interface configuration in Static IPV4 mode 
 - Test cases to verify Management interface configuration in IPV6 DHCP mode
 - Test case to verify Management interface configuration in Static IPV6 mode


##  Test cases to verify Management interface configuration in IPV4 DHCP mode ##
### Objective ###
 Test cases to configure,reconfigure and unconfigure the management interface and to verify the expected behavior of management interface with DHCP IPV4 addressing mode.
   
### Requirements ###
The requirements for this test case are:

 - IPv4 DHCP Server
 
### Setup ###
#### Topology Diagram ####
<pre>





                                                           +-------------------+
              +------------------+                         | Linux workstation |
              |                  |eth0                eth0 |+-----------------+|
              |  AS5712 switch   |&lt;----+         +--------&gt;||DHCP IPV4 Server ||
              |                  |     |         |         |+-----------------+|
              +------------------+     |         |         +-------------------+
                                       |         |
                                       v         v
                                 +---------------------+
                                 | port 1      port 2  |
                                 |                     |
                                 |      Switch         |
                                 |                     |
                                 +---------------------+</pre>
#### Test Setup ####
### Test case 1.01 : Verify DHCP client is started on the management interface  ###
#### Description ####
Test to verify whether dhcp client has started on Management interface by using the following systemctl command "systemctl status dhclient@eth0.service" after booting the switch.

### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if dhcpclient service status is in running state.
#### Test Fail Criteria ####
Testcase result is fail if dhcpclient service status is not in running state.

### Test case 1.02 - Verify management interface is updated from image.manifest file ###
#### Description ####
Test to verify management interface name is updated from image.manifest file during bootup".
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if 'name=eth0' is present in mgmt_intf column.
#### Test Fail Criteria ####
Testcase result is fail if 'name=eth0' is missing in mgmt_intf column.

### Test case 1.03 - Verify management interface attributes are configured in DHCP mode ###
#### Description ####
Test to verify management interface attributes are configured in DHCP mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if ipv4 address, default gateway and DNS server address is present in 'show interface mgmt' output and dhcclient@eth0.service status is in running state.
#### Test Fail Criteria ####
Testcase result is fail if ipv4 address or default gateway or DNS server address is not present in 'show interface mgmt' output or
dhcclient@eth0.service status is not in running state.

##  Test case to verify Management interface configuration in Static IPV4 mode ##

### Objective ###
 Test cases to configure, reconfigure and unconfigure the management interface and to verify the expected behavior of management interface in static IPV4 mode.
   
### Requirements ###
No Requirements.
 
### Setup ###
#### Topology Diagram ####
<pre>





                                                           +-------------------+
              +------------------+                         |                   |
              |                  |eth0                eth0 |                   |
              |  AS5712 switch   |&lt;----+         +--------&gt;| Linux Workstation |
              |                  |     |         |         |                   |
              +------------------+     |         |         +-------------------+
                                       |         |
                                       v         v
                                 +---------------------+
                                 | port 1      port 2  |
                                 |                     |
                                 |      Switch         |
                                 |                     |
                                 +---------------------+</pre>
#### Test Setup ####
### Test case 2.01 - Verify static IPV4 address is configured on management interface  ###
#### Description ####
Test whether user is able to configure static ipv4 address on management interface from management interface context.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if configured ipv4 address is present in show interface mgmt & ifconfig output.
#### Test Fail Criteria ####
Testcase result is fail if configured ipv4 address is not present in show interface mgmt or ifconfig output.

### Test case 2.02 - Verify default gateway is configured in static mode ###
#### Description ####
Test whether user is able to configure static ipv4 on management interface from management interface context.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if configured default gateway is present in show interface mgmt & ip route show output.
#### Test Fail Criteria ####
Testcase result is fail if configured Default gateway is not present in show interface mgmt or ip route show output.

### Test case 2.03 - Verify default gateway is removed in static mode ###
#### Description ####
Test whether user is able to remove default gateway in state mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if configured default gateway is not present in show interface mgmt & ip route show output.
#### Test Fail Criteria ####
Testcase result is fail if configured default gateway is present in show interface mgmt or ip route show output.

### Test case 2.04 - Verify Primary DNS and secondary DNS are configured in static mode ###
#### Description ####
Test whether user is able to configure primary DNS and secondary DNS in static mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if configured Primary DNS and secondary DNS is present in show interface mgmt output & /etc/resolv.conf file.
#### Test Fail Criteria ####
Testcase result is fail if configured primary DNS and secondary DNS is not present in show interface mgmt output or /etc/resolv.conf file.

### Test case 2.05 - Verify Primary DNS and secondary DNS are removed in static mode ###
#### Description ####
Test whether user is able to remove primary DNS and secondary DNS in static mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if configured primary DNS and secondary DNS are not present in show interface mgmt output & /etc/resolv.conf file.
#### Test Fail Criteria ####
Testcase result is fail if configured primary DNS and secondary DNS are present in show interface mgmt output or /etc/resolv.conf file.

##  Test cases to verify Management interface configuration in IPV6 DHCP mode ##

### Objective ###
Test cases to configure,reconfigure and unconfigure the management interface and to verify the expected behavior of management interface with DHCP IPV6 addressing mode. 

   
### Requirements ###
The requirements for this test case are:

 -  IPv6 DHCP Server
 
### Setup ###
#### Topology Diagram ####
<pre>





                                                           +-------------------+
              +------------------+                         | Linux workstation |
              |                  |eth0                eth0 |+-----------------+|
              |  AS5712 switch   |&lt;----+         +--------&gt;||DHCP IPV6 Server ||
              |                  |     |         |         |+-----------------+|
              +------------------+     |         |         +-------------------+
                                       |         |
                                       v         v
                                 +---------------------+
                                 | port 1      port 2  |
                                 |                     |
                                 |      Switch         |
                                 |                     |
                                 +---------------------+</pre>
#### Test Setup ####
### Test case 3.01 - Verify default gateway is configurable in dhcp mode ###
#### Description ####
Test whether the user is able to configure default gateway in dhcp mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if user not able to configure default gateway in dhcp mode.
#### Test Fail Criteria ####
Testcase result is fail if user able to configure.

### Test case 3.02 - Verify management interface attributes are updated in DHCP mode ###
#### Description ####
Test to verify management interface attributes are configured in DHCP mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if ipv6 address, default gateway and DNS server address is present in 'show interface mgmt' output and dhcclient@eth0.service status is in running state.
#### Test Fail Criteria ####
Testcase result is fail if ipv6 address or default gateway or DNS server address is not present in 'show interface mgmt' output or
dhcclient@eth0.service status is not in running state.


##  Test case to verify Management interface configuration in Static IPV6 mode ##

### Objective ###
 Test cases to configure, reconfigure and unconfigure the management interface and to verify the expected behavior of management interface in static IPV6 mode.
   
### Requirements ###
No Requirements.
 
### Setup ###
#### Topology Diagram ####
<pre>





                                                           +-------------------+
              +------------------+                         |                   |
              |                  |eth0                eth0 |                   |
              |  AS5712 switch   |&lt;----+         +--------&gt;| Linux Workstation |
              |                  |     |         |         |                   |
              +------------------+     |         |         +-------------------+
                                       |         |
                                       v         v
                                 +---------------------+
                                 | port 1      port 2  |
                                 |                     |
                                 |      Switch         |
                                 |                     |
                                 +---------------------+</pre>
#### Test Setup ####
### Test case 4.01 - Verify static IPV6 address is configured on management interface  ###
#### Description ####
Test whether the user is able to configure static ipv6 address on management interface from management interface context.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if configured ipv6 address is present in show interface mgmt & ip -6 addr show dev eth0 output.
#### Test Fail Criteria ####
Testcase result is fail if configured ipv6 address is not present in show interface mgmt or ip -6 addr show dev eth0 output.

### Test case 4.02 - Verify default gateway IPv6 address is configured in static mode ###
#### Description ####
Test whether user is able to configure static ipv6 on management interface from management interface context.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if configured default gateway is present in show interface mgmt & ip route show output.
#### Test Fail Criteria ####
Testcase result is fail if configured Default gateway is not present in show interface mgmt or ip route show output.

### Test case 4.02 - Verify default gateway IPv6 address is removed in static mode ###
#### Description ####
Test whether user is able to remove default gateway in state mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if configured default gateway is not present in show interface mgmt & ip route show output.
#### Test Fail Criteria ####
Testcase result is fail if configured default gateway is present in show interface mgmt or ip route show output.

### Test case 4.04 - Verify Primary DNS and secondary DNS IPv6 addresses are configured in static mode ###
#### Description ####
Test whether user is able to configure primary DNS and secondary DNS in static mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if configured Primary DNS and secondary DNS is present in show interface mgmt output & /etc/resolv.conf file.
#### Test Fail Criteria ####
Testcase result is fail if configured primary DNS and secondary DNS is not present in show interface mgmt output or /etc/resolv.conf file.

### Test case 4.05 - Verify Primary DNS and secondary DNS IPv6 addresses are removed in static mode ###
#### Description ####
Test whether user is able to remove primary DNS and secondary DNS in static mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if configured primary DNS and secondary DNS are not present in show interface mgmt output & /etc/resolv.conf file.
#### Test Fail Criteria ####
Testcase result is fail if configured primary DNS and secondary DNS are present in show interface mgmt output or /etc/resolv.conf file.

Management Interface Feature Test Cases
=======

 - [Test cases to verify Management interface configuration in IPV4 DHCP mode.](#test-cases-to-verify-management-interface-configuration-in-ipv4-dhcp-mode)
 - [Test case to verify Management interface configuration in Static IPV4 mode.](#test-case-to-verify-management-interface-configuration-in-static-ipv4-mode)
 - [Test cases to verify Management interface configuration in IPV6 DHCP mode.](#test-cases-to-verify-management-interface-configuration-in-ipv6-dhcp-mode)
 - [Test case to verify Management interface configuration in Static IPV6 mode.](#test-cases-to-verify-management-interface-configuration-in-static-ipv6-mode)


##  Test cases to verify Management interface configuration in IPV4 DHCP mode ##
### Objectives ###
These cases test:
- Configuring, reconfiguring, and unconfiguring the management interface.
- Verifying the expected behavior of the management interface with the DHCP IPV4 addressing mode.

### Requirements ###
The requirements for this test case are:

 - IPv4 DHCP Server.

### Setup ###
#### Topology Diagram ####
```ditaa
                                                           +-------------------+
              +------------------+                         | Linux workstation |
              |                  |eth0                eth0 |+-----------------+|
              |  AS5712 switch   |-----+         +---------||DHCP IPV4 Server ||
              |                  |     |         |         |+-----------------+|
              +------------------+     |         |         +-------------------+
                                       |         |
                                       v         v
                                 +---------------------+
                                 | port 1      port 2  |
                                 |                     |
                                 |      Switch         |
                                 +---------------------+
```
### Test case 1.01 : Verify that the DHCP client has started on the management interface  ###
#### Description ####
After booting the switch, verify that the dhcp client has started on the management interface by using the fsystem ctl command `systemctl status dhclient@eth0.service`.

### Test Result Criteria ###
#### Test Pass Criteria ####

The test case result is successful if the dhcpclient service state is in a running state.
#### Test Fail Criteria ####
The test case result is a failure if the dhcpclient is not in a running state.

### Test case 1.02 - Verify management interface is updated from image.manifest file ###
#### Description ####
Verify that the management interface name is updated from the image.manifest file during boot.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case result is successful if the `name=eth0` is present in the mgmt_intf column.
#### Test Fail Criteria ####
The test case result is a failure if the `name=eth0` is missing in the mgmt_intf column.

### Test case 1.03 - Verify management interface attributes are configured in DHCP mode ###
#### Description ####
Verify that the management interface attributes are configured in DHCP mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case result is successful if the `IPv4 address/subnet-mask`,`Default gateway IPv4`,`Primary Nameserver`,`Secondary Nameserver` address is present in the `show interface mgmt` output and dhcpclient service state is in a running state.

#### Test Fail Criteria ####
The test case result is a failure if the `IPv4 address/subnet-mask`,`Default gateway IPv4`,`Primary Nameserver`,`Secondary Nameserver` address is missing in the `show interface mgmt` output or dhcpclient is not in a running state.

##  Test cases to verify Management interface configuration in Static IPV4 mode ##

### Objectives ###
These cases test:
- Configuring, reconfiguring, and unconfiguring the management interface.
- Verifying the expected behavior of the management interface with the static IPV4 addressing mode.

### Requirements ###
No Requirements.
 
### Setup ###
#### Topology Diagram ####
```ditaa
              +------------------+                         +-------------------+
              |                  |eth0                eth0 |                   |
              |  AS5712 switch   |-----+         +---------| Linux Workstation |
              |                  |     |         |         |                   |
              +------------------+     |         |         +-------------------+
                                       |         |
                                       v         v
                                 +---------------------+
                                 | port 1      port 2  |
                                 |                     |
                                 |      Switch         |
                                 +---------------------+
```
### Test case 2.01 - Verify static IPV4 address is configured on management interface  ###
#### Description ####
Configure the static ipv4 address on the management interface using the management interface context.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case result is successful if the `IPv4 address/subnet-mask` address is present in the `show interface mgmt` output and `ifconfig` ouptut.
#### Test Fail Criteria ####
The test case result is a failure if the `IPv4 address/subnet-mask` address is missing in the `show interface mgmt` output and `ifconfig` ouptut.
### Test case 2.02 - Verify default gateway is configured in static mode ###
#### Description ####
Configure static default ipv4 gateway on the management interface using the management interface context.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case result is successful if the `Default gateway IPv4` address is present in the `show interface mgmt` output and `ip route show` output.
#### Test Fail Criteria ####
The test case result is a failure if the `Default gateway IPv4` address is missing in the `show interface mgmt` or `ip route show` ouput.
### Test case 2.03 - Verify default gateway is removed in static mode ###
#### Description ####
Remove the ipv4 default gateway in state mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case result is successful if the `Default gateway IPv4` address is missing in the `show interface mgmt` or `ip route show` ouput.
#### Test Fail Criteria ####
The test case result is a failure if the `Default gateway IPv4` address is present in the `show interface mgmt` output and `ip route show` output.
### Test case 2.04 - Verify Primary DNS and secondary DNS are configured in static mode ###
#### Description ####
Configure ipv4 primary DNS and secondary DNS in static mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case result is successful if the `Primary Nameserver`,`Secondary Nameserver` address is present in the `show interface mgmt` output and `/etc/resolv.conf` file.
#### Test Fail Criteria ####
The test case result is a failure if the `Primary Nameserver`,`Secondary Nameserver` address is missing in the `show interface mgmt` output or `/etc/resolv.conf` file.

### Test case 2.05 - Verify Primary DNS and secondary DNS are removed in static mode ###
#### Description ####
Remove ipv4 primary DNS and secondary DNS in static mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case result is successful if the `Primary Nameserver`,`Secondary Nameserver` address is missing in the `show interface mgmt` output and `/etc/resolv.conf` file.
#### Test Fail Criteria ####
The test case result is a failure if the `Primary Nameserver`,`Secondary Nameserver` address is present in the `show interface mgmt` output or `/etc/resolv.conf` file.

##  Test cases to verify Management interface configuration in IPV6 DHCP mode ##

### Objectives ###
These cases test:
- Configuring, reconfiguring, and unconfiguring the management interface.
- Verifying the expected behavior of the management interface with the DHCP IPV6 addressing mode.

### Requirements ###
The requirements for this test case are:

 -  IPv6 DHCP Server.

### Setup ###
- #### Topology Diagram ####
```ditaa
                                                           +-------------------+
              +------------------+                         | Linux workstation |
              |                  |eth0                eth0 |+-----------------+|
              |  AS5712 switch   |-----+         +---------||DHCP IPV6 Server ||
              |                  |     |         |         |+-----------------+|
              +------------------+     |         |         +-------------------+
                                       |         |
                                       v         v
                                 +---------------------+
                                 | port 1      port 2  |
                                 |                     |
                                 |      Switch         |
                                 +---------------------+
```
### Test case 3.01 - Verify default gateway is configurable in dhcp mode ###
#### Description ####
Configure the ipv6 default gateway in dhcp mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case result is successful if the ipv6 default gateway is not configured.
#### Test Fail Criteria ####
The test case result is a failure if the ipv6 default gateway is configured.
### Test case 3.02 - Verify management interface attributes are updated in DHCP mode ###
#### Description ####
Verify that the management interface attributes are configured in DHCP mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case result is successful if the `IPv6 address/prefix`,`Default gateway IPv6`,`Primary Nameserver`,`Secondary Nameserver` address is present in the `show interface mgmt` output and dhcpclient service state is in a running state.
#### Test Fail Criteria ####
The test case result is a failure if the `IPv6 address/prefix`,`Default gateway IPv6`,`Primary Nameserver`,`Secondary Nameserver` address is missing in the `show interface mgmt` output or dhcpclient is not in a running state.


##  Test cases to verify Management interface configuration in Static IPV6 mode ##

### Objectives ###
These cases test:
- Configuring, reconfiguring, and unconfiguring the management interface.
- Verifying the expected behavior of the management interface In static IPV6 mode.

### Requirements ###
No Requirements.

### Setup ###
- #### Topology Diagram ####
```ditaa
              +------------------+                         +-------------------+
              |                  |eth0                eth0 |                   |
              |  AS5712 switch   |-----+         +---------| Linux Workstation |
              |                  |     |         |         |                   |
              +------------------+     |         |         +-------------------+
                                       |         |
                                       v         v
                                 +---------------------+
                                 | port 1      port 2  |
                                 |                     |
                                 |      Switch         |
                                 +---------------------+
```
### Test case 4.01 - Verify static IPV6 address is configured on management interface  ###
#### Description ####
Configure static ipv6 address on the management interface in management interface context.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case result is successful if the `IPv6 address/prefix` address is present in the `show interface mgmt` output and `ip -6 addr show dev eth0` output.
#### Test Fail Criteria ####
The test case result is a failure if the `IPv6 address/prefix` address is missing in the `show interface mgmt` output or `ip -6 addr show dev eth0` output.
### Test case 4.02 - Verify default gateway IPv6 address is configured in static mode ###
#### Description ####
Configure static ipv6 default gateway on the management interface from the management interface context.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case result is successful if the `Default gateway IPv6` address is present in the `show interface mgmt` output and `ip route show` output.
#### Test Fail Criteria ####
The test case result is a failure if the `Default gateway IPv6` address is missing in the `show interface mgmt` output or `ip route show` output.
Testcase result is fail if configured Default gateway is not present in show interface mgmt or ip route show output.

### Test case 4.02 - Verify default gateway IPv6 address is removed in static mode ###
#### Description ####
Remove the ipv6 default gateway that is in state mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case result is successful if the `Default gateway IPv6` address is missing in the `show interface mgmt` output and `ip route show` output.
#### Test Fail Criteria ####
The test case result is a failure if the `Default gateway IPv6` address is present in the `show interface mgmt` output or `ip route show` output.

### Test case 4.04 - Verify Primary DNS and secondary DNS IPv6 addresses are configured in static mode ###
#### Description ####
Configure ipv6 primary DNS and secondary DNS in static mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case result is successful if the `Primary Nameserver`,`Secondary Nameserver` address is present in the `show interface mgmt` output and `/etc/resolv.conf` file.
#### Test Fail Criteria ####
The test case result is a failure if the `Primary Nameserver`,`Secondary Nameserver` address is missing in the `show interface mgmt` output or `/etc/resolv.conf` file.
### Test case 4.05 - Verify Primary DNS and secondary DNS IPv6 addresses are removed in static mode ###
#### Description ####
Remove ipv6 primary DNS and secondary DNS in static mode.
### Test Result Criteria ###
#### Test Pass Criteria ####
The test case result is successful if the `Primary Nameserver`,`Secondary Nameserver` address is missing in the `show interface mgmt` output and `/etc/resolv.conf` file.
#### Test Fail Criteria ####
The test case result is a failure if the `Primary Nameserver`,`Secondary Nameserver` address is present in the `show interface mgmt` output or `/etc/resolv.conf` file.

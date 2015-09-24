#Configuration support for AAA
## Table of Contents
- [Authentication configuration commands](#authentication-configuration-commands)
	- [Configure local or RADIUS authentication](#configure-local-or-radius-authentication)
	- [Configure fallback to local authentication](#configure-fallback-to-local-authentication)
	- [Configure RADIUS servers](#configure-radius-servers)
	- [Configure SSH authentication method](#configure-ssh-authentication-method)
- [User configuration commands](#user-configuration-commands)
    - [Add users to switch](#add-users-to-switch)
    - [Configure existing user password](#configure-existing-user-password)
    - [Delete an existing user](#delete-an-existing-user)
- [Authentication display commands](#authentication-display-commands)
    - [Display authentication for switch login](#display-authentication-for-switch-login)
    - [Display RADIUS servers configured](#display-radius-servers-configured)
    - [Display SSH authentication method](#display-ssh-authentication-method)
    - [Display auto provisioning status](#display-auto-provisioning-status)
- [Display running configuration](#display-running-configuration)

## Authentication configuration commands##

### Configure local or RADIUS authentication
This command used to select authentication for accessing the switch.
#### Syntax ####
```
aaa authentication login { local | radius }
```
#### Description ####
Enables local authentication or RADIUS authentication. By default local authentication is enabled.
#### Authority ####
Admin
#### Parameters ####
local   -  Local authentication

radius  -  RADIUS authentication
#### Examples ####
```
    (config)# aaa authentication login local
    (config)# aaa authentication login radius
```
### Configure fallback to local authentication
This command is used to enable or disable fallback to local authentication.
#### Syntax ####
```
[no] aaa authentication login fallback error local
```
#### Description ####
This command enables fallback to local switch access authentication when the RADIUS server is configured but not reachable. The `no` form of this command disables falling back to local switch access authentication. By default fallback to local is enabled.
#### Authority ####
Admin
#### Parameters ####
N/A
#### Examples ####
```
    (config)# aaa authentication login fallback error local
    (config)# no aaa authentication login fallback error local
```
### Configure RADIUS servers
This command is used to configure RADIUS servers on the switch.
#### Syntax ####
```
[no] radius-server host A.B.C.D
[no] radius-server host A.B.C.D auth-port <0-65535>
[no] radius-server host A.B.C.D key WORD
[no] radius-server retries <0-5>
[no] radius-server timeout <1-60>
```
#### Description ####
This command configures RADIUS server information on the switch. Based on the RADIUS server information, the authentication takes place accordingly.

The priority of the RADIUS servers depends on the order in which they are configured.
#### Authority ####
Admin
#### Parameters ####
A.B.C.D: takes valid IPv4 addresses (Broadcast, Multicast and Loopback are not allowed)

<0-65535>: takes numeric values from 0 to 65535 - Default 1812

WORD : takes string values - Default testing123-1

<0-5>: takes values between 0 to 5 - Default 1

<1-60>: takes values between 1 to 60 - Default 5
#### Examples ####
```
    (config)# radius-server host 10.10.10.10
    (config)# no radius-server host 10.10.10.10
    (config)# radius-server host 20.20.20.20 key testRadius
    (config)# no radius-server host 20.20.20.20 key testRadius
    (config)# radius-server host 30.30.30.30 auth-port 2015
    (config)# no radius-server host 30.30.30.30 auth-port 2015
    (config)# radius-server retries 5
    (config)# no radius-server retries 5
    (config)# radius-server timeout 10
    (config)# no radius-server timeout 10
```
### Configure SSH authentication method
This command is used to configure ssh authentication methods.
#### Syntax ####
```
[no] ssh password-authentication
[no] ssh public-key-authentication
```
#### Description ####
This command enables the selected SSH authentication method. Public key authentication uses authorized keys downloaded by the auto provisioning script. By default public key authentication and password authentication are enabled.
#### Authority ####
Admin
#### Parameters ####
N/A
#### Examples ####
```
    (config)# ssh password-authentication
    (config)# no ssh password-authentication
    (config)# ssh public-key-authentication
    (config)# no ssh public-key-authentication
```
## User configuration commands##
### Add users to switch###
#### Syntax ####
```
user add WORD
```
#### Description ####
This command adds users to the switch and configures user passwords.
#### Authority ####
All users
#### Parameters ####
User name
#### Examples ####
```
    ops-as5712# user add openswitch-user
    Adding user openswitch-user
    Enter new password:
    Confirm new password:
    user added successfully.
```
### Configure existing user password###
#### Syntax ####
```
passwd WORD
```
#### Description ####
Configure existing users password except for root user.
#### Authority ####
All users
#### Parameters ####
User name
#### Examples ####
```
    ops-as5712# password openswitch-user
    Changing password for user openswitch-user
    Enter new password:
    Confirm new password:
    password updated successfully
```
### Delete an existing user###
#### Syntax ####
```
user remove WORD
```
#### Description ####
This command deletes a user entry from the switch. The command cannot delete the root user, or a user that is currently logged into the switch. Also, this command cannot delete a user that has last existing user on the switch.
#### Authority ####
All users
#### Parameters ####
User name
#### Examples ####
```
    switch# user remove openswitch-user
```
## Authentication display commands ##
### Display authentication for switch login###
#### Syntax ####
```
show aaa authentication
```
#### Description ####
This command displays authentication used for switch login.
#### Authority ####
All users
#### Parameters ####
N/A
#### Examples ####
```
    switch# show aaa authentication
    AAA Authentication
     Local authentication                  : Enabled
     Radius authentication                 : Disabled
     Fallback to local authentication      : Enabled
```
### Display RADIUS servers configured###
#### Syntax ####
```
show radius-server
```
#### Description ####
This command displays all configured RADIUS servers.
The output displays the following
-IP addresss
-Shared secrets
-Ports used for authentication
-Retries and timeouts
#### Authority ####
All users
#### Parameters ####
N/A
#### Examples ####
```
     switch# show radius-server
     ***** Radius Server information ******
     Radius-server:1
      Host IP address    : 1.2.3.4
      Shared secret      : testRadius
      Auth port          : 2015
      Retries            : 5
      Timeout            : 10
```
### Display SSH authentication method###
#### Syntax ####
```
show SSH authentication-method
```
#### Description ####
This command displays the configured SSH authentication method.
#### Authority ####
All users
#### Parameters ####
N/A
#### Examples ####
```
    switch# show ssh authentication-method 
     SSH publickey authentication : Enabled
     SSH password authentication  : Enabled
```
### Display auto provisioning status###
#### Syntax ####
```
show autoprovisioning
```
#### Description ####
This command displays the presence of auto-provisioning. If auto-provisioning is active, the command output shows the URL that was used to fetch auto-provisioning script.
#### Authority ####
All users
#### Parameters ####
N/A
#### Examples ####
```
    switch# show autoprovisioning
     Performed : Yes
     URL       : https://192.168.0.1/my_autoprov_script_path
```
## Display running configuration##
#### Syntax ####
```
show running-config
```
#### Description ####
This command displays the current non-default configuration on the switch. No user information is displayed as the user configuration is an exec command and is not saved in the OVSDB.
#### Authority ####
All users
#### Parameters ####
N/A
#### Examples ####
```
    switch# show running-config
    Current configuration:
    !
    aaa authentication login radius
    no aaa authentication login fallback error local
    no ssh password-authentication
    no ssh public-key-authentication
    radius-server host 1.2.3.4 key testRadius
    radius-server host 1.2.3.4 auth_port 2015
    radius-server retries 5
    radius-server timeout 10
```
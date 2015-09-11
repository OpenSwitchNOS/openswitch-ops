
<!--  See the https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet for additional information about markdown text.
Here are a few suggestions in regards to style and grammar:
* Use active voice. With active voice, the subject is the doer of the action. Tell the reader what
to do by using the imperative mood, for example, Press Enter to view the next screen. See https://en.wikipedia.org/wiki/Active_voice for more information about the active voice. 
* Use present tense. See https://en.wikipedia.org/wiki/Present_tense for more information about using the present tense. 
* Avoid the use of I or third person. Address your instructions to the user. In text, refer to the reader as you (second person) rather than as the user (third person). The exception to not using the third-person is when the documentation is for an administrator. In that case, *the user* is someone the reader interacts with, for example, teach your users how to back up their laptop. 
* See https://en.wikipedia.org/wiki/Wikipedia%3aManual_of_Style for an online style guide.
Note regarding anchors:
--StackEdit automatically creates an anchor tag based off of each heading.  Spaces and other nonconforming characters are substituted by other characters in the anchor when the file is converted to HTML. 
 --> 
AAA Feature CLI commands
=======

<!--Provide the name of the grouping of commands, for example, LLDP commands-->

 1. Authentication configuration commands.
 
	1.1  Configure local/RADIUS authentication

	1.2  Configure fallback to local 

	1.3  Configure RADIUS servers

	1.4  Configure ssh authentication method


 2. User configuration commands.
 
    2.1 Add users to switch.

    2.2 Configure existing users password.

    2.3 Delete existing users.
 
 3. Authentication display commands.
 
    3.1 Display authentication for switch login

    3.2 Display RADIUS servers
    
    3.3 Display ssh authentication method

    3.4 Display auto provisioning status

 4. Display running configuration.
 

## 1. Authentication configuration commands##

### 1.1 Configure authentication
This command used to select authentication for accessing the switch.
#### Syntax ####
aaa authentication login { local | radius }
#### Description ####
Enables local authentication or RADIUS authentication. By default local authentication is enabled.
#### Authority ####
Admin
#### Parameters ####
local   -  Local authentication

radius  -  RADIUS authentication
#### Examples ####
    config# aaa authentication login local
    config# aaa authentication login radius
### 1.2 Configure fallback to local
This command is used to enable or disable fallback to local authentication. 
#### Syntax ####
[no] aaa authentication login fallback error local 

#### Description ####
Enables fallback to local authentication for switch access when RADIUS server is configured and not reachable. "No" form of this command disables falling back to local authentication. By default fallback to local is enabled. 
#### Authority ####
Admin
#### Parameters ####
N/A
#### Examples ####
    config# aaa authentication login fallback error local
    config# no aaa authentication login fallback error local
### 1.3  Configure RADIUS servers
This command is used to configure RADIUS servers on the switch. 
#### Syntax ####
[no] radius-server host A.B.C.D

[no] radius-server host A.B.C.D auth-port <0-65535>

[no] radius-server host A.B.C.D key WORD

[no] radius-server retries <0-5>

[no] radius-server timeout <1-60>

#### Description ####
Configures RADIUS servers information on the switch. Based on the RADIUS servers information the authentication takes place accordingly. The CLI gives user to configure maximum of 64 RADIUS servers.

The priority of the RADIUS servers depends on the order in which they are configured.
#### Authority ####
Admin
#### Parameters ####
#######Parameters are based on syntax mentioned above.
  
A.B.C.D: takes valid IPv4 addresses (Broadcast, Multicast and Loopback are not allowed)

<0-65535>: takes numeric values from 0 to 65535 - Default 1812

WORD : takes string values - Default testing123-1

<0-5>: takes values between 0 to 5 - Default 1 

<1-60>: takes values between 1 to 60 - Default 5
#### Examples ####
    config# radius-server host 10.10.10.10
    config# no radius-server host 10.10.10.10
    config# radius-server host 20.20.20.20 key testRadius
    config# no radius-server host 20.20.20.20 key testRadius
    config# radius-server host 30.30.30.30 auth-port 2015
    config# no radius-server host 30.30.30.30 auth-port 2015
    config# radius-server retries 5
    config# no radius-server retries 5
    config# radius-server timeout 10
    config# no radius-server timeout 10

### 1.4 Configure ssh authentication method
This command is used to configure ssh authentication methods. 
#### Syntax ####
[no] ssh password-authentication

[no] ssh public-key-authentication 

#### Description ####
Enables the SSH authentication method to be used. Public key authentication uses authorized keys downloaded by auto provisioning script. By default public key authentication and password authentication are enabled.
#### Authority ####
Admin
#### Parameters ####
N/A
#### Examples ####
    config# ssh password-authentication
    config# no ssh password-authentication
    config# ssh public-key-authentication
    config# no ssh public-key-authentication


##2. User configuration commands. ##
### 2.1 Add users to switch.###
#### Syntax ####
username WORD
#### Description ####
Adds the user to switch and configure user password.
#### Authority ####
All users
#### Parameters ####
User name and password
#### Examples ####
    switch# username openswitch-user
    Enter password: 
    Confirm password:

### 2.2 Configure existing users password.###
#### Syntax ####
passwd WORD
#### Description ####
Configure existing users password except for root user.
#### Authority ####
All users
#### Parameters ####
User name
#### Examples ####
    switch# passwd openswitch-user
    Enter new password: 
    Confirm new password:
### 2.3 Delete existing users.###
#### Syntax ####
no username WORD
#### Description ####
Delete user entry from switch. Cannot delete root user, or current logged in user and last existing user.
#### Authority ####
All users
#### Parameters ####
User name
#### Examples ####
    switch# no user openswitch-user

##3. Authentication display commands ##
### 3.1 Display authentication for switch login###
#### Syntax ####
show aaa authentication 
#### Description ####
Display authentication used for switch login.
#### Authority ####
All users
#### Parameters ####
N/A
#### Examples ####
    switch# show aaa authentication
    AAA Authentication
     Local authentication                  : Enabled
     Radius authentication                 : Disabled
     Fallback to local authentication      : Enabled
### 3.2 Display RADIUS servers###
#### Syntax ####
show radius-server
#### Description ####
Displays all RADIUS servers configured. The output has IP address, shared secret, port used for authentication, retries and timeout for all RADIUS servers configured.
#### Authority ####
All users
#### Parameters ####
N/A
#### Examples ####
     switch# show radius-server 
     ***** Radius Server information ******
     Radius-server:1
      Host IP address	: 1.2.3.4
      Shared secret		: testRadius
      Auth port			: 2015
      Retries			: 5
      Timeout			: 10
### 3.3 Display SSH authentication method###
#### Syntax ####
show SSH authentication-method 
#### Description ####
Displays SSH authentication method configured.
#### Authority ####
All users
#### Parameters ####
N/A
#### Examples ####
    switch# show ssh authentication-method 
     SSH publickey authentication : Enabled
     SSH password authentication  : Enabled
### 3.4 Display auto provisioning status###
#### Syntax ####
show autoprovisioning 
#### Description ####
Displays if auto provisioning is performed or not. If performed, command output has URL that was used to fetch auto-provisioning script. 
#### Authority ####
All users
#### Parameters ####
N/A
#### Examples ####
    switch# show autoprovisioning
     Performed : Yes
     URL       : https://192.168.0.1/my_autoprov_script_path
## 4. Display running configuration.##
#### Syntax ####
show 
#### Description ####
Display current non default configuration on the switch.
#### Authority ####
All users
#### Parameters ####
N/A
#### Examples ####
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
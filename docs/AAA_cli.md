# Configuration support for AAA

## Contents

- [Authentication configuration commands](#authentication-configuration-commands)
    - [aaa authentication login](#aaa-authentication-login)
    - [aaa authentication login fallback error local](#aaa-authentication-login-fallback-error-local)
    - [aaa authentication allow-fail-through](#aaa-authentication-allow-fail-through)
    - [aaa group server](#aaa-group-server)
    - [aaa authentication login default](#aaa-authentication-login-default)
    - [radius-server host](#radius-server-host)
    - [radius-server retries](#radius-server-retries)
    - [radius-server timeout](#radius-server-timeout)
    - [tacacs-server](#tacacs-server)
    - [tacacs-server timeout](#tacacs-server-timeout)
    - [tacacs-server key](#tacacs-server-key)
    - [tacacs-server port](#tacacs-server-port)
    - [ssh](#ssh)
- [User configuration commands](#user-configuration-commands)
    - [user add](#user-add)
    - [passwd](#passwd)
    - [user remove](#user-remove)
- [Display commands](#display-commands)
    - [show aaa authentication](#show-aaa-authentication)
    - [show radius-server](#show-radius-server)
    - [show tacacs-server](#show-tacacs-server)
    - [show SSH authentication-method](#show-ssh-authentication-method)
    - [show running-config](#show-running-config)

## Authentication configuration commands

### aaa authentication login

#### Syntax
```
aaa authentication login <local | radius [radius-auth <pap | chap>] | tacacs+ [tacacs-auth <pap | chap>]>
```
#### Description
Enables local authentication, RADIUS authentication, or TACACS+ authentication. By default local authentication is enabled.
#### Authority
Admin
#### Parameters

| Parameter  | Status   | Syntax  |      Description               |
|------------|----------|------------------------------------------|
| **local**  | Required | Literal | Enable local authentication. |
| **radius** | Required | Literal | Enable RADIUS authentication. |
| **tacacs+** | Required | Literal | Enable TACACS authentication. |
| **chap**   | Optional | Literal | Use CHAP with RADIUS/TACACS+ authentication. |
| **pap**    | Optional | Literal | Use PAP with RADIUS/TACACS+ authentication. |

#### Examples
```
    (config)# aaa authentication login local
    (config)# aaa authentication login radius
    (config)# aaa authentication login radius radius-auth chap
    (condig)# aaa authentication login tacacs+ tacacs-auth pap
```
### aaa authentication login fallback error local

#### Syntax
```
[no] aaa authentication login fallback error local
```
#### Description
Enables fallback to local switch access authentication when the RADIUS server is configured but not reachable.

#### Authority
Admin user.
#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Disables falling back to local switch access authentication. |

#### Examples
```
    (config)# aaa authentication login fallback error local
    (config)# no aaa authentication login fallback error local
```

### aaa authentication allow-fail-through

#### Syntax
```
[no] aaa authentication allow-fail-through
```
#### Description
Enables AAA fail-through - try the next TACACS+/RADIUS server according to priority if authentication fails at a server.

#### Authority
Admin user.
#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Disables AAA fail-through. |

#### Examples
```
    (config)# aaa authentication allow-fail-through
    (config)# no aaa authentication allow-fail-through
```


### aaa group server

#### Syntax
```
[no] aaa group server (tacacs+ | radius) <group-name>
```

#### Description
Create a TACACS+ or RADIUS server group. Then enter (config-sg) node

#### Authority
Admin user.

#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Delete a TACACS+ or RADIUS server group. |
| **tacacs+/radius** | Required| Literal | Create a TACACS+ or RADIUS server group. |
| **group-name** | Required | String | Server group name. |

#### Examples
```
    (config)# aaa group server tacacs+ tac1
    (config)# aaa group server radius rad1
    (config)# no aaa group server tacacs+ tac1
```

#### Syntax
```
[no] server <name | ipv4-addr>
```

#### Description
Add a TACACS+ or RADIUS server to corresponding server group. Visible under (config-sg) node

#### Authority
Admin user.

#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Remove a server from server group. |
| **name** | Required | Name-string of maximum length 57 characters or A.B.C.D. | The name or IPV4 address of the server. |

#### Examples
```
    (config)# aaa group server tacacs+ sg1
    (config-sg)#server 1.1.1.1
    (config-sg)#no server 1.1.1.1
```
### aaa authentication login default

#### Syntax
```
[no] aaa authentication login default <local | group group-list>
```

#### Description
Enable AAA authentication and define the sequence in which different server-groups will be traversed.

#### Authority
Admin

#### Parameters
| Parameter  | Status   | Syntax  |      Description               |
|------------|----------|------------------------------------------|
| **local**  | Optional | Literal | Enable local authentication. |
| **group-list** | Optional | String | Space separated group or family names  |
| **no** | Optional | Literal | Disables AAA authentication. |

Notes:
1. Valid familty names are: local, tacacs+ and radius.
2. Each group should be given only once in group-list.
3. 'local' can be given at most once, either before 'group' literal or as part of group-list.
4. Either the 'local' literal or user defined group-list must be given in command.

#### Examples
```
    (config)# aaa authentication login default local
    (config)# aaa authentication login default local group tacacs+ rad1 rad2
    (config)# aaa authentication login default group tac1 tac2 radius local
    (config)# aaa authentication login default group tac1 tac2 rad1 rad2
    (config)# no aaa authentication login default local
```

### radius-server host

#### Syntax
```
[no] radius-server host <A.B.C.D> [auth-port <0-65535> | key <WORD>]
```
#### Description
Configures a RADIUS server host on the switch with the authentication port or the key for a specific RADIUS server. The authentication takes place accordingly.

The priority of the RADIUS servers depends on the order in which they are configured.
#### Authority
Admin user.
#### Parameters
| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Removes the specified host configuration of a switch. |
| *A.B.C.D* | Required | A.B.C.D | A valid IPv4 address (Broadcast, Multicast and Loopback addresses are not allowed). |
| *0-65535* | Required | 0 - 65535 | The authentication port, with a default of port 1812. |
| *WORD* | Required | String | The key for a specific RADIUS server. The default is `testing123-1`. |

#### Examples
```
    (config)# radius-server host 10.10.10.10
    (config)# no radius-server host 10.10.10.10
    (config)# radius-server host 20.20.20.20 key testRadius
    (config)# no radius-server host 20.20.20.20 key testRadius
    (config)# radius-server host 30.30.30.30 auth-port 2015
    (config)# no radius-server host 30.30.30.30 auth-port 2015
```

### radius-server retries

#### Syntax
```
[no] radius-server retries <0-5>
```
#### Description
Configures the number of retries when connecting to the RADIUS server host from the switch. The authentication takes place accordingly.

The priority of the RADIUS servers depends on the order in which they are configured.
#### Authority
Admin user.
#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Removes the configuration for the number of retries. |
| *0-5* | Required | 0-5 | The number of retries. |

#### Examples
```
    (config)# radius-server retries 5
    (config)# no radius-server retries 5
```
### radius-server timeout

#### Syntax
```
[no] radius-server timeout <1-60>
```
#### Description
Configures the timeout in seconds when connecting to the RADIUS server host from the switch. The authentication takes place accordingly.

The priority of the RADIUS servers depends on the order in which they are configured.
#### Authority
Admin user.
#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Removes the configuration for the timeout. |
| *1-60* | Required | 1-60 | The maximum amount of seconds the RADIUS client waits for a response from the RADIUS authentication server before it times out. |

#### Examples
```
    (config)# radius-server timeout 10
    (config)# no radius-server timeout 10
```

### tacacs-server

#### Syntax
```
[no] tacacs-server host <name|ipv4-address> [key passkey] [timeout timeout-val] [port port-num]
```

#### Description
Forms an association with a TACACS+ server.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Delete a previously configured server. |
| *name* | Required | Name-string of maximum length 57 characters or A.B.C.D. | The name or IPV4 address of the server. |
| *passkey* | Optional | Key-string of maximum length 63 characters | The key used while communicating with the server. |
| *timeout-val* | Optional | 1-60 | Timeout value |
| *port-num* | Optional | 1-65535 | TCP port number |

#### Examples
```
s1(config)#tacacs-server host 1.1.1.2 port 1111 timeout 12 key test-key
s1(config)#no tacacs-server host 1.1.1.2
```

### tacacs-server timeout

#### Syntax
```
tacacs-server timeout <timeout-val>
[no] tacacs-server timeout
```

#### Description
Configure global timeout for TACACS+ servers. This will be the timeout value used when timeout is not configured using tacacs-server host command.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *timeout-val* | Required | 1-60 | Timeout value |
| **no** | Optional | Literal | Remove the global TACACS+ server timeout. |

#### Examples
```
switch(config)# tacacs-server timeout 12
switch(config)# no tacacs-server timeout
```

### tacacs-server key

#### Syntax
```
tacacs-server key <passkey>
[no] tacacs-server key
```

#### Description
Configure global passkey for TACACS+ servers. This will be the passkey value used when passkey is not configured using tacacs-server host command.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *passkey* | Required | Key-string of maximum length 63 characters | The key used while communicating with the server. |
| **no** | Optional | Literal | Remove the global TACACS+ server passkey. |

#### Examples
```
switch(config)# tacacs-server key sample-key
switch(config)# no tacacs-server key
```

### tacacs-server port

#### Syntax
```
tacacs-server port <port-num>
[no] tacacs-server port
```

#### Description
Configure global port for TACACS+ servers. This will be the port value used when port is not configured using tacacs-server host command.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *port-num* | Required | 1-65535 | TCP port number |
| **no** | Optional | Literal | Remove the global TACACS+ server port. |

#### Examples
```
switch(config)# tacacs-server port 1112
switch(config)# no tacacs-server port
```

### ssh

#### Syntax
```
[no] ssh <password-authentication | public-key-authentication>
```
#### Description
Enables the selected SSH authentication method. Public key authentication uses authorized keys saved in the user's .ssh folder, either by autoprovisioning script or manually. By default public key authentication and password authentication are enabled.
#### Authority
Admin user.

#### Parameters

|Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Disables the selected SSH authentication method. |
| **password-authentication** | Required | Literal | Sets the SSH authentication method for password authentication. |
| **public-key-authentication** | Required | Literal | Sets the SSH authentication method for public key authentication. |

#### Examples
```
    (config)# ssh password-authentication
    (config)# no ssh password-authentication
    (config)# ssh public-key-authentication
    (config)# no ssh public-key-authentication
```
## User configuration commands
### user add
#### Syntax
```
user add <user_name>
```
#### Description
Adds users to the switch and configures their passwords.
#### Authority
All users.
#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| *user_name* | Required | String | The user name to be added to the switch. |

#### Examples
```
    ops-as5712# user add openswitch-user
    Adding user openswitch-user
    Enter new password:
    Confirm new password:
    user added successfully.
```
### password
#### Syntax
```
password <user_name>
```
#### Description
Configures an existing user password, except for the root user.
#### Authority
All users.
#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| user_name | Required | String | The user name corresponding to the password to be changed. |

#### Examples
```
    ops-as5712# password openswitch-user
    Changing password for user openswitch-user
    Enter new password:
    Confirm new password:
    password updated successfully
```
### user remove
#### Syntax
```
user remove <user_name>
```
#### Description
Deletes a user entry from the switch. The command cannot delete the root user or a user that is currently logged into the switch. Also, this command cannot delete the last existing user on the switch.
#### Authority
All users.
#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| user_name | Required | String | The user name corresponding to the user entry to be removed from the switch. |

#### Examples
```
    switch# user remove openswitch-user
```
## Display commands
### show aaa authentication
#### Syntax
```
show aaa authentication
```
#### Description
Displays the authentication used for the switch login.

#### Authority
All users.

#### Parameters
N/A

#### Examples
```
    switch# show aaa authentication
    AAA Authentication
     Local authentication                  : Enabled
     Radius authentication                 : Disabled
     Fallback to local authentication      : Enabled

    switch# show aaa authentication
    AAA Authentication
     Local authentication                  : Disabled
     Radius authentication                 : Enabled
     Radius authentication type            : CHAP
     Fallback to local authentication      : Enabled
```
### show radius-server
#### Syntax
```
show radius-server
```
#### Description
Displays all configured RADIUS servers, with the following information for each server:
- IP addresss
- Shared secrets
- Ports used for authentication
- Retries and timeouts

#### Authority

All users.
#### Parameters
N/A
#### Examples
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
### show tacacs-server
#### Syntax
```
show tacacs-server [detail]
```

#### Description
Shows the global parameters configured, if any. Also shows the information about each TACACS+ server added.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *detail* | Optional | Literal | Shows the details of TACACS+ servers |

#### Examples
```
switch# show tacacs-server

******** Global TACACS+ configuration *******
Shared secret: testing123-1
Timeout: 15
Auth port: 49
Number of servers: 2

-----------------------------------------------------
                   NAME             PORT  STATUS
-----------------------------------------------------
                 1.1.1.1              49
                 abc.com              49

```

#### Key
```
NAME         : TACACS+ server FQDN/IPV4 address
PORT         : TACACS+ server authentication port
STATUS       : TACACS+ server reachability status
```

```
switch# show tacacs-server detail

******** Global TACACS+ configuration *******
Shared secret: testing123-1
Timeout: 15
Auth port: 49
Number of servers: 2

***** TACACS+ Server information ******
tacacs-server:1
 Server name:   : abc.com
 Auth port      : 49
 Shared secret    : testing123-1
 Timeout      : 15

tacacs-server:2
 Server name:   : 1.1.1.1
 Auth port      : 49
 Shared secret    : testing123-1
 Timeout      : 15

```

### show SSH authentication-method
#### Syntax
```
show SSH authentication-method
```
#### Description
Displays the configured SSH authentication method.
#### Authority
All users.
#### Parameters
N/A
#### Examples
```
    switch# show ssh authentication-method
     SSH publickey authentication : Enabled
     SSH password authentication  : Enabled
```
### show running-config
#### Syntax
```
show running-config
```
#### Description
Displays the current non-default configuration on the switch. No user information is displayed, as the user configuration is an exec command and is not saved in the OVSDB.
#### Authority
All users.
#### Parameters
N/A
#### Examples
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

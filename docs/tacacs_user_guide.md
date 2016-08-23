# TACACS+

## Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Limitations](#limitations)
- [Defaults](#defaults)
- [Configuring TACACS+](#configuring-tacacs)
  - [Adding global timeout](#adding-global-timeout)
  - [Deleting global timeout](#deleting-global-timeout)
  - [Adding global passkey](#adding-global-passkey)
  - [Deleting global passkey](#deleting-global-passkey)
  - [Adding global authentication port](#adding-global-authentication-port)
  - [Deleting global authentication port](#deleting-global-authentication-port)
  - [Adding global authentication mechanism](#adding-global-authentication-mechanism)
  - [Deleting global authentication mechanism](#deleting-global-authentication-mechanism)
  - [Adding a server](#adding-a-server)
  - [Deleting a server](#deleting-a-server)
  - [Adding a server-group](#adding-a-server-group)
  - [Deleting a server-group](#deleting-a-server-group)
  - [Configuring authentication sequence](#configuring authentication sequence)
  - [Deleting authentication sequence](#deleting authentication sequence)
  - [Configuring AAA authorization with fallback](#configuring-aaa-authorization-with-fallback)
  - [Deleting AAA authorization with fallback](#deleting-aaa-authorization-with-fallback)
- [Verifying the configuration](#verifying-the-configuration)
  - [Viewing global config and TACACS+ servers](#viewing-global-config-and-tacacs-servers)
  - [Viewing AAA Authorization information](#viewing-aaa-authorization-information)
  - [Viewing Privilege level information for current user](#viewing-privilege-level-information-for-current-user)
- [CLI](#cli)

## Overview
TACACS+ is a protocol that handles authentication, authorization, and accounting (AAA) services.
TACACS+ client functionality is supported on the switch.

## Prerequisites
- A TACACS+ server (either local or remote) is needed for AAA services.
- OpenSwitch needs to have management interface UP and enabled.

## Limitations
- Currently only TACACS+ Authentication is supported.
- A maximum of 64 TACACS+ servers can be configured.
- Server can be configured with a unicast IPV4/IPV6 address or FQDN
- A maximum of 29 user-defined AAA servers-groups can be configured.
- No session-type (console/ssh/telnet) distinction will be made for authentication.
- TACACS+ server reachability is over the management interface.

## Defaults
- The default authentication tcp-port is 49.
- The default authentication timeout value is 5.
- The default authentication key (shared-secret between client and server) is testing123-1.
- The default authentication-protocol is pap

## Configuring TACACS+
Configure the terminal to change the CLI context to config context with the following commands:
```
switch# configure terminal
switch(config)#
```

### Adding global timeout
The timeout value specifies the number of seconds to wait for a response from TACACS+ server before moving to next TACACS+ server.
If not specified, a default value of 5 seconds will be used.
This can be over-ridden by a fine-grained per server timeout while configuring individual servers.

```
switch(config)# tacacs-server timeout <1-60>
```

### Deleting global timeout
Delete a previously configured global timeout using the following command:
```
switch(config)# no tacacs-server timeout
```

### Adding global passkey
This key is used as shared-secret for encrypting the communication between all tacacs-server and OpenSwitch.
This can be over-ridden by a fine-grained per server passkey configuration.

```
switch(config)# tacacs-server key WORD
```
The length of key should be less than 64.

### Deleting global passkey
Delete a previously configured global key using the following command:
```
switch(config)# no tacacs-server key
```

### Adding global authentication port
The tcp-port to be used for communication with TACACS+ servers.
This can be over-ridden by a fine-grained per server tcp-port configuration.

```
switch(config)# tacacs-server port <1-65535>
```
The authentication port should be in range 1-65535.

### Deleting global authentication port
Delete a previously configured global authentication port using the following command:
```
switch(config)# no tacacs-server port
```

### Adding global authentication mechanism
This is the authentication protocol to be used for communication with TACACS+ servers.
This can be over-ridden by a fine-grained per server auth-type configuration.

```
switch(config)# tacacs-server auth-type [pap/chap]
```

### Deleting global authentication mechanism
Delete a previously configured authentication mechanism.
```
switch(config)# no tacacs-server auth-type [pap/chap]
```

### Adding a server
Add a TACACS+ server with the following command:
```
switch(config)# tacacs-server host <FQDN/IPv4/IPv6 address> [key passkey] [timeout timeout-val] [port port-num] [auth-type pap/chap]
```
A configured TACACS+ server will be added to the default TACACS+ family group (named "tacacs+").

### Deleting a server
Delete a previously added TACACS+ server using the following command:
```
switch(config)# no tacacs-server host <FQDN/IPv4/IPv6 address>
```

### Adding a server-group
Create a AAA server-group that contains 0 or more pre-configured TACACS+ servers.
A maximum of 32 server-groups can be present in the system.
Out of these 3 are default server-groups (local, radius, tacacs+).
Hence 29 user-defined groups are allowed.
The user-defined group cannot be named "local", "radius" or "tacacs+".
Predefined TACACS+ servers can then be added to this group.
The server continues to be part of the default "tacacs+" family group.
For authentication using a server-group, the servers will be accessed in the
same order in which they were added to the group.
```
  switch(config)# aaa group server tacacs+ <group-name>
<aaa-group-mode># server 1.1.1.1 port 49
<aaa-group-mode># server 2.2.2.2 port 49
```

### Deleting a server-group
Only a pre-configured user-defined TACACS+ server-group can be deleted.
The servers belonging to the group being deleted are still a part of the
default "tacacs+" family group.
```
switch(config)# no aaa group server tacacs+ <group-name>
```

### Configuring authentication sequence
Preconfigured server groups can be sequenced to be accessed for authentication.
The server groups will be accessed in the order in which they are mentioned
in the following CLI.
Also the servers within the groups will be accessed in the order in which
they were added to the group.
By default "local" authentication is triggered if no group is mentioned
or if the mentioned list is exhausted.
All servers will be accessed in a fail-through manner.
Upon failure in connection or failure in authentication, the next server
will be reached out to.
```
switch(config)# aaa authentication login default {group <group-list> | local}

For example:
switch(config)# aaa authentication login default group tacacs+ radius local
switch(config)# aaa authentication login default group TacGroup1 TacGroup2 local
```

### Deleting authentication sequence
A configured sequence of server-groups for authentication can be deleted
by the following CLI -
```
switch(config)# no aaa authentication login default
```

### Configuring AAA Authorization with fallback

By issuing 'aaa authorization commands default' command, the user can configure Authorization on the
switch. Fallback preference is dictated by the sequence of groups and local entered
by the user. This command would mean that it would reach out to TACACS+ for each command entered for all users.

```
switch(config)# aaa authorization commands default {group <group-list> | local}
For example:
switch(config)# aaa authorization commands default group tacacs+ local
switch(config)# aaa authorization commands default group TacGroup1 tacacs+ local
```

### Deleting AAA Authorization with fallback

By issuing 'no aaa authorization commands default' command, the user can unconfigure Authorization on the
switch.

```
switch(config)# no aaa authorization commands default
For example:
switch(config)# no aaa authorization commands default group tacacs+ local
switch(config)# aaa authorization commands default group TacGroup1 tacacs+ local
```


## Verifying the configuration
### Viewing global config and TACACS+ servers
The `show tacacs-server` and `show tacacs-server detail` commands display the configured TACACS+ servers.
Both the commands show the global parameters as well as per server configurations.

```
switch# show tacacs-server

******** Global TACACS+ configuration *******
Shared secret: testing123-1
Timeout: 15
Auth port: 49
Number of servers: 2

-----------------------------------------
                   NAME             PORT
-----------------------------------------
                 1.1.1.1              49
                 2.2.2.2              49

```

```
switch# show tacacs-server detail

******** Global TACACS+ configuration *******
Shared secret: testing123-1
Timeout: 5
Auth port: 49
Number of servers: 2

***** TACACS+ Server information ******
tacacs-server:1
 Server name:   : abc.com
 Auth port      : 49
 Shared secret  : testing123-1
 Timeout        : 5
 Auth-Type      : pap
 Server-Group   : tacacs+

tacacs-server:2
 Server name:   : 1.1.1.1
 Auth port      : 49
 Shared secret  : testing123-1
 Timeout        : 5
 Auth-Type      : pap
 Server-Group   : TacGroup1

```

### Viewing AAA Authorization information

The 'show aaa authorization' command displays detailed information on Authorization configuration on the switch.

```
switch# show aaa authorization
For all commands:
  Group TacGroup1:
    Priority : 1
    Servers:
    1.1.1.1 key awesomeKey timeout 10
    2.2.2.2 key bestKey
  Group tacacs+:
    Priority : 2
    Servers:
    1.1.1.1 key awesomeKey timeout 10
    2.2.2.2 key bestKey
    3.3.3.3 key letsBeFreeKey
```

### Viewing Privilege level information for current user

The 'show privilege' command displays the current user privilege level for the current session.

```
switch# show privilege
Current user privilege level is : level-10
```

## CLI
Click [here](/documents/user/tacacs_cli) for the CLI commands related to the TACACS+ feature.

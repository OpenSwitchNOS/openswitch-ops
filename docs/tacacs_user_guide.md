# TACACS+

## Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Limitations](#limitations)
- [Defaults](#defaults)
- [Configuring TACACS+](#configuring-tacacs)
  - [Adding a server](#adding-a-server)
  - [Deleting a server](#deleting-a-server)
  - [Adding global timeout](#adding-global-timeout)
  - [Deleting global timeout](#deleting-global-timeout)
  - [Adding global passkey](#adding-global-passkey)
  - [Deleting global passkey](#deleting-global-passkey)
  - [Adding global authentication port](#adding-global-authentication-port)
  - [Deleting global authentication port](#deleting-global-authentication-port)
- [Verifying the configuration](#verifying-the-configuration)
  - [Viewing global config and TACACS+ servers](#viewing-global-config-and-tacacs-servers)
- [CLI](#cli)

## Overview
TACACS+ is a protocol that handles authentication, authorization, and accounting (AAA) services. TACACS+ functionality is supported on the switch.

## Prerequisites
- A TACACS+ server (either local or remote) is needed for AAA services.
- OpenSwitch needs to have management interface UP and enabled.

## Limitations
- A maximum of 64 TACACS+ servers can be configured.
- The server name can be a maximum of 57 characters long.
- Currently IPv4/IPv6 address is supported. However, multicast, broadcast or loopback addresses are not supported.
- Currently only Authentication is supported.

## Defaults
- The default authentication port is 49.
- The default timeout value is 5.
- The default key is testing123-1.

## Configuring TACACS+
Configure the terminal to change the CLI context to config context with the following commands:
```
switch# configure terminal
switch(config)#
```

### Adding a server
Add a TACACS+ server with the following command:
```
switch(config)# tacacs-server host <FQDN/IPv4/IPv6 address> [key passkey] [timeout timeout-val] [port port-num]
```

### Deleting a server
Delete a previously added TACACS+ server using the following command:
```
switch(config)# no tacacs-server host <FQDN/IPv4/IPv6 address>
```

### Adding global timeout
The timeout value to be used when no timeout is provided while adding server using tacacs-server command. The timeout specifies the number of seconds to wait for a response from TACACS+ serer before moving to next TACACS+ server.

```
switch(config)# tacacs-server timeout <1-60>
```
- The timeout value should be in range 1-60.

### Deleting global timeout
Delete a previously configured global timeout using the following command:
```
switch(config)# no tacacs-servet timeout
```

### Adding global passkey
The key value to be used when no key is provided while adding server using tacacs-server command. This key is used for communication between tacacs-server and OpenSwitch.

```
switch(config)# tacacs-server key WORD
```
- The length of key should be less than 64.

### Deleting global passkey
Delete a previously configured global key using the following command:
```
switch(config)# no tacacs-servet key
```

### Adding global authentication port
The authentication port to be used when no port is provided while adding server using tacacs-server command.

```
switch(config)# tacacs-server port <1-65535>
```
- The authentication port should be in range 1-65535.

### Deleting global authentication port
Delete a previously configured global authentication port using the following command:
```
switch(config)# no tacacs-servet port
```

## Verifying the configuration
### Viewing global config and TACACS+ servers
The `show tacacs-server` and `show tacacs-server detail` commands displays the configured TACACS+ servers. Both the commands also shows global parameters configured.

```
switch# show tacacs-server

******** Global TACACS+ configuration *******
Timeout: 15
Number of servers: 2

-----------------------------------------------------
                   NAME             PORT  STATUS
-----------------------------------------------------
                 1.1.1.1              49
                 abc.com              49

```

```
switch# show tacacs-server detail

******** Global TACACS+ configuration *******
Timeout: 15
Number of servers: 2

***** TACACS+ Server information ******
tacacs-server:1
 Server name:   : abc.com
 Timeout      : 15

tacacs-server:2
 Server name:   : 1.1.1.1
 Timeout      : 15

```

## CLI
Click [here](/documents/user/tacacs_cli) for the CLI commands related to the TACACS+ feature.

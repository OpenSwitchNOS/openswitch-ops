# TACACS+ Commands Reference

## Contents
- [TACACS+ configuration commands](#tacacs-configuration-commands)
	- [tacacs-server](#tacacs-server)
	- [tacacs-server timeout](#tacacs-server-timeout)
	- [tacacs-server key](#tacacs-server-key)
	- [tacacs-server port](#tacacs-server-port)
- [Display commands](#display-commands)
	- [show tacacs-server](#show-tacacs-server)

## TACACS+ configuration commands

### tacacs-server

#### Syntax
```
tacacs-server host <name|ipv4-address> [key passkey] [timeout timeout-value] [port port-number]
[no] tacacs-server host <name|ipv4-address>
```

#### Description
Forms an association with a TACACS+ server.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *name* | Required | Name-string of maximum length 57 characters or A.B.C.D. | The name or IPV4 address of the server. |
| *passkey* | Optional | Key-string of maximum length 63 characters | The key used while communicating with the server. |
| *timeout-val* | Optional | 1-60 | Timeout value |
| *port-num* | Optional | 1-65535 | TCP port number |
| **no** | Optional | Literal | Destroys a previously configured server. |

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
| Parameter | Status   | Syntax |	Description          |
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
| Parameter | Status   | Syntax |	Description          |
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
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *port-num* | Required | 1-65535 | TCP port number |
| **no** | Optional | Literal | Remove the global TACACS+ server port. |

#### Examples
```
switch(config)# tacacs-server port 1112
switch(config)# no tacacs-server port
```

## Display commands

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
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *detail* | Optional | Literal | Shows the details of TACACS+ servers |

#### Examples
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

#### Key
```
NAME         : TACACS+ server FQDN/IPV4 address
PORT         : TACACS+ server authentication port
STATUS       : TACACS+ server reachability status
```

```
switch# show tacacs-server detail

******** Global TACACS+ configuration *******
Timeout: 15
Number of servers: 2

***** TACACS+ Server information ******
tacacs-server:1
 Server name:		: abc.com
 Timeout			: 15

tacacs-server:2
 Server name:		: 1.1.1.1
 Timeout			: 15

```

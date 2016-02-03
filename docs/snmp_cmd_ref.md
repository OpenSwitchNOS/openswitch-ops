#Configuration support for SNMP Support


## Contents

- [Manage SNMP agent](#manage-snmp-agent-configuration)

- [Manage SNMP authentication and authorization](#manage-snmp-authentication-and-authorization)

- [Configuring SNMP Traps](#configuring-snmp-trap)

- [Configuring SNMPv3 Traps](#configuring-snmpv3-trap)

- [Display Commands](#display-commands)

## Manage SNMP Agent Configuration


### SNMP Master Agent Configuration

The following command configures the port to which the SNMP master agent is bound.

####Syntax

```
[no] snmp-server agent-port <1-65535>

```

####Description

This command resets the SNMP master agent port to specific value. The value must be between 1 and 65535.

####Authority

Admin

####Parameters

| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|

| **no** | Optional | Literal | Resets the master agent port to default 161|


| **<1-65535>** | Required | Integer | The port on which the SNMP master agent listens for SNMP requests. Default is 161.|


####Examples

```

(config)# snmp-server  agent-port 2000

(config)# no snmp-server agent-port 2000

```

## Manage SNMP authentication and authorization

### SNMPv1, SNMPv2c Community strings

This command is used to configure community strings for the SNMP Agent.

####Syntax

```
[no] snmp-server community <WORD>
```

####Description

This command adds/removes community strings.
####Authority

Admin

####Parameters

| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|

| **no** | Optional | Literal | Removes the specified community string|

| **WORD** | Required | String | The name of the community string. Default is public.|


####Examples

```
(config)# snmp-server community "abcd"

(config)# no snmp-server community "abcd"

```

## Configuring SNMPv3 Users

This command is used to configure SNMPv3 users credentials. The SNMPv3 provides secure access to devices by a combination of authenticating and encrypting SNMP protocol packets over the network.

####Syntax

```
[no] snmp-server user <WORD> [auth <md5 | sha>] auth-pass <WORD> [priv <aes | des>]
priv-pass <WORD>
```

####Description

This command adds/removes SNMPv3 users.
####Authority

Admin

####Parameters

| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|

| **no** | Optional | Literal | Removes the specified SNMPv3 user.|

| **WORD** | Required | String | The name of the SNMPv3 User. |

| **md5 | sha** | Optional | Literal | The SNMPv3 authentication protocol can be either MD5 or SHA. Default is md5|

| **WORD** | Required | String | The auth passphrase of the SNMPv3 User. It must be at least 8 characters in length.|

| **aes | des** | Optional | Literal | The SNMPv3 privacy protocol can be either aes or des. Default is aes|

| **WORD** | Required | String | The privacy passphrase of the SNMPv3 User. It must be at least 8 characters in length.|

####Examples

```
(config)# snmp-server user Admin auth sha auth-pass mypassword priv des priv-pass myprivpass

(config)# no snmp-server user Admin auth sha auth-pass mypassword priv des priv-pass myprivpass

```

## Configuring SNMP Trap


This command is used to configure the trap receivers to which the SNMP agent can send trap notifications.

####Syntax

```
[no] snmp-server host <A.B.C.D | X:X::X:X >  traps | informs version < 1 | 2c > [community WORD] [port <UDP port>]
```

####Description

This command is used to configure the SNMP Trap receivers with IP and port, trap version, community string.

####Authority

Admin

####Parameters

| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|

| **no** | Optional | Literal | Removes the specified trap receiver configuration.|


| **A.B.C.D** | Required | A.B.C.D | Valid IPv4 address of the trap receiver.|

| **X:X::X:X** | Required | X:X::X:X | Valid IPv6 address of the trap receiver.|

| ** 1 | 2c ** | Required | 1 | 2c | The SNMP trap notifications version from the SNMP agent.|

| **WORD** | Optional | String | The name of the community string to be used in the SNMP trap notifications. Default is public|

| **UDP_port** | Optional | Integer | The port on which the SNMP manager  listens for SNMP trap notifications from the SNMP agent. Default is 162|


####Examples

```
(config)# snmp-server host 10.10.10.10 traps version 1

(config)# no snmp-server host 10.10.10.10 traps version 1

(config)# snmp-server host 10.10.10.10 traps version 2c community public

(config)# no snmp-server host 10.10.10.10 traps version 2c community public

(config)# snmp-server host 10.10.10.10 traps version 2c community public port 5000

(config)# no snmp-server host 10.10.10.10 traps version 2c community public port 5000

(config)# snmp-server host 10.10.10.10 informs version 2c community public

(config)# no snmp-server host 10.10.10.10 informs version 2c community public

(config)# snmp-server host 10.10.10.10 informs version 2c community public port 5000

(config)# no snmp-server host 10.10.10.10 informs version 2c community public port 5000

```

## Configuring SNMPv3 Trap


This command is used to configure the trap receivers to which the SNMP agent can send SNMPv3 trap notifications.

####Syntax

```
[no] snmp-server host <A.B.C.D | X:X::X:X >  traps version < 3 > < auth | noauth | priv > user <WORD> [port <UDP port>]
```

####Description

This command is used to configure the SNMPv3 trap receivers with IP and port, trap version, SNMPv3 user credentials.

####Authority

Admin

####Parameters

| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|

| **no** | Optional | Literal | Removes the specified trap receiver configuration|


| **A.B.C.D** | Required | A.B.C.D | Valid IPv4 address of the trap receiver.|

| **X:X::X:X** | Required | X:X::X:X | Valid IPv6 address of the trap receiver.|

| ** 3 ** | Required | 3 | The SNMP trap notifications version from the SNMP agent.|

| **WORD** | Optional | String | The name of the community string to be used in the SNMP trap notifications. Default is public.|

| **UDP_port** | Optional | Integer | The port on which the SNMP manager  listens for SNMP trap notifications from the SNMP agent. Default is 162|


####Examples

```
(config)# snmp-server host 10.10.10.10 trap version 1

(config)# no snmp-server host 10.10.10.10 trap version 1

(config)# snmp-server host 10.10.10.10 trap version 2c community public

(config)# no snmp-server host 10.10.10.10 trap version 2c community public

(config)# snmp-server host 10.10.10.10 trap version 2c community public port 5000

(config)# no snmp-server host 10.10.10.10 trap version 2c community public port 5000

```




## Display Commands

###show snmp

#### Syntax

```
show snmp
```

#### Description

This command displays all the SNMP configuration with following information.

-	master agent port
-	community string
-	trap receivers
-	snmpv3 users

#### Authority

All users

#### Parameters

N/A

#### Examples

```
switch# show snmp

     Master Agent :
         Port    : 161 (Default)

     Community Names :
         public (Default)
         xyz
         abc

      Trap Receivers:
	  ---------------------------------------------------
	  Host            Port      Type             SecName
      ---------------------------------------------------
	  10.1.1.1        6000      SNMPv1 trap      testcom
      10.1.1.1        162       SNMPv2c inform   public
	  10.1.1.1        5000      SNMPv3 inform    Admin

	 SNMPv3 Users :
     ---------------------------------
	  User       AuthMode    PrivMode
     ---------------------------------
	  Admin        MD5       AES
      Guest        MD5       AES

      SNMPv3 EngineID :
		Engine ID : 00000009020000000C025808 (Default)

```

###show snmp community

#### Syntax

```
show snmp community
```

#### Description

This command displays details of all the configured community strings.

#### Authority

All users

#### Parameters

N/A

#### Examples

```

    switch# show snmp community

    Community Names :
      public (Default)
      xyz
      abc

```


###show snmp host

#### Syntax

```
show snmp host
```

#### Description

This command displays details of all the configured trap receivers,with the following information for each trap receiver


- Host IP Address

- Port

- Notification Type

- Security Name


#### Authority

All users

#### Parameters

N/A

#### Examples

```

  switch# show snmp host

  Trap Receivers:
  ---------------------------------------------------
  Host            Port      Type             SecName
  ---------------------------------------------------
  10.1.1.1        6000      SNMPv1 trap      testcom
  10.1.1.1        162       SNMPv2c inform   public
  10.1.1.1        5000      SNMPv3 inform    Admin


```
###show snmpv3 user

#### Syntax

```
show snmpv3 user
```

#### Description

This command displays details of all the configured SNMPv3 users.


- User name

- Authentication protocol

- Privacy protocol

- Security Name

- SNMPv3 EngineID

#### Authority

All users

#### Parameters

N/A

#### Examples

```

  switch# show snmpv3 user
  SNMPv3 Users :
  ---------------------------------
	User       AuthMode    PrivMode
  ---------------------------------
	Admin        MD5       AES
    Guest        MD5       AES

  SNMPv3 EngineID :
	Engine ID : 00000009020000000C025808 (Default)

```

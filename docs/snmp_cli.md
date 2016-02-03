#Configuration support for SNMP Support


## Contents

- [Manage SNMP authentication and authorization](#manage-snmp-authentication-and-authorization)

- [Manage SNMP Agent IP,Port Configuration](#manage-snmp-agent-ip,port-configuration)

- [Configuring SNMP Trap](#configuring-snmp-trap)

- [Display Commands](#display-commands)


## Manage SNMP authentication and authorization

### SNMPv1, SNMPv2C Community strings

This command is used to configure community strings for the SNMP Agent

####Syntax

```
[no] snmp community <WORD> host <A.B.C.D | X:X::X:X> [OID_Access <OID>]]
```

####Description

This command adds/removes community string with ro or rw privilege for A.B.C.D host and optionally restriced to MIB Sub-tree with Object Identifier as OID


####Authority

Admin

####Parameters

| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|

| **no** | Optional | Literal | Removes the specified community string|

| **WORD** | Required | String | The name of the community string|


| **A.B.C.D**  | Required | A.B.C.D | Valid IPv4 address of the host for which access is allowed for this community string|

| **X:X::X:X**  | Required | X:X::X:X | Valid IPv6 address of the host for which access is allowed for this community string|

| **OID** | Optional | String | The OID of the MIB for which access is granted|


####Examples

```
(config)# snmp community "abcd" host 10.10.10.10

(config)# snmp community "defg" host 10.10.10.10

(config)# snmp community "efgh" host 20.20.2.20 OID_Access "1.3.6.1.2.1.1.1"

(config)# no snmp community "abcd" host 10.10.10.10
```


### SNMPv3 Users

This command is used to configure users for the SNMPv3 support


####Syntax

```
[no] snmpv3 user <“WORD”> [auth <{md5 | sha}> } auth_pass <"AUTH_PASS_KEY"> [priv <{aes | des}> priv_pass <"PRIV_PASS_KEY"> ]] security_level <{noAuth | auth | priv}> [OID_Access <OID>]
```

####Description

This command add SNMPv3 users with following information.
User Name, Authentication information, privacy information, access control information and security level for the user.

####Authority

Admin

####Parameters

| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|

| **no** | Optional | Literal | Removes the specified user|

| **WORD** | Required | String | The name of the user|

| **md5** or **sha** | Optional | String | The authentication protocol to be used for authenticating the user|

| **AUTH_PASS_KEY** | Optional | String | The authentication key to be used while authenticating the user. This should be minimum of 8 characters|

| **aes** or **des** | Optional | String | The privacy protocol to be used for encryption|

| **PRIV_PASS_KEY** | Optional | String | The privacy key to be used for encryption. This should be minimum of 8 characters |

| **noAuth** or **auth** or **priv** | Required | Literal | The Security Level specified for the user. noAuth for No authentication and no Privacy, auth for Authentication and no Privacy, priv for both authenticationa and privacy |

| **OID** | Optional | String | The Object Identifier of the MIB object to which the user has access |

####Examples

```
(config)# snmpv3 user "abcd" security_level noAuth

(config)# no snmpv3 user "abcd" security_level noAuth

(config)# snmpv3 user "eabcd" auth sha auth_pass "password" security_level auth

(config)# snmpv3 user "deabcd" auth sha auth_pass "password" priv "aes" priv_pass "password" security_level authPriv 1.3.6.1.2.1.1.0


```

## Manage SNMP Agent IP,Port Configuration


### SNMP Master Agent Configuration

The following command is used to configure IP and Port to which the SNMP master agent is bound.

####Syntax

```
snmp master-agent ip <A.B.C.D | X:X::X:X > [port <"PORT">]
```

####Description

This command configures the IP and port to which the SNMP Master agent should be bound.

####Authority

Admin

####Parameters

| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|


| **A.B.C.D** | Required | A.B.C.D | The Valid IPv4 address to which the SNMP Master Agent is bound to|

| **X:X::X:X** | Required | X.X::X:X | The Valid IPv6 address to which the SNMP Master Agent is bound to|

| **PORT** | Optional | Integer | The Port on which the SNMP Master agent listens on for SNMP requests|


####Examples

```
(config)# snmp master-agent ip 10.10.10.10

(config)# snmp master-agent ip 10.10.10.10 port 161

```



### SNMP Sub-Agent Configuration

The following command is used to configure Port on which the SNMP Sub-Agent listens for SNMP requests

####Syntax

```
snmp subagent port <"PORT">
```

####Description

This command configures the Port on which the SNMP Sub-agent listens for SNMP requests

####Authority

Admin

####Parameters

| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|


| **PORT** | Required | Integer | The Port on which the SNMP Sub-Agent listens on for SNMP requests|


####Examples

```
(config)# snmp subagent port 1705
```


## Configuring SNMP Trap


This command is used to configure the trap receivers to which the SNMP Agent can send trap notification.

####Syntax

```
[no] snmp trap ip <A.B.C.D | X:X::X:X > [community_string <"WORD"> [port <"UDP_port">]]
```

####Description

This command adds/removes community string with ro or rw privilege for A.B.C.D host and optionally restriced to MIB Sub-tree with Object Identifier as OID


####Authority

Admin

####Parameters

| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|

| **no** | Optional | Literal | Removes the specified trap receiver configuration|


| **A.B.C.D** | Required | A.B.C.D | Valid IPv4 address of the trap receiver|

| **X:X::X:X** | Required | X:X::X:X | Valid IPv6 address of the trap receiver|


| **WORD** | Optional | String | The name of the community string. Default is public|


| **UDP_port** | Optional | Integer | The port on which the trap receiver listens for SNMP trap notifications from the SNMP Agent. Default is 162|


####Examples

```
(config)# snmp trap ip 10.10.10.10

(config)# snmp trap ip 10.10.10.20 community_string "abcd" [port <"UDP_port">]]

(config)# snmp trap ip 10.10.10.20 community_string "abcd" port 9876

(config)# no snmp trap ip 10.10.10.20 community_string "abcd" port 9876

```

## Display Commands

###show snmpv3 user

#### Syntax

```
show snmpv3 user
```

#### Description

This command displays details of all the configured users,with the following information for each user, who can submit requests to SNMP agent.


- user name

- authentication protocol

- privacy protocol


#### Authority

All users

#### Parameters

N/A

#### Examples

```
    switch# show snmpv3 user

    User Name : xyz
      Authentication Protocol    : md5
      Privacy Protocol      	 : des

```

###show snmp community

#### Syntax

```
show snmp community
```

#### Description

This command displays details of all the configured community strings,with the following information for each community string


- community string

- host

- OID


#### Authority

All users

#### Parameters

N/A

#### Examples

```

    switch# show snmp community

    Community : xyz
      host    : 10.10.10.10
      OID	  : 1.3.6.1.2.1.1.1


```


###show snmp trap

#### Syntax

```
show snmp trap
```

#### Description

This command displays details of all the configured trap receivers,with the following information for each trap receiver


- host

- community string

- port


#### Authority

All users

#### Parameters

N/A

#### Examples

```

    switch# show snmp trap

    Trap Receiver
      host    : 10.10.10.10
      community : abc
      port	  : 1987

```



###show snmp

#### Syntax

```
show snmp
```

#### Description

This command displays all the SNMP configuration with following information.

-	master Agent Ip and Port
-	sub-Agent Port
-	snmpv3 users
-	community strings
-	trap receivers



#### Authority

All users

#### Parameters

N/A

#### Examples

```
switch# show snmp

     Master Agent
         Ip Address : 10.10.20.10
         Port 		 : 161 (UDP) 

     Sub-Agent Port : 1705

     SNMPv3 Users
         User Name : xyz
             Authentication Protocol    : md5
             Privacy Protocol      	 : des

         User Name : abc
             Authentication Protocol    : sha
             Privacy Protocol      	 : aes

     SNMP Community
         Community : xyz
             host    : 10.10.10.10
             OID	  : 1.3.6.1.2.1.1.1

         Community : abc
             host    : 10.10.10.20
             OID	  : 1.3.6.2.1.2.1.1

	Trap Receiver
	  host    : 10.10.10.10
      community : abc
      port	  : 1987

      host    : 10.10.10.30
      community : xyz
      port	  : 162

```


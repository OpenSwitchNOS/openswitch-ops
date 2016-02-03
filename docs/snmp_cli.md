#Configuration support for SNMP Support


## Contents

- [Manage SNMP authentication and authorization](#manage-snmp-authentication-and-authorization)

- [Manage SNMP agent](#manage-snmp-agent-configuration)

- [Configuring SNMP Traps](#configuring-snmp-trap)

- [Display Commands](#display-commands)


## Manage SNMP authentication and authorization

### SNMPv1, SNMPv2C Community strings

This command is used to configure community strings for the SNMP Agent.

####Syntax

```
[no] snmp community <WORD>
```

####Description

This command adds/removes community strings.
####Authority

Admin

####Parameters

| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|

| **no** | Optional | Literal | Removes the specified community string|

| **WORD** | Required | String | The name of the community string|


####Examples

```
(config)# snmp community "abcd" 

(config)# no snmp community "abcd" 
```



## Manage SNMP Agent Configuration


### SNMP Master Agent Configuration

The following command configures the port to which the SNMP master agent is bound.

####Syntax

```
snmp master-agent port <1-65535>
```

####Description

This command resets the SNMP master agent port to specific value. The value must be between 1 and 65535.

####Authority

Admin

####Parameters

| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|


| **<1-65535>** | Required | Integer | The port on which the SNMP master agent listens for SNMP requests.|


####Examples

```

(config)# snmp master-agent  port 161

```


## Configuring SNMP Trap


This command is used to configure the trap receivers to which the SNMP agent can send trap notifications.

####Syntax

```
[no] snmp trap ip <A.B.C.D | X:X::X:X > [port <"UDP_port">]]
```

####Description

This command is used to configure the SNMP Trap receivers with IP and port.

####Authority

Admin

####Parameters

| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|

| **no** | Optional | Literal | Removes the specified trap receiver configuration|


| **A.B.C.D** | Required | A.B.C.D | Valid IPv4 address of the trap receiver|

| **X:X::X:X** | Required | X:X::X:X | Valid IPv6 address of the trap receiver|


| **UDP_port** | Optional | Integer | The port on which the trap receiver listens for SNMP trap notifications from the SNMP agent. Default is 162|


####Examples

```
(config)# snmp trap ip 10.10.10.10


(config)# snmp trap ip 10.10.10.20 port 9876

(config)# no snmp trap ip 10.10.10.20 port 9876

```

## Display Commands

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

    Community : xyz
    Community : abc

```


###show snmp trap

#### Syntax

```
show snmp trap
```

#### Description

This command displays details of all the configured trap receivers,with the following information for each trap receiver


- host

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
      port	  : 1987

```



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



#### Authority

All users

#### Parameters

N/A

#### Examples

```
switch# show snmp

     Master Agent
         Port 		 : 161 (UDP) 

     SNMP Community
         Community : xyz
         Community : abc

     Trap Receiver
	      host    : 10.10.10.10
         port	  : 1987

         host    : 10.10.10.30
         port	  : 162

```


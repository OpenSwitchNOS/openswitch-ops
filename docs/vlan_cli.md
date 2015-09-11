# VLAN

## Contents
- [Configuration commands](#configuration-commands)
	- [vlan](#vlan)
	- [vlan internal range](#vlan-internal-range)
	- [interface vlan](#interface-vlan)
	- [interface](#interface)
- [Display commands](#display-commands)
	- [show vlan](#show-vlan)
	- [show vlan internal](#show-vlan-internal)
	- [show interface](#show-interface)

## Configuration commands

###  vlan

##### Syntax
Under the config context.

`[no] vlan <vlan-id>`

##### Description
Configure a VLAN.

##### Authority
Admin.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *vlan-id*  | Required. | 1-4094 |	The VLAN identifier. |

##### Example

Enter the VLAN context (VLAN: 101).
```
hostname(config)# vlan 101
hostname(config-vlan)#
```

###  vlan internal range

##### Syntax
Under the config context.

`[no] vlan internal range <start-vlan> <end-vlan> <order>`

##### Description
Create an internal range of VLANs.

##### Authority
Admin.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *start-vlan*  | Required. |1-4094 |	The start of the VLAN range. |
| *end-vlan*  | Required. |1-4094 |	The end of the VLAN range. |
| *order*  | Required. | **ascending** - **descending** |	Assign VLANs in ascending or descending order. |


##### Example

Create a VLAN range in ascending order (range: 101-202).
```
hostname(config)# vlan internal range 101 202 ascending
hostname(config)#
```

###  interface vlan

##### Syntax
Under the config context.

`[no] interface vlan <vlan-id>`

##### Description
Enter the interface VLAN configuration.

##### Authority
Admin.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *vlan-id*  | Required. |1-4094 |	The VLAN id. |


##### Example

Enter the VLAN interface configuration (VLAN: 101)
```
hostname(config)# interface vlan 101
hostname(config-if-vlan)#
```

###  interface

##### Syntax
Under the config context.

`[no] interface <vlan-name>`

##### Description
Enter the interface VLAN configuration.

##### Authority
Admin.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *vlan-name*  | Required. |String. |	The VLAN name. |

##### Example

###### Enter the VLAN interface configuration (name: vlan101)
```
hostname(config)# interface vlan101
hostname(config-if-vlan)#
```

## Display commands

### show vlan

##### Syntax
Under privileged mode.

`show vlan [<vlan-id>]`

#### Description
Displays VLAN configuration.

#### Authority
Operator.

##### Parameters

| Parameter | Status   | Synatx | Description          |
|-----------|----------|--| --------------------|
| *vlan-id*   | Optional. | 1-4094|  The VLAN id.|


##### Example
Display all VLANs.
```
hostname# show vlan

--------------------------------------------------------------------------------
VLAN    Name      Status   Reason         Reserved       Ports
--------------------------------------------------------------------------------
1024    VLAN1024  up       ok             (null)
101     vlan101   down     admin_down     (null)
102     vlan102   down     admin_down     (null)
1025    VLAN1025  up       ok             (null)
hostname#
```
Display a specific VLAN (VLAN: 101).
```
hostname# show vlan 101

--------------------------------------------------------------------------------
VLAN    Name      Status   Reason         Reserved       Ports
--------------------------------------------------------------------------------
101     vlan101   down     admin_down     (null)

```

### show vlan internal

##### Syntax
Under privileged mode.

`show vlan internal`

#### Description
Display the VLAN internal configuration.

#### Authority
Operator.

##### Parameters

None.

##### Example
```
hostname# show vlan internal

Internal VLAN range  : 101-202
Internal VLAN policy : ascending
------------------------
Assigned Interfaces:
        VLAN            Interface
        ----            ---------
        1025            2
        1024            1
hostname#
```

### show interface

##### Syntax
Under privileged mode.

`show interface <vlan-name>`

#### Description
Displays the VLAN interface configuration.

#### Authority
Operator.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *vlan-name*  | Required. |String. |	The VLAN name. |

##### Example
Display the VLAN interface configuration (VLAN: vlan101)
```
hostname# show interface vlan101

Interface vlan101 is down (Administratively down)
 Admin state is down
 Hardware: Ethernet, MAC Address: 48:0f:cf:af:02:17
```

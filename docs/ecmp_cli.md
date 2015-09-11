# ECMP

## Contents
- [Configuration commands](#configuration-commands)
	- [ip ecmp disable](#ip-ecmp-disable)
	- [ip ecmp load-balance](#ip-ecmp-load-balance)
- [Display commands](#display-commands)
	- [show ip ecmp](#show-ip-ecmp)

## Configuration commands

### ip ecmp disable
##### Syntax
Under the config context.

`[no] ip ecmp disable`

##### Description
Disables ECMP.

##### Authority
Admin.

##### Parameters
None.

##### Example
No examples to display.

###  ip ecmp load-balance

##### Syntax
Under the config context.

`[no] ip ecmp load-balance <dst-ip | dst-port | src-ip | src-port> disable`

##### Description
Disables ECMP load-balancing for a specific destination/source IP or port.

##### Authority
Admin.

##### Parameters
| Parameter | Status   | Syntax| Description          |
|-----------|----------|-| ---------------------|
| *dst-ip*  | Required. | A.B.C.D/M | The destination address. |
| *dst-port*  | Required. | 1-65535 | The destination port. |
| *src-ip*  | Required. | A.B.C.D/M | The source address. |
| *src-port*  | Required. | 1-65535 | The source port. |

##### Example
No examples to display.

## Display commands

### show ip ecmp

##### Syntax
Under privileged mode.

`show ip ecmp`

#### Description
Displays the ECMP configuration.

#### Authority
Operator.

##### Parameters
None.

##### Example
```
hostname# show ip ecmp
 ECMP Configuration
---------------------------
 ECMP Status : Enabled
 ECMP Load Balancing by
---------------------------------
Source IP : Enabled
Destination IP : Disabled
Source Port : Enabled
Destination Port : Enabled
```

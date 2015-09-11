# VRF

## Contents
- [Configuration commands](#configuration-commands)
	- [vrf](#vrf)
	- [vrf attach](#vrf-attach)
- [Display commands](#display-commands)
	- [show vrf](#show-vrf)

## Configuration commands

###  vrf

##### Syntax
Under the config context.

`[no] vrf <vrf-name>`

##### Description
Add or remove a VRF.

##### Authority
Admin.

##### Parameters
| Parameter | Status   | Syntax| Description          |
|-----------|----------|-| ---------------------|
| *vrf-name*  | Required. | String. | The name of the VRF. |

##### Example
No examples to display.

###  vrf attach

##### Syntax
Under the interface context.

`[no] vrf attach <vrf-name>`

##### Description
Attach or detach an interface to or from a VRF.

##### Authority
Admin.

##### Parameters
| Parameter | Status   | Syntax| Description          |
|-----------|----------|-| ---------------------|
| *vrf-name*  | Required. | String. | The name of the VRF. |

##### Example
Attach an interface to a VRF (interface: 1, VRF: myVRF)
```
hostname(config)# interface 1
hostname(config-if)# vrf attach myVRF
hostname(config-if)#
```

## Display commands

### show vrf

##### Syntax
Under privileged mode.

`show vrf`

#### Description
Display the details of the configured VRFs.

#### Authority
Operator.

##### Parameters

None.

##### Example
```
hostname# show vrf
VRF Configuration:
------------------
VRF Name : vrf_default

        Interfaces :
        ------------
		1
        30
```

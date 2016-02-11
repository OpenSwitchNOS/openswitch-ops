# Show Core Dump CLI Guide

## Contents

- [show core-dump](#show-core-dump)
	- [Syntax](#syntax)
	- [Description](#description)
	- [Authority](#authority)
	- [Parameters](#parameters)
	- [Examples](#examples)

### show core-dump

#### Syntax
``` show core-dump ```

#### Description
This command will list out all the core dumps present in the switch.

#### Authority
all users.

#### Parameters
No Parameters

#### Examples

```
switch#show core-dump

---------------------------------------------------
TimeStamp                  Daemon Name
---------------------------------------------------
2016-01-20:14:17:15        ops-lldpd

Total number of core dumps present in the system : 1
```


If there is no core-dump present then

```
switch#show core-dump

No core dump present in the system
```



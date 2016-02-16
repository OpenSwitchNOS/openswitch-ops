# Show Core Dump CLI Guide

## Contents

- [show core dump](#show-core-dump)
	- [Syntax](#syntax)
	- [Description](#description)
	- [Authority](#authority)
	- [Parameters](#parameters)
	- [Examples](#examples)

### show core dump

#### Syntax
```
show core-dump
```

#### Description
This command lists all the core dumps in the switch.

#### Authority
all users.

#### Parameters
No Parameters

#### Examples

```
switch# show core-dump
===========================================================
TimeStamp           | Daemon Name
===========================================================
2016-10-09 09:08:22   ops-lldpd
2015-09-12 10:34:56   kernel
===========================================================
Total number of core dumps : 1
===========================================================
```

If there is no core dump present then

```
switch# show core-dump
No core dumps are present
```

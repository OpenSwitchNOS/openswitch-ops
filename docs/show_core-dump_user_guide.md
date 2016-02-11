# Show Core Dump User Guide

## Contents

- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
	- [Example](#example)


## Overview
This command lists out all the core dumps that are present in the switch.  It display the list of coredumps along with the time they got generated as well as the daemon which got crashed.

## How to use the feature
Execute the cli command "show core-dump".

### Example

```
switch#show core-dump

---------------------------------------------------
TimeStamp                  Core Dump Name
---------------------------------------------------
2016-01-20:14:17:15        ops-lldpd
```

# Diagnostic dump Commands

## Contents

- [Diagnostic dump Commands](#diagnostic-dump-commands)
    - [Contents](#contents)
    - [Configuration Commands](#configuration-commands)
    - [Display Commands](#display-commands)
        - [Show Supported Feature List](#show-supported-feature-list)
            - [Syntax](#syntax)
            - [Description](#description)
            - [Authority](#authority)
            - [Examples](#examples)
        - [Show basic diagnostic](#show-basic-diagnostic)
            - [Syntax](#syntax)
            - [Description](#description)
            - [Authority](#authority)
            - [Parameters](#parameters)
            - [Examples](#examples)
        - [Capture Basic Diagnostic to File](#capture-basic-diagnostic-to-file)
            - [Syntax](#syntax)
            - [Description](#description)
            - [Authority](#authority)
            - [Parameters](#parameters)
            - [Examples](#examples)
    - [References](#references)

## Configuration Commands
We don't have any configuration command as part of diag-dump.

##Display Commands
### Show Supported Feature List
#### Syntax
`diag-dump list`
#### Description
This command displays list of features supported by the diag-dump CLI.
#### Authority
All users
#### Examples
```
switch# diag-dump list
List of Supported Features
lldp                    Link Layer Discovery Protocol
lacp                    Link Aggregation Control Protocol
switch#
```

### Show basic diagnostic
#### Syntax
`diag-dump <feature> basic
`
#### Description
This command displays basic diagnostic information of the feature. Check supported features by command "diag-dump list".

#### Authority
All users
#### Parameters
None
#### Examples
```
switch# diag-dump ?
  FEATURE_NAME  Feature name
  list          Show supported features with description

switch# diag-dump list
Diagnostic Dump Supported Features List
lldp                    Link Layer Discovery Protocol

switch# diag-dump lldp
basic  Basic information

switch# diag-dump lldp basic
LLDP : DISABLED

    intf name   |   OVSDB interface     |   LLDPD Interface     |    LLDP Status        |  Link State
==============================================================================================
bridge_normal   |    Yes                |    Yes                |    rxtx               |    down
51-3            |    Yes                |No             |
53              |    Yes                |No             |
49-4            |    Yes                |No             |
51-1            |    Yes                |No             |
35              |    Yes                |No             |
39              |    Yes                |No             |
4               |    Yes                |No             |
6               |    Yes                |No             |
50-1            |    Yes                |No             |
53-3            |    Yes                |No             |
25              |    Yes                |No             |
50-4            |    Yes                |No             |
40              |    Yes                |No             |
51-4            |    Yes                |No             |
37              |    Yes                |No             |
48              |    Yes                |No             |
49              |    Yes                |No             |
50-2            |    Yes                |No             |
52              |    Yes                |No             |
11              |    Yes                |No             |
22              |    Yes                |No             |
5               |    Yes                |No             |
36              |    Yes                |No             |
49-2            |    Yes                |No             |
34              |    Yes                |No             |
54-3            |    Yes                |No             |
9               |    Yes                |No             |
42              |    Yes                |No             |
46              |    Yes                |No             |
17              |    Yes                |No             |
20              |    Yes                |No             |
49-3            |    Yes                |No             |
23              |    Yes                |No             |
47              |    Yes                |No             |
12              |    Yes                |No             |
30              |    Yes                |No             |
24              |    Yes                |No             |
27              |    Yes                |No             |
50              |    Yes                |No             |
13              |    Yes                |No             |
33              |    Yes                |No             |
49-1            |    Yes                |No             |
28              |    Yes                |No             |
43              |    Yes                |No             |
45              |    Yes                |No             |
51              |    Yes                |No             |
50-3            |    Yes                |No             |
8               |    Yes                |No             |
3               |    Yes                |No             |
16              |    Yes                |No             |
15              |    Yes                |No             |
51-2            |    Yes                |No             |
29              |    Yes                |No             |
53-1            |    Yes                |No             |
26              |    Yes                |No             |
52-1            |    Yes                |No             |
18              |    Yes                |No             |
14              |    Yes                |No             |
53-4            |    Yes                |No             |

Diagnostic dump captured for all daemons
```
### Capture Basic Diagnostic to File
#### Syntax
`diag-dump basic [FILE]`
#### Description
This command captures diagnostic information to given file .
#### Authority
All users
#### Parameters
None
#### Examples
```
switch# diag-dump lldp basic /tmp/lldp
```
##References
* [Reference 1]`diagnostic_cli.md`

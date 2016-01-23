# Diagnostic dump Commands

## Contents
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
This command display list of supported features which are enabled  to capture by diag-dump cli.
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
switch# diag-dump lldp basic
    Fan speed Override: normal
    Fan speed: normal
    Fan details:
        Name: base-5L
            rpm: 9600
            direction: f2b
            status: ok
        Name: base-1L
            rpm: 9450
            direction: f2b
            status: ok
        Name: base-3L
            rpm: 9450
            direction: f2b
            status: ok
        Name: base-1R
            rpm: 8100
            direction: f2b
            status: ok
        Name: base-2L
            rpm: 9450
            direction: f2b
            status: ok
        Name: base-3R
            rpm: 8100
            direction: f2b
            status: ok
        Name: base-4L
            rpm: 9450
            direction: f2b
            status: ok
        Name: base-5R
            rpm: 8100
            direction: f2b
            status: ok
        Name: base-2R
            rpm: 8100
            direction: f2b
            status: ok
        Name: base-4R
            rpm: 8100
            direction: f2b
            status: ok


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

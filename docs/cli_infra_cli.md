# CLI infra commands
## Contents

- [Configuration commands](#configuration-commands)
	- [Setting the session-timeout](#setting-the-session-timeout)
	- [Unsetting the session-timeout](#unsetting-the-session-timeout)
	- [Setting alias](#setting-alias)
	- [Unsetting an alias](#unsetting-an-alias)
- [Display commands](#display-commands)
	- [Displaying the session-timeout value](#displaying-the-session-timeout-value)
	- [Displaying the aliases](#displaying-the-aliases)

## Configuration commands
### Setting the session-timeout
#### Syntax
`session-timeout <0-43200>  `

#### Description
Session times out from each CLI session when the session is idle for the configured timeout period. When the user shows no activity for the timeout period, the session times out and exits.The default session timeout period is 30 minutes.
#### Authority
All users.

#### Parameters
This command takes a value between 0 and 43200 and sets the idle timeout in minutes. The value 0 disables the timeout.
#### Examples
```
switch(config)# session-timeout 2
switch(config)#
```
after 2 minutes...
```
Idle session timeout reached, logging out.

Halon 0.3.0 switch ttyS1

switch login:
```
### Unsetting session-timeout
#### Syntax
`no session-timeout`

#### Description
This command resets the idle session timeout to the default value. The default value is 30 minutes.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
switch(config)# no session-timeout
switch(config)# do show session-timeout
session-timeout: 30 minutes (Default)

switch(config)#

```
### Setting alias
#### Syntax
`alias WORD .LINE `

#### Description
This command sets an alias for a particular CLI command.
#### Authority
All users.

#### Parameters
This command takes a string followed by the command to be aliased as parameters .Multiple commands should be separated by ";". Parameters $1, $2, etc. in the body are replaced by the corresponding argument from the command line. Extra arguments are appended at the end. (Max length 400 characters)
#### Examples
```
switch(config)# alias abc hostname $1
switch(config)# abc trial
switch(config)#
trial(config)#
trial(config)# do show alias
 Alias Name                     Alias Definition
 -------------------------------------------------------------------------------
 abc                            hostname $1
trial(config)#

```
### Unsetting an alias
#### Syntax
`no alias WORD `

#### Description
This command removes a set alias.
#### Authority
All users.

#### Parameters
This command takes a string containing the alias as a parameter.
#### Examples
```
trial(config)# no alias abc
trial(config)# do show alias
 Alias Name                     Alias Definition
 -------------------------------------------------------------------------------
trial(config)#

```

## Display commands
### Displaying the session-timeout value
#### Syntax
`show session-timeout  `
#### Description
This command shows the idle timeout in minutes.
#### Authority
All users.
#### Parameters
No Parameters.
#### Examples
```
switch# show session-timeout
session-timeout: 2 minutes

switch#

```
### Displaying the aliases
#### Syntax
`show alias  `
#### Description
This command shows aliases that are configured in the switch.
#### Authority
All users.
#### Parameters
No Parameters.
#### Examples
```
trial# show alias
 Alias Name                     Alias Definition
 -------------------------------------------------------------------------------
 abc                            hostname $1
```
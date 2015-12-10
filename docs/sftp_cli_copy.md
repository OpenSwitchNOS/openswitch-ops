Sftp Utility
======
## Contents

- [SFTP server](#sftp-server)
	- [Enable/Disable](#enable/disable)
	- [Show command](#show-command)
- [SFTP client](#sftp-client)
	- [Interactive mode](#interactive-mode)
	- [Non-interactive mode](#non-interactive-mode)

##SFTP server
###Enable/Disable
#### Syntax
`[no] sftp server enable`
#### Description
This command is used to enable/disable the SFTP server.
#### Authority
Root and Admin user.
#### Examples
```
switch(config)#sftp server enable

switch(config)#no sftp server enable
```

### Show command
#### Syntax
`show sftp server`
#### Description
This command is used to show the SFTP server status.
#### Authority
Root and Admin user.
#### Examples
```
switch# show sftp server

SFTP server configuration
........................................
SFTP server : Enabled
```

##SFTP client
### Interactive mode
#### Syntax
`copy sftp WORD ( <IPv4-address> | <hostname> | <IPv6-address>)`
#### Description
This command will enter the sftp interactive mode.
#### Examples
```
switch# copy sftp abc hostmachine
abc@hostmachine's password:
Connected to hostmachine.
sftp>

switch# copy sftp abc 10.1.1.1
The authenticity of host '10.1.1.1 (10.1.1.1)' can't be established.
ECDSA key fingerprint is SHA256:uWeyXm2j6VkDfCitlyz/P+xGgZW9YYw5GnDOsEgVHeU.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.1.1.1' (ECDSA) to the list of known hosts.
abc@10.1.1.1's password:
Connected to 10.1.1.1.
sftp>

switch# copy sftp abc a::1
The authenticity of host 'a::1 (a::1)' can't be established.
ECDSA key fingerprint is SHA256:uWeyXm2j6VkDfCitlyz/P+xGgZW9YYw5GnDOsEgVHeU.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'a::1' (ECDSA) to the list of known hosts.
abc@a::1's password:
Connected to a::1.
sftp>
```

### Non-Interactive mode
#### Syntax
`copy sftp WORD ( <IPv4-address> | <hostname> | <IPv6-address> ) WORD [WORD]`
#### Description
This command will perform a non-interactive sftp get.
#### Parameters
| Parameter | Syntax | Description
| *WORD* | string | specify the source path of the file
| *WORD* | string | specify the detination path to store the file (default is '/')
#### Examples
```
switch# copy sftp abc hostmachine source-file
abc@hostmachine's password:
Connected to 10.1.1.1.
Fetching source-file to source-file
source-file                   100%   25     0.0KB/s   00:00
switch#

switch# copy sftp abc 10.1.1.1 source-file
abc@10.1.1.1's password:
Connected to 10.1.1.1.
Fetching source-file to source-file
source-file                   100%   25     0.0KB/s   00:00
switch#

switch# copy sftp abc a::1 source-file
abc@a::1's password:
Connected to a::1.
Fetching source-file to source-file
source-file                   100%   25     0.0KB/s   00:00
switch#

switch# copy sftp abc hostmachine source-file destination-file
abc@hostmachine's password:
Connected to hostmachine.
Fetching source-file to destination-file
source-file                   100%   25     0.0KB/s   00:00
switch#

switch# copy sftp abc 10.1.1.1 source-file destination-file
abc@10.1.1.1's password:
Connected to 10.1.1.1.
Fetching source-file to destination-file
source-file                   100%   25     0.0KB/s   00:00
switch#

switch# copy sftp abc a::1 source-file destination-file
abc@a::1's password:
Connected to a::1.
Fetching source-file to destination-file
source-file                   100%   25     0.0KB/s   00:00
switch#
```

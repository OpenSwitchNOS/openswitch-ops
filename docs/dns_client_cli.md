# DNS client

## Contents

- [DNS client configuration](#dns-client-configuration)
    - [Global enable/disable DNS client](#global-enable/disable-dns-client)
    - [Configure Domain Name](#configure-domain-name)
    - [Configure DNS client Domain Lists](#configure-dns-client-domain-lists)
    - [Configure DNS client Name Servers](#configure-dns-client-name-servers)
    - [Configure DNS client hosts](#configure-dns-client-hosts)
    - [Show DNS client](#show-dns-client)

## DNS client configuration
### Global enable/disable DNS client
#### Syntax
`[no] ip dns`
#### Description
This command enables/disables the DNS client.
#### Authority
Root and Admin users.
#### Parameters
No parameters.
#### Examples
```
switch(config)#ip dns

switch(config)#no ip dns
```

### Configure Domain Name
#### Syntax
`[no] ip dns domain-name <WORD>`
#### Description
This command configures a domain name.
#### Authority
Root and Admin users.
#### Parameters
| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:------------------------|
| *WORD* | Required | String | Domain Name.
#### Examples
```
switch(config)#ip dns domain-name domain.com

switch(config)#no ip dns domain-name domain.com

```

### Configure DNS client Domain Lists
#### Syntax
`[no] ip dns domain-list <WORD>`
#### Description
This command configures a DNS client domain list. Maximum of 6 domain list can be configured.
#### Authority
Root and Admin users.
#### Parameters
| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:------------------------|
| *WORD* | Required | String | DNS client Domain List.
#### Examples
```
switch(config)#ip dns domain-list domain1.com
switch(config)#ip dns domain-list domain2.com

switch(config)#no ip dns domain-list domain1.com
switch(config)#no ip dns domain-list domain2.com

```

### Configure DNS client Name Servers
#### Syntax
`[no] ip dns server-address <IPv4-address | IPv6-address>`
#### Description
This command configures a DNS client name servers. Maximum of 6 name servers can be configured.
#### Authority
Root and Admin users.
#### Parameters
| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:------------------------|
| *IPv4-address* | Required | A.B.C.D | DNS client IPv4 name server address.
| *IPv6-address* | Required | X:X::X:X | DNS client IPv6 name server address.
#### Examples
```
switch(config)#ip dns server-address 1.1.1.1
switch(config)#ip dns server-address a::1

switch(config)#no ip dns server-address 1.1.1.1
switch(config)#no ip dns server-address a::1

```

### Configure DNS client Hosts
#### Syntax
`[no] ip dns host <WORD> <IPv4-address | IPv6-address>`
#### Description
This command configures a DNS client host. Maximum of 6 hosts can be configured.
#### Authority
Root and Admin users.
#### Parameters
| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:------------------------|
| *WORD* | Required | String | DNS client host name.
| *IPv4-address* | Required | A.B.C.D | DNS client IPv4 host address.
| *IPv6-address* | Required | X:X::X:X | DNS client IPv6 host address.
#### Examples
```
switch(config)#ip dns host host1 3.3.3.3
switch(config)#ip dns host host1 b::5
switch(config)#ip dns host host2 7.8.9.10
switch(config)#ip dns host host2 121::121

switch(config)#no ip dns host host1 3.3.3.3
switch(config)#no ip dns host host1 b::5

```


### Show DNS client
#### Syntax
`show ip dns`
#### Description
This command shows the DNS client configurations.
#### Authority
Root and Admin users.
#### Parameters
No parameters.
#### Examples
```
switch(config)#ip dns domain-name domain.com
switch(config)#ip dns domain-list domain5.com
switch(config)#ip dns domain-list domain8.com
switch(config)#ip dns server-address 4.4.4.4
switch(config)#ip dns server-address 6.6.6.6
switch(config)#ip dns host host3 5.5.5.5
switch(config)#ip dns host host3 c::12

switch#show ip dns

DNS Client Mode: Enabled
Domain Name : domain.com
DNS Domain list : domain5.com, domain8.com
Name Server(s) : 4.4.4.4, 6.6.6.6

Host Name    Address
-------------------------------
host3            5.5.5.5
host3            c::12

```

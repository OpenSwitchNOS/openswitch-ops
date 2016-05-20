# Configuration support for BroadView

## Contents

- [BroadView configuration commands](#broadview-configuration-commands)
    - [client ip port](#client-ip-port)
    - [agent port](#agent-port)
- [Display Commands](#display-commands)
    - [show broadview](#show-broadview)


## BroadView configuration commands

### client ip port

#### Syntax
```
broadview client ip <ip-address> port <port-num>
```
#### Description
Sets client IP address and port number.

client ip: IP address of remote application which visualizes and analyzes data from agent
client port : port number of remote application which visualizes and analyzes data from agent


#### Authority
Admin
#### Parameters

No Parameters

#### Examples
```
    (config)# broadview client ip 192.168.1.1 port 8080
```
### agent port

#### Syntax
```
broadview agent-port <port-num>
```
#### Description
Sets agent port number  
agent port : Port on which BroadView Daemon listens
#### Authority
Admin user.
#### Parameters

No Parameters

#### Examples
```
    (config)# broadview agent-port 8080
```
## Display Commands
### show broadview

#### Syntax
```
show broadview
```
#### Description
Displays broadview client IP, client port and agent port.
#### Authority
Admin user.
#### Parameters
No Parameters

#### Examples
```
     switch# show broadview
     BroadView client IP is 10.130.168.30
     BroadView client port is 9054
     BroadView agent port is 8080

```

 
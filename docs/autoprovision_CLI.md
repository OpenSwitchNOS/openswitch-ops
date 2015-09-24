# CLI support for Autoprovision

[TOC]

## 1. Autoprovision Show Command ##
### 1.1  show autoprovision
Display the status of autoprovision.
#### Syntax ####
show startup-config

#### Description ####
Display the status of autoprovision if it is performed or not. If performed it shows the URL from where autoprovision script was downloaded and executed.

#### Authority ####
Admin
#### Parameters ####

None

#### Examples ####
If autoprovision is performed
```bash
switch # show autoprovision
Performed : Yes
URL : http://192.168.1.1/autoprovision.sh
```
If autoprovision is not performed
```bash
switch # show autoprovision
Performed : No
```

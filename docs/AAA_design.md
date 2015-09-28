[TOC]
#High level design of ops-aaa-utils(Authentication,Authorization,Accounting)

AAA feature leverages Linux PAM(Pluggable Authentication Modules) to provide authentication for user based login access to services(SSH,Console,REST)running on the switch. pam_unix.so and pam_radius_auth.so are used for local and Radius based authenticatin respectively. Refer to AAA_Component_Design.md for more details on PAM. REST service generates a secure cookie on initial user login by the REST Client. The subsequent requests from the REST client are authenticated based on the secure cookie contained in them till the cookie expires.AAA feature provides either password or publicKey based SSH access to the switch by leveraging the openSSH daemon's file based configuration options.

##Design choices
Linux PAM(http://www.linux-pam.org/) Vs openPAM(http://www.openpam.org/). Linux PAM chosen as it supports more number of modules

##Participating modules
```ditaa
                                                    +-----------------+      +----------+
                                                    |                 |      |   SSHd    |
                                                    | AAA Daemon      +------>  Config  |
                                                    |                 |      |  file    |
                                                    +---------------+-+      +----------+
                                                                    |
                                                                    |
                                                                    |
+----------------+           +----------------------+             +-v------------------+
|   Applications +----------->                      +------------->  /etc/pam.d        |
|SSH,Console,REST|           |     Linux PAM        |             |  config files      |
|                <-----------+                      <-------------+ SSH,Console,REST   |
+----------------+           +-----+-------^--------+             |                    |
                                   |       |                      +--------------------+
                                   |       |
                                   |       |
                                   |       |
                                   |       |
                                +--v-------+-----+
                                |                |
                                |   PAM Module   |
                                | pam_unix and/or|
                                | pam_radius_auth|
                                +----------------+

```

##OVSDB-Schema
Refer to AAA_Component_Design.md

##Any other sections that are relevant for the module

##References

* [Reference 1]AAA_Component_Design.md
* [Reference 2]AAA_user_guide.md
* [Reference 3]AAA_cli.md

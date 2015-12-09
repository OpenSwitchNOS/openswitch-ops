#PING design

##Contents
   - [High level design of Ping](#high-level-design-of-ping)
   - [Design choices](#design-choices)
   - [Internal structure](#internal-structure)
       - [CLI-Daemon](#cli-daemon)

##High level design of Ping

Ping Application is most commonly used for troubleshooting the accessibility of devices.
It is mostly used to verify connectivity between your switch and a host or port.
OpenSwitch uses open source `ping` from inetutils package for implementation of ping functionality.
Ping parameters are obtained from the user through CLI.
Information obtained is stored in a structure and passed to the handler as an argument.
The handler performs mapping of ping parameters entered by the user to the open source ping options and invokes Linux ping utility.
The handler sends back the response obtained from the open source ping to the user through CLI.
The end to end operation is performed in a single thread context as part of CLI Daemon.
No OVSDB Interaction or any other module interaction is involved.

##Design choices

There are multiple open source packages available for the Ping application.
The open source `Ping` application used is taken from Linux Inetutils package.

##Internal structure

```

                     +------------------------------------+
                     |                                    |
                     |                CLI                 |
                     |                                    |
                     +-----------------+------------------+
                                       |
                                       |
                                       |
                                       |
                    +------------------+------------------+
                    |                                     |
                    |             Ping Handler            |
                    |                                     |
                    +-------------------------------------+

```

###CLI-Daemon
All information needed by the ping application is obtained from the user through CLI.
Below information is stored in a structure and maintained in the CLI daemon.

* IPv4-Address
* IPv6-Address
* Hostname
* Datagram-size
* Data-fill pattern
* Timeout value
* Interval value
* Ip-options
* Repetitions value
* Type-of-service value


References:
Inetutils Package (http://www.gnu.org/software/inetutils/)
Linux Ping Man page (http://linux.die.net/man/8/ping)

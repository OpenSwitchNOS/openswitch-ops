#TRACEROUTE design

##Contents
   - [High level design of Traceroute](#high-level-design-of-traceroute)
   - [Design choices](#design-choices)
   - [Internal structure](#internal-structure)
       - [CLI-Daemon](#cli-daemon)

##High level design of Traceroute

Traceroute is a computer network diagnostic tool for displaying the route (path) and measuring transit delays of packets
across an Internet Protocol (IP) network.
OpenSwitch uses open source `traceroute` from inetutils package for implementation of traceroute functionality.
OpenSwitch uses open source `traceroute6` from iputils package for implementation of traceroute6 functionality.
Traceroute parameters are obtained from the user through CLI.
Information obtained is stored in a structure and passed to the handler as an argument.
The handler performs mapping of traceroute parameters entered by the user to the open source traceroute options and invokes Linux traceroute utility.
The handler sends back the response obtained from the open source traceroute to the user through CLI.
The end to end operation is performed in a single thread context as part of CLI Daemon.
No OVSDB Interaction or any other module interaction is involved.

##Design choices

There are multiple open source packages available for the Traceroute application.
The open source `Traceroute` application used is taken from Linux Inetutils package.
The open source `Traceroute6` application used is taken from Linux Iputils package.

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
                    |             Traceroute Handler      |
                    |                                     |
                    +-------------------------------------+

```

###CLI-Daemon
All information needed by the traceroute application is obtained from the user through CLI.
Below information is stored in a structure and maintained in the CLI daemon.

* IPv4-Address
* IPv6-Address
* Hostname
* Maximum TTL
* Minimum TTL
* Timeout value
* Destination port
* probes
* Ip-option loose source route



References:
Inetutils Package (http://www.gnu.org/software/inetutils/)
Iputils Package   (http://www.skbuff.net/iputils/iputils-current.tar.bz2)
Linux Traceroute Man page (http://linux.die.net/man/8/traceroute)

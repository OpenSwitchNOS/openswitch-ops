# High Level Design of Daemon Coredump
The primary goal of the daemon coredump module is to generate and store sufficient information of the crashed daemon for debugging purpose.

## Contents

- [High level design of daemon coredump](#high-level-design-of-daemon-coredump)
	- [Contents](#contents)
	- [Responsibilities](#responsibilities)
	- [Design choices](#design-choices)
	- [Internal structure](#internal-structure)
	- [Configuration](#configuration)
	- [References](#references)


## Responsibilities
This feature enables openswitch to capture daemon coredump on daemon crash.

## Design choices

- Daemon corefile is compressed and archived with build,release information file(/etc/os-release )
- Default path for daemon coredump is /tmp/core/<daemon name>/<daemon name>.<count>.<unix time stamp>.<signal number causing crash>.core.tar.gz . Coredump path can be configured using config file /tmp/core_file.conf .
- No of CoreFiles per Daemon is limited to 1. When the limit is reached the last stored coredump will be overwritten by the new coredump.  Hence we will have the coredump of first four and the latest Crash instance.  This limit is configurable in the config file /tmp/core_file.conf .
- We will install the Coredump manager script(/tmp/cdm.sh) as the frontend for coredump process.  It will have the responsibility of collecting the coredump from the system, limiting it to 1 coredumps, archiving and storing the corresponding path.
- Our primary , secondary requirements for compression are time and memory. GZ compression is used for compression of coreDump since it provides compression in lowest time and best compression ratio.

## Internal structure

```ditaa
                                   +----------------------------------+
+---------+ stdout                 |stdin                             |
| Kernel  +----------------------> |       Corefile processing script |
+----+----+                        +----------------+-----------------+
     |                                              |
     |                                              |
     |                                              |
     |signal                                        |
     |                                              |
     |                                              |
     |                                              v
     |                             +----------------------------------+
     v                             | corefile.tar.gz                  |
+---------+                        |   + release/build info text file |
| Daemon  |                        |   + corefile                     |
+---------+                        +----------------------------------+
```

## Configuration
Enabling this feature on openswitch need configuration changes in multiple config files , which are given below .

- target machine config file /etc/profile.d/ops_core_profile
  ```
  ulimit -c unlimited
  echo 0x7f > /proc/self/coredump_filter
  ```
- target machine config file /etc/sysctl.d/sysctl.conf
  ```
  kernel.core_pattern=|/tmp/cdm.sh %e %t %s
  kernel.core_uses_pid=0
  kernel.core_pipe_limit=4
  ```
 (here cdm.sh is coredump processing script )

- target machine config file /etc/systemd/ops_core_system.conf
  ```
  DumpCore=yes
  DefaultLimitCORE=infinity
  ```
- target machine config file /tmp/core_file.conf
  ```
  maxcore=1
  corepath=/tmp/core
  ```
  maxcore is used to limit maximum number of core file per daemon.

- build machine config file local.conf
  enable debug symbols for all daemons by adding
  ```
  EXTRA_IMAGE_FEATURES = "dbg-pkgs"
  ```
  gdb tool need debug symbols while debugging coredump .

## References
 [Reference 1] daemon_coredump_design.md

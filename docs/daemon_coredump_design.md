# High level design of daemon coredump

The primary goal of the daemon coredump module is to generate and store sufficient information of the crashed daemon for debugging purpose.

## Contents

- [High level design of daemon coredump](#high-level-design-of-daemon-coredump)
	- [Contents](#contents)
	- [Design choices](#design-choices)
	- [How core dumps are generated](#how-core-dumps-are-generated)
	- [Core Dump handling in Docker](#core-dump-handling-in-docker)
		- [Piping core dumps to a program](#piping-core-dumps-to-a-program)
		- [Revert back to original configuration stored in host machine.](#revert-back-to-original-configuration-stored-in-host-machine)

## Design choices


- Uses Systemd Core dump feature to capture and generate the coredump file.
- Generated core dump files will be stored in location /var/lib/systemd/coredump.
- The folder "/var/lib/systemd/coredump" will be created as a symbolic link to a persistant location in order to store the core dumps persistantly.
- Coredumps are stored in compressed format.



## How core dumps are generated

Whenever a process misbehaves, the kernel would generate the appropriate signal and sends it to the process.  The Process's signal handler mechanism would determine whether to core dump or not.  Accordingly Kernel would call the core dump utility as specified by kernel.core_pattern.  We set this kernel.core_pattern to use the systemd helper binary called *systemd-coredump*.  This core dump helper utility would receive the crashing process's core file along with the process PID, timestamp of the crash, signal number leading to the core dump,etc.,  Systemd-coredump utility will then compress and save the core dump file in the path /var/lib/systemd/coredump.  It would additionally add the following meta data information to the files extended attributes.

|Key|Value|Example|
|----------------------|
|user.coredump.comm | Process Name  | vtysh |
|user.coredump.exe | Program location  | /usr/bin/vtysh |
|user.coredump.pid | Process PID | 4166 |
|user.coredump.signal | Signal Number leading to core dump | 11 |
|user.coredump.timerstamp | Timestamp of the core dump event | 1459354952 |

show core dump cli command uses these extended attributes to extract information about the core dump and display to the us

```ditaa
                 corefile,           +-----------------------+
     +--------+  crash info    (3)   |                       |
     | Kernel +-------------------------> Systemd coredump   |
     +-+----^-+                      |           +           |
       |    |                        |           |           |
       |    |                        |           v           |
       |    |(2)                     |        compress       |
       |    |                        |           +           |
       |    |                        |           |           |
signal |    | Core file              |           v           |
       |    |                        |     save metadata     |
       |    |                        |                       |
    (1)|    |                        |                       |
       |    |                        +-----------------------+
       |    |
     +-v----+-+
     | Daemon |
     +--------+
```

## Core Dump handling in Docker

In case of the coredump of a process running inside the docker, the core dump handling is done by the kernel of the host machine.  Core dump handling using systemd mandates that the host machine has systemd installed.  The kernel.core_pattern of the host machine may not be configured to use systemd core dump utility or the host machine might not have systemd installed.  Hence in order to generate coredumps for switch image running in docker, we could use the host machine's core dump handler.
The following step helps us to configure the host machine to generate coredump.

### Piping core dumps to a program
Update the kernel.core_pattern variable to reflect the core dump handler of our choice.

Example :

```
sysctl kernel.core_pattern="|/tmp/ops_cdm.sh %e %p %t"
```

### Revert back to original configuration stored in host machine.
Use sysctl command ```sysctl --system``` to revert back to the original configuration in the host machine.

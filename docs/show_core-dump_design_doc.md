#Show Core Dump design document

##Contents
- [High level design of show core-dump](#high-level-design-of-show-core-dump)
- [Design choices](#design-choices)
	- [Get crash information from the event log and display the coredumps](#get-crash-information-from-the-event-log-and-display-the-coredumps)
	- [Iterate through the core dump storage location and list all the coredump present there.](#iterate-through-the-core-dump-storage-location-and-list-all-the-coredump-present-there)
	- [Final choice](#final-choice)
- [Limitations](#limitations)
- [Block Diagram](#block-diagram)
- [Example](#example)

### High level design of show core-dump
show core-dump list out all the core-dumps present in the switch including kernel core dump.  This helps the user/support team to find the crashes happened in the system.  It displays the name of crashed daemon along with time of the crash.

### Design choices
We had the following two design choices for displaying the core dumps :


#### Get crash information from the event log and display the coredumps

When the user executes "show core-dump" the system will look up into sd-journal log for crash events.  It then verifies whether the file exits in the given file location. If it exists then it will display the same in the output.  Since the coredumps could have been removed by the user, we need to verify whether it is present in the system.

#### Iterate through the core dump storage location and list all the coredump present there.

The location of the core dump is read from the core dump configuration file.  Later iterate though the core dump storage location and list only those files present in that location.  The daemon name and the timestamp of core dump is obtained by parsing the name of the core dump file.

#### Final choice
Iterate through the core dump storage location and list all the coredumps present there.  We finalized on this choice based on the following two reasons
  1. Going through all the entries in the journal is expensive process
  2. Some entries might refer to core dumps which are already removed

### Limitations
Core dump files are stored with specific name format.  The name includes the daemon that got crashed and the timestamp of the crash event.  If the user changes the name of the core file, then the information will be based on the new file name.  If the new file name doesn't follow the core dump file naming format, then that core dump will be ignored for display.

### Block Diagram

```ditaa

  Cli Command
 +---------------+        +-------+------+
 |show core-dump | Read   |  Core-Dump   |
 |               |------->+ Location     |
 +---------------+        +-------+------+
```

### Example

```

switch# show core-dump
===========================================================
TimeStamp           | Daemon Name
===========================================================
2016-10-09 09:08:22   ops-lldpd
2015-09-12 10:34:56   kernel
===========================================================
Total number of core dumps : 1
===========================================================

```

If there is no core-dump present then

```
switch# show core-dump
No core dumps are present
```

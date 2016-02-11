#Show Core Dump Design Document

##contents

- [High level design of show core-dump](#high-level-design-of-show-core-dumps)
- [Design choices](#design-choices)
	- [1) Get Crash information from the event log and display the coredumps](#1-get-crash-information-from-the-event-log-and-display-the-coredumps)
	- [2) Iterate through the core dump storage location and list all the coredump present there.](#2-iterate-through-the-core-dump-storage-location-and-list-all-the-coredump-present-there)
- [Block Diagram](#block-diagram)
- [Example](#example)


### High level design of show core-dump
show core-dump list out all the core-dumps present in the switch.  This helps the user/support team to find out the list of crashes in the switch.  It displays the name of crashed daemon along with time of the crash.

### Design choices
We had the following two choices for displaying the coredumps:


#### 1) Get Crash information from the event log and display the coredumps

When the user executes "show core-dump" the system will look up into sd-journal log for crash events.  It then verifies whether the file exits in the given file location. If it exists then it will display the same in the output.  Since the coredumps could have been removed by the user, we need to verify whether it is a

#### 2) Iterate through the core dump storage location and list all the coredump present there.

Iterate though the coredump storage location and list only those files present in that location.  But this design needs the code dumps to be stored in a predetermined single location and removes the flexibility of storing it under different place.

#### Final choice
Iterate through the core dump storage location and list all the coredumps present there.

### Limitations
* If the user changes the daemon folder name to any other new name, the core files inside that folder will still be displayed with new name as daemon name. We cannot check for daemon name due to the intensive nature of the task.
* If the user changes the name of the core file, that particular core file will not be displayed.

### Block Diagram

```ditaa

  Cli Command                         
 +---------------+        +-------+------+
 |show core-dump| Read   |  Core-Dump   |
 |               |------->+ Location     |
 +---------------+        +-------+------+    
```

### Example

```
switch#show core-dump

---------------------------------------------------
TimeStamp                  Core Dump Name
---------------------------------------------------
2016-01-20:14:17:15        ops-lldpd
```

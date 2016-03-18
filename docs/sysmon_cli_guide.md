# System monitoring command Reference

## Contents
- [Show commands](#display-commands)
  - [show system cpu](#show-system-cpu)
  - [show system memory](#show-system-memory)

## Show commands

### show system cpu

#### Syntax
```
show system cpu
```

#### Description
Shows information about the global CPU usage within the system and
per process info and a snapshot of how much CPU(%) is utilized.

#### Authority
Privileged user.

#### Parameters
No parameters.

#### Examples
```
switch#show system cpu

CPU Average (in %)
Average for last 1  min: 3.44
Average for last 5  min: 2.70
Average for last 15 min: 1.50
CPU util to run user applications        : 9.1
CPU util to run kernel processes         : 1.6
CPU idle time waiting for I/O completion : 1.6
CPU util for servicing h/w interrupts    : 0.1
CPU util for servicing s/w interrupts    : 0.2

Total tasks in system   : 43
Number of tasks running : 1
Number of tasks sleeping: 40
Number of tasks stopped : 0
Number of zombies       : 2

  PID USER      State  %CPU  COMMAND
-------------------------------------
    1 root      S       0.1  systemd
   18 root      S       1.2  systemd-journal
   82 root      S       0.0  systemd-udevd
  131 message+  S       1.1  dbus-daemon
```

### show system memory

#### Syntax
```
show system memory
```

#### Description
Shows information about the global Memory/Swap usage within the system and
per process info and a snapshot of how much memory is utilized.

#### Authority
Privileged user.

#### Parameters
No parameters.

#### Examples
```
switch#show system memory

Physical memory (in KiB)
Total memory      : 8669756
Total free memory : 131108
Total used memory : 1176480
Total buffers     : 7362168

Virtual memory (in KiB)
Total memory      : 8385532
Total free memory : 8364232
Total used memory : 21300
Total buffers     : 7136604


  PID USER      VIRT    RES    SHR  State  %MEM  COMMAND
---------------------------------------------------------
    1 root      23516   4468   3424 S      0.1   systemd
   18 root      78304  50308  50048 S      0.6   systemd-journal
   82 root      32412   2896   2444 S      0.0   systemd-udevd
  131 message+  13180   2388   2168 S      0.0   dbus-daemon
```

```
Legend:
```
State: This column refers to the status of the task which can be one of:
       D = uninterruptible sleep
       R = running
       S = sleeping
       T = traced or stopped
       Z = zombie
VIRT: The  total  amount  of  virtual memory used by the task.  It includes all code, data and
      shared libraries plus pages that have been swapped out and pages that have  been  mapped
      but not used. (in KiB)
RES: This column refers to Resident Memory Size which stores the non-swapped physical memory a task has used. (KiB)
SHR: This column refers to Shared Memory Size which is the amount of shared memory available to a task, not all of which is typically resident. (in KiB)
```

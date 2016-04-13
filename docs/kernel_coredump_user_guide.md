# Kernel Coredump  User Guide

## Contents

- [Kernel Coredump  User Guide](#kernel-coredump-user-guide)
    - [Contents](#contents)
    - [Overview](#overview)
    - [How to use this feature](#how-to-use-this-feature)
        - [Troubleshooting](#troubleshooting)
        - [configuration](#configuration)
        - [How to debug vmcore](#how-to-debug-vmcore)
    - [Supported platforms](#supported-platforms)
    - [CLI](#cli)
    - [References](#references)


## Overview
This feature enables switch to recover itself in case of kernel panic as well as to store kernel core dump to debug the root cause.

## How to use this feature
In case of kernel panic it will capture vmcore and reboot the switch . You can see existing vmcore file present in switch by vtysh cli command "show croe-dump". You can copy out this core file by using "copy core-dump" cli command to external tftp/sftp server.

### Troubleshooting
Ensure /var/diagnostic partition has enough memory ( at least 100 MB free space ) to store kernel vmcore.

### configuration
No need to configure .

### How to debug vmcore
- Check "show core-dump" cli to see kernel core dump file.
- Use "copy core-dump" cli to take out kernel core to build machine where image was built.
- Uncompress the tar.gz file and extract vmcore  .
- Check the file format of vmcore by command "head -1 <path of vmcore>
- For ELF format launch gdb or crash ( ELF format is supported by gdb and crash)
       syntax: gdb <path of vmlinux> <vmcorepath>
       syntax: crash <path of vmlinux> <vmcorepath>
       e.g. "gdb  build/tmp/work/as5712-openswitch-linux/linux-ops/3.9.11-r1_as5712/package/boot/vmlinux-3.9.11 <vmcorepath>"  (ELF format)
- For KDUMP format launch crash
       syntax: crash  <path of vmlinux> <vmcorepath>
       e.g. "crash build/tmp/work/as5712-openswitch-linux/linux-ops/3.9.11-r1_as5712/package/boot/vmlinux-3.9.11 <vmcorepath>" (KDUMP format)

## Supported platforms
Following platforms are supported for this feature
- as5712
- as6712

## CLI
You can use "show core-dump" cli to check last kernel vmcore file.
you can take out this core file by using "copy core-dump" command to external tftp/sftp server.

## References
* [ Kernel coredump design document ] kernel_coredump_design.md
* [ Kernel coredump test document ] kernel_coredump_test.md
* [ Kernel coredump user guide ] kernel_coredump_user_guide.md
* [ Reference Crash tool white paper ] https://people.redhat.com/anderson/crash_whitepaper/

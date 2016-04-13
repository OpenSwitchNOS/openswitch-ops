# Feature Test Cases for Kernel Core

## Contents

- [Feature Test Cases for Kernel Core](#feature-test-cases-for-kernel-core)
    - [Contents](#contents)
        - [Objective](#objective)
        - [Requirements](#requirements)
        - [Setup](#setup)
            - [Topology diagram](#topology-diagram)
            - [Test setup](#test-setup)
        - [Description](#description)
        - [Test result criteria](#test-result-criteria)
            - [Test pass criteria](#test-pass-criteria)
            - [Test fail criteria](#test-fail-criteria)
    - [Supported platforms](#supported-platforms)
    - [References](#references)


### Objective
How to verify kernel coredump feature

### Requirements
Switch running OpenSwitch.

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```

#### Test setup
Standalone Switch

### Description
Step:
- log in to root user
- run "echo c > /proc/sysrq-trigger" command in bash shell.
- system will reboot and core file will be stored in /var/diagnostics/coredump/kernel-core.
- After reboot wait for  2-3 minutes and login to vtysh and run "show core-dump" cli command to see corefile.
- Copy kernel core dump using  "copy core-dump kernel " cli .


### Test result criteria
#### Test pass criteria
- System recovers automatically within 60seconds.
- Kernel core dump file is generated

#### Test fail criteria
- System hangs forever.
- System did not generate kernel core file


## Supported platforms
Following platforms ae supported for this feature
- as5712
- as6712

## References
* [ Kernel coredump design document ] kernel_coredump_design.md
* [ Kernel coredump test document ] kernel_coredump_test.md
* [ Kernel coredump user guide ] kernel_coredump_user_guide.md
* [ Reference Crash tool white paper ] https://people.redhat.com/anderson/crash_whitepaper/

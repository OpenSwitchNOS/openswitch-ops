## High level design of kernel coredump

It is desirable to have the Kernel CoreDump for analysing and root causing issues related to Kernel Configuration, Kernel Code, Kernel Exceptions, Device Driver Code and Exceptions.

When the running kernel crashes due to above mentioned exceptions, it wouldn't be in a stable state to store and process its own core dump.  Hence we use utility like makedumpfile to dump the core dump of Crashed Kernel.

Kdump is a standard Linux mechanism to dump machine memory content on kernel crash. Kdump internally uses collection of tools like kexec, makedumpfile etc.  to perform core dump.  In order to perform this task kdump needs a stable running kernel.  Hence kdump utilizes two kernels: primary kernel and secondary kernel. Primary kernel is the normal kernel that is booted with special kdump-specific flags.  Secondary Kernel is the Kernel which will take control when the primary kernel has crashed.  Its primary objective is to dump the Kernel Core Dump and reboot the system as early as possible.   In the boot option of System Kernel we additionally need to specify/reserve some amount of physical memory where dump-capture kernel will be loaded.  The boot script of SystemKernel will be configured to load the secondary  kernel in advance because at the moment crash happens there is no way to read any data from disk to load the Dump Capture Kernel, since kernel is broken.

Once kernel crash happens the kernel crash handler uses kexec mechanism to boot dump capture kernel. Please note that memory with primary kernel is untouched and accessible from dump capture kernel as seen at the moment of crash. Once dump capture kernel is booted, the kdump script will make use of tools like makedumpfile and dumps the Kernel Core Dump.

## Contents

	- [High level design of kernel coredump](#high-level-design-of-kernel-coredump)
	- [Contents](#contents)
	- [Responsibilities](#responsibilities)
	- [Design choices](#design-choices)
	- [Internal structure](#internal-structure)
	- [Configuration](#configuration)
		- [1.  Bulid kernel witth enabling debug flags](#1-bulid-kernel-witth-enabling-debug-flags)
		- [2.  configure kdump parameters](#2-configure-kdump-parameters)
		- [3.  Boot Loader Configuration](#3-boot-loader-configuration)
	- [How kernel vmcore is generated](#how-kernel-vmcore-is-generated)
	- [Supported platforms](#supported-platforms)

## Responsibilities

The primary goal of the kernel coredump module is to generate and store sufficient information of the crashed kernel for debugging purpose.

## Design choices


The design choices made for kernel coredump module are:
- Core file is compressed and archived with build,release information file(/etc/os-release )
- Corefile is stored at /var/diagnostics/coredump/ .
- Default format to capture vmcore is ELF. It supports ELF and KDUMP format to capture vmcore. Format changing can be done by changing kdump config file(/etc/kdump.conf).
- Our primary , secondary requirements for compression are time and memory.  When the System Kernel is crashed we want to dump the coredump and bring back the system to stable state as soon as possible.  Hence GZ compression is used for compression of coredump since it provides compression in lowest time and best compression ratio.

## Internal structure

```ditaa

+-------------------+
|Primary Kernel     | <----------------------------------------------------+
+-------+-----------+                                                      |
        |                          +----------------------------------+    |
        |                 +------> |                                  |    |
        |                 |        |makedumpfile                      |    |
+-------v-----------+     |        |copy from  /proc/vmcore(RAM)      |    |
|Kernel Panic       |     |        |to <flash>/vmcore (FLASH)         |    |
+-------+-----------+     |        |                                  |    |
        |                 |        +---------------+------------------+    |
        |                 |                        |                       |
        |                 |        +---------------v------------------+    |
+-------v-----------+     |        |/etc/systemd/kdump                |    |
|Panic Handler      |     |        |tar archive vmcore                |    |
+-------+-----------+     |        |   vmcore-dmesg                   |    |
        |                 |        |tar.gz compress all               |    |
        |                 |        |                                  |    |
        |                 |        +---------------+------------------+    |
+-------v-----------+     |                        |                       |
|kexec              |     |                        |                       |
+-------+-----------+     |                        |                       |
        |                 |        +---------------v------------------+    |
        |                 |        | Reboot                           +----+
        |                 |        +----------------------------------+
+-------v-----------+     |
|Secondary Kernel   +-----+
+-------------------+

```

## Configuration
-------------
Enabling this feature on openswitch requires the following recommended configuration changes in multiple config files , which are given below .

### 1.  Bulid kernel witth enabling debug flags
         make menuconfig=>
         CONFIG_LOCALVERSION=""
         CONFIG_PHYSICAL_START=0x1000000
         CONFIG_SYSFS=y
         CONFIG_RELOCATABLE=y
         CONFIG_INITRAMFS_SOURCE=""
         CONFIG_KEXEC=y
         CONFIG_DEBUG_INFO=y
         CONFIG_CRASH_DUMP=y

### 2.  configure kdump parameters
        /etc/kdump.conf
        path /var/core
        for ELF format:
        core_collector makedumpfile -E -f --message-level 1 -d 31
        for KDUMP format:
        core_collector makedumpfile -c --message-level 1 -d 31

### 3.  Boot Loader Configuration
        boot kernel with parameter  "crashkernel=128M@0M"


## How kernel vmcore is generated
When openswitch starts, boot loader specifies the crashkernel parameter and systemd starts kdump service . This crashkernel parameter is used to reserve memory for secondary kernel.  Kdump service launches  kexec with required parameters. When an exception or NULL dereference occurs kernel panic is invoked .  Panic handler will launch secondary kernel using kexec with isolated and reserved memory space. Secondary kernel launches kdump service .  Primary kernel RAM is accessible by reading /proc/vmcore .  kdump service checks for  /proc/vmcore .  Creates vmcore in ELF or KDUMP format by makedumpfile utility. vmcore-dmesg utility generates dmesg from vmcore. Aftere finishing these  job by  makedumpfile  and vmcore-dmesg secondary kernel will reboot and boot loader will launch primary kernel .  Primary kernel will launch kdump service and  compress  vmcore core.

## Supported platforms
Following platforms are supported for this feature
- as5712
- as6712

References
----------
* [Reference Crash tool white paper] https://people.redhat.com/anderson/crash_whitepaper/

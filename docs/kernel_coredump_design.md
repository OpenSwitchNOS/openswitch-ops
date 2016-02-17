High level design of kernel coredump
=====================================

It is desirable to have the Kernel CoreDump for analysing and root causing issues related to Kernel Configuration, Kernel Code, Kernel Exceptions, Device Driver Code and Exceptions.

When the running kernel crashes due to above mentioned exceptions, it wouldnt be in a stable state to store and process its own core dump.  Hence we use utility like Kdump to dump the core dump of Crashed Kernel.

Kdump is a standard Linux mechanism to dump machine memory content on kernel crash. Kdump internally uses collection of tools like Kexec, makedumpfile etc. to perform core dump.  In order to perform this task KDump needs a stable running kernel.  Hence Kdump utilizes two kernels: system kernel and dump capture kernel. System kernel is the normal kernel that is booted with special kdump-specific flags.  Dump Capture Kernel is the Kernel which will take control when the System Kernel has crashed.  Its primary objective is to dump the Kernel Core Dump and reboot the system as early as possible.   In the boot option of System Kernel we additionally need to specify/reserve some amount of physical memory where dump-capture kernel will be loaded.  The boot script of System Kernel will be configured to load the dump capture kernel in advance because at the moment crash happens there is no way to read any data from disk to load the Dump Capture Kernel, since kernel is broken.

Once kernel crash happens the kernel crash handler uses Kexec mechanism to boot dump capture kernel. Please note that memory with system kernel is untouched and accessible from dump capture kernel as seen at the moment of crash. Once dump capture kernel is booted, the KDump script will make use of tools like makedumpfile and dumps the Kernel Core Dump.

Kexec is a system call that enables you to load and boot into another kernel from the currently running kernel. This is useful for kernel developers or other people who need to reboot very quickly without waiting for the whole BIOS boot process to finish. Note that kexec may not work correctly for you due to devices not fully re-initializing when using this method, however this is rarely the case.

[toc]


Responsibilities
---------------
The primary goal of the kernel coredump module is to generate and store sufficient information of the crashed kernel for debugging purpose.

Design choices
--------------

The design choices made for kernel coredump module are:
-core file archive shall contaion build/release information with vmcore.
-core file is compressed and archived with build,release information file(/etc/os-release )
-Default path for kernel coredump is /var/core/kernel-core/vmcore.
-Default format to capture vmcore is ELF. It supports ELF and KDUMP format to capture vmcore.
Format changing can be done by changing KDump config file(/etc/kdump.conf).
-Our primary , secondary requirements for compression are time and memory.  When the System Kernel is crashed we want to dump the coredump and bring back the system to stable state as soon as possible.  Hence GZ compression is used for compression of coredump since it provides compression in lowest time and best compression ratio.

Internal structure
------------------
```ditaa

+-------------------+
| System Kernel     | <----------------------------------------------------+
+-------+-----------+                                                      |
        |                          +----------------------------------+    |
        |                 +------> |/etc/systemd/kdump                |    |
        |                 |        |makedumpfile                      |    |
+-------v-----------+     |        |copy from  /proc/vmcore(RAM)      |    |
|Kernel Panic       |     |        |to <flash>/vmcore (FLASH)         |    |
+-------+-----------+     |        |                                  |    |
        |                 |        +---------------+------------------+    |
        |                 |                        |                       |
        |                 |        +---------------v------------------+    |
+-------v-----------+     |        |/etc/systemd/kdump                |    |
|Panic Handler      |     |        |tar archive vmcore                |    |
+-------+-----------+     |        |   build/release info             |    |
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
|Dump Capture Kernel+-----+
+-------------------+

```



Configuration
-------------
Enabling this feature on openswitch requires the following recommended configuration changes in multiple config files , which are given below .

####1.	Bulid kernel witth enabling debug flags
         make menuconfig=>
         CONFIG_LOCALVERSION="-kdump"
         CONFIG_PHYSICAL_START=0x1000000
         CONFIG_SYSFS=y
         CONFIG_HIGHMEM4G=y
         CONFIG_RELOCATABLE=y
         CONFIG_INITRAMFS_SOURCE=""
         CONFIG_KEXEC=y
         CONFIG_DEBUG_INFO=y
         CONFIG_CRASH_DUMP=y


####2.	bitbake configuration  local.conf
        INITRAMFS_IMAGE_BUNDLE = "1"           (build initramfs with bzImage )
        INITRAMFS_IMAGE = "core-image-minimal-initramfs"
        EXTRA_IMAGE_FEATURES = "dbg-pkgs"     (this is same as gcc -g option)

####3.  configure kdump parameters
        /etc/kdump.conf
        path /var/core
        for ELF format:
        core_collector makedumpfile -E -f --message-level 1 -d 31
        for KDUMP format:
        core_collector makedumpfile -c --message-level 1 -d 31

        /etc/sysconfig/kdump
        KDUMP_IMG="bzImage"

  These config files are required by kdump script

####4.  Boot Loader Configuration
		boot kernel with parameter  "crashkernel=128M@0M" or make change in grub entry so that it will boot with it.

Repro and debug steps
---------------------
    1) ensure that kdump service is running . Start the service if kdump service is not running
    2) echo c > /proc/sysrq-trigger
    3) (repeat step 1)
    4) OBSERVE: core file saveing will start , size of kernel coredump with kdump format 48MB , ELF format 350MB
    5) system will reboot and you can see coredump file in configured location
    6) use tftp/scp to copy corefile from switch to workspace
    7) on workspace launch crash by "crash build/tmp/work/as5712-openswitch-linux/linux-ops/3.9.11-r1_as5712/package/boot/vmlinux-3.9.11 <vmcorepath>" (KDUMP format)
        on workspace launch gdb by "gdb  build/tmp/work/as5712-openswitch-linux/linux-ops/3.9.11-r1_as5712/package/boot/vmlinux-3.9.11 <vmcorepath>"  (ELF format)
    8) now run commands in crash prompt  for analysis (e.g. ps , bt , set <pid>  ...)




References
----------
* [Reference 1] https://people.redhat.com/anderson/crash_whitepaper/
* [Reference 2] http://tukaani.org/lzma/benchmarks.html
* [Reference 3] cdm.sh internal script to write core file to disk
* [Reference 4] external utility man:kexec(8), man:makedumpfile(8) , man:vmcore-dmesg(8)

# Daemon Coredump  User Guide

## Contents

- [Daemon Coredump  User Guide](#daemon-coredump-user-guide)
    - [Contents](#contents)
    - [Overview](#overview)
    - [How to use this feature](#how-to-use-this-feature)
        - [genericx86-64 platform](#genericx86-64-platform)
        - [Other platforms](#other-platforms)
        - [Troubleshooting](#troubleshooting)
        - [configuration](#configuration)
            - [Docker platform](#docker-platform)
                - [Example](#example)
            - [Other than docker platform](#other-than-docker-platform)
    - [CLI](#cli)
    - [References](#references)


## Overview
Enable openswitch to generate coredump file and store sufficient information of the crashed daemon for debugging purpose.

## How to use this feature
When a daemon is crashed it generates corefile.

### genericx86-64 platform
Core file generation is controlled by host machines sysctl kernel.core_pattern parameter.
"show cored-dump" and "copy core-dump" is not supported for this platform.

### Other platforms
"show core-dump" command is used to display the core dumps present in the system.
"copy core-dump" command is used to copy the core dump file to external tftp/sftp server. Refer copy core-dump cli document.

### Troubleshooting
Ensure at least 50MB free space for /var/diagnostic partition .

### configuration
#### Docker platform
I order to get core dump on docker, setup and configure a core dump handler in the host machine. Example configuration is given below.

##### Example
Configuration
```
sysctl kernel.core_pattern="|/tmp/cdm.sh %e %p %t"
sysctl kernel.core_uses_pid=0
sysctl kernel.core_pipe_limit=4
```

Install the following script in the /tmp/cdm.sh location.
Ensure that root user can execute this script .


```
#!/bin/sh

LIMIT=5    #default maximum limt
ARCHIVED_CORE="/tmp/core"

PROCESS_NAME=$1
PROCESS_PID=$2
TIME_STAMP=$3
CORE_NO=0

TIME_STAMP_FMT=$(date -d @${TIME_STAMP} "+%Y%m%d.%H%M%S")
if [ ! -d "${ARCHIVED_CORE}/${PROCESS_NAME}" ]; then
    mkdir -p $ARCHIVED_CORE/${PROCESS_NAME} 2> /dev/null
fi

COUNT=$(ls ${ARCHIVED_CORE}/${PROCESS_NAME}/${PROCESS_NAME}*core.tar.gz  2> /dev/null | wc -l)
((COUNT++))

if  (( COUNT >= LIMIT )) ; then
    CORE_NO=$LIMIT
else
    CORE_NO=$COUNT
fi

CORE_DIR=${ARCHIVED_CORE}/${PROCESS_NAME}
CORE_FILE=${CORE_DIR}/${PROCESS_NAME}.${CORE_NO}.${TIME_STAMP_FMT}.core

rm -f  ${CORE_DIR}/${PROCESS_NAME}.${CORE_NO}.*
cat >  ${CORE_FILE}
tar -czvf  ${CORE_FILE}.tar.gz ${CORE_FILE}
if [ $? -eq 0 ] ; then
    rm -f  ${CORE_FILE}
fi

```

#### Other than docker platform
Core dump works by default, no configuration required.

## CLI
You can use "show core-dump" cli to check daemon core file lists.
You can take out this core file by using "copy core-dump" command to external tftp/sftp server.

## References
* [ Daemon coredump design document ] daemon_coredump_design.md
* [ Daemon coredump user guide ] daemon_coredump_user_guide.md

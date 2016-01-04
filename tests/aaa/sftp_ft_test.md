# SFTP Feature Test Cases

## Contents
   - [Verify SFTP server](#verify-sftp-server)
   - [Verify SFTP client](#verify-sftp-client)

## Verify SFTP server
### Objective
Verify SFTP server functionality.
### Requirements
The requirements for this test case are:
 - RTL
 - 1 switch
 - 1 workstation

### Setup
#### Topology Diagram
    ```ditaa

                    +---+----+        +--------+
                    |        |        |        |
                    + dut1   +--------| host1  |
                    |        |        |        |
                    +--------+        +--------+
    ```
#### Test setup
On dut1 CLI, enter the configure terminal and set an IP address.

### Test case 1.01
Test case checks if host1 can download a file from dut1 when SFTP server is disabled by default.
### Description
From host1, perform an SFTP get from dut1.
### Test result criteria
#### Test pass criteria
On host1, SFTP get failed.
#### Test fail criteria
On host1, SFTP get succeeded.

### Test case 1.02
Test case enables the SFTP server service on dut1 and then host1 copies a file.
### Description
On dut1 CLI, in configure terminal and execute, `sftp server enable`.
From host1, perform an SFTP get from dut1.
### Test result criteria
#### Test pass criteria
On host1, SFTP get succeeded.
#### Test fail criteria
On host1, SFTP get failed.

### Test case 1.03
Test case performs an SFTP put from host1 to dut1 when SFTP server is enabled.
### Description
From host1, perform an SFTP put to dut1.
### Test result criteria
#### Test pass criteria
On host1, SFTP put succeeded.
#### Test fail criteria
On host1, SFTP put failed.

### Test case 1.04
Test case disables the SFTP service on dut1 and then host1 copies a file.
### Description
On dut1 CLI, in configure terminal and execute, `no sftp server enable`.
From host1, perform an SFTP get from dut1.
### Test result criteria
#### Test pass criteria
On host1, SFTP get failed.
#### Test fail criteria
On host1, SFTP get succeeded.

### Test case 1.05
Test case performs an SFTP put from host1 to dut1 when SFTP server is disabled.
### Description
From host1, perform an SFTP put to dut1.
### Test result criteria
#### Test pass criteria
On host1, SFTP put failed.
#### Test fail criteria
On host1, SFTP put succeeded.

## Verify SFTP client
### Objective
Verify SFTP client functionality.
### Requirements
The requirements for this test case are:
 - RTL
 - 2 switches

### Setup
#### Topology Diagram
    ```ditaa

                    +---+----+        +--------+
                    |        |        |        |
                    + dut1   +--------| dut2   |
                    |        |        |        |
                    +--------+        +--------+
    ```
#### Test setup
On dut2, enable the SFTP server.
On dut2 CLI, enter the configure terminal and set an IP address.

### Test case 2.01
Test case to verify non-interactive SFTP client get to a specific destination.
### Description
On dut1 CLI, enter the command `copy sftp <user-name> <hostIP> <source-path> <destination-path>`.
### Test result criteria
#### Test pass criteria
On dut1, SFTP get succeeded.
#### Test fail criteria
On dut1, SFTP get failed.

### Test case 2.02
Test case to verify non-interactive SFTP get to default destination.
### Description
On dut1 CLI, enter the command `copy sftp <user-name> <hostIP> <source-path>`.
### Test result criteria
#### Test pass criteria
On dut1, SFTP get succeeded.
#### Test fail criteria
On dut1, SFTP get failed.

### Test case 2.03
Test case to verify interactive SFTP client get.
### Description
On dut1 CLI, enter the command `copy sftp <user-name> <hostIP>`.
In interactive mode on dut1, perform `get <source-path> <destination-path>`.
### Test result criteria
#### Test pass criteria
On dut1, SFTP interactive get succeeded.
#### Test fail criteria
On dut1, SFTP interactive get failed.

### Test case 2.04
Test case to verify interactive SFTP client put.
### Description
On dut1 CLI, enter the command `copy sftp <user-name> <hostIP>`.
In interactive mode on dut1, perform `put <source-path> <destination-path>`.
### Test result criteria
#### Test pass criteria
On dut1, SFTP interactive put succeeded.
#### Test fail criteria
On dut1, SFTP interactive put failed.

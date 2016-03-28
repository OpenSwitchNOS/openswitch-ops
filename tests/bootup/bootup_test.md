# Boot Up Test Case

## Contents
- [Boot Up Verification](#boot-up-verification)

## Boot Up Verification
### Objective
The test case verifies that all platform daemons are up and running. It also parses the log files to detect any errors logged by the platform daemons.

### Requirements
The requirements for this test case are:
 - Two Switches
 - One Host

### Setup
#### Topology diagram

```ditaa
+--------+      +---------+    +----------+
|        |      |         |    |          |
| Host 1 +------+  SW 1   +----+   SW 2   |
|        |      |         |    |          |
+--------+      +---------+    +----------+
```

#### Test Setup
**Switch 1** is confiured with:
    ```
    !
    vlan 1
        no shutdown
    interface 1
        no shutdown
        ip address 10.0.30.2/24
    interface 2
        no shutdown
        ip address 10.0.10.2/24
    !
    ```

**Switch 2** is confiured with:
    ```
    !
    vlan 1
        no shutdown
    interface 1
        no shutdown
        ip address 10.0.30.3/24
    !
    ```

### Description
1. Configure Switch 1 and Switch 2 in **vtysh** with the following commands:

    ***Switch 1***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 10.0.30.2/24
    interface 2
    no shutdown
    ip address 10.0.10.2/24
    ```

    ***Switch 2***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 10.0.30.3/24
    ```

2. Host ip address is configured as **10.0.10.1/24**.
3. Verify that the platform processes are running on the switches by confirming that a non-null value is displayed after executing "ps -e".
3. Verify that there are no platform error messages in the log file at **/var/log/messages**. After boot-up copy the log file  into another file and parse it for error messages using **cat /messages | grep segfault** command.
4. Verify that the switch is reachable over network by doing ping test from **Switch 2** to **Host 1**. Execute **ping 10.0.10.1/24** in the Switch 2 - **vtysh** command prompt.

### Test result criteria
#### Test pass criteria
The test case is considered passing in the following cases:

 - If all the platform daemons are up and running.
 - If no error message is logged in the log file by platform daemons while boot-up.
 - If the switch is reachable over a network. Verify by doing a IPv4-address ping test.

#### Test fail criteria
The test case is considered failing in the following cases:

- If any of the platform daemons is not running, this is verified as daemon couldn't be found in **ps -e** output.
- If the platform specific error message is logged in the system log file.
- If the ping test between **Host 1** and **Switch 1** fails.

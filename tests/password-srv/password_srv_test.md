# Password Server Test Cases

## Contents
- [Update password for netop](#Update-password-for-netop)
- [Update password with invalid old password] (#Invalid-old-password)

## Update password for netop
### Objective
The objective of the test case is to verify whether the update of password for user netop via CLI is successfully performed.

### Requirements
The requirements for this test case are:

- OpenSwitch
- Ubuntu Workstation

#### Setup
#### Topology diagram
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```

### Description
Update the password via CLI.

#### Steps

1. Connect a user 'netop' to the switch via SSH
2. Run 'password' CLI command
3. Enter the old-password 'netop' (netop is the default password for netop)
4. Enter the new password '1111'
5. Logout from SSH
6. Reconnect a user 'netop' to the switch via SSH
7. Verify that password '1111' is required to logon

### Test result criteria
#### Test pass criteria
- After step 4, "Password update executed successfully." must be output by CLI
- Logon must be successful using a new password '1111' at step 6

#### Test fail criteria
- After step 4, "Password update executed successfully." is not shown
- Logon cannot be done with a new password at step 6

## Invalid old password
### Objective
The objective of the test case is to verify the password update failure when a user
did not provide the correct password.

### Requirements
The requirements for this test case are:

- OpenSwitch
- Ubuntu Workstation

#### Setup
#### Topology diagram
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```

### Description
User 'netop' provides the invalid old password to update password.

#### Steps

1. Connect a user 'netop' to the switch via SSH
2. Run 'password' CLI command
3. Enter the old-password as 'netop22' (netop is the default password for netop)
4. Enter the new password '1111'
6. Verify "Old password did not match." message is shown
6. Logout from SSH
7. Reconnect a user 'netop' to the switch via SSH
8. Verify that logon failed with a new password '1111'

### Test result criteria
#### Test pass criteria
- After step 4, CLI must show "Old password did not match."
- Logon must be failed using a new password '1111' at step 6

#### Test fail criteria
- After step 4, "Password update executed successfully." is not shown
- Logon cannot be done with a new password at step 6
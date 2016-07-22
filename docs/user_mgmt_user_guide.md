# User Management

## Contents

- [Overview](#overview)
- [Limitations](#limitations)
- [Defaults](#defaults)
- [Configuring users](#configuring-users)
    - [Adding a user](#adding-a-user)
    - [Deleting a user](#deleting-a-user)
    - [Changing user password](#Changing-user-password)
- [Verifying the configuration](#verifying-the-configuration)
    - [Viewing the configured users](#viewing-the-configured-users)
- [Troubleshooting user management](#troubleshooting-user-management)
    - [Generic tips for troubleshooting](#generic-tips-for-troubleshooting)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
The User Management feature allows users to be configured on the switch.
Only users of "admin" group have the privilege to configure users on
the switch.

## Limitations
- A maximum of eight users can be configured in a valid group.
- Users cannot be configured through a REST interface.

## Defaults
- An "admin" user is created in the "admin" group.
- A "netop" user is created in the "netop" group.

## Configuring users
### Adding a user
Login into the switch as an "admin" group user.
Issue the following command to add a new user:

```
switch#user add username group groupname
```
- A user name may only be up to 32 characters.
- The groupname should be among the below list.
    - admin
    - netop
- The command prompts for a password.
  Configure and confirm a password for the user.

### Deleting a user
Login into the switch as an "admin" group user.
Issue the following command to remove a previously added user:

```
switch#user remove username
```
### Changing user password
A user can change his/her own password using the `password` CLI command.

```
switch# password
Changing password for user alice
Enter old password:
Enter new password:
Confirm new password:
Password update executed successfully.
```
## Verifying the configuration
### Viewing the configured users
Login into the switch as an "admin" group user.
The `show user-list` CLI command displays the configured users on the switch
and their corresponding group names.

```
switch#show user-list
USER                 GROUP
--------------------------
admin                admin
netop                netop
```
## Troubleshooting user management
### Generic tips for troubleshooting
Contact users of the "admin" group to troubleshoot User Management feature, as only
users of "admin" group have the privilege to add/remove users on the switch.

## CLI
Click [here](/documents/user/user_mgmt_cli) for the CLI commands related to the
User Management feature.

## Related features
None


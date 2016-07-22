# User Management CLI commands

## Contents

- [Configuration commands](#configuration-commands)
       - [Create user](#create-user)
       - [Remove user](#remove-user)
       - [Change user password](#change-user-password)
- [Display commands](#display-commands)
       - [List of configured users](#List-of-configured-users)


## Configuration commands
###  Create user
#### Syntax
```
user add username group groupname
```
#### Description
This command creates a new user 'username' and adds the user to the group 'groupname'.
#### Authority
All users of the 'admin' group.
#### Parameters
| Parameter | Status   | Syntax  |	Description  |
|-----------|----------|-----------------------------|
| username  | Required | Literal | Name of the user. |
| groupname | Required | Literal | Name of the group.|
```
The list of supported group-names are:
admin
netop
```
#### Examples
```
switch#user add test1 group admin
Adding user test1
Enter password:
Confirm password: User add executed successfully.
```

###  Remove user
#### Syntax
```
user remove username
```
#### Description
This command deletes the user 'username'.
#### Authority
All users of the 'admin' group.
#### Parameters
| Parameter | Status   | Syntax  |	Description  |
|-----------|----------|-----------------------------|
| username  | Required | Literal | Name of the user. |
#### Examples
```
switch#user remove test1
User remove executed successfully.
```

### Change user password
#### Syntax
```
password
```
#### Description
This command allows a user to change his/her own password.
#### Authority
All users can change only their own password.
#### Parameters
None
#### Examples
```
switch# password
Changing password for user alice
Enter old password:
Enter new password:
Confirm new password:
Password update executed successfully.
```

## Display commands
###  List of configured users
#### Syntax
```
show user-list
```
#### Description
This command lists the configured users and their corresponding group names.
#### Authority
All users of the 'admin' group.
#### Parameters
None
#### Examples
```
switch# show user-list
USER                 GROUP
--------------------------
admin                admin
netop                netop
```

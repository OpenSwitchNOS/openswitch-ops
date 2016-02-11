# ++RBAC How-To Guide for OpenSwitch Developers++

Role-Based Access Control (RBAC) is a method for allowing or restricting an authenticated user access to resources based on a role the user has been assigned. Roles are assigned to the user when the user's account is created.

In OpenSwitch we will be using these roles to restrict a user's access to configuration changes and system management functions which include user password changing and firmware upgrades.


The diagram below shows the relationship between users, roles, and permissions.

```ditaa

     +---------+                                              +------------+
     | User 1  +---+                                     +----> Permission |
     |         |   |                                     |    |      A     |
     +---------+   |         +-------------------+       |    +------------+
                   |         |     Role Alpha    |       |
     +---------+   +--------->                   +-------+    +------------+
     | User 2  +---+         |                   |       +----> Permission |
     |         |             +-------------------+       |    |      B     |
     +---------+                                         |    +------------+
                                                         |
     +---------+             +-------------------+       |    +------------+
     | User 3  +-----+       |     Role Beta     |    +--+----> Permission |
     |         |     +------->                   +----+  |    |      C     |
     +---------+     |       |                   |    |  |    +------------+
                     |       +-------------------+    |  |
     +---------+     |                                |  |    +------------+
     | User 4  +-----+                                +--+----> Permission |
     |         |             +-------------------+    |  |    |      D     |
     +---------+             |    Role Gamma     |    |  |    +------------+
                       +----->                   +-+  |  |
     +---------+       |     |                   | |  |  |    +------------+
     | User 5  +-------+     +-------------------+ +--+--+----> Permission |
     |         |                                              |      E     |
     +---------+                                              +------------+
```

This guide documents how OpenSwitch management modules (CLI, REST, WebUI) can use the RBAC module APIs to check for a user's role and their corresponding permissions. It will provide both the API and code examples in both "C" and Python code.

## The RBAC Module

The RBAC module provides a library of functions used to retrieve or check a user's permissions.   A summary of the calls are as follows:
```
	check_user_permission(…) - Check if a user has been assigned a specific permission.
    get_user_permissions(…) – Get the list of permissions assigned to the user.
    get_user_role(…) – Get the role of the specified user.
```

### check_user_permission()
This is one of two APIs that allows the management interfaces to check and see if the authenticated user has rights to a specific permission. This routine will allow the interfaces to specify a username and permission and will return true if the user has rights to this permission, otherwise will return false.

### get_user_permission()
This is the other API that allows the management interfaces to check a users permission by retrieving a list or structure containing all the permissions that the authenticated user has right to.

### get_user_role()
This routine will return the users role in case the management interfaces have a desire to display this information to the user. The user role should not be used to make decisions on whether the user has rights to supported permission listed below.

### Supported Permissions
The following permissions will be supported:
READ_SWITCH_CONFIG - Gives the user permission to read switch configuration information.
WRITE_SWITCH_CONFIG - Gives the user permission to write switch configituration information.
SYS_MGMT - Gives the user permission to do system management tasks such as create users, change user passwords and update firmware images.

NOTE - We will not be supporting read-only access, so a user will either have both READ_SWITCH_CONFIG/WRITE_SWITCH_CONFIG permissions, or neither.

### RBAC "C" Interface routines

This section details the three API calls and how they are called from "C" code.

#### `rbac_check_user_permission`

```[C]
bool rbac_check_user_permission(const char *username, const char *permission)
```
This function returns true if the user has access to the specified permission, otherwise this function will return false.

##### const char *username
This is a pointer to a null-terminated username. This function does not authenticate the user but assumes the user has already been successfully authenticated.

##### const char *permission
This is a pointer to a null-terminated permission name. The current permissions supported by the system are:

RBAC_READ_SWITCH_CONFIG
RBAC_WRITE_SWITCH_CONFIG
RBAC_SYS_MGMT

#### `rbac_get_user_permissions`

```[C]
bool rbac_get_user_permissions(const char *username, rbac_permissions_t *permissions)
```
This function returns true if the call returned without any errors and the rbac_permission_t structure was successfully updated, otherwise it will return false.

##### const char *username
This is a pointer to a null-terminated username. This function does not authenticate the user but assumes the user has already been successfully authenticated.

##### rbac_permission_t *permissions
This is a pointer to the rbac_permission_t structure. On successful return, the count field will contain the number of permissions (null-terminated) in the array, starting at index 0;
```[C]

#define RBAC_MAX_NUM_PERMISSIONS		3   /* MAX number of permissions */
#define RBAC_MAX_PERMISSION_NAME_LEN	25 /* Max length of permission name */

typedef struct {
  int count;
  char name[RBAC_MAX_NUM_PERMISSIONS][RBAC_MAX_PERMISSION_NAME_LEN];
} rbac_permissions_t;
```

#### `rbac_get_user_role`

```[C]
bool rbac_get_user_role(const char *username, rbac_role_t *role)
```
This function returns true if the call returned without any errors and the rbac_role_t structure contains a null-terminated role name, otherwise it will return false.

##### const char *username
This is a pointer to a null-terminated username. This function does not authenticate the user but assumes the user has already been successfully authenticated.

##### rbac_role_t *role
This is a pointer to the rbac_role_t structure. On successful return, this structure will contain a null-terminated role name.
```[C]
#define RBAC_MAX_ROLE_NAME_LEN		20   /* Max length of a role name */

typedef struct {
  char role[RBAC_MAX_ROLE_NAME_LEN];
} rbac_role_t;
```

### RBAC Python Interface Routines

#### `rbac.check_user_permission`

```[Python]
rbac.check_user_permission(username, permission)
```
This function returns True if the user has access to the specified permission, otherwise this function will return false.

##### username
This is a username string. This function does not authenticate the user but assumes the user has already been successfully authenticated.

##### permission
This is the permission name string. The current permissions supported by the system are:

rbac.READ_SWITCH_CONFIG
rbac.WRITE_SWITCH_CONFIG
rbac.SYS_MGMT

#### `rbac.get_user_permissions`

```[Python]
rbac.get_user_permissions(username)
```
This function returns List of permissions that is accessible by the user.

##### username
This is a username string. This function does not authenticate the user but assumes the user has already been successfully authenticated.

#### `rbac.get_user_role`

```[Python]
rbac.get_user_role(username)
```
This function returns the role for the specified username.

##### username
This is a username string. This function does not authenticate the user but assumes the user has already been successfully authenticated.

## "C" Code Example

In order to use the rbac library, you will need to change your repo recipe to link in librbac.so (shared). These examples show how to use all three rbac interface calls.

### Example for rbac_check_user_permission()
``` [C]
#include <rbac.h>

      bool result;
      ......
      result = rbac_check_user_permission("user", RBAC_WRITE_SWITCH_CONFIG);
      if (result == true) {
         /* User has write access to the switch config */
         ...
         }
      ......
```

### Example for rbac_get_user_permissions()
``` [C]
#include <rbac.h>

     ......
     bool                 result;
     rbac_permissions_t   permission_list;
     result = rbac_get_user_permissions("user", &permission_list);
     if (result == true) {
        int i = 0;
        while (i < permission_list.count) {
           if (strcmp(permission_list.name[i], RBAC_READ_SWITCH_CONFIG) == 0) {
              /* User has read access to the switch config */
              }
           i++;
           ...
           }
        }
     ......
```

### Example for rbac_get_user_role()
``` [C]
#include <rbac.h>

     .....
     bool           result;
     rbac_role_t    role;
     result = rbac_get_user_role("user", &role);
     if (result == true) {
        /* Display the role name */
        }
     ......
```
## Python Code Example
Below are coding example for the three RBAC interface calls in Python

### Example for rbac.check_user_permission()
``` [Python]
import rbac

      ......
      result = rbac.check_user_permission("user", rbac.WRITE_SWITCH_CONFIG)
      if result == True:
         /* User has write access to switch config */
         ...
      ......
```

### Example for rbac.get_user_permissions()
``` [Python]
import rbac

     ......
     permission_list = rbac.get_user_permissions("user")
     ......
     if rbac.READ_SWITCH_CONFIG in permissions_list:
         /* User has read access to the switch config */
         ...
     ......
     if rbac.WRITE_SWITCH_CONFIG in permissions_list:
         /* User has write access to the swith config */
         ...

```

### Example for rbac.get_user_role()
``` [Python]
import rbac

     ......
     role_name = rbac.get_user_role("user")
     ......
     /* Display the role name */
     ......
```

# ++Audit Log How-To Guide for OpenSwitch Developers++

The goal of an audit log/trace feature is to track who did what.  This Guide documents how to use the Linux Audit Framework to create audit events for tracking configuration changes made by users to OpenSwitch.  It will describe the audit log functions and their parameters.  It will provided examples of their usage in both "C" and Python code.

## Trusted Applications

The Audit Framework only allows trusted applications to create audit events.  A trusted application is defined as any process running as root or a non-root process that has the CAP_AUDIT_WRITE capability set.  The *restd* process is an example of a process that runs as the root user.  The *vtysh* process is an example of a non-root process (as long as a non-root user is logged in).  In order to turn a non-root process into a trusted application, the *setcap* utility must be used.  To turn the *vtysh* process into a trusted application by the audit framwork, the following command needs to be issued:

	setcap cap_audit_write+eip /usr/bin/vtysh

This command needs to be issued after *vtysh* is built, but before the OpenSwitch image is created.  If you issue this on a running switch, you may need to reboot for the capability to take effect.  One caution about Python programs.  Since Python programs are not native executables, but are interpreted, the CAP_AUDIT_WRITE capability must be set on the Python interpreter itself.

## Supplying the User for a Configuration Change

When creating an audit event, the end user associated with the configuration change must always be noted.  There are some implementation issues you need to be aware of.  If the process which calls the audit log library function is running as the actual end user, the audit framework will automatically inject the correct user ID into the audit event record.  For example, vtysh runs with the actual uid/gid of the user that logged in.  No special provision is needed to supply the user in the audit log call.

However, if the process is running as root on behalf of one or more end users. the audit framework would always inject the root user into audit event record.  In this case, the audit log function caller **MUST** supply the user that is responsible for the configuration change as noted below.

## The Audit Log Library

The Audit Framework provides a library of functions used to create audit event records.  There are bindings for *C/C++*, *Python*, and *Go*.  A summary of the calls are as follows:

	audit_open() - Initiate a connection to the audit framework for subsequent audit calls.
    audit_encode_nv_string(…) – Used to encode user supplied data to prevent injection attacks.
    audit_log_user_message(…) – Log a general configuration change to the switch.
    audit_log_user_command(…) – Log a user command.  Only needed if you schedule a program
								which modifies the switch configuration.
    audit_log_acct_message(…) – Log changes to user accounts (add/delete/role change/etc).
    audit_log_comm_message(…) – Log a console app message while executing a script.  Probably will not be used.

Each of these functions have an associated man page.  You can look them up in your browser, or install them on your local VM using the folowing command:

	sudo apt-get install auditd

Many of the parameters used in the audit_log...() function calls are common.  These will be described in the next section followed by a detailed description of each audit log function individually.

### Common Audit Log Function Parameters

#### int audit_fd

This parameter is returned by a call to *audit_open()* and must be passed unaltered as the first parameter in all audit_log...() calls.

#### int type

This parameter is the audit event type.  There is a large number of different event types that are available whose use depend on the type of audit event data being logged.  In most cases we will use only a couple of these event types.  The full list can be found in */usr/include/libaudit.h*.  In addition, a more complete description of each event type can be found in Appendix B.2 of the [Red Hat Enterprise Linux Security Guide](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Security_Guide/sec-Audit_Record_Types.html).  We will be primarily be using the following event types:

	AUDIT_USYS_CONFIG - Used when a user-space system configuration change is detected.
    AUDIT_TRUSTED_APP - Used when system configuration change is made and the message parameter uses free-form text (rare).

Daemons and services that create audit events should also use the following events:

	AUDIT_SERVICE_START - Used to indicate the service/daemon has started.
    AUDIT_SERVICE_STOP  - Used to indicate the service/daemon has stopped.

#### const char *hostname

This parameter contains the local hostname of the switch if known. or NULL (None in Python) if unknown.  This parameter is especially important when a customer redirects the audit events to a  central remote system.   During analysis, it allows one to determine which system a given event is associated with.  It is recommended you always supply a valid hostname.

#### const char *addr

This parameter contains the remote network address of the user if known, or NULL (None in Python) if unknown.  Our http REST server code should supply this parameter as it is available in every REST request.

#### const char *tty

This parameter is the *tty* of the user if known, or NULL (None in Python) if unknown.  When NULL is supplied, the audit function will attempt to automatically figure out the user's tty.  This  parameter will normally only have a value for CLI based code.

#### int result

The result of the configuration operation.  The value 1 is used for success and the value 0 is used for failure.  Obviously this implies that the audit log call must be made after the configuration action has taken place.

###  Audit Log Functions

This section supplements the standard audit log man pages.  You should consult the audit log man page for the details on each function and its parameters.  The intention of this section is to provide OpenSwitch specific usage context and to provide critical usage infomation missing from the standard man pages.

#### `int audit_open()`

This function opens a netlink socket connection to the audit framework and returns it's file descriptor.  This file descriptor must be passed to all subsequent audit_log...() calls.  This function should only be called once in a program.

#### `char *audit_encode_nv_string(const char *name, const char *value, unsigned int vlen)`

Audit event records are made up of a set of name/value pairs.  The name parameter is one of the standard predefined audit field names.  The value parameter is the data associated with that field, which could be supplied by a user.  The primary purpose of this function is to encode user supplied data that could cause log injection attacks where malicious values could cause parsing errors in the aureport and ausearch audit utilities or other analysis utilities.  A secondary use is to encode any field's value data that contains a space, double-quote, or control character.  You should only use field names that expect encoded data as these are the only fields that will be decoded when displaying the event data.  This function returns a pointer to a malloc'ed string.  C programs must free this string after use.

The vlen parameter must be set to zero (0) unless the data contains an embedded null, in which case it is set to the actual length of the data.

The full list of field names and their expected formats can be found in the "How to write good events" white paper on the Audit Framework web site at [http://people.redhat.com/sgrubb/audit/audit-events.txt](http://people.redhat.com/sgrubb/audit/audit-events.txt).


```[C]
int audit_log_user_message(int audit_fd, int type, const char *message,
						   const char *hostname, const char *addr, const char *tty, int result)
```

This is the main function developers will use to generate a general user audit event.  The message parameter should contain a set of field name/value pairs each separated by a space.  The general form is`<field name>=<value>`.  The primary field names that most calls will use is *op*, *data*, and *user*.  However, additional fields may be needed depending on the nature on the event and it's data.  The previous section has a link to the full list of field names.  You can also find a description of the field names in Appendix B.1 of the [Red Hat Enterprise Linux Security Guide](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Security_Guide/app-Audit_Reference.html).

The **op** field should contain a description of the configuration operation being performed.  It must not contain a space, double-quote, or control character.  If the operation would normally contain multiple words, you should replace the space with a dash or underscore character.  It is recommended that you add a short prefix representing the module creating the audit event.  Examples:

	op=RESTD:Set-hostname
    op=CLI:Disable-Port

The **data** field is expected to be in an encoded format (using *audit_encode_nv_string*) and should contain the data associated with the configuration change.  If there is no data, it can be ommitted.  For example, if the operation was to disable port A2, you would call `audit_encode_nv_string("data", port_name, 0)` which would return the following string:

	data="A2"

The **user** field is only used in programs that run as root (on other user different from the end user making the change).  In the context of OpenSwitch, the restd daemon.  The Audit Framework normally automatically supplies the user id and login uid (auid field) of the executing process.  In the case of the restd daemon, the user id would always be 0 (root) and the login uid would be unset.  The restd code handles REST requests from a previously authenticated user.  The user field **MUST** always be supplied in all audit events created by the restd daemon or other similar programs.  Example:

	user=fredflintstone

So putting it all together, the following two examples are what a message string might look like for the CLI (vtysh) and restd code:

	op=CLI:Disable-Port data="A2"
	op=RESTD:Set-hostname data="MyHostname" user=fredflintstone


#### int audit_log_user_command(int audit_fd, int type, const char \*command, const char *tty, int result)

This function is used when a program is scheduled to change the OpenSwitch configuration.  The command parameter is the full full text of the command being issued.   For example, if a command to change the hostname was issued, this parameter might look like:

	/bin/hostname my-new-hostname


``` [C]
int audit_log_acct_message(int audit_fd, int type, const char *pgname, const char *op, const char *name,
                           unsigned int id, const char *hostname, const char *addr, const char *tty, int result)
```

This function is used for all account manipulation operations.  This includes adding and deleting users, changing user roles, user loging and authentication, etc.  The OpenSwitch code uses PAM and the useradd and userdel utilities for these operations which have already implemented the correct audit log calls. Therefore, it is not anticipated that any OpenSwitch code will need to call this function.

However, if in the future, a custom/sophisticated Role Based Access Control  functionality is implemented.  This call may be needed to log various  "role" events.

``` {C]
int audit_log_user_comm_message(int audit_fd, int type, const char *message, const char *command,
						        const char *hostname, const char *addr, const char *tty, int result)
```

This function is  used for commands executing a script.  For exmaple *crond* wanting to say what they are executing.  This function probably will not be used by any OpenSwitch code.  Note the command and message parameters have already been documented above.

## Python Code Example (for RESTD)

Python code should be able to directly use the audit libary without any changes to your recipe files.  In this example, the following variables are assumed to contain:

	op 		- the text indicating the operation that was performed (mandatory).
    cfgdata	- the optional configuration data associated with the operation.
    user_name  - the name of the user (e.g. linux user name) issuing the REST request (mandatory).
    hostname   - the local host name of the system (or None).
    addr       - the remote IP address of the user issuing the REST request.
    result     - the value 1 or 0 indicating success or failure of the operation.
    self 	  - Is the Tornado web.RequestHandler instance (see basy.py BaseHandler class).

``` [python]
import audit
import socket

audit_fd = audit.audit_open()

cfg = ""
if (cfgdata != None):
    cfg = audit.audit_encode_nv_string("data", str(cfgdata), 0)
    if (cfg == None):
        cfg = ""		# You may want to throw a MemoryError exception

addr = self.request.remote_ip;
hostname = socket.getfqdn()
user_name = self.get_secure_cookie("user")
msg = str("op=RESTD:%s %s  user=%s" % (op, cfg, user_name))
audit.audit_log_user_message(audit_fd, audit.AUDIT_USYS_CONFIG,
                             msg, hostname, addr, None, result)
```

### RESTD Audit Log Wrapper Function

If your audit log events are substantially of the same form, it is highly recommended that you implement a wrapper function to ensure that required parameters and field values are supplied and follow a consistent format.  An example wrapper function has been implemented in the ops-restd code that you can use as is or tweak to meet your needs.  Other repos (e.g. ops-cli) should use this as the example pattern for creating their own wrapper functions.  You can find this function in *opsrest/utils/utils.py*.  The name of the function is *audit_log_user_msg*:

	audit_log_user_msg(op, cfgdata, user, hostname, addr, result)

Where:

* **op** is text representing the operation being performed.  Note that a "RESTD:" prefix is automatically added.
* **cfgdata** is the configuration data associated with the operation or None if there is no data.
* **user** is the name of the user that issued the REST request.
* **hostname** is the local host name of the system or the value None
* **addr** is the remote user's IP address or None if unknown.
* **result** is 1 if the configuration operation succeeded, otherwise the value 0 if the operation failed.


## "C" Code Example

In order to use the audit log library, you will need to change your repo recipe to link in libaudit.a (static) or libaudit.so (shared).  The build system will also need a dependency on the audit framework.  Like the Python example, this example assumes the same variables (and their contents).  This example is appropriate for creating an audit event in the vtysh (CLI) code.

``` [C
#include <libaudit.h>

int audit_fd;
char *cfg;          /* Ptr to the encoded data field/value string. */
char aubuf[160];	/* Buffer to hold the message string. */
char hostname[HOST_NAME_MAX+1];

audit_fd = audit_open();

gethostname(hostname, HOST_NAME_MAX);
strcpy(aubuf, "op=CLI:Disable-Port ");
if (cfgdata != NULL) {
    cfg = audit_encode_nv_string("data", cfgdata, 0);
    if (cfg == NULL) {
        /* Handle fatal out-of-memory condition. */
    } else {
        strncat(aubuf, cfg, 130);
        free(cfg);
    }
}

audit_log_user_message(audit_fd, AUDIT_USYS_CONFIG, aubuf, hostname, NULL, NULL, result);
```

## Interpreting and Displaying Audit Log Events

**WARNING**:  Currently the Audit Framework will not write audit events to the audit log file when running inside a docker container.  These means a physical switch will be needed to see the audit events.  The default audit log file is located at /var/log/audit/audit.log.  A typical raw log record will appear as follows:

	type=USYS_CONFIG msg=audit(1446776250.787:91): pid=540 uid=1002 auid=4294967295 ses=4294967295 msg='op=CLI:Set-Hostname data="newHostName" exe="/usr/bin/vtysh" hostname=? addr=? terminal=pts/1 res=success

This particular record was generated by prototype code calling the audit_log_user_message() function in vtysh.  Most fields are self-explanitory.  Several match the parameters supplied in the audit_log_user_message() function.  Some  fields need further explanation.

**msg=audit(1446776250.787:91)** is the time stamp and   event number.  The time stamp value is 1446776250.787 and the event number is 91.

**pid=540** is the process id of the program that made the audit log call.

**uid=1002** is the user id of the program that made the audit log call.

**auid=4294967295** is the login user id.  This specific value represents -1 for a "C" int and indicates the value is not set.

**ses=4294967295** is the session id, if any.  In this case, it is not set.

**op=CLI:Set-Hostname data="newHostName"** is the content of the message parameter passed to audit_log_user_message().

The *ausearch* utility is used to display audit log events.  Note that all audit utilities are restricted to the root user. To get an easier to read output, use the "-i" or "--interpret" option.  There are many options for this utility, so you should consult the man page.  If I issued *"ausearch -i -a 91"* to display event number 91, it would output the following:

	type=USYS_CONFIG msg=audit(11/06/15 02:17:30.787:91) : pid=540 uid=fredf auid=unset ses=unset msg='op=CLI:Set-Hostname data="newHostName"exe=/usr/bin/vtysh hostname=? addr=? terminal=pts/1 res=success'

The other main audit utility is *aureport* which is used to get a variety of summary reports.  Again, you should read the man page for details.  Running it without any options will display the following summary:

	Summary Report
	======================
	Range of time in logs: 01/08/01 07:11:42.847 - 11/06/15 03:01:02.171
	Selected time for report: 01/08/01 07:11:42 - 11/06/15 03:01:02.171
	Number of changes in configuration: 2
	Number of changes to accounts, groups, or roles: 5
	Number of logins: 0
	Number of failed logins: 0
	Number of authentications: 3
	Number of failed authentications: 5
	Number of users: 1
	Number of terminals: 5
	Number of host names: 3
	Number of executables: 8
	Number of commands: 3
	Number of files: 0
	Number of AVC's: 0
	Number of MAC events: 0
	Number of failed syscalls: 0
	Number of anomaly events: 0
	Number of responses to anomaly events: 0
	Number of crypto events: 0
	Number of integrity events: 0
	Number of virt events: 0
	Number of keys: 0
	Number of process IDs: 14
	Number of events: 92

A typical report for OpenSwitch would be a configuration report using *"aureport -c"* which would display:

	Config Change Report
	===================================
	# date time type auid success event
	===================================
	1. 11/06/15 02:17:30 USYS_CONFIG -1 yes 91
	2. 11/06/15 02:17:30 USYS_CONFIG -1 yes 93


## Additional References

* [Linux Audit Framework web site](http://people.redhat.com/sgrubb/audit/)
* ["How to to write good events" white paper](http://people.redhat.com/sgrubb/audit/audit-events.txt)
* [Linux Audit Quick Start](https://www.suse.com/documentation/sles11/singlehtml/audit_quickstart/audit_quickstart.html)
* [Red Hat Enterprise Linux 7 Security Guide](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Security_Guide/index.html)
* [SUSE Linux Enterprise Desktop 11 Security Guide](https://www.suse.com/documentation/sled11/book_security/data/book_security.html)

# Password Server

## Contents
- [Overview](#overview)
- [How to use this feature](#how-to-use-this-feature)
    - [Setting up the basic configuration](#setting-up-the-basic-configuration)
    - [Verify configuration] (#troubleshooting-the-configuration)
- [CLI](#cli)
- [Related features] (#related-features)

## Overview
The password server provides a password service to other subsystems (clients) in
OpenSwitch.

This feature provides two functionalities:

- Update user password upon reqquest
  - user must be in ovsdb-client group

- Add or remove user
  - requester must be in ops-admin group

## How to use this feature
To use the password server to update a user password, the client program
open UNIX socket connection to the password and then send request via socket.

A message must be encrypted using the public key provided by the password server.
Upon execution of the request, the password server sends the status
of operation back to the client program regardless of whether the operation is
successfully completed or not.

### Setting up the basic configuration

This feature is included in the switch image build and is enabled by default.
Since the password server uses a UNIX socket for the communication, the client
program must open UNIX socket to communicate with the password server.

To communicate with the password server, the information below is needed:
- Location of the socket descriptor created by the password server
- Location of the public key file to encrypt the message
- Operation codes
- Status codes

Above information can be found in the design document.  Design document is
located at https://git.openswitch.net/cgit/openswitch/ops-passwd-srv/tree/DESIGN.md

### Troubleshooting the configuration

#### Condition
Error in updating user password.
#### Cause
- Client program cannot connect to the password server (UNIX socket open fails)
- User password is not updated successfully
#### Remedy
- Make sure that the password server is running ('/usr/bin/ops-passwd-srv')
    - run command to list the password server daemon as below
      - 'ps aux | grep ops-passwd-srv'
      - verify '/usr/bin/ops-passwd-srv' is a running process
- Make sure user provided valid old and new password to update the password
- Make sure the client program has proper permission
    - only users from ovsdb-client group are allow to change their own password
    - only users from ovs-admin group are allow to add or remove user

## CLI
The password server is a service module, it has no CLIs of its own.

## Related features
- The password server uses crypto library to generate private/public keys.  A public
key is stored in filesystem.
- The password server uses yaml-cpp library to parse configuration
- The password server uses a UNIX socket to listen for the request
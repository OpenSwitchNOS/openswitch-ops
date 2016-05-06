# Banner feature test cases

- [Test Cases](#test-cases)
    - [Restore defaults](#restore-defaults)
    - [Restore default post-login banner](#restore-default-post-login-banner)


#Test Cases
##  Verify the custom login banners feature
### Objective
Verify the custom login banners feature
### Requirements
The requirements for this test case are:
 - Docker version 1.10 or above

### Setup
#### Topology
              +------------------------+
              |                        |
              |  Openswitch container  |
              |                        |
              +------------------------+

#### Test Setup
None.

### Test case 1.1 : Restore default pre-login banner
### Description ###
Restore the default pre-login banner and confirm the expected string is displayed in a new SSH session.
### Test Result Criteria
#### Test Pass Criteria
The banner string matches the default pre-login banner string.
#### Test Fail Criteria
The banner string does not match the default pre-login banner string.

### Test case 1.2 : Restore default post-login banner
### Description
Restore the default post-login banner and confirm the expected string is displayed in a new SSH session.
### Test Result Criteria
#### Test Pass Criteria
The banner string matches the default post-login banner string.
#### Test Fail Criteria
The banner string matches the default post-login banner string.

### Test case 2.1 : Customize the pre-login banner
### Description
Modify the pre-login banner with a known string and confirm the expected string is displayed in a new SSH session.
### Test Result Criteria
#### Test Pass Criteria
The banner string matches the known string.
#### Test Fail Criteria ####
The banner string does not match the known string.

### Test case 2.2 : Customize the post-login banner
### Description
Modify the post-login banner with a known string and confirm the expected string is displayed in a new SSH session.
### Test Result Criteria
#### Test Pass Criteria
The banner string matches the known string.
#### Test Fail Criteria ####
The banner string does not match the known string.

### Test case 3.1 : Disable the pre-login banner
### Description
Disable the pre-login banner and confirm that no text is displayed before the login prompt in a new SSH session.
### Test Result Criteria
#### Test Pass Criteria
No text is displayed before the login prompt.
#### Test Fail Criteria ####
Unexpected non-whitespace characters are displayed before the login prompt.

### Test case 3.2 : Disable the post-login banner
### Description
Disable the post-login banner and confirm that no text is displayed after the login prompt and before the shell prompt in a new SSH session.
### Test Result Criteria
#### Test Pass Criteria
No unexpected text is displayed after the login prompt and before the shell prompt.
#### Test Fail Criteria ####
Unexpected non-whitespace characters are displayed after the login prompt and before the shell prompt.

### Test case 4.1 : Display the pre-login banner
### Description
Use the show command to display the pre-login banner and confirm that it matches an expected value.
### Test Result Criteria
#### Test Pass Criteria
Displayed banner matches an expected value.
#### Test Fail Criteria
Displayed banner does not match an expected value.

### Test case 4.2 : Display the post-login banner
### Description
Use the show command to display the post-login banner and confirm that it matches an expected value.
### Test Result Criteria
#### Test Pass Criteria
Displayed banner matches an expected value.
#### Test Fail Criteria
Displayed banner does not match an expected value.

#!/usr/bin/env python

# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import pytest
import re
from smart.util import pexpect
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02",
            "topoLinks":  "lnk01:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch"}


def enterConfigShell(dut01):
    retStruct = dut01.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    return True


def configSftpServer(**kwargs):

    dut01 = kwargs.get('switchObj', None)
    condition = kwargs.get('cond', None)

    retStruct = dut01.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    dut01.DeviceInteract(command="configure terminal")

    if condition is True:
        devIntReturn = dut01.DeviceInteract(command="sftp server enable")
        dut01.DeviceInteract(command="end")
        devIntReturn = dut01.DeviceInteract(command="show running-config")
        output = devIntReturn.get('buffer')
        if 'enable' not in output:
            assert "Enable SFTP server - FAIL"
    else:
        devIntReturn = dut01.DeviceInteract(command="no sftp server enable")
        dut01.DeviceInteract(command="end")
        devIntReturn = dut01.DeviceInteract(command="show running-config")
        output = devIntReturn.get('buffer')
        if 'enable' in output:
            assert "Disable SFTP server - FAIL"

    retCode = devIntReturn.get('returnCode')
    output = devIntReturn.get('buffer')
    assert retCode == 0, "Failed to enable SFTP server"

    dut01.DeviceInteract(command="end")

    returnCls = returnStruct(returnCode=1)
    return returnCls


def interfaceMgmtConfig(**kwargs):

    dut01 = kwargs.get('switchObj', None)
    ipAddr = kwargs.get('ipAddr', None)

    if(enterConfigShell(dut01) is False):
        return False

    static = "ip static"
    dut01.DeviceInteract(command="configure terminal")
    devIntReturn = dut01.DeviceInteract(command="interface mgmt")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter the mgmt interface"
    cmd = static+" "+ipAddr
    devIntReturn = dut01.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to assign the ip static address"
    dut01.DeviceInteract(command="end")

    returnCls = returnStruct(returnCode=1)
    return returnCls


def sftp_feature(**kwargs):
    LogOutput('info', "\n############################################\n")
    LogOutput('info', "Verify SFTP feature")
    LogOutput('info', "\n############################################\n")

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)

    opsuccess = False
    copy = "copy sftp"
    username = "root"
    srcpath = "/etc/ssh/sshd_config"
    destpath = "/home/admin/"
    destfile = "trial_file"
    failMsg = "Connection reset by peer"
    invalidSrcPath = "/invalid/src_path"
    srcFailMsg = "not found"
    invalidDestPath = "/invalid/dest_file"
    destFailMsg = "No such file or directory"

    # Enabling interface mgmt on SW1.
    retStruct = interfaceMgmtConfig(switchObj=switch1, ipAddr="10.1.1.1/24")
    if retStruct.returnCode() != 0:
        assert "Unable to config mgmt interface on switch1"
    LogOutput('info', "Enable interface mgmt on switch1 - SUCCESS")

    # Enabling interface mgmt on SW2
    retStruct = interfaceMgmtConfig(switchObj=switch2, ipAddr="10.1.1.2/24")
    if retStruct.returnCode() != 0:
        assert "Unable to config mgmt interface on switch2"
    LogOutput('info', "Enable interface mgmt on switch2 - SUCCESS")

    # Enable SFTP server on SW2
    retStruct = configSftpServer(switchObj=switch2, cond=True)
    if retStruct.returnCode() != 0:
        assert "switch2 SFTP server is disabled."
    LogOutput('info', "Enable SFTP server on switch2 - SUCCESS")

    # SFTP operations.
    if(enterConfigShell(switch1) is False):
        return False

    hostip = "10.1.1.2"
    cmd = copy+" "+username+" "+hostip+" "+srcpath+" "+destpath+destfile
    switch1.expectHndl.send(cmd)
    switch1.expectHndl.send('\r')
    time.sleep(1)
    switch1.expectHndl.send("yes")
    switch1.expectHndl.send('\r')
    time.sleep(1)

    # Verify the downloaded file
    devIntReturn = switch1.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter the bash shell"

    cmd1 = "ls "+destpath+destfile
    out = switch1.DeviceInteract(command=cmd1)

    if destpath+destfile in out.get('buffer') and \
       "No such file" not in out.get('buffer'):
        opsuccess = True
        LogOutput('info', "Downloaded file found")
        cmd2 = "rm -rf "+destpath+destfile
        devIntReturn = switch1.DeviceInteract(command=cmd2)
        retCode = devIntReturn.get('returnCode')
        assert retCode == 0, "Failed to erase the downloaded file"
        LogOutput('info', "Downloaded file clean up - SUCCESS")
        LogOutput('info', "Verification of SFTP get operation - SUCCESS")

    switch1.DeviceInteract(command="exit")
    assert opsuccess is True, "Verification of SFTP get operation failed"

    # Interactive mode - get operation
    opsuccess = False
    cmd = copy+" "+username+" "+hostip
    switch1.expectHndl.send(cmd)
    switch1.expectHndl.send('\r')
    time.sleep(1)

    # Perform get operation
    getcmd = "get"+" "+srcpath+" "+destpath+destfile
    switch1.expectHndl.send(getcmd)
    switch1.expectHndl.send('\r')
    time.sleep(1)

    switch1.DeviceInteract(command="quit")

    # Verify the interactive get operation
    devIntReturn = switch1.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter the bash shell"

    cmd1 = "ls "+destpath+destfile
    out = switch1.DeviceInteract(command=cmd1)

    if destpath+destfile in out.get('buffer') and \
       "No such file" not in out.get('buffer'):
        opsuccess = True
        LogOutput('info', "Downloaded file found")
        cmd2 = "rm -rf "+destpath+destfile
        devIntReturn = switch1.DeviceInteract(command=cmd2)
        retCode = devIntReturn.get('returnCode')
        assert retCode == 0, "Failed to erase the downloaded file"
        LogOutput('info', "Downloaded file clean up - SUCCESS")
        LogOutput('info', "Verification of interactive SFTP "
                          "get operation - SUCCESS")

    switch1.DeviceInteract(command="exit")
    assert opsuccess is True, "Verification of SFTP get operation failed"

    # Interactive mode - put operation
    opsuccess = False
    cmd = copy+" "+username+" "+hostip
    switch1.expectHndl.send(cmd)
    switch1.expectHndl.send('\r')
    time.sleep(1)

    # Perform put operation
    putcmd = "put"+" "+srcpath+" "+destpath+destfile
    switch1.expectHndl.send(putcmd)
    switch1.expectHndl.send('\r')
    time.sleep(1)

    switch1.DeviceInteract(command="quit")

    # Verify the interactive put operation
    if(enterConfigShell(switch2) is False):
        return False

    devIntReturn = switch2.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter the bash shell"

    cmd1 = "ls "+destpath+destfile
    out = switch2.DeviceInteract(command=cmd1)

    if destpath+destfile in out.get('buffer') and \
       "No such file" not in out.get('buffer'):
        opsuccess = True
        LogOutput('info', "Uploaded file found")
        cmd2 = "rm -rf "+destpath+destfile
        devIntReturn = switch2.DeviceInteract(command=cmd2)
        retCode = devIntReturn.get('returnCode')
        assert retCode == 0, "Failed to erase the uploaded file"
        LogOutput('info', "Uploaded file clean up - SUCCESS")
        LogOutput('info', "Verification of interactive SFTP "
                          "put operation - SUCCESS")

    switch2.DeviceInteract(command="exit")
    assert opsuccess is True, "Verification of SFTP put operation failed"

    # SFTP operation after server is disabled

    # Disable SFTP server on SW2
    retStruct = configSftpServer(switchObj=switch2, cond=False)
    if retStruct.returnCode() != 0:
        assert "switch2 disable SFTP server - FAILED."
    LogOutput('info', "Disable SFTP server on switch2 - SUCCESS")

    # Perform SFTP operation on SW1
    cmd = copy+" "+username+" "+hostip+" "+srcpath+" "+destpath+destfile
    out = switch1.DeviceInteract(command=cmd)

    if failMsg in out.get('buffer'):
        LogOutput('info', "Verify SFTP get after SFTP "
                          "server disable - SUCCESS")
    else:
        LogOutput('error', "Verify SFTP get after SFTP "
                           "server disable - FAILED")
        assert "Verification of SFTP get post SFTP " \
               "server disable failed"

    ###### Negative Test Cases ######
    LogOutput('info', "\n###### Negative Test Cases ######\n")

    # Enable SFTP server on SW2.
    retStruct = configSftpServer(switchObj=switch2, cond=True)
    if retStruct.returnCode() != 0:
        assert "switch2 enable SFTP server - FAILED."
    LogOutput('info', "Enable SFTP server on switch2 - SUCCESS")

    # Invalid source path test
    cmd = copy+" "+username+" "+hostip+" "+invalidSrcPath+" "+destpath+destfile
    out = switch1.DeviceInteract(command=cmd)

    if srcFailMsg in out.get('buffer'):
        LogOutput('info', "Verify invalid source path test - SUCCESS")
    else:
        LogOutput('error', "Verify invalid source path test - FAILED")
        assert "Verification of SFTP get with invalid source path failed"

    # Invalid destination path test
    cmd = copy+" "+username+" "+hostip+" "+srcpath+" "+invalidDestPath
    out = switch1.DeviceInteract(command=cmd)

    if destFailMsg in out.get('buffer'):
        LogOutput('info', "Verify invalid destination path test - SUCCESS")
    else:
        LogOutput('error', "Verify invalid destination path test - FAILED")
        assert "Verification of SFTP get with invalid destination path failed"

    return True


def switch_reboot(deviceObj):
    # Reboot switch
    LogOutput('info', "Reboot switch " + deviceObj.device)
    deviceObj.Reboot()
    rebootRetStruct = returnStruct(returnCode=0)
    return rebootRetStruct


def sftpRebootTest(**kwargs):
    LogOutput('info', "\n############################################\n")
    LogOutput('info', "Verify SFTP feature post reboot")
    LogOutput('info', "\n############################################\n")

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)

    opsuccess = False
    copy = "copy sftp"
    username = "root"
    srcpath = "/etc/ssh/sshd_config"
    destpath = "/home/admin/"
    destfile = "trial_file"

    # Enabling interface mgmt on SW1
    retStruct = interfaceMgmtConfig(switchObj=switch1, ipAddr="10.1.1.1/24")
    if retStruct.returnCode() != 0:
        assert "Unable to config mgmt interface on switch1"
    LogOutput('info', "Enable interface mgmt on switch1 - SUCCESS")

    # Enabling interface mgmt on SW2
    retStruct = interfaceMgmtConfig(switchObj=switch2, ipAddr="10.1.1.2/24")
    if retStruct.returnCode() != 0:
        assert "Unable to config mgmt interface on switch2"
    LogOutput('info', "Enable interface mgmt on switch2 - SUCCESS")

    # Enable SFTP server on SW2
    retStruct = configSftpServer(switchObj=switch2, cond=True)
    if retStruct.returnCode() != 0:
        assert "switch2 SFTP server is disabled."
    LogOutput('info', "Enable SFTP server on switch2 - SUCCESS")

    # SFTP operations before reboot
    if(enterConfigShell(switch1) is False):
        return False

    hostip = "10.1.1.2"
    cmd = copy+" "+username+" "+hostip+" "+srcpath+" "+destpath+destfile
    switch1.expectHndl.send(cmd)
    switch1.expectHndl.send('\r')
    time.sleep(1)

    # Verify the downloaded file
    devIntReturn = switch1.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter the bash shell"

    cmd1 = "ls "+destpath+destfile
    out = switch1.DeviceInteract(command=cmd1)

    if destpath+destfile in out.get('buffer') and \
       "No such file" not in out.get('buffer'):
        opsuccess = True
        LogOutput('info', "Downloaded file found")
        cmd2 = "rm -rf "+destpath+destfile
        devIntReturn = switch1.DeviceInteract(command=cmd2)
        retCode = devIntReturn.get('returnCode')
        assert retCode == 0, "Failed to erase the downloaded file"
        LogOutput('info', "Downloaded file clean up - SUCCESS")
        LogOutput('info', "Verification of SFTP before reboot - SUCCESS")

    switch1.DeviceInteract(command="exit")
    assert opsuccess is True, "Verification of SFTP before reboot failed"

    # Save the configuration on SW2.
    if(enterConfigShell(switch2) is False):
        return False

    runCfg = "copy running-config startup-config"
    devIntReturn = switch2.DeviceInteract(command=runCfg)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to save the running configuration"

    # Perform reboot of SW2.
    devRebootRetStruct = switch_reboot(switch2)
    if devRebootRetStruct.returnCode() != 0:
        LogOutput('error', "Switch2 reboot - FAILED")
        assert(devRebootRetStruct.returnCode() == 0)
    else:
        LogOutput('info', "Switch2 reboot - SUCCESS")

    # SFTP operation after reboot.
    opsuccess = False
    cmd = copy+" "+username+" "+hostip+" "+srcpath+" "+destpath+destfile
    switch1.expectHndl.send(cmd)
    switch1.expectHndl.send('\r')
    time.sleep(1)

    # Verify the downloaded file
    devIntReturn = switch1.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter the bash shell"

    cmd1 = "ls "+destpath+destfile
    out = switch1.DeviceInteract(command=cmd1)

    if destpath+destfile in out.get('buffer') and \
       "No such file" not in out.get('buffer'):
        opsuccess = True
        LogOutput('info', "Downloaded file found")
        cmd2 = "rm -rf "+destpath+destfile
        devIntReturn = switch1.DeviceInteract(command=cmd2)
        retCode = devIntReturn.get('returnCode')
        assert retCode == 0, "Failed to erase the downloaded file"
        LogOutput('info', "Downloaded file clean up - SUCCESS")
        LogOutput('info', "Verification of SFTP after reboot - SUCCESS")

    switch1.DeviceInteract(command="exit")
    assert opsuccess is True, "Verification of SFTP after reboot failed"

    return True


class Test_sftpfeature:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_sftpfeature.testObj =\
            testEnviron(topoDict=topoDict, defSwitchContext="vtyShell")
        # Get topology object
        Test_sftpfeature.topoObj = \
            Test_sftpfeature.testObj.topoObjGet()

    def teardown_class(cls):
        Test_sftpfeature.topoObj.terminate_nodes()

    def test_sftp_feature(self):
        # GEt Device objects
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        retValue = sftp_feature(switch1=dut01Obj, switch2=dut02Obj)
        if retValue is not True:
            LogOutput('info', "\n Test SFTP feature - FAILED\n")
            assert " SFTP feature - FAILED"
        else:
            LogOutput('info', "\n Test SFTP feature - PASSED\n")

    def test_post_reboot(self):
        # Get device objects
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        devRebootRetStruct = sftpRebootTest(switch1=dut01Obj, switch2=dut02Obj)
        if devRebootRetStruct is not True:
            LogOutput('info', "\n SFTP feature post reboot - FAILED\n")
            assert "SFTP feature post reboot"
        else:
            LogOutput('info', "\n SFTP feature post reboot - PASSED\n")

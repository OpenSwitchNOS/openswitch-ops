
#Copyright (C) 2016 Hewlett Packard Enterprise Development LP
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
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *

#NTP server IPs
global WORKSTATION_IP_ADDR_SER1
global WORKSTATION_IP_ADDR_SER2


# Topology definition
topoDict = {"topoExecution": 3000,
            "topoTarget": "dut01",
            "topoDevices": "dut01 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,lnk02:dut01:wrkston02",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston01:docker-image:openswitch/centos_ntp,\
                            wrkston02:system-category:workstation,\
                            wrkston02:docker-image:openswitch/centos_ntp",
            "topoLinkFilter": "lnk01:dut01:interface:1,lnk02:dut01:interface:2"}


def switchWsConfig(dut01, wrkston01, wrkston02):
    global WORKSTATION_IP_ADDR_SER1
    global WORKSTATION_IP_ADDR_SER2
    info('### Configuring workstation 1###\n')
    wrkston01.cmd("echo \"authenticate yes\" >> /etc/ntp.conf")
    wrkston01.cmd("ntpd -c /etc/ntp.conf")
    ifConfigCmdOut = wrkston01.cmd("ifconfig eth0")
    lines = ifConfigCmdOut.split('\n')
    target = 'inet'
    for line in lines:
        word = line.split()
        for i,w in enumerate(word):
            if w == target:
               WORKSTATION_IP_ADDR_SER1 = word[i+1]
               break

    info('### Configuring workstation 2###\n')
    wrkston02.cmd("ntpd -c /etc/ntp.conf")
    ifConfigCmdOut = wrkston02.cmd("ifconfig eth0")
    lines = ifConfigCmdOut.split('\n')
    target = 'inet'
    for line in lines:
        word = line.split()
        for i,w in enumerate(word):
            if w == target:
               WORKSTATION_IP_ADDR_SER2 = word[i+1]
               break

    devIntReturn = dut01.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter bash shell"
    info("\n###Configuring Switch###\n")
    dut01.cmdVtysh(command="vtysh")
    dut01.cmdVtysh(command="configure terminal")
    dut01.cmdVtysh(command="ntp authentication-key 55 md5 secretpassword")
    dut01.cmdVtysh(command="ntp trusted-key 55")
    dut01.cmdVtysh(command="ntp authentication enable")
    dut01.cmdVtysh(command="ntp server %s prefer key 55" % WORKSTATION_IP_ADDR_SER1)
    dut01.cmdVtysh(command="ntp server %s prefer " % WORKSTATION_IP_ADDR_SER2)

def validateNtpAssociationInfo(dut01, wrkston01, wrkston02):
    global WORKSTATION_IP_ADDR_SER1
    global WORKSTATION_IP_ADDR_SER2
    out = dut01.cmdVtysh(command="do show ntp associations")
    print(out)
    lines = out.split('\n')
    for line in lines:
        if WORKSTATION_IP_ADDR_SER1 in line:
           if ('.NKEY.' or '.INIT.' or '.TIME.' or '.RATE.' or '.AUTH.') in line:
              return False
    return True

def validateNtpStatus(dut01, wrkston01, wrkston02):
    out = dut01.cmdVtysh(command="do show ntp status")
    print(out)
    if 'Synchronized' in out:
	return True
    out = dut01.cmdVtysh(command="do show ntp associations")
    print(out)
    return False

#timeout increased to provide enough time to download the images from docker hub
@pytest.mark.timeout(900)
class Test_Ntpserver_Feature:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_Ntpserver_Feature.testObj =\
            testEnviron(topoDict=topoDict, defSwitchContext="vtyShell")
        #Get topology object
        Test_Ntpserver_Feature.topoObj = \
            Test_Ntpserver_Feature.testObj.topoObjGet()

    def teardown_class(cls):
	    Test_Ntpserver_Feature.topoObj.terminate_nodes()


    def test_feature(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        switchWsConfig(dut01Obj, wrkston01Obj, wrkston02Obj)
        #timeout selected as per the reference max ntp association time period
        total_timeout = 600
	timeout = 1
	check1 = False
	check2 = False
	for t in range(0,total_timeout,timeout):
            sleep(timeout)
            if check1 == False:
		    check1 = validateNtpAssociationInfo(dut01Obj, wrkston01Obj, wrkston02Obj)
            if check2 == False:
		    check2 = validateNtpStatus(dut01Obj, wrkston01Obj,  wrkston02Obj)
            if check1 == True and check2 == True:
                info("\n###NTP Functionality is working and has been validated###\n")
                return
	if check1 == False:
		error("\n###NTP Association info could not be validated###\n")
	if check2 == False:
		error("\n###NTP status info could not be validated###\n")
        error("\n###Timeout occured, NTP config failed###\n")

# (C) Copyright 2015 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
##########################################################################
# Name:        VlanName.py
#
# Description: Verify that a VLAN string name has a limit to the amount of
#             characters it can accept and VLAN name string will not
#             accept duplicate names of existing VLAN's in the system
#
# Author:      Roy Ibarra
#
# Topology:      |Switch|
#
# Success Criteria:  PASS -> Up to 32 alphanumeric characters to name the VLAN
#                            can be used and no duplicate names are accepted.
#
#                    FAILED -> No more than 250 alphanumeric characters
#                              accepted for VLAN's name or duplicate
#                              names were configured.
#
##########################################################################

import pytest
from opstestfw import *
from opstestfw import testEnviron
from opstestfw.switch.CLI import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01",
            "topoDevices": "dut01",
            "topoFilters": "dut01:system-category:switch"}


def showVlanDescription(**kwargs):
    deviceObj = kwargs.get('deviceObj', None)

    overallBuffer = []
    # If Device object is not passed, we need to error out
    if deviceObj is None:
        LogOutput('error', "Need to pass switch device object deviceObj \
        and VLAN Id vlanId to this routine")
        returnCls = returnStruct(returnCode=1)
        return returnCls

    # Get into vtyshelll
    returnStructure = deviceObj.VtyshShell(enter=True)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        LogOutput('error', "Failed to get vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=1, buffer=bufferString)
        return returnCls

    command = "show running-config\n"

    returnDevInt = deviceObj.DeviceInteract(command=command)
    retCode = returnDevInt['returnCode']
    overallBuffer.append(returnDevInt['buffer'])
    temporaryBuffer = returnDevInt['buffer']
    if retCode != 0:
        LogOutput('error', "Failed to create VLAN." + command)
    else:
        LogOutput('debug', "Created VLAN." + command)

    # Get out of vtyshell
    returnStructure = deviceObj.VtyshShell(enter=False)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        LogOutput('error', "Failed to exit vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=1, buffer=bufferString)
        return returnCls

    # List of tuples containing the description of each vlan
    vlansList = re.findall(
        r'\b(vlan)\s+(\d+)\r\n\s+\b(description)\s+(\w+)', temporaryBuffer)
#    print vlansList

    result = []
    for item in vlansList:
        dictionary = {}
        dictionary[item[0]] = item[1]
        dictionary[item[2]] = item[3]
        result.append(dictionary)

    # Return results
    bufferString = ""
    for curLine in overallBuffer:
        bufferString += str(curLine)
    returnCls = returnStruct(returnCode=0, buffer=bufferString, data=result)
    return returnCls


def deviceCleanup(dut01Obj):
    returnCode = 0
    LogOutput('info', "############################################")
    LogOutput('info', "CLEANUP: Reboot the switch")
    LogOutput('info', "############################################")
    rebootRetStruct = dut01Obj.Reboot()
    rebootRetStruct = returnStruct(returnCode=0)
    if rebootRetStruct.returnCode() != 0:
        LogOutput('error', "Switch Reboot failed")
        returnCode = 1
    else:
        LogOutput('info', "Passed Switch Reboot piece")
        # Global cleanup return structure
        cleanupRetStruct = returnStruct(returnCode=returnCode)
        return cleanupRetStruct


class Test_VlanNameTC:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_VlanNameTC.testObj = testEnviron(topoDict=topoDict)
        Test_VlanNameTC.topoObj = Test_VlanNameTC.testObj.topoObjGet()
        Test_VlanNameTC.dut01Obj = Test_VlanNameTC.topoObj.deviceObjGet(
            device="dut01")

    def teardown_class(cls):
        # Terminate all nodes
        deviceCleanup(cls.dut01Obj)
        Test_VlanNameTC.topoObj.terminate_nodes()

    def test_vlan_add(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 1- Create Vlan")
        LogOutput('info', "############################################")

        devRetStruct = AddVlan(deviceObj=self.dut01Obj, vlanId=30)
        if devRetStruct.returnCode() != 0:
            LogOutput('info', "Failed to add Vlan with ID 30")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Vlan with ID 30 added to the switch")

    def test_check_vlan_status(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 2- Check Vlan 30" +
                  "was created on the switch successfully")
        LogOutput('info', "############################################")
        returnCLS = ShowVlan(deviceObj=self.dut01Obj)
        result = returnCLS.returnCode()
        # Get the list containing the output of 'show vlan'. Each position in
        # the list is a dictionary that corresponds to a row of the 'show vlan'
        showVlanOutput = returnCLS.valueGet()
        if result != 0:
            LogOutput('error', "Step failed, Unable to get the vlan table")
            assert result == 0
        else:
            myDict = showVlanOutput[0]
            if myDict['VLAN'] != "30":
                LogOutput('error', "Step failed. Vlan 30 doesn't \
                exist in the vlan table")
                assert 1 != 1
            else:
                LogOutput(
                    'info', "Passed - Vlan with ID 30 exists" +
                    "in the vlan table")

    def test_add_vlan_description(self):
        LogOutput('info', "############################################")
        LogOutput(
            'info', "Step 3- Configure a vlan description with" +
            "the text: My_first_description")
        LogOutput('info', "############################################")
        returnCLS = VlanDescription(deviceObj=self.dut01Obj, vlanId=30,
                                    description="My_first_description")
        result = returnCLS.returnCode()
        if result != 0:
            LogOutput('error', "Error when adding a description to the vlan")
            assert result == 0
        else:
            returnCLS = showVlanDescription(deviceObj=self.dut01Obj)
            showVlanOutput = returnCLS.valueGet()
            myDict = showVlanOutput[0]
            # This is to make sure that no garbage characters where added to
            # the description
            if myDict['description'] != "My_first_description":
                LogOutput('error', "Step failed. It seems that a description \
                was added but it does not correspond \
                to the text My_first_description")
                assert 1 != 1
            else:
                LogOutput(
                    'info', "Passed - Vlan with ID 30 has a description" +
                    "of My_first_description")

    def test_vlan_description_rename(self):
        LogOutput('info', "############################################")
        LogOutput(
            'info', "Step 4- Rename previous vlan description " +
            "with the text: DUT_VLAN")
        LogOutput('info', "############################################")
        returnCLS = VlanDescription(
            deviceObj=self.dut01Obj, vlanId=30, description="DUT_VLAN")
        result = returnCLS.returnCode()
        if result != 0:
            LogOutput(
                'error', "Error when changing the description of the vlan 30")
            assert result == 0
        else:
            returnCLS = showVlanDescription(deviceObj=self.dut01Obj)
            showVlanOutput = returnCLS.valueGet()
            myDict = showVlanOutput[0]
            # This is to make sure that no garbage characters where added to
            # the description
            if myDict['description'] != "DUT_VLAN":
                LogOutput('error', "Step failed. It seems that the \
                description was changed but it does not \
                correspond to the text DUT_VLAN")
                assert 1 != 1
            else:
                LogOutput(
                    'info', "Passed - Vlan with ID 30 has changed" +
                    "its description to DUT_VLAN")

    def test_vlan_description_length(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 5-  Maximum length of 250 characters " +
                  "in the VLAN description")
        LogOutput('info', "############################################")
        returnCLS = VlanDescription(deviceObj=self.dut01Obj, vlanId=30,
                                    description="Verify_that_a_VLAN_string_"
                                    + "name_has_a_limit_to_the_amount_of_"
                                    + "characters_it_can_accept_and_vlan_"
                                    + "name_string_will_not_accept_duplicate"
                                    + "_names_of_existing_vlan's_in_the"
                                    + "_system.........................."
                                    + ".............................."
                                    + ".............................")
        result = returnCLS.returnCode()
        if result != 0:
            returnCLS = showvlandescription(deviceobj=self.dut01obj)
            showvlanoutput = returnCLS.valueget()
            mydict = showvlanoutput[0]
            # in case the command was accepted, the new description should not
            # be applied
            if mydict['description'] == "verify_that_a_vlan_string_"\
                + "name_has_a_limit_to_the_amount_of_characters_it_" +\
                    "can_accept_and_vlan_name_string_will_not_accept_" +\
                    "duplicate_names_of_existing_vlan's_in_the_system" +\
                    "................................................" +\
                    ".....................................":
                logoutput('error', "step failed. vlan description with more \
                than 250 characters was applied to the switch")
                assert 1 != 1
            else:
                LogOutput('info', "passed - vlan with id 30 did not accepted a \
                    description with more than 250 characters")
        else:
            LogOutput('error', "step failed, the dut has accepted a description\
             of more than 250 characters")
            assert result == 0

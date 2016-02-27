# (C) Copyright 2015-2016 Hewlett Packard Enterprise Development LP
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
###############################################################################
# Name:        DynamicLagDeleteMaxNumberOfMembers.py
#
# Description: Tests that a previously configured dynamic Link Aggregation of 8
#              members can be deleted
#
# Author:      Jose Hernandez
#
# Topology:    |Switch| ---------------------- |Switch|
#                      (Dynamic LAG - 8 links)
#
# Success Criteria:  PASS -> LAGs are deleted when having 8 members
#
#                    FAILED -> LAGs cannot be deleted in the scenario
#                              mentioned in the pass criteria
#
###############################################################################

from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *

topoDict = {"topoExecution": 3000,
            "topoDevices": "dut01 dut02",
            "topoLinks": "lnk01:dut01:dut02,\
                          lnk02:dut01:dut02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut01:dut02,\
                          lnk05:dut01:dut02,\
                          lnk06:dut01:dut02,\
                          lnk07:dut01:dut02,\
                          lnk08:dut01:dut02",\
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch"}

# Adds interfaces to LAG


def addInterfacesToLAG(deviceObj, lagId, intArray):
    overallBuffer = []
    returnStructure = deviceObj.VtyshShell(enter=True)
    overallBuffer.append(returnStructure.buffer())
    returnCode = returnStructure.returnCode()
    if returnCode != 0:
        LogOutput('error', "Failed to get vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls

    # Get into config context
    returnStructure = deviceObj.ConfigVtyShell(enter=True)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        LogOutput('error', "Failed to get vtysh config prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls

    # Add interfaces
    for i in intArray:
        command = "interface %s\r" % str(i)
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to configure interface " +
                      str(i) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput(
                'debug', "Entered interface " + str(i) + " on device " +
                deviceObj.device)

        command = "lag %s" % str(lagId)
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to add interface " + str(i) +
                      " to LAG" + str(lagId) + " on device " +
                      deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode,
                                     buffer=bufferString)
            return returnCls
        else:
            LogOutput('info', "Added interface " + str(i) +
                      " to LAG" + str(lagId) + " on device " +
                      deviceObj.device)

        command = "exit"
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to exit configuration of interface " +
                      str(i) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput('debug', "Exited configuration of interface " +
                      str(i) + " on device " + deviceObj.device)

    # Get out of config context
    returnStructure = deviceObj.ConfigVtyShell(enter=False)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        LogOutput('error', "Failed to exit vtysh config prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls
    # Exit vtysh
    returnStructure = deviceObj.VtyshShell(enter=False)
    overallBuffer.append(returnStructure.buffer())
    returnCode = returnStructure.returnCode()
    if returnCode != 0:
        LogOutput('error', "Failed to exit vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls
    bufferString = ""
    for curLine in overallBuffer:
        bufferString += str(curLine)
    returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
    return returnCls

# Enable/disable interface on DUT


def enableDutInterface(deviceObj, int, enable):
    if enable:
        retStruct = InterfaceEnable(
            deviceObj=deviceObj, enable=enable, interface=int)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed to enable " + deviceObj.device +
                " interface " + int)
            return False
        else:
            LogOutput(
                'info', "Enabled " + deviceObj.device + " interface " + int)
    else:
        retStruct = InterfaceEnable(
            deviceObj=deviceObj, enable=enable, interface=int)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed to disable " + deviceObj.device +
                " interface " + int)
            return False
        else:
            LogOutput(
                'info', "Disabled " + deviceObj.device + " interface " + int)
    return True

# Create/delete a LAG and add interfaces


def createLAG(deviceObj, lagId, configure, intArray, mode):
    if configure:
        retStruct = lagCreation(
            deviceObj=deviceObj, lagId=str(lagId), configFlag=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to create LAG1 on " + deviceObj.device)
            return False
        else:
            LogOutput(
                'info', "Created LAG" + str(lagId) + " on " +
                deviceObj.device)
        retStruct = addInterfacesToLAG(deviceObj, 1, intArray)
        if retStruct.returnCode() != 0:
            return False
        if mode != 'off':
            retStruct = lagMode(
                lagId=str(lagId), deviceObj=deviceObj, lacpMode=mode)
            if retStruct.returnCode() != 0:
                return False
        retStruct = lacpAggregatesShow(deviceObj=deviceObj)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed to verify if LAG was created on " +
                deviceObj.device)
            return False
        if len(retStruct.dataKeys()) == 0:
            LogOutput('error', "No LAGs were configured on device")
            return False
        if retStruct.valueGet(key=str(lagId)) is None:
            LogOutput('error', "Configured LAG is not present on device")
            return False
        if len(retStruct.valueGet(key=str(lagId))['interfaces']) !=\
                len(intArray):
            LogOutput('error', "The number of interfaces in the LAG (" +
                      len(retStruct.valueGet(key=str(lagId))['interfaces']) +
                      ") does not match the configured number of " +
                      len(intArray))
            return False
        if retStruct.valueGet(key=str(lagId))['lacpMode'] != mode:
            LogOutput('error', "The LAG have been configured in LACP mode " +
                      mode + " but instead it is in LACP mode " +
                      retStruct.valueGet(key=str(lagId))['lacpMode'])
            return False
    else:
        retStruct = lagCreation(
            deviceObj=deviceObj, lagId=str(lagId), configFlag=False)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to delete LAG1 on " + deviceObj.device)
            return False
        else:
            LogOutput(
                'info', "Deleted LAG" + str(lagId) + " on " + deviceObj.device)
        retStruct = lacpAggregatesShow(deviceObj=deviceObj)
        if len(retStruct.dataKeys()) != 0:
            if retStruct.valueGet(key=str(lagId)) is not None:
                LogOutput(
                    'error', "The LAG was not deleted from configuration")
                return False
    return True


class Test_ft_framework_basics:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_ft_framework_basics.testObj = testEnviron(topoDict=topoDict)
        Test_ft_framework_basics.topoObj =\
            Test_ft_framework_basics.testObj.topoObjGet()

    def teardown_class(cls):
        # Terminate all nodes
        Test_ft_framework_basics.topoObj.terminate_nodes()

    def test_createLAGs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Create LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(createLAG(dut01Obj, '1', True, [
            dut01Obj.linkPortMapping['lnk01'],
            dut01Obj.linkPortMapping['lnk02'],
            dut01Obj.linkPortMapping['lnk03'],
            dut01Obj.linkPortMapping['lnk04'],
            dut01Obj.linkPortMapping['lnk05'],
            dut01Obj.linkPortMapping['lnk06'],
            dut01Obj.linkPortMapping['lnk07'],
            dut01Obj.linkPortMapping['lnk08']], 'active'))
        assert(createLAG(dut02Obj, '1', True, [
            dut02Obj.linkPortMapping['lnk01'],
            dut02Obj.linkPortMapping['lnk02'],
            dut02Obj.linkPortMapping['lnk03'],
            dut02Obj.linkPortMapping['lnk04'],
            dut02Obj.linkPortMapping['lnk05'],
            dut02Obj.linkPortMapping['lnk06'],
            dut02Obj.linkPortMapping['lnk07'],
            dut02Obj.linkPortMapping['lnk08']], 'passive'))

    def test_enableDUTsInterfaces(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Enable switches interfaces")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        LogOutput('info', "Configuring switch dut01")
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk01'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk02'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk03'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk04'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk05'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk06'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk07'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk08'],
                               True))

        LogOutput('info', "Configuring switch dut02")
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk01'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk04'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk05'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk06'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk07'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk08'],
                               True))

    def test_deleteLAGs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Delete LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(createLAG(dut01Obj, '1', False, [], None))
        assert(createLAG(dut02Obj, '1', False, [], None))

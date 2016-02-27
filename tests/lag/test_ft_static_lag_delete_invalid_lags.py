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
# Name:        StaticLagDeleteNonExistingLags.py
#
# Description: Tests that a previously configured static Link Aggregation does
#              not stop forwarding traffic when attempting to delete several
#              non-existent Link Aggregations with different names that may not
#              be supported
#
# Author:      Jose Hernandez
#
# Topology:    |Switch| ---------------------- |Switch|
#                       (Static LAG - 2 links)
#
# Success Criteria:  PASS -> Non-existent LAGs cannot be deleted and they
#                            don't affect the functioning LAG
#
#                    FAILED -> Functioning LAG configuration is changed or any
#                              of the non-existing LAGs don't produce errors
#                              when attempting to delete them
#
###############################################################################


from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *

topoDict = {"topoExecution": 3000,
            "topoDevices": "dut01 dut02",
            "topoLinks": "lnk01:dut01:dut02,\
                          lnk02:dut01:dut02",
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

# Function to try and delete a non-existent LAG. It assumes there is only
# 1 other LAG and then matches the information present in DUT to verify it
# wasn't modified


def deleteLAGNegative(
        deviceObj, lagId, goodLagId, goodLagMode, goodLagInterfaces,
        goodLagHash, goodLagFallback, goodLagFastFlag):
    retStruct = lagCreation(
        deviceObj=deviceObj, lagId=str(lagId), configFlag=False)
    if retStruct.returnCode() != 0:
        LogOutput('info', "Failed to delete LAG " + str(lagId) +
                  " as expected on " + deviceObj.device)
    else:
        LogOutput('error', "Deleted LAG " + str(lagId) +
                  " unexpectedly on " + deviceObj.device)
        return False
    retStruct = lacpAggregatesShow(deviceObj=deviceObj)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to verify if deleting LAG" +
                  str(lagId) + " procuded changes on device " +
                  deviceObj.device)
        return False
    if len(retStruct.dataKeys()) != 1:
        for i in retStruct.dataKeys():
            helperText += "\n" + i
        LogOutput(
            'error',
            "Expected to find only 1 LAG in configuration, found " +
            str(len(retStruct.dataKeys())) + " with the following IDs:\n" +
            helperText)
        return False
    if retStruct.dataKeys()[0] == lagId:
        LogOutput('error', "Found deleted LAG ID on device " +
                  deviceObj.device + " configuration")
        return False
    if retStruct.valueGet(key=goodLagId)['lacpMode'] != goodLagMode:
        LogOutput(
            'error',
            "Remaining LAG LACP mode altered. Expected: " + str(goodLagMode) +
            " - Found: " + str(retStruct.valueGet(key=goodLagId)['lacpMode']))
        return False
    if retStruct.valueGet(key=goodLagId)['hashType'] != goodLagHash:
        LogOutput(
            'error',
            "Remaining LAG hashing algorithm altered. Expected: " +
            str(goodLagHash) + " - Found: " +
            str(retStruct.valueGet(key=goodLagId)['hashType']))
        return False
    if retStruct.valueGet(key=goodLagId)['fallbackFlag'] != goodLagFallback:
        LogOutput(
            'error',
            "Remaining LAG fallback flag altered. Expected: " +
            str(goodLagFallback) + " - Found: " +
            str(retStruct.valueGet(key=goodLagId)['fallbackFlag']))
        return False
    if retStruct.valueGet(key=goodLagId)['lacpFastFlag'] != goodLagFastFlag:
        LogOutput(
            'error',
            "Remaining LAG fast speed setting altered. Expected: " +
            str(goodLagFastFlag) + " - Found: " +
            str(retStruct.valueGet(key=goodLagId)['lacpFastFlag']))
        return False
    if len(retStruct.valueGet(key=goodLagId)['interfaces']) !=\
            len(goodLagInterfaces):
        helperText1 = ''
        helperText2 = ''
        for i in retStruct.valueGet(key=goodLagId)['interfaces']:
            helperText1 += "\n" + i
        for i in goodLagInterfaces:
            helperText2 += "\n" + i
        LogOutput(
            'error',
            "Number of links in remaining LAG was modified. Expected: " +
            str(len(goodLagInterfaces)) + " with interfaces:\n" +
            helperText2 + "\n Found: " +
            str(len(retStruct.valueGet(key=goodLagId)['interfaces'])) +
            " with interfaces: \n" + helperText1)
        return False
    for i in goodLagInterfaces:
        found = False
        for k in retStruct.valueGet(key=goodLagId)['interfaces']:
            if i == k:
                found = True
                break
        if not found:
            LogOutput(
                'error', "Could not find interface " + i + "in remaining LAG")
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
               dut01Obj.linkPortMapping['lnk02']], 'off'))
        assert(createLAG(dut02Obj, '1', True, [dut02Obj.linkPortMapping[
               'lnk01'], dut02Obj.linkPortMapping['lnk02']], 'off'))

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

        LogOutput('info', "Configuring switch dut02")
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk01'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'],
                               True))

    def test_deleteLAGs1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Delete non-existent LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        LogOutput('info', 'With ID XX')
        assert(deleteLAGNegative(dut01Obj, 'XX', '1', 'off', [
            dut01Obj.linkPortMapping['lnk01'],
            dut01Obj.linkPortMapping['lnk02']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 0')
        assert(deleteLAGNegative(dut01Obj, '0', '1', 'off', [
            dut01Obj.linkPortMapping['lnk01'],
            dut01Obj.linkPortMapping['lnk02']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID -1')
        assert(deleteLAGNegative(dut01Obj, '-1', '1', 'off', [
            dut01Obj.linkPortMapping['lnk01'],
            dut01Obj.linkPortMapping['lnk02']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 2000')
        assert(deleteLAGNegative(dut01Obj, '2000', '1', 'off', [
            dut01Obj.linkPortMapping['lnk01'],
            dut01Obj.linkPortMapping['lnk02']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 2001')
        assert(deleteLAGNegative(dut01Obj, '2001', '1', 'off', [
            dut01Obj.linkPortMapping['lnk01'],
            dut01Obj.linkPortMapping['lnk02']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID @%&$#()')
        assert(deleteLAGNegative(dut01Obj, '@%&$#()', '1', 'off', [
            dut01Obj.linkPortMapping['lnk01'],
            dut01Obj.linkPortMapping['lnk02']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 60000')
        assert(deleteLAGNegative(dut01Obj, '60000', '1', 'off', [
            dut01Obj.linkPortMapping['lnk01'],
            dut01Obj.linkPortMapping['lnk02']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 600')
        assert(deleteLAGNegative(dut01Obj, '600', '1', 'off', [
            dut01Obj.linkPortMapping['lnk01'],
            dut01Obj.linkPortMapping['lnk02']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 2')
        assert(deleteLAGNegative(dut01Obj, '2', '1', 'off', [
            dut01Obj.linkPortMapping['lnk01'],
            dut01Obj.linkPortMapping['lnk02']], 'l3-src-dst', False, False))

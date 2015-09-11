import pytest
from switch.CLI import *
from switch.CLI.lag import *
from switch.CLI.vlan import *
from switch.CLI.interface import *
from lib import testEnviron
#from common import *

topoDict = {"topoExecution": 3000,
            "topoDevices": "dut01 dut02 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut01:dut02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut02:wrkston02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation"}

#Reboots switch
def switch_reboot(deviceObj):
    # Reboot switch
    LogOutput('info', "Reboot switch " + deviceObj.device) 
    deviceObj.Reboot()
    rebootRetStruct = returnStruct(returnCode=0)
    return rebootRetStruct

#Adds interfaces to LAG
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
    
    #Add interfaces
    for i in intArray:
        command = "interface %s\r" % str(i)
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to configure interface " + str(i) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput('debug', "Entered interface " + str(i) + " on device " + deviceObj.device)
        
        command = "lag %s" % str(lagId)
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to add interface " + str(i) + " to LAG" + str(lagId) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput('info', "Added interface " + str(i) + " to LAG" + str(lagId) + " on device " + deviceObj.device)
        
        command = "exit"
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to exit configuration of interface " + str(i) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput('debug', "Exited configuration of interface " + str(i) + " on device " + deviceObj.device)
    
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
    #Exit vtysh
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

#Disable routing on interfaces so VLANs can be configured
def enableInterfaceRouting(deviceObj, int, enable):
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
    #enter interface
    command = "interface %s\r" % str(int)
    returnDevInt = deviceObj.DeviceInteract(command=command)
    retCode = returnDevInt['returnCode']
    overallBuffer.append(returnDevInt['buffer'])
    if retCode != 0:
        LogOutput('error', "Failed to configure interface " + str(int) + " on device " + deviceObj.device)
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
        return returnCls
    else:
        LogOutput('debug', "Entered interface " + str(int) + " on device " + deviceObj.device)
    if enable:
        #configure interface
        command = "routing"
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to enable routing on interface " + str(int) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput('info', "Enabledrouting on interface " + str(int) + " on device " + deviceObj.device)
    else:
        #configure interface
        command = "no routing"
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to disable routing on interface " + str(int) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput('info', "Disabled routing on interface " + str(int) + " on device " + deviceObj.device)
        #exit
    command = "exit"
    returnDevInt = deviceObj.DeviceInteract(command=command)
    retCode = returnDevInt['returnCode']
    overallBuffer.append(returnDevInt['buffer'])
    if retCode != 0:
        LogOutput('error', "Failed to exit configure interface " + str(int) + " on device " + deviceObj.device)
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
        return returnCls
    else:
        LogOutput('debug', "Exited configure interface " + str(int) + " on device " + deviceObj.device)
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
    #Get out of vtysh
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
    #Return
    bufferString = ""
    for curLine in overallBuffer:
        bufferString += str(curLine)
    returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
    return returnCls
  
#Enable/disable interface on DUT
def enableDutInterface(deviceObj, int, enable):
    if enable:
        retStruct = InterfaceEnable(deviceObj=deviceObj, enable=enable, interface=int)
        if retStruct.returnCode() != 0:
            LogOutput('error',"Failed to enable " + deviceObj.device +" interface " + int)
            return False
        else:
            LogOutput('info', "Enabled " + deviceObj.device +" interface " + int)
    else:
        retStruct = InterfaceEnable(deviceObj=deviceObj, enable=enable, interface=int)
        if retStruct.returnCode() != 0:
            LogOutput('error',"Failed to disable " + deviceObj.device +" interface " + int)
            return False
        else:
            LogOutput('info', "Disabled " + deviceObj.device +" interface " + int)
    return True

#Create/delete a LAG and add interfaces   
def createLAG(deviceObj, lagId, configure, intArray, mode):
    if configure:
        retStruct = lagCreation(deviceObj=deviceObj,lagId=str(lagId),configFlag=True)
        if retStruct.returnCode() != 0:
            LogOutput('error',"Failed to create LAG1 on " + deviceObj.device)
            return False
        else:
            LogOutput('info', "Created LAG" + str(lagId) + " on " + deviceObj.device)
        retStruct = addInterfacesToLAG(deviceObj, 1, intArray)
        if retStruct.returnCode() != 0:
            return False
        if mode != 'off':
            retStruct = lagMode(lagId=str(lagId), deviceObj=deviceObj, lacpMode=mode)
            if retStruct.returnCode() != 0:
                return False
        retStruct = lacpAggregatesShow(deviceObj=deviceObj)
        if retStruct.returnCode() != 0:
            LogOutput('error',"Failed to verify if LAG was created on " + deviceObj.device)
            return False
        if len(retStruct.dataKeys()) == 0:
            LogOutput('error',"No LAGs were configured on device")
            return False
        if retStruct.valueGet(key=str(lagId)) is None:
            LogOutput('error',"Configured LAG is not present on device")
            return False
        if len(retStruct.valueGet(key=str(lagId))['interfaces']) != len(intArray):
            LogOutput('error',"The number of interfaces in the LAG (" + len(retStruct.valueGet(key=str(lagId))['interfaces']) + ") does not match the configured number of " + len(intArray))
            return False
        if retStruct.valueGet(key=str(lagId))['lacpMode'] != mode:
            LogOutput('error',"The LAG have been configured in LACP mode " + mode + " but instead it is in LACP mode " + retStruct.valueGet(key=str(lagId))['lacpMode'])
            return False
    else:
        retStruct = lagCreation(deviceObj=deviceObj,lagId=str(lagId),configFlag=False)
        if retStruct.returnCode() != 0:
            LogOutput('error',"Failed to delete LAG1 on " + deviceObj.device)
            return False
        else:
            LogOutput('info', "Deleted LAG" + str(lagId) + " on " + deviceObj.device)
        retStruct = lacpAggregatesShow(deviceObj=deviceObj)
        if len(retStruct.dataKeys()) != 0:
            if retStruct.valueGet(key=str(lagId)) is not None:
                LogOutput('error',"The LAG was not deleted from configuration")
                return False
    return True

#Change LAG mode and verify configuration is consistent
def changeLagMode(deviceObj, lagId, mode):
    #Variables
    modeHelper = ''
    retStructOriginal = lacpAggregatesShow(deviceObj=deviceObj,lagId=str(lagId))
    if retStructOriginal.returnCode() != 0:
        return False
    if mode == 'off':
        modeHelper = 'off'
    else:
        modeHelper = mode
    retStruct = lagMode(lagId=str(lagId), deviceObj=deviceObj, lacpMode=mode)
    if retStruct.returnCode() != 0:
        return False
    retStruct = lacpAggregatesShow(deviceObj=deviceObj,lagId=str(lagId))
    if retStructOriginal.returnCode() != 0:
        return False
    if len(retStruct.valueGet(key=str(lagId))['interfaces']) != len(retStructOriginal.valueGet(key=str(lagId))['interfaces']):
        text1 = ""
        for i in retStruct.valueGet(key=str(lagId))['interfaces']:
            text1 = " " + i
        text2 = ""
        for i in retStructOriginal.valueGet(key=str(lagId))['interfaces']:
            text2 = " " + i
        LogOutput('error',"Number of interfaces on LAG changed. Before:" + text2 + ". After: " + text1)
        return false
    for i in xrange(0, len(retStructOriginal.valueGet(key=str(lagId))['interfaces'])):
        coincidence = False
        try:
            for k in xrange(0, len(retStruct.valueGet(key=str(lagId))['interfaces'])):
                if retStruct.valueGet(key=str(lagId))['interfaces'][k] == retStructOriginal.valueGet(key=str(lagId))['interfaces'][i]:
                    coincidence = True
                    break
            if not coincidence:
                LogOutput('error',"Interface " + retStructOriginal.valueGet(key=str(lagId))['interfaces'][i] + " is no longer present in LAG")
                return False
        except:
                LogOutput('error',"Found unidentified error when comparing for changes on interfaces members of LAG")
                LogOutput('error',"Dumping information before change:\n" + retStructOriginal.buffer())
                LogOutput('error',"Dumping information after change:\n" + retStruct.buffer())
                return False
    if retStruct.valueGet(key=str(lagId))['lacpFastFlag'] != retStructOriginal.valueGet(key=str(lagId))['lacpFastFlag']:
        LogOutput('error',"Heartbeat settings on LAG changed. Before:" + retStructOriginal.valueGet(key=str(lagId))['lacpFastFlag'] + ". After: " + retStruct.valueGet(key=str(lagId))['lacpFastFlag'])
        return False
    if retStruct.valueGet(key=str(lagId))['hashType'] != retStructOriginal.valueGet(key=str(lagId))['hashType']:
        LogOutput('error',"Hash settings on LAG changed. Before:" + retStructOriginal.valueGet(key=str(lagId))['hashType'] + ". After: " + retStruct.valueGet(key=str(lagId))['hashType'])
        return False
    if retStruct.valueGet(key=str(lagId))['fallbackFlag'] != retStructOriginal.valueGet(key=str(lagId))['fallbackFlag']:
        LogOutput('error',"Fallback settings on LAG changed. Before:" + retStructOriginal.valueGet(key=str(lagId))['fallbackFlag'] + ". After: " + retStruct.valueGet(key=str(lagId))['fallbackFlag'])
        return False
    if retStruct.valueGet(key=str(lagId))['lacpMode'] != modeHelper:
        LogOutput('error',"The LAG have been configured in LACP mode " + modeHelper + " but instead it is in LACP mode " + retStruct.valueGet(key=str(lagId))['lacpMode'])
        return False
    LogOutput('info',"Changed LAG" + str(lagId) + " to LACP " + modeHelper + "mode on device " + deviceObj.device)
    return True

#Add VLAN to interface
def addInterfaceVLAN(deviceObj, vlanId, enable, int):
    if enable:
        retStruct = enableInterfaceRouting(deviceObj, int, False)
        if retStruct.returnCode() != 0:
            return False
        retStruct = AddPortToVlan(deviceObj=deviceObj,vlanId=vlanId,interface=int, access=True)
        LogOutput('info',"Added VLAN " + str(vlanId) + " to interface " + int)
        if retStruct.returnCode() != 0:
            LogOutput('error',"Failed to add VLAN " + str(vlanId) + " to interface " + int)
            return False
    else:
        retStruct = AddPortToVlan(deviceObj=deviceObj,vlanId=vlanId,interface=int, config=False, access=True)
        LogOutput('info',"Delete VLAN " + str(vlanId) + " to interface " + int)
        if retStruct.returnCode() != 0:
            LogOutput('error',"Failed to delete VLAN " + str(vlanId) + " to interface " + int)
            return False
        retStruct = enableInterfaceRouting(deviceObj, int, True)
        if retStruct.returnCode() != 0:
            return False
    return True
 
#Configure/delete VLAN on switch   
def configureVLAN(deviceObj, vlanId, enable):
    if enable:
        LogOutput('debug',"Configuring VLAN " + str(vlanId) + " on device " + deviceObj.device)
        retStruct = AddVlan(deviceObj=deviceObj,vlanId=vlanId)
        if retStruct.returnCode() != 0:
            LogOutput('error',"Failed to create VLAN " + str(vlanId) + " on device " + deviceObj.device)
            return False
        else:
            LogOutput('info',"Created VLAN " + str(vlanId) + " on device " + deviceObj.device)
        retStruct = VlanStatus(deviceObj=deviceObj,vlanId=vlanId,status=True)
        if retStruct.returnCode() != 0:
            LogOutput('error',"Failed to enable VLAN " + str(vlanId) + " on device " + deviceObj.device)
            return False
        else:
            LogOutput('info',"Enabled VLAN " + str(vlanId) + " on device " + deviceObj.device)
    else:
        LogOutput('debug',"Deleting VLAN " + str(vlanId) + " on device " + deviceObj.device)
        retStruct = AddVlan(deviceObj=deviceObj,vlanId=vlanId, config=False)
        if retStruct.returnCode() != 0:
            LogOutput('error',"Failed to delete VLAN " + str(vlanId) + " on device " + deviceObj.device)
            return False
        else:
            LogOutput('info',"Deleted VLAN " + str(vlanId) + " on device " + deviceObj.device)
    return True

#Configure/unconfigure the IP address of a workstation
def configureWorkstation(deviceObj, int, ipAddr, netMask, broadcast, enable):
    if enable:
        retStruct = deviceObj.NetworkConfig(ipAddr=ipAddr,
                                        netMask=netMask,
                                        broadcast=broadcast,
                                        interface=int, configFlag=True)
        if retStruct.returnCode() != 0:
            LogOutput('error',"Failed to configure IP on workstation " + deviceObj.device)
            return False
        cmdOut = deviceObj.cmd("ifconfig "+ int)
        LogOutput('info', "Ifconfig info for workstation " + deviceObj.device + ":\n" + cmdOut)
    else:
        retStruct = deviceObj.NetworkConfig(ipAddr=ipAddr,
                                        netMask=netMask,
                                        broadcast=broadcast,
                                        interface=int, configFlag=False)
        if retStruct.returnCode() != 0:
            LogOutput('error',"Failed to unconfigure IP on workstation " + deviceObj.device)
            return False
        cmdOut = deviceObj.cmd("ifconfig "+ int)
        LogOutput('info', "Ifconfig info for workstation " + deviceObj.device + ":\n" + cmdOut)
    return True

#Ping between workstation
def pingBetweenWorkstations(deviceObj1, deviceObj2, ipAddr, success):
    LogOutput('info', "Pinging between workstation " + deviceObj1.device + " and workstation " + deviceObj2.device)
    if success:
        retStruct = deviceObj1.Ping(ipAddr=ipAddr)
        if retStruct.returnCode() != 0:
            LogOutput('error',"Failed to ping from workstation " + deviceObj1.device + ":\n" + str(retStruct.retValueString()))
            return False
        else:
            LogOutput('info', "IPv4 Ping from workstation 1 to workstation 2 return JSON:\n" + str(retStruct.retValueString()))
            packet_loss = retStruct.valueGet(key='packet_loss')
            packets_sent = retStruct.valueGet(key='packets_transmitted')
            packets_received = retStruct.valueGet(key='packets_received')
            LogOutput('info', "Packets Sent:\t"+ str(packets_sent))
            LogOutput('info', "Packets Recv:\t"+ str(packets_received))
            LogOutput('info', "Packet Loss %:\t"+str(packet_loss))
            LogOutput('info', "Passed ping test between workstation " + deviceObj1.device + " and workstation " + deviceObj2.device)
    else:
        retStruct = deviceObj1.Ping(ipAddr=ipAddr)
        if retStruct.returnCode() != 0:
            LogOutput('debug',"Failed to ping workstation2 as expected:\n" + str(retStruct.retValueString()))
            LogOutput('info', "Passed negative ping test between workstation " + deviceObj1.device + " and workstation " + deviceObj2.device)
        else:
            LogOutput('error', "IPv4 Ping from workstation 1 to workstation 2 return JSON:\n" + str(retStruct.retValueString()))
            packet_loss = retStruct.valueGet(key='packet_loss')
            packets_sent = retStruct.valueGet(key='packets_transmitted')
            packets_received = retStruct.valueGet(key='packets_received')
            LogOutput('error', "Packets Sent:\t"+ str(packets_sent))
            LogOutput('error', "Packets Recv:\t"+ str(packets_received))
            LogOutput('error', "Packet Loss %:\t"+str(packet_loss))
            return False
    return True

class Test_ft_framework_basics:
    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_ft_framework_basics.testObj = testEnviron(topoDict=topoDict)
        Test_ft_framework_basics.topoObj = Test_ft_framework_basics.testObj.topoObjGet()
        
    def teardown_class(cls):
        # Terminate all nodes
        Test_ft_framework_basics.topoObj.terminate_nodes()
    
    def test_reboot_switch(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Reboot the switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        devRebootRetStruct = switch_reboot(dut01Obj)
        if devRebootRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to reboot Switch 1")
            assert(devRebootRetStruct.returnCode() == 0)
        else:
            LogOutput('info', "Passed Switch 1 Reboot piece")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        devRebootRetStruct = switch_reboot(dut02Obj)
        if devRebootRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to reboot Switch 2")
            assert(devRebootRetStruct.returnCode() == 0)
        else:
            LogOutput('info', "Passed Switch 2 Reboot piece")
    
    def test_createLAGs(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Create LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        
        assert(createLAG(dut01Obj, '1', True, [dut01Obj.linkPortMapping['lnk02'], dut01Obj.linkPortMapping['lnk03']], 'active'))
        assert(createLAG(dut02Obj, '1', True, [dut02Obj.linkPortMapping['lnk02'], dut02Obj.linkPortMapping['lnk03']], 'passive'))
    
    def test_configureVLANs(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Configure VLANs on switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        #Switch 1
        LogOutput('info', "Configure VLAN on dut01")
        assert(configureVLAN(dut01Obj, 900, True))
        assert(addInterfaceVLAN(dut01Obj, 900, True, dut01Obj.linkPortMapping['lnk01']))
        assert(addInterfaceVLAN(dut01Obj, 900, True, 'lag 1'))
        etStruct = LogOutput('info', "Configure VLAN on dut02")
        assert(configureVLAN(dut02Obj, 900, True))
        assert(addInterfaceVLAN(dut02Obj, 900, True, dut02Obj.linkPortMapping['lnk04']))
        assert(addInterfaceVLAN(dut02Obj, 900, True, 'lag 1'))
          
      
    def test_enableDUTsInterfaces(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Enable switches interfaces")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        LogOutput('info', "Configuring switch dut01")
        assert(enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk01'], True))
        assert(enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk02'], True))
        assert(enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk03'], True))
          
        LogOutput('info', "Configuring switch dut02")
        assert(enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'], True))
        assert(enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03'], True))
        assert(enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk04'], True))
      
    def test_configureWorkstations(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Configure workstations")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        LogOutput('info', "Configuring workstation 1")
        assert(configureWorkstation(wrkston01Obj, wrkston01Obj.linkPortMapping['lnk01'], "140.1.1.10", "255.255.255.0", "140.1.1.255", True))
        LogOutput('info', "Configuring workstation 2")
        assert(configureWorkstation(wrkston02Obj, wrkston02Obj.linkPortMapping['lnk04'], "140.1.1.11", "255.255.255.0", "140.1.1.255", True))
      
    def test_pingBetweenClients1(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Test ping between clients work")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        assert(pingBetweenWorkstations(wrkston01Obj, wrkston02Obj, "140.1.1.11", True))
         
    def test_changelagMode(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Change LAGs from dynamic to static")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        LogOutput('info', "Change LAG mode on dut01")
        assert(changeLagMode(dut01Obj, '1', 'off'))
        LogOutput('info', "Change LAG mode on dut02")
        assert(changeLagMode(dut02Obj, '1', 'off'))
        
    def test_pingBetweenClients2(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Test ping between clients continue working")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        assert(pingBetweenWorkstations(wrkston01Obj, wrkston02Obj, "140.1.1.11", True))
    
    def test_disableAndEnableInterfacesOfLAGs(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Disable and re-enable interfaces associated to LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        LogOutput('info', "Disable interfaces on DUTs")
        LogOutput('info', "Configuring switch dut01")
        assert(enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk02'], False))
        assert(enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk03'], False))
          
        LogOutput('info', "Configuring switch dut02")
        assert(enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'], False))
        assert(enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03'], False))
        
        LogOutput('info', "Re-enable interfaces on DUTs")
        LogOutput('info', "Configuring switch dut01")
        assert(enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk02'], True))
        assert(enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk03'], True))
          
        LogOutput('info', "Configuring switch dut02")
        assert(enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'], True))
        assert(enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03'], True))
        
    def test_pingBetweenClients3(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Test ping between clients continue working")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        assert(pingBetweenWorkstations(wrkston01Obj, wrkston02Obj, "140.1.1.11", True))
        
    def test_clean_up_devices(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Device Cleanup - rolling back config")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        LogOutput('info', "Unconfigure workstations")
        LogOutput('info', "Unconfiguring workstation 1")
        assert(configureWorkstation(wrkston01Obj, wrkston01Obj.linkPortMapping['lnk01'], "140.1.1.10", "255.255.255.0", "140.1.1.255", False))
        LogOutput('info', "Unconfiguring workstation 2")
        assert(configureWorkstation(wrkston02Obj, wrkston02Obj.linkPortMapping['lnk04'], "140.1.1.11", "255.255.255.0", "140.1.1.255", False))
         
        LogOutput('info', "Delete LAGs on DUTs")
        assert(createLAG(dut01Obj, '1', False, [], 'off'))
        assert(createLAG(dut02Obj, '1', False, [], 'off'))
         
        LogOutput('info', "Disable interfaces on DUTs")
        LogOutput('info', "Configuring switch dut01")
        assert(enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk01'], False))
        assert(enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk02'], False))
        assert(enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk03'], False))
          
        LogOutput('info', "Configuring switch dut02")
        assert(enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'], False))
        assert(enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03'], False))
        assert(enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk04'], False))
         
        LogOutput('info', "Remove VLAN from DUTs")
        assert(configureVLAN(dut01Obj, 900, False))
        assert(configureVLAN(dut02Obj, 900, False))
         
        LogOutput('info', "Cleaned up devices")
        
    
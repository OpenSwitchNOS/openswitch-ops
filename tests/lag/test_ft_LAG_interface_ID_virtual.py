import pytest
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *
from lib_test import lagVerifyTrafficFlow
from lib_test import lagVerifyLACPStatusAndFlags
from lib_test import lagVerifyConfig
from lib_test import lagCheckLACPInterfaceStatus
from lib_test import switchEnableInterface
from lib_test import lagCreate
from lib_test import vlanAddInterface
from lib_test import vlanConfigure
from lib_test import workstationConfigure
from lib_test import switchReboot
from lib_test import lagAddInterface
from lib_test import lagVerifyNumber
from lib_test import showInterface
from lib_test import showRun
from lib_test import interfaceEnableRouting

topoDict = {"topoExecution": 3000,
            "topoType": "virtual",
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut01:dut02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut02:wrkston02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation,\
                            wrkston01:docker-image: openswitch/ubuntutest,\
                            wrkston02:docker-image: openswitch/ubuntutest"}

# Clean up devices


def clean_up_devices(dut01Obj, dut02Obj, wrkston01Obj, wrkston02Obj):
    # Clean up devices
    LogOutput('info', "\n############################################")
    LogOutput('info', "Device Cleanup - rolling back config")
    LogOutput('info', "############################################")
    finalResult = []
    dut01 = {'obj': dut01Obj, 'links': ['lnk01', 'lnk02', 'lnk03'],
             'wrkston_links': ['lnk01']}
    dut02 = {'obj': dut02Obj, 'links': ['lnk02', 'lnk03', 'lnk04'],
             'wrkston_links': ['lnk04']}

    LogOutput('info', "Unconfigure workstations")
    LogOutput('info', "Unconfiguring workstation 1")
    finalResult.append(workstationConfigure(
        wrkston01Obj,
        wrkston01Obj.linkPortMapping['lnk01'], "140.1.1.10",
        "255.255.255.0", "140.1.1.255", False))
    LogOutput('info', "Unconfiguring workstation 2")
    finalResult.append(workstationConfigure(
        wrkston02Obj,
        wrkston02Obj.linkPortMapping['lnk04'], "140.1.1.11",
        "255.255.255.0", "140.1.1.255", False))

    LogOutput('info', "Delete LAGs on DUTs")
    finalResult.append(lagCreate(dut01Obj, '1', False, [], None))
    finalResult.append(lagCreate(dut02Obj, '1', False, [], None))

    LogOutput('info', "Enable routing on DUTs workstations links")
    for dut in [dut01, dut02]:
        LogOutput('info', "Configuring switch %s" % dut['obj'].device)
        for link in dut['wrkston_links']:
            finalResult.append(interfaceEnableRouting(dut['obj'],
                                                      dut['obj'].
                                                      linkPortMapping[link],
                                                      True))

    LogOutput('info', "Disable interfaces on DUTs")
    for dut in [dut01, dut02]:
        LogOutput('info', "Configuring switch %s" % dut['obj'].device)
        for link in dut['links']:
            finalResult.append(switchEnableInterface(dut['obj'],
                                                     dut['obj'].
                                                     linkPortMapping[link],
                                                     False))

    LogOutput('info', "Remove VLAN from DUTs")
    finalResult.append(vlanConfigure(dut01Obj, 900, False))
    finalResult.append(vlanConfigure(dut02Obj, 900, False))

    for i in finalResult:
        if not i:
            LogOutput('error', 'Errors were detected while cleaning ' +
                      'devices')
            return
    LogOutput('info', "Cleaned up devices")


class Test_ft_framework_basics:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_ft_framework_basics.testObj = testEnviron(topoDict=topoDict)
        Test_ft_framework_basics.topoObj =\
            Test_ft_framework_basics.testObj.topoObjGet()

    def teardown_class(cls):
        # clean devices
        clean_up_devices(
            cls.topoObj.deviceObjGet(device="dut01"),
            cls.topoObj.deviceObjGet(device="dut02"),
            cls.topoObj.deviceObjGet(device="wrkston01"),
            cls.topoObj.deviceObjGet(device="wrkston02"))
        # Terminate all nodes
        Test_ft_framework_basics.topoObj.terminate_nodes()

    def test_reboot_switch(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Reboot the switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        devRebootRetStruct = switchReboot(dut01Obj)
        if not devRebootRetStruct:
            LogOutput('error', "Failed to reboot and clean Switch 1")
            assert(devRebootRetStruct.returnCode() == 0)
        else:
            LogOutput('info', "Passed Switch 1 Reboot piece")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        devRebootRetStruct = switchReboot(dut02Obj)
        if not devRebootRetStruct:
            LogOutput('error', "Failed to reboot and clean Switch 2")
            assert(devRebootRetStruct.returnCode() == 0)
        else:
            LogOutput('info', "Passed Switch 2 Reboot piece")

    def test_enableDUTsInterfaces(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Enable switches interfaces")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        LogOutput('info', "Configuring switch dut01")
        assert(
            switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk01'],
                                  True))
        assert(
            switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk02'],
                                  True))
        assert(
            switchEnableInterface(dut01Obj, dut01Obj.linkPortMapping['lnk03'],
                                  True))

        LogOutput('info', "Configuring switch dut02")
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'],
                                  True))
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03'],
                                  True))
        assert(
            switchEnableInterface(dut02Obj, dut02Obj.linkPortMapping['lnk04'],
                                  True))

    def test_createLAGs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Create LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagCreate(dut01Obj, '1', True,
                         [dut01Obj.linkPortMapping['lnk02'],
                          dut01Obj.linkPortMapping['lnk03']], 'active'))
        assert(lagCreate(dut02Obj, '1', True,
                         [dut02Obj.linkPortMapping['lnk02'],
                          dut02Obj.linkPortMapping['lnk03']], 'active'))

    def test_configureVLANs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Configure VLANs on switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        # Switch 1
        LogOutput('info', "Configure VLAN on dut01")
        assert(vlanConfigure(dut01Obj, 900, True))
        assert(
            vlanAddInterface(dut01Obj, 900, True,
                             dut01Obj.linkPortMapping['lnk01']))
        assert(vlanAddInterface(dut01Obj, 900, True, 'lag 1'))
        # Switch 2
        LogOutput('info', "Configure VLAN on dut02")
        assert(vlanConfigure(dut02Obj, 900, True))
        assert(
            vlanAddInterface(dut02Obj, 900, True,
                             dut02Obj.linkPortMapping['lnk04']))
        assert(vlanAddInterface(dut02Obj, 900, True, 'lag 1'))

    def test_configureWorkstations(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Configure workstations")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        LogOutput('info', "Configuring workstation 1")
        assert(workstationConfigure(
            wrkston01Obj,
            wrkston01Obj.linkPortMapping[
                'lnk01'], "140.1.1.10", "255.255.255.0", "140.1.1.255", True))
        LogOutput('info', "Configuring workstation 2")
        assert(workstationConfigure(
            wrkston02Obj,
            wrkston02Obj.linkPortMapping[
                'lnk04'], "140.1.1.11", "255.255.255.0", "140.1.1.255", True))

    def test_lagConfiguration(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAG configuration was successfully applied")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                           ['lnk02', 'lnk03'], 'lag1', 'lag1'))

    def test_lagTraffic(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAG traffic")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")

        assert(lagVerifyTrafficFlow(dut01Obj, dut02Obj, wrkston01Obj,
                                    wrkston02Obj, '140.1.1.10',
                                    '140.1.1.11', ['lnk02', 'lnk03'],
                                    'lnk01', 'lnk04', '140.1.1'))

    def test_setLACPPOrtID_1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Set LACP port-id to 1")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        interf = int(dut01Obj.linkPortMapping['lnk02'])
        returnCLS = InterfaceLacpPortIdConfig(
            deviceObj=dut01Obj, interface=interf, lacpPortId=1)
        result = returnCLS.returnCode()
        if result != 0:
            LogOutput('error', "Step failed, Unable to set LACP port-id")
            assert 1 != 1
        else:
            LogOutput('info', "Passed - LACP port-id set to 1")

        assert(lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                           ['lnk02', 'lnk03'], "lag1", "lag1",
                                           dut01PortIds=["1", None]))

    def test_setLACPPOrtID_65535(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Set LACP port-id to 65535")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        interf = int(dut01Obj.linkPortMapping['lnk02'])
        returnCLS = InterfaceLacpPortIdConfig(
            deviceObj=dut01Obj, interface=interf, lacpPortId=65535)
        result = returnCLS.returnCode()
        if result != 0:
            LogOutput(
                'error', "Step failed, Unable to set LACP port-id to 65535")
            assert 1 != 1
        else:
            LogOutput('info', "Passed - LACP port-id set to 65535")

        assert(lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                           ['lnk02', 'lnk03'],
                                           "lag1", "lag1",
                                           dut01PortIds=["65535", None]))

    def test_setLACPPOrtID_same(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Set LACP port-id to same value as another port")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        portID = lagCheckLACPInterfaceStatus(
            dut01Obj, dut01Obj.linkPortMapping['lnk03'])['actor_port_id']
        portID = portID.split(',')[1]
        interf = int(dut01Obj.linkPortMapping['lnk02'])
        returnCLS = InterfaceLacpPortIdConfig(
            deviceObj=dut01Obj, interface=interf,
            lacpPortId=int(portID))
        result = returnCLS.returnCode()
        if result != 0:
            LogOutput(
                'error', "Step failed, Unable to set LACP port-id to " +
                portID)
            assert 1 != 1
        else:
            LogOutput('info', "Passed - LACP port-id set to " +
                      portID)

        assert(lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                           ['lnk02', 'lnk03'], "lag1",
                                           "lag1",
                                           dut01PortIds=[portID, None]))

    def test_setLACPPOrtID_negative(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Set LACP port-id to -1 and 0")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        interf = int(dut01Obj.linkPortMapping['lnk02'])
        returnCLS = InterfaceLacpPortIdConfig(
            deviceObj=dut01Obj, interface=interf, lacpPortId=int("-1"))
        result = returnCLS.returnCode()
        if result != 0:
            LogOutput('info', "Passed - Unable to set LACP port-id to -1")
        else:
            LogOutput(
                'error', "Step failed, LACP port-id accepted a value of -1")
            assert 1 != 1
        result = lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                             ['lnk02',
                                                 'lnk03'], "lag1", "lag1",
                                             dut01PortIds=["-1", None])
        if not result:
            LogOutput('info', "Passed - LACP port-id with value of " +
                      "-1 was not applied to the port")
        else:
            LogOutput('error', "Step failed, LACP port-id with value of " +
                      "-1 was applied to the port")
            assert 1 != 1

        returnCLS = InterfaceLacpPortIdConfig(
            deviceObj=dut01Obj, interface=interf, lacpPortId=0)
        result = returnCLS.returnCode()
        if result != 0:
            LogOutput('info', "Passed - Unable to set LACP port-id to 0")
        else:
            LogOutput(
                'error', "Step failed, LACP port-id accepted a value of 0")
            assert 1 != 1

        result = lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                             ['lnk02', 'lnk03'], "lag1",
                                             "lag1", dut01PortIds=["0", None])
        if not result:
            LogOutput('info', "Passed - LACP port-id with value of " +
                      "0 was not applied to the port")
        else:
            LogOutput('error', "Step failed, LACP port-id with value of " +
                      "0 was applied to the port")
            assert 1 != 1

    def test_setLACPPOrtID_65536(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Set LACP port-id to 65536")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        interf = int(dut01Obj.linkPortMapping['lnk02'])
        returnCLS = InterfaceLacpPortIdConfig(
            deviceObj=dut01Obj, interface=interf, lacpPortId=65536)
        result = returnCLS.returnCode()
        if result != 0:
            LogOutput(
                'info', "Passed - Cannot accept LACP port-id set to 65536")
        else:
            LogOutput('error',
                      "Step failed, LACP port-id accepted a value of 65536")
            assert 1 != 1

        result = lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                             ['lnk02', 'lnk03'], "lag1",
                                             "lag1",
                                             dut01PortIds=["65536", None])

        if not result:
            LogOutput('info', "Passed - LACP port-id with value of 65536 " +
                      "was not applied to the port")
        else:
            LogOutput(
                'error', "Step failed, LACP port-id with value of 65536 " +
                "was applied to the port")
            assert 1 != 1

    def test_setLACPPOrtID_letter(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Set LACP port-id to a letter")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        interf = int(dut01Obj.linkPortMapping['lnk02'])
        returnCLS = InterfaceLacpPortIdConfig(
            deviceObj=dut01Obj, interface=interf, lacpPortId="H")
        result = returnCLS.returnCode()
        if result != 0:
            LogOutput(
                'info', "Passed - Cannot accept LACP port-id set to a letter")
        else:
            LogOutput('error', "Step failed, Set LACP port-id to a letter")
            assert 1 != 1

        result = lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                             ['lnk02', 'lnk03'], "lag1",
                                             "lag1", dut01PortIds=["H", None])

        if not result:
            LogOutput('info', "Passed - LACP port-id with value of " +
                      "a letter was not applied to the port")
        else:
            LogOutput(
                'error', "Step failed, LACP port-id with value of " +
                "a letter was applied to the port")
            assert 1 != 1

    def test_setLACPPOrtID_special_char(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Set LACP port-id to a special character")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        interf = int(dut01Obj.linkPortMapping['lnk02'])
        returnCLS = InterfaceLacpPortIdConfig(
            deviceObj=dut01Obj, interface=interf, lacpPortId="%")
        result = returnCLS.returnCode()
        if result != 0:
            LogOutput('info', "Passed - Cannot accept LACP " +
                      "port-id set to a special character")
        else:
            LogOutput(
                'error', "Step failed, Set LACP port-id to special character")
            assert 1 != 1

        result = lagVerifyLACPStatusAndFlags(dut01Obj, dut02Obj, True,
                                             ['lnk02', 'lnk03'], "lag1",
                                             "lag1", dut01PortIds=["%", None])

        if not result:
            LogOutput('info', "Passed - LACP port-id with value of a special" +
                      " character was not applied to the port")
        else:
            LogOutput(
                'error', "Step failed, LACP port-id with value of a special" +
                " character was applied to the port")
            assert 1 != 1

    def test_lagTraffic_2(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test LAG traffic after changing " +
                  "LACP port-id several times")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")

        assert(lagVerifyTrafficFlow(dut01Obj, dut02Obj, wrkston01Obj,
                                    wrkston02Obj, '140.1.1.10',
                                    '140.1.1.11', ['lnk02', 'lnk03'],
                                    'lnk01', 'lnk04', '140.1.1'))

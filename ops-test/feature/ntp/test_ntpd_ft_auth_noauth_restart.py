# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from time import sleep
TOPOLOGY = """
# +-------+                   +-------+
# |       |     +-------+     |       |
# |  hs1  <----->  sw1  <----->  hs2  |
# |       |     +-------+     |       |
# +-------+                   +-------+

# Nodes
[type=openswitch name="Switch 1"] ops1
[type=host name="Host 1"] hs1
[type=host name="Host 2"] hs2

# Links
hs1:1 -- ops1:1
ops1:2 -- hs2:1
"""
# Global Variable
min_lag = 1
global WORKSTATION_IP_ADDR_SER1
global WORKSTATION_IP_ADDR_SER2
global SERVER_UNREACHABLE
"""
Author: Tamilmannan Harikrishnan - tamilmannan.h@hpe.com
testID: LAG FT Test
test name: test_ntpd_ft_auth_noauth_restart
test Description:  Test checks if the switch is configured as a NTP client
                   and if the switch is successfully configured with the
                   local NTP server."""


def ntpconfig(ops1, wrkston01, wrkston02, step):
    step("CONFIGURING WS1 AND WS2 AS LOCAL NTP SERVER WITH AND WITHOUT AUTH")
    global WORKSTATION_IP_ADDR_SER1
    global WORKSTATION_IP_ADDR_SER2
    global SERVER_UNREACHABLE
    sleep(10)
    command = "echo \"authenticate yes\" >> /etc/ntp.conf"
    wrkston01(command, shell="bash")
    cmd = "ntpd -c /etc/ntp.conf"
    wrkston01(cmd, shell="bash")
    wrkston02(cmd, shell="bash")
    sleep(10)
    out = wrkston01("ntpq -p -n", shell="bash")
    if ".INIT." in out or "Connection refused" in out:
        SERVER_UNREACHABLE = True
    else:
        SERVER_UNREACHABLE = False
    ifconfigcmdout = wrkston01("ifconfig eth0", shell="bash")
    lines = ifconfigcmdout.split('\n')
    target = 'inet'
    for line in lines:
        word = line.split()
        for i, w in enumerate(word):
            if w == target:
                WORKSTATION_IP_ADDR_SER1 = word[i+1]
                break
    ifconfigcmdout = wrkston02("ifconfig eth0", shell="bash")
    lines = ifconfigcmdout.split('\n')
    target = 'inet'
    for line in lines:
        word = line.split()
        for i, w in enumerate(word):
            if w == target:
                WORKSTATION_IP_ADDR_SER2 = word[i+1]
                break
    out = wrkston02("ntpq -p -n", shell="bash")
    if SERVER_UNREACHABLE is False:
        if ".INIT." in out or "Connection refused" in out:
            SERVER_UNREACHABLE = True
        else:
            SERVER_UNREACHABLE = False
    with ops1.libs.vtysh.Configure() as ctx:
        ctx.ntp_authentication_key_md5("55", "secretpassword")
        ctx.ntp_trusted_key("55")
        ctx.ntp_authentication_enable()
        ctx.ntp_server_key_id(WORKSTATION_IP_ADDR_SER1, "55")
        ctx.ntp_server_prefer(WORKSTATION_IP_ADDR_SER2)


def validatentpassocinfo(ops1, wrkston01, wrkston02, step):
    global WORKSTATION_IP_ADDR_SER1
    global WORKSTATION_IP_ADDR_SER2
    out = ops1("show ntp associations", shell="vtysh")
    lines = out.split('\n')
    for line in lines:
        if WORKSTATION_IP_ADDR_SER1 in line:
            assert ('.NKEY.' or '.TIME.' or '.RATE.' or '.AUTH.') not in line,\
                "### NTP client has incorrect information###\n"
        if WORKSTATION_IP_ADDR_SER2 in line:
            assert ('.NKEY.' or '.TIME.' or '.RATE.' or '.AUTH.') not in line,\
                "### NTP client has incorrect information###\n"
    return True


def validatentpstatus(ops1, wrkston01, wrkston02, step):
    global WORKSTATION_IP_ADDR_SER2
    out = ops1("show ntp status", shell="vtysh")
    if 'Synchronized' in out:
        return True
    return False


def restartntpdaemon(ops1, wrkston01, wrkston02, step):
    ops1("systemctl restart ops-ntpd", shell="bash")
    sleep(30)
    output = ops1("ps -ef | grep ntpd", shell="bash")
    if 'ntpd -c' in output:
        print("### OPS-NTPD Daemon restart successful ###\n")
    else:
        print('### OPS-NTPD Daemon restart FAILED Please check###\n')


def chkntpassociationandstatus(ops1, wrkston01, wrkston02, step):
    global SERVER_UNREACHABLE
    total_timeout = 600
    timeout = 10
    check1 = False
    check2 = False
    for t in range(0, total_timeout, timeout):
        sleep(5)
        if check1 is False:
            check1 = validatentpassocinfo(ops1, wrkston01, wrkston02, step)
        if check2 is False:
            check2 = validatentpstatus(ops1, wrkston01, wrkston02, step)
        if check1 is True and check2 is True:
            return True
    if SERVER_UNREACHABLE is True:
        ops1("show ntp status", shell="vtysh")
        ops1("show ntp associations", shell="vtysh")
        wrkston01("ntpq -p -n", shell="bash")
        wrkston02("ntpq -p -n", shell="bash")
        return True
    print('### TIMEOUT TEST CASE FAILED ###\n')
    ops1("show ntp status", shell="vtysh")
    ops1("show ntp associations", shell="vtysh")
    wrkston01("ntpq -p -n", shell="bash")
    wrkston02("ntpq -p -n", shell="bash")
    return False


def test_ntpd_ft_auth_noauth_restart(topology, step):
    step("TEST CASE test_ntpd_ft_auth_noauth_restart VALIDATION")
    ops1 = topology.get('ops1')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')
    assert ops1 is not None
    assert hs1 is not None
    assert hs2 is not None
    ntpconfig(ops1, hs1, hs2, step)
    status = chkntpassociationandstatus(ops1, hs1, hs2, step)
    assert status is True
    restartntpdaemon(ops1, hs1, hs2, step)
    status = chkntpassociationandstatus(ops1, hs1, hs2, step)
    assert status is True

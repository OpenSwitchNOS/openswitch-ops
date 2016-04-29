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
TOPOLOGY = """
#
#    +--------+
#    |  ops1  |
#    +--------+
#
# Nodes
[type=openswitch name="OpenSwitch 1"] ops1
# Links
ops1:if01
"""
# Global Variable
min_lag = 1
max_lag = 2000
invalid_lag = "theLag01"
invalid_lag_zero = 0
invalid_lag_range = 2001
invalid_negative_lag = "-1"
"""
Author: Tamilmannan Harikrishnan - tamilmannan.h@hpe.com
testID: LAG FT Test
test name: lagStaticSupportedAndUnsupportedNames
test Description:  This test verifies that a static LAG can be configured
                   using correct names and cannot be configured if it
                   uses a name longer than permitted or if if the name
                   contains unsupported characters."""


def config_lag(ops1, lag_id, step):
    step("CONFIGURE THE LAG INTERFACE")
    with ops1.libs.vtysh.ConfigInterfaceLag(lag_id) as ctx:
        ctx.no_shutdown()


def negative_config_lag(ops1, lag_id, step):
    step("CONFIGURE THE INVALID LAG INTERFACE VALIDATION")
    config_command = "configure terminal"
    ops1(config_command, shell="vtysh")
    lag_command = "interface lag " + str(lag_id)
    lag_output = ops1(lag_command, shell="vtysh")
    assert lag_output == '% Unknown command.'
    ops1("end", shell="vtysh")


def test_lagstaticsupportedandunsupportednames(topology, step):
    step("TEST CASE lagStaticSupportedAndUnsupportedNames VALIDATION")
    ops1 = topology.get('ops1')
    assert ops1 is not None
    config_lag(ops1, min_lag, step)
    config_lag(ops1, max_lag, step)
    negative_config_lag(ops1, invalid_lag, step)
    negative_config_lag(ops1, invalid_lag_zero, step)
    negative_config_lag(ops1, invalid_lag_range, step)
    negative_config_lag(ops1, invalid_negative_lag, step)

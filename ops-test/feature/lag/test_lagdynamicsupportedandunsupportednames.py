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
test name: lagDynamicSupportedAndUnsupportedNames
test Description:  This test is to validate dynamic LAG can be configured
                   using valid names or can be configured using
                   an invalid name."""


def lag_possitive_validation(ops1, lag_name, step):
    step("LAG POSSITIVE VALIDATION")
    status = ops1.libs.vtysh.show_lacp_aggregates()
    key = "lag" + str(lag_name)
    assert status[str(key)]['name'] == key


def lag_negative_validation(ops1, lag_name, step):
    step("LAG NEGATIVE VALIDATION")
    status = ops1.libs.vtysh.show_lacp_aggregates()
    key = "lag" + str(lag_name)
    assert status.get(str(key), None) is None


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


def config_active_lag(ops1, lag_id, step):
    step("CONFIGURE ACTIVE MODE TO THE LAG INTERFACE")
    with ops1.libs.vtysh.ConfigInterfaceLag(lag_id) as ctx:
        ctx.lacp_mode_active()


def test_lagdynamicsupportedandunsupportednames(topology, step):
    step("TEST CASE lagDynamicSupportedAndUnsupportedNames VALIDATION")
    ops1 = topology.get('ops1')
    assert ops1 is not None
    config_lag(ops1, min_lag, step)
    lag_possitive_validation(ops1, min_lag, step)
    config_active_lag(ops1, min_lag, step)
    config_lag(ops1, max_lag, step)
    lag_possitive_validation(ops1, max_lag, step)
    config_active_lag(ops1, max_lag, step)
    negative_config_lag(ops1, invalid_lag, step)
    lag_negative_validation(ops1, invalid_lag, step)
    negative_config_lag(ops1, invalid_lag_zero, step)
    lag_negative_validation(ops1, invalid_lag_zero, step)
    negative_config_lag(ops1, invalid_lag_range, step)
    lag_negative_validation(ops1, invalid_lag_range, step)
    negative_config_lag(ops1, invalid_negative_lag, step)
    lag_negative_validation(ops1, invalid_negative_lag, step)
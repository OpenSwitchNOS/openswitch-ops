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
max_lag = 2
interface = 10
"""
Author: Tamilmannan Harikrishnan - tamilmannan.h@hpe.com
testID: LAG FT Test
test name: lagStaticInterfacesOnOtherLAG
test Description:  Test verifies that an interface can be moved
                   from one static LAG to another static LAG."""


def lag_possitive_validation(ops1, lag_name, step):
    step("LAG POSSITIVE VALIDATION")
    status = ops1.libs.vtysh.show_lacp_aggregates()
    key = "lag" + str(lag_name)
    assert status[str(key)]['name'] == key


def config_lag(ops1, lag_id, step):
    step("CONFIGURE THE LAG INTERFACE")
    with ops1.libs.vtysh.ConfigInterfaceLag(lag_id) as ctx:
        ctx.no_shutdown()


def validate_lag(ops1, interface, lag_id, step):
    step("VALIDATE THE LAG INTERFACE")
    out = ops1.libs.vtysh.show_lacp_interface(interface)
    assert out['lag_id'] == str(lag_id)


def test_ft_lag_static_interfaces_otherlag(topology, step):
    step("TEST CASE lagStaticInterfacesOnOtherLAG VALIDATION")
    ops1 = topology.get('ops1')
    assert ops1 is not None
    config_lag(ops1, min_lag, step)
    lag_possitive_validation(ops1, min_lag, step)
    with ops1.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.lag(min_lag)
    validate_lag(ops1, interface, min_lag, step)
    config_lag(ops1, max_lag, step)
    lag_possitive_validation(ops1, max_lag, step)
    with ops1.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.lag(max_lag)
    validate_lag(ops1, interface, max_lag, step)

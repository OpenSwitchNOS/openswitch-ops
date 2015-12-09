#!/usr/bin/env python
#
# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
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

import crypt


# User Management
DEFAULT_USER_GRP = "ovsdb_users"
CLI_PROMPT = "/usr/bin/vtysh"
BASH_PROMPT = "/usr/bin/bash"


def create_user(dut, user_prefix, password, user_group, user_prompt, num):
    user_list = []
    password = crypt.crypt(password, "$6$ab$").replace("$", "\$")
    if user_group == "ovsdb_users":
        user_list.append({"username": "admin"})
    for i in range(0, num):
        user_name = user_prefix + "_user_" + str(i)
        dut.switch.cmd("useradd " + user_name + " -p " + password +
                       " -g " + user_group + " -s " + user_prompt)
        user_list.append({"username": user_name})
    return user_list


def delete_user(dut, user_prefix, num):
    for i in range(0, num):
        user_name = user_prefix + "_user_" + str(i)
        dut.switch.cmd("userdel -r " + user_name)

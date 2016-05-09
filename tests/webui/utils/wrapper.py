#!/usr/bin/env python
#
# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
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

from functools import wraps
from opsvsi.opsvsitest import *


def retry_wrapper(
    init_msg,
    soft_err_msg,
    time_steps,
    timeout,
    err_condition=None
):
    if err_condition is None:
        err_condition = AssertionError

    def actual_retry_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(init_msg)
            cont = 0
            while cont <= timeout:
                try:
                    func(*args, **kwargs)
                    print('#### Completed in {} out of {} second timout ####'.
                          format(cont, timeout))
                    return
                except err_condition:
                    print(soft_err_msg)
                    if cont < timeout:
                        print('Waiting {} seconds to retry'.format(
                            time_steps
                        ))
                        sleep(time_steps)
                        cont += time_steps
                        continue
                    print('Retry time of {} seconds expired'.format(
                        timeout
                    ))
                    raise
        return wrapper
    return actual_retry_wrapper

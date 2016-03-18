# -*- coding: utf-8 -*-
#
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

"""
OpenSwitch Test for ECMP Resilient Hash
"""
from pytest import mark
# from pytest import set_trace
from time import sleep
# from re import match
import threading
# import re

TOPOLOGY = """
#                             +-------+
#                             |       |
#                    +-------->  nh1  |
#                    |        |       |
#                    |        +-------+
#                    |
# +-------+          |        +-------+
# |       |     +----v--+     |       |
# |  hs1  <----->  sw1  <----->  nh2  |
# |       |     +----^--+     |       |
# +-------+          |        +-------+
#                    |
#                    |        +-------+
#                    |        |       |
#                    +-------->  nh3  |
#                             |       |
#                             +-------+

# Nodes
[type=openswitch name="Switch 1"] sw1
[type=host name="Host 1"] hs1
[type=host name="Nexthop 1"] nh1
[type=host name="Nexthop 2"] nh2
[type=host name="Nexthop 3"] nh3

# Links
sw1:1 -- nh1:1
sw1:2 -- nh2:1
sw1:3 -- nh3:1
sw1:4 -- hs1:1
"""

PING_DEST_RE = (
    r'^From (?P<source>[0-9a-f.:]+) icmp_seq=\d+ .+$'
)

exit_flag = False   # 1 writer, many readers
check_ping = False  # 1 writer, many readers
nexthop_lock = threading.Lock()
nexthop_list = []   # All can write
threads = []


def my_assert(cond):
    global exit_flag
    global threads
    if not cond:
        exit_flag = True
        for t in threads:
            t.join()
    assert cond


class GeneratorThread (threading.Thread):
    '''Generate traffic from the host until
       a nexthop is found
    '''
    def __init__(self, thread_id, host, src, dst):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.host = host
        self.src = src
        self.dst = dst

    def run(self):
        global nexthop_lock
        global nexthop_list  # Read only
        global exit_flag
        while exit_flag is False and not nexthop_list:
            print("###### Inside thread Ping Start  ######")
            generated_traffic = self.host('ping -c 50 -i 0.5 '
                                          '{0}'.format(self.dst))
            print("generated_traffic", generated_traffic)
            my_assert(generated_traffic is not None)


class ReceiverThread (threading.Thread):
    '''Receive traffic on the nexthop via tcpdump
       Update the nexthop_list when packets are found
    '''
    def __init__(self, thread_id, host, src, dst):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.host = host
        self.src = src
        self.dst = dst
        self.daemon = True

    def run(self):
        global nexthop_lock
        global nexthop_list
        global check_ping
        global exit_flag
        while exit_flag is False:
            print("Self.host", self.host)
            dumped_traffic = self.host('timeout 5 tcpdump -ni eth1 '
                                       'dst {0}'.format(self.dst))
            # m = re.search("(20.0.0.10 > 70.0.0.1)", dumped_traffic)
            m = dumped_traffic.find("{0} > {1}".format(self.src, self.dst))
            print("Printing thread_id", self.thread_id)
            if m != -1 and not nexthop_list:
                print("Find results: ", m)
                nexthop_lock.acquire()
                if check_ping is True:
                    # Main thread may have cleared the list by the time we got
                    # here
                    nexthop_list.append(self.thread_id)
                    print("nexthop_list Receiver", nexthop_list)
                nexthop_lock.release()


@mark.test_id(10000)
@mark.platform_incompatible(['docker'])
def test_ecmp(topology):
    """
    Set network addresses and static routes between a host, switch, and 3
    hosts acting as next hops. Use the response from ping to ensure flows
    not disrupted when a next hop is removed or added
    """
    global threads
    global nexthop_list
    global nexthop_lock
    global check_ping

    sw1 = topology.get('sw1')
    hs1 = topology.get('hs1')
    nh1 = topology.get('nh1')
    nh2 = topology.get('nh2')
    nh3 = topology.get('nh3')

    assert sw1 is not None
    assert hs1 is not None
    assert nh1 is not None
    assert nh2 is not None
    assert nh3 is not None

    ps1hs1 = sw1.ports['4']
    ps1nh1 = sw1.ports['1']
    ps1nh2 = sw1.ports['2']
    ps1nh3 = sw1.ports['3']
    phs1 = hs1.ports['1']
    pnh1 = nh1.ports['1']
    pnh2 = nh2.ports['1']
    pnh3 = nh3.ports['1']

    # Configure IP and bring UP host 1 interfaces
    hs1.libs.ip.interface('1', addr='20.0.0.10/24', up=True)

    # Configure IP and bring UP nexthop 1 interfaces
    nh1.libs.ip.interface('1', addr='1.0.0.1/24', up=True)

    # Configure IP and bring UP nexthop 2 interfaces
    nh2.libs.ip.interface('1', addr='2.0.0.1/24', up=True)

    # Configure IP and bring UP nexthop 3 interfaces
    nh3.libs.ip.interface('1', addr='3.0.0.1/24', up=True)

    # Configure IP and bring UP switch 1 interfaces
    # sw1 <-> hs1
    with sw1.libs.vtysh.ConfigInterface('4') as ctx:
        ctx.ip_address('20.0.0.1/24')
        ctx.no_shutdown()

    # sw1 <-> nh1
    with sw1.libs.vtysh.ConfigInterface('1') as ctx:
        ctx.ip_address('1.0.0.2/24')
        ctx.no_shutdown()

    # sw1 <-> nh2
    with sw1.libs.vtysh.ConfigInterface('2') as ctx:
        ctx.ip_address('2.0.0.2/24')
        ctx.no_shutdown()

    # sw1 <-> nh3
    with sw1.libs.vtysh.ConfigInterface('3') as ctx:
        ctx.ip_address('3.0.0.2/24')
        ctx.no_shutdown()

    # now wait for interfaces to come up
    show_int1 = ''
    show_int2 = ''
    show_int3 = ''
    show_int4 = ''
    attempts = 10
    while (
      ("Interface {ps1hs1} is up".format(**locals()) not in show_int1) and
      ("Interface {ps1hs1} is up".format(**locals()) not in show_int2) and
      ("Interface {ps1hs1} is up".format(**locals()) not in show_int3) and
      ("Interface {ps1hs1} is up".format(**locals()) not in show_int4) and
      attempts > 0):
        sleep(2)
        show_int1 = sw1('show interface {ps1hs1}'.format(**locals()))
        show_int2 = sw1('show interface {ps1nh1}'.format(**locals()))
        show_int3 = sw1('show interface {ps1nh2}'.format(**locals()))
        show_int4 = sw1('show interface {ps1nh3}'.format(**locals()))
        attempts = attempts + 1

    # Set ECMP static routes in switch
    with sw1.libs.vtysh.Configure() as ctx:
        ctx.ip_route('70.0.0.0/24', '1.0.0.1')
        ctx.ip_route('70.0.0.0/24', '2.0.0.1')
        ctx.ip_route('70.0.0.0/24', '3.0.0.1')

    sw1('ip netns exec swns ip route list', shell="bash")

    # Set gateway in host
    hs1.libs.ip.add_route('default', '20.0.0.1')

    # Next hops need a route back to the hs1 for the icmp replies
    nh1.libs.ip.add_route('20.0.0.0/24', '1.0.0.2')
    nh2.libs.ip.add_route('20.0.0.0/24', '2.0.0.2')
    nh3.libs.ip.add_route('20.0.0.0/24', '3.0.0.2')

    # set_trace()
    hs1.libs.ping.ping(1, '1.0.0.1')
    hs1.libs.ping.ping(1, '2.0.0.1')
    hs1.libs.ping.ping(1, '3.0.0.1')

    hs1_thread = GeneratorThread('20.0.0.10', hs1, '20.0.0.10', '70.0.0.1')
    nh1_thread = ReceiverThread('1.0.0.1', nh1, '20.0.0.10', '70.0.0.1')
    nh2_thread = ReceiverThread('2.0.0.1', nh2, '20.0.0.10', '70.0.0.1')
    nh3_thread = ReceiverThread('3.0.0.1', nh3, '20.0.0.10', '70.0.0.1')

    threads.append(hs1_thread)
    threads.append(nh1_thread)
    threads.append(nh2_thread)
    threads.append(nh3_thread)

    # set_trace()
    nh1_thread.start()
    nh2_thread.start()
    nh3_thread.start()
    check_ping = True  # Start checking for ping traffic
    hs1_thread.start()

    print("nexthop_list Main", nexthop_list)
    # set_trace()
    attempts = 3
    # The ReceiverThread will append its IP to the nexthop_list when it
    # sees traffic
    while not nexthop_list and attempts > 0:
        attempts -= 1
        sleep(5)

    print("nexthop_list Main", nexthop_list)
    check_ping = False  # Receivers stop updating nexthop_list
    # set_trace()
    # Make sure we found one and only one next hop
    my_assert(len(nexthop_list) == 1)

    # Shut off one of the unused next hops; make sure the current one is not
    # disturbed
    nexthop_lock.acquire()
    first_nexthop = nexthop_list[0]

    # Currently this won't work, given a bug in OPS that does not reconfigure
    # Nexthops in the FIB when a port goes down.
    # TODO: Ashwin to re-enable this when that bug is fixed
    # Instead, remove the next hop from the switch

    if nexthop_list[0] == '1.0.0.1':
        # nh2.libs.ip.interface(pnh2, up=False)
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.no_ip_route('70.0.0.0/24', '2.0.0.1')
    if nexthop_list[0] == '2.0.0.1':
        # nh3.libs.ip.interface(pnh3, up=False)
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.no_ip_route('70.0.0.0/24', '3.0.0.1')
    if nexthop_list[0] == '3.0.0.1':
        # nh1.libs.ip.interface(pnh1, up=False)
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.no_ip_route('70.0.0.0/24', '1.0.0.1')

    nexthop_list = []
    print("nexthop_list Main", nexthop_list)
    check_ping = True  # Start checking for ping traffic
    nexthop_lock.release()

    # set_trace()
    attempts = 5
    # The ReceiverThread will append its IP to the nexthop_list when it
    # sees traffic
    while not nexthop_list and attempts > 0:
        attempts -= 1
        sleep(15)

    print("nexthop_list Main", nexthop_list)
    check_ping = False  # Receivers stop updating nexthop_list
    # Make sure we found one and only one next hop
    print("nexthop_list Main after check_ping", nexthop_list)
    print("nexthop_list Main Length", len(nexthop_list))
    my_assert(len(nexthop_list) == 1)
    # Make sure the flow didn't move to another nexthop
#    my_assert(nexthop_list[0] == first_nexthop)

    # Turn the unused next hop back on; make sure the current one is not
    # disturbed
    nexthop_lock.acquire()
    # Currently this won't work, given a bug in OPS that does not reconfigure
    # Nexthops in the FIB when a port goes up or down.
    # TODO: Ashwin to re-enable this when that bug is fixed
    # Instead, add the next hop to the switch

    if first_nexthop == '1.0.0.1':
        # nh2.libs.ip.interface(pnh2, up=True)
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.ip_route('70.0.0.0/24', '2.0.0.1')
    if first_nexthop == '2.0.0.1':
        # nh3.libs.ip.interface(pnh3, up=True)
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.ip_route('70.0.0.0/24', '3.0.0.1')
    if first_nexthop == '3.0.0.1':
        # nh1.libs.ip.interface(pnh1, up=True)
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.ip_route('70.0.0.0/24', '1.0.0.1')

    nexthop_list = []
    print("nexthop_list Main", nexthop_list)
    check_ping = True  # Start checking for ping traffic
    nexthop_lock.release()

    # set_trace()
    attempts = 5
    # The ReceiverThread will append its IP to the nexthop_list when it
    # sees traffic
    while not nexthop_list and attempts > 0:
        attempts -= 1
        sleep(15)

    print("nexthop_list Main", nexthop_list)
    check_ping = False  # Receivers stop updating nexthop_list
    # Make sure we found one and only one next hop
    print("nexthop_list Main after check_ping", nexthop_list)
    print("nexthop_list Main Length", len(nexthop_list))
    my_assert(len(nexthop_list) == 1)
    # Make sure the flow didn't move to another nexthop
#    my_assert(nexthop_list[0] == first_nexthop)

    # Now we want to turn off the next hop in use
    nexthop_lock.acquire()
    first_nexthop = nexthop_list[0]
    # Currently thss won't work, gsven a bug in OPS that does not reconfigure
    # Nexthops in the FIB when a port goes up or down.
    # TODO: Ashwin to re-enable this when that bug is fixed
    # Instead, remove the next hop from the switch

    if first_nexthop == '1.0.0.1':
        # nh1.libs.ip.interface(pnh1, up=False)
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.no_ip_route('70.0.0.0/24', '1.0.0.1')
    if first_nexthop == '2.0.0.1':
        # nh2.libs.ip.interface(pnh2, up=False)
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.no_ip_route('70.0.0.0/24', '2.0.0.1')
    if first_nexthop == '3.0.0.1':
        # nh3.libs.ip.interface(pnh3, up=False)
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.no_ip_route('70.0.0.0/24', '3.0.0.1')

    sw1('ip netns exec swns ip route list', shell="bash")
    nexthop_list = []
    check_ping = True  # Start checking for ping traffic
    print("nexthop_list Main", nexthop_list)
    nexthop_lock.release()

    # set_trace()
    attempts = 3
    # The ReceiverThread will append its IP to the nexthop_list when it
    # sees traffic
    while not nexthop_list and attempts > 0:
        attempts -= 1
        sleep(15)

    # set_trace()
    print("nexthop_list Main", nexthop_list)
    check_ping = False  # Receivers stop updating nexthop_list
    print("nexthop_list Main after check_ping", nexthop_list)
    print("nexthop_list Main Length", len(nexthop_list))
    # Because we lock, clear, and release the nexthop_list
    # there should only be one entry
    my_assert(len(nexthop_list) == 1)
    # Make sure the flow goes to another next hop
#    my_assert(first_nexthop not in nexthop_list)

    # Re-enable the first next hop
    nexthop_lock.acquire()
    print("first_nexthop", first_nexthop)
    second_nexthop = nexthop_list[0]
    # Currently this won't work, given a bug in OPS that does not reconfigure
    # Nexthops in the FIB when a port goes up or down.
    # TODO: Ashwin to re-enable this when that bug is fixed
    # Instead, add the next hop to the switch

    if first_nexthop == '1.0.0.1':
        # nh1.libs.ip.interface(pnh1, up=False)
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.ip_route('70.0.0.0/24', '1.0.0.1')
    if first_nexthop == '2.0.0.1':
        # nh2.libs.ip.interface(pnh2, up=False)
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.ip_route('70.0.0.0/24', '2.0.0.1')
    if first_nexthop == '3.0.0.1':
        # nh3.libs.ip.interface(pnh3, up=False)
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.ip_route('70.0.0.0/24', '3.0.0.1')
    sleep(20)
    sw1('ip netns exec swns ip route list', shell="bash")

    nexthop_list = []
    print("########## testing #####")
    check_ping = True  # Start checking for ping traffic
    print("nexthop_list Main", nexthop_list)
    hs1.libs.ping.ping(100, '70.0.0.1')
    nexthop_lock.release()
    # hs1.libs.ping.ping(100, '70.0.0.1')
    # set_trace()
    attempts = 3
    # The ReceiverThread will append its IP to the nexthop_list when it
    # sees traffic
    while not nexthop_list and attempts > 0:
        attempts -= 1
        sleep(15)

    print("nexthop_list Main", nexthop_list)
    check_ping = False  # Receivers stop updating nexthop_list
    print("nexthop_list Main after check_ping", nexthop_list)
    print("nexthop_list Main Length", len(nexthop_list))
    # Because we lock, clear, and release the nexthop_list
    # there should only be one entry
    my_assert(len(nexthop_list) == 1)
    # Make sure the flow goes to another next hop
    my_assert(first_nexthop not in nexthop_list)
    my_assert(second_nexthop in nexthop_list)

    exit_flag = True

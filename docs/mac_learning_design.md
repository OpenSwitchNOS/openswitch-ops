# MAC Learning Design:
----------------------

- [Overview](#overview)
- [Design considerations](#design-considerations)
- [OVSDB schema]($ovsdb-schema)
- [High Level Design](#high-level-design)
- [Design detail](#design-detail)
- [Operations on MAC table](#operations-mac-table)
- [References](#references)


## Overview:
------------

Using MAC Learning, the switch learns MAC Addresses in the network in order to identify on which port to send traffic in order to avoid flooding.
The current implementation involves ASIC to learn the MAC addresses on all interfaces and software to maintain the MAC address table.


## Design considerations:
-------------------------

i. Reliability
   No dynamic memory allocation in the opennsl plugin layer. This is to shorten the time to copy information given by the ASIC so that no entry is missed.
ii. Performance
    The callback function is running in a separate thread, need to separate the data stored so that the main thread can read and the callback thread can write to different buffers to avoid any waiting period.
iii. Efficiency
     Use of the data structure such that finding the entry should be O(1).
     This is because it's very possible that ASIC can learn a MAC on a port and it's moved to a different port in a relatively short time.

The hash map used in the opennsl plugin only holds the delta (difference) of the recent changes. The final MAC Table is in OVSDB.


## OVSDB Schema:
----------------

The following columns are written:
```
mac_addr: MAC address learnt
bridge: bridge reference
vlan: VLAN associated
from: Who has configured/learnt
port: Port reference
```


## High level design:
---------------------

```
     +-------------+
     |             |
     |    OVSDB    |
     |             |
     +-------------+
            ^
            |4                                                                                 ops-switchd process
  +---------|------------------------------------------------------------------------------------------------------+
  |         |                                +------------------------------------------------------------------+  |
  |  +-------------+                         |                       opennsl plugin                             |  |
  |  | vswitchd    |                     1   |                                                                  |  |
  |  | main        |-------------------------|--------> init()                                                  |  |
  |  | thread      |                         |            |                                                     |  |
  |  +-------------+                         |            |                                                     |  |
  |        ^                                 |            |                                                     |  |
  |        |                                 |            |                                           2         |  |
  |        |                                 |            |                                        +------      |  |
  |        |                                 |            v                                        |     |      |  |
  |        |                                 |    mac_learning_init +-----> opennsl_l2_addr_reg(cb_fn)   |      |  |
  |        |                                 |                      |-----> opennsl_l2_traverse(cb_fun)  +----  |  |
  |        |                                 |                                                           |   |  |  |
  |        |                                 |                                                           v   |  |  |
  |        |                                 |   +--------------+                                 +--+  +--+ |  |  |
  |        |           3                     |   |              |                                 |  |  |--| |  |  |
  |        +---------------------------------|---|  bcm timer   |                                 |  |  |  | |  |  |
  |        |                                 |   |    thread    |                                 +--+  +--+ |  |  |
  |        |                                 |   +--------------+                                   HMAPS    |  |  |
  |        |           3                     |                                                               |  |  |
  |        +---------------------------------|---------------------------------------------------------------+  |  |
  |                                          |                                                                  |  |
  |                                          +------------------------------------------------------------------+  |
  +----------------------------------------------------------------------------------------------------------------+

```

The above diagram describes the steps of the interaction between difference functions and threads in ops-switchd process.
1. When the process starts, the main thread creates bcm init thread to do the initialization. As part of the mac learning, the initialization involves registering for callback functions in SDK when a L2 address is added/deleted in L2 table.
2. The callback function is called by the SDK as part of a separate thread. The callback routine involves adding the entries in the hmap.
3. When the hmap is full or the timer thread times out which ever event happens first, the notification to switchd main thread is triggered.
4. Once the switchd main thread gets the notification, it will process the hmap and add/delete the entries in the database.

## Design detail:
-----------------

1. asic-plugin changes
   This comprises of the PD implementation of PI-PD API.
2. Registering for BCM callback
   MACs are learnt by ASIC and are stored in L2 Table in ASIC.
3. Callback function, updating the hmap
4. notifying switchd main thread
5. mac learing plugin
6. updating OVSDB

### Details:
------------

1. asic-plugin changes
                                                  switchd main thread
    +-------------------------------------------------------------------------------------------------------+
    |      main() in ovs-vswitchd.c                         |            bcm_plugins.c                      |
    |                                                       |                                               |
    |      plugins_init() ----------------------------------|---------------> init()                        |
    |                                                       |                                               |
    |                                                       |            get_mac_learning_hmap (added)      |
    +-------------------------------------------------------------------------------------------------------+

   asic plugin is the new developed infrastructure to use plugin model instead of ofproto-provider APIs. This extends the PI-PD functionality such that the APIs can be invoked independent of ofproto knowledge. This is extremely necessary in the case of mac learning as when more than one ASICs will be supported, at that time the hmap to store the new entries of the L2 table will be shared across all the ASICs. Hence to limit it per bridge won't be beneficial.

  Changes involved to add the PI-PD function in the asic plugins.


2. Registering for BCM callback

    bcm_init thread

    init()   -------------> ops_mac_learning_init()  ------------------> opennsl_l2_addr_register & opennsl_l2_traverse()

   The bcm init thread is created by switchd main thread to do the initialization of the ASIC SDK. New function was added for mac learning to register for callback for learnt l2 addresses as well as traverse the current l2 addresses in L2 MAC table. There is no use of registering opennsl_l2_traverse as whenever the switchd process restarts, ASIC is reset. Once HA infrastructure will be in place, this function will be useful when the process restarts and to do mark and sweep.


3. Callback function, updating the hmap

   Whenever any L2 entry is added/deleted in L2 Table in ASIC, the SDK will invoke the callback function used to registration (Point 2.). This is not a bulk call and hence the main criteria is to use least time spent while copying the entry to the hash map.

   The hash is the combination of MAC address, VLAN and hw_unit (which ASIC?).

4. How hash maps are getting used?

   The opennsl plugin will be writing to the hmap and the mac learning plugin will be reading from the hmaps. As the opennsl plugin and mac learning plugin are part of same ops-switchd process, using of two hmaps will avoid using lock for reading the hmap. While writing to hmap, the lock needs to be used as bcm init thread and vswitchd main thread can simultaneously write to the hmap. Using two hmap buffer also provides advantage in case of the incoming L2 entries in one hmap gets full quicker, the second hmap can be used immediately to avoid loss of any updates from the SDK.


5. notifying switchd main thread

   When the updates for L2 entry are received from the SDK, they are stored locally in opennsl plugin. In order for it to be written in OVSDB, the updates need to go to switchd main thread. OVS has seq_change to trigger notification to the thread waiting on the event to be triggered for that sequence.
   The sequence change can occur in the two cases:
   i. the current hmap is full.
   ii. The timer thread times out and there is at-least an entry in the hmap.


6. mac_learing plugin

```ditaa
    +-------------------------------------------------------------------------------------------------------+
    |      main() in ovs-vswitchd.c                         |            mac_learning_plugin.c              |
    |                                                       |                                               |
    |      plugins_init() ----------------------------------|---------------> init()                        |
    |                                                       |                                               |
    |                                                       |                                               |
    |      plugins_wait() ----------------------------------|---------------> wait()                        |
    |                                                       |                                               |
    |                                                       |                                               |
    |      plugins_run() -----------------------------------|---------------> run()                         |
    |                                                       |                                               |
    |                                                       |                                               |
    |      plugins_destroy() -------------------------------|---------------> destroy()                     |
    |                                                       |                                               |
    +-------------------------------------------------------------------------------------------------------+

```

    The mac learning plugin is part of ops-switchd repository. This plugin was created to remove the dependency on modifying bridge.c for all features.
    It comprises of: init(), wait(), run() and destroy. It's order of execution is similar to bridge_init(), bridge_wait(), bridge_run() and bridge_destroy().
    The init is called during the initialization, wait and run will be in continuous infinite loop until the process exits. During the exit, destroy is invoked.

    Mac learning plugin init registers the plugin extension, registers for the bridge init event.
    Wait does wait on the sequence change event in order to get notifications from PD.
    run will reconfigure the MAC Table in OVSDB depending on the changes.
    Destroy will unregister the plugin extension.

7. updating ovsdb

   This function will be invoked by run() in mac learnng plugin. It does check for the seq change. If change is detected, it will use the asic plugin to invoke PI-PD API to get the hmap.
   Based on the hmap contents, it will modify OVSDB.

## Operations on MAC table:
---------------------------

Currently supported operations:

i. MAC Address (dynamic) learning
   Dynamically learnt MAC address when a frame is received whose source MAC address is not present on the MAC table for the port.

ii. MAC Move
    MAC Move occurs when the same MAC address is learnt on a different port in the bridge for same VLAN.

iii. MAC address aging
     The synamically learnt MAC addresses are deleted from the MAC table if the the age-out timer expires and no frame is received for the same MAC address, VLAN on the port.

## Current hard coded values:
-----------------------------

1. Two hmap buffers
2. hmap buffer size is 16K (will be changed to optimum value after having scale performance testing).
3. The timeout of the timer thread to invoke notification to switchd main thread is 1 minute.

## References:
--------------

* [Openvswitch] (http://openvswitch.org/)

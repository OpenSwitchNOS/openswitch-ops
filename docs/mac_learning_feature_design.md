# Mac Learning Design:
----------------------

- [Overview](#overview)
- [OVSDB schema]($ovsdb-schema)
- [High Level Design](#high-level-design)
- [Design detail](#design-detail)
- [References](#references)


## Overview:
------------

Using mac learning, the switch learns MAC addresses in the network in order to identify on which port to send traffic in order to avoid flooding.
The current implementation involves ASIC to learn the MAC addresses on all interfaces and software to maintain the MAC address table.


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
      |4                                   ops-switchd process
  +---|------------------------------------------------------------+
  |   |                                                            |
  |   |                                                            |
  |   |    mac_learning_plugin                asic-plugin          |
  |   |   +-------------+         +-----------------------------+  |
  |   |   |    init (1) |         |                             |  |
  |   |   |             |   3     |                             |  |
  |   ----|----run------|---------|---> get_mac_learning_hmap() |  |
  |       |             |         |                             |  |
  |       |    wait (2) |         |                             |  |
  |       |             |         +-----------------------------+  |
  |       |    exit (5) |                                          |
  |       +-------------+                                          |
  +----------------------------------------------------------------+

```

The above diagram describes the steps in terms of ops-switchd.
1. When the process ops-switchd starts, the main thread creates invokes plugin_init. The initialization is responsible for creating mac_learning plugin and registering for MAC table for read/write access.
2. wait function registers for event to happen. In this case register for sequence change event.
3. run function detects sequence change event, if found it invokes asic plugin API to get the hmap.
4. Once the hmap is received, the main thread processes it and update the necessary changes in OVSDB.
5. exit function removes any dynamically allocated memory during initialization.
[Refer to #design-detail for further information related to mac learning plugin]

## Design detail:
-----------------

1. asic-plugin changes (ops-switchd, platform plugin)
   This comprises of the PD implementation of PI-PD API.
2. mac learing plugin (ops-switchd)
3. updating OVSDB (ops-switchd)

### Details:
------------

1. asic-plugin changes
                                                  switchd main thread
    +-------------------------------------------------------------------------------------------------------+
    |      main() in ovs-vswitchd.c                         |            platform plugin                    |
    |                                                       |                                               |
    |      plugins_init() ----------------------------------|---------------> init()                        |
    |                                                       |                                               |
    |                                                       |            get_mac_learning_hmap (added)      |
    +-------------------------------------------------------------------------------------------------------+

   asic plugin is the infrastructure to use plugin model instead of ofproto-provider APIs. This plugin extends the platform specific functionality such that the APIs can be invoked independent of ofproto knowledge. This is extremely necessary in the case of mac learning as the hmap to store the new entries of the L2 table is shared across all the ASICs. Hence to limit it per bridge would not be beneficial.

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
    It comprises of: init(), wait(), run() and destroy. It is order of execution is similar to bridge_init(), bridge_wait(), bridge_run() and bridge_destroy().
    The init is called during the initialization, wait and run are in continuous infinite loop until the process exits. During the exit, destroy is invoked.

    Mac learning plugin init registers the plugin extension, registers for the bridge init event.
    Wait does wait on the sequence change event in order to get notifications from PD.
    run reconfigures the MAC Table in OVSDB depending on the changes.
    Destroy unregisters the plugin extension.

7. Updating OVSDB

   This function is invoked by run() in mac learing plugin. It does check for the seq change. If change is detected, it uses the asic plugin to invoke PI-PD API to get the hmap.
   Based on the hmap contents, it modifies OVSDB.

## References:
--------------

* [Openvswitch] (http://openvswitch.org/)
* Component design: [ops-switchd-opennsl-plugin](/documents/dev/ops-switchd-opennsl-plugin/docs/mac_learning_design)

LLDP Test Cases

===============





## Contents



- [CLI](#cli)

  - [LLDP enable disable](#lldp-enable-disable)

  - [LLDP interface transmit and receive](#lldp-interface-transmit-and-receive)

  - [LLDP wait and hold timers](#lldp-wait-and-hold-timers)

- [SNMP](#snmp)

  - [snmpget](#snmpget)
  - [snmpgetNext](#snmpgetnext)
  - [snmpgetBulk](#snmpgetBulk)
  - [snmpwalk](#snmpwalk)
  - [Test to verify the SNMP master agent port operation](#test-to-verify-the-snmp-master-agent-port-operation)
  - [Test to verify the SNMP master communities operation](#test-to-verify-the-snmp-master-communities-operation)
  - [Test to verify the SNMP system MIB configurations](#test-to-verify-the-snmp-system-MIB-configurations)



##CLI

### LLDP enable disable

#### Objective

The test case checks if LLDP has been enabled or disabled on a switch port by checking the neighbor port ID for the connected neighboring switch.

#### Requirements

- Physical Switch/Switch Test setup

- **FT File**: `ops/tests/lldp/test_lldp_ft_enable_disable.py`(LLDP enable/disable)



#### Setup

##### Topology diagram

```ditaa

    +--------+               +--------+

    |        |               |        |

    |   S1   | <-----------> |   S2   |

    |        |               |        |

    +--------+               +--------+

```



#### Description

1. Create a topology with a single link between two switches, switch 1 and switch 2.

2. Configure **lldp** on switch 1 and switch 2 and enable the connected interfaces on both switches.

3. Wait for 30 seconds for the neighbors to advertise and check if we see the neighbors on the connected ports.

4. Disable **lldp** on both switches.

5. Check if neighbor entries have cleared on both switches.



###  LLDP interface transmit and receive

#### Objective

The test case checks if LLDP transmit and receive can be configured successfully for individual interfaces.

#### Requirements

- Physical Switch/Switch Test setup

- **FT File**: `ops/tests/lldp/test_lldp_ft_interface_txrx.py`(LLDP transmit/receive)



#### Setup

##### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   S2   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```



#### Description

1. Create a topology with a four links between two switches, switch 1 and switch 2.

2. Disable transmission on link 2 of switch 1(rx only), disable reception on link 3 of switch 1(tx only), disable both transmission and reception on link 4 of switch 1.

3. Configure **lldp** on switch 1 and switch 2 and enable the connected interfaces on both switches.

4. Wait for 30 seconds for the neighbors to advertise.

5. Check each of the cases for neighbor entries.

6. The link 1 on switch 1 and switch 2 is default case, so neighbors should be present on both.

7. The link 2 of switch 1 must have neighbor entry but link 2 of switch 2 must not.

8. The link 3 of switch 1 must not have neighbor entry but switch 2 link 3 must have.

9. The link 4 of switch 1 and switch 2 must not have neighbor entries.



###  LLDP wait and hold timers

#### Objective

The test case checks if LLDP wait and hold timers can be set.

#### Requirements

- Physical Switch/Switch Test setup

- **FT File**: `ops/tests/lldp/test_lldp_ft_wait_hold.py`(LLDP wait/hold)



#### Setup

##### Topology diagram

```ditaa

    +--------+               +--------+

    |        |               |        |

    |   S1   | <-----------> |   S2   |

    |        |               |        |

    +--------+               +--------+

```



#### Description

1. Create a topology with a single link between two switches, switch 1 and switch 2.

2. Configure transmit time of 5 seconds and hold time of 2 seconds on both the switches.

3. Enable **lldp** on both switches.

4. Wait for 15 seconds and check to see if neighbor entries are present.

5. Disable **lldp** on both the switches.

6. Wait for 15 seconds and check if neighbor entries have been deleted.



##SNMP



### Snmpget

#### Test case 1

##### Objective

The test case verifies that when a snmpget (v1/v2/v3) query for a LLDP object is processed by an SNMP agent, the data is properly retrieved from the OVSDB. The testcase is verified from a localhost and from workstation as well.



##### Requirements

- Physical Switch/switch, workstation Test setup



##### Setup



###### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```





##### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.

2. Query for an OID.

3. Configure the schema equivalent of the above OID through the CLI. Query for the same OID again.





##### Pass/Fail criteria

- This test passes in the following scenarios:

  - Example considered for this test case is *lldp_tx_interval*.

  - First query gets the default value of `lldp tx interval`

  - Second query gets the configured value of `lldp tx interval`.

- The test fails in the following scenarios:

  - Get query fails to read from the OVSDB.

  - Second query does not get the configured value.



#### Test case 2

##### Objective

This test verifies that a snmpget(v1/v2/v3) query for a LLDP object which does not have a schema equivalent, results in returning the default value. The testcase is verified from a localhost and from workstation as well.



##### Requirements

- Physical Switch/switch, workstation Test setup



##### Setup



###### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```





##### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.

2. Query for an OID which does not have a schema equivalent object.





##### Pass/Fail criteria

- This test passes if the query returns the default value.

- This test fails if the query does not return the default value.





### SnmpgetNext

#### Test case 1

##### Objective

- This test case verifies that when a snmpgetNext(v1/v2/v3) query for a lldp object is processed by the  SNMP agent, the data is properly retrieved from the OVSDB.



##### Requirements

- Physical Switch/switch, workstation Test setup





##### Setup



###### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```





##### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.

2. Query for the next OID.

3. Configure the schema equivalent of the above OID through the CLI. Query for the same OID again.



##### Pass/Fail criteria

- This test passes in the following scenarios:

  - First query gets the default value of a next OID in a lexicographical order.

  - Second query gets the configured value for the OID.

- The test fails in the following scenarios:

  - Get query fails to read from OVSDB.

  - Second query does not get the configured value.



#### Test case 2

##### Objective

This test verifies that a snmpgetNext(v1/v2/v3) query for a LLDP object which does not have a schema equivalent, results in a returning the default value. The testcase is verified from a localhost and from workstation as well.



##### Requirements

- Physical Switch/switch, workstation Test setup





##### Setup



###### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```





##### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.

2. Query for a OID whose next OID does not have a schema equivalent object.





##### Pass/Fail criteria

- The test passes if the query returns the default value.

- The test fails if the query does not return the default value.





### SnmpgetBulk

#### Test case 1

##### Objective

The test case verifies that when a snmpgetBulk(v1/v2/v3) query for a set of LLDP objects is processed by a SNMP agent, the data is retrieved properly from the OVSDB.The testcase is verified from a localhost and from workstation as well.



##### Requirements

- Physical Switch/switch, workstation Test setup





##### Setup



###### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```





##### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.

2. Query for an OID.

3. Configure the schema equivalent of the above OID through the CLI. Query for the same OID again.



##### Pass/Fail criteria

- This test passes in the following scenarios:

  - The first query gets the default values.

  - The second query gets the configured value for the OID.

- The test fails in the following scenarios:

  - The query fails to read from the OVSDB.

  - The second query does not get the configured value.



### Snmpwalk

#### Testcase 1

#### Objective

The test verifies that when using snmpwalk(v1/v2/v3), the query walks the complete LLDP-MIB.The testcase is verified from a localhost and from workstation as well.



#### Requirements

- Physical Switch/switch, workstation Test setup



#### Setup



##### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```





#### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.

2. Walk the table using snmpwalk.



##### Pass/Fail criteria

- The test passes if the query walks through all the OIDs of the LLDP-MIB.

- This tests fails if the query does not walk through all the OIDs of the LLDP-MIB.



### Test for cache timeout of a SNMP table

#### Objective

- The test verifies that when a OVSDB schema value of a MIB table object is changed through CLI, by default takes 30 seconds to reflect in SNMP container. the test is validated using snmpwalk(v3) before and after 30 seconds. The testcase is verified from a localhost and from workstation as well.



#### Requirements

- Physical Switch/switch, workstation Test setup



#### Setup



##### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```





#### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.

2. Configure a MIB table object in OVSDB, through CLI.

3. Walk the table using snmpwalk immediately.

4. Walk the table using snmpwalk after 30 seconds.



##### Pass/Fail criteria

- The test passes if the query walks through all the OIDs, and the configured value is reflected after 30 seconds.

- This tests fails if the query does not walk through all the OIDs or the value is not reflected even after 30 seconds.

### Test to verify the SNMP master agent port operation

#### Objective

- The test verifies that when a port on which a SNMP agent is liostening on to for the user queries is modified, the agent will listen on the new port. Test case is validated using snmpwalk version 2 query.



#### Requirements

- Physical Switch/switch, workstation Test setup



#### Setup



##### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```





#### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.
2. Configure a SNMP agent port using CLI `snmp-server agent-port <1-65535>`.
3. Verify the configuration using `show snmp agent-port`
4.  Walk the MIB using `snmpwalk` on configured port



##### Pass/Fail criteria

- The test passes if the query walks through all the OIDs on the new port.

- This tests fails if the query does not walk through all the OIDs on the new port.

### Test to verify the SNMP master communities operation

#### Objective

- The test verifies that when a new community is configured using CLI, all the snmp queries will answer to that community. Test case is validated using snmpwalk version 2 query.



#### Requirements

- Physical Switch/switch, workstation Test setup



#### Setup



##### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```





#### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.
2. Configure a SNMP community using CLI `snmp-server community WORD`.
3. Verify the configration using `show snmp community`
3. Walk the MIB.



##### Pass/Fail criteria

- The test passes if the query walks through all the OIDs for a configured community.

- This tests fails if the query does not walk through all the OIDs for a configured community.

### Test to verify the SNMP system MIB configurations.

#### Objective

- The test verifies that when a system MIB objects are configured through CLI, the new values are reflected when walked through system MIB. Test case is validated using snmpwalk version 2 query.



#### Requirements

- Physical Switch/switch, workstation Test setup



#### Setup



##### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```





#### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.

2. Configure a SNMP system description using `snmp-server system-description .LINE`.
3. Configure a SNMP system location using `snmp-server system-location .LINE`.
4. Configure a SNMP system contact using `snmp-server system-contact .LINE`.
5. Verify the configuration using `show anmp system`.
6. Configure hostname using `hostname WORD`
7. Walk the system MIB.



##### Pass/Fail criteria

- The test passes if the query walks through all the system MIB OIDs reflecting the configured values.

- This tests fails if the query does not walk through all the system MIB OIDs or does not reflect the configured values.

### Test to verify the SNMP version 3 configurations.

#### Objective

- The test verifies that when snmpv3 user is configured, agent responds to thye queries for the new user.



#### Requirements

- Physical Switch/switch, workstation Test setup



#### Setup



##### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```





#### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.

2. Configure a SNMPv3 user using CLI `snmpv3 user WORD [auth (md5|sha) auth-pass WORD [priv (aes | des) priv-pass WORD]]`
6. Verify the configuration using `show snmpv3 user`.
7. Walk on .1 for the configured user.



##### Pass/Fail criteria

- The test passes if the query walks through all the MIB OIDs.

- This tests fails if the query does not walk through  MIB OIDs.




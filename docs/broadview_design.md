High level design of FEATURE
============================

High level description of a FEATURE design. 

Please also refer to DESIGN.md document of the repo that contains BroadView daemon. 

Design choices
--------------
The BroadView Daemon was chosen, as it would export the BST Instrumentation Statistics in the Open BroadView Instrumentation defined REST API (JSON). This allows OpenSwitch to have the BroadView REST API support and allows Collectors and Instrumentation Apps to support OpenSwitch based switches. The same statistics are also available from the OVSDB Schema and would serve Collectors and Management systems that support OVSDB.

Participating modules
---------------------

                          +----+
+--------------------+    | O  |
|                    |    | V  |
| BroadView Daemon   <--->+ S  |
|                    |    | D  |
+--------------------+    | B  |
                          | |  |
                          | S  |
                          | e  |     +--------------------+
                          | r  |     |                    |
                          | v  <---->+                    |
                          | e  |     |     Driver         |
                          | r  |     +--------------------+
                          |    |
                          |    |
                          |    |
                          +----+

The BroadView Daemon interfaces with the OVSDB-Server and is loosely coupled with the Driver. The Driver is responsible for obtaining the statistics from the Switch Silicon and populating the BST statistics counters defined via the OVSDB schema. The Driver is the Publisher of the data and the BroadView Daemon is the Subscriber (consumer) of the data. This allows the design to be modular, with simple, well-defined interfaces.


The BroadView Daemon gets the configuration from the OVSDB schema. It exports statistics via its REST API using JSON messaging to a Collector or Controller. 



References
----------
* [BroadView design](/documents/dev/ops-broadview/DESIGN)


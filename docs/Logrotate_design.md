High level design of log-rotate
===============================

CLI or REST enables user to configure log-rotate parameters in to OVSDB. From OVSDB , a python script shall read the log-rotate config , populate the respective log-rotate config file (/etc/logrotate.ovs) and shall execute logrotate command 'logrotate /etc/logrotate.ovs'
 

Responsibilities
---------------

Log-rotate as a feature,

  - Rotates the log files either based on period or based on size or based on both period and size (whichever condition occurs first). 
  - Compresses the rotated log files.
  - Rotated log files shall be stored locally or transferred to the remote destination.


Design choices
--------------
The design decisions made for log-rotate:

- Log-rotate python script shall be a cron job scheduled every hour.
- Log-rotate script shall use Linux logrotate utility for log rotation.- 
- Post rotation,log-rotate script shall compress the rotated log file in gunzip format.
- All module logs shall be stored in var/log/messages and auth logs in /var/log/auth.log.Only logs stored in the above path will be rotated.
- Management of rotated log files:
  - Rotated log files shall be compressed and stored locally regardless of remote host configuration in the path '/var/log/'
  - Rotated log files shall be stored with respective time extension to the granularity of hour in the format "file1- YYYYMMDDHH.gz" (e.g., messages-2015080715.gz)
  - Replacement of rotated log files happen when number of old rotated log files exceeds 3. In case of replacement, newly rotated log file shall replace the oldest rotated log file.
- Remote transfer of rotated log files:
  -  Only TFTP protocol is supported in BASIL PSI release.
  -  Both IPv4 and IPv6 addresses are supported. But broadcast, multicast and loopback addresses are not supported.
  -  Only rotated log files at that instant of logrotation , shall be transferred to remote host and not old rotated log files.
  -  In case of TFTP failure, packet level failures are handled in protocol itself with retransmission. With tftp session failure, tftp retry will happen for 3 times. Each retry shall timeout in 5 second.


Relationships to external OpenSwitch entities
---------------------------------------------
The following diagram provides detailed description of relationships and interactions.

	
	+---------------+              +---------------+                      
	|               |              |               |                      
	|   CLI         |              |    REST       |                      
	|               |              |               |                      
	+--------+------+              +------+--------+                      
	         |                            |                                                 
	         |                            |                                                  
	         |                            |                                                 
	    +------------------------------------------------------------------------------------+
	    |  +----------------------------------------+                          OVSDB         |
	    |  |                             openvswitch|                                        |
	    |  | logrotate_config_col                   |                                        |
	    |  |                                        |                                        |
	    |  |                                        |                                        |
	    |  +----------------------------------------+                                        |
	    +------------------------------------------------------------------------------------+
	                          |                                                              
	                          |                                                             
	                          |                                                              
	                          |                                                             
	        +-----------------+--------------------+              
	        |                                      |              
	        |  Logrotate script scheduled as       |               
	        |    hourly cron job                   |               
	        |                                      |               
	        |                                      |               
	        +--------------------------------------+               


OVSDB-Schema
------------
The log-rotate configuration parameters are specified as logrotate\_config column in openVswitch table.

	+------------------------------------------------------------------------------------+
	|  +----------------------------------------+                          OVSDB         |
	|  |                             openvswitch|                                        |
	|  | logrotate_config_col                   |                                        |
	|  |                                        |                                        |
	|  |                                        |                                        |
	|  +----------------------------------------+                                        |
	+------------------------------------------------------------------------------------+


Internal structure
------------------
The various functionality of sub modules are :

####CLI####
The CLI module is used for configuring the various log-rotate configuration parameters such as period,maxsize and target. The CLI provides basic sanity check of the parameters entered like checking the validity of the IP entered, checking the range of maxsize etc.
The "logrotate\_config" column shall be updated by the CLI. 

The CLI also displays the log-rotate parameters with 'show' command.

####REST####
REST module works similar to CLI.

####Log-rotate script####
Log-rotate script (scheduled as a hourly cron job) is responsible for the following,

- Retrieving the configurations from OVSDB and populate the respective logrotate config file (/etc/logrotate.ovs)
- Execute the logrotate command using the updated config 'logrotate /etc/logrotate.ovs'
- Perform port rotate operations such as compression and remote transfer.  


  
References
----------
* [Logrotate CLI](http://www.openswitch.net/docs/redest1)
* ...

<!-- Include references to any other modules that interact with this module directly or through the database model. For example, CLI, REST, etc.
ops-fand might provide reference to ops-sensord, etc. -->

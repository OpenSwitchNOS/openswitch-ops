
Config Persistence
=======
<!--Provide the title of the feature-->
- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
	- [Configuration types](#configuration-types)
	- [Startup configuration persistence](#startup-configuration-persistence)
	- [Configuration Format](#configuration-format)
	- [Action Taken During Configuration Save](#action-taken-during-configuration-save)
	- [System Action Taken During System Boot](#system-action-taken-during-system-boot)
	- [User Actions](#user-actions)
- [CLI](#cli)
- [Related features](#related-features)

## Overview ##
 <!--Provide an overview here. This overview should give the reader an introduction of when, where and why they would use the feature. -->
In general, there are two types of configuration at any given time, the current "running" configuration and "startup" configuration. The running configuration is not persisted across reboots, whereas startup configuration is persisted across reboots. In the future, in order to facilitate rollbacks and local preservation of old configuration, we might add the ability to store multiple "startup" configurations. OSVDB schema would be designed to accommodate such a future enhancement.

## How to use the feature ##
###Configuration types
1) running: The running configuration is dynamic and is defined to be the current state of all the elements in the OVSDB that are of type "config".

2) startup: The startup configuration, if present,  is the configuration that will be used on next boot.

####Startup configuration persistence
When a configuration is "saved", such that it is persisted across reboots, it is stored into the "configuration" table in OVSDB (configtbl). Technically, this table resides in a separate DB, which is served by the same ovsdb-server daemon. In practice, this separation is only needed in order to provide different persistence characteristics for the table. Any daemon can still access the table in the same way as other tables.

The configtbl has zero or more rows. More than one row might be used in future releases to accommodate multiple persisted configurations. The content of each row includes:

- type: Only supported type is startup

- name: Unique name, specified either by the system or by the user (Currently not populated).

- writer: Identifies who requested this configuration to be saved (Currently not populated).
- date: Date/Time when this row was last modified (Currently not populated).
- config: Configuration data
- hardware: JSON formatted list of dictionaries containing the following information for all subsystems configured by the configuration data (Currently not populated).

####Configuration Format
The configuration data is stored as a JSON string. The schema used is the same schema used by the REST API.
####Action Taken During Configuration Save
When the user requests that the running configuration be saved as a startup-config, the following actions are taken

- All OVSDB elements of type config are extracted from the database and formatted into the configuration format as noted above.
- If startup row is not found in configdb create a new row with type=startup or overwite the existing row and save the configuration to config row.
- Configtbl is updated with all required information.

####System Action Taken During System Boot
Except for the configurations table, the OVSDB is not persisted across reboots, so it comes up initially empty. After the platform daemons have discovered all of the hardware present and populated the OVSDB with the relevant information for the hardware, the configuration daemon (cfgd) looks into configtbl to see if any saved configuration exists. cfgd looks for an entry of type startup. If a startup configuration is found it is applied over the rest of the tables, else cfgd notes that no configuration was found.

####User Actions

The REST and CLI APIs provide rich commands for managing configuration of system. With respect to full declarative configuration support, a user is able to:

- Request that the current running configuration be saved as a startup configuration.
- Request that a startup configuration be written to the running configuration.
- Request a read/show of a startup configuration.
- Request a read/show of a running configuration.

## CLI ##
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here-TBL](https://openswitch.net/cli_feature_name.html#cli_command_anchor) for the CLI commands related to the named feature.
## Related features ##
None.

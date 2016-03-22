# Guidelines for tagging the schema for supporting Kconfig features

## Contents
- [Description](#description)
- [Schema tagging mechanism](#schema-tagging-mechanism)
	- [Feature-tagging the JSON schema](#feature-tagging-json)
		- [Feature-tagging a table](#feature-tagging-json-table)
		- [Feature-tagging a column](#feature-tagging-json-column)
		- [Feature-tagging an enum within a column](#feature-tagging-json-enum)
	- [Feature-tagging the XML schema](#feature-tagging-xml)
		- [Feature-tagging a table](#feature-tagging-xml-table)
		- [Feature-tagging a group](#feature-tagging-xml-group)
		- [Feature-tagging a column within a group](#feature-tagging-xml-column-group)
		- [Feature-tagging a column within a table](#feature-tagging-xml-column-table)

## Description
As part of Kconfig, we will be able to build images with certain features enabled/disabled.
Whenever a feature is not included in a build, we plan to prune the schema of the fields related to that feature.
This document captures the guidelines to do so.

## Schema tagging mechanism
The schema is captured as part of the JSON format file (Ex: vswitch.extschema) and the corresponding XML format file (Ex: vswitch.xml).
These schema-files are located within the ops repository (ops/schema).
We will be feature-tagging the entries in both these file formats.
Correspondingly, we will need to prune entries from both these file formats whenever a feature is not included in an image.
The feature-name used for tagging corresponds to the Kconfig symbol defined for that feature.

The general guidelines are as follows: 
1. Features need to tag an entity (table/column/enum) only if they are using it exclusively.
   If a certain entity is exclusively used by 2 features, then both these features need to tag this entity.
   Only when both these features are not included in the image will this entity be pruned out.

2. If an entity is untagged, it takes the tag of the immediate outer entity.
   For example:
   If all columns within a table are untagged, but the table itself is tagged as feature-A, then all columns are implicitly tagged as feature-A.
   If the table itself is untagged, then it represents a generic table (like "System") which is used by multiple features.
   Such untagged tables will always be included in the schema.

3. The feature-tag at innermost granularity overrides the feature-tag at outer granularities.
   For example: 
   Say feature-A is using Table-A which it has tagged.
   Later feature-B is introduced which wants to add a column to Table-A. This column is exclusively used by feature-B.
   So this new column will be tagged with feature-B.
   What this means is feature-A owns the Table-A except for this new column. And feature-B merely owns this new column in Table-A.
   If feature-A too wants to use this new column, it too must tag this new column.

### Feature-tagging the JSON schema
JSON schema can be feature-tagged at 3 levels: table, column, enum.
The feature-tag at innermost granularity overrides the feature-tag at outer granularities.
Hence the feature-tag of an enum within a column will override the feature-tag of the column which in turn will override the feature-tag of the table.

The feature tag is defined as a list of features:
```ditaa
    "feature_list": ["feature-A", "feature-B", ..., "feature-N"],
```

#### Feature-tagging a table
```ditaa
{
    "name": "OpenSwitch",
    "tables": {
        ...
        "bufmon": {
            "feature_list": ["BUFMON"],
            "columns": {
                ...
            }
        }
    },
    "version": "0.1.8"
}
```

#### Feature-tagging a column
```ditaa
{
    "name": "OpenSwitch",
    "tables": {
        ...
        "System": {
            "columns": {
                ...
                "bufmon_config": {
                    "feature_list": ["BUFMON"],
                    "category": "configuration",
                    ...
                },
                "ntp_status": {
                    "feature_list": ["NTP"],
                    "category": "status",
                    ...
                },
                ...
            }
        },
        ...
    },
    "version": "0.1.8"
}
```
#### Feature-tagging an enum within a column
In this case, instead of a regular string entry inside an enum-set, 
we need to define a dictionary type containing "val" and "feature_list"
```ditaa
{
    "name": "OpenSwitch",
    "tables": {
        ...
        "Subsystem": {
            "columns": {
                ...
                "type": {
                    "category": "status",
                    "type": {
                        "key": {
                            "type": "string",
                            "enum": [
                                "set",
                                [
                                    {
                                         "val": "uninitialized",
                                         "feature_list": ["featureA", "featureB"]
                                    },
                                    "system",
                                    "chassis",
                                    {
                                        "val": "line_card",
                                        "feature_list": ["featureA"]
                                    },
                                    "mezz_card"
                                ]
                            ]
                        },
                        "min": 0,
                        "max": 1
                    }
                },
            }
        },
        ...
    },
    "version": "0.1.8"
}
```

### Feature-tagging the XML schema
XML schema can be feature-tagged at 3 levels: table, group, column.
The feature-tag at innermost granularity overrides the feature-tag at outer granularities.
Hence the feature-tag of a column within a group will override the feature-tag of the group which in turn will override the feature-tag of the table.
If a column within a table is not part of a group, then the feature-tag of the column will override the feature-tag of the table.

The feature tag is defined as a list of features:
```ditaa
    <feature_list>
        <feature>featureA</feature>
        <feature>featureB</feature>
        ...
        <feature>featureN</feature>
    </feature_list>
```

#### Feature-tagging a table
```ditaa
<?xml version="1.0" encoding="utf-8"?>
<database title="OpenSwitch Configuration Database">
    ...
    <table name="bufmon">
        <p>
            Configuration and status of the counters per Capacity Monitoring feature
        </p>
        <feature_list>
            <feature>BUFMON</feature>
        </feature_list>
        ...    
    </table>
    ...
</database>
```

#### Feature-tagging a group
```ditaa
<?xml version="1.0" encoding="utf-8"?>
<database title="OpenSwitch Configuration Database">
    ...
    <table name="System">
        ...
        <group title="Bufmon configuration">
            <feature_list>
                <feature>BUFMON</feature>
            </feature_list>
            <column name="bufmon_config" key="enabled"
                ...
            </column>
            ...
        </group>
        ...
    </table>
    ...
</database>
```

#### Feature-tagging a column within a group
```ditaa
<?xml version="1.0" encoding="utf-8"?>
<database title="OpenSwitch Configuration Database">
    ...
    <table name="System">
        ...
        <group title="NTP configuration">
            <p>
                Specifies the NTP global configuration.
            </p>
            <feature_list>
                <feature>NTP</feature>
            </feature_list>
            <column key="authentication_enable" name="ntp_config" type="{&quot;type&quot;: &quot;boolean&quot;}">
                Determines whether NTP Authentication is enabled in the system.
                Default is false.

                <feature_list>
                    <feature>NTP_CLIENT</feature>
                </feature_list>
            </column>
        </group>
        ...
    </table>
    ...
</database>
```

#### Feature-tagging a column within a table
```ditaa
<?xml version="1.0" encoding="utf-8"?>
<database title="OpenSwitch Configuration Database">
    ...
    <table name="System">
        ...
        <column name="ntp_status" key="uptime">
            Time in hours since the system was last rebooted.
            <feature_list>
                <feature>NTP</feature>
            </feature_list>
        </column>
        ...
    </table>
    ...
</database>
```

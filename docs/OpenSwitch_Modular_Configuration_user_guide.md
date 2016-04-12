# OpenSwitch Modular Configuration - Steps and Guidelines

## Contents
-----------
- [Integrating Feature](#integrating-feature)
	- [Update Kconfig files](#update-kconfig-files)
	- [Update default configuration file](#update-default-configuration-file)
	- [Update recipe files](#update-recipe-files)
	- [Tag schema entries](#tag-schema-entries)
		- [Feature-tagging the JSON schema](#feature-tagging-json)
			- [Feature-tagging a table](#feature-tagging-json-table)
			- [Feature-tagging a column](#feature-tagging-json-column)
			- [Feature-tagging an enum within a column](#feature-tagging-json-enum)
		- [Feature-tagging the XML schema](#feature-tagging-xml)
			- [Feature-tagging a table](#feature-tagging-xml-table)
			- [Feature-tagging a group](#feature-tagging-xml-group)
			- [Feature-tagging a column within a group](#feature-tagging-xml-column-group)
			- [Feature-tagging a column within a table](#feature-tagging-xml-column-table)
	- [Embed decorators in test scripts](#embed-decorators-in-test-scripts)
		- [Test skipping mechanism](#test-skipping-mechanism)
			- [Skipping a script](#skipping-script)
			- [Skipping a class](#skipping-class)
			- [Skipping a test](#skipping-test)

## Integrating Feature
--------------
Following high level steps one should follow to integrate a feature into
OpenSwitch Modular Configuration. Detailed guidelines and steps are provided
in each section:

1. [Update Kconfig files](#update-kconfig-files)
2. [Update default configuration file](#update-default-configuration-file)
3. [Update recipe files](#update-recipe-files)
4. [Tag schema entries](#tag-schema-entries)
5. [Embed decorators in test scripts](#embed-decorators-in-test-scripts)

### Update Kconfig files
-----------------------
Updating Kconfig files will present the option to user via UI. Typically this
involves adding 2 to 4 lines to an existing Kconfig file. Guidelines are:

1. Identify an existing Kconfig file for the feature and use it instead of
   creating a new Kconfig file. A new platform creation always requires adding
   a new platform specific Kconfig file. Check "Kconfig files layout" section
   of OpenSwitch_Modular_Configuration_design.md for details on existing Kconfig
   files.

2. Adding a new feature into Kconfig front-end typically involves adding 2 to 4
   lines into a Kconfig file. Refer to Kconfig language syntax which is simple
   with small set of constructs:
   https://www.kernel.org/doc/Documentation/kbuild/kconfig-language.txt

   Example 1: NTP feature added to $(BUILD_ROOT)/yocto/openswitch/
   meta-distro-openswitch/recipes-ops/mgmt/Kconfig file.

```ditaa
   config NTPD
        bool "Network Time Protocol (NTP) Client"
        default y
        ---help---
          The NTP client feature provides the Network Time Protocol client
          functionality which synchronizes information from NTP servers.
          For more details, please visit:
            http://openswitch.net/documents/dev/ops-ntpd/design
```

   Example 2: Buffmon feature added to $(BUILD_ROOT)/yocto/openswitch/
   meta-distro-openswitch/recipes-ops/utils/Kconfig file.

```ditaa
   config BUFMOND
        bool "Buffer Monitor"
        default y
        ---help---
          Buffers Monitoring is a feature that provides OpenSwitch users the ability
          to monitor buffer space consumption inside the ASIC. It is useful for
          troubleshooting complex performance problems in the data center networking
          environment.
          For more details, please visit:
            http://openswitch.net/documents/dev/ops-bufmond/design
```

   Example 3: Broadview feature added to $(BUILD_ROOT)/tools/kconfig/Kconfig.bcm
   file.

```ditaa
    config BROADVIEW
        bool "Broadview"
        depends on BUFMOND
        default y
        ---help---
          BroadView Instrumentation exposes various instrumentation
          capabilities in Broadcom silicon.
```

3. Kconfig symbol naming should follow below rule if the symbol being added is
   for a feature/sub-feature. This rule does not apply to key-value pairs:
   - If the feature repo name is ops-<repo-name>, then <repo-name> should be
     used as Kconfig symbol.
   - If the sub-feature directory name is <sub-feature> (inside ops-<repo-name>),
     then use <sub-feature> as Kconfig symbol.
   - Both <repo-name> and <sub-feature> can be added as Kconfig symbols with
     proper dependencies. Its up to the feature owner how to group and present
     features/sub-features to the user.

   Example 1: ops-dhcp-tftp will have DHCP-TFTP as Kconfig symbol

   Example 2: ops-quagga having bgpd and ospfd subfeatures. Here either one can
   add QUAGGA, BGPD and OSPFD as a Kconfig symbols and make BGPD and OSPFD as
   dependent on QUAGGA. Or just specify BGPD and OSPFD. First method is
   recommended as it can nicely group and present quagga routing protocol suite
   to user and also user can disable entire quagga routing protocol suite with
   a single selection instead of going and separately disabling BGPD and OSPFD.

4. Although Kconfig language has limited set of constructs, many advanced
   configuration options can be covered by intelligently using them. Refer to
   many examples available online or in Linux kernel source.

### Update default configuration file
-------------------------------------
Default configuration file (.ops-config) is used if user decides to skip
"make menuconfig" and build the image. So default configuration file should be
updated with any changes to Kconfig files. If this step is skipped, then the
feature will be disabled by default.

1. Run "make menuconfig" and set default value for newly added feature. Save
   and exit configuration file. Commit the configuration file present at:
   yocto/openswitch/meta-platform-$(DISTRO)-$(CONFIGURED_PLATFORM)/.ops-config

2. Since configuration file is platform specific, the above step should be
   followed for all platforms. Run "make switch-platform <platform>" followed
   by "make menuconfig".

### Update recipe files
-----------------------
1. If the feature being added has a one to one mapping with the repository and
   recipe being created, then the enable/disable of that feature is controlled
   by including/excluding corresponding yocto package. Yocto internally can
   include/exclude a bunch of dependent packages.

   But often there will be requirement to pass certain buid-time flags to repo
   level makefiles. Some example scenarios (but not limited to):
   - Key-value pair exposed to user.
   - A single repository consisting multiple sub-features.
     Example: ops-quagga containing bgp and ospf
   - Partial dependencies among features. Feature can continue to exist with
     reduced functionality if the other feature is disabled. Such partial
     dependencies cannot be expressed using Kconfig files.
     Example: ops-cli has code specific to many other features that can be
     independently enabled/disabled.
     Example: Broadcom switchd plugin can have code specific to broadview feature.

   IMAGE_FEATURES data store variable of Yocto contains a list of enabled features
   (Kconfig symbols). All recipe files will have access to this variable and hence
   access to enabled feature list. Logical decisions can be taken based on
   presence/absence of a Kconfig symbol in IMAGE_FEATURES.

2. To pass feature flag to repo level makefiles:
   <Yocto Flag> += "${@bb.utils.contains('IMAGE_FEATURES', ‘<Kconfig Symbol>', '-DENABLE_<Kconfig Symbol>=1', '', d)}"
   Where <Yocto Flag> can be EXTRA_OECMAKE, EXTRA_OECONF, EXTRA_OEMAKE depending
   on type of build tool used (Autotools, CMake).

   Example 1: Pass information about whether broadview and bufmon features are
   enabled/disabled to bcm switchd plugin, ops-switchd-opennsl-plugin.bb should
   include:

```ditaa
   # Pass required feature configuration flags to make process.
   # Syntax: -DENABLE_<Kconfig symbol>=1
   EXTRA_OECMAKE += "${@bb.utils.contains('IMAGE_FEATURES','BUFMOND','-DENABLE_BUFMON=1','',d)}"
   EXTRA_OECMAKE += "${@bb.utils.contains('IMAGE_FEATURES','BROADVIEW','-DENABLE_BROADVIEW=1','',d)}"
```

3. Recipe files may require more changes in addition to simply passing flags
   to repo level makefiles. One example is if each of sub-features have their
   own set of resources (daemons, files...). In such cases, all sub-feature
   related content in recipe file should be protected with check to sub-feature
   specific Kconfig symbol in IMAGE_FEATURES.

   Example 1: In do_install_append() task of ops-quagga.bb:

```ditaa
   if ${@bb.utils.contains('IMAGE_FEATURES','BGPD','true','false',d)}; then
   install -m 0644 ${WORKDIR}/ops-bgpd.service ${D}${systemd_unitdir}/system/
   fi

   if ${@bb.utils.contains('IMAGE_FEATURES','OSPFD','true','false',d)}; then
   install -m 0644 ${WORKDIR}/ops-ospfd.service ${D}${systemd_unitdir}/system/
   fi

```

### Tag schema entries
----------------------
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
   If all columns within a table are untagged, but the table itself is tagged as feature-1, then all columns are implicitly tagged as feature-1.
   If the table itself is untagged, then it represents a generic table (like "System") which is used by multiple features.
   Such untagged tables will always be included in the schema.

3. The feature-tag at innermost granularity overrides the feature-tag at outer granularities.
   For example:
   Say feature-1 is exclusively using Table-A which it has tagged.
   Later feature-2 is introduced which wants to add a column to Table-A. This column is exclusively used by feature-2.
   So this new column will be tagged with feature-2.
   What this means is feature-1 owns the Table-A except for this new column. And feature-2 merely owns this new column in Table-A.
   If feature-1 too wants to use this new column, it too must tag this new column.
   If Table-A is tagged with feature-1 as well as feature-2, then all columns within it will be implicitly tagged as feature-1 & feature-2.
   To distinguish, the columns can be explicitly tagged (which will override any previous implicit tagging trickled due to tags at outer layers).
   Note: If a table is untagged and a feature that wants to use it is unsure whether the Table is being used by other features besides it,
         then it should not tag the table exclusively.

#### Feature-tagging the JSON schema
JSON schema can be feature-tagged at 3 levels: table, column, enum.
The feature-tag at innermost granularity overrides the feature-tag at outer granularities.
Hence the feature-tag of an enum within a column will override the feature-tag of the column which in turn will override the feature-tag of the table.

The feature tag is defined as a list of features:
```ditaa
    "feature_list": ["feature-1", "feature-2", ..., "feature-N"],
```

##### Feature-tagging a table
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

##### Feature-tagging a column
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
##### Feature-tagging an enum within a column
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
                                         "feature_list": ["feature-1", "feature-2"]
                                    },
                                    "system",
                                    "chassis",
                                    {
                                        "val": "line_card",
                                        "feature_list": ["feature-1"]
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

#### Feature-tagging the XML schema
XML schema can be feature-tagged at 3 levels: table, group, column.
The feature-tag at innermost granularity overrides the feature-tag at outer granularities.
Hence the feature-tag of a column within a group will override the feature-tag of the group which in turn will override the feature-tag of the table.
If a column within a table is not part of a group, then the feature-tag of the column will override the feature-tag of the table.

The feature tag is defined as a list of features:
```ditaa
    <feature_list>
        <feature>feature-1</feature>
        <feature>feature-2</feature>
        ...
        <feature>feature-N</feature>
    </feature_list>
```

##### Feature-tagging a table
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

##### Feature-tagging a group
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

##### Feature-tagging a column within a group
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

##### Feature-tagging a column within a table
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

### Embed decorators in test scripts
------------------------------------
This is still work-in-progress. Nevertheless capturing details that have been discussed/implemented so far.

The CIT framework deploys "pytest" to run the python test-scripts that are placed within the repos.
As part of Kconfig, when a certain feature is disabled, the tests corresponding to it should not be run (as they will fail).
A file containing the list of features enabled by Kconfig will be generated as part of "make" and will also be available as part of the manifest.
This file and the manifest will act as inputs to the Test framework to create a global set of features (say "enabled_features") that will be available to all test-scripts (either through import of a module or by calling some function).
```ditaa
from opstestfw.kconfig import *
```

A test-script can contain multiple individual tests.
Each test can cater to multiple Kconfig features (especially for feature-tests or test scripts catering to system wide testing).
Hence we need a mechanism to tag each test with the features that it caters to and then to run the test only if all its tagged-features have been enabled.
So similar to the schema, this information will be captured within the test-script, instead of with the framework.

We plan to use the native pytest support of "skipif markers" to skip the script/class/test.

#### Skipping a script
Say a test-script caters to feature-1, feature-2, ... feature-N.
And we plan to skip running all tests in the test-script if either of these features is disabled.
Then this can be achieved as follows:
```ditaa
from opstestfw.kconfig import *

pytestmark = pytest.mark.skipif("'feature-1' and 'feature-2' and ... not in enabled_features", reason="Kconfig feature not enabled")
```

#### Skipping a class
Say a class within a test-script caters to feature-1, feature-2, ... feature-N.
And we plan to skip running all tests within this class if either of these features is disabled.
Then this can be achieved as follows:
```ditaa
from opstestfw.kconfig import *

@pytest.mark.skipif("'feature-1' and 'feature-2' and ... not in enabled_features", reason="Kconfig feature not enabled")
class <classname>:
    ...
```
Another method is to tag the class with features that it caters to and then to call a function to skip this class
(This function will be imported from the "kconfig" module)
```ditaa
from opstestfw.kconfig import *

@kconfig_check_class
@pytest.mark.feature-1
@pytest.mark.feature-2
...
@pytest.mark.feature-N
class <classname>:
    ...
```
However, due to convenience, we prefer and advocate the first method.

#### Skipping a test
Say a class within a test-script has a test that caters to feature-1, feature-2, ... feature-N.
And we plan to skip running this test if either of these features is disabled.
Then this can be achieved as follows:
```ditaa
from opstestfw.kconfig import *

class <classname>:
    ...
    @pytest.mark.skipif("'feature-1' and 'feature-2' and ... not in enabled_features", reason="Kconfig feature not enabled")
    def <testname>(self):
        ...
```
Another method is to tag the function with features that it caters to and then to call a function to skip this class
(This function will be imported from the "kconfig" module)
```ditaa
from opstestfw.kconfig import *

class <classname>:
    ...

    @kconfig_check_func
    @pytest.mark.feature-1
    @pytest.mark.feature-2
    ...
    @pytest.mark.feature-N
    def <testname>(self):
        ...
```
However, due to convenience, we prefer and advocate the first method.

# Custom Validators Framework Design

- [Overview](#overview)
- [High level design](#high-level-design)
	- [Validator](#validator)
	- [Base](#base)
	- [Plugins](#plugins)
	- [Errors](#errors)
	- [BitBake class](#bitbake-class)
- [Custom validator framework](#custom-validator-framework)
	- [Location of custom validators](#location-of-custom-validators)
	- [Installation of custom validators](#installation-of-custom-validators)
	- [Discovery of custom validators](#discovery-of-custom-validators)
	- [Invocation of custom validators](#invocation-of-custom-validators)
	- [Validation errors](#validation-errors)
- [Implementing a custom validator](#implementing-a-custom-validator)
	- [BitBake recipe modifications](#bitbake-recipe-modifications)
	- [Custom validator location](#custom-validator-location)
	- [Derived custom validator class](#derived-custom-validator-class)
		- [Filename](#filename)
		- [Imports and usages](#imports-and-usages)
		- [Class name](#class-name)
		- [Defining the resource name](#defining-the-resource-name)
		- [Overriding validation methods](#overriding-validation-methods)
		- [Using the validation arguments](#using-the-validation-arguments)
- [Examples](#examples)
	- [Example of BitBake recipe modifications](#example-of-bitbake-recipe-modifications)
	- [Example of a custom validator](#example-of-a-custom-validator)
- [References](#references)

## Overview

Custom validators are python modules for performing feature specific validations for resource creating, updating, and deleting. Beyond the generic validations, for example, checking if a resource exists, some features require specific checks, such as whether a resource is already referenced by another resource. Custom validators are used by REST APIs and Declarative Configuration (DC) for validation prior to committing a transaction to the database.

## High level design

The custom validator framework is responsible for the installation, discovery, registration, and invocation of the custom validators. The framework consists of the following components:

From the `opsvalidator` package:

- Validator - Implemented in the `validator.py` module.
- Base - Implemented in the `base.py` module.
- Plugins/custom validators - Implemented in each feature's repository for each table.
- Errors - Implemented in the `error.py` module.

In addition to the `opsvalidator` package, a BitBake class `opsplugins.bbclass` is introduced in the `ops-build` repository for assisting in the custom validators consolidation and installation.

The validator, error, and base modules are implemented as a part of the `opsvalidator` python package. The `opsvalidator` is used by REST and DC to perform validations to prevent invalid configurations from the database. The diagram, below, highlights how the main components are interfaced.

```ditaa
	+--------------+
	|              |
	|              |       +---------------+    +---------------+
	|     REST     |       |               |    |               |
	|              +-------+               |    |  +------------+--+
	|              |       |               |    |  |               |
	+--------------+       |               |    |  |  +------------+--+
	                       |   Validator   +----|  |  |               |
	+--------------+       |               |    |  |  |               |
	|              |       |               |    +--+  |    Plugins    |
	|              +-------+               |       |  |               |
	|      DC      |       |               |       +--+               |
	|              |       |               |          |               |
	|              |       +---------------+          +---------------+
	+--------------+

```

### Validator
The validator discovers, loads, and registers all plugins/custom validators upon `restd` start-up. The validator is the interface for invoking custom validators for REST/DC requests. The plugins are invoked based on the resource/table name the REST/DC request is for. The validator manages all of the custom validators and is responsible for invoking the correct validators. The validator provides the custom validators with the necessary data for validations. The caller of the validator must handle errors returned from the validator.

### Base
The base module is used as the super class of the derived custom validators. The base module declares methods that the validator invokes as hooks to the derived plugins. The base module also serves the role of allowing the validator module to discover all derived classes. Default definitions of the validation methods are defined in the base module.

### Plugins
Plugins/custom validators derive from the base module and are implemented for each resource/table. Custom validators override the inherited methods from the base module in order for the validator module to invoke upon receiving a REST/DC request. Custom validators are used for performing feature-specific validations and raise any errors, to the validator caller, if any validations fail.

### Errors
The error module defines the error codes, error messages, and exceptions that are returned from the custom validators upon validation failure. The error module is the central module for defining additional error codes and messages for use by custom validators. The exception raised includes the error code, message, and any additional details the custom validators include.

### BitBake class
The **BitBake** class `opsplugins.bbclass` defines utility functions for BitBake recipes to inherit from and utilize for the consolidation and installation of the custom validators in the image's **site-packages** directory. The `opsplugins.bbclass` is added in the `ops-build/yocto/openswitch/meta-distro-openswitch/classes` directory.

## Custom validator framework

### Location of custom validators

Custom validators are distributed across repositories. Custom validators are located in a directory named `opsplugins`. During build time, **BitBake** recipes for each repository locate validators using the specific directory name `opsplugins`.

### Installation of custom validators

Custom validators are utilized during run-time. All custom validators are consolidated and packaged as a part of the OpenSwitch image. The added **BitBake** class `opsplugins.bbclass` provides a utility function for BitBake recipes to help consolidate the custom validators in the `opsplugins` package and is installed under the `site-packages` directory. BitBake recipes for each repository copy the validators from `opsplugins` into the image's `site-packages` directory by inheriting from `opsplugins.bbclass` and invoking the `copy_ops_plugins` function.

### Discovery of custom validators

The `opsplugins.bbclass` **BitBake** class creates and installs an `opsplugins` package in the image's `site-packages` directory, which allows the `validator.py` module to be able to discover, load, and register custom validators.

All custom validators derive from the `BaseValidator` class from `opsvalidator/base.py`. Deriving from `BaseValidator` allows the `validator.py` module to discover subclasses of the `BaseValidator` when the custom validator module is loaded. All custom validators will register with a resource name. During initialization of the custom validator framework, all validators are loaded from the `opsplugins` directory in `site-packages`. When the custom validators are discovered and loaded, the validator is mapped to the value of the class variable `resource`. The value of the `resource` is stored as the key in a dictionary for retrieving the custom validator. If more than one custom validators are registered using the same resource name, the custom validators will be added to the list of validators for that `resource`.

For example, a custom validator for the table **BGP Router** will derive from `BaseValidator` with `resoruce` initialized:

```
resource = "bgp_router"
```

When a custom validator is discovered and loaded in `validators.py`, an instance of the plugin is stored and mapped in a dictionary:

```
VALIDATORS[resource] = plugin_instance
```

### Invocation of custom validators

Upon reception of a request to create or modify a resource, the `validator.py` module is used for invoking the associated custom validators based on the resource's table name. The `validator.py` module can be utilized in the following way:

```
from opsvalidator import validator
from opsvalidator.error import ValidationError

try:
    res = validator.exec_validator(idl, schema, resource, request_type, data)
except ValidationError as e:
    # Logic to handle the exception
```

The following arguments are passed to the API:

* `idl`: The Interface Definition Language (IDL) object is the in-memory replica of the database. It is an object from the `ovs.db.idl` python module.
* `schema`: The parsed schema of the database as described in `vswitch.extschema`.
* `resource`: Metadata of the resource, which includes a reference and relationship to related resources.
* `request_type`: Type of the incoming request, which can be `"POST"`, `"PUT"`, or `"DELETE"`.
* `data`: JSON format of the incoming data for the resource.

All custom validators are loaded upon `restd` start-up and are stored by it's associated resource name. The `validator.py` module uses the `resource` name to perform a custom validator dictionary look-up. If a custom validator is not found for the `resource` then a message is logged and the validation is skipped. If the name exists in the dictionary then all custom validators registered under the `resource` name are invoked. If any custom validators fail, when more than one validators are registered to the same resource, the validation will immediately return with an error. If a specific validator should only be executed for specific types of the resource, the custom validator should include a check to enforce skipping or proceeding of the validation.

The `validator.py` module invokes the custom validator's corresponding `validate_create`, `validate_update`, or `validate_delete` method based on the value of the `request_type`, which can be `"POST"`, `"PUT"`, or `"DELETE"`. The `ValidationArgs` object is passed as an argument. The `ValidationArgs` object stores the IDL, schema, resource, and request data for the custom validators to perform validations. If any of the validation methods are not overridden in the custom validators, the activity will be logged and validation will be skipped.

The `validator` module performs the look-up and invocation of custom validators with the following logic:

```
if resource_name in VALIDATORS:
        resource_validators = VALIDATORS[resource_name]
        validation_args = ValidationArgs(idl, schema, resource_name, data)

        for validator in resource_validators:
            res = validator.validate(validation_args)
            ...
```

### Validation errors

The error codes, error messages, and exceptions are defined in the `error.py` module in `opsvalidators`. Custom validators will raise a `ValidationError` upon encountering a validation error. The `ValidationError` exception accepts an error code and any additional plugin-specific details, stores the information in an `error` variable that includes the `code`, `message`, and `details` for the caller of the validator. Clients of the validator will import `ValidationError` from `opsvalidators.error` for catching exceptions raised from the custom validators.

The `ValidationError` exception utilizes the `code` argument to look-up the predefined error message for the error `code`. If a predefined message for the error code is not found, the default error is utilized as a part of the error response to the caller of the validator. Any additional error codes and messages must be added in the `error.py` module. The error codes and messages are common for all validators. New error codes and messages should be defined generically. When raising the `ValidationError` exception, custom validators can provide additional information in the `details` parameter.


## Implementing a custom validator

### BitBake recipe modifications

The **BitBake** recipe for each repository implementing custom validators must be modified to invoke helper functions for copying the custom validators into the image's `site-packages` directory. Recipes must `inherit` from the `opsplugins.bbclass` file for invoking the helper functions then invoke `copy_ops_plugins` from the `do_install_append` function. Modification of the **BitBake** recipe only needs to occur once for the repository.

The following is an example of modifying the recipe file for `ops-quagga`, located at `yocto/openswitch/meta-distro-openswitch/recipes-ops/l3/ops-quagga.bb` under `ops-build` repository:

```
inherit opsplugins

do_install_append() {
    # Any existing logic...

	copy_ops_plugins
}
```

If the `do_install_append` function does not exist in the recipe file then it must be added. If it does exist then the `copy_ops_plugins` should be added at the end of the function.

### Custom validator location

Custom validators must be implemented in the `opsplugins` directory of the repository for each resource. The correct location of the custom validators is important for the validators to be discovered correctly by the custom validator framework.

### Derived custom validator class

#### Filename

The custom validator file should be named using the resource/table name in lowercase. If the resource contains more than one word then the name of the file should be separated by `_`. For example, the custom validator file name for the table `BGP Router` should be named `bgp_router.py` following the `resource_name.py` convention. If a validator is created for a table that already has a custom validator then the type should be appended at the end, such as `resource_name_type.py`. If the selected file name for the custom validator exists, an error will occur during build time and the name must be changed to avoid conflict.

#### Imports and usages

Custom validators will typically import the following:

```
from opsvalidator.base import *
from opsvalidator import error
from opsvalidator.error import ValidationError
from tornado.log import app_log
```

- `opsvalidator.base`: Module that includes the base class used for registration and invocation of derived custom validators.
- `opsvalidator.error`: Module that includes the predefined error codes and messages. Error codes can be accessed, for example: `error.VERIFICATION_FAILED`
- `opsvalidator.error.ValidationError`: The exception to indicate there was an error during validation.

	Exceptions are raised, for example, in the following way:

	```
	code = error.VERIFICATION_FAILED
	details = ['invalid asn', 'invalid type']

	raise ValidationError(code, details)
	```

- `tornado.log.app_log`: Part of the **Tornado** web framework for logging. Custom validators can log information or debug messages with the following APIs:

	```
	app_log.info("")
	app_log.debug("")
	```


#### Class name

The name of the custom validator should be in upper camel-casing. The class name includes the name of the resource, type, and appended by the string "Validator". The type should be included if there are more than one validator for the same table name. For example, the custom validator class name for the table `BGP Router` should be `BgpRouterValidator` following the `ResourceNameValidator` convention. If a validator already exists for the table then the class name should be `ResourceNameTypeValidator`.

#### Defining the resource name

A custom validator is registered to a table/resource name by assigning the name to the `resource` class variable:

```
class BgpRouterValidator(BaseValidator):
    resource = "bgp_router"

    ...
```

The value of the resource should be in the format of `resource_name`. Correct naming of the resource is crucial for correct registering and look-up of the custom validator.

#### Overriding validation methods

The `BaseValidator` class declares the `validate_create`, `validate_update`, and `validate_delete` methods. The `validate_create`, `validate_update`, and `validate_delete` methods should be overridden in the custom validators, as shown below. If the method is not overridden the default behavior is logging the unimplemented method and skipping validation.

```
class BgpRouterValidator(BaseValidator):
    resource = "bgp_router"

    def validate_create(self, validation_args):
        # Validation logic
        return result

    def validate_update(self, validation_args):
        # Validation logic
        return result
```

#### Using the validation arguments

The `validation_args` argument is passed to the custom validator to perform validations. The `validation_args` is an object of the `ValidationArgs` from `opsvalidator.base` that includes the IDL, schema, resource metadata, and request data, and can be accessed via:

```
resource = validation_args.resource
idl = validation_args.idl
schema = validation_args.schema
data = validation_args.data
```

The `resource` argument is an object from the `opsrest.resource` module that contains metadata about the resource, which includes the table name, associated row, column name in the table under which the resource is found, the index of the current row in the table, and any relationship information to other resources.

The `idl` argument is an object from the `ovs.db.idl` module. The IDL includes tables, rows, and columns information. For example, the following code snippet obtains the rows from a table:

```
for row in idl.tables[table_name].rows.itervalues():
```

For more information of the `ovs.db.idl` module, please refer to the comments in the original [source](https://github.com/osrg/openvswitch/blob/master/python/ovs/db/idl.py).

The `schema` argument is a `RESTSchema` object, from the `opslib.restparser` module, as a result of parsing the schema from `vswitch.extschema`. The schema of the tables, configurations, status, statistics, and etc, can be found from the `schema` argument.

For example, the tables from the schema can be obtained from the following code snippet:

```
for table_name, table in schema.ovs_tables.iteritems():
```

The configurations defined for a table can be accessed via:

```
for column_name, column in table.config.iteritems():
```

The `data` argument deserializes the request data that was in JSON to a Python object. If the data contains a dictionary, then the dictionary can be accessed via a key to obtain the associated value. For example, if the request data includes:

```
"configuration": {
    "always_compare_med": true,
    "timers": {
      "holdtime": 0,
      "keepalive": 0
    },
    "asn": 6001
  }
}
```

The `configuration`s can be retrieved by:

```
config_data = data["configuration"]
```

Accessing a specific column data after obtaining the configurations can be achieved by:

```
asn = config_data["asn"]
```

## Examples

### Example of BitBake recipe modifications

```
inherit opsplugins

do_install_append() {
    # Any existing logic...

    # Add invocation of the following function for copying plugins
	copy_ops_plugins
}
```

### Example of a custom validator

```
from opsvalidator.base import *
from opsvalidator import error
from opsvalidator.error import ValidationError
from tornado.log import app_log

class BgpRouterValidator(BaseValidator):
    resource = "bgp_router"

    def validate_create(self, validation_args):
        validation_result = False

        app_log.info("This validation routine will fail")
        if not validation_result:
            code = error.VERIFICATION_FAILED
            details = ['invalid asn', 'invalid type']

            raise ValidationError(code, details)

		# No exception raised indicates successful validation
```

## References

- [Yocto - BitBake](http://www.yoctoproject.org/docs/1.8/bitbake-user-manual/bitbake-user-manual.html#bitbake-user-manual)
- [Open vSwitch - OVS Python APIs](https://github.com/osrg/openvswitch/tree/master/python/ovs)

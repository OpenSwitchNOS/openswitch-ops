add_custom_target(ovsschema ALL)

include("dbschemas.cmake")

# Process the legacy header files
add_subdirectory(legacy)

# Process the OpenSwitch database
add_subdirectory(openswitch)

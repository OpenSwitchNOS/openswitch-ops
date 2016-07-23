add_custom_target(ovsschema ALL)

include("build.cmake")

# Common definitions
set(unified_schema "${CMAKE_CURRENT_BINARY_DIR}/openswitch.extschema.json")

# Generate database schemas from master file
set(master_schema_file ${CMAKE_CURRENT_SOURCE_DIR}/master.extschema.json)
generate_database_schema(${master_schema_file})

# Process the database schemas
add_subdirectory(dbschemas)

# Process the legacy header files
add_subdirectory(legacy)

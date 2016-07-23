# Process extschema files

include("build.cmake")

file(GLOB extschema
	RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
	"${CMAKE_CURRENT_SOURCE_DIR}/*.extschema"
)

foreach(fn ${extschema})
	message(STATUS "Process file: ${fn}")
	generate_ovsschema(${fn})
endforeach(fn)

# Process ovsschema files

file(GLOB ovsschema
	RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
	"${CMAKE_CURRENT_SOURCE_DIR}/*.ovsschema"
)

# If we are building in-source, the .ovsschema file might be a leftover
# from a previous run. Remove generated files from ovsschema list.
foreach(fn ${extschema})
	string(REGEX REPLACE "\\.extschema$" ".ovsschema" fn ${fn})
	list(REMOVE_ITEM ovsschema ${fn})
endforeach(fn)

# Install all the ovsschema files and their documentation if it exists
foreach(fn ${ovsschema})
	message(STATUS "Existing file: ${fn}")
	process_ovsschema(${fn})
endforeach(fn)

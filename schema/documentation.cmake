# Generate the schema documentation in HTML format

# This function will process the unified extended schema file to
# generate the documentation project for a specific database
function(generate_database_documentation)

	set(docs_temp_dir "${CMAKE_CURRENT_BINARY_DIR}/tmp")

	# Get the DB name from the current directory
	string(REGEX MATCH "[^/.]+$" dbname ${CMAKE_CURRENT_SOURCE_DIR})

	message(STATUS "Processing database documentation for: ${dbname}")

	set(unified_schema "${CMAKE_CURRENT_BINARY_DIR}/${dbname}.opsschema")

	file(GLOB json_tables
		RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}/openswitch/common/"
		"${CMAKE_CURRENT_SOURCE_DIR}/openswitch/common/*.json"
	)

	# Prepare docs directory structure
	#file(MAKE_DIRECTORY ${docs_work_dir})
	#file(MAKE_DIRECTORY ${img_dir})
	#file(MAKE_DIRECTORY ${docs_destiny_dir})
	#file(COPY "${docs_source_dir}/conf.py" DESTINATION ${docs_work_dir})
	#file(COPY "${docs_source_dir}/Makefile" DESTINATION ${docs_work_dir})

	file(MAKE_DIRECTORY "${docs_temp_dir}/")
	file(MAKE_DIRECTORY "${docs_temp_dir}/_static")
	file(COPY "${CMAKE_SOURCE_DIR}/schema/lib/conf.py" DESTINATION ${docs_temp_dir})

	# Generate MarkDown files out of the unified schema
	set(rst_file "index.rst")

	#foreach(table ${json_tables})
	#	string(REPLACE ".json" ".md" output ${table})
	#	list(APPEND md_files "${output}")
	#endforeach(table)

	set(documentor "${CMAKE_SOURCE_DIR}/schema/bin/doc_generator")
	add_custom_command(
		OUTPUT ${rst_file}
		COMMAND ${documentor}
			--output-dir ${docs_temp_dir}
			--plantuml-server-url http://www.plantuml.com/plantuml
			${unified_schema}
		DEPENDS ${documentor}
			${unified_schema}
	)

	add_custom_target(diagrams DEPENDS ${rst_file})
	add_dependencies(database-documentation diagrams)

	# Generate HTML documentation
	set(html_dir "${CMAKE_CURRENT_BINARY_DIR}/_build")
	set(index "${html_dir}/html/index.html")
	add_custom_command(
		OUTPUT ${index}
		COMMAND sphinx-build 
			-b html 
			-d ${html_dir}/doctrees .
			${html_dir}/html
		WORKING_DIRECTORY ${docs_temp_dir}
		DEPENDS ${rst_file}
	)

	add_custom_target(generate-${dbname}-documentation
		DEPENDS ${index}
	)
	add_dependencies(database-documentation generate-${dbname}-documentation)

	install(DIRECTORY ${html_dir}/html DESTINATION /srv/www
		PATTERN ".*" EXCLUDE)

endfunction(generate_database_documentation)

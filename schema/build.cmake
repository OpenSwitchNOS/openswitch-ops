# This function will process the master schema file to generate
# the unified schema file, the extended schema file, and the IDL
# constants files for C
function(generate_database_schema MASTER_SCHEMA_FN)
	set(unified_generator "${CMAKE_SOURCE_DIR}/schema/bin/unified_generator")
	set(schemas_generator "${CMAKE_SOURCE_DIR}/schema/bin/schemas_generator")

	set(vswitch_extschema "${CMAKE_CURRENT_BINARY_DIR}/vswitch.extschema")
	set(vswitch_ovsschema "${CMAKE_CURRENT_BINARY_DIR}/vswitch.ovsschema")
	set(vswitch_xml "${CMAKE_CURRENT_BINARY_DIR}/vswitch.xml")
	set(empty_values_header "${CMAKE_CURRENT_BINARY_DIR}/ops-empty-values.h")
	set(metaschema "${CMAKE_CURRENT_SOURCE_DIR}/openswitch.metaschema.json")

	file(GLOB python_scripts
		${CMAKE_CURRENT_SOURCE_DIR}/bin/*.py
	)

	file(GLOB json_schemas
		${CMAKE_CURRENT_SOURCE_DIR}/common/*.json
		${CMAKE_CURRENT_SOURCE_DIR}/docs/*.json
	)

	add_custom_command(
		OUTPUT ${unified_schema}
		COMMAND ${unified_generator}
			${MASTER_SCHEMA_FN}
			${unified_schema}
		MAIN_DEPENDENCY ${MASTER_SCHEMA_FN}
		DEPENDS ${unified_generator} ${json_schemas}
	)

	add_custom_target(db_schema DEPENDS ${unified_schema})
	add_dependencies(ovsschema db_schema)

	add_custom_command(
		OUTPUT ${vswitch_extschema}
			${vswitch_ovsschema}
			${vswitch_xml}
			${empty_values_header}
		COMMAND ${schemas_generator}
			${unified_schema}
			--extschema ${vswitch_extschema}
			--ovsschema ${vswitch_ovsschema}
			--xml ${vswitch_xml}
			--metaschema ${metaschema}
			--empty_values_header ${empty_values_header}
			MAIN_DEPENDENCY ${unified_schema}
			DEPENDS ${schemas_generator} ${python_scripts} ${metaschema}
	)

	add_custom_target(extschema
		DEPENDS ${vswitch_extschema}
			${vswitch_ovsschema}
			${vswitch_xml}
			${empty_values_header}
	)
	add_dependencies(ovsschema extschema)

	install(FILES ${empty_values_header} DESTINATION include)
	install(FILES ${unified_schema} DESTINATION share/openvswitch)
	install(FILES ${vswitch_extschema} DESTINATION share/openvswitch)
	install(FILES ${vswitch_ovsschema} DESTINATION share/openvswitch)
	install(FILES ${vswitch_xml} DESTINATION share/openvswitch)

endfunction(generate_database_schema)

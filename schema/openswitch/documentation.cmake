# Generate the schema documentation in HTML format

add_custom_target(html ALL)

set(docs_temp_dir "${CMAKE_CURRENT_BINARY_DIR}/tmp")


file(GLOB json_tables
	RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}/common/"
	"${CMAKE_CURRENT_SOURCE_DIR}/common/*.json"
)


# Prepare docs directory structure
#file(MAKE_DIRECTORY ${docs_work_dir})
#file(MAKE_DIRECTORY ${img_dir})
#file(MAKE_DIRECTORY ${docs_destiny_dir})
#file(COPY "${docs_source_dir}/conf.py" DESTINATION ${docs_work_dir})
#file(COPY "${docs_source_dir}/Makefile" DESTINATION ${docs_work_dir})


file(MAKE_DIRECTORY "${docs_temp_dir}/")
file(MAKE_DIRECTORY "${docs_temp_dir}/_static")
file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/../lib/conf.py" DESTINATION ${docs_temp_dir})


# Generate MarkDown files out of the unified schema
set(rst_file "index.rst")
#foreach(table ${json_tables})
#	string(REPLACE ".json" ".md" output ${table})
#	list(APPEND md_files "${output}")
#endforeach(table)

set(documentor "${CMAKE_CURRENT_SOURCE_DIR}/../bin/doc_generator")
add_custom_command(
	OUTPUT ${rst_file}
	COMMAND ${documentor}
		--output-dir ${docs_temp_dir}
		--plantuml-server http://www.plantuml.com/plantuml/img/
		${unified_schema}
	DEPENDS ${documentor}
		${unified_schema}
)

add_custom_target(diagrams DEPENDS ${rst_file})
add_dependencies(html diagrams)


# Generate HTML documentation
set(html_dir "${docs_temp_dir}/_build")
set(index "${html_dir}/html/index.html")
string(REPLACE "/" "__" index_target ${index})
add_custom_command(
	OUTPUT ${index}
	COMMAND sphinx-build 
		-b html 
		-d ${html_dir}/doctrees .
		${html_dir}/html
	WORKING_DIRECTORY ${docs_temp_dir}
	DEPENDS ${rst_file}
)
add_custom_target(index_html DEPENDS ${index})
add_dependencies(html index_html)

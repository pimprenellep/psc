cmake_minimum_required(VERSION 3.10)

foreach(TEST basic highlevel main)
	add_test(NAME ${TEST}
		WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
		COMMAND ${PYTHON_EXECUTABLE} ${TEST}.py)
	set_tests_properties(${TEST} PROPERTIES ENVIRONMENT LD_LIBRARY_PATH=${CMAKE_CURRENT_SOURCE_DIR})
endforeach()

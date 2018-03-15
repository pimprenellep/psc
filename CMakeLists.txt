cmake_minimum_required(VERSION 3.10)
project(psesca)

add_subdirectory(psesca_ext)
add_subdirectory(tests)

install(DIRECTORY psesca/ DESTINATION psesca
	PATTERN "*.py" EXCLUDE
	PATTERN "__pycache__*" EXCLUDE
	)

set(CPACK_PACKAGE_FILE_NAME ${CMAKE_PROJECT_NAME})
include(CPack)

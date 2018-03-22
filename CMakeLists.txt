cmake_minimum_required(VERSION 3.10)
project(psesca)

# Tools
set(Python_ADDITIONAL_VERSIONS 3.6 3.5 3.4 3.3 3.2 3.1 3.0)
find_package(PythonInterp)

enable_testing()

add_subdirectory(psesca_ext)
add_subdirectory(tests)
add_subdirectory(doc)

set(CPACK_PACKAGE_FILE_NAME ${CMAKE_PROJECT_NAME})
include(CPack)

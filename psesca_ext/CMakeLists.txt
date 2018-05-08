cmake_minimum_required(VERSION 3.10)

# System libs
find_package(OpenGL REQUIRED OpenGL OPTIONAL_COMPONENTS EGL)
if(OpenGL_EGL_FOUND)
	set(GL_PLATFORM EGL)
	add_definitions(-DWITH_EGL)
	set(GL_LIBS OpenGL::OpenGL OpenGL::EGL)
	find_path(GLEXT_Includes GL/glext.h)
	include_directories(${GLEXT_Includes})
else()
	set(GL_PLATFORM WGL)
	add_definitions(-DWITH_WGL)
	set(GL_LIBS OpenGL::GL)
endif()


find_path(ODE_Includes ode/ode.h)
include_directories(${ODE_Includes})
add_definitions(-DdSINGLE)
find_library(ODE_Lib NAMES ode ode_single)

find_path(GLM_Includes glm/glm.hpp)
include_directories(${GLM_Includes})

# Sources
set(NATIVE_SOURCES
	native/glcontext.cpp
	native/simulator.cpp
	native/climbermodel.cpp
	native/morphology.cpp
	native/controller.cpp
	native/shape.cpp
	native/wha_shape.cpp
	native/route.cpp
	native/stancegraph.cpp
	native/renderer.cpp
	native/shaders.cpp
	native/cmaes.c
	)
if(${GL_PLATFORM} STREQUAL WGL)
	set(NATIVE_SOURCES ${NATIVE_SOURCES} native/glew.c)
	add_definitions(-DGLEW_BUILD)
endif()

set(MOD_SOURCES
	psesca/morphology.pyx
	psesca/climbermodel.pyx
	psesca/controller.pyx
	psesca/shape.pyx
	psesca/wha_shape.pyx
	psesca/route.pyx
	psesca/stancegraph.pyx
	)

set(MOD_HEADERS
	psesca/morphology.pxd
	psesca/climbermodel.pxd
	psesca/controller.pxd
	psesca/shape.pxd
	psesca/wha_shape.pxd
	psesca/route.pxd
	psesca/stancegraph.pxd
	)

# Configuration files
set(MOD_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR})
get_directory_property(MOD_INCLUDES INCLUDE_DIRECTORIES)
get_directory_property(MOD_DEFINES COMPILE_DEFINITIONS)
configure_file(setup.py.in setup.py)

foreach(shader vertex fragment)
	string(TOUPPER ${shader} SHADER)
	execute_process(
		COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/scripts/lit.py
			${CMAKE_CURRENT_SOURCE_DIR}/native/${shader}.glsl
		OUTPUT_VARIABLE ${SHADER}_SHADER_SOURCE
		)
endforeach()
configure_file(native/shaders_data.hpp.in native/shaders_data.hpp)
include_directories(${CMAKE_CURRENT_BINARY_DIR}/native)

# Programs
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
add_library(native SHARED ${NATIVE_SOURCES})
target_link_libraries(native ${GL_LIBS} ${ODE_Lib})

set($ENV{MSSdk} 1)
set($ENV{DISTUTILS_USE_SDK} 1)
add_custom_command(
	OUTPUT extensions.ts
	COMMAND ${PYTHON_EXECUTABLE} setup.py install -f --root=${CMAKE_BINARY_DIR}  --install-lib=.
	COMMAND ${CMAKE_COMMAND} -E copy_directory "${CMAKE_BINARY_DIR}/psesca"
	"${CMAKE_BINARY_DIR}/tests/psesca_ext"
	COMMAND ${CMAKE_COMMAND} -E touch extensions.ts
	DEPENDS ${MOD_SOURCES} ${MOD_HEADERS} setup.py.in native
	)

# Targets
add_custom_target(extensions ALL DEPENDS extensions.ts)

# Install
install(TARGETS native DESTINATION lib)
install(DIRECTORY "${CMAKE_BINARY_DIR}/tests/psesca_ext" DESTINATION .)


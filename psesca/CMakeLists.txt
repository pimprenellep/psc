cmake_minimum_required(VERSION 3.10)

# Tools
find_program(PYTHON3 python3)

# System libs
find_package(OpenGL REQUIRED OpenGL EGL)

# Sources
set(NATIVE_SOURCES 
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
	    )

set(MOD_SOURCES
	native.pyx
	morphology.pyx
	climbermodel.pyx
	controller.pyx
	shape.pyx
	wha_shape.pyx
	route.pyx
	stancegraph.pyx
	)

# Configuration files
configure_file(setup.py.in setup.py)

foreach(shader vertex fragment)
	string(TOUPPER ${shader} SHADER)
	execute_process(
		COMMAND ${PYTHON3} ${CMAKE_CURRENT_SOURCE_DIR}/scripts/lit.py
			${CMAKE_CURRENT_SOURCE_DIR}/native/${shader}.glsl
		OUTPUT_VARIABLE ${SHADER}_SHADER_SOURCE
		)
endforeach()
configure_file(native/shaders.cpp.in native/shaders.cpp)

# Programs
add_library(native SHARED ${NATIVE_SOURCES})
target_link_libraries(native OpenGL::OpenGL OpenGL::EGL ode)

add_custom_command(
	OUTPUT native.ts
	COMMAND ${PYTHON3} setup.py build_ext
	COMMAND ${PYTHON3} setup.py install -f --install-lib=.
	COMMAND ${CMAKE_COMMAND} -E touch native.ts
	DEPENDS ${MOD_SOURCES} setup.py native
	)

# Targets
add_custom_target(main ALL DEPENDS native.ts)

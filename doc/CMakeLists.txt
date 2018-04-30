find_program(DOXYGEN doxygen)

if(NOT "${DOXYGEN}" STREQUAL DOXYGEN-NOTFOUND)
	configure_file(Doxyfile.in Doxyfile)
	add_custom_target(
		doc
		COMMAND "${DOXYGEN}" Doxyfile
		)
else()
	message("Doxygen no found, not creating documentation target.")
endif()

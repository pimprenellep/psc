all : uml.svg

uml.svg : uml.dia
	dia -e $@ $<

doxygen:
	doxygen Doxyfile

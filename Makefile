all : 
	$(MAKE) -C psesca $@
	$(MAKE) -C doc $@
	$(MAKE) -C tests $@

test :
	$(MAKE) -C tests $@



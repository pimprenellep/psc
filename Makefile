all : 
	$(MAKE) -C doc $@
	$(MAKE) -C tests $@

test :
	$(MAKE) -C tests $@



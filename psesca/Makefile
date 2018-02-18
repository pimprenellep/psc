all : nativelib native.so

native.so : native.o native/native.a
	g++ -shared -pthread -lode -o $@ $^
	
nativelib :
	$(MAKE) -C native
	
%.o : %.cpp
	g++ -c -fPIC -fwrapv ${CXXFLAGS} -fno-strict-aliasing -I/usr/include/python3.5 -o $@ $<

%.cpp : %.pyx
	cython --cplus $<

native.pyx : morphology.pyx climbermodel.pyx controller.pyx
	cat $^ > $@


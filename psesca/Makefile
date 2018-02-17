all : native.so

native.so : native.o native.a
	g++ -shared -pthread -o $@ $< native/morphology.o native/climbermodel.o

native.a :
	$(MAKE) -C native
	cp -u native/native.a native.a
	
%.o : %.cpp
	g++ -c -fPIC -fwrapv ${CXXFLAGS} -fno-strict-aliasing -I/usr/include/python3.5 -o $@ $<

%.cpp : %.pyx
	cython --cplus $<

native.pyx : morphology.pyx climbermodel.pyx controller.pyx
	cat $^ > $@


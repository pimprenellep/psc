SUBDIRS = native

all : native.so

native.so : native.o native/libnative.a
	g++ -shared -pthread -lode -o $@ $^
	
%.o : %.cpp
	g++ -c -fPIC -fwrapv ${CXXFLAGS} -fno-strict-aliasing -I/usr/include/python3.5 -o $@ $<

%.cpp : %.pyx
	cython --cplus $<

native.pyx : morphology.pyx climbermodel.pyx controller.pyx
	cat $^ > $@


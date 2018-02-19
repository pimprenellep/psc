SUBDIRS = native

lib_LTLIBRARIES=libwrappers.la
libwrappers_la_LDFLAGS=-pthread -lode
libwrappers_la_LIBADD= native/libnative.a
libwrappers_la_CXXFLAGS=-fPIC -fwrapv -fno-strict-aliasing -I/usr/include/python3.5
libwrappers_la_SOURCES = native.cpp

all-local :
	cp -uL .libs/libwrappers.so native.so

#ative.so : native.o native/libnative.a
#	g++ -shared -pthread -lode -o $@ $^
	
#%.o : %.cpp
#	g++ -c -fPIC -fwrapv ${CXXFLAGS} -fno-strict-aliasing -I/usr/include/python3.5 -o $@ $<

%.cpp : %.pyx
	cython --cplus $<

native.pyx : morphology.pyx climbermodel.pyx controller.pyx
	cat $^ > $@


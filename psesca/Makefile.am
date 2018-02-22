SUBDIRS = native

lib_LTLIBRARIES=native.la
native_la_LDFLAGS=-pthread -lode -lEGL -module -avoid-version -shared
native_la_LIBADD= native/libnative.a
native_la_CXXFLAGS=-fPIC -fwrapv -fno-strict-aliasing -I/usr/include/python3.5
native_la_SOURCES = native.cpp

all-local :
	cp -uL .libs/native.so native.so

#ative.so : native.o native/libnative.a
#	g++ -shared -pthread -lode -o $@ $^
	
#%.o : %.cpp
#	g++ -c -fPIC -fwrapv ${CXXFLAGS} -fno-strict-aliasing -I/usr/include/python3.5 -o $@ $<

%.cpp : %.pyx
	cython --cplus $<

native.pyx : morphology.pyx climbermodel.pyx controller.pyx shape.pyx wha_shape.pyx route.pyx stancegraph.pyx
	cat $^ > $@


SUBDIRS = native

lib_LTLIBRARIES=native.la
native_la_LDFLAGS=-pthread ${ODE_LIBS} ${EGL_LIBS} -module -avoid-version -shared
native_la_LIBADD= native/libnative.a
native_la_CXXFLAGS=-fPIC -fwrapv -fno-strict-aliasing ${PY3_CFLAGS}
native_la_SOURCES = native.cpp

all-local :
	cp -uL .libs/native.so native.so

%.cpp : %.pyx
	cython --cplus $<

native.pyx : morphology.pyx climbermodel.pyx controller.pyx shape.pyx wha_shape.pyx route.pyx stancegraph.pyx
	cat $^ > $@


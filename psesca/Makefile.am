SUBDIRS = native

lib_LTLIBRARIES=native.la
native_la_LDFLAGS=-pthread ${ODE_LIBS} ${OpenGL_LIBS} ${EGL_LIBS} -module -avoid-version -shared
native_la_CXXFLAGS=-fPIC -fwrapv -fno-strict-aliasing ${PY3_CFLAGS} ${ODE_CFLAGS} ${EGL_CFLAGS} ${OpenGL_CFLAGS}
native_la_SOURCES = native.cpp \
	native/simulator.cpp	\
	native/climbermodel.cpp	\
	native/morphology.cpp	\
	native/controller.cpp	\
	native/shape.cpp	\
	native/wha_shape.cpp	\
	native/route.cpp	\
	native/stancegraph.cpp	\
	native/renderer.cpp	\
	native/shaders.cpp	\
	native/vertex.s		\
	native/fragment.s

all-local : native.${pymod_ext}

native.${pymod_ext} : native.la
	cp -uL .libs/native.${so_ext} $@

%.s : %.glsl
	touch $@

%.cpp : %.pyx
	cython --cplus $<

native.pyx : morphology.pyx climbermodel.pyx controller.pyx shape.pyx wha_shape.pyx route.pyx stancegraph.pyx
	cat $^ > $@


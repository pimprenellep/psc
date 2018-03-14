#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_INIT([psesca], [0.1], [BUG-REPORT-ADDRESS])
AC_CONFIG_MACRO_DIRS([m4])
AM_INIT_AUTOMAKE([subdir-objects])
LT_INIT
AC_CONFIG_SRCDIR([psesca/native/controller.cpp])
AC_CONFIG_HEADERS([config.h])
AC_CANONICAL_HOST

case "${host_os}" in
    linux*)
	AC_SUBST([pymod_ext], [so])
	AC_SUBST([so_ext], [so])
        ;;
    cygwin*|mingw*)
	AC_SUBST([pymod_ext], [pyd])
	AC_SUBST([so_ext], [dll])
        ;;
    *)
        AC_MSG_ERROR(["OS $host_os is not supported"])
        ;;
esac


# Checks for programs.
AC_PROG_CXX
AM_PROG_AS

# Checks for libraries.

# Checks for header files.

# Checks for typedefs, structures, and compiler characteristics.
AC_CHECK_HEADER_STDBOOL

# Checks for library functions.

AC_ARG_VAR(ODE_LIBS)
AC_ARG_VAR(OpenGL_LIBS)
AC_ARG_VAR(EGL_LIBS)
AC_ARG_VAR(PY3_CFLAGS)
AC_ARG_VAR(ODE_CFLAGS)
AC_ARG_VAR(EGL_CFLAGS)
AC_ARG_VAR(OpenGL_CFLAGS)

if test "x${ODE_LIBS}" = x ; then
	ODE_LIBS="-lode"
fi
if test "x${OpenGL_LIBS}" = x ; then
	OpenGL_LIBS="-lGL"
fi
if test "x${EGL_LIBS}" = x ; then
	EGL_LIBS="-lEGL"
fi
if test "x${PY3_CFLAGS}" = x ; then
	PY3_CFLAGS="-I/usr/include/python3.5"
fi

AC_CONFIG_FILES([Makefile
                 doc/Makefile
                 psesca/Makefile
                 psesca/native/Makefile
                 tests/Makefile])
AC_OUTPUT

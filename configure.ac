#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_INIT([psesca], [0.1], [BUG-REPORT-ADDRESS])
AM_INIT_AUTOMAKE([subdir-objects])
LT_INIT
AC_CONFIG_SRCDIR([psesca/native/controller.cpp])
AC_CONFIG_HEADERS([config.h])

# Checks for programs.
AC_PROG_CXX
AC_PROG_RANLIB

# Checks for libraries.
PKG_CHECK_MODULES([PY3], [python3])
PKG_CHECK_MODULES([ODE], [ode])
PKG_CHECK_MODULES([EGL], [egl])
PKG_CHECK_MODULES([OpenGL], [gl])

# Checks for header files.

# Checks for typedefs, structures, and compiler characteristics.
AC_CHECK_HEADER_STDBOOL

# Checks for library functions.

AC_CONFIG_FILES([Makefile
                 doc/Makefile
                 psesca/Makefile
                 psesca/native/Makefile
                 tests/Makefile])
AC_OUTPUT

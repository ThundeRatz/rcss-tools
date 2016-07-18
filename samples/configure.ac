AC_INIT([rcss-tools-samples], [0.1], [tiago.shibata@thunderatz.org])
# For debugging:
# -fstack-protector-all -Wstack-protector --param ssp-buffer-size=4 -­D_FORTIFY_SOURCE=2 -O2 -g
: ${CXXFLAGS="-Werror -O2 -flto"}
AM_INIT_AUTOMAKE([-Wall -Werror foreign subdir-objects])
AC_PROG_CC(gcc)
AC_PROG_CXX(g++)
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_FILES([
    Makefile
])

AC_OUTPUT

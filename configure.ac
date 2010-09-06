AC_INIT(cortexcpu, 0.1)
AM_INIT_AUTOMAKE(foreign subdir-objects color-tests)
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_FILES(Makefile)
AC_PROG_LIBTOOL
AM_PROG_AS

AC_ARG_WITH([cpu],
	    AS_HELP_STRING([--with-cpu=CPU],
                           [select code for CPU variant @<:@default=cortex-a8@:>@]]),
	    [dnl
  case "$withval" in
  yes|'') AC_MSG_ERROR([--with-cpu requires an argument]) ;;
  no) ;;
  *) submachine="$withval" ;;
  esac
],
[submachine=cortex-a8])

AC_SUBST(submachine)

AC_ARG_WITH([neon],
            AC_HELP_STRING([--with-neon],
                           [include NEON specific routines @<:@default=yes@:>@]),
	    [with_neon=$withval],
	    [with_neon=yes])
AC_SUBST(with_neon)

AC_OUTPUT

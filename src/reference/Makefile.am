lib_LTLIBRARIES = \
	libhelpers.la \
	libplain.la \
	libbionic.la \
	libnewlib.la \
	libglibc.la

#libbionic.la #libglibc.a libnewlib.a

libbionic_la_SOURCES = \
	bionic/memcpy.S \
	bionic/strlen.c

libglibc_la_SOURCES = \
	glibc/memcpy.S \
	glibc/strlen.S

libnewlib_la_SOURCES = \
	newlib/strcmp.c \
	newlib/strcpy.c \
	newlib/strlen.c

AM_CFLAGS = -std=gnu99

libhelpers_la_SOURCES = helpers/bounce.c helpers/spawn.c
libplain_la_SOURCES = plain/memcpy.c

lib_LTLIBRARIES = \
	libhelpers.la \
	libplain.la \
	libbionic.la \
	libnewlib.la \
	libglibc.la

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

libhelpers_la_SOURCES = \
	helpers/bounce.c \
	helpers/spawn.c

libplain_la_SOURCES = \
	plain/memcpy.c \
	plain/strcpy.c \
	plain/strcmp.c

AM_CFLAGS = -std=gnu99


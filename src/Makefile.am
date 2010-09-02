lib_LTLIBRARIES = \
	libcortexcpu.la

sources = \
	neon/memcpy.S \
	neon/memset.S \
	thumb-2/strcmp.c \
	thumb-2/strcpy.c \
	thumb-2/strlen.c

libcortexcpu_la_SOURCES = $(sources)

AM_CFLAGS = -std=gnu99


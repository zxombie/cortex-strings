COMPILER = $(shell $(CC) --version 2>&1 | head -n1)

lib_LTLIBRARIES = \
	libcortexcpu.la

sources = \
	src/neon/memcpy.S \
	src/neon/memset.S \
	src/thumb-2/strcmp.c \
	src/thumb-2/strcpy.c \
	src/thumb-2/strlen.c

noinst_LIBRARIES = \
	libbionic.a \
	libcsl.a \
	libglibc.a \
	libnewlib.a \
	libplain.a \
	libmulti.a

libbionic_a_SOURCES = \
	reference/bionic/memcmp.S \
	reference/bionic/memcmp16.S \
	reference/bionic/strlen.c \
	reference/bionic/memset.S \
	reference/bionic/memcpy.S

libcsl_a_SOURCES = \
	reference/csl/memcpy.c \
	reference/csl/memset.c

libglibc_a_SOURCES = \
	reference/glibc/memmove.S \
	reference/glibc/memset.S \
	reference/glibc/strlen.S \
	reference/glibc/memcpy.S

libnewlib_a_SOURCES = \
	reference/newlib/strcmp.c \
	reference/newlib/strlen.c \
	reference/newlib/strcpy.c

libplain_a_SOURCES = \
	reference/plain/memset.c \
	reference/plain/memcpy.c \
	reference/plain/strcmp.c \
	reference/plain/strcpy.c

libmulti_a_SOURCES = \
	benchmarks/multi/harness.c

noinst_PROGRAMS = \
	dhry \
	try-bionic \
	try-csl \
	try-glibc \
	try-newlib \
	try-plain

dhry_SOURCES = \
	benchmarks/dhry/dhry_1.c \
	benchmarks/dhry/dhry_2.c

try_bionic_SOURCES =
try_bionic_LDFLAGS = -lrt
try_bionic_LDADD = libmulti.a libbionic.a
try_csl_SOURCES =
try_csl_LDFLAGS = -lrt
try_csl_LDADD = libmulti.a libcsl.a
try_glibc_SOURCES =
try_glibc_LDFLAGS = -lrt
try_glibc_LDADD = libmulti.a libglibc.a
try_newlib_SOURCES =
try_newlib_LDFLAGS = -lrt
try_newlib_LDADD = libmulti.a libnewlib.a
try_plain_SOURCES =
try_plain_LDFLAGS = -lrt
try_plain_LDADD = libmulti.a libplain.a

dhry_CFLAGS = -Dcompiler="\"$(COMPILER)\"" -Doptions="\"$(CFLAGS)\""

libcortexcpu_la_SOURCES = $(sources)

check_PROGRAMS = \
	tests/test-memcpy \
	tests/test-memset \
	tests/test-strcmp \
	tests/test-strcpy \
	tests/test-strlen

tests_test_memcpy_LDADD = libcortexcpu.la
tests_test_memcpy_CFLAGS = -Itests $(AM_CFLAGS)
tests_test_memset_LDADD = libcortexcpu.la
tests_test_memset_CFLAGS = -Itests $(AM_CFLAGS)
tests_test_strcmp_LDADD = libcortexcpu.la
tests_test_strcmp_CFLAGS = -Itests $(AM_CFLAGS)
tests_test_strcpy_LDADD = libcortexcpu.la
tests_test_strcpy_CFLAGS = -Itests $(AM_CFLAGS)
tests_test_strlen_LDADD = libcortexcpu.la
tests_test_strlen_CFLAGS = -Itests $(AM_CFLAGS)

TESTS = $(check_PROGRAMS)

AM_CFLAGS = -std=gnu99 -mfpu=neon
AM_CPPFLAGS = -mfpu=neon


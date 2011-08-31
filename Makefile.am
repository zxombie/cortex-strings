# Top level Makefile for cortex-strings

# Used to record the compiler version in the executables
COMPILER = $(shell $(CC) --version 2>&1 | head -n1)

if WITH_NEON
# Pull in the NEON specific files
neon_sources = \
	src/neon/memcpy.S
neon_bionic_sources = \
	reference/bionic/memcpy.S
neon_cppflags = -mfpu=neon
neon_dirs = neon
endif

# The main library
lib_LTLIBRARIES = \
	libcortex-strings.la

# Test suite
check_PROGRAMS = \
	tests/test-memchr \
	tests/test-memcpy \
	tests/test-memset \
	tests/test-strchr \
	tests/test-strcmp \
	tests/test-strcpy \
	tests/test-strlen

# Benchmarks and example programs
noinst_PROGRAMS = \
	dhry \
	dhry-native \
	try-none \
	try-this \
	try-bionic \
	try-csl \
	try-glibc \
	try-newlib \
	try-newlib-xscale \
	try-plain

# Libraries used in the benchmarks and examples
noinst_LIBRARIES = \
	libbionic.a \
	libcsl.a \
	libglibc.a \
	libnewlib.a \
	libnewlib-xscale.a \
	libplain.a \
	libmulti.a

# Main library
libcortex_strings_la_SOURCES = \
	$(neon_sources) \
	src/thumb-2/strcmp.c \
	src/thumb-2/strcpy.c \
	src/linaro-a9/memchr.s \
	src/linaro-a9/strchr.s \
	src/linaro-a9/strlen.s \
	src/linaro-a9/memset.S

# Options for the tests
tests_cflags = -I$(srcdir)/tests $(AM_CFLAGS)
tests_ldadd = libcortex-strings.la
tests_test_memcpy_LDADD = $(tests_ldadd)
tests_test_memcpy_CFLAGS = $(tests_cflags)
tests_test_memset_LDADD = $(tests_ldadd)
tests_test_memset_CFLAGS = $(tests_cflags)
tests_test_strcmp_LDADD = $(tests_ldadd)
tests_test_strcmp_CFLAGS = $(tests_cflags)
tests_test_strcpy_LDADD = $(tests_ldadd)
tests_test_strcpy_CFLAGS = $(tests_cflags)
tests_test_strlen_LDADD = $(tests_ldadd)
tests_test_strlen_CFLAGS = $(tests_cflags)

TESTS = $(check_PROGRAMS)

# Libraries containing the difference reference versions
libbionic_a_SOURCES = \
	$(neon_bionic_sources) \
	reference/bionic/memchr.c \
	reference/bionic/memset.S \
	reference/bionic/strchr.c \
	reference/bionic/strcmp.c \
	reference/bionic/strcpy.c \
	reference/bionic/strlen.c

libbionic_a_CFLAGS = -Wa,-mimplicit-it=thumb

libcsl_a_SOURCES = \
	reference/csl/memcpy.c \
	reference/csl/memset.c \
	reference/csl/arm_asm.h

libglibc_a_SOURCES = \
	reference/glibc/memchr.c \
	reference/glibc/memcpy.S \
	reference/glibc/memset.S \
	reference/glibc/strchr.c \
	reference/glibc/strcmp.c \
	reference/glibc/strcpy.c \
	reference/glibc/strlen.S

libnewlib_a_SOURCES = \
	reference/newlib/memchr.c \
	reference/newlib/memcpy.c \
	reference/newlib/memset.c \
	reference/newlib/strchr.c \
	reference/newlib/strcmp.c \
	reference/newlib/strcpy.c \
	reference/newlib/strlen.c \
	reference/newlib/arm_asm.h

libnewlib_xscale_a_SOURCES = \
	reference/newlib-xscale/memchr.c \
	reference/newlib-xscale/memcpy.c \
	reference/newlib-xscale/memset.c \
	reference/newlib-xscale/strchr.c \
	reference/newlib-xscale/strcmp.c \
	reference/newlib-xscale/strcpy.c \
	reference/newlib-xscale/strlen.c

libplain_a_SOURCES = \
	reference/plain/memset.c \
	reference/plain/memcpy.c \
	reference/plain/strcmp.c \
	reference/plain/strcpy.c

libmulti_a_SOURCES = \
	benchmarks/multi/harness.c

libmulti_a_CFLAGS = -DVERSION=\"$(VERSION)\" $(AM_CFLAGS)

# Flags for the benchmark helpers
try_none_SOURCES =
try_none_LDADD = libmulti.a -lrt
try_this_SOURCES =
try_this_LDADD = libmulti.a libcortex-strings.la -lrt
try_bionic_SOURCES =
try_bionic_LDADD = libmulti.a libbionic.a -lrt
try_csl_SOURCES =
try_csl_LDADD = libmulti.a libcsl.a -lrt
try_glibc_SOURCES =
try_glibc_LDADD = libmulti.a libglibc.a -lrt
try_newlib_SOURCES =
try_newlib_LDADD = libmulti.a libnewlib.a -lrt
try_newlib_xscale_SOURCES =
try_newlib_xscale_LDADD = libmulti.a libnewlib-xscale.a -lrt
try_plain_SOURCES =
try_plain_LDADD = libmulti.a libplain.a -lrt

# Good 'ol Dhrystone
dhry_SOURCES = \
	benchmarks/dhry/dhry_1.c \
	benchmarks/dhry/dhry_2.c \
	benchmarks/dhry/dhry.h

dhry_CFLAGS = -Dcompiler="\"$(COMPILER)\"" -Doptions="\"$(CFLAGS)\""
dhry_LDADD = libcortex-strings.la

dhry_native_SOURCES = $(dhry_SOURCES)
dhry_native_CFLAGS = $(dhry_CFLAGS)

AM_CPPFLAGS = $(neon_cppflags)
AM_CFLAGS = -std=gnu99 -Wall -mtune=$(submachine) $(AM_CPPFLAGS)

EXTRA_DIST = \
	tests/hp-timing.h \
	tests/test-string.h \
	tests/test-skeleton.c \
	autogen.sh

add_on_dist = add-on-dist
add_on_dest = $(add_on_dist)/$(PACKAGE)/sysdeps/arm/eabi/arm/$(submachine)
add_on_dirs = thumb-2 $(submachine) $(neon_dirs)

add_on_src = \
	$(wildcard $(add_on_dirs:%=$(srcdir)/src/%/*.c)) \
	$(wildcard $(add_on_dirs:%=$(srcdir)/src/%/*.S)) \
	$(wildcard $(add_on_dirs:%=$(srcdir)/src/%/*.h))

add-on:
	rm -rf $(add_on_dist)
	mkdir -p $(add_on_dest)
	cp -f $(add_on_src) $(add_on_dest)
	python $(srcdir)/scripts/fixup.py GLIBC $(add_on_dest)/*
	tar cf $(PACKAGE).tar -C $(add_on_dist) .

# Top level Makefile for cortex-strings

# Used to record the compiler version in the executables
COMPILER = $(shell $(CC) --version 2>&1 | head -n1)

if WITH_NEON
# Pull in the NEON specific files
neon_sources = \
	src/neon/memcpy.S \
	src/neon/memset.S
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
	tests/test-memcpy \
	tests/test-memset \
	tests/test-strcmp \
	tests/test-strcpy \
	tests/test-strlen

# Benchmarks and example programs
noinst_PROGRAMS = \
	dhry \
	dhry-native \
	try-none \
	try-all \
	try-bionic \
	try-csl \
	try-glibc \
	try-newlib \
	try-plain

# Libraries used in the benchmarks and examples
noinst_LIBRARIES = \
	libbionic.a \
	libcsl.a \
	libglibc.a \
	libnewlib.a \
	libplain.a \
	libmulti.a

# Main library
libcortex_strings_la_SOURCES = \
	$(neon_sources) \
	src/thumb-2/strcmp.c \
	src/thumb-2/strcpy.c \
	src/thumb-2/strlen.c

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
	reference/bionic/memcmp16.S \
	reference/bionic/strlen.c \
	reference/bionic/memset.S \
	reference/bionic/memcmp.S

libcsl_a_SOURCES = \
	reference/csl/memcpy.c \
	reference/csl/memset.c \
	reference/csl/arm_asm.h

libglibc_a_SOURCES = \
	reference/glibc/memmove.S \
	reference/glibc/memset.S \
	reference/glibc/strlen.S \
	reference/glibc/memcpy.S

libnewlib_a_SOURCES = \
	reference/newlib/strcmp.c \
	reference/newlib/strlen.c \
	reference/newlib/strcpy.c \
	reference/newlib/arm_asm.h

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
try_all_SOURCES =
try_all_LDADD = libmulti.a libcortex-strings.la -lrt
try_bionic_SOURCES =
try_bionic_LDADD = libmulti.a libbionic.a -lrt
try_csl_SOURCES =
try_csl_LDADD = libmulti.a libcsl.a -lrt
try_glibc_SOURCES =
try_glibc_LDADD = libmulti.a libglibc.a -lrt
try_newlib_SOURCES =
try_newlib_LDADD = libmulti.a libnewlib.a -lrt
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
AM_CFLAGS = -std=gnu99 -Wall -Wa,-mimplicit-it=thumb $(AM_CPPFLAGS)

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

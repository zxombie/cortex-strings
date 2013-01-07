# Copyright (c) 2011, Linaro Limited
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Linaro nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# Top level Makefile for cortex-strings

# Used to record the compiler version in the executables
COMPILER = $(shell $(CC) --version 2>&1 | head -n1)

# The main library
lib_LTLIBRARIES = \
	libcortex-strings.la

## Test suite
check_PROGRAMS = \
	tests/test-memchr \
	tests/test-memcmp \
	tests/test-memcpy \
	tests/test-memmove \
	tests/test-memset \
	tests/test-strchr \
	tests/test-strcmp \
	tests/test-strcpy \
	tests/test-strlen \
	tests/test-strncmp

# Options for the tests
tests_cflags = -I$(srcdir)/tests $(AM_CFLAGS)
tests_ldadd = libcortex-strings.la
tests_test_memchr_LDADD = $(tests_ldadd)
tests_test_memchr_CFLAGS = $(tests_cflags)
tests_test_memcmp_LDADD = $(tests_ldadd)
tests_test_memcmp_CFLAGS = $(tests_cflags)
tests_test_memcpy_LDADD = $(tests_ldadd)
tests_test_memcpy_CFLAGS = $(tests_cflags)
tests_test_memmove_LDADD = $(tests_ldadd)
tests_test_memmove_CFLAGS = $(tests_cflags)
tests_test_memset_LDADD = $(tests_ldadd)
tests_test_memset_CFLAGS = $(tests_cflags)
tests_test_strchr_LDADD = $(tests_ldadd)
tests_test_strchr_CFLAGS = $(tests_cflags)
tests_test_strcmp_LDADD = $(tests_ldadd)
tests_test_strcmp_CFLAGS = $(tests_cflags)
tests_test_strcpy_LDADD = $(tests_ldadd)
tests_test_strcpy_CFLAGS = $(tests_cflags)
tests_test_strlen_LDADD = $(tests_ldadd)
tests_test_strlen_CFLAGS = $(tests_cflags)
tests_test_strncmp_LDADD = $(tests_ldadd)
tests_test_strncmp_CFLAGS = $(tests_cflags)

TESTS = $(check_PROGRAMS)

## Benchmarks
noinst_PROGRAMS = \
	dhry \
	dhry-native \
	try-none \
	try-this \
	try-plain \
	try-newlib-c \
	try-bionic-c \
	try-glibc-c

# Good 'ol Dhrystone
dhry_SOURCES = \
	benchmarks/dhry/dhry_1.c \
	benchmarks/dhry/dhry_2.c \
	benchmarks/dhry/dhry.h

dhry_CFLAGS = -Dcompiler="\"$(COMPILER)\"" -Doptions="\"$(CFLAGS)\""
dhry_LDADD = libcortex-strings.la

dhry_native_SOURCES = $(dhry_SOURCES)
dhry_native_CFLAGS = $(dhry_CFLAGS)

# Benchmark harness
noinst_LIBRARIES = \
	libmulti.a \
	libbionic-c.a \
	libglibc-c.a \
	libnewlib-c.a \
	libplain.a

libmulti_a_SOURCES = \
	benchmarks/multi/harness.c

libmulti_a_CFLAGS = -DVERSION=\"$(VERSION)\" $(AM_CFLAGS)

## Other architecture independant implementaions
libbionic_c_a_SOURCES = \
	reference/bionic-c/bcopy.c \
	reference/bionic-c/memchr.c \
	reference/bionic-c/memcmp.c \
	reference/bionic-c/memcpy.c \
	reference/bionic-c/memset.c \
	reference/bionic-c/strchr.c \
	reference/bionic-c/strcmp.c \
	reference/bionic-c/strcpy.c \
	reference/bionic-c/strlen.c

libglibc_c_a_SOURCES = \
	reference/glibc-c/memchr.c \
	reference/glibc-c/memcmp.c \
	reference/glibc-c/memcpy.c \
	reference/glibc-c/memset.c \
	reference/glibc-c/strchr.c \
	reference/glibc-c/strcmp.c \
	reference/glibc-c/strcpy.c \
	reference/glibc-c/strlen.c \
	reference/glibc-c/wordcopy.c \
	reference/glibc-c/bp-checks.h \
	reference/glibc-c/memcopy.h \
	reference/glibc-c/pagecopy.h

libnewlib_c_a_SOURCES = \
	reference/newlib-c/memchr.c \
	reference/newlib-c/memcmp.c \
	reference/newlib-c/memcpy.c \
	reference/newlib-c/memset.c \
	reference/newlib-c/strchr.c \
	reference/newlib-c/strcmp.c \
	reference/newlib-c/strcpy.c \
	reference/newlib-c/strlen.c \
	reference/newlib-c/shim.h

libplain_a_SOURCES = \
	reference/plain/memset.c \
	reference/plain/memcpy.c \
	reference/plain/strcmp.c \
	reference/plain/strcpy.c

try_none_SOURCES =
try_none_LDADD = libmulti.a -lrt
try_this_SOURCES =
try_this_LDADD = libmulti.a libcortex-strings.la -lrt
try_bionic_c_SOURCES =
try_bionic_c_LDADD = libmulti.a libbionic-c.a -lrt
try_glibc_c_SOURCES =
try_glibc_c_LDADD = libmulti.a libglibc-c.a -lrt
try_newlib_c_SOURCES =
try_newlib_c_LDADD = libmulti.a libnewlib-c.a -lrt
try_plain_SOURCES =
try_plain_LDADD = libmulti.a libplain.a -lrt

# Architecture specific

if HOST_AARCH32

if WITH_NEON
# Pull in the NEON specific files
neon_sources = \
	src/linaro-a9/memcpy-hybrid.S
neon_bionic_sources = \
	reference/bionic/memcpy.S
neon_cppflags = -mfpu=neon
neon_dirs = neon
else
alternate_sources = \
	src/linaro-a9/memcpy.S
endif

# Benchmarks and example programs
noinst_PROGRAMS += \
	try-bionic \
	try-csl \
	try-glibc \
	try-newlib \
	try-newlib-xscale

# Libraries used in the benchmarks and examples
noinst_LIBRARIES += \
	libbionic.a \
	libcsl.a \
	libglibc.a \
	libnewlib.a \
	libnewlib-xscale.a

# Main library
libcortex_strings_la_SOURCES = \
	$(neon_sources) \
	$(alternate_sources) \
	src/thumb-2/strcpy.c \
	src/linaro-a9/memchr.S \
	src/linaro-a9/strchr.S \
	src/linaro-a9/strlen.S \
	src/linaro-a9/memset.S

# Libraries containing the difference reference versions
libbionic_a_SOURCES = \
	$(neon_bionic_sources) \
	reference/bionic/memcmp.S \
	reference/bionic/memset.S \
	reference/bionic/strcmp.S \
	reference/bionic/strcpy.S \
	reference/bionic/strlen.c

libbionic_a_CFLAGS = -Wa,-mimplicit-it=thumb

libcsl_a_SOURCES = \
	reference/csl/memcpy.c \
	reference/csl/memset.c \
	reference/csl/arm_asm.h

libglibc_a_SOURCES = \
	reference/glibc/memcpy.S \
	reference/glibc/memset.S \
	reference/glibc/strlen.S

libnewlib_a_SOURCES = \
	reference/newlib/memcpy.S \
	reference/newlib/strcmp.S \
	reference/newlib/strcpy.c \
	reference/newlib/strlen.c \
	reference/newlib/arm_asm.h \
	reference/newlib/shim.h

libnewlib_xscale_a_SOURCES = \
	reference/newlib-xscale/memchr.c \
	reference/newlib-xscale/memcpy.c \
	reference/newlib-xscale/memset.c \
	reference/newlib-xscale/strchr.c \
	reference/newlib-xscale/strcmp.c \
	reference/newlib-xscale/strcpy.c \
	reference/newlib-xscale/strlen.c \
	reference/newlib-xscale/xscale.h

# Flags for the benchmark helpers
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

AM_CPPFLAGS = $(neon_cppflags)

endif

# aarch64 specific
if HOST_AARCH64

libcortex_strings_la_SOURCES = \
	src/aarch64/memcpy.S \
	src/aarch64/memset.S \
	src/aarch64/strcmp.S

endif

libcortex_strings_la_LDFLAGS = -version-info 1:0:0

AM_CFLAGS = \
	-std=gnu99 -Wall \
	-fno-builtin -fno-stack-protector -U_FORTIFY_SOURCE \
	$(AM_CPPFLAGS)

if WITH_SUBMACHINE
AM_CFLAGS += \
	-mtune=$(submachine)
endif

EXTRA_DIST = \
	tests/hp-timing.h \
	tests/test-string.h \
	tests/test-skeleton.c \
	scripts/add-license.sh \
	scripts/bench.py \
	scripts/fixup.py \
	scripts/libplot.py \
	scripts/plot-align.py \
	scripts/plot.py \
	scripts/plot-sizes.py \
	scripts/plot-top.py \
	scripts/trim.sh \
	autogen.sh

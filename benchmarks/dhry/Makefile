# Simple Makefile to build dhry
#

CC = gcc
OPT = -O3 -g
CFLAGS += $(OPT)
REF = ../../src/reference

COMPILER = $(shell $(CC) --version 2>&1 | head -n1)

CFLAGS += -Dcompiler="\"$(COMPILER)\"" -Doptions="\"$(OPT)\""

TESTS = dhry dhry-plain dhry-neon

all: $(TESTS)

# Against the system libc
dhry: dhry_1.c dhry_2.c
	$(CC) $(CFLAGS) -o $@ $^

# Using the simple, optimised for size routines from Newlib
dhry-plain: dhry_1.c dhry_2.c $(REF)/plain/strcpy.c $(REF)/plain/memcpy.c $(REF)/plain/strcmp.c
	$(CC) $(CFLAGS) -save-temps -o $@ $^

# Using the best routines from Newlib and Bionic
dhry-neon: dhry_1.c dhry_2.c $(REF)/newlib/strcpy.c $(REF)/bionic/memcpy.S $(REF)/newlib/strcmp.c
	$(CC) $(CFLAGS) -save-temps -o $@ $^

# Using link time optimisation.  Invalidates the test as dhry uses two files
# to force certain code to run
dhry-lto: dhry_1.c dhry_2.c
	$(CC) $(CFLAGS) -flto -save-temps -o $@ $^

# Best routines with LTO.  With 4.5.1 this requires modifying the string routines
# to compile
dhry-neon-lto: dhry_1.c dhry_2.c $(REF)/newlib/strcpy.c $(REF)/bionic/memcpy.S $(REF)/newlib/strcmp.c
	$(CC) $(CFLAGS) -flto -save-temps -o $@ $^

run: dhry
	./$< N

clean:
	rm -f $(TESTS) *~ *.o *.i *.s Dhry.txt dhry-*lto

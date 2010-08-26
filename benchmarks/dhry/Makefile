# Simple Makefile to build dhry
#

CC = gcc
OPT = -O3
CFLAGS += $(OPT)

COMPILER = $(shell $(CC) --version 2>&1 | head -n1)

CFLAGS += -Dcompiler="\"$(COMPILER)\"" -Doptions="\"$(OPT)\""

TESTS = dhry

all: $(TESTS)

dhry: dhry_1.c dhry_2.c
	$(CC) $(CFLAGS) -o $@ $^

run: dhry
	./$< N

clean:
	rm -f $(TESTS) *~ *.o

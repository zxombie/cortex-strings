CFLAGS = -O2 -g -Wall -save-temps -std=gnu99 -mfpu=neon
CFLAGS += -DWITH_MEMSET

V = null libc bionic glibc newlib plain linaro csl
REF = ../../src/reference

all:
	for i in $(V); do $(MAKE) sub S=$$i; done

sub: test-$(S)

test-$(S): harness.c $(wildcard $(REF)/$(S)/*.c) $(wildcard $(REF)/$(S)/*.S)
	$(CC) $(CFLAGS) -o $@ $^
	mkdir -p obj/$(S)
	mv -f *.s *.o *.i obj/$(S)

clean:
	rm -rf $(V:%=test-%) *.o *.s *.i obj

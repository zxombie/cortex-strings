CFLAGS = -O2 -g -Wall -save-temps -std=gnu99 -mfpu=neon -lrt

VARIANTS = libc bionic glibc newlib plain linaro csl
REF = ../../reference
VERSION := $(shell bzr version-info --custom --template "{revno} ({date})")

all: $(VARIANTS:%=build-%)

build-%:
	$(MAKE) test-$* VARIANT=$*

test-$(VARIANT): harness.c $(wildcard $(REF)/$(VARIANT)/*.c) $(wildcard $(REF)/$(VARIANT)/*.S)
	$(CC) $(CFLAGS) -DVERSION="$(VERSION)" -DVARIANT=$(VARIANT) -o $@ $^
	mkdir -p obj/$(VARIANT)
	mv -f *.s *.o *.i obj/$(VARIANT)

clean:
	rm -rf $(VARIANTS:%=test-%) *.o *.s *.i obj

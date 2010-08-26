import ctypes
import timeit
import pprint
import gc
import math

plain = ctypes.cdll.LoadLibrary("install/lib/libplain.so")
libc = ctypes.cdll.LoadLibrary("/lib/libc.so.6")
bionic = ctypes.cdll.LoadLibrary("install/lib/libbionic.so")
glibc = ctypes.cdll.LoadLibrary("install/lib/libglibc.so")
newlib = ctypes.cdll.LoadLibrary("install/lib/libnewlib.so")
helpers = ctypes.cdll.LoadLibrary("install/lib/libhelpers.so")

dest = ctypes.create_string_buffer(1024*1024)
src = ctypes.create_string_buffer(('\x55' * 13) + '\0', 1024*1024)

overhead = 0

def round2(v):
    base = 10**(int(math.log10(v)))
    return int(v/base + 1) * base

def run(fun):
    timer = timeit.default_timer
    gcold = gc.isenabled()
    gc.disable()

    t0 = timer()
    fun()
    t1 = timer()

    if gcold:
        gc.enable()

    elapsed = t1 - t0

    return elapsed

# Calculate a good number of loops
loops = 100000

while True:
    elapsed = run(lambda: helpers.spawniis(plain.memcpy, loops, dest, src, 20))

    if elapsed < 0.1:
        loops *= 10
    else:
        loops = round2(loops*2/elapsed)
        print loops
        break

limit = 512*1024
step = 2
last = None

#small = range(4096, limit, 4096)
big = [int(step**x) for x in range(1, int(math.log(limit)/math.log(step)+1))]
big = []
small = range(1, 3)
steps = sorted(list(set(big) | set(small)))

print steps

for size in steps:
    if size >= 8:
        l = round2(int(loops*30/size))
    else:
        l = loops

    # tests = [
    #     lambda: helpers.spawniis(helpers.bounce, l, dest, src, size),
    #     lambda: helpers.spawniis(plain.memcpy, l, dest, src, size),
    #     lambda: helpers.spawniis(plain.memcpy2, l, dest, src, size),
    #     lambda: helpers.spawniis(libc.memcpy, l, dest, src, size),
    #     lambda: helpers.spawniis(glibc.memcpy, l, dest, src, size),
    #     lambda: helpers.spawniis(bionic.memcpy, l, dest, src, size),
    #     ]
    # tests = [
    #     lambda: helpers.spawniis(helpers.bounce, l, dest, src, size),
    #     lambda: helpers.spawniis(libc.strcpy, l, dest, src, size),
    #     lambda: helpers.spawniis(newlib.strcpy, l, dest, src, size)
    #     ]
    tests = [
        lambda: helpers.spawniis(helpers.bounce, l, dest, src, size),
        lambda: helpers.spawniis(libc.strlen, l, src, src, size),
        lambda: helpers.spawniis(glibc.strlen, l, src, src, size),
        lambda: helpers.spawniis(bionic.strlen, l, src, src, size),
        lambda: helpers.spawniis(newlib.strlen, l, src, src, size),
        ]

    results = [size, l] + [run(x) for x in tests]
    print '\t'.join('%s' % x for x in results)

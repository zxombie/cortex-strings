import ctypes
import timeit
import pprint
import gc

from pylab import *

plain = ctypes.cdll.LoadLibrary("install/lib/libplain.so")
helpers = ctypes.cdll.LoadLibrary("install/lib/libhelpers.so")

dest = ctypes.create_string_buffer(1024)
src = ctypes.create_string_buffer('Hi there', 1024)

def run(fun):
    timer = timeit.default_timer
    gcold = gc.isenabled()
    gc.disable()

    t0 = timer()
    fun()
    t1 = timer()

    if gcold:
        gc.enable()

    return t1 - t0

# Calculate a good number of loops
loops = 100000

while True:
    elapsed = run(lambda: helpers.spawniis(plain.memcpy, loops, dest, src, 20))
    print loops, elapsed

    if elapsed < 0.1:
        loops *= 10
    else:
        loops *= 2/elapsed
        base = 10**(int(math.log10(loops)))
        loops = int(loops/base + 1) * base
        print loops
        break

# Calculate the call overhead
elapsed = run(lambda: helpers.spawniis(helpers.bounce, loops, dest, src, 20))

print elapsed

elapsed = run(lambda: helpers.spawniis(plain.memcpy, loops, dest, src, 20))
print elapsed

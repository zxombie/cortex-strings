#!/usr/bin/env python

"""Simple harness that benchmarks different variants of the routines,
caches the results, and emits all of the records at the end.

Results are generated for different values of:
 * Source
 * Routine
 * Length
 * Alignment
"""

import subprocess
import math
import sys

# Prefix to the executables
build = '../build/try-'

ALL = 'memchr memcmp memcpy memset strchr strcmp strcpy strlen'

HAS = {
    'this': 'bounce memchr memcpy memset strchr strcpy strlen',
    'bionic': 'memcmp memcpy memset strcmp strcpy strlen',
    'bionic-c': ALL,
    'csl': 'memcpy memset',
    'glibc': 'memcpy memset strlen',
    'glibc-c': ALL,
    'newlib': 'memcpy strcmp strcpy strlen',
    'newlib-c': ALL,
    'newlib-xscale': 'memchr memcpy memset strchr strcmp strcpy strlen',
    'plain': 'memset memcpy strcmp strcpy',
}

def run(cache, variant, function, bytes, loops, alignment=8, quiet=False):
    """Perform a single run, exercising the cache as appropriate."""
    key = ':'.join('%s' % x for x in (variant, function, bytes, loops, alignment))

    if key in cache:
        got = cache[key]
    else:
        xbuild = build
        cmd = '%(xbuild)s%(variant)s -t %(function)s -c %(bytes)s -l %(loops)s -a %(alignment)s' % locals()

        try:
            got = subprocess.check_output(cmd.split()).strip()
        except OSError, ex:
            assert False, 'Error %s while running %s' % (ex, cmd)

    parts = got.split(':')
    took = float(parts[5])

    cache[key] = got

    if not quiet:
        print got
        sys.stdout.flush()

    return took

def run_many(cache, variants, bytes, alignments):
    # We want the data to come out in a useful order.  So fix an
    # alignment and function, and do all sizes for a variant first
    bytes = sorted(bytes)
    mid = bytes[len(bytes)/2]

    # Use the ordering in 'this' as the default
    all_functions = HAS['this'].split()

    # Find all other functions
    for functions in HAS.values():
        for function in functions.split():
            if function not in all_functions:
                all_functions.append(function)

    for alignment in alignments:
        for function in all_functions:
            for variant in variants:
                if function not in HAS[variant].split():
                    continue

                # Run a tracer through and see how long it takes and
                # adjust the number of loops based on that.  Not great
                # for memchr() and similar which are O(n), but it will
                # do
                f = 50000000
                want = 5.0

                loops = int(f / math.sqrt(max(1, mid)))
                took = run(cache, variant, function, mid, loops, alignment, quiet=True)
                # Keep it reasonable for silly routines like bounce
                factor = min(20, max(0.05, want/took))
                f = f * factor
                
                # Round f to a few significant figures
                scale = 10**int(math.log10(f) - 1)
                f = scale*int(f/scale)

                for b in sorted(bytes):
                    # Figure out the number of loops to give a roughly consistent run
                    loops = int(f / math.sqrt(max(1, b)))
                    run(cache, variant, function, b, loops, alignment)

def run_top(cache):
    variants = sorted(HAS.keys())

    # Upper limit in bytes to test to
    top = 512*1024
    # Test all powers of 2
    step1 = 2.0
    # Test intermediate powers of 1.4
    step2 = 1.4
    
    bytes = []
    
    for step in [step1, step2]:
        if step:
            # Figure out how many steps get us up to the top
            steps = int(round(math.log(top) / math.log(step)))
            bytes.extend([int(step**x) for x in range(0, steps+1)])

    alignments = [8, 16, 4, 1, 2, 32]

    run_many(cache, variants, bytes, alignments)

def main():
    cachename = 'cache.txt'

    cache = {}

    try:
        with open(cachename) as f:
            for line in f:
                line = line.strip()
                parts = line.split(':')
                cache[':'.join(parts[:5])] = line
    except:
        pass

    try:
        run_top(cache)
    finally:
        with open(cachename, 'w') as f:
            for line in sorted(cache.values()):
                print >> f, line

if __name__ == '__main__':
    main()

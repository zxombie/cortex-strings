#!/usr/bin/env python

import subprocess
import math
import sys

# Prefix to the executables
build = '../build/try-'

DEFAULTS = 'memchr memcpy memset strchr strcmp strcpy strlen'

HAS = {
    'this': DEFAULTS + ' bounce',
    'bionic': DEFAULTS,
    'glibc': DEFAULTS,
    'newlib': DEFAULTS,
    'newlib-xscale': DEFAULTS,
    'plain': 'memset memcpy strcmp strcpy',
    'csl': 'memcpy memset'
}

ORDER = 'this'.split()

def run(cache, variant, function, bytes, loops, alignment=8):
    """Perform a single run, exercising the cache as appropriate."""
    key = ':'.join('%s' % x for x in (variant, function, bytes, loops, alignment))

    if key in cache:
        print cache[key]
    else:
        xbuild = build
        cmd = '%(xbuild)s%(variant)s -t %(function)s -c %(bytes)s -l %(loops)s -a %(alignment)s' % locals()

        try:
            got = subprocess.check_output(cmd.split()).strip()
            cache[key] = got
            print got
        except OSError, ex:
            assert False, 'Error %s while running %s' % (ex, cmd)

    sys.stdout.flush()


def run_many(cache, variants, bytes, alignments):
    for variant in variants:
        functions = HAS[variant].split()

        for function in functions:
            for alignment in alignments:
                for b in sorted(bytes):
                    # Figure out the number of loops to give a roughly consistent run
                    loops = int(50000000*5 / math.sqrt(b))
                    run(cache, variant, function, b, loops, alignment)

def run_top(cache):
    variants = sorted(HAS.keys())

    bytes = set([128])
    bytes.update([2**x for x in range(0, 14)])
#    bytes.extend([2**x - 1 for x in range(1, 14)])
#    bytes.extend([int(1.3*x) for x in range(1, 45)])

    alignments = [8, 16] #1, 2, 4, 8, 16, 32]
    alignments = [16]

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
            for line in cache.values():
                print >> f, line

if __name__ == '__main__':
    main()

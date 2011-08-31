#!/usr/bin/env python

import subprocess
import math
import sys

build = '../build/try-'


def run(cache, variant, function, bytes, loops):
    key = ':'.join('%s' % x for x in (variant, function, bytes, loops))

    if key in cache:
        print cache[key]
    else:
        xbuild = build
        cmd = '%(xbuild)s%(variant)s -t %(function)s -c %(bytes)s -l %(loops)s' % locals()

        got = subprocess.check_output(cmd.split()).strip()
        cache[key] = got
        print got

    sys.stdout.flush()


def run_bytes(cache, variant, function, bytes):
    for b in bytes:
        loops = int(500000000/5 / math.sqrt(b))
        run(cache, variant, function, b, loops)


def run_functions(cache, variant, functions, bytes):
    for function in functions:
        run_bytes(cache, variant, function, bytes)


HAS = {
    'this': 'strcmp strcpy memchr strchr strlen memcpy memset',
    'bionc': 'strlen memset memcpy',
    'glibc': 'memset strlen memcpy  strcmp strcpy memchr strchr',
    'newlib': 'strcmp strlen strcpy',
    'plain': 'memset memcpy strcmp strcpy',
    'csl': 'memcpy memset'
}


def run_variant(cache, variant, bytes):
    functions = HAS[variant].split()
    run_functions(cache, variant, functions, bytes)


def run_variants(cache, variants, bytes):
    for variant in variants:
        run_variant(cache, variant, bytes)


def run_top(cache):
    variants = HAS.keys()
    bytes = [2**x for x in range(1, 12)]
    run_variants(cache, variants, bytes)


def main():
    cachename = 'cache.txt'

    cache = {}

    try:
        with open(cachename) as f:
            for line in f:
                line = line.strip()
                parts = line.split(':')
                cache[':'.join(parts[:4])] = line
    except:
        pass

    try:
        run_top(cache)
    finally:
        with open(cachename, 'w') as f:
            for line in cache.values():
                print >> f, line

main()

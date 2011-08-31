#!/usr/bin/env python

"""Plot the performance for different block sizes of one function across
variants.
"""

import libplot

import pylab
import pdb

def plot(records, function):
    variants = libplot.unique(records, 'variant')
    records = [x for x in records if x.function==function]

    bytes = libplot.unique(records, 'bytes')

    colours = iter('bgrcmyk')

    pylab.clf()

    for variant in variants:
        matches = [x for x in records if x.variant==variant]
        matches.sort(key=lambda x: x.bytes)

        X = [x.bytes for x in matches]
        Y = [x.bytes*x.loops/x.elapsed/(1024*1024) for x in matches]

        colour = colours.next()

        if X:
            pylab.plot(X, Y, c=colour)
            pylab.scatter(X, Y, c=colour, label=variant)

    pylab.legend(loc='upper left')
    pylab.grid()
    pylab.title('%s in MB/s' % function)
    pylab.xlabel('Size (B)')
    pylab.ylabel('Rate (MB/s)')
    pylab.semilogx()
    pylab.xlim(0, max(X))
    pylab.ylim(0, pylab.ylim()[1])

def main():
    records = libplot.parse()

    functions = libplot.unique(records, 'function')

    for function in functions:
        plot(records, function)
        pylab.savefig('sizes-%s.png' % function)

if __name__ == '__main__':
    main()


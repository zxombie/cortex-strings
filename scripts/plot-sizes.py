#!/usr/bin/env python

"""Plot the performance for different block sizes of one function across
variants.
"""

import libplot

import pylab
import pdb

def plot(records, function, alignment=None):
    variants = libplot.unique(records, 'variant')
    records = [x for x in records if x.function==function]

    if alignment != None:
        records = [x for x in records if x.alignment==alignment]

    alignments = libplot.unique(records, 'alignment')
    assert len(alignments) == 1
    aalignment = alignments[0]

    bytes = libplot.unique(records, 'bytes')[0]

    colours = iter('bgrcmyk')
    all_x = []

    pylab.clf()

    for variant in variants:
        matches = [x for x in records if x.variant==variant]
        matches.sort(key=lambda x: x.bytes)

        X = [x.bytes for x in matches]
        Y = [x.bytes*x.loops/x.elapsed/(1024*1024) for x in matches]

        all_x.extend(X)
        colour = colours.next()

        if X:
            pylab.plot(X, Y, c=colour)
            pylab.scatter(X, Y, c=colour, label=variant)

    pylab.legend(loc='upper left')
    pylab.grid()
    pylab.title('%(function)s of %(aalignment)s byte aligned, %(bytes)s byte blocks' % locals())
    pylab.xlabel('Size (B)')
    pylab.ylabel('Rate (MB/s)')
    pylab.semilogx()
    pylab.xlim(0, max(all_x))
    pylab.ylim(0, pylab.ylim()[1])

def main():
    records = libplot.parse()

    functions = libplot.unique(records, 'function')

    for function in functions:
        plot(records, function)
        pylab.savefig('sizes-%s.png' % function)

if __name__ == '__main__':
    main()


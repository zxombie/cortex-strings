#!/usr/bin/env python

"""Plot the performance of different variants of the string routines
for one size.
"""

import libplot

import pylab


def plot(records, bytes):
    records = [x for x in records if x.bytes==bytes]

    variants = libplot.unique(records, 'variant')
    functions = libplot.unique(records, 'function')

    X = pylab.arange(len(functions))
    width = 1.0/(len(X)+1)

    colours = iter('bgrcmyk')

    for i, variant in enumerate(variants):
        heights = []

        for function in functions:
            matches = [x for x in records if x.variant==variant and x.function==function]

            if matches:
                match = matches[0]
                heights.append(match.bytes*match.loops/match.elapsed/(1024*1024))
            else:
                heights.append(0)

        pylab.bar(X+i*width, heights, width, color=colours.next(), label=variant)

    axes = pylab.axes()
    axes.set_xticklabels(functions)
    axes.set_xticks(X + 0.5)

    pylab.title('Performance of different variants for %d byte blocks' % bytes)
    pylab.ylabel('Rate (MB/s)')
    pylab.legend()
    pylab.grid()
    pylab.savefig('top-%d.png' % bytes)

def main():
    records = libplot.parse()
    plot(records, 64)
    pylab.show()

if __name__ == '__main__':
    main()


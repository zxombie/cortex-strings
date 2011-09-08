#!/usr/bin/env python

"""Plot the performance of different variants of one routine versus alignment.
"""

import libplot

import pylab


def plot(records, bytes, function):
    records = [x for x in records if x.bytes==bytes and x.function==function]

    variants = libplot.unique(records, 'variant', prefer='this')
    alignments = libplot.unique(records, 'alignment')

    X = pylab.arange(len(alignments))
    width = 1.0/(len(variants)+1)

    colours = iter('bgrcmyk')

    pylab.figure(1).set_size_inches((16, 12))
    pylab.clf()

    for i, variant in enumerate(variants):
        heights = []

        for alignment in alignments:
            matches = [x for x in records if x.variant==variant and x.alignment==alignment]

            if matches:
                match = matches[0]
                heights.append(match.bytes*match.loops/match.elapsed/(1024*1024))
            else:
                heights.append(0)

        pylab.bar(X+i*width, heights, width, color=colours.next(), label=variant)


    axes = pylab.axes()
    axes.set_xticklabels(alignments)
    axes.set_xticks(X + 0.5)

    pylab.title('Performance of different variants of %(function)s for %(bytes)d byte blocks' % locals())
    pylab.ylabel('Rate (MB/s)')
    pylab.legend(loc='upper left', ncol=3)
    pylab.grid()
    pylab.savefig('alignment-%(function)s-%(bytes)d.png' % locals(), dpi=72)

def main():
    records = libplot.parse()

    for function in libplot.unique(records, 'function'):
        for bytes in libplot.unique(records, 'bytes'):
            plot(records, bytes, function)

    pylab.show()

if __name__ == '__main__':
    main()

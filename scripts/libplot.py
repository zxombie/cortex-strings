import fileinput
import collections

Record = collections.namedtuple('Record', 'variant function bytes loops elapsed rest')


def parse_value(v):
    try:
        return float(v)
    except ValueError:
        return v


def unique(records, name):
    values = set(getattr(x, name) for x in records)
    return sorted(values)


def parse():
    return [Record(*[parse_value(y) for y in x.split(':')]) for x in fileinput.input()]

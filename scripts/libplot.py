"""Shared routines for the plotters."""

import fileinput
import collections

Record = collections.namedtuple('Record', 'variant function bytes loops alignment elapsed rest')


def parse_value(v):
    """Turn text into a primitive"""
    try:
        if '.' in v:
            return float(v)
        else:
            return int(v)
    except ValueError:
        return v


def unique(records, name, prefer=''):
    """Return the unique values of a column in the records"""
    values = list(set(getattr(x, name) for x in records))

    if not values:
        return values
    elif type(values[0]) == str:
        keys = ['%06d|%s' % (-prefer.find(x), x) for x in values]
        print keys, prefer
        return sorted(values, key=lambda x: '%-06d|%s' % (-prefer.find(x), x))
    else:
        return sorted(values)

def parse():
    """Parse a record file into named tuples, correcting for loop
    overhead along the way.
    """
    records = [Record(*[parse_value(y) for y in x.split(':')]) for x in fileinput.input()]

    # Pull out any bounce values
    costs = {}

    for record in [x for x in records if x.function=='bounce']:
        costs[(record.bytes, record.loops)] = record.elapsed

    # Fix up all of the records for cost
    out = []

    for record in records:
        if record.function == 'bounce':
            continue

        cost = costs.get((record.bytes, record.loops), None)

        if not cost:
            out.append(record)
        else:
            # Unfortunately you can't update a namedtuple...
            values = list(record)
            values[-2] -= cost
            out.append(Record(*values))

    return out

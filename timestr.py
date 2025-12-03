#! /usr/bin/env python3
from decimal import Decimal
import datetime
"""
    this is a helper modual
    count the time and format the output

"""


def timefm(second):
    timedelt = datetime.timedelta(seconds=(second))
    [hh, mm, ss] = str(timedelt).split(":")
    ss = str(Decimal(ss).quantize(Decimal("0.000")))
    return "{}:{}:{}".format(hh, mm, ss)


if __name__ == "__main__":
    str_start = datetime.timedelta(seconds=(4.444))
    [h, m, s] = str(str_start).split(':')
    s = Decimal(s).quantize(Decimal("0.000"))
    print(str_start)
    print(type(str_start))
    print(timefm(4.44444))

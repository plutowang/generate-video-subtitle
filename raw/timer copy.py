#! /usr/bin/env python3
import time
"""
    this is a helper modual
    count the time and format the output

"""
from decimal import Decimal
#  import math
import datetime
#
#
#  class TimeStamp():
#      hh = 0
#      mm = 0
#      ss = 0
#
#      def __init__(self, start):
#          if start < 60:
#              self.ss = start
#          else:
#              [a, b] = math.modf(start)
#              self.mm = b / 60
#              self.ss = self.ss % 60 + a
#          if self.mm >= 60:
#              self.hh = self.mm / 60
#              self.mm = self.mm % 60
#
#      def addSeconds(self, seconds):
#          self.ss = Decimal(self.ss).quantize(
#              Decimal("0.000000000")) + Decimal(seconds).quantize(
#                  Decimal("0.000000000"))
#          if self.ss >= 60:
#              [a, b] = math.modf(self.ss)
#              self.mm += int(b / 60)
#              self.ss = b % 60 + a
#          if self.mm >= 60:
#              self.hh += int(self.mm / 60)
#              self.mm = self.mm % 60
#
#      def toString(self):
#          self.ss = Decimal(self.ss).quantize(Decimal("0.000"))
#          self.mm = Decimal(self.mm).quantize(Decimal("0"))
#          self.hh = Decimal(self.hh).quantize(Decimal("0"))
#          #  self.hh = round(self.hh, 8)
#          if self.ss < 10:
#              str_s = '0' + str(self.ss)
#          else:
#              str_s = str(self.ss)
#
#          if self.mm < 10:
#              str_m = '0' + str(self.mm)
#          else:
#              str_m = str(self.mm)
#
#          if self.hh < 10:
#              str_h = '0' + str(self.hh)
#          else:
#              str_h = str(self.hh)
#
#          return str_h + ':' + str_m + ':' + str_s
#

#  class DeltaTemplate(Template):
#      delimiter = "%"
#

#  def strfdelta(tdelta, fmt):
#      d = {"D": tdelta.days}
#      d["H"], rem = divmod(tdelta.seconds, 3600)
#      d["M"], d["S"] = divmod(rem, 60)
#      t = DeltaTemplate(fmt)
#      return t.substitute(**d)
#

if __name__ == "__main__":
    str_start = datetime.timedelta(seconds=(4.444))
    [h, m, s] = str(str_start).split(':')
    s = Decimal(s).quantize(Decimal("0.000"))
    print(s)
    print(str_start)
    print(type(str_start))

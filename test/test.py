__author__ = 'pok'
import sys

sys.path.append("../rec/")

from rec.rec import user_cf


print user_cf("./u1.base")

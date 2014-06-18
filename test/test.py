__author__ = 'pok'
import sys, time

sys.path.append("../rec/")

from rec.rec import user_cf
from rec.rec import item_cf
from rec.rec import slope_one
# b = time.time()
# print user_cf("./u1.base")
# print time.time() - b

# b = time.time()
# print item_cf("./u1.base")
# print time.time() - b

b = time.time()
print slope_one("./u1.base")
print time.time() - b
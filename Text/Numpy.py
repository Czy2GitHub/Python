# coding:utf-8
import numpy as np
from array import array
a = array("d", [1, 2, 3, 4])
print(a)
na = np.frombuffer(a, dtype=np.float)
print(na)
na[1] = 20
print(na)
print(a)

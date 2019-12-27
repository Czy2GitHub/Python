# coding:utf-8
# lambda匿名函数的测试
# 只会使用到一次的函数 为简化代码而采用
import math

def circle(r):
    return r*r*math.pi
    print(circle(2))

# 等价于
print(circle(2))
d = 2
r = lambda r:d*d*math.pi
print(r(d))



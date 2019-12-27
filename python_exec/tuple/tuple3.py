# -*- coding:utf-8 -*-
import random
# 元组推导式 快速生成一个元组
# 与列表推导式不同 元组推导式生成的结果是一个生成器对象 需要强制转换(tuple()和list())来生成元组或列表
# 生成器对象在执行tuple()或者list()函数后就会被清空
random_number = (random.randint(10, 20) for x in range(10))
print("生成的生成器对象为:", random_number)
random_number1 = (random.randint(10, 20) for i in range(10))
# 强制转型
tuple1 = tuple(random_number)
list1 = list(random_number1)
print(tuple1, " ", "类型为:", type(tuple1))
print(list1, " ", "类型为:", type(list1))

# 利用_next()_方法遍历生成器对象
number1 = (random.randint(10, 20) for i in range(10))
print(number1.__next__())





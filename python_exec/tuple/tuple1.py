# -*- coding:utf-8 -*-

# 空元组 应用于为函数传递空值的情况下(需要传递但不想为其传递)
empty_tuple = ()

# 可以使用range()函数来生成元组
tuple1 = tuple(range(10, 20, 2))
print("生成的元组为:", tuple1)

# 删除元组
del tuple1

# 访问元组元素
tuple2 = (7, 2, 6, 9, 8, 7)
print(tuple2)

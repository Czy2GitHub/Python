# -*- coding:utf-8 -*-

# 定义一个列表，使用循环为其赋值
list1 = []
for element in range(10):
    list1.append(element)
print(list1)
list1 = ["777", '888', '999']
print(list1)

# 定义元组
tuple1 = ("666", '777', 'abc')
for value in tuple1:
    print(value)
try:
    tuple1[1] = 'bcd'
except TypeError:
    print("元组元素不能被修改!")
finally:
    print("OK!")

# 在元组中嵌套列表 其中的列表可以修改
tuple2 = ('a', 'b', ['c', 'd'])
try:
    tuple2[2][0] = 'n'
    tuple2[2][1] = 'q'
    tuple2[0] = 'c'
except TypeError:
    print("元组元素不能被修改!")
finally:
    print(tuple2)

# 条件判断语句 if else    if elif elif else  if
# && == and   || == or


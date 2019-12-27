# -*- coding:utf-8 -*-
# 使用函数对python进行统计
list1 = [1,3,4,5,6,1,3,1,2,4,5]

# 统计指定元素在列表里出现的个数
# 使用count()函数, listname.count(obj)
# obj:只能精确匹配，如果列表中不存在指定元素则会报错
print(list1.count(1))

# 统计指定元素在列表中第一次出现的索引
# 使用index()函数, listname.index(obj)
print(list1.index(3))

# 统计各元素的和
# 使用sum()函数, sum(iterable,start)
# iterable值需要求和的列表，start是在统计结果后再加上start的值，不填默认是0
value = sum(list1)
print(value)

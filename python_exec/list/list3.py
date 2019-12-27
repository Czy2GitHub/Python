# -*- coding: utf-8 -*-
# 列表的增删改查
list1 = ["基本语言", "c语言", "Java", "c++", "python"]
# 添加
list1.append("JavaScript")
print(list1)
# 删除
# del listname[下标]
# listname.remove()指定元素删除
value = 'c++'
if list1.count(value) > 0:
    list1.remove(value)
del list1[-1]
del list1[1]
print(list1)
#修改
#直接使用下标修改
list[-1] = "HTML"
list[2] = "Java辣鸡语言"
#查找
#for循环查找
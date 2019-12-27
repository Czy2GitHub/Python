# -*- coding: utf-8 -*-
# 创建列表
list1=["python","人脸识别","语音识别","简单易上手"]
# 遍历列表
for item in list1:
    print(item)
# 删除列表
# del list
# 使用list()来快速创建列表,数值为10到二十之间的偶数
list2 = list(range(10, 20, 2))
for item in list2:
    print(item)
# 使用for和enumerate()循环来实现输出列表元素的下标和元素的值
# for index,item in enumerate(listname):
# index,item 为数组的下标和元素值的形参 listname 列表的名字
for index, item in enumerate(list1):
    print(index + 1, item)


# -*- coding: utf-8  -*-
# 序列的定义和下标的读取
list = ["哇哈哈哈哈哈","ohohohohh00","nnnnnnnnnnnnnnnnn"]
# python中允许下标为副，下标-1为数组最后一个元素
print(list[2])
print(list[-1])

# 序列的切片操作
# sname(start:end:step)i
# sname : 名字  start： 切片操作开始的位置 end：切片操作结束的位置
print("将数组切片输出的结果是:")
print(list[1:2])

# 序列相加，生成新的序列
list1 = ["我日"]
list2 = list + list1
print(list2)

# 使用乘法
print(list1*2)

# 检查某元素是否在序列内，使用in关键字
print("我日"in list2)

# 输出序列的长度，最大值，最小值
print("序列list的长度为", len(list))
num = [1, 2, 3, 4, 5, 6, 7, 9, 5, 8]
print("序列num的最大值为", max(num))
print("序列num的最小值为", min(num))

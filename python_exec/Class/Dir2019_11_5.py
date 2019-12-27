# -*- coding:utf-8 -*-

# 使用list()与range()函数生成一个列表
even_number = list(range(2, 11, 2))
print(even_number)

# print()使用','达到不换行
x = 1
y = 2
print(x, y)
# 使用end = ""来使print()不换行
print(x, end="")
print(y)


# 列表 下标从0开始 有序 可以存放任意类型的元素
list1 = ['IG', 'The Shy', 'Ning', 'Rooie', "JackLove", "baoLan", 3, 5, True]
print(list1)
print(list1[1], "被定住了")

# 使用负数下标
print(list1[-1])    # 最后一个元素

# 使用":", 截取下标 前包后不包
t = list1[1:3]
t1 = list1[1:]      # 冒号后面不填默认最大
t2 = list1[:-1]     # 冒号前面不填默认为0
print(t, t1, t2)
'''
try:
    print(list1[1000])
except:
    print("下标错误!")
'''

# 删除列表元素
del list1[-1]
print(list1)

# 在队尾插入元素
list1.append("登峰造极境")
print(list1)

# 指定位置插入元素
list1.insert(0, '翻过这座山')
print(list1)

# 使用pop()方法删除元素 删除列表最后一个元素
for i in range(3):
   data = list1.pop()
   print(data)
print(list1)

# 指定元素删除 .remove()方法
list1.remove('IG')
print(list1)

# 为列表永久排序 .sort()方法排序
list1.sort()
print(list1)

# 为列表临时排序,sorted()方法
sorted(list1, reverse=True)
print(list1)

# 倒序排列 .sort(reverse=True)
list1.sort(reverse=True)
print(list1)

# 倒序打印列表 .reverse()方法
list1.reverse()


# -*- coding:utf-8 -*-

# 第一行代码
print("Hello World")
# python2中 为 print "Hello World"

# input()方法输入 python2中为raw_input()
list1 = []
count = 0
'''
number = int(input("请输入需要求和的数的数量:"))
for i in range(number):
    i = input("请输入一个数:")
    j = int(i)
    count += j
print("所输入的数的和为:", count)
'''
'''
str1 = input("请输入一个数:")
str2 = input("请再输入一个数:")
sum = int(str1) + int(str2)
print("两个数的和为:", sum)
'''
# 使用type()来判断类型
k = True
type(k)
# python 布尔类型可以进行计算 True = 1 False = 0
j = 2 ; print(j + k)

# 允许给多个变量同时赋值
a = b = c = 1
n, m, d = 1, 2, "JackLove"
print(type(d))
print(type(a))













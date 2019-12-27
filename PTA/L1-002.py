# coding:utf-8
# 本题要求你写个程序把给定的符号打印成沙漏的形状。例如给定17个“*”，要求按下列格式打印
# #
# # *****
# #  ***
# #   *
# #  ***
# # *****
# # 所谓“沙漏形状”，是指每行输出奇数个符号；各行符号中心对齐；相邻两行符号数差2；符号数先从大到小顺序递减到1，再从小到大顺序递增；首尾符号数相等。
# #
# # 给定任意N个符号，不一定能正好组成一个沙漏。要求打印出的沙漏能用掉尽可能多的符号。

# 注：得到的沙漏 总元素数为 2*n^2 - 1, 一半为n^2；每一行与字符串的关系:2 n - 1
from math import sqrt
# 得到字符总数
number = int(input())
# 得到指定字符
char = input()
# 根据元素个数判断能输出多少行
n = int(sqrt(number / 2))  # 得到元素的行数
temp1 = n


while temp1 >= 0:
    if temp1 <= n:
        print("1"*(n - temp1))

    if temp1 == 0:
        print(char*(temp1*2 - 1), end="")
        temp1 -= 1
        break
    else:
        print(char*(temp1*2 - 1), end="")
    temp1 -= 1


temp1 = n
for i in range(1, n):
    print(char*(temp1*2 - 1))

# -*- coding:utf-8 -*-

# 字符串的分隔
# str.split(sep, maxsplit)
# str:表示要分隔的字符串
# sep:指定分割所需要的换行符
# maxsplit:指定分割的次数
str1 = '百度一下 你就知道 >>> www.baidu.com'
print(str1.split('>>>'))
print(str1.split('.', 2))

# 检索字符串
# str.count(sub[, start[, end]])方法
# str:表示原字符串
# sub:表示要检索的子字符串
# start:可选参数, 起始索引， 默认从头开始
# end:可选参数, 结束位置，默认到结尾
i = str1.count('.', 1)
print(i)

# 查找子字符串
# 查找子字符串第一次出现的索引
# str.find(sub, start, end)  or str.index()
print(str1.find('www'))
print(str1.index('www'))


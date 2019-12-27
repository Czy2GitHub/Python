# -*- coding:utf-8 -*-
# 千年虫问题 把下列列表中存在千年虫问题的数据进行提取并修改，然后按年龄从高到低输出
# list = [45, 89, 1998, 00, 75, 33, 1968, 37, 1958, 90]
# 输出结果:list = [1933, 1937, 1945, 1958, 1968, 1975, 1989, 1990,1998, 2000]
list_first= [45, 89, 1998, 00, 75, 33, 1968, 37, 1958, 90]
for k, i in enumerate(list_first):
    if (i < 100) and (i > 0):
        list_first[k] = 1900 + i
    if i == 00:
        list_first[k] = 2000 + i
list_first.sort()
print(list_first)


# -*-coding:utf-8-*-

# 使用循环遍历列表
list1 = ["FPX", "doinb"]
for i in list1:
    print(i, end=",")

# .titile()  使首字母大写 只是生成一个新的元素 不改变原来元素的值
i = list1[1].title()
print(i)

# 使用循环创建列表
for index, value in enumerate(list1):
    print(value, index)

# 最大值最小值求和max() min() sum()

# 元组 不可变的列表 改变只能为其重新定义
tuple1 = ("IG", "FPX", "SKT", "G2")

# 字典 key 与 value 对应 如果存在重复的key值 后者的值会将前者的值覆盖 字典中key起着下标的作用
dictionary1 = {'color': 'Red', 'code': 'Red'}
print(dictionary1['code'])

# 直接添加字典中元素
dictionary1["color"] = 'Yellow'
dictionary1["Blue"] = 'None'
print(dictionary1)

# 遍历字典 使用.items()方法
for index, value in dictionary1.items():
    print(value, index)

# 遍历key值
for i in dictionary1.keys():
    print(i)

# 字符串
str1 = ""

# 字符串的拼接
str1 = str1 + "7"

# 字符串的查找

print(str1.find('7'))         # 查找指定字符 存在返回0 不存在返回-1
str1.index("7")                  # 查找指定字符的下标 不存在会抛出异常
print(str1.replace("7", '7777777'))       # 替换字符串 函数执行完毕会生成一个新的字符串，不会更改原本字符串
print(str1)

# 去除空格
str2 = " Hello World"
print(str2.strip())                # 左右两边
print(str2.lstrip())               # 左边
print(str2.rstrip())               # 右边

# 拆分字符串
str3 = "7d5d9d6d3d2d5d"
list2 = str.split(str3, 'd')
print(list2)

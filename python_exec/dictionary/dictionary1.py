# -*- coding:utf-8 -*-

# 使用映射创建字典
# dictionary = dict(zip(list1,list2))
# 其中list1, list2 分别为对应的key值 value值
# 如果两个列表的长度不同 则生成的字典则以最短的列表为主

list1 = ["animals", "fruit", "green"]
list2 = ["Cat", "peach", "you_dian"]
dictionary1 = dict(zip(list1, list2))
print(dictionary1)

# 使用dict(key1=value1, key2=value2)的方式创建字典
dictionary2 = dict(print='python', printf='c++', out_println='Java')
print(dictionary2)

# 通过元组和列表 创建字典
name_tuple = ('python', 'Java', 'C++', 'C语言')
name_list = ['print', 'out.println', 'printf']
dictionary3 = {name_tuple:name_list}
print(dictionary3)

# 使用元组 创建字典的key值
name1_tuple = ('p', 'J', 'C', '++')
dictionary4 = dict.fromkeys(name1_tuple)
print(dictionary4)


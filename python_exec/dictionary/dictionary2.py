# -*- coding:utf-8 -*-

# 查找字典
dictionary = {'python': 'print', 'java': 'out.println'}
print("python的输出方式为:", dictionary["python"] if 'python' in dictionary else "字典里无其资料！")

# 遍历字典
# 使用.items()方法
for item in dictionary.items():
    print(item)

# 遍历输出键与值
for key, value in dictionary.items():
    print(key, "对应的值是:", value)

# 添加、修改、删除元素
# 若存在所新定义的键 则为修改 若不存在 则为添加
dictionary["python人脸识别"] = "dlib库"
print(dictionary)
dictionary['python'] = 'print()'
print(dictionary)
if 'python' in dictionary:
    del dictionary["python"]
    print("删除成功!")
else:
    print("该元素不在字典中!")


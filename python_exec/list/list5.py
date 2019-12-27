# -*- coding:utf-8 -*-
# 对列表进行排序
list1 = [1, 9, 8, 7, 6, 3, 5, 6, 2, 4]
# 使用sort()方法来实现
# listname.sort()(key=None, reverse=False)
# key:设置比较键(例如：key=str.lower表示在排序的时候不区分大小写)
# reverse:若值为True 则为降序排列 若值为Flase 则为升序排列
print("原序列", list1)
list1.sort()
print("排序后的序列", list1)
list1.sort(reverse=True)
print("降序排列的顺序为", list1)
# 按字母顺序排序,默认区分大小写
list_a = ['Angela', 'Tom', 'pet', 'cat']
list_a.sort()
print("区分大小写排序", list_a)
list_a.sort(key=str.lower)
print("不区分大小写", list_a)




# 使用内置的sorted()函数实现
# sorted(iterable, key=None, reverse=False)
# iterable:排序的列表名称
# key:比较键
# reverse:若值为True 则为降序排列 若值为Flase 则为升序排列
# 与.sort()区别:生成了一个新的列表，而sort()只是在原列表上进行修改
list2 = sorted(list1)
print("升序排列的顺序为", list2)
list3 = sorted(list1, reverse=True)
print("降序排列的序列", list3)





# -*-coding:utf-8 -*-
# 列表推导式
# listname = [Expression for var in range]
# Expression:表达式，用于计算新列表的元素
# var:循环变量
# range:采用range()函数生成range对象
import random

# 生成一个存在10个值在10到100之间的随机数的列表
random_number = [random.randint(10, 100) for var in range(10)]
print("生成的列表为", random_number)

# 根据列表生成指定功能的列表
# newList = [Expression for var in  list]
price = [1200, 3500, 2580, 7894, 1478]
new_price = [int(x*0.5) for x in price]
print("原价格", price)
print("打五折价格", new_price)

# 从列表中选择符合条件的元素 创建新的列表
# newList = [Expression for  var in list if condition]
# condition:条件表达式 用来指定筛选条件
sale = [x for x in price if x > 5000]
print("价格大于五千的商品有:", sale)












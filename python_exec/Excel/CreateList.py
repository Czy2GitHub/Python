# -*- coding:utf-8 -*-
import xlwt
from Data import *
# 使用xlwt.Workbook()创建一个表格对象
xls = xlwt.Workbook()

# 再调用对象创建一个表格，使用add_sheet方法添加到表格文件里
sht1 = xls.add_sheet("text_sheet1")

# 使用write的方法写入，write(行，列，值)
count = 0
k = True
for i in list1:
    if count == 0:
        k = True
    else:
        k = False
    if k :
        sht1.write_merge(0, 0, 0, 2, i)
        continue
    sht1.write(count+1, 1, count+1)
    sht1.write(count+1, 3, i)
    count += 1
xls.save("List/Mydata.xls")
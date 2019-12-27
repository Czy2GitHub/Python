# coding:utf-8
import xlwt
from Data import *

dictionary = {}
xls = xlwt.Workbook()

sheet1 = xls.add_sheet("Text_sheet1")

for index,value in enumerate(list4):
    sheet1.write(index, 1, value)
for index, value in enumerate(list5):
    sheet1.write(index, 3, value)
for index, value in enumerate(list6):
    sheet1.write(index, 5, value)
for index, value in enumerate(list7):
    sheet1.write(index+len(list5), 3, value)
for index, value in enumerate(list8):
    sheet1.write(index+len(list6), 5, value)
xls.save("List/成员统计表.xls")
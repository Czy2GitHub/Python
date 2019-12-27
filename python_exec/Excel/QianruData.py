# coding:utf-8

import xlwt

dictionary = {"041940931": "赵敏杰", "041940409": "李瑾", "041940232": "徐金铠", "041940228": "王鹏飞", "041940834": "周晓岐", "041940526": "陶昊天",
              "041940510": "王一竹", "041940306": "李佩晏", "041940313": "杨晶雯", "041940311": "王丽然", "041940824": "王英龙", "041940810": "包龙"
              , "041940414": "朱桐", "041940406": "冷嘉轩"}
# 创建一个新的Excel表格
xls = xlwt.Workbook()
sht1 = xls.add_sheet("Sheet1")
count = 0
for key, value in dictionary.items():
    sht1.write(count, 4, key)
    sht1.write(count, 3, value)
    count += 1
count = 0
for i in range(int(len(dictionary)/2)):
    sht1.write(count, 2, i+1)
    count += 2
xls.save("./List/参赛人员.xls")
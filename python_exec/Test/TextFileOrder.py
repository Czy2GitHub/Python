# coding:utf-8
# 测试文件的读写，与创建
# open()方法打开文件
# 使用with expression as file 的格式
# open()的参数：第一个为文件名 第二个为权限
# w：只写 w+：清空文件，只写 a：追加模式打开文件 a+:读写权限，若文件不存在，则创建 r：只读
with open("TextFile.txt","r") as file:
    # file.write(" 我曾难自拔于世界之大，也沉浸于其中梦话 ")        # 写入内容,必须为w，w+，a，a+下有效
    massage = file.readlines()   # 读一行，仅r，r+下有效
    for value in massage:
        print(value)
# .read()方法
# 读取指定字符个数，不给参数默认全部字符
with open("TextFile.txt", "r") as file:
    # massage = file.read()
    massage1 = file.read(5)
    print(massage, "  ", massage1)
# .seek()方法
# 改变文件指针的位置
with open("TextFile.txt", "r") as file:
    file.seek(22)       # 移动的是字节位 一个汉字两个字节 UNICODE
    print(file.read(8)) # 读取的是字符

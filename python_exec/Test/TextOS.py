# coding:utf-8
import os
# 测试OS的各种命令
# os.name 获得操作系统名称 nt为windows posix 为Linux等
# print(os.name)
# os.linesep 获得操作系统中的换行符
print(os.linesep)       # 在pyCharm中不显示

# .getcwd()获取当前级目录
print(os.getcwd())
# .path.abspath()方法
print(os.path.abspath("/Test"))
# os.mkdir()创建目录
# os.rmdir()删除目录
# os.walk()遍历一个目录
# os.remove()删除一个文件
# os.rename(old, new)重命名一个文件
# os.stat()获取文件基本信息
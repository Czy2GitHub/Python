# -*- coding:utf-8 -*-

# 字符串的拼接 +
str1 = "python"
str2 = "Java"
print(str1 + str2)

# 使用len()获得字符串的长度
i = len(str1)
print(i)

# 使用utf-8时汉字占3字节 GBK中汉字占2字节
# 使用encode()方法编码后再进行获取
str2 = "人生苦短, 我用python!"
i = len(str2.encode())
print(i)
j = len(str2.encode('gbk'))
print(j)

# 截取字符串
str3 = str1[2:5]    # 截取3到5个字符
print(str3)
str4 = str1[5:]     # 从第6个字符截取到最后
print(str4)
str5 = str1[1]      # 截取第2个字符
print(str5)


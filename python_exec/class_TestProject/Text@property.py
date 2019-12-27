# coding:utf-8
# 测试装饰器 @property
# 能够将有返回值的方法转换成类的属性
import math

class Rectangle:
    def __init__(self,width, heigth):
        self.width = width
        self.heigth = heigth
        print("类初始化完成!")
# 通过装饰器@property 将方法转化成属性
    @property
    def area(self):
        return self.heigth*self.width*math.pi


if __name__ == "__main__":
    c = Rectangle(5, 5)
    print(c. area)

# -*- coding:utf-8 -*-
from Shape import Shape
class Square(Shape):
    def __init__(self, side):
        Shape.__init__(self, side, side)
        self.side = side
    def area(self):
        print("矩形的面积为:", self.side**2)
    def girth(self):
        print("矩形的周长为:", self.side*4)

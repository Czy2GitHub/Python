# -*- coding:utf-8 -*-
from Shape import Shape
from math import pi
class Circle(Shape):
    def __init__(self, radius):
        Shape.__init__(self, radius, radius)
        self.radius = radius
    def area(self):
        print("圆形的面积为:", self.radius**2*pi)
    def girth(self):
        print("图形的周长为:", self.radius*2*pi)








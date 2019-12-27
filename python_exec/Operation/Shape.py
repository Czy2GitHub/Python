# -*- coding:utf-8 -*-
class Shape(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def area(self):
        print(self, "的面积为:", self.width * self.height)
    def grith(self):
        print(self, "的周长为:", self.width + self.height)
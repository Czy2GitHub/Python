# -*- coding:utf-8 -*-
from Circle import Circle
from Square import Square


if __name__ == '__main__':
    c = Circle(5)
    s = Square(7)
    c.area()
    c.girth()
    s.area()
    s.girth()
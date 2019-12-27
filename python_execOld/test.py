# -*- coding: utf-8 -*-
class Text:
    def __init__(self):
        print("Hello World")

class TextSon(Text):
    def __init__(self):
        Text.__init__(self)



if __name__ == "__main__":
    t = TextSon()
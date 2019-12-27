# -*- coding: utf-8 -*-
import turtle
turtle.pen()
turtle.width(5)

turtle.penup()
turtle.goto(-125, 0)      #第一个圆
turtle.pendown()
turtle.color("Blue")    #改颜色
turtle.circle(50)


turtle.penup()
turtle.goto(0, 0)        #第二个圆
turtle.pendown()
turtle.color("Black")
turtle.circle(50)

turtle.penup()
turtle.goto(125, 0)      #第三个圆
turtle.pendown()

turtle.color("Red")
turtle.circle(50)

turtle.penup()
turtle.goto(-62.5, -50)    #第四个圆
turtle.pendown()
turtle.color("Yellow")
turtle.circle(50)
turtle.penup()
turtle.goto(62.5, -50)
turtle.pendown()
turtle.color("Green")
turtle.circle(50)

import turtle
import os

os.environ["DISPLAY"] = "0"

screen = turtle.Screen()

t = turtle.Turtle()

t.forward(100)
t.right(90)
t.forward(50)
t.left(90)
t.backward(30)

turtle.done()

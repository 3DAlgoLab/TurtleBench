import subprocess
import os
from math import *
import utils.rabbit as rabbit

import turtle
turtle.pensize(5)
turtle.hideturtle()
t = turtle.Turtle()
t.pensize(5)
t.hideturtle()
t.pensize(3)
t.color('blue')
t.forward(100)
t.right(90)
t.forward(50)
turtle.done()
# Create/ensure screen exists before calling tracer
screen = turtle.Screen() if not hasattr(turtle, '_screen') or turtle._screen is None else turtle._screen
turtle.tracer(0, 0)
turtle.update()

# Get canvas and save
canvas = screen.getcanvas()
canvas.postscript(file='ps_file.ps', colormode='color')

# Convert the PostScript file to JPEG
jpg_file = os.path.join(f"/tmp/tmpf8oq15ef", f"test_final.jpg")
from PIL import Image
img = Image.open('ps_file.ps')
img.save(jpg_file, 'JPEG', quality=95)

# Clean up
screen.bye()
os.remove('ps_file.ps')
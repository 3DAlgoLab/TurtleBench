import subprocess
import os
import turtle
turtle.tracer(0, 0)
from math import *
import utils.rabbit as rabbit
import turtle
turtle.pensize(5)
turtle.hideturtle()
t = turtle.Turtle()
t.pensize(5)
t.hideturtle()
t.forward(100)
t.right(90)
t.forward(50)
turtle.done()
turtle.update()
wn = turtle.Screen()
canvas = wn.getcanvas()
canvas.postscript(file='ps_file.ps', colormode='color')
# Convert the PostScript file to PNG using ImageMagick
jpg_file = os.path.join(f"/tmp/tmp7tu2wl3t", f"test_fixed.jpg")
#subprocess.run(['magick', 'ps_file.ps', jpg_file])
from PIL import Image
img = Image.open('ps_file.ps')
img.save(jpg_file, 'JPEG', quality=95)
wn.bye()
os.remove('ps_file.ps')
from svg_turtle import SvgTurtle

t = SvgTurtle(800, 600)  # Width, height in pixels
# Your drawing code here...
t.forward(100)
t.left(90)
# ...

t.save_as("drawing.svg")  # Or convert SVG to PNG with other tools

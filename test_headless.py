import tkinter
from turtle import RawTurtle, TurtleScreen
from PIL import Image  # pip install pillow if needed

# Create hidden root and canvas
root = tkinter.Tk()
root.withdraw()  # Hide the window
canvas = tkinter.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Set up turtle on the hidden canvas
screen = TurtleScreen(canvas)
t = RawTurtle(screen)
t.pencolor("blue")
t.pensize(3)

# Example drawing: a simple spiral
t.penup()
t.goto(0, 0)
t.pendown()
for i in range(100):
    t.forward(i * 2)
    t.left(90 + 10)

# Force drawing update
canvas.update()

# Save as PostScript (vector, captures full path)
eps_file = "drawing.eps"
canvas.postscript(file=eps_file, colormode="color")

# Convert to PNG with Pillow
img = Image.open(eps_file)
img.save("drawing.png", "PNG")

# Clean up
root.destroy()

print("Drawing saved as drawing.png")

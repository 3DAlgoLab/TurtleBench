try:
    from svg_turtle import SvgTurtle
    # Create wrapper class for SVG turtle compatibility
    class SVGRabbit(SvgTurtle):
        def __init__(self):
            super().__init__(800, 600)
            self.setheading(90)
            self.width(5)  # SVG turtle uses width() instead of pensize()
            # self.hideturtle()  # Not available in SVG turtle

        def aa(self, length):
            self.forward(length)

        def bb(self, degree):
            self.right(degree)

        def cc(self, radius, degree):
            self.circle(radius, degree)

        def pp(self, vanish):
            if vanish:
                self.penup()
            else:
                self.pendown()
    
    Rabbit = SVGRabbit
except ImportError:
    import turtle
    import math
    
    class Rabbit(turtle.Turtle):
        def __init__(self):
            super().__init__()
            self.setheading(90)
            self.pensize(5)
            self.hideturtle()

        def aa(self, length):
            self.forward(length)

        def bb(self, degree):
            self.right(degree)

        def cc(self, radius, degree):
            self.circle(radius, degree)

        def pp(self, vanish):
            if vanish:
                self.penup()
            else:
                self.pendown()

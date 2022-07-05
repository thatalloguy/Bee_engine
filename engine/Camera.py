from engine.Window import *
from tkinter import *

canvas = Bee.return_canvas(None)


class Camera:
    def __init__(self):
        global canvas
        self.x = 0
        self.y = 0
        self.canvas = canvas

    def move_x(self,amount):
        self.canvas.xview_scroll(amount, "units")
        self.x += amount

    def move_y(self,amount):
        self.canvas.yview_scroll(amount, "units")
        self.y += amount
    def zoom_in(self,x,y):
        self.canvas.scale("all", x, y, 1.1, 1.1)

    def zoom_out(self,x,y):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)

    def get_loc(self):
        return self.x, self.y
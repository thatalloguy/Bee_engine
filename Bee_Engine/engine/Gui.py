from engine.Logger import *
from tkinter import *
import time, os, sys
import pymunk
from playsound import playsound
from PIL import Image,ImageTk
from engine.Window import *

_window = Bee.return_window(None)
_canvas = Bee.return_canvas(None)

class Gui:
    def __init__(self,x,y,color=None,text=None,entry=None,button=None,bt=None,command=None):
        self.bt = bt
        self.command = command
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.entry = entry
        self.button = button

    def draw(self):
        if self.text != None:
            if self.color != None:
             self.shaper = _canvas.create_text(self.x,self.y,text=self.text,fill=self.color)
        if self.entry == True:
            self.shaper = Entry(_canvas, bd=5)
            _canvas.create_window(self.x, self.y, window=self.shaper)
        if self.button == True:
            self.shaper = Button(_canvas,text=self.bt, command=self.command)
            _canvas.create_window(self.x, self.y, window=self.shaper)


    def undraw(self):
        _canvas.delete(self.shaper)


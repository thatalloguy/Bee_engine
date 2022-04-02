from bee_engine.logger import *
from tkinter import *
import time, os, sys

__version__ = "0.1"


_window = Tk()
_canvas = Canvas(_window)
_debug = True
_update = time.time()


max_width = _window.winfo_screenwidth()
max_height = _window.winfo_screenheight()
_canvas = Canvas(_window, width=int(max_width), height=int(max_height))
_canvas.pack()


class Bee:
    def __init__(self,width,height,title=None,icon=None,resizable=None,fullscreen=None,no_window_bar=None):
        Logger.send_info(self, "initializing the window", _debug)
        self.width = width
        self.height = height
        self.size = str(self.width) + "x" + str(self.height)
        _window.geometry(self.size)
        self.title = title
        self.icon = icon
        self.no_win = no_window_bar
        _window.overrideredirect(self.no_win)
        self.fullscreen = fullscreen
        _window.attributes("-fullscreen", self.fullscreen)
        self.resizable = resizable
        ############################################################
        if self.fullscreen == True:
            #self.max_width = _window.winfo_screenwidth()
            #Logger.send_info(self, str(self.max_width), _debug)
            self.max_height = _window.winfo_screenheight()
            Logger.send_info(self, str(self.max_height), _debug)
            #_canvas = Canvas(_window, width=int(self.max_width), height=int(self.max_height), bg="black").pack()
        else:
            _canvas = Canvas(_window,width=self.width,height=self.height,bg="black").pack()
        ############################################################
        ############SETTINGS
        if self.resizable == False:
            _window.resizable(False, False)
            Logger.send_info(self, "Disabled Resizing", _debug)
        else:
            _window.resizable(True, True)
            Logger.send_info(self, "Enabeld Resizing", _debug)
        if self.icon == None:
            pass
        else:
            _window.iconbitmap(icon)
            Logger.send_info(self, "Setting up the Icon", _debug)
        if title == None:
            Logger.send_info(self, "Using default the title", _debug)
            _window.title("A Bee Window")
        else:
            Logger.send_info(self, "Using an custom title", _debug)
            _window.title(self.title)



    def fullscreen(self, full):
        Logger.send_info(self, "FULLSCREEN TOGGELD", _debug)
        self.full = full
        _window.attributes("-fullscreen", self.full)

    def config(self,color=None):
        self.color = color
        _canvas.configure(bg=self.color)

    def update(self):
        Logger.send_info(self, "Mainloop: TRUE", _debug)
        _window.mainloop()

    def wait(self, command, tick):
        self.command = command
        self.tick = tick
        _window.after(self.tick, self.command)


class Entity:
    def __init__(self,id,x,y,size,shape=None,color=None,path=None):
        global _canvas
        self.path = path
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.shape = shape
        self.color = color
        self.c =  _canvas

    def draw(self):
        self.x2 = self.x + self.size
        self.y2 = self.y + self.size

        if self.shape == "image":
            if self.path != None:
                self.image = PhotoImage(master=_canvas, file=self.path, width=self.size, height=self.size)
                self.shaper = _canvas.create_image(self.x, self.y, image=self.image)
            else:
                Logger.send_error(self, "-Path is missing!", _debug)
        else:
            if self.shape == None:
                Logger.send_error(self, "-Shape is missing!", _debug)
            if self.color == None:
                Logger.send_error(self, "-Colour is missing!", _debug)
            else:
                if self.shape == "rectangle":
                    self.shaper = _canvas.create_rectangle(self.x, self.y, self.x2, self.y2, fill=self.color)
                elif self.shape == "circle":
                    self.shaper = _canvas.create_oval(self.x, self.y, self.x2, self.y2, fill=self.color)
                elif self.shape == "line":
                    self.shaper = _canvas.create_line(self.x, self.y, self.x2, self.y2,fill=self.color)

        #_canvas.delete(self.shaper)

    def getid(self):
        return self.id

    def undraw(self):
        _canvas.delete(self.shaper)

    def move(self,x,y):
        _canvas.move(self.shaper, x, y)

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

##############################
def bind(evnt,command):
    _window.bind(evnt,command)
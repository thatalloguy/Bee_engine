from bee_engine.logger import *
from tkinter import *
import time, os, sys
import pymunk
from playsound import playsound
from PIL import Image,ImageTk
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

    def wipe(self):
        _canvas.delete("all")


class Entity:
    def __init__(self,id,x,y,size=None,shape=None,color=None,path=None,physicsless=None,mass=None,width=None,height=None):
        global _canvas
        self.physicsless = physicsless
        self.mass = mass
        self.path = path
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.shape = shape
        self.color = color
        self.c =  _canvas
        self.width = width
        self.height = height

        ########PHYSICS STUFF###########
        if not self.physicsless:
            if self.mass != None:
                self.body = pymunk.Body()
                self.body.position = self.x,self.y
        elif self.physicsless == None:
            if self.mass != None:
                Logger.send_error(self, "Cant use mass since the entity doesnt allow Physics")

    def draw(self):
        if self.shape == "image":
            if self.path != None:
                self.image = (Image.open(self.path))
                self.resized = self.image.resize((self.width,self.height), Image.ANTIALIAS)
                self.shaper = ImageTk.PhotoImage(self.resized)
            else:
                Logger.send_error(self, "-Path is missing!", _debug)
        else:
            if self.size == None:
                Logger.send_error(self, "-Size is missing!", _debug)
            if self.shape == None:
                Logger.send_error(self, "-Shape is missing!", _debug)
            if self.color == None:
                Logger.send_error(self, "-Colour is missing!", _debug)
            else:
                self.x2 = self.x + self.size
                self.y2 = self.y + self.size
                if self.shape == "rectangle":
                    self.shaper = _canvas.create_rectangle(self.x, self.y, self.x2, self.y2, fill=self.color)
                elif self.shape == "circle":
                    self.shaper = _canvas.create_oval(self.x, self.y, self.x2, self.y2, fill=self.color)
                elif self.shape == "line":
                    self.shaper = _canvas.create_line(self.x, self.y, self.x2, self.y2,fill=self.color)

        #_canvas.delete(self.shaper)

    def getid(self):
        return self.id

    def get_object(self):
        return self.shaper

    def get_x(self):
        return _canvas.coords(self.shaper)[0]

    def get_y(self):
        return _canvas.coords(self.shaper)[1]

    def undraw(self):
        _canvas.delete(self.shaper)

    def move(self,x,y):
        _canvas.move(self.shaper, x, y)

    def collided_with(self, target):
        a = _canvas.bbox(self.shaper)
        b = _canvas.bbox(target)
        if b[0] in range(a[0], a[2]) or b[2] in range(a[0], a[2]) and b[1] in range(a[1], a[3]) or b[3] in range(a[1],a[3]):
            return True

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



class Space:
    def __init__(self,gravity,debug):
        self.debug = debug
        self.gravity = gravity
        self.space = pymunk.space()
        self.space.gravity = self.gravity

    def add(self,body, poly):
        self.body = body
        self.poly = poly
        self.space.add(self.body,self.poly)



class Musicman:
    def __init__(self):
        pass
    def play(self, sound):
        self.sound = sound
        playsound(self.sound)


##############################
def bind(evnt,command):
    _window.bind(evnt,command)

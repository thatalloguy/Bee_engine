from engine.Logger import *
from tkinter import *
import time, os, sys
import pymunk
from playsound import playsound
from PIL import Image,ImageTk

_window = None
_canvas = None
_debug = True
_update = time.time()
import time

start_time = time.time()
fp = 0.001 # displays the frame rate every 1 second
counter = 0
#max_width = _window.winfo_screenwidth()
#max_height = _window.winfo_screenheight()
#_canvas = Canvas(_window, width=int(max_width), height=int(max_height))
#_canvas.pack()

class Bee:
    def __init__(self,width,height,title=None,icon=None,bg=None,resizable=None,fullscreen=None,no_window_bar=None,window=None,canvas=None):
        global _window, _canvas, max_height, max_width
        if window == None:
            print("sss")
            _window = Tk()
            _window.geometry((str(width) + "x" + str(height)))
        else:
            _window = window
        if canvas == None:
            print("HELLO")
            _canvas = Canvas(_window, width=width, height=height,bg="black")
            _canvas.pack()
        else:
            _canvas = canvas
        Logger.send_info(self, "initializing the window", _debug)
        self.width = width
        self.height = height
        self.size = str(self.width) + "x" + str(self.height)
        #_window.geometry(self.size)
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
            pass
            #_canvas = Canvas(_window,width=self.width,height=self.height,bg="black").pack()
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

    def updater(self):
        global counter, fp, start_time
        ######### Everything what is written in this function happens every second!!! ##########
        counter += 1
        if (time.time() - start_time) > fp:
            print("BEE EDTIOR " + "FPS: " + str(counter / (time.time() - start_time)))
            counter = 0
            start_time = time.time()
        _window.after(1, self.updater)

    def update(self):
        Logger.send_info(self, "Mainloop: TRUE", _debug)
        #self.updater()
        _window.mainloop()

    def wait(self, command, tick):
        self.command = command
        self.tick = tick
        _window.after(self.tick, self.command)

    def wipe(self):
        _canvas.delete("all")

    def return_window(self):
        return _window


    def return_canvas(self):
        return _canvas


    def return_debug(self):
        return _debug
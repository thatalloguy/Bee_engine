from engine.Logger import *
from tkinter import *
import time, os, sys
import pymunk
from playsound import playsound
from PIL import Image,ImageTk
from engine.Window import *

_window = Bee.return_window(None)
_canvas = Bee.return_canvas(None)

class Space:
    def __init__(self,gravity,time):
        #self.debug = debug
        self.time = time
        self.gravity = gravity
        self.lists = []
        self.space = pymunk.Space()
        self.space.gravity = self.gravity
        self.ticker()


    def add_entity(self, entity):
        self.lists.append(entity)
        self.space.add(entity.body, entity.poly)

    def add(self,body, poly):
        self.body = body
        self.poly = poly
        self.space.add(self.body,self.poly)

    def update(self, time_between_step):
        self.time = time_between_step
        self.space.step(self.time)

    def ticker(self):
        self.space.step(self.time)
        for i in self.lists:
            i.draw()
        Bee.wait(self, self.ticker, 1)

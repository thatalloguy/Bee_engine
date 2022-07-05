from engine.Logger import *
from tkinter import *
import time, os, sys
from PIL import Image,ImageTk
from math import sin, cos
from engine.Window import *



class Particle:
    def __init__(self,window,canvas,id,type,x,y,radius,delay,lifespan,degree,shape,width,height,color,amount,animation_type,speed,path=None):
        global _canvas, _window
        self.animation_type = animation_type
        self.c = canvas
        self.path = path
        self.speed = speed
        self.win = window
        self.id = id
        self.amount = amount
        self.type = type
        self.or_degree = degree
        self.x = x
        self.y = y
        self.radius = radius
        self.delay = delay
        self.lifespan = lifespan
        self.degree = degree
        self.shape = shape
        self.width = width
        self.height = height
        self.color = color
        self.particles = []
        self.renderd = False
        if self.shape == "image" and self.path == None:
            Logger.send_error(self, "Please specify -path", True)
        try:
            self.__draw()

            self.__animation()
        except:
            pass


    def __draw(self):
        print("DRAWING")
        if self.type == "tangential":
            #print("HELP ME")
            self.rounds = round(self.degree / 360)
            for i in range(self.amount):#self.rounds):
                #print("HELLO DEATH")
                self.x1 = self.x + self.radius * cos(self.degree)
                self.y1 = self.y + self.radius * sin(self.degree)
                if self.shape == "rectangle":
                    #print("DRWAING")
                    self.shaper = self.c.create_rectangle(self.x1, self.y1, self.x1 + self.width, self.y1 + self.height,fill=self.color)
                    self.particles.append(self.shaper)
                elif self.shape == "circle":
                    self.shaper = self.c.create_oval(self.x1, self.y1, self.x1 + self.width, self.y1 + self.height,fill=self.color)
                    self.particles.append(self.shaper)

                self.degree += self.or_degree

                #time.sleep(0.1)
                self.win.update()
        elif self.type == "radial":
            # print("HELP ME")
            self.rounds = round(self.degree / 360)
            for i in range(self.amount):  # self.rounds):
                # print("HELLO DEATH")
                self.x1 = self.x + self.radius * cos(self.degree)
                self.y1 = self.y + self.radius * sin(self.degree)
                if self.shape == "rectangle":
                    # print("DRWAING")
                    self.shaper = self.c.create_rectangle(self.x1, self.y1, self.x1 + self.width, self.y1 + self.height,
                                                          fill=self.color)
                    self.particles.append(self.shaper)
                elif self.shape == "circle":
                    self.shaper = self.c.create_oval(self.x1, self.y1, self.x1 + self.width, self.y1 + self.height,
                                                     fill=self.color)
                    self.particles.append(self.shaper)
                elif self.shape == "image":
                    #print("IMAGGE")
                    self.image = (Image.open(self.path))
                    self.resized = self.image.resize((self.width, self.height))
                    self.imager = ImageTk.PhotoImage(self.resized)
                    self.shaper = self.c.create_image(self.x, self.y, image=self.imager)
                    self.particles.append(self.shaper)

                self.degree += self.or_degree

                # time.sleep(0.1)
                self.win.update()
        self.renderd = True

    def __animation(self):

        while self.renderd:
            time.sleep(self.delay)
            self.win.update()
            if self.type == "tangential":
                for i in self.particles:
                    self.degree += self.or_degree
                    self.x1 = self.x + self.radius * cos(self.degree)
                    self.y1 = self.y + self.radius * sin(self.degree)
                    self.c.moveto(i,self.x1,self.y1)
                    self.win.update()
                    time.sleep(0.001)
            elif self.type == "radial":
                if self.animation_type == "out":
                    for i in self.particles:
                        self.x1 = self.x + self.radius * cos(self.degree)
                        self.y1 = self.y + self.radius * sin(self.degree)
                        self.c.moveto(i, self.x1, self.y1)
                        self.win.update()
                        time.sleep(0.001)
                        self.radius += self.speed
                        self.degree += self.or_degree
                elif self.animation_type == "in":
                    for i in self.particles:
                        self.x1 = self.x + self.radius * cos(self.degree)
                        self.y1 = self.y + self.radius * sin(self.degree)
                        self.c.moveto(i, self.x1, self.y1)
                        self.win.update()
                        time.sleep(0.001)
                        self.radius -= self.speed
                        self.degree -= self.or_degree

    def set_radius(self,radius):
        self.radius = radius


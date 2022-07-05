from engine.Logger import *
from tkinter import *
import time, os, sys
import pymunk
from playsound import playsound
from PIL import Image,ImageTk
from engine.Scene import *
from engine.Window import *

frame = 0

_window = Bee.return_window(None)
_debug = Bee.return_debug(None)
#_canvas = Bee.return_canvas(None)

class Entity(object):
    def __init__(self,id=int,name="",x=int,y=int,shape=None,layer=None,color=None,path=None,physicsless=None,mass=None,width=None,height=None,tags=None,per_scene=None,scene=None):
        global _window
        self._canvas = Bee.return_canvas(self)
        self.c = self._canvas
        self.name = name
        self.physicsless = physicsless
        self.tags = tags
        self.mass = mass
        self.path = path
        self.scene = scene
        self.id = id
        self.x = x
        self.y = y
        self.ps = per_scene

        self.shape = shape
        self.color = color
        self.c =  self._canvas
        self.width = width
        self.c_s = None
        self.height = height
        self.renderd = False
        self.layer = layer

        self.scripts = []

        Logger.send_info(self,("Created Entity named " + self.name),_debug)

        if self.scene == None or self.ps == None:
            Logger.send_error(self, "Missing -Scene or -Per_Scene Option", True)
            # its an critical error so it stops the process
            quit()
            pass
        self.c_s = self.scene.get_current_scene()

        #self.draw()
        print("ELLO")


        self.list_of_animations = []
        self.current_frame = 0

        self.draw()

        if self.layer == "top":
            self.c.tag_raise(self.shaper)
        elif self.layer == "bottom":
            self.c.tag_lower(self.shaper)
        elif self.layer == None:
            Logger.send_info(self, "Not using any Layer for: " + self.name, _debug)
        else:
            Logger.send_error(self, "Not an Supported layer please use -bottom or -top", _debug)



    def add_script(self,scriptname,password):
        self.scriptname = scriptname
        self.password = password

        if self.password != "EDITOR":
            Logger.send_error(self, "ONLY THE EDITOR CAN USE THIS FUNCTION")
        else:
            self.scripts.append(self.scriptname)

    def return_all_scripts(self, password):
        self.password = password

        if self.password != "EDITOR":
            Logger.send_error(self, "ONLY THE EDITOR CAN USE THIS FUNCTION")
        else:
            return self.scripts


    def play_animation(self, animation_names, delay):
        self.framer(animation_names)
        self.c.after(delay, lambda: self.play_animation(animation_names, delay))

    def set_layer(self, layer=""):
        pass


    def draw(self):
        print("Current Scene: " + str(self.c_s))
        if self.ps == self.c_s:
            #print("HEY")
            ########PHYSICS STUFF###########
            if self.renderd == False:
                try:
                    self.c.delete(self.shaper)
                except:
                    pass
               # self.renderd = True
                if self.shape == "image":
                    if self.path != None:
                        if self.width != None:
                            if self.height != None:
                                if _debug == True:
                                    print("Info: drawing image")
                                self.image = (Image.open(self.path))
                                self.resized = self.image.resize((self.width, self.height))
                                self.imager = ImageTk.PhotoImage(self.resized)
                                self.shaper = self._canvas.create_image(self.x, self.y, image=self.imager,tags=str(self.id))
                            else:
                                Logger.send_error(self, "-Height is missing!", _debug)
                        else:
                            Logger.send_error(self, "-Width is missing!", _debug)
                    else:
                        Logger.send_error(self, "-Path is missing!", _debug)



                else:
                    if self.shape == None:
                        Logger.send_error(self, "-Shape is missing!", _debug)
                    if self.color == None:
                        Logger.send_error(self, "-Colour is missing!", _debug)
                    else:
                        self.x2 = self.x + self.width
                        self.y2 = self.y + self.height
                        if self.shape == "rectangle":
                            self.c = Bee.return_canvas(self)
                            self.shaper = self.c.create_rectangle(self.x, self.y, self.x2, self.y2, fill=self.color,tags=str(self.id))
                        elif self.shape == "circle":
                            self.shaper = self.c.create_oval(self.x, self.y, self.x2, self.y2, fill=self.color,tags=str(self.id))
                        elif self.shape == "line":
                            self.shaper = self.c.create_line(self.x, self.y, self.x2, self.y2, fill=self.color,tags=str(self.id))
                if not self.physicsless:
                    if self.mass != None:
                        if self.shape == "image":
                            self.body = pymunk.Body()
                            self.body.position = self.x, self.y
                            #Genaration of the Poly vertices
                            self.vertices = [(-self.width/2,-self.height/2), (self.width/2,-self.height/2), (self.width/2,self.height/2), (-self.width/2,self.height/2)]
                            self.poly = pymunk.Poly(self.body, self.vertices)
                            self.poly.mass = self.mass

                        else:
                            Logger.send_error(self, "Entities without the shape :image: arent supported", _debug)
                elif self.physicsless == None:
                    if self.mass != None:
                        Logger.send_error(self, "Cant use mass since the entity doesnt allow Physics", _debug)
            elif self.renderd == True:
                try:
                    self.c.delete(self.shaper)
                    self.image = (Image.open(self.path))
                    self.resized = self.image.resize((self.width, self.height))
                    self.imager = ImageTk.PhotoImage(self.resized)
                    self.shaper = self.c.create_image(self.body.position.x, self.body.position.y, image=self.imager,tags=str(self.id))
                except:
                    pass
        else:
            try:
                pass
                #
            except:
                pass

            #Logger.send_info(self, "Entity cant render because of current scene isnt his", True)



        #self.c.delete(self.shaper)

    def resize(self,x,y,width,height):
        self.undraw()
        #update the posistion
        self.x = x
        self.y = y
        #oh no im to lazy
        if self.shape == "image":
            self.c.delete(self.shaper)
            self.image = (Image.open(self.path))
            self.resized = self.image.resize((width, height))
            self.imager = ImageTk.PhotoImage(self.resized)
            self.shaper = self.c.create_image(x, y, image=self.imager,
                                              tags=str(self.id))
        #UE5
        elif self.shape == "rectangle":
            self.x2 = self.x + width
            self.y2 = self.y + height
            self.shaper = self._canvas.create_rectangle(self.x,self.y,self.x2,self.y2,fill=self.color,tags=str(self.id))
        elif self.shape == "circle":
            self.x2 = self.x + width
            self.y2 = self.y + height
            self.shaper = self._canvas.create_oval(self.x,self.y,self.x2,self.y2,fill=self.color,tags=str(self.id))
        elif self.shape == "line":
            self.x2 = self.x + width
            self.y2 = self.y + height
            self.shaper = self._canvas.create_line(self.x,self.y,self.x2,self.y2,fill=self.color,tags=str(self.id))

    def get_body(self):
        return self.body

    def get_poly(self):
        return self.poly

    def getid(self):
        return self.id

    def get_object(self):
        return self.shaper

    def get_x(self):
        return self.c.coords(self.shaper)[0]

    def get_y(self):
        return self.c.coords(self.shaper)[1]

    def get_x_origin(self):
        return self.x
    def get_y_origin(self):
        return self.y

    def change_per_scene(self,scene):
        self.scene = scene
        self.draw()

    def get_per_scene(self):
        return self.ps

    def get_name(self):
        return self.name

    def change_name(self,name):
        self.name = name

    def undraw(self):
        self.c.delete(self.shaper)

    def move(self,x,y):
        self.c.move(self.shaper, x, y)

    def move_to(self, x, y):
        self.c.moveto(self.shaper, x, y)

    def collided_with(self, target):
        try:
            self.c.delete(a)
            self.c.delete(b)
        except:
            pass
        self.a = self.c.bbox(self.shaper)
        self.b = self.c.bbox(target)
        if self.b[0] in range(self.a[0], self.a[2]) or self.b[2] in range(self.a[0], self.a[2]) and self.b[1] in range(self.a[1], self.a[3]) or self.b[3] in range(self.a[1],self.a[3]):
            return True

    def framer(self, image):
        global frame
        if self.shape == "image":
            try:
                self.images = PhotoImage(file=image, format=("gif -index " + str(frame)))
                self.c.itemconfig(self.shaper,image=self.images)
                frame += 1
            except:
                frame = 0
                return True

            #_window.update()
        else:
            Logger.send_error(self, "Cant change image if shape isnt an image", _debug)

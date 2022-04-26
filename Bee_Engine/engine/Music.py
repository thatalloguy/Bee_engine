from engine.Logger import *
from tkinter import *
import time, os, sys
import pymunk
from playsound import playsound
from PIL import Image,ImageTk

class Musicman:
    def __init__(self):
        pass
    def play(self, sound):
        self.sound = sound
        playsound(self.sound)

from tkinter import filedialog
from customtkinter import *
from tkinter import *
import customtkinter
from pypresence import Presence
import time
import settings
from PIL import Image, ImageTk
from tkinter import ttk

def log(msg):
    print("LOGGER: " + msg)


class Launcher:
    def __init__(self):
        if settings.RICH_PRESENCE == True:
            log("setting up richpresence")
            self.rpc = Presence("963488657745014794")
            self.rpc.connect()
            self.rpc.update(state="Using Bee Launcher", large_image="launcher",
                            start=time.time())
        log("setting up the window")
        self.root = CTk()
        self.root.title("Bee launcher")
        #self.entity_list_frame = CTkFrame(self.root)
        #self.entity_list_frame.place(x=200, y=155)
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.icon = PhotoImage(file='engine/images/icon/launcher.png')
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.icon)
        #self.root.resizable(False,False)
        self.root.geometry("900x500")
        self.c = Canvas(self.root,width=900,height=150,bg="gray")
        self.c.pack()
        self.create_splash()
        self.create_buttons()
        log("Window setup is done")

        #self.root.bind("<Button-1>", self.awd)

    def open_project(self):
        self.file = filedialog.askopenfile(defaultextension=".py", filetypes=[("Python Files", "*.py*")])

        self.c.destroy()
        self.root.destroy()
        from Editor import Editor
        self.ed = Editor(self.file)
        self.ed.tick()
        self.ed.mainloop()

    def create_buttons(self):
        log("getting image path")
        self.play_image = PhotoImage(file="engine/images/icon/create.png")
        self.create_button = customtkinter.CTkButton(master=self.root,image=self.play_image, text="", border_color="blue",text_color="white", fg_color="green", hover_color="lime",width=50,height=25)
        self.create_button.place(x=265,y=300)
        log("getting image path")
        self.open_image = PhotoImage(file="engine/images/icon/open.png")
        self.open_button = customtkinter.CTkButton(master=self.root, command=self.open_project,image=self.open_image, text="", border_color="blue", text_color="white", fg_color="blue",hover_color="cyan", width=50, height=25)
        self.open_button.place(x=550, y=300)


    def create_splash(self):
        log("getting image path")
        self.image = (Image.open("engine/images/icon/splash.png"))
        log("Creating splash")
        self.resized = self.image.resize((900, 150))
        self.imager = ImageTk.PhotoImage(self.resized)
        self.shaper = self.c.create_image(450, 72, image=self.imager)



    def mainloop(self):
        log("Mainloop is now enabled")
        self.root.mainloop()

if __name__ == "__main__":
    win = Launcher()
    win.mainloop()
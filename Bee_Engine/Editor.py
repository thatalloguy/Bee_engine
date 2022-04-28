from engine import *
import tkinter
import customtkinter
import settings
from pypresence import Presence
import tkinter.filedialog
from engine.Scene import *
import time
import numpy as np
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkcode import CodeEditor




start_time = time.time()
fp = 0.001 # displays the frame rate every 1 second
counter = 0
#abel.pack()
###########################################################################
class Ecs:
    def __init__(self,writer,canvas):
        self.entities_id = []
        self.entities = []
        self.entities_x = []
        self.entities_y = []
        self._canvas = canvas
        self.writer = writer

    def add(self,entity):
        self.id = entity.getid()
        self.name = entity.name
        self.entities.append(entity)
        Logger.send_info(self,(" ECS: added " + str(self.name) + " to Entity list"), True)
        self.entities_id.append(str(self.id))
        #print(str(self.entities_id))

    def get_all_id(self):
        return self.entities_id

    def get_entity(self,id):
        return self.entities[id]

    def get_all_entities(self):
        return self.entities


    def change(self, id, line):
        for i in self.entities:
            #print("oi" + str(i))
            #print("oi" + str(id))
            if str(id) == str(i):
               # print("IT WORKEd")

                self.writer.change(int(id), str(line))

    def get_closest(self,entity):
        self.tag = self._canvas.gettags(entity)
        self.id = self.tag[0]
        self.count = 0
        for i in self.entities_id:
            if str(self.id) == i:
                #print("MACTH1212")
                #print(str(self.count))
                self.entity = self.entities[self.count]
                #print(self.entity.get_name())
                return self.entity
            else:
                self.count += 1









class Writer:
    def __init__(self):
        self.file = ""
        self.game = []
        self.Add("from engine import *")
        if settings.FILE != "":
            self.file = settings.FILE

    def change(self, num, line):
        self.new_line = self.game[num] = line
        print(str(self.new_line))

    def check_Save(self):
        #self.Save()
        if self.file == "":
           self.files = [('Python Files', '*.py')]
           self.file = tkinter.filedialog.asksaveasfilename(defaultextension=".py", filetypes=[
                                      ("Bee Project", "*.py*")])
           print(str(self.file))
           self.Save()
        else:
           self.Save()
    def Add(self, line):
        self.line = line + '\n'
        self.game.append(str(self.line))

    def Save(self):
        for i in self.game:
            print(i)
            with open(self.file, 'w') as out:
                self.out = out.writelines(self.game)
                print(str(self.out))

    def Open(self, file):
        pass

    def get_file(self):
        return self.file

pressed = False


class Camera_Editor(Frame):
    def __init__(self, root, canvas):
        Frame.__init__(self, root)
        self.canvas = canvas
        self.xsb = Scrollbar(self, orient="horizontal",
                             command=self.canvas.xview)
        self.ysb = Scrollbar(self, orient="vertical",
                             command=self.canvas.yview)
##        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
##        self.canvas.configure(scrollregion=(0,0,1000,1000))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
##        self.canvas.grid(row=0, column=0, sticky="nsew")
##        self.grid_rowconfigure(0, weight=1)
##        self.grid_columnconfigure(0, weight=1)

        #Plot some rectangles


        #self.canvas.create_text(250, 250, anchor="nw", text="Click and drag to move the canvas\nScroll to zoom.")

        # This is what enables using the mouse:
        self.canvas.bind("<ButtonPress-2>", self.move_start)
        self.canvas.bind("<B2-Motion>", self.move_move)

##        self.canvas.bind("<ButtonPress-2>", self.pressed2)
        self.canvas.bind("<Motion>", self.move_move2)

        #linux scroll
        self.canvas.bind("<Button-4>", self.zoomerP)
        self.canvas.bind("<Button-5>", self.zoomerM)
        #windows scroll
        self.canvas.bind("<MouseWheel>", self.zoomer)
        # Hack to make zoom work on Windows
        root.bind_all("<MouseWheel>", self.zoomer)

    #move
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    #move
    def pressed2(self, event):
        global pressed
        pressed = not pressed
        self.canvas.scan_mark(event.x, event.y)

    def move_move2(self, event):
        if pressed:
            self.canvas.scan_dragto(event.x, event.y, gain=1)

    #windows zoom
    def zoomer(self, event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    #linux zoom
    def zoomerP(self, event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoomerM(self, event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class Editor:
    def __init__(self):
        ####DISCORD THINGY
        if settings.RICH_PRESENCE == True:
            self.rpc = Presence("963488657745014794")
            self.rpc.connect()
            self.rpc.update(state="Using Bee Engine",details="editing an project",large_image="bee",start=time.time())
        ###DA REST
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.root_tk = customtkinter.CTk()
        self.root_width = self.root_tk.winfo_screenwidth()
        self.root_height = self.root_tk.winfo_screenheight()
        self.create_canvas()
        game_root = Bee(self.root_width - 700, self.root_height, title="Game Engine", resizable=True, window=self.root_tk,
                        canvas=self._canvas)
        self.root_tk.geometry(str(self.root_width) + "x" + str(self.root_height))
        self.root_tk.title("Bee Editor")
        self.icon = PhotoImage(file='engine/images/bee1.png')
        self.root_tk.tk.call('wm', 'iconphoto', self.root_tk._w, self.icon)

        Camera_Editor(self.root_tk,self._canvas)

        ##################################################
        # setting up the layout
        self.entity_list_frame = customtkinter.CTkFrame(master=self.root_tk, width=250, height=(self.root_height - 100),
                                                   corner_radius=10)
        self.entity_list_frame.grid(row=1, column=0, padx=10, pady=20)
        self.entity_list_frame.grid_propagate(0)
        self.entity_info_frame = customtkinter.CTkFrame(master=self.root_tk, width=400, height=self.root_height - 100,
                                                   corner_radius=10)
        self.entity_info_frame.grid(row=1, column=2, padx=10, pady=20)
        self.entity_info_frame.grid_propagate(0)
        self.label = customtkinter.CTkLabel(master=self.root_tk,
                                       text="Hello World",
                                       width=120,
                                       height=25,
                                       fg_color=("white", "gray75"),
                                       corner_radius=8)
        ##########################################
        # SAVE

        self.writer = Writer()

        ##########################################
        self._Ecs = Ecs(self.writer,self._canvas)
        self._Scene = Scene(self._canvas)
        self._Scene.set_scene(0)
        self.entity_counter = 0
        ######### TEST ################
        self.entities = self._Ecs.get_all_id()
        print(self.entities)
        for i in self.entities:
            self.button = customtkinter.CTkButton(master=self.entity_list_frame, text=i.getid(),command=lambda: self.show_entity_info(i))
            self.button.pack(anchor=tkinter.NW,pady=10)
        self.last_entity = ""

        #MENU

        self.Save_button = customtkinter.CTkButton(master=self.root_tk,width=50, text="Menu",border_color="blue",text_color="white",fg_color="green",hover_color="gray",command=self.open_menu)
        self.Save_button.place(x=10,y=10)
        #self.test_button = customtkinter.CTkButton(master=self.root_tk, text="Create", border_color="blue",
                                                   #text_color="white", fg_color="green", hover_color="gray", command=self.test)
        #self.test_button.place(x=10, y=50)
        self.play_image = PhotoImage(file="engine/images/play.png")
        self.test_button = customtkinter.CTkButton(master=self.root_tk, text="Create", border_color="blue",
                                                   text_color="white", fg_color="green", hover_color="gray",
                                                   command=self.test,width=50)
        self.play_button = customtkinter.CTkButton(master=self.root_tk,image=self.play_image, text="", border_color="blue",
                                                   text_color="white", fg_color="green", hover_color="gray",
                                                   command=self.play,width=50,height=25)
        self.play_button.place(x=125, y=10)
        self.test_button.place(x=65, y=10)
        self._canvas.bind("<B1-Motion>", self.onObjectClick)


        ##### TREEVIEW
        #create the tree view
        self.tree = self.create_tree_widget()

    def create_tree_widget(self):
        style = ttk.Style(self.entity_list_frame)
        # set ttk theme to "clam" which support the fieldbackground option
        style.theme_use("clam")
        style.configure("Treeview", background="black",
                        fieldbackground="light gray", foreground="white")
        self.columns = ('first_name', 'last_name', 'email')
        self.tree = ttk.Treeview(self.entity_list_frame, columns=self.columns, show='headings',height=self.root_height - 10)

        # define headings
        self.tree.heading('first_name', text='Entity')
        self.tree.heading('last_name', text='Id')
        #self.tree.heading('email', text='Email')

        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        self.tree.grid(row=0, column=0, sticky=NSEW)

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self.entity_list_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        # generate sample data
        self.contacts = []
        #for n in range(1, 100):
        #    self.contacts.append((f'first {n}', f'last {n}'))

        #for contact in self.contacts:
        #    self.tree.insert('', END, values=contact)

        return self.tree

    def item_selected(self, event):
        for selected_item in self.tree.selection():
            self.item = self.tree.item(selected_item)
            self.record = self.item['values']
            # show a message
            #showinfo(title='Information', message=','.join(str(self.record)))
            #for i in self.record:
            #    print(str(i))
            #    if i.isdigit():
            #        i = int(i)
            #        self.list_entity = self._Ecs.get_entity(i)
            #        self.edit_en



    def tree_refresh(self):
        self.tree.delete(*self.tree.get_children())
        self.list = self._Ecs.get_all_id()
        #print(str(self.list))
        for entity in self.list:
            entity = int(entity)
            #print(str(entity))
            self.tree_bob = self._Ecs.get_entity(entity - 1)
            contact = (self.tree_bob.name, str(self.tree_bob.id))
            self.tree.insert('', END, values=contact)


    def test(self):
        self.bob = Entity(1,"bob",250,250,width=50,height=50,shape="rectangle",color="green",per_scene=0,scene=self._Scene)
        self.bob.draw()
        self._Ecs.add(self.bob)
        self.writer.check_Save()
        self.writer.Add("1")
        self.bob_id = self.bob.getid()
        self._Ecs.change(self.bob_id, "IT WORKED BABBYY")


    def onObjectClick(self, event):
        #print('Clicked', event.x, event.y, event.widget)
        colest = event.widget.find_closest(event.x, event.y)
        self._canvas.moveto(colest, event.x, event.y)
        self.result = self._Ecs.get_closest(colest)
        self.edit_entity(colest,self.result)

    def open_menu(self):
        self._canvas.config(width=0, height=0)
        self.menu_frame = customtkinter.CTkFrame(master=self.root_tk, width=self.root_width - 400,
                                                            height=self.root_height - 100,
                                                            corner_radius=10)
        ####LAYOUT#########
        self.menu_frame.grid(row=1, column=1)
        self.menu_frame.grid_propagate(0)

        self.save_button = customtkinter.CTkButton(master=self.menu_frame, text="Save", border_color="black",border_width=4,text_color="black", fg_color="lime", command=self.writer.Save)
        self.save_button.place(x=10,y=10)
        self.save_as_button = customtkinter.CTkButton(master=self.menu_frame, text="Save As", border_color="black",
                                                   border_width=4, text_color="black", fg_color="lime",
                                                   command=self.writer.check_Save)
        self.save_as_button.place(x=140, y=10)
        self.open_button = customtkinter.CTkButton(master=self.menu_frame, text="Open", border_color="black",
                                                      border_width=4, text_color="black", fg_color="lime",
                                                      command=self.writer.check_Save)
        self.open_button.place(x=280, y=10)
        self.settings_label = customtkinter.CTkLabel(master=self.menu_frame, text="Settings", fg_color="gray", text_color="white", width=350, height=90)
        self.settings_label.place(x=10, y=120)
        ##DA SETTINGS
        self.rich_switch = customtkinter.CTkSwitch(master=self.menu_frame, text="rich presence", onvalue="on", offvalue="off")
        self.rich_switch.place(x=10,y=260)
        self.place_holder_switch = customtkinter.CTkSwitch(master=self.menu_frame, text="place holder", onvalue="on",
                                                   offvalue="off")
        self.place_holder_switch.place(x=10, y=320)
        self.place_holder_switch = customtkinter.CTkSwitch(master=self.menu_frame, text="place holder", onvalue="on",
                                                           offvalue="off")
        self.place_holder_switch.place(x=10, y=380)
        self.place_holder_switch = customtkinter.CTkSwitch(master=self.menu_frame, text="place holder", onvalue="on",
                                                           offvalue="off")
        self.place_holder_switch.place(x=10, y=450)
        self.done_button = customtkinter.CTkButton(master=self.menu_frame, width=200, height=50,
                                                   text="Done", command=self.back_to_canvas)
        self.done_button.place(x=50, y=self.root_height - 200)

    def back_to_canvas(self):
        self.menu_frame.destroy()
        self._canvas.config(width=self.root_width - 700, height=self.root_height)

    def play(self):
        self.file = self.writer.get_file()
        try:
            if self.file == "":
                self.writer.Save()
            else:
                exec(self.file)
                Logger.send_info(self, "Starting game", True)
        except:
            self.writer.Save()


    def edit_entity(self, entity, Entity):
        #print(str(self.last_entity))

        self.scripts = []
        self.x_pos = round(self._canvas.coords(entity)[0])
        self.y_pos = round(self._canvas.coords(entity)[1])
        self.bounds = self._canvas.bbox(entity)  # returns a tuple like (x1, y1, x2, y2)
        self.width  = self.bounds[2] - self.bounds[0]
        self.height = self.bounds[3] - self.bounds[1]
        self.scene = Entity.get_per_scene()
        # SCRIPTS
        self.scripts_files = Entity.return_all_scripts("EDITOR")
        self.scripts.append(self.scripts_files)

        #print(self.width)
        #print(self.height)
        try:
            try:
                self.script_butto.destroy()
                self.place_y = 335
            except:
                pass
            #x
            self.x_entry.delete(0,END)
            self.x_entry.insert(0,str(self.x_pos))
            #Y
            self.y_entry.delete(0, END)
            self.y_entry.insert(0, str(self.y_pos))
            #width
            self.w_entry.delete(0, END)
            self.w_entry.insert(0, str(self.width))
            # height
            self.h_entry.delete(0, END)
            self.h_entry.insert(0, str(self.height))
            #name
            self.n_entry.delete(0, END)
            self.n_entry.insert(0, str(Entity.get_name()))
            # scene #to lazy to fix
            #self.s_entry.delete(0, END)
            #self.s_entry.insert(0, str(self.scene))

            #SCRIPT
            #for i in self.scripts:
            #    if str(i) != "[]":
            #        print(str(i))
            #        for j in i:
            #            print(str(j))
            #           self.name_script = str(j)
            #            self.name_script = self.name_script.replace("[", "")
            #            self.name_script = self.name_script.replace("]", "")
            #            self.name_script = self.name_script.replace("'", "")
            #            self.script_butto = customtkinter.CTkButton(master=self.entity_info_frame,
            ##                                                        text=self.name_script,
            #                                                        fg_color="blue", text_color="white")
            #            self.script_butto.place(x=0, y=self.place_y)
            #            self.script_butto.bind("<Button-1>",lambda: self.script_editor(self.script_butto.config('text')[-1]))
            #            self.place_y += 50

        except:
            pass

        if entity == self.last_entity:
            pass
        else:
            self.last_entity = entity
            self.entity_W = entity
            print(str(self.entity_W))

            self.x_label = customtkinter.CTkLabel(master=self.entity_info_frame,text="X",width=5,height=5,fg_color="gray",text_color="white",corner_radius=8)
            self.x_label.place(x=0,y=10)
            self.y_label = customtkinter.CTkLabel(master=self.entity_info_frame, text="Y", width=5, height=5,fg_color="gray", text_color="white", corner_radius=8)
            self.y_label.place(x=0, y=50)
            self.w_label = customtkinter.CTkLabel(master=self.entity_info_frame, text="Width", width=5, height=5,
                                                  fg_color="gray", text_color="white", corner_radius=8)
            self.w_label.place(x=0, y=90)
            self.h_label = customtkinter.CTkLabel(master=self.entity_info_frame, text="Height", width=5, height=5,
                                                  fg_color="gray", text_color="white", corner_radius=8)
            self.h_label.place(x=0, y=130)
            self.n_label = customtkinter.CTkLabel(master=self.entity_info_frame, text="Name", width=5, height=5,
                                                  fg_color="gray", text_color="white", corner_radius=8)
            self.n_label.place(x=0, y=170)
            #self.s_label = customtkinter.CTkLabel(master=self.entity_info_frame, text="Scene", width=5, height=5,
            #                                      fg_color="gray", text_color="white", corner_radius=8)
            #self.s_label.place(x=0, y=210)

            #self.r_label = customtkinter.CTkLabel(master=self.entity_info_frame, text="Rotation", width=5, height=5,
            #                                      fg_color="gray", text_color="white", corner_radius=8)
            #self.r_label.place(x=0, y=170)
            ####################################################################################################

            self.x_entry = customtkinter.CTkEntry(master=self.entity_info_frame, placeholder_text=str(self.x_pos))
            self.x_entry.place(x=30, y=5)

            self.x_button = customtkinter.CTkButton(master=self.entity_info_frame, text="Move", command=lambda: self._canvas.moveto(entity, int(self.x_entry.get()), int(self.y_entry.get())),fg_color="green", text_color="white")
            self.x_button.place(x=170, y=5)

            self.y_entry = customtkinter.CTkEntry(master=self.entity_info_frame, placeholder_text=str(self.y_pos))
            self.y_entry.place(x=30, y=45)

            self.y_button = customtkinter.CTkButton(master=self.entity_info_frame, command=lambda: self._canvas.moveto(entity, int(self.x_entry.get()), int(self.y_entry.get())),text="Move", fg_color="green",
                                                    text_color="white")
            self.y_button.place(x=170, y=45)

            self.w_entry = customtkinter.CTkEntry(master=self.entity_info_frame, placeholder_text=str(self.width))
            self.w_entry.place(x=50, y=85)

            self.w_button = customtkinter.CTkButton(master=self.entity_info_frame,command=lambda: self.edit_size(Entity,int(self.x_entry.get()),int(self.y_entry.get()),int(self.w_entry.get()),int(self.h_entry.get())),text="Change", fg_color="green",text_color="white")
            self.w_button.place(x=170, y=85)

            self.h_entry = customtkinter.CTkEntry(master=self.entity_info_frame, placeholder_text=str(self.height))
            self.h_entry.place(x=50, y=125)

            self.h_button = customtkinter.CTkButton(master=self.entity_info_frame,command=lambda: self.edit_size(Entity,int(self.x_entry.get()),int(self.y_entry.get()),int(self.w_entry.get()),int(self.h_entry.get())),text="Change", fg_color="green", text_color="white")
            self.h_button.place(x=170, y=125)

            self.n_entry = customtkinter.CTkEntry(master=self.entity_info_frame, placeholder_text=str(Entity.get_name()))
            self.n_entry.place(x=50, y=165)

            self.n_button = customtkinter.CTkButton(master=self.entity_info_frame,text="Change", fg_color="green", text_color="white",command=lambda: Entity.change_name(self.n_entry.get()))
            self.n_button.place(x=170, y=165)

            #self.s_entry = customtkinter.CTkEntry(master=self.entity_info_frame, placeholder_text=str(Entity.get_name()))
            #self.s_entry.place(x=50, y=205)

            #self.s_button = customtkinter.CTkButton(master=self.entity_info_frame, text="Change", fg_color="green",command=lambda: Entity.change_per_scene(int(self.s_entry.get())),text_color="white")
            #self.s_button.place(x=170, y=205)

            ##################################
            # SCRIPT

            self.script_label = customtkinter.CTkLabel(master=self.entity_info_frame, text="Scripts: ", width=100, height=40,fg_color="gray", text_color="white", corner_radius=8)
            self.script_label.place(x=0, y=280)

            self.script_entry = customtkinter.CTkEntry(master=self.entity_info_frame,placeholder_text="script name")
            self.script_entry.place(x=125, y=285)

            self.script_button = customtkinter.CTkButton(master=self.entity_info_frame, command=lambda: self.create_script(Entity,self.script_entry.get()),text="Add", fg_color="blue",text_color="white")
            self.script_button.place(x=250, y=285)

            self.place_y = 335
            self.tree_refresh()

            ## SCRIPT TREE VIEW WHOOO
            self.script_tree = ttk.Treeview(self.entity_info_frame, columns=self.columns, show='headings',
                                     height=self.root_height - 10)


            # self.tree.heading('email', text='Email')

            self.script_tree.bind('<<TreeviewSelect>>', self.item_selected)
            self.script_tree.place(x=5,y=335)#.grid(row=0, column=0, sticky=NSEW)

            # add a scrollbar
            self.script_scrollbar = ttk.Scrollbar(self.entity_info_frame, orient=VERTICAL, command=self.script_tree.yview)
            self.script_tree.configure(yscroll=self.script_scrollbar.set)
            self.script_scrollbar.place(x=self.entity_info_frame.width - 10,y=335,relheight=1)


    def create_script(self,entity, name):
        if name != "":
            if ".py" in name:
                self.script_name = name
                self.entity_script = entity
                self.entity_script.add_script(self.script_name,"EDITOR")
                self.script_tree.insert(self.script_name, END)
                #self.script_editor(self.script_name)
            elif "." in name and not "py" in name :
                Logger.send_error(self, "CANT HAVE , OR . IN FILE NAME", True)
            elif "," in name:
                Logger.send_error(self, "CANT HAVE , OR . IN FILE NAME", True)
            elif not ".py" in name:
                self.script_name = name + ".py"
                self.entity_script = entity
                self.entity_script.add_script(self.script_name, "EDITOR")
                self.script_tree.insert('', END, values=(self.script_name))
                #self.script_editor(self.script_name)
        else:
            Logger.send_error(self, "INVALID SCRIPT NAME", True)




    def script_editor(self, filename):
        self._canvas.config(width=0, height=0)
        self.code = filename
        self.root_tk.option_add("*tearOff", 0)
        self.notebook = ttk.Notebook(self.root_tk)
        self.tab_1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_1, text=self.code)
        self.notebook.grid(row=1, column=1, sticky=tkinter.NW)
        self.notebook.grid_propagate(0)
        self.code_editor = CodeEditor(self.tab_1,
            height=50,width=120,
            language="python",
            background="black",
            highlighter="dracula",
            font="Consolas",
            autofocus=True,
            blockcursor=True,
            insertofftime=0,
            padx=10,
            pady=10,

        )

        #rpc stuff
        if settings.RICH_PRESENCE == True:
            self.rpc.update(state="Using Bee Engine", details="editing script: " + self.code, large_image="bee", start=time.time())

        self.code_editor.grid(row=1, column=1)
        self.code_editor.content = """import engine"""
        self.root_tk.update()

    def slider_event(self, value):
        print(value)

    def edit_x(self, value, entity):
        print(value)
        #self._canvas.move(entity, int(value), 0)

    def edit_size(self,entity,x,y,width,height):
        entity.resize(x,y,width,height)

    def create_canvas(self):
        self._canvas = Canvas(self.root_tk, width=self.root_width - 700, height=self.root_height, bg="gray")
        self._canvas.grid(row=1, column=1)

    def create(self):
        self._canvas.config(width=0, height=0)
        self.entity_creation_frame = customtkinter.CTkFrame(master=self.root_tk, width=self.root_width - 400, height=self.root_height - 100,
                                                        corner_radius=10)
        self.entity_creation_frame.grid(row=1, column=1)
        self.entity_creation_frame.grid_propagate(0)
        #######THE LAYOUT#########
        self.title_label = customtkinter.CTkLabel(master=self.entity_creation_frame,text="Entity Creation Menu",width=self.root_width - 400,height=50,fg_color="gray",text_color="white",corner_radius=8)
        self.title_label.grid(row=0,column=0)
        self.id_label = customtkinter.CTkLabel(master=self.entity_creation_frame, text="id",width=50, height=50, fg_color="gray",text_color="white", corner_radius=8)
        self.id_label.place(x=10,y=60)
        self.id_entry = customtkinter.CTkEntry(master=self.entity_creation_frame, placeholder_text="Entity Name")
        self.id_entry.place(x=75,y=70)
        self.x_label = customtkinter.CTkLabel(master=self.entity_creation_frame, text="X", width=50, height=50,
                                               fg_color="gray", text_color="white", corner_radius=8)
        self.x_label.place(x=10, y=120)
        self.x_entry = customtkinter.CTkEntry(master=self.entity_creation_frame, placeholder_text="Entity X")
        self.x_entry.place(x=75, y=130)
        self.y_label = customtkinter.CTkLabel(master=self.entity_creation_frame, text="Y", width=50, height=50,
                                              fg_color="gray", text_color="white", corner_radius=8)
        self.y_label.place(x=10, y=180)
        self.y_entry = customtkinter.CTkEntry(master=self.entity_creation_frame, placeholder_text="Entity Y")
        self.y_entry.place(x=75, y=190)

        self.shape_entry = customtkinter.CTkEntry(master=self.entity_creation_frame, placeholder_text="Entity Shape")
        self.shape_entry.place(x=75, y=310)
        self.shape_label = customtkinter.CTkLabel(master=self.entity_creation_frame, text="Shape", width=50, height=50,
                                                  fg_color="gray", text_color="white", corner_radius=8)
        self.shape_label.place(x=10, y=300)
        self.color_entry = customtkinter.CTkEntry(master=self.entity_creation_frame, placeholder_text="Entity Color")
        self.color_entry.place(x=75, y=370)
        self.color_label = customtkinter.CTkLabel(master=self.entity_creation_frame, text="Color", width=50, height=50,
                                                  fg_color="gray", text_color="white", corner_radius=8)
        self.color_label.place(x=10, y=360)
        self.mass_entry = customtkinter.CTkEntry(master=self.entity_creation_frame, placeholder_text="Entity Mass")
        self.mass_entry.place(x=75, y=430)
        self.mass_label = customtkinter.CTkLabel(master=self.entity_creation_frame, text="Mass", width=50, height=50,
                                                  fg_color="gray", text_color="white", corner_radius=8)
        self.mass_label.place(x=10, y=420)
        self.width_entry = customtkinter.CTkEntry(master=self.entity_creation_frame, placeholder_text="Entity Width")
        self.width_entry.place(x=325, y=70)
        self.width_label = customtkinter.CTkLabel(master=self.entity_creation_frame, text="Width", width=50, height=50,
                                                 fg_color="gray", text_color="white", corner_radius=8)
        self.width_label.place(x=250, y=60)
        self.height_entry = customtkinter.CTkEntry(master=self.entity_creation_frame, placeholder_text="Entity Height")
        self.height_entry.place(x=325, y=130)
        self.height_label = customtkinter.CTkLabel(master=self.entity_creation_frame, text="Height", width=50, height=50,
                                                  fg_color="gray", text_color="white", corner_radius=8)
        self.height_label.place(x=250, y=120)
        self.scene_entry = customtkinter.CTkEntry(master=self.entity_creation_frame, placeholder_text="Entity Scene")
        self.scene_entry.place(x=325, y=190)
        self.scene_label = customtkinter.CTkLabel(master=self.entity_creation_frame, text="Scene", width=50,
                                                   height=50,
                                                   fg_color="gray", text_color="white", corner_radius=8)
        self.scene_label.place(x=250, y=180)
        ####IMAGE VIEWER
        self.path_entry = customtkinter.CTkEntry(master=self.entity_creation_frame, placeholder_text="Entity Path")
        self.path_entry.place(x=325, y=250)
        self.path_label = customtkinter.CTkLabel(master=self.entity_creation_frame, text="Path", width=50,
                                                  height=50,
                                                  fg_color="gray", text_color="white", corner_radius=8)
        self.path_label.place(x=250, y=240)
        self.name_label = customtkinter.CTkLabel(master=self.entity_creation_frame, text="Name", width=50,
                                                 height=50,
                                                 fg_color="gray", text_color="white", corner_radius=8)
        self.name_label.place(x=250, y=300)
        self.name_entry = customtkinter.CTkEntry(master=self.entity_creation_frame, placeholder_text="Entity Name")
        self.name_entry.place(x=325, y=310)

        self.preview_image = customtkinter.CTkButton(master=self.entity_creation_frame, text="Preview", command=self.image_preview)
        self.preview_image.place(x=450, y=250)
        self.done_button = customtkinter.CTkButton(master=self.entity_creation_frame, width=200,height=50,text="Create Entity",command=self.create_entity)
        self.done_button.place(x=50, y=self.root_height - 200)

    def create_entity(self):
        self.new_entity_id = int(self.id_entry.get())
        self.new_entity_name = self.name_entry.get()
        self.new_entity_x = int(self.x_entry.get())
        self.new_entity_y = int(self.y_entry.get())

        self.new_entity_shape = self.shape_entry.get()
        self.new_entity_color = self.color_entry.get()
        self.new_entity_path = self.path_entry.get()
        self.new_entity_mass = int(self.mass_entry.get())
        self.new_entity_width = int(self.width_entry.get())
        self.new_entity_height = int(self.height_entry.get())
        self.new_entity_scene = int(self.scene_entry.get())

        self.entity_creation_frame.destroy()
        self._canvas.config(width=self.root_width - 700, height=self.root_height)
        #make the actaul entity
        self.new_entity = Entity(self.new_entity_id,self.new_entity_name,self.new_entity_x,self.new_entity_y,shape=self.new_entity_shape,path=self.new_entity_path,color=self.new_entity_color,width=self.new_entity_width,height=self.new_entity_height,per_scene=self.new_entity_scene,scene=self._Scene)
        Ecs.add(self, self.new_entity)
        self.writer.Add((self.new_entity_name + " = " + "Entity(" + str(self.new_entity_id) + "," + self.new_entity_name + "," + str(self.new_entity_x) + "," + str(self.new_entity_y) + "," +  "," + "shape=" + str(self.new_entity_shape) + ",path=" + str(self.new_entity_path) + ",color=" + str(self.new_entity_color) + ",width=" + str(self.new_entity_width) + ",height=" + str(self.new_entity_height) + ",per_scene=" + str(self.new_entity_scene) + ",scene=_scene"))
        #print(self.new_entity_name + " = " + "Entity(" + str(self.new_entity_id) + "," + self.new_entity_name + "," +self.new_entity_x + "," + self.new_entity_y + "," + "size=" + self.new_entity_size + "," + "shape=" + self.new_entity_shape + ",canvas=_canvas,path=" + self.new_entity_path + ",color=" + self.new_entity_color + ",width=" + self.new_entity_width + ",height=" + self.new_entity_height + ",per_scene=" + self.new_entity_scene + ",scene=_scene")
        self.new_entity.draw()
        self._canvas.bind('<B1-Motion>', self.onObjectClick)



    def image_preview(self):
        self.image_width = int(self.width_entry.get())
        self.image_height = int(self.height_entry.get())
        self._image_viewer = Canvas(master=self.entity_creation_frame, width=self.image_width, height=self.image_height, bg="gray")
        self._image_viewer.place(x=700,y=100)
        self.path = self.path_entry.get()
        self.image = (Image.open(self.path))
        self.resized = self.image.resize((self.image_width, self.image_height))
        self.imager = ImageTk.PhotoImage(self.resized)
        self.shaper = self._image_viewer.create_image(self.image_width / 2, self.image_height / 2, image=self.imager)

    def tick(self):
        global counter, fp, start_time
        ######### Everything what is written in this function happens every second!!! ##########
        counter += 1
        if (time.time() - start_time) > fp:
            self.root_tk.title("BEE EDTIOR " + "FPS: " + str(counter / (time.time() - start_time)))
            counter = 0
            start_time = time.time()
        ##this makes it so that the functions repeats it self
        self.root_tk.after(1, self.tick)

    def show_entity_info(self, entity):
        self.entity = entity
        self.name = self.entity.getid()
        print(self.name)
        print("Hello Testing")
        #clear the frame
        self.entity_info_frame.grid_forget()
        self.entity_info_frame = customtkinter.CTkFrame(master=self.root_tk, width=400, height=self.root_height - 100,
                                                        corner_radius=10)
        self.entity_info_frame.grid(row=1, column=2, padx=10, pady=20)
        #show the info of the entity
        self.entity_x = self.entity.get_x()
        self.entity_y = self.entity.get_y()
        self.coord_label_x = customtkinter.CTkLabel(master=self.entity_info_frame,
                                       text=("X: " + str(self.entity_x)),
                                       width=120,
                                       height=25,
                                       fg_color=("white", "gray"),
                                       corner_radius=8)
        self.coord_label_y = customtkinter.CTkLabel(master=self.entity_info_frame,
                                                    text=("Y: " + str(self.entity_y)),
                                                    width=120,
                                                    height=25,
                                                    fg_color=("white", "gray"),
                                                    corner_radius=8)

        self.name_label = customtkinter.CTkLabel(master=self.entity_info_frame,text=("Name: " + str(self.name)),width=120,height=25,fg_color=("white", "gray"),corner_radius=8)
        self.size_label = customtkinter.CTkLabel(master=self.entity_info_frame,text=("Size: " + str(self.entity.get_size())),width=120,height=25,fg_color=("white", "gray"),corner_radius=8)

        self.coord_label_x.grid(row=1,column=0)
        self.coord_label_y.grid(row=2, column=0)
        self.name_label.grid(row=0, column=0)
        self.size_label.grid(row=3, column=0)

        if self.entity.color != None:
            self.color_label = customtkinter.CTkLabel(master=self.entity_info_frame,text=("Color: " + str(self.entity.color)), width=120,height=25, fg_color=("white", "gray"), corner_radius=8)
            self.color_label.grid(row=4, column=0)
        if self.entity.shape != None:
            self.shape_label = customtkinter.CTkLabel(master=self.entity_info_frame,text=("Shape: " + str(self.entity.shape)), width=120,height=25, fg_color=("white", "gray"), corner_radius=8)
            self.shape_label.grid(row=5, column=0)

    def mainloop(self):
        self.root_tk.mainloop()



if __name__ == "__main__":
    editor = Editor()
    editor.tick()
    editor.mainloop()
from tkinter import *

class Window:
    def __init__(self):
        self.window = Tk()
        self.window.title("Animation Editor")
        self.size = str(self.window.winfo_screenwidth()) + "x" + str(self.window.winfo_screenheight())
        print("LOGGER: window size: " + self.size)
        self.window.geometry(self.size)

    def get_window(self):
        return self.window

    def mainloop(self):
        self.window.mainloop()


class Screen:
    def __init__(self,window):
        self.window = window.get_window()
        self.height = self.window.winfo_screenheight() - 400
        self.canvas = Canvas(self.window, width=self.window.winfo_screenwidth(), height=self.height, bg="light gray")

    def init(self):
        self.canvas.grid(row=0,column=0)

class Timeline:
    def __init__(self, window):
        self.window = window.window
        self.height = 300
        self.canvas = Canvas(self.window, width=self.window.winfo_screenwidth(), height=self.height, bg="gray")
        self.canvas.propagate(0)
        self.vbar = Scrollbar(self.canvas, orient=VERTICAL)
        self.vbar.pack(side=LEFT, fill=Y)
        self.vbar.config(command=self.canvas.xview)

        self.canvas.bind('<Configure>', self.create_grid)
        #self.window.after(5, self.update)
        #self.window.after(self.update, 10)

    def init(self):
        self.canvas.grid(row=1,column=0)

    def update(self):
        print("Logger: REFERSH TIMELINE GRID")
        self.create_grid()
        self.window.after(4, self.update)


    def create_grid(self):
        for x in range(0, 10000, 50):
            for y in range(0, 300, 100):
                self.canvas.create_rectangle(x, y, x + 30, y + 30, outline='black')


if __name__ == '__main__':
    window = Window()
    screen = Screen(window)
    screen.init()
    timeline = Timeline(window)
    timeline.init()
    timeline.create_grid()

    window.mainloop()
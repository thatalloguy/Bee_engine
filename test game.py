from tkinter import *
from math import sin, cos
from time import sleep

"""
from engine import *
from engine.Particles import *
window = Bee(500,500,title="Test Game",resizable=True,bg="black",icon="engine/images/bee1.png")
canvas = window.return_canvas()
win = window.return_window()
scener = Scene(canvas)
scener.set_scene(0)
bob = Entity(1,"bob",250,250,shape="image",path="C:/Users/allos/Documents/arts/shee1.png",per_scene=0,scene=scener,width=50,height=50)
bob.draw()
bob.play_animation("C:/Users/allos/Documents/arts/duck_illusionist-walking.gif", 100)
ducks = Particle(win,canvas,1,"radial",250,250,50,0.1,12,30,"circle",5,5,"green",9,"in",9,path="C:/Users/allos/Documents/arts/duck_illusionist.png")
window.update()
"""

"""
import numpy as np


def closest_value(input_list, input_value):
    arr = np.asarray(input_list)

    i = (np.abs(arr - input_value)).argmin()

    return arr[i]


if __name__ == "__main__":
    list1 = [22, 12, 51, 23, 48, 16, 34, 61]

    num = int(input("Enter the value: "))

    val = closest_value(list1, num)

    print("The closest value to the " + str(num) + " is", val)
    


"""
win = Tk()
win.title("CIRCLE TEST")
c = Canvas(win, width=500,height=500,bg="black")
c.pack()
t = 90
r = 90
particles = []

def draw_point(x1,y1, lifespan):

    global c, t, r, win, particles
    while t < 360:
        y = y1 + r * sin(t)
        x = x1 + r * cos(t)
        print(str(x) + "|" + str(y))
        bob = c.create_rectangle(x, y, x + 5, y + 5, fill="green", tags="part")
        particles.append(bob)
        print("DRWA")
        t += 30

        sleep(0.01)
        win.update()

    print("DONE")
    t = 0


    while True:
        for i in particles:
            t += 30
            y = y1 + r * sin(t)
            x = x1 + r * cos(t)
            c.moveto(i,x,y)
            win.update()
            sleep(0.0001)
    """
    global c, t, r, win, particles
    while t != 360:
        y = y1 + r * sin(t)
        x = x1 + r * cos(t)
        print(str(x) + "|" + str(y))
        bob = c.create_rectangle(x,y,x+5,y+5,fill="green",tags="part")
        particles.append(bob)
        print("DRWA")
        t += 3

        sleep(0.01)
        win.update()

    print("DONE")

    for i in particles:
        if lifespan > 0:
            print(str(lifespan))
            y = y1 + r * sin(t)
            x = x1 + r * cos(t)
            #print(str(x) + "|" + str(y))
            r += 1
            t += 3
            c.moveto(i, x, y)
            win.update()
            lifespan -= 1
            sleep(0.001)
            #c.delete(i)


    sleep(0.02)
    c.delete("part")
    win.update()

    print("DONE!")
    """

Button(win, text="PARTICLE TEST", command=lambda: draw_point(250,250, 100)).pack()


win.mainloop()



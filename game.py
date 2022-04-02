from bee_engine.graphics import *

window = Bee(500,500,title="HELLO WORLD",resizable=False,fullscreen=True)
bob = Entity(69,100,100,50,shape="line",color="blue")
josh = Entity(12,120,120,225,shape="image",path="images/bee1.png")


def move(event):
    if event.char == "a":
        josh.move(10,0)
    elif event.char == "d":
        josh.move(-10,0)

bind("<Key>", move)

#text = Gui(500,500,entry=True,color="white")
#text2 = Gui(500,500,button=True,bt="HELLO WORLD",command=None,color="white")
#text.draw()
#text2.draw()
josh.draw()
#bob.draw()
#bob2.undraw()
hey = bob.getid()
print(str(hey))
window.update()


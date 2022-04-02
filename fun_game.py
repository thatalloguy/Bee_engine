import random

from bee_engine.graphics import *
right = 10000
night = False
def cycle():
    global right, night
    if right >0:
        night = False
        cloud1.move(0.1, 0)
        cloud2.move(0.1, 0)
        cloud3.move(0.1, 0)
        cloud4.move(0.1, 0)
        right -= 1
        window.config("light blue")
    else:
        night = True
        window.config("blue")
        if right == -10000:
            right = 10000

        right -= 1
        cloud1.move(-0.1, 0)
        cloud2.move(-0.1, 0)
        cloud3.move(-0.1, 0)
        cloud4.move(-0.1, 0)
    window.wait(cycle, 5)


def generate_flowers():
    pass

window = Bee(69,69,title="A Bee life",resizable=False,fullscreen=True)
window.config(color='light blue')
generate_flowers()
tree = Entity(6, 1200, 900,0,shape="image",path="images/tree.png")
player = Entity(1,500,500,100,shape="image",path="images/bee2.png")
cloud1 = Entity(2,64,64,100,shape="image",path="images/cloud.png")
cloud2 = Entity(3, 500, 64, 100, shape="image", path="images/cloud.png")
cloud3 = Entity(4, 844, 64, 100, shape="image", path="images/cloud.png")
cloud4 = Entity(5, 1404, 64, 100, shape="image", path="images/cloud.png")
player.draw()
tree.draw()
cloud1.draw()
x = random.randint(32,1000)
print(str(x))
y =1055
flower1 = Entity(7, x, y, 0,shape="image",path="images/flower.png")
x = random.randint(32,1000)
flower2 = Entity(7, x, y, 0,shape="image",path="images/flower.png")
x = random.randint(32,1000)
flower3 = Entity(7, x, y, 0,shape="image",path="images/flower.png")
x = random.randint(32,1000)
flower1.draw()
flower2.draw()
flower3.draw()
cloud2.draw()
cloud3.draw()
cloud4.draw()
window.wait(cycle, 1)
window.update()


import engine.Logger
import engine.Entity

class Scene:
    def __init__(self,canvas):
        self.c = canvas
        self.current_scene = 0
        self.last_scene = 0

    def set_scene(self,scene):
        self.c.delete("all")
        self.scene = scene
        self.last_scene = self.current_scene
        self.current_scene = self.scene
        engine.Logger.send_info(self, ("Scene changed to: " + str(self.scene)), True)

    def get_current_scene(self):
        return self.current_scene

    def get_last_scene(self):
        return self.last_scene
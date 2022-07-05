from engine.Logger import *

class Script:
    def __init__(self,type="",entity=None):
        self.type = type
        self.entity = entity


        #check it
        if self.type != "" or self.type != "general" and self.type != "entity":
            Logger.send_error(self, "Error invalid -type in SCRIPT class", True)
        if self.entity == None:
            Logger.send_error(self, "Error invalid -entity in SCRIPT CLASS", True)

    def return_type(self):
        return self.type

    def return_entity(self):
        return self.entity

    def change_type(self, type):
        self.type = type

    def change_entity(self,entity):
        try:
            self.entity = entity
        except:
            Logger.send_error(self, "Error invalid -entity in SCRIPT CLASS", True)
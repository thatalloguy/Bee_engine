import logging
import easygui

class Logger:
    def __init__(self):
        pass

    def send_info(self, message, debug):
        if debug == True:
            print("INFO: " + message)

    def send_error(self, message, debug):
        if debug == True:
            print("ERROR: " + message)
        easygui.msgbox("ERROR " + message, 'ERROR')

    def send_warning(self, message, poppup=False):
        self.poppup = poppup
        self.send_info("CRITICAL " + message)
        if self.poppup == True:
            easygui.msgbox(message, 'ERROR')


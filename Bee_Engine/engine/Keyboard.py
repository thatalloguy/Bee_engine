from pynput import keyboard


class Keyboard:
    def __init__(self):
        self.last_pressed = ""
        self.last_released = ""

        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
            self.listener.join()
            self.listener.start()

        # ...or, in a non-blocking fashion:
        #self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def start(self):
        self.listener.start()

    def on_press(self, key):
        #print(str(key))
        self.last_pressed = str(key)

    def on_release(self, key):
        self.last_released = str(key)

    def get_pressed(self):
        return self.last_pressed

    def get_released(self):
        return self.last_released

import curses
from vii.config import *
from vii.view import View
from vii.model import Model
from vii.controller import Controller

class Application:
    def __init__(self, screen):
        self.screen = screen
        self.main()

    def main(self):
        self.model = Model(self)
        self.view = View(self)
        self.controller = Controller(self)
        self.wireUp()
        self.controller.loop()

    def wireUp(self):
        pass

def main(): curses.wrapper(Application)

from .NormalMode import NormalMode
from .Setup import numberBarWidth, commandMap
from .Logger import *
import os

# Executed before call to curses.wrapper(Application) during import in app.py
os.environ.setdefault('ESCDELAY', '25')

class Controller():

    def __init__(self, model, view):
        self.screen = view.root
        self.normalMode = NormalMode(model, view)

    def loop(self):
        self.screen.nodelay(0)
        while True:
            key = self.screen.getch()
            self.normalMode.handleKey(key)


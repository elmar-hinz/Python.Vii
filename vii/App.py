import curses
from .Model import Model
from .Controller import Controller
from .view.View import View

class Application:
    def __init__(self, root):
        model = Model()
        view = View(root)
        Controller(model, view).loop()

def main(): curses.wrapper(Application)

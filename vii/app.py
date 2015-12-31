import curses
from .model.model import Model
from .controller.controller import Controller
from .view.view import View

class Application:
    def __init__(self, root):
        model = Model()
        view = View(root)
        Controller(model, view).loop()

def main(): curses.wrapper(Application)

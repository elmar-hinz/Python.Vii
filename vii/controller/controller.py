from .commandmode import CommandMode
from .editmode import EditMode
from .insertmode import InsertMode
from .cursor import Cursor
from ..logger import *
import os

# Executed before call to curses.wrapper(Application) during import in app.py
os.environ.setdefault('ESCDELAY', '25')

class Controller:

    def __init__(self, model, view):
        self.model, self.view = model, view
        self.view.commandLine.buffer = self.model.commandLine
        self.createWindow()
        self.commandMode = CommandMode(self)
        self.editMode = EditMode(self)
        self.insertMode = InsertMode(self)
        self.currentMode = self.insertMode

    def loop(self):
        self.view.root.nodelay(0)
        while True:
            key = self.view.root.getch()
            self.currentMode = self.currentMode.handleKey(key)

    def createWindow(self):
        """ TODO: multiple windows """
        """ TODO: dynamic relation betwenn buffer and windows """
        buffer = self.model.createBuffer(Cursor())
        self.view.createWindow(buffer)


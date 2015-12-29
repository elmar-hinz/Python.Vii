from .commandmode import CommandMode
from .editmode import EditMode
from .insertmode import InsertMode
from ..logger import *
import os

# Executed before call to curses.wrapper(Application) during import in app.py
os.environ.setdefault('ESCDELAY', '25')

class Controller:

    def __init__(self, model, view):
        self.model, self.view = model, view
        self.commandMode = CommandMode(self)
        debug("controller: buffer length: %s" % self.model.buffer.length())
        self.editMode = EditMode(self)
        debug("controller: buffer length: %s" % self.model.buffer.length())
        self.insertMode = InsertMode(self)
        self.currentMode = self.insertMode
        self.wireUp()

    def wireUp(self):
        self.view.commandLine.setBuffer(self.model.commandLine)
        self.view.window.setBuffer(self.model.buffer)

    def loop(self):
        self.view.root.nodelay(0)
        while True:
            key = self.view.root.getch()
            self.currentMode = self.currentMode.handleKey(key)
            debug(self.currentMode)


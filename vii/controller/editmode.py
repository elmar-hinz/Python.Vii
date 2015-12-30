from .abstractmode import AbstractMode
from .move import *
from ..config import numberBarWidth
from ..logger import *

class EditMode(AbstractMode):

    def __init__(self, controller):
        super().__init__(controller)
        self.window = controller.view.window
        self.buffer = controller.model.buffer
        self.cursor = self.buffer.cursor

    def handleKey(self, key):
        super().handleKey(key)
        if key == 27: return self.controller.commandMode
        if key == 104: return self.left()
        if key == 106: return self.down()
        if key == 107: return self.up()
        if key == 108: return self.right()
        if key == 65: return self.appendToLine()
        return self.controller.editMode

    def up(self):
        self.cursor.position(*up(self.cursor.position(), 1))
        self.window.draw()
        return self.controller.editMode

    def down(self):
        self.cursor.position(*down(self.cursor.position(), 1))
        self.window.draw()
        return self.controller.editMode

    def left(self):
        self.cursor.position(*left(self.cursor.position(), 1))
        self.window.draw()
        return self.controller.editMode

    def right(self):
        self.cursor.position(*right(self.cursor.position(), 1))
        self.window.draw()
        return self.controller.editMode

    def appendToLine(self):
        x = self.currentLine().length() + numberBarWidth
        self.cursor.position(x=x)
        self.window.draw()
        return self.controller.insertMode

    def currentLine(self):
        return self.buffer[self.cursor.y]



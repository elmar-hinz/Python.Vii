from .abstractmode import AbstractMode
from .movements import Movements
from ..config import numberBarWidth
from ..logger import *

class EditMode(AbstractMode):

    def __init__(self, controller):
        super().__init__(controller)
        self.window = controller.view.window
        self.buffer = controller.model.buffer
        self.cursor = self.buffer.cursor
        self.move = Movements(self.window, self.buffer, self.cursor)

    def handleKey(self, key):
        super().handleKey(key)
        if key == ord('$'): return self.endOfLine()
        if key == ord(':'): return self.controller.commandMode
        if key == ord('^'): return self.beginningOfLine()
        if key == ord('A'): return self.appendToLine()
        if key == ord('I'): return self.insertBeforeLine()
        if key == ord('a'): return self.append()
        if key == ord('h'): return self.left()
        if key == ord('i'): return self.insert()
        if key == ord('j'): return self.down()
        if key == ord('k'): return self.up()
        if key == ord('l'): return self.right()
        return self.controller.editMode

    def append(self):
        self.cursor.position(*self._append(self.cursor.position()))
        return self.controller.insertMode

    def insert(self):
        return self.controller.insertMode

    def up(self):
        self.cursor.position(*self.move.up())
        return self.controller.editMode

    def down(self):
        self.cursor.position(*self.move.down())
        return self.controller.editMode

    def left(self):
        self.cursor.position(*self.move.left())
        return self.controller.editMode

    def right(self):
        self.cursor.position(*self.move.right())
        return self.controller.editMode

    def endOfLine(self):
        self.cursor.position(*self.move.endOfLine())
        return self.controller.editMode

    def beginningOfLine(self):
        self.cursor.position(*self.move.beginningOfLine())
        return self.controller.editMode

    def appendToLine(self):
        self.cursor.position(*self._append(self.move.endOfLine()))
        return self.controller.insertMode

    def insertBeforeLine(self):
        self.cursor.position(*self.move.beginningOfLine())
        return self.controller.insertMode

    def currentLine(self):
        return self.buffer[self.cursor.y]

    def _append(self, position):
        return (position[0], position[1] + 1)


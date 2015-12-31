from .abstractmode import AbstractMode
# from .commandmode import CommandMode
from .insertmode import InsertMode
from .cursor import Cursor
from .movements import Movements
from ..logger import *
from ..config import numberBarWidth, commandMap
import os

# Executed before call to curses.wrapper(Application) during import in app.py
os.environ.setdefault('ESCDELAY', '25')

class NormalMode(AbstractMode):

    model, view, window, buffer, cursor = None, None, None, None, None
    command, commandMap, delegating = None, dict(), False
    move, insertMode = None, None

    def __init__(self, model, view):
        self.model, self.view = model, view
        self.createWindow()
        self.window = self.view.window
        self.buffer = self.model.buffer
        self.cursor = self.buffer.cursor
        self.parseCommandMap()
        # self.view.commandLine.buffer = self.model.commandLine
        # self.commandMode = CommandMode(self)
        self.insertMode = InsertMode(self)
        self.view.window.draw()
        self.move = Movements(self.window, self.buffer, self.cursor)

    def parseCommandMap(self):
        for line in commandMap.strip().splitlines():
            try:
                k, v = tuple(i.strip() for i in line.split(":"))
                self.commandMap[k] = v
            except:
                pass

    def createWindow(self):
        """ TODO: multiple windows """
        """ TODO: dynamic relation betwenn buffer and windows """
        buffer = self.model.createBuffer(Cursor())
        self.view.createWindow(buffer)

    def handleKey(self, key):
        super().handleKey(key)
        if key == 27:
            info("escape")
            self.delegating = False
            if self.child == self.insertMode: self.left()
            self.child = None
        if self.delegating:
            info("delegate %s"%chr(key))
            self.child.handleKey(key)
        elif self.catchCommand(key):
            self.switchCommand()
            self.command = None

    def catchCommand(self, key):
        if self.command == None:
            self.command = {'count': "0", 'operator': ""}
        if chr(key).isdigit():
            self.command['count'] += chr(key)
            return False
        else:
            self.command['count'] = int(self.command['count'])
            self.command['operator'] += chr(key)
            return True

    def switchCommand(self):
        c, o = self.command['count'], self.command['operator']
        info("switch %s %s"%(c, o))
        try:
            operator = self.commandMap[o]
            function = getattr(self, operator)
            return function()
        except:
            pass

    def append(self):
        self.delegating = True
        self.child = self.insertMode
        self.cursor.position(*self._append(self.cursor.position()))

    def insert(self):
        self.delegating = True
        self.child = self.insertMode

    def up(self):
        self.cursor.position(*self.move.up())

    def down(self):
        self.cursor.position(*self.move.down())

    def left(self):
        self.cursor.position(*self.move.left())

    def right(self):
        self.cursor.position(*self.move.right())

    def endOfLine(self):
        self.cursor.position(*self.move.endOfLine())

    def beginningOfLine(self):
        self.cursor.position(*self.move.beginningOfLine())

    def appendToLine(self):
        self.delegating = True
        self.child = self.insertMode
        self.cursor.position(*self._append(self.move.endOfLine()))

    def insertBeforeLine(self):
        self.delegating = True
        self.child = self.insertMode
        self.cursor.position(*self.move.beginningOfLine())

    def currentLine(self):
        return self.buffer[self.cursor.y]

    def _append(self, position):
        return (position[0], position[1] + 1)


from .AbstractMode import AbstractMode
from .InsertMode import InsertMode
from .Cursor import Cursor
from .Buffer import Buffer
from .NormalActions import NormalActions
from .Logger import *
from .Setup import commandMap
import os

class NormalMode(AbstractMode):

    view, window, buffer, cursor = None, None, None, None
    actions, command, commandMap, delegating = None, None, dict(), False
    insertMode = None

    def __init__(self, view):
        self.view = view
        self.createWindow()
        self.window = self.view.window
        self.cursor = self.window.cursor
        self.buffer = self.cursor.buffer
        self.parseCommandMap()
        self.insertMode = InsertMode(self)
        self.view.window.draw()
        self.actions = NormalActions(self.buffer, self.cursor)

    def parseCommandMap(self):
        for line in commandMap.strip().splitlines():
            try:
                k, v = tuple(i.strip() for i in line.split(":"))
                self.commandMap[k] = v
            except:
                pass

    def handleKey(self, key):
        super().handleKey(key)
        if self.delegating:
            info("delegate %s"%chr(key))
            self.child.handleKey(key)
            if key == 27:
                self.delegating = False
                self.child = None
        elif self.catchCommand(key):
            """ when command complete """
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
            function = getattr(self.actions, operator)
            mode = function()
            if mode == "InsertMode":
                self.delegating = True
                self.child = self.insertMode
        except KeyError:
            debug("Switching failed for %s" % o)

    # TODO: where is the right place?
    def createWindow(self):
        """ TODO: multiple windows """
        """ TODO: dynamic relation between buffer and windows """
        buffer = Buffer()
        buffer.insertLines(0,"")
        cursor = Cursor(buffer)
        self.view.createWindow(buffer, cursor)


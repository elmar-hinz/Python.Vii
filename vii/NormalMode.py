from .InsertMode import InsertMode
from .Cursor import Cursor
from .Buffer import Buffer
from .CommandCatcher import CommandCatcher
from .NormalActions import NormalActions
from .Logger import *
from .Setup import commandMap

class NormalMode:

    view, buffer = None, None
    commandCatcher, actions, delegating = None, None, False
    insertMode = None

    def __init__(self, view, buffer):
        self.view = view
        self.buffer = buffer
        self.createWindow()
        self.view.window.draw()
        self.commandCatcher = CommandCatcher(commandMap)
        self.insertMode = InsertMode(self)
        self.actions = NormalActions(self.buffer, self.view.window.cursor)

    def step(self, key):
        if self.delegating:
            info("delegate %s"%chr(key))
            self.child.setp(key)
            if key == 27:
                self.delegating = False
                self.child = None
        elif self.commandCatcher.ready(key):
            """ when command complete """
            self.switchCommand()
            self.commandCatcher.reset()

    def switchCommand(self):
        count = self.commandCatcher.count()
        operator = self.commandCatcher.command()
        info("switch %s %s"%(count, operator))
        try:
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
        buffer = self.buffer
        buffer.insertLines(0,"")
        cursor = Cursor(buffer)
        self.view.createWindow(buffer, cursor)


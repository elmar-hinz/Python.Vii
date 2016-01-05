from .InsertMode import InsertMode
from .NormalActions import NormalActions
from .Logger import *

class Controller:

    def __init__(self, windowManager, commandCatcher):
        self.windowManager = windowManager
        self.commandCatcher = commandCatcher
        self.insertMode = InsertMode(windowManager, commandCatcher)
        self.actions = NormalActions(windowManager, commandCatcher)
        self.delegating = False

    def step(self, key):
        if self.delegating:
            debug("delegate %s"%chr(key))
            self.child.setp(key)
            if key == 27:
                self.delegating = False
                self.child = None
        elif self.commandCatcher.ready(key):
            """ when command complete """
            self.dispatch()
            self.commandCatcher.reset()

    def dispatch(self):
        action = self.commandCatcher.action()
        debug("switch  %s"%(action))
        try:
            function = getattr(self.actions, action)
            mode = function(self.commandCatcher)
            if mode == "InsertMode":
                self.delegating = True
                self.child = self.insertMode
        except TypeError:
            debug("Switching failed for %s: %s"
                % (self.commandCatcher.operator(), action))


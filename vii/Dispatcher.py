from .Logger import *
from .Command import Command

class TokenExecption(Exception): pass

class Dispatcher:

    def __init__(self):
        self.actionManager = None
        self.currentMode = None
        self.currentAction = None
        self.currentCommand = None

    def step(self, token):
        self.stepInit(token)
        self.stepCommand(token)
        self.stepAction(token)

    def stepInit(self, token):
        if isinstance(token, int): raise TokenExecption
        if self.currentCommand == None: self.reset()
        if self.currentMode == None or self.currentAction == None:
            self.currentMode = "normal"
            self.currentAction = self.actionManager.action(
                "normal", "idle")

    def stepCommand(self, token):
        if self.currentMode == "insert":
            debug("INSERT")
            self.currentCommand.last().appendToInserts(token)
        else:
            if token.isdigit():
                self.currentCommand.last().appendToNumeral(token)
                self.currentCommand.last().numeralToCount()
            else:
                self.currentCommand.last().operator = token
                self.currentCommand.last().ready = True

    def stepAction(self, token):
        if token == chr(27):
            self.currentAction.finish()
            self.currentMode = "normal"
            self.currentAction = self.actionManager.action(
                "normal", "idle")
        if self.currentCommand.last().ready:
            self.currentMode, self.currentAction = self.currentAction.act()

    def logHistory(self):
        # TODO
        pass

    def extend(self):
        self.currentCommand.extend()

    def reset(self):
        self.currentCommand = Command()
        self.currentCommand.extend()


from .Logger import *
from .Command import Command

class TokenExecption(Exception): pass

class Dispatcher:
    def __init__(self):
        self.actionManager = None
        self.currentMode = None
        self.currentAction = None
        self.currentCommand = None
        self.forceTokenToString = False

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
            self.currentCommand.last().appendToInserts(token)
        else:
            if(len(self.currentCommand.last().numeral) == 0
                and token == '0'): self.forceTokenToString = True
            if token.isdigit() and not self.forceTokenToString:
                self.currentCommand.last().appendToNumeral(token)
                self.currentCommand.last().numeralToCount()
            else:
                self.forceTokenToString = True
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
        self.forceTokenToString = False

    def reset(self):
        self.currentCommand = Command()
        self.currentCommand.extend()
        self.forceTokenToString = False


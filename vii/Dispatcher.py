from .Logger import *

class Dispatcher:

    def __init__(self):
        self.windowManager = None
        self.actionManager = None
        self.currentMode = None
        self.currentAction = None
        self.currentToken = None
        self.currentCommand = None
        self.operatorReady = False

    def step(self, token):
        self.currentToken = token
        self.stepInit(token)
        self.stepCommand(token)
        self.stepAction(token)

    def stepInit(self, token):
        if isinstance(token, int): raise Exception
        if self.currentMode == None or self.currentAction == None:
            self.currentMode, self.currentAction = self.actionManager.action(
                "normal", "idle")
        if self.currentCommand == None:
            self.reset()

    def stepCommand(self, token):
        if self.currentMode == "insert":
            self.currentCommand['inserts'] += token
        elif self.currentMode == "normal":
            if token.isdigit():
                self.currentCommand['count'] += token
            else:
                count = int(self.currentCommand['count'])
                self.currentCommand['count'] = count if count > 0 else 1
                self.currentCommand['operator'] += token
                self.operatorReady = True

    def stepAction(self, token):
        if token == chr(27):
            self.currentAction.finish()
            self.currentMode, self.currentAction = self.actionManager.action(
                "normal", "idle")
        self.currentMode, self.currentAction = self.currentAction.act()

    def ready(self):
        return self.operatorReady

    def count(self):
        return self.currentCommand['count']

    def operator(self):
        return self.currentCommand['operator']

    def token(self):
        return self.currentToken

    def command(self):
        return self.currentCommand

    def logHistory(self):
        # TODO
        pass

    def reset(self):
        self.currentCommand = {'count': "0", 'operator': "", "inserts" : []}
        self.operatorReady = False


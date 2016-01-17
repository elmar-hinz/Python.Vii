from .Logger import *

class TokenExecption(Exception): pass

class Dispatcher:

    def __init__(self):
        self.windowManager = None
        self.actionManager = None
        self.currentMode = None
        self.currentAction = None
        self.currentToken = None
        self.currentCommand = None
        self.operatorReady = False
        self.operator2Ready = False

    def step(self, token):
        self.currentToken = token
        self.stepInit(token)
        self.stepCommand(token)
        self.stepAction(token)

    def stepInit(self, token):
        if isinstance(token, int): raise TokenExecption
        if self.currentMode == None or self.currentAction == None:
            self.currentMode = "normal"
            self.currentAction = self.actionManager.action(
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
                count = self.currentCommand['count']
                if count == "": self.currentCommand['count'] = None
                else: self.currentCommand['count'] = int(count)
                self.currentCommand['operator'] += token
                self.operatorReady = True
        elif self.currentMode == "operatorPending":
            if token.isdigit():
                self.currentCommand['count2'] += token
            else:
                count = self.currentCommand['count2']
                if count == "": self.currentCommand['count2'] = None
                else: self.currentCommand['count2'] = int(count)
                self.currentCommand['operator2'] += token
                self.operator2Ready = True

    def stepAction(self, token):
        if token == chr(27):
            self.currentAction.finish()
            self.currentMode = "normal"
            self.currentAction = self.actionManager.action(
                "normal", "idle")
        self.currentMode, self.currentAction = self.currentAction.act()

    def ready(self):
        return self.operatorReady

    def count(self):
        return self.currentCommand['count']

    def operator(self):
        return self.currentCommand['operator']

    def operatorPendingReady(self):
        return self.operator2Ready

    def operatorPendingCount(self):
        return self.currentCommand['count2']

    def operatorPendingOperator(self):
        return self.currentCommand['operator2']

    def token(self):
        return self.currentToken

    def command(self):
        return self.currentCommand

    def logHistory(self):
        # TODO
        pass

    def reset(self):
        self.currentCommand = {
                "inserts" : [],
                'count': "",
                'operator': "",
                'count2': "",
                'operator2': "",
                }
        self.operatorReady = False
        self.operator2Ready = False

    def noneCountTo1(self):
        if self.currentCommand['count'] == None:
            self.currentCommand['count'] = 1


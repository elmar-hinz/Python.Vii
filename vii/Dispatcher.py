from .Logger import *

class Dispatcher:

    def __init__(self):
        self.windowManager = None
        self.actionManager = None
        self.currentMode = None
        self.currentAction = None
        self.parts = None
        self.operatorReady = False

    def step(self, key):
        if self.currentMode == None or self.currentAction == None:
            self.currentMode, self.currentAction = self.actionManager.action(
                "normal", "idle")
        self.stepCommand(key)
        self.stepAction(key)

    def stepAction(self, key):
        if key == 27:
            self.currentAction.finish()
            self.currentMode, self.currentAction = self.actionManager.action(
                "normal", "idle")
            self.reset()
        self.currentMode, self.currentAction = self.currentAction.act()

    def stepCommand(self, key):
        if isinstance( key, int ): raise Exception
        else: char = key
        if self.currentMode == "insert":
            self.passChar = char
        elif self.currentMode == "normal":
            if self.parts == None:
                self.parts = {'count': "0", 'operator': "", }
            if char.isdigit():
                self.parts['count'] += char
            else:
                count = int(self.parts['count'])
                self.parts['count'] = count if count > 0 else 1
                self.parts['operator'] += char
                self.operatorReady = True

    def ready(self):
        return self.operatorReady

    def count(self):
        return self.parts['count']

    def operator(self):
        return self.parts['operator']

    def character(self):
        return self.passChar

    def reset(self):
        self.parts = None
        self.operatorReady = False
        self.passChar = None


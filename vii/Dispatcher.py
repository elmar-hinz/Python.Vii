from .Logger import *

class Dispatcher:

    def __init__(self):
        self.windowManager = None
        self.actionManager = None
        self.currentAction = None
        self.parts = None
        self.operatorReady = False

    def step(self, key):
        self.stepCommand(key)
        self.stepAction(key)

    def stepAction(self, key):
        if self.currentAction == None:
            self.currentAction = self.actionManager.action("normal", "idle")
        if key == 27:
            self.currentAction.finish()
            self.currentAction = self.actionManager.action("normal", "idle")
        self.currentAction = self.currentAction.act()

    def stepCommand(self, key):
        if self.parts == None:
            self.parts = {'count': "0", 'operator': "", }
        if chr(key).isdigit():
            self.parts['count'] += chr(key)
        else:
            count = int(self.parts['count'])
            self.parts['count'] = count if count > 0 else 1
            self.parts['operator'] += chr(key)
            self.operatorReady = True

    def ready(self):
        return self.operatorReady

    def count(self):
        return self.parts['count']

    def operator(self):
        return self.parts['operator']

    def reset(self):
        self.parts = None
        self.operatorReady = False


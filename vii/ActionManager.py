from .Logger import *
from .BufferRanges import BufferRanges
from .AbstractAction import AbstractAction

class DummyAction(AbstractAction):

    def act(self, dummyCallback = None):
        return "normal", self.actionManager.action("normal", "idle")


class ActionManager:

    def __init__(self):
        self.dispatcher = None
        self.windowManager =  None
        self.registerManager = None
        self.actionMaps = dict()
        self.actionModules = dict()

    def addModule(self, mode, module):
        self.actionModules[mode] = module

    def addMap(self, mode, map):
        self.actionMaps[mode] = self.parseMap(map)

    def action(self, mode, operator):
        try:
            action = self.actionMaps[mode][operator]
            module = self.actionModules[mode]
            Action = getattr(module, action)
            action = Action()
        except KeyError:
            debug("Key Error: %s %s" % (mode, operator))
            self.dispatcher.reset()
            action = DummyAction()
        action.dispatcher = self.dispatcher
        action.command = self.dispatcher.currentCommand
        action.windowManager = self.windowManager
        action.actionManager = self
        action.registerManager = self.registerManager
        action.window = self.windowManager.window
        action.buffer = self.windowManager.buffer
        action.cursor = self.windowManager.cursor
        action.ranges = self.windowManager.ranges
        return action

    def parseMap(self, text):
        map = dict()
        for line in text.strip().splitlines():
            try:
                k, v = tuple(i.strip() for i in line.split(":"))
                map[k] = v
            except:
                pass
        return map


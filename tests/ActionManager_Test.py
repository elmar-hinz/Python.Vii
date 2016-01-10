import sys
from vii.ActionManager import ActionManager
from vii.AbstractAction import AbstractAction

class Alpha:
    def __init__(self, dispatcher, windowManager, actionManager):
        self.dispatcher = dispatcher
        self.windowManager = windowManager
        self.actionManager = actionManager

class ActionManager_Test:

    mode = "mmm"
    operator = "a"
    actionMap = {"a":"Alpha", "b":"Beta"}
    mapString = """
    a: Alpha
    b: Beta
    """

    def setup(self):
        self.dispatcher = "Dispatcher"
        self.windowManager = "WM"
        self.manager = ActionManager()
        self.manager.dispatcher = self.dispatcher
        self.manager.windowManager = self.windowManager

    def test_parseMap(self):
        result = self.manager.parseMap(self.mapString)
        assert result == self.actionMap

    def test_addMap(self):
        self.manager.addMap(self.mode, self.mapString)
        result = self.manager.actionMaps[self.mode]
        assert result == self.actionMap

    def test_addModule(self):
        me = sys.modules[__name__]
        self.manager.addModule(self.mode, me)
        result = self.manager.actionModules[self.mode]
        assert result == me

    def test_action(self):
        me = sys.modules[__name__]
        self.manager.addModule(self.mode, me)
        self.manager.addMap(self.mode, self.mapString)
        action = self.manager.action("mmm", "a")
        # assert action.__class__ == Alpha
        # assert action.windowManager == self.windowManager
        # assert action.dispatcher == self.dispatcher



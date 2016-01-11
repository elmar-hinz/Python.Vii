import sys
from vii.ActionManager import ActionManager

class Alpha:
    pass

class Mock():
    window = "Window"
    buffer = "Buffer"
    cursor = "Cursor"

class ActionManager_Test:

    mode = "mmm"
    operator = "a"
    actionMap = {"a":"Alpha", "b":"Beta"}
    mapString = """
    a: Alpha
    b: Beta
    """

    def setup(self):
        self.manager = ActionManager()
        self.manager.dispatcher = Mock()
        self.manager.windowManager = Mock()
        self.manager.registerManager = Mock()

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
        mode, action = self.manager.action("mmm", "a")
        assert action.__class__ == Alpha
        assert mode == "mmm"
        wanted = ("dispatcher windowManager actionManager"
        " window buffer cursor registerManager ")
        for w in wanted.split():
            print(w)
            assert w in dir(action)





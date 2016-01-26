import sys
from vii.ActionManager import ActionManager

class Alpha:
    pass

class Mock():
    window = "Window"
    buffer = "Buffer"
    cursor = "Cursor"
    motions = "Motions"
    currentCommand = "Command"

class ActionManager_Test:

    mode = "mmm"
    operator = "a"
    actionMap = {"a":"tests.ActionManager_Test.Alpha", "b":"tests.ActionManager_Test.Beta"}
    mapString = """
    a: tests.ActionManager_Test.Alpha
    b: tests.ActionManager_Test.Beta
    """

    def setup(self):
        self.manager = ActionManager()
        self.manager.dispatcher = Mock()
        self.manager.windowManager = Mock()
        self.manager.registerManager = Mock()

    def test_init(self):
        pass

    def test_parseMap(self):
        result = self.manager.parseMap(self.mapString)
        assert result == self.actionMap

    def test_addMap(self):
        self.manager.addMap(self.mode, self.mapString)
        result = self.manager.actionMaps[self.mode]
        assert result == self.actionMap

    def test_action(self):
        self.manager.addMap(self.mode, self.mapString)
        action = self.manager.action("mmm", "a")
        assert action.__module__ == __name__
        assert action.__class__ == Alpha
        wanted = ("""
        command dispatcher windowManager
        actionManager registerManager
        window buffer cursor motions
            """)
        for word in wanted.split():
            assert word in dir(action)


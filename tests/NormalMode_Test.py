from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.NormalMode import NormalMode

class Mock1:
    buffer = None

class Mock:

    cursor = Mock1()

    def createBuffer(self):
        print("create Buffer called")
        return self.buffer

    def createWindow(self, buffer, cursor):
        print("create  window called")

    def draw(self):
        print("draw called")

    def insertLines(self, y, l):
        print("insertLines called")

class TestNormalMode:

    def setup(self):
        cursor, buffer, window, view = (
                Mock(), Mock(), Mock(), Mock())
        buffer.cursor, window.buffer, view.window = (
                cursor, buffer, window)
        self.fixture = NormalMode(view, buffer)

    def teardown(self):
        pass

    def testInit(self):
        for member in (" view window buffer cursor "
        " command commandMap delegating " " insertMode ").split():
            assert member in dir(self.fixture)

    def testParseCommandMap(self):
        orig = NormalMode.parseCommandMap.__globals__['commandMap']
        NormalMode.parseCommandMap.__globals__['commandMap'] = """
        a: alpha
        b: beta
        """
        self.fixture.commandMap = dict()
        self.fixture.parseCommandMap()
        assert self.fixture.commandMap == {'a': 'alpha', 'b': 'beta'}
        NormalMode.parseCommandMap.__globals__['commandMap'] = orig




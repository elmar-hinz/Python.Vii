# from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.controller.cursor import Cursor
from vii.model.buffer import Buffer
from vii.model.line import Line

class TestCursor:

    def setup(self):
        self.fixture = Cursor()
        text = "line one\nline two\nline three"
        self.fixture.buffer = Buffer(text)

    def teardown(self):
        pass

    def testInit(self):
        assert self.fixture.__class__ == Cursor
        assert self.fixture.buffer.length() == 3
        assert self.fixture.x == 0
        assert self.fixture.y == 0

    def testMoveVertical(self):
        self.fixture.moveVertical(0)
        assert self.fixture.y == 0
        self.fixture.moveVertical(1)
        assert self.fixture.y == 1
        self.fixture.moveVertical(2)
        assert self.fixture.y == 3
        self.fixture.moveVertical(-2)
        assert self.fixture.y == 1

    def testMoveVerticalBounds(self):
        self.fixture.moveVertical(0)
        assert self.fixture.y == 0
        self.fixture.moveVertical(10)
        assert self.fixture.y == 3
        self.fixture.moveVertical(-10)
        assert self.fixture.y == 0

    def testMoveHorizontal(self):
        self.fixture.moveHorizontal(0)
        assert self.fixture.x == 0
        self.fixture.moveHorizontal(1)
        assert self.fixture.x == 1
        self.fixture.moveHorizontal(2)
        assert self.fixture.x == 3
        self.fixture.moveHorizontal(-2)
        assert self.fixture.x == 1

    def testMoveHorizontalBounds(self):
        width = self.fixture.buffer[0].length()
        self.fixture.moveHorizontal(0)
        assert self.fixture.x == 0
        self.fixture.moveHorizontal(50)
        assert self.fixture.x == width
        self.fixture.moveHorizontal(-50)
        assert self.fixture.x == 0

    def testTrackVerticalInsert(self):
        """ insert after: cursor is fix """
        lines = [Line("a"), Line("b")]
        self.fixture.y = 0
        self.fixture.buffer.insert(1, lines)
        self.fixture.trackVerticalInsert(1, len(lines))
        assert self.fixture.y == 0
        """ insert before: cursor moves """
        lines = [Line("a"), Line("b")]
        self.fixture.y = 1
        self.fixture.buffer.insert(1, lines)
        self.fixture.trackVerticalInsert(1, len(lines))
        print(self.fixture.y)
        assert self.fixture.y == 3

    def testTrackHorizontalInsert(self):
        """ insert after: cursor is fix """
        line, insert = self.fixture[0], "xxx"
        self.fixture.x = 0
        line.insert(1, insert)
        self.fixture.trackHorizontalInsert(1, len(insert))
        assert self.fixture.x == 0
        """ insert before: cursor moves """
        self.fixture.x = 1
        line.insert(1, insert)
        self.fixture.trackHorizontalInsert(1, len(insert))
        assert self.fixture.x == 4






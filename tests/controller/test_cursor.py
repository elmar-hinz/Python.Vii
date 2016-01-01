# from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.controller.cursor import Cursor
from vii.signals import *

class BufferMock:
    text = "line one\nline two\nline three".splitlines()

    def getLine(self, index):
        return self.text[index]

    def length(self):
        return len(self.text)

class TestCursor:

    reception = False

    def setup(self):
        self.buffer = BufferMock()
        self.fixture = Cursor(self.buffer)
        slot("cursorMoved", self)
        self.reception = False

    def receive(self, signal, sender):
        if signal == "cursorMoved":
            if sender == self.fixture:
                self.reception = True

    def testInit(self):
        assert self.fixture.__class__ == Cursor
        assert self.fixture.buffer == self.buffer
        assert self.fixture.x == 0
        assert self.fixture.y == 0

    def testUpdate(self):
        self.fixture.update()
        assert self.reception

    def testPosition(self):
        assert self.fixture.position() == (0,0)
        self.fixture.position(1,2)
        assert self.fixture.position() == (1,2)
        assert self.reception

    def testMoveVertical(self):
        self.fixture.moveVertical(0)
        assert self.fixture.y == 0
        self.fixture.moveVertical(2)
        assert self.fixture.y == 2
        self.fixture.moveVertical(-1)
        assert self.fixture.y == 1
        assert self.reception

    def testMoveVerticalBounds(self):
        self.fixture.moveVertical(0)
        assert self.fixture.y == 0
        self.fixture.moveVertical(10)
        assert self.fixture.y == 2
        self.fixture.moveVertical(-10)
        assert self.fixture.y == 0
        assert self.reception

    def testMoveHorizontal(self):
        self.fixture.moveHorizontal(0)
        assert self.fixture.x == 0
        self.fixture.moveHorizontal(1)
        assert self.fixture.x == 1
        self.fixture.moveHorizontal(2)
        assert self.fixture.x == 3
        self.fixture.moveHorizontal(-2)
        assert self.fixture.x == 1
        assert self.reception

    def testMoveHorizontalBounds(self):
        width = len(self.fixture.buffer.getLine(0))
        self.fixture.moveHorizontal(0)
        assert self.fixture.x == 0
        self.fixture.moveHorizontal(50)
        assert self.fixture.x == width
        self.fixture.moveHorizontal(-50)
        assert self.fixture.x == 0
        assert self.reception

    def testTrackHorizontalInsert(self):
        """ insert after: cursor is fix """
        self.fixture.x = 0
        signal("horizontalInsert", self.buffer, 1, 3)
        assert self.fixture.x == 0
        """ insert before: cursor moves up """
        self.fixture.x = 1
        signal("horizontalInsert", self.buffer, 1, 3)
        assert self.fixture.x == 4
        assert self.reception

    def testTrackHorizontalDelete(self):
        """ delete after: cursor is fix """
        self.fixture.x = 0
        signal("horizontalDelete", self.buffer, 1, 2)
        assert self.fixture.x == 0
        """ delete before: cursor moves down """
        self.fixture.x = 5
        signal("horizontalDelete", self.buffer, 1, 2)
        assert self.fixture.x == 3
        """ delete before including cursor """
        """ cursor moves down to position """
        self.fixture.x = 2
        signal("horizontalDelete", self.buffer, 1, 5)
        assert self.fixture.x == 1
        assert self.reception

    def testTrackVerticalInsert(self):
        """ insert after: cursor is fix """
        self.fixture.y = 0
        signal("verticalInsert", self.buffer, 1, 2)
        assert self.fixture.y == 0
        """ insert before: cursor moves up """
        self.fixture.y = 1
        signal("verticalInsert", self.buffer, 1, 1)
        assert self.fixture.y == 2
        assert self.reception

    def testTrackVerticalDelete(self):
        """ delete after: cursor is fix """
        self.fixture.y = 0
        signal("horizontalDelete", self.buffer, 1, 1)
        assert self.fixture.y == 0
        """ delete before: cursor moves down """
        self.fixture.x = 2
        signal("horizontalDelete", self.buffer, 0, 1)
        assert self.fixture.x == 1
        """ delete before including cursor """
        """ cursor moves down to position """
        self.fixture.x = 1
        signal("horizontalDelete", self.buffer, 0, 2)
        assert self.fixture.x == 0
        assert self.reception



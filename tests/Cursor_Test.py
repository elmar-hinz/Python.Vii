# from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.Cursor import Cursor
from vii.Signals import *

class BufferMock:
    text = "line one\nline two\nline three".splitlines()

    def lengthOfLine(self, index):
        return len(self.text[index - 1])

    def copyLines(self, index, count):
        return self.text[index - 1]

    def countOfLines(self):
        return len(self.text)

class MotionsMock:
    pass

class TestCursor:

    reception = False

    def setup(self):
        self.buffer = BufferMock()
        self.motions = MotionsMock()
        self.fixture = Cursor()
        self.fixture.buffer = self.buffer
        self.fixture.motions = self.motions
        slot("cursorMoved", self)
        self.reception = False

    def receive(self, signal, sender):
        if signal == "cursorMoved":
            if sender == self.fixture:
                self.reception = True

    def testInit(self):
        assert self.fixture.__class__ == Cursor
        assert self.fixture.buffer == self.buffer
        assert self.fixture.x == 1
        assert self.fixture.y == 1

    def testUpdate(self):
        self.fixture.updated()
        assert self.reception

    def testPosition(self):
        assert self.fixture.position() == (1,1)
        self.fixture.position(2,3)
        assert self.fixture.position() == (2,3)
        assert self.reception

    def testTrackHorizontalInsert(self):
        """ insert after: cursor is fix """
        self.fixture.x = 1
        signal("horizontalInsert", self.buffer, 2, 3)
        assert self.fixture.x == 1
        """ insert before: cursor moves up """
        self.fixture.x = 2
        signal("horizontalInsert", self.buffer, 2, 3)
        assert self.fixture.x == 5
        assert self.reception

    def testTrackHorizontalDelete(self):
        """ delete after: cursor is fix """
        self.fixture.x = 1
        signal("horizontalDelete", self.buffer, 2, 2)
        assert self.fixture.x == 1
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
        self.fixture.y = 1
        signal("verticalInsert", self.buffer, 2, 2)
        assert self.fixture.y == 1
        """ insert before: cursor moves up """
        self.fixture.y = 2
        signal("verticalInsert", self.buffer, 2, 1)
        assert self.fixture.y == 3
        assert self.reception

    def testTrackVerticalDelete(self):
        """ delete after: cursor is fix """
        self.fixture.y = 1
        signal("horizontalDelete", self.buffer, 1, 1)
        assert self.fixture.y == 1
        """ delete before: cursor moves down """
        self.fixture.x = 3
        signal("horizontalDelete", self.buffer, 2, 1)
        assert self.fixture.x == 2
        """ delete before including cursor """
        """ cursor moves down to position """
        self.fixture.x = 2
        signal("horizontalDelete", self.buffer, 1, 2)
        assert self.fixture.x == 1
        assert self.reception



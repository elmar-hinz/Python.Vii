# from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.controller.cursor import Cursor
from vii.model.buffer import Buffer

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

    def testPosition(self):
        assert self.fixture.position() == (0,0)
        self.fixture.position(1,2)
        assert self.fixture.position() == (1,2)

    def testMoveVertical(self):
        self.fixture.moveVertical(0)
        assert self.fixture.y == 0
        self.fixture.moveVertical(2)
        assert self.fixture.y == 2
        self.fixture.moveVertical(-1)
        assert self.fixture.y == 1

    def testMoveVerticalBounds(self):
        self.fixture.moveVertical(0)
        assert self.fixture.y == 0
        self.fixture.moveVertical(10)
        assert self.fixture.y == 2
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

    def testTrackHorizontalInsert(self):
        """ insert after: cursor is fix """
        self.fixture.x = 0
        self.fixture.trackHorizontalInsert(1, 3)
        assert self.fixture.x == 0
        """ insert before: cursor moves up """
        self.fixture.x = 1
        self.fixture.trackHorizontalInsert(1, 3)
        assert self.fixture.x == 4

    def testTrackHorizontalDelete(self):
        """ delete after: cursor is fix """
        self.fixture.x = 0
        self.fixture.trackHorizontalDelete(1,2)
        assert self.fixture.x == 0
        """ delete before: cursor moves down """
        self.fixture.x = 5
        self.fixture.trackHorizontalDelete(1, 2)
        assert self.fixture.x == 3
        """ delete before including cursor """
        """ cursor moves down to position """
        self.fixture.x = 2
        self.fixture.trackHorizontalDelete(1, 5)
        assert self.fixture.x == 1

    def testTrackVerticalInsert(self):
        """ insert after: cursor is fix """
        self.fixture.y = 0
        self.fixture.trackVerticalInsert(1, 2)
        assert self.fixture.y == 0
        """ insert before: cursor moves up """
        self.fixture.y = 1
        self.fixture.trackVerticalInsert(1, 2)
        assert self.fixture.y == 3

    def testTrackVerticalDelete(self):
        """ delete after: cursor is fix """
        self.fixture.y = 0
        self.fixture.trackHorizontalDelete(1, 1)
        assert self.fixture.y == 0
        """ delete before: cursor moves down """
        self.fixture.x = 2
        self.fixture.trackHorizontalDelete(0, 1)
        assert self.fixture.x == 1
        """ delete before including cursor """
        """ cursor moves down to position """
        self.fixture.x = 1
        self.fixture.trackHorizontalDelete(0, 2)
        assert self.fixture.x == 0



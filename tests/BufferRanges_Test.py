# from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.BufferRanges import BufferRanges

class Dummy():
    text = ["aa", "bbb", "ccccc", "ddd", "ee"]

    def lengthOfLine(self, y):
        return len(self.text[y - 1])

    def countOfLines(self):
        return len(self.text)

class TestBufferRanges:
    def setup(self):
        self.buffer = Dummy()
        self.cursor = Dummy()
        self.fixture = BufferRanges()
        self.fixture.buffer = self.buffer
        self.fixture.cursor = self.cursor
        self.cursor.x = 3
        self.cursor.y = 3

    def testUp(self):
        assert self.fixture.up() == (2,3)
        assert self.fixture.up(2) == (1,2)
        assert self.fixture.up(3) == (1,2)

    def testDown(self):
        assert self.fixture.down() == (4,3)
        assert self.fixture.down(2) == (5,2)
        assert self.fixture.down(3) == (5,2)

    def testLeft(self):
        assert self.fixture.left() == (3,2)
        assert self.fixture.left(2) == (3,1)
        assert self.fixture.left(3) == (3,1)

    def testRight(self):
        assert self.fixture.right() == (3,4)
        assert self.fixture.right(2) == (3,5)
        assert self.fixture.right(3) == (3,5)

    def testBeginningOfBuffer(self):
        assert self.fixture.beginningOfBuffer() == (1, 1)

    def testBeginningOfLine(self):
        assert self.fixture.beginningOfLine() == (3,1)

    def testEndOfBuffer(self):
        assert self.fixture.endOfBuffer() == (5,2)

    def testEndOfLine(self):
        assert self.fixture.endOfLine() == (3,5)
        assert self.fixture.endOfLine(2) == (4,3)


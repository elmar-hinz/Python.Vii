# from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.BufferRanges import BufferRanges

class Dummy():
    text = ["aa", "bbb", "cccc", "ddddd"]

    def lengthOfLine(self, y):
        return len(self.text[y])

    def countOfLines(self):
        return len(self.text)

class TestBufferRanges:

    def setup(self):
        self.buffer = Dummy()
        self.cursor = Dummy()
        self.fixture = BufferRanges(self.buffer, self.cursor)
        self.cursor.x = 2
        self.cursor.y = 2

    def testUp(self):
        assert self.fixture.up() == (1,2)
        assert self.fixture.up(2) == (0,2)

    def testDown(self):
        assert self.fixture.down() == (3,2)
        assert self.fixture.down(2) == (4,2)

    def testLeft(self):
        assert self.fixture.left() == (2,1)
        assert self.fixture.left(2) == (2,0)

    def testRight(self):
        assert self.fixture.right() == (2,3)
        assert self.fixture.right(2) == (2,4)

    def testBeginningOfBuffer(self):
        assert self.fixture.beginningOfBuffer() == (0,0)

    def testBeginningOfLine(self):
        assert self.fixture.beginningOfLine() == (2,0)

    def testEndOfBuffer(self):
        assert self.fixture.endOfBuffer() == (3,4)

    def testEndOfLine(self):
        assert self.fixture.endOfLine() == (2,3)
        print(self.fixture.endOfLine(2))
        assert self.fixture.endOfLine(2) == (3,4)


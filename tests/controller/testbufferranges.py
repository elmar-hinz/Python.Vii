# from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.controller.bufferranges import BufferRanges

class Dummy(): pass

class TestBufferRanges:

    def setup(self):
        self.buffer = ["aa", "bbb", "cccc", "ddddd"]
        self.cursor = Dummy()
        self.fixture = BufferRanges(self.buffer, self.cursor)
        self.cursor.x = 2
        self.cursor.y = 2

    def testUp(self):
        assert self.fixture.up() == (1,2)

    def testDown(self):
        assert self.fixture.down() == (3,2)

    def testLeft(self):
        assert self.fixture.left() == (2,1)

    def testRight(self):
        assert self.fixture.right() == (2,3)

    def testBeginningOfBuffer(self):
        assert self.fixture.beginningOfBuffer() == (0,0)

    def testBeginningOfLine(self):
        assert self.fixture.beginningOfLine() == (2,0)

    def testEndOfBuffer(self):
        assert self.fixture.endOfBuffer() == (3,4)

    def testEndOfLine(self):
        assert self.fixture.endOfLine() == (2,3)


# from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.Motions import Motions
from vii.Range import Range, Position

class Dummy():
    text = ["aa\n", "bbb\n", "ccccc\n", "ddd\n", "ee\n"]

    def lengthOfLine(self, y):
        return len(self.text[y - 1])

    def countOfLines(self):
        return len(self.text)

    def position(self):
        return Position(self.y, self.x)

class Motions_Test:
    def setup(self):
        self.buffer = Dummy()
        self.cursor = Dummy()
        self.fixture = Motions()
        self.fixture.buffer = self.buffer
        self.fixture.cursor = self.cursor
        self.cursor.x = 3
        self.cursor.y = 3

    def range(self, y, x):
        return Range(self.cursor.position().toPosition(), (y, x))

    def test_up(self):
        assert self.fixture.up() == self.range(2,3)
        assert self.fixture.up(2) == self.range(1,2)
        assert self.fixture.up(3) == self.range(1,2)

    def test_down(self):
        assert self.fixture.down() == self.range(4,3)
        assert self.fixture.down(2) == self.range(5,2)
        assert self.fixture.down(3) == self.range(5,2)

    def test_left(self):
        assert self.fixture.left() == self.range(3,2)
        assert self.fixture.left(2) == self.range(3,1)
        assert self.fixture.left(3) == self.range(3,1)

    def test_right(self):
        assert self.fixture.right() == self.range(3,4)
        assert self.fixture.right(2) == self.range(3,5)
        assert self.fixture.right(3) == self.range(3,5)

    def test_beginningOfBuffer(self):
        assert self.fixture.beginningOfBuffer() == self.range(1, 1)

    def test_beginningOfLine(self):
        assert self.fixture.beginningOfLine() == self.range(3,1)

    def test_endOfBuffer(self):
        assert self.fixture.endOfBuffer() == self.range(5,3)

    def test_endOfLine(self):
        assert self.fixture.endOfLine() == self.range(3,5)
        assert self.fixture.endOfLine(2) == self.range(4,3)
        assert self.fixture.endOfLine(4) == self.range(5, 2)


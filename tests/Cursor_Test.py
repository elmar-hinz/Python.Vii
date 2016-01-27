# from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.Cursor import *
from vii.Signals import *

class BufferMock:
    text = "line one\nline two\nline three\n".splitlines()

    def isEmpty(self):
        return len(self.text) == 0

    def lengthOfLine(self, index):
        return len(self.text[index - 1])

    def copyLines(self, index, count):
        return self.text[index - 1]

    def countOfLines(self):
        return len(self.text)

    # def gotoPositionStrict(self, position):
    #     pass

class MotionsMock:

    def gotoPositionStrict(self, position):
        self.targetPosition = position
        if position == Position(1,1):
            " test_delete_all_lines() "
            return Range((0,0), (0,0))
        else:
            " other tests "
            return Range((1,1), (1,1))

class Cursor_Test:

    def setup(self):
        self.buffer = BufferMock()
        self.motions = MotionsMock()
        self.fixture = Cursor()
        self.fixture.x = 1
        self.fixture.y = 1
        self.fixture.buffer = self.buffer
        self.fixture.motions = self.motions
        slot("cursorMoved", self)
        self.cursorMoved = False

    def receive(self, signal, sender):
        if signal == "cursorMoved":
            if sender == self.fixture:
                self.cursorMoved = True

    def test_init(self):
        assert self.fixture.__class__ == Cursor
        assert self.fixture.buffer == self.buffer
        assert self.fixture.motions == self.motions
        assert self.fixture.x == 1
        assert self.fixture.y == 1

    def test_update(self):
        self.fixture.updated()
        assert self.cursorMoved
        # TODO test execptions

    def test_position(self):
        assert self.fixture.position() == Position(1,1)
        assert not self.cursorMoved
        self.fixture.position(Position(2,3))
        assert self.fixture.position() == Position(2,3)
        assert self.cursorMoved

    """ Track insertions """

    def test_insert_vertically_after_cursor(self):
        """ cursor is fix """
        signal("insertedIntoBuffer", self.buffer,
                startPosition = Position(2,1),
                afterPosition = Position(3,1))
        assert self.fixture.position() == Position(1,1)
        assert not self.cursorMoved

    def test_insert_horizontally_after_cursor(self):
        """ cursor is fix """
        signal("insertedIntoBuffer", self.buffer,
                startPosition = Position(1,2),
                afterPosition = Position(1,3))
        assert self.fixture.position() == Position(1,1)
        assert not self.cursorMoved

    def test_insert_vertically_before_cursor(self):
        """ cursor moves down """
        self.fixture.position(Position(3, 2))
        text = "line one\naa\nbb\nline two\nline three\n".splitlines()
        self.buffer.text = text
        signal("insertedIntoBuffer", self.buffer,
                startPosition = Position(2,1),
                afterPosition = Position(4,1))
        assert self.fixture.position() == Position(5,2)
        assert self.cursorMoved

    def test_insert_horizontally_before_cursor(self):
        """ cursor moves right """
        self.fixture.position(Position(2, 4))
        text = "line one\nlxxxine two\nline three\n".splitlines()
        self.buffer.text = text
        signal("insertedIntoBuffer", self.buffer,
                startPosition = Position(2,2),
                afterPosition = Position(2,5))
        assert self.fixture.position() == Position(2, 7)
        assert self.cursorMoved

    def test_insert_before_cursor(self):
        """ cursor moves in both dimensions """
        self.fixture.position(Position(2, 8))
        text = "line one\nline xxx\n\nytwo\nline three\n".splitlines()
        self.buffer.text = text
        signal("insertedIntoBuffer", self.buffer,
                startPosition = Position(2,6),
                afterPosition = Position(4,2))
        assert self.fixture.position() == Position(4, 4)
        assert self.cursorMoved

    """ Track deletions """

    def test_delete_vertically_after_cursor(self):
        """ cursor is fix """
        signal("deletedFromBuffer", self.buffer,
                afterPosition = Position(2,1),
                startPosition = Position(3,1))
        assert self.fixture.position() == Position(1,1)
        assert not self.cursorMoved

    def test_delete_horizontally_after_cursor(self):
        """ cursor is fix """
        signal("deletedFromBuffer", self.buffer,
                afterPosition = Position(1,2),
                startPosition = Position(1,3))
        assert self.fixture.position() == Position(1,1)
        assert not self.cursorMoved

    def test_delete_vertically_before_cursor(self):
        """ cursor moves up """
        text = "line one\naa\nbb\nline two\nline three\n".splitlines()
        self.buffer.text = text
        self.fixture.position(Position(5, 2))
        text = "line one\nline two\nline three\n".splitlines()
        self.buffer.text = text
        signal("deletedFromBuffer", self.buffer,
                afterPosition = Position(2,1),
                startPosition = Position(4,1))
        assert self.fixture.position() == Position(3,2)
        assert self.cursorMoved

    def test_delete_horizontally_before_cursor(self):
        """ cursor moves left """
        text = "line one\nlxxxine two\nline three\n".splitlines()
        self.buffer.text = text
        self.fixture.position(Position(2, 7))
        text = "line one\nline two\nline three\n".splitlines()
        self.buffer.text = text
        signal("deletedFromBuffer", self.buffer,
                afterPosition = Position(2,2),
                startPosition = Position(2,5))
        assert self.fixture.position() == Position(2, 4)
        assert self.cursorMoved

    def test_delete_before_cursor(self):
        """ cursor moves in both dimensions """
        text = "line one\nline xxx\n\nytwo\nline three\n".splitlines()
        self.buffer.text = text
        self.fixture.position(Position(4, 4))
        text = "line one\nline two\nline three\n".splitlines()
        self.buffer.text = text
        signal("deletedFromBuffer", self.buffer,
                afterPosition = Position(2,6),
                startPosition = Position(4,2))
        assert self.fixture.position() == Position(2, 8)
        assert self.cursorMoved

    def test_delete_around_cursor(self):
        " cursor moves in both dimensions "
        text = "line one\nline xxx\nyyy\nzzz two\nline three\n".splitlines()
        self.buffer.text = text
        self.fixture.position(Position(3, 2))
        text = "line one\nline two\nline three\n".splitlines()
        self.buffer.text = text
        signal("deletedFromBuffer", self.buffer,
                afterPosition = Position(2,6),
                startPosition = Position(4,5))
        assert self.motions.targetPosition == Position(2,6)
        assert self.cursorMoved

    def test_delete_last_lines_with_cursor(self):
        " cursor moves to beginning of last line "
        text = "line one\nline two\nline three\n44\n55\n".splitlines()
        self.buffer.text = text
        self.fixture.position(Position(5, 2))
        text = "line one\nline two\nline three\n".splitlines()
        self.buffer.text = text
        signal("deletedFromBuffer", self.buffer,
                afterPosition = Position(4,1),
                startPosition = Position(5,3))
        assert self.motions.targetPosition == Position(4,1)
        assert self.cursorMoved

    def test_delete_all_lines(self):
        " cursor moves to 0, 0 "
        self.fixture.position(Position(2, 2))
        self.buffer.text = []
        signal("deletedFromBuffer", self.buffer,
                afterPosition = Position(1, 1),
                startPosition = Position(4, 1))
        assert self.motions.targetPosition == Position(1,1)
        assert self.fixture.position() == Position(0,0)
        assert self.cursorMoved


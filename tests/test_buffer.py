from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.buffer import *

class TestBuffer:

    def setup(self):
        self.buffer = Buffer()

    def test_init(self):
        assert self.buffer.__class__ == Buffer
        assert self.buffer.updateSignal == "bufferUpdate"
        assert Buffer.updateSignal == "bufferUpdate"
        assert "lines" not in dir(Buffer)
        assert "lines" in dir(self.buffer)

    def test__checkBufferBounds_validInnerRange(self):
        text = "1\n2\n3"
        self.buffer.insertLines(0, text)
        self.buffer._checkBufferBounds(0)
        self.buffer._checkBufferBounds(2)
        assert True

    @raises(BufferBoundsException)
    def test__checkBufferBounds_negativeException(self):
        text = "1\n2\n3"
        self.buffer.insertLines(0, text)
        self.buffer._checkBufferBounds(-1)

    @raises(BufferBoundsException)
    def test__checkBufferBounds_positiveException(self):
        text = "1\n2\n3"
        self.buffer.insertLines(0, text)
        self.buffer._checkBufferBounds(3)

    def test__checkBufferBoundsPlus1_validInnerRange(self):
        text = "1\n2\n3"
        self.buffer.insertLines(0, text)
        self.buffer._checkBufferBoundsPlus1(0)
        self.buffer._checkBufferBoundsPlus1(3)
        assert True

    @raises(BufferBoundsException)
    def test__checkBufferBoundsPlus1_negativeException(self):
        text = "1\n2\n3"
        self.buffer.insertLines(0, text)
        self.buffer._checkBufferBoundsPlus1(-1)

    @raises(BufferBoundsException)
    def test__checkBufferBoundsPlus1_positiveException(self):
        text = "1\n2\n3"
        self.buffer.insertLines(0, text)
        self.buffer._checkBufferBoundsPlus1(4)

    def test_countOfLines(self):
        text = "1\n2\n3"
        self.buffer.insertLines(0, text)
        assert self.buffer.countOfLines() == 3

    def test_lengthOfLine(self):
        text = "1\n22\n333"
        self.buffer.insertLines(0, text)
        assert self.buffer.lengthOfLine(2) == 3

    def test_copyLines(self):
        text = "1\n2\n3\n4"
        self.buffer.insertLines(0, text)
        assert self.buffer.copyLines(1, 2) == "2\n3"
        assert self.buffer.copyLines(0, 4) == text

    def test_copyFromLine(self):
        text = "1\n123"
        self.buffer.insertLines(0, text)
        assert self.buffer.copyFromLine((1,0),3) == "123"

    def test_copyRange_inLine(self):
        text = "abc\ndef\nghi"
        self.buffer.insertLines(0, text)
        expect = "e"
        assert self.buffer.copyRange((1,1), (1,1)) == expect
        expect = "def"
        assert self.buffer.copyRange((1,0), (1,2)) == expect

    def test_copyRange_withoutBody(self):
        text = "abc\ndef\nghi\njkl"
        self.buffer.insertLines(0, text)
        expect = "ef\ngh"
        assert self.buffer.copyRange((1,1), (2,1)) == expect

    def test_copyRange_withBody(self):
        text = "abc\ndef\nghi\njkl"
        self.buffer.insertLines(0, text)
        expect = "ef\nghi\njk"
        assert self.buffer.copyRange((1,1), (3,1)) == expect

    def test_copyRangeSingleChar(self):
        text = "abc\ndef\nghi\njkl"
        self.buffer.insertLines(0, text)
        expect = "e"
        assert self.buffer.copyRange((1,1), (1,1)) == expect

    def test_parse(self):
        text = "1\n2\n3"
        expect = ['1', '2', '3']
        assert self.buffer._parse(text) == expect

    def test_insertLinesWhenEmpty(self):
        text = "1\n2\n3"
        expect = "1\n2\n3"
        self.buffer.insertLines(0, text)
        assert str(self.buffer) == expect

    def test_insertLinesBetween(self):
        prefill = "1\n2\n3"
        text = "a\nb"
        expect = "1\na\nb\n2\n3"
        self.buffer.insertLines(0, prefill)
        self.buffer.insertLines(1, text)
        assert str(self.buffer) == expect

    def test_insertLinesOnTop(self):
        prefill = "1\n2\n3"
        text = "a\nb"
        expect = "a\nb\n1\n2\n3"
        self.buffer.insertLines(0, prefill)
        self.buffer.insertLines(0, text)
        assert str(self.buffer) == expect

    def test_insertLinesAtBottom(self):
        prefill = "1\n2\n3"
        text = "a\nb"
        expect = "1\n2\n3\na\nb"
        self.buffer.insertLines(0, prefill)
        self.buffer.insertLines(3, text)
        assert str(self.buffer) == expect



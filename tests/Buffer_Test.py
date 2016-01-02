from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.Buffer import *

class TestBuffer:

    def setup(self):
        self.buffer = Buffer()

    def test_init(self):
        assert self.buffer.__class__ == Buffer
        assert self.buffer.updateSignal == "bufferUpdate"
        assert Buffer.updateSignal == "bufferUpdate"
        assert "lines" not in dir(Buffer)
        assert "lines" in dir(self.buffer)

    """ utilities """

    def test__parse(self):
        text = "1\n2\n\n4"
        expect = ["1", "2", "", "4"]
        assert self.buffer._parse(text) == expect

    def test__parse_emptyString(self):
        text = ""
        expect = [""]
        assert self.buffer._parse(text) == expect

    def test__parse_newline(self):
        text = "\n"
        expect = ["", ""]
        assert self.buffer._parse(text) == expect

    def test__join(self):
        expect = "1\n2\n\n4"
        lines = ["1", "2", "", "4"]
        assert self.buffer._join(lines) == expect

    def test_countOfLines(self):
        text = "1\n2\n3"
        self.buffer.fill(text)
        assert self.buffer.countOfLines() == 3

    def test_lengthOfLine(self):
        text = "1\n22\n333"
        self.buffer.fill(text)
        assert self.buffer.lengthOfLine(2) == 3

    def test_fill(self):
        text = "1\n2\n3"
        text2 = "a\nb"
        self.buffer.fill(text)
        assert str(self.buffer) == text
        self.buffer.fill(text2)
        assert str(self.buffer) == text2


    """ checking """

    """ TODO: line checks """
    """ TODO: range checks """

    def test__checkBufferBounds_validInnerRange(self):
        text = "1\n2\n3"
        self.buffer.fill(text)
        self.buffer._checkBufferBounds(0)
        self.buffer._checkBufferBounds(2)
        assert True

    @raises(BufferBoundsException)
    def test__checkBufferBounds_negativeException(self):
        text = "1\n2\n3"
        self.buffer.fill(text)
        self.buffer._checkBufferBounds(-1)

    @raises(BufferBoundsException)
    def test__checkBufferBounds_positiveException(self):
        text = "1\n2\n3"
        self.buffer.fill(text)
        self.buffer._checkBufferBounds(3)

    def test__checkBufferBoundsPlus1_validInnerRange(self):
        text = "1\n2\n3"
        self.buffer.fill(text)
        self.buffer._checkBufferBoundsPlus1(0)
        self.buffer._checkBufferBoundsPlus1(3)
        assert True

    @raises(BufferBoundsException)
    def test__checkBufferBoundsPlus1_negativeException(self):
        text = "1\n2\n3"
        self.buffer.fill(text)
        self.buffer._checkBufferBoundsPlus1(-1)

    @raises(BufferBoundsException)
    def test__checkBufferBoundsPlus1_positiveException(self):
        text = "1\n2\n3"
        self.buffer.fill(text)
        self.buffer._checkBufferBoundsPlus1(4)

    """ copying """

    def test_copyLines(self):
        text = "1\n2\n3\n4"
        self.buffer.fill(text)
        assert self.buffer.copyLines(1, 2) == "2\n3"

    def test_copyAllLines(self):
        text = "1\n2\n3\n4"
        self.buffer.fill(text)
        assert self.buffer.copyLines(0, 4) == text

    def test_copyNullLines(self):
        text = "1\n2\n3\n4"
        self.buffer.fill(text)
        assert self.buffer.copyLines(0, 0) == ""

    def test_copyFromLine(self):
        text = "1\n1234"
        self.buffer.fill(text)
        assert self.buffer.copyFromLine((1,1),2) == "23"

    def test_copyAllFromLine(self):
        text = "1\n1234"
        self.buffer.fill(text)
        assert self.buffer.copyFromLine((1,0),4) == "1234"

    def test_copyNullFromLine(self):
        text = "1\n123"
        self.buffer.fill(text)
        assert self.buffer.copyFromLine((0,0),0) == ""

    def test_copyRange_inLine(self):
        text = "abc\ndef\nghi"
        self.buffer.fill(text)
        expect = "e"
        assert self.buffer.copyRange((1,1), (1,1)) == expect
        expect = "def"
        assert self.buffer.copyRange((1,0), (1,2)) == expect

    def test_copyRange_withoutBody(self):
        text = "abc\ndef\nghi\njkl"
        self.buffer.fill(text)
        expect = "ef\ngh"
        assert self.buffer.copyRange((1,1), (2,1)) == expect

    def test_copyRange_withBody(self):
        text = "abc\ndef\nghi\njkl"
        self.buffer.fill(text)
        expect = "ef\nghi\njk"
        assert self.buffer.copyRange((1,1), (3,1)) == expect

    def test_copyRange_onlyBody(self):
        text = "abc\ndef\nghi\njkl"
        self.buffer.fill(text)
        expect = "def\nghi"
        assert self.buffer.copyRange((1,0), (2,2)) == expect

    def test_copyRangeSingleChar(self):
        text = "abc\ndef\nghi\njkl"
        self.buffer.fill(text)
        expect = "e"
        assert self.buffer.copyRange((1,1), (1,1)) == expect

    """ deleting """

    def test_deleteLines(self):
        text = "1\n2\n3\n4"
        expect = "1\n4"
        self.buffer.fill(text)
        self.buffer.deleteLines(1, 2)
        assert str(self.buffer) == expect

    def test_deleteAllLines(self):
        text = "1\n2\n3\n4"
        expect = ""
        self.buffer.fill(text)
        self.buffer.deleteLines(0, 4)
        assert str(self.buffer) == expect

    def test_deleteNullLines(self):
        text = "1\n2\n3\n4"
        expect = text
        self.buffer.fill(text)
        self.buffer.deleteLines(0, 0)
        assert str(self.buffer) == expect

    def test_deleteFromLine(self):
        text = "0\nabcde\n3"
        expect = "0\nade\n3"
        self.buffer.fill(text)
        self.buffer.deleteFromLine((1,1),2)
        assert str(self.buffer) == expect

    def test_deleteAllFromLine(self):
        text = "0\nabcde\n3"
        expect = "0\n\n3"
        self.buffer.fill(text)
        self.buffer.deleteFromLine((1,0),5)
        assert str(self.buffer) == expect

    def test_deleteNullFromLine(self):
        text = "0\nabcde\n3"
        expect = text
        self.buffer.fill(text)
        self.buffer.deleteFromLine((0,0),0)
        assert str(self.buffer) == expect

    def test_deleteRange_inLine(self):
        text = "abc\ndef\nghi"
        self.buffer.fill(text)
        expect = "abc\ndf\nghi"
        self.buffer.deleteRange((1,1), (1,1))
        assert str(self.buffer) == expect
        text = "abc\ndef\nghi"
        self.buffer.fill(text)
        expect = "abc\n\nghi"
        self.buffer.deleteRange((1,0), (1,2))
        assert str(self.buffer) == expect

    def test_deleteRange_withoutBody(self):
        text = "abc\ndef\nghi\njkl"
        self.buffer.fill(text)
        expect = "abc\ndi\njkl"
        self.buffer.deleteRange((1,1), (2,1))
        assert str(self.buffer) == expect

    def test_deleteRange_withBody(self):
        text = "abc\ndef\nghi\njkl"
        self.buffer.fill(text)
        expect = "al"
        self.buffer.deleteRange((0,1), (3,1))
        assert str(self.buffer) == expect

    def test_deleteRange_onlyBody(self):
        text = "abc\ndef\nghi\njkl"
        self.buffer.fill(text)
        expect = "abc\n\njkl"
        self.buffer.deleteRange((1,0), (2,2))
        assert str(self.buffer) == expect

    """ inserting """

    def test_insertLinesWhenEmpty(self):
        text = "1\n2\n3"
        expect = "1\n2\n3"
        self.buffer.insertLines(0, text)
        assert str(self.buffer) == expect

    def test_insertLinesBetween(self):
        prefill = "1\n2\n3"
        text = "a\nb"
        expect = "1\na\nb\n2\n3"
        self.buffer.fill(prefill)
        self.buffer.insertLines(1, text)
        assert str(self.buffer) == expect

    def test_insertLinesOnTop(self):
        prefill = "1\n2\n3"
        text = "a\nb"
        expect = "a\nb\n1\n2\n3"
        self.buffer.fill(prefill)
        self.buffer.insertLines(0, text)
        assert str(self.buffer) == expect

    def test_insertLinesAtBottom(self):
        prefill = "1\n2\n3"
        text = "a\nb"
        expect = "1\n2\n3\na\nb"
        self.buffer.fill(prefill)
        self.buffer.insertLines(3, text)
        assert str(self.buffer) == expect

    def test_insertLines_leadingNewline(self):
        prefill = "1\n2\n3"
        text = "\n5"
        expect = "1\n2\n3\n\n5"
        self.buffer.fill(prefill)
        self.buffer.insertLines(3, text)
        assert str(self.buffer) == expect

    def test_insertLines_trailingNewline(self):
        prefill = "1\n2\n3"
        text = "4\n"
        expect = "1\n2\n3\n4\n"
        self.buffer.fill(prefill)
        self.buffer.insertLines(3, text)
        assert str(self.buffer) == expect

    def test_insertLines_singleNewline(self):
        prefill = "1\n2\n3"
        text = "\n"
        expect = "1\n2\n3\n\n"
        self.buffer.fill(prefill)
        self.buffer.insertLines(3, text)
        assert str(self.buffer) == expect

    def test_insert_empty_string(self):
        prefill = "1\n22\n3"
        text = ""
        expect = "1\n22\n3"
        self.buffer.fill(prefill)
        self.buffer.insert((1,1), text)
        assert str(self.buffer) == expect

    def test_insert_simple_string(self):
        prefill = "1\n22\n3"
        text = "aa"
        expect = "1\n2aa2\n3"
        self.buffer.fill(prefill)
        self.buffer.insert((1,1), text)
        assert str(self.buffer) == expect

    def test_insert_newline(self):
        prefill = "1\n22\n3"
        text = "\n"
        expect = "1\n2\n2\n3"
        self.buffer.fill(prefill)
        self.buffer.insert((1,1), text)
        assert str(self.buffer) == expect

    def test_insert_surrounding_newlines(self):
        prefill = "1\n22\n3"
        text = "\naa\n"
        expect = "1\n2\naa\n2\n3"
        self.buffer.fill(prefill)
        self.buffer.insert((1,1), text)
        assert str(self.buffer) == expect

    def test_insertWithoutBody(self):
        prefill = "1\n22\n3"
        text = "aa\nbb"
        expect = "1\n2aa\nbb2\n3"
        self.buffer.fill(prefill)
        self.buffer.insert((1,1), text)
        assert str(self.buffer) == expect

    def test_insertWithBody(self):
        prefill = "1\n22\n3"
        text = "aa\nbb\ncc"
        expect = "1\n2aa\nbb\ncc2\n3"
        self.buffer.fill(prefill)
        self.buffer.insert((1,1), text)
        assert str(self.buffer) == expect


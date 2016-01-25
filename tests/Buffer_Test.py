from nose.tools import *
from vii.Buffer import *
from vii.Signals import slot

class Receiver:

    def __init__(self):
        slot("updatedBuffer", self)
        slot("filledBuffer", self)
        slot("deletedFromBuffer", self)
        slot("insertedIntoBuffer", self)
        self.seen = {}

    def receive(self, signal, sender, **args):
        self.seen[signal] = args

class Buffer_Test:

    def fillAndClear(self, text):
        self.buffer.fill(text)
        self.signals.clear()

    def setup(self):
        self.receiver = Receiver()
        self.signals = self.receiver.seen
        self.buffer = Buffer()

    def test_init(self):
        assert self.buffer.__class__ == Buffer
        assert Buffer.updatedSignal == "updatedBuffer"
        assert Buffer.filledSignal == "filledBuffer"
        assert Buffer.deletedSignal == "deletedFromBuffer"
        assert Buffer.insertedSignal == "insertedIntoBuffer"
        assert "lines" not in dir(Buffer)
        assert self.buffer.lines == []
        assert "updatedBuffer" in self.signals

    """ utilities """

    def test__parse_emptyString(self):
        assert self.buffer._parse("") == []
        assert self.buffer._join([]) == ""

    def test__parse_nl(self):
        assert self.buffer._parse("\n") == ["\n"]
        assert self.buffer._join(["\n"]) == "\n"

    def test__parse_x(self):
        assert self.buffer._parse("x") == ["x"]
        assert self.buffer._join(["x"]) == "x"

    def test__parse_xnl(self):
        assert self.buffer._parse("x\n") == ["x\n"]

    def test__parse_xnlx(self):
        assert self.buffer._parse("x\nx") == ["x\n", "x"]
        assert self.buffer._join(["x\n", "x"]) == "x\nx"

    def test__parse_xnlxnl(self):
        assert self.buffer._parse("x\nx\n") == ["x\n", "x\n"]

    def test__parse_withEmptyLine(self):
        text = "\n2\n3\n"
        expect = ["\n", "2\n", "3\n"]
        assert self.buffer._parse(text) == expect
        assert self.buffer._join(expect) == text
        text = "1\n\n\n4\n"
        expect = ["1\n", "\n", "\n", "4\n"]
        assert self.buffer._parse(text) == expect
        assert self.buffer._join(expect) == text
        text = "1\n2\n\n"
        expect = ["1\n", "2\n", "\n"]
        assert self.buffer._parse(text) == expect
        assert self.buffer._join(expect) == text

    def test_fill(self):
        self.signals.clear()
        self.buffer.fill("")
        assert self.buffer.lines == []
        assert not "filledBuffer" in self.signals
        assert not "updatedBuffer" in self.signals
        self.buffer.fill("\n")
        assert self.buffer.lines == ["\n"]
        self.buffer.fill("x\n")
        assert self.buffer.lines == ["x\n"]

    def test__resolve_range_lines(self):
        text = "1\n22\n333\n"
        self.buffer.fill(text)
        range = Range((2,None), (2,None))
        resolved = self.buffer._resolveRange(range)
        assert resolved == Range((2,1), (2,3))
        range = Range((1,None), (2,None))
        resolved = self.buffer._resolveRange(range)
        assert resolved == Range((1,1), (2,3))
        range = Range((3,None), (2,None))
        resolved = self.buffer._resolveRange(range)
        assert resolved == Range((2,1), (3,4))

    def test__resolve_range_in_line(self):
        range = Range((2,2), (2,2))
        resolved = self.buffer._resolveRange(range)
        assert resolved == range
        range = Range((2,1), (2,2))
        resolved = self.buffer._resolveRange(range)
        assert resolved == range
        range = Range((2,2), (2,1))
        resolved = self.buffer._resolveRange(range)
        assert resolved == Range((2,1), (2,2))

    def test__resolve_range_positions(self):
        range = Range((1,2), (2,2))
        resolved = self.buffer._resolveRange(range)
        assert resolved == range
        range = Range((2,2), (1,1))
        resolved = self.buffer._resolveRange(range)
        assert resolved == Range((1,1), (2,2))

    """ statistics """

    def test_isEmpty(self):
        assert self.buffer.isEmpty()
        self.buffer.fill("")
        assert self.buffer.isEmpty()
        self.buffer.fill("\n")
        assert not self.buffer.isEmpty()

    def test_characterCount(self):
        self.buffer.fill("")
        assert self.buffer.characterCount() == 0
        self.buffer.fill("\n")
        assert self.buffer.characterCount() == 1
        self.buffer.fill("\n\n")
        assert self.buffer.characterCount() == 2
        self.buffer.fill("x\n")
        assert self.buffer.characterCount() == 2

    def test_countOfLines(self):
        text = "1\n2\n3\n"
        self.buffer.fill(text)
        assert self.buffer.countOfLines() == 3

    def test_lengthOfLine(self):
        " Does contain linebreaks "
        text = "1\n22\n333\n"
        self.buffer.fill(text)
        assert self.buffer.lengthOfLine(3) == 4

    """ checking """

    # """ TODO: line checks """
    # """ TODO: range checks """

    def test__checkBufferBounds_validInnerRange(self):
        text = "1\n2\n3\n"
        self.buffer.fill(text)
        self.buffer._checkBufferBounds(1)
        self.buffer._checkBufferBounds(3)
        assert True

    @raises(BufferBoundsException)
    def test__checkBufferBounds_negativeException(self):
        text = "1\n2\n3\n"
        self.buffer.fill(text)
        self.buffer._checkBufferBounds(0)

    @raises(BufferBoundsException)
    def test__checkBufferBounds_positiveException(self):
        text = "1\n2\n3\n"
        self.buffer.fill(text)
        self.buffer._checkBufferBounds(4)

    def test__checkBufferBounds_plus1_validInnerRange(self):
        text = "1\n2\n3\n"
        self.buffer.fill(text)
        self.buffer._checkBufferBounds(4, plus = 1)
        assert True

    @raises(BufferBoundsException)
    def test__checkBufferBounds_plus1_positiveException(self):
        text = "1\n2\n3\n"
        self.buffer.fill(text)
        self.buffer._checkBufferBounds(5, plus = 1)

    """ copying """

    def test_copy_lines(self):
        text = "1\n22\n3\n44\n5\n66\n"
        self.buffer.fill(text)
        result = self.buffer.copy(Range(1, 1))
        assert result == "1\n"
        result = self.buffer.copy(Range(2, 2))
        assert result == "22\n"
        result = self.buffer.copy(Range(6, 6))
        assert result == "66\n"
        result = self.buffer.copy(Range(1, 2))
        assert result == "1\n22\n"
        result = self.buffer.copy(Range(1, 6))
        assert result == text
        result = self.buffer.copy(Range(6, 1))
        assert result == text
        result = self.buffer.copy(Range(2, 5))
        assert result == "22\n3\n44\n5\n"
        result = self.buffer.copy(Range(5, 2))
        assert result == "22\n3\n44\n5\n"

    def test_copy_from_line(self):
        text = "1\n1234\n"
        self.buffer.fill(text)
        result = self.buffer.copy(Range((1,1), (1,1)))
        assert result == "1"
        result = self.buffer.copy(Range((2,4), (2,4)))
        assert result == "4"
        result = self.buffer.copy(Range((2,5), (2,5)))
        assert result == "\n"
        result = self.buffer.copy(Range((2,2), (2,2)))
        assert result == "2"
        result = self.buffer.copy(Range((2,2), (2,4)))
        assert result == "234"
        result = self.buffer.copy(Range((2,4), (2,2)))
        assert result == "234"
        result = self.buffer.copy(Range((1,1), (1,2)))
        assert result == "1\n"
        result = self.buffer.copy(Range((2,2), (2,5)))
        assert result == "234\n"
        result = self.buffer.copy(Range((2,1), (2,5)))
        assert result == "1234\n"

    def test_copy_from_range(self):
        text = "1\n22\n333\n4444\n555555\n666666\n"
        self.buffer.fill(text)
        result = self.buffer.copy(Range((1,1), (6,7)))
        assert result == text
        result = self.buffer.copy(Range((2,2), (3,1)))
        assert result == "2\n3"
        result = self.buffer.copy(Range((2,2), (3,4)))
        assert result == "2\n333\n"
        result = self.buffer.copy(Range((2,2), (5,1)))
        assert result == "2\n333\n4444\n5"
        result = self.buffer.copy(Range((2,3), (3,1)))
        assert result == "\n3"

    """ deleting """

    def deleted(self, key):
        return self.signals["deletedFromBuffer"][key]

    """ deleting linewise """

    def test_delete_first_line(self):
        text = "1\n22\n3\n44\n5\n66\n"
        self.fillAndClear(text)
        self.buffer.delete(Range(1, 1))
        assert self.buffer.lines == ['22\n', '3\n', '44\n', '5\n', '66\n']
        assert self.deleted("startPosition") == Position(1,1)
        assert self.deleted("afterPosition") == Position(2,1)
        assert self.deleted("deltaX") == 0
        assert "updatedBuffer" in self.signals

    def test_delete_intermediate_line(self):
        text = "1\n22\n3\n44\n5\n66\n"
        self.fillAndClear(text)
        self.buffer.delete(Range(2, 2))
        assert self.buffer.lines == ['1\n', '3\n', '44\n', '5\n', '66\n']
        assert self.deleted("afterPosition") == Position(3,1)
        assert self.deleted("deltaX") == 0

    def test_delete_last_line(self):
        text = "1\n22\n3\n44\n5\n66\n"
        self.fillAndClear(text)
        self.buffer.delete(Range(6, 6))
        assert self.buffer.lines == ['1\n', '22\n', '3\n', '44\n', '5\n']
        assert self.deleted("afterPosition") == Position(7,1)
        assert self.deleted("deltaX") == 0

    def test_delete_muliple_lines_at_start(self):
        text = "1\n22\n3\n44\n5\n66\n"
        self.fillAndClear(text)
        self.buffer.delete(Range(1, 2))
        assert self.buffer.lines == ['3\n', '44\n', '5\n', '66\n']
        assert self.deleted("afterPosition") == Position(3,1)
        assert self.deleted("deltaX") == 0

    def test_delete_muliple_lines_inversed(self):
        text = "1\n22\n3\n44\n5\n66\n"
        self.fillAndClear(text)
        self.buffer.delete(Range(5, 2))
        assert self.buffer.lines == ['1\n', '66\n']
        assert self.deleted("afterPosition") == Position(6,1)
        assert self.deleted("deltaX") == 0

    def test_delete_muliple_lines_at_end(self):
        text = "1\n22\n3\n44\n5\n66\n"
        self.fillAndClear(text)
        self.buffer.delete(Range(5, 6))
        assert self.buffer.lines == ['1\n', '22\n', '3\n', '44\n']
        assert self.deleted("afterPosition") == Position(7,1)
        assert self.deleted("deltaX") == 0

    def test_delete_all_lines(self):
        text = "1\n22\n3\n44\n5\n66\n"
        self.fillAndClear(text)
        self.buffer.delete(Range(1, 6))
        assert str(self.buffer) == ""
        assert self.buffer.lines == []
        assert self.deleted("afterPosition") == Position(7,1)
        assert self.deleted("deltaX") == 0

    def test_delete_all_lines_inversed(self):
        text = "1\n22\n3\n44\n5\n66\n"
        self.fillAndClear(text)
        self.buffer.delete(Range(6, 1))
        assert str(self.buffer) == ""
        assert self.buffer.lines == []
        assert self.deleted("afterPosition") == Position(7,1)
        assert self.deleted("deltaX") == 0

    """ deleting inside line """

    def test_delete_first_sign_in_line(self):
        text = "1\n1234\n"
        self.fillAndClear(text)
        self.buffer.delete(Position(1,1))
        assert self.buffer.lines == ["\n", "1234\n"]
        assert self.deleted("startPosition") == Position(1,1)
        assert self.deleted("afterPosition") == Position(1,2)
        assert self.deleted("deltaX") == -1

    def test_delete_last_sign_in_line(self):
        text = "1\n1234\n"
        self.fillAndClear(text)
        self.buffer.delete(Range((1,2), (1,2)))
        assert self.buffer.lines == ["11234\n"]
        assert self.deleted("afterPosition") == Position(2,1)
        assert self.deleted("deltaX") == +1

    def test_delete_in_line_without_bounds(self):
        text = "1\n1234\n"
        self.fillAndClear(text)
        self.buffer.delete(Range((2,1), (2,4)))
        assert self.buffer.lines == ["1\n", "\n"]
        assert self.deleted("afterPosition") == Position(2,5)
        assert self.deleted("deltaX") == -4

    @raises(LastLinebreakLostExecption)
    def test_delete_last_singn_in_last_line_excepts(self):
        text = "1\n1234\n"
        self.buffer.fill(text)
        self.buffer.delete(Position(2,5))

    @raises(LastLinebreakLostExecption)
    def test_delete_last_singns_in_last_line_excepts(self):
        text = "1\n1234\n"
        self.buffer.fill(text)
        self.buffer.delete(Range((2,2), (2,5)))

    """ deleting mulitline ranges """

    def test_delete_from_range_of_end_of_lines(self):
        text = "1\n22\n333\n4444\n55555\n666666\n"
        self.buffer.fill(text)
        self.buffer.delete(Range((2,3), (5,6)))
        assert self.buffer.lines == ["1\n", "22666666\n"]
        assert self.deleted("afterPosition") == Position(6,1)
        assert self.deleted("deltaX") == +2

    def test_delete_from_range_amidst_lines(self):
        text = "1\n22\n333\n4444\n55555\n666666\n"
        self.buffer.fill(text)
        self.buffer.delete(Range((2,2), (3,2)))
        assert self.buffer.lines == ['1\n', '23\n', '4444\n', '55555\n', '666666\n']
        assert self.deleted("afterPosition") == Position(3,3)
        assert self.deleted("deltaX") == -1

    def test_delete_from_range_amidst_lines_inversed(self):
        text = "1\n22\n333\n4444\n55555\n666666\n"
        self.buffer.fill(text)
        self.buffer.delete(Range((3,2), (2,2)))
        assert self.buffer.lines == ['1\n', '23\n', '4444\n', '55555\n', '666666\n']
        assert self.deleted("afterPosition") == Position(3,3)
        assert self.deleted("deltaX") == -1

    def test_delete_from_range_amidst_to_end(self):
        text = "1\n22\n333\n4444\n55555\n666666\n"
        self.buffer.fill(text)
        self.buffer.delete(Range((2,2), (5,6)))
        assert self.buffer.lines == ['1\n', '2666666\n']
        assert self.deleted("afterPosition") == Position(6,1)
        assert self.deleted("deltaX") == +1

    def test_delete_from_range_end_to_amidst(self):
        text = "1\n22\n333\n4444\n55555\n666666\n"
        self.buffer.fill(text)
        self.buffer.delete(Range((2,3), (5,2)))
        assert self.buffer.lines == ['1\n', '22555\n', '666666\n']
        assert self.deleted("afterPosition") == Position(5,3)
        assert self.deleted("deltaX") == 0

    """ inserting """
    def inserted(self, key):
        return self.signals["insertedIntoBuffer"][key]

    def test_insert_lines_when_empty(self):
        text = "1\n2\n3\n"
        expect = ['1\n', '2\n', '3\n']
        self.buffer.insert(Position(1,1), text)
        assert self.buffer.lines == expect
        assert "updatedBuffer" in self.signals
        assert self.inserted("startPosition") == Position(1,1)

    def test_insert_lines_between(self):
        prefill = "11\n22\n33\n"
        text = "aa\nbb\n"
        expect = ['11\n', 'aa\n', 'bb\n', '22\n', '33\n']
        self.fillAndClear(prefill)
        self.buffer.insert(Position(2,1), text)
        assert self.buffer.lines == expect
        assert self.inserted("afterPosition") == Position(4,1)
        assert self.inserted("deltaX") == 0

    def test_insert_lines_on_top(self):
        prefill = "1\n2\n3\n"
        text = "a\nb\n"
        expect = ['a\n', 'b\n', '1\n', '2\n', '3\n']
        self.fillAndClear(prefill)
        self.buffer.insert(Position(1,1), text)
        assert self.buffer.lines == expect
        assert self.inserted("afterPosition") == Position(3,1)
        assert self.inserted("deltaX") == 0

    def test_insert_lines_at_bottom(self):
        prefill = "1\n2\n3\n"
        text = "a\nb\n"
        expect = ['1\n', '2\n', '3\n', 'a\n', 'b\n']
        self.fillAndClear(prefill)
        self.buffer.insert(Position(4,1), text)
        assert self.buffer.lines == expect

    @raises(LastLinebreakLostExecption)
    def test_insert_line_into_empty_buffer_without_nl(self):
        prefill = ""
        text = "abc"
        self.fillAndClear(prefill)
        self.buffer.insert(Position(1,1), text)

    @raises(LastLinebreakLostExecption)
    def test_insert_line_at_bottom_without_nl(self):
        prefill = "a\n"
        text = "abc"
        self.fillAndClear(prefill)
        self.buffer.insert(Position(2,1), text)

    @raises(LastLinebreakLostExecption)
    def test_insert_lines_at_bottom_without_nl(self):
        prefill = "1\n2\n3\n"
        text = "a\nb"
        self.fillAndClear(prefill)
        self.buffer.insert(Position(4,1), text)

    def test_insert_single_line(self):
        prefill = "11\n22\n33\n"
        text = "bb\n"
        expect = ['11\n', '\n', 'bb\n', '22\n', '33\n']
        self.fillAndClear(prefill)
        self.buffer.insert(Position(2,1), "bb\n")
        self.buffer.insert(Position(2,1), "\n")
        assert self.buffer.lines == expect
        assert self.inserted("afterPosition") == Position(3,1)
        assert self.inserted("deltaX") == 0

    def test_insert_empty_lines(self):
        prefill = "1\n2\n"
        text = "\n\n"
        self.fillAndClear(prefill)
        self.buffer.insert(Position(1,1), text)
        assert self.inserted("afterPosition") == Position(3,1)
        assert self.inserted("deltaX") == 0
        # print(self.buffer.lines)
        self.buffer.insert(Position(4,1), text)
        assert self.inserted("afterPosition") == Position(6,1)
        assert self.inserted("deltaX") == 0
        self.buffer.insert(Position(7,1), text)
        expect = ['\n', '\n', '1\n', '\n', '\n', '2\n', '\n', '\n']
        assert self.buffer.lines == expect

    def test_insert_empty_string(self):
        prefill = "1\n22\n3\n"
        text = ""
        expect = "1\n22\n3\n"
        self.fillAndClear(prefill)
        self.buffer.insert(Position(2,2), text)
        assert str(self.buffer) == expect
        assert not "updatedBuffer" in self.signals

    def test_insert_simple_string(self):
        prefill = "1\n22\n3\n"
        text = "aa"
        expect = ['1\n', '2aa2\n', '3\n']
        self.fillAndClear(prefill)
        self.buffer.insert(Position(2,2), text)
        assert self.buffer.lines == expect
        assert self.inserted("afterPosition") == Position(2,4)
        assert self.inserted("deltaX") == 2

    def test_insert_at_begin_of_line(self):
        prefill = "1\n22\n3\n"
        text = "aa"
        expect = ['1\n', 'aa22\n', '3\n']
        self.fillAndClear(prefill)
        self.buffer.insert(Position(2,1), text)
        assert self.buffer.lines == expect
        assert self.inserted("afterPosition") == Position(2,3)
        assert self.inserted("deltaX") == 2

    def test_insert_newline_at_begin_of_line(self):
        prefill = "1\n22\n3\n"
        text = "\n"
        expect = ['1\n', '\n', '22\n', '3\n']
        self.fillAndClear(prefill)
        self.buffer.insert(Position(2,1), text)
        assert self.buffer.lines == expect
        assert self.inserted("afterPosition") == Position(3,1)
        assert self.inserted("deltaX") == 0

    def test_insert_at_end_of_line(self):
        prefill = "1\n22\n3\n"
        text = "aa"
        expect = ['1\n', '22aa\n', '3\n']
        self.fillAndClear(prefill)
        self.buffer.insert(Position(2,3), text)
        assert self.buffer.lines == expect
        assert self.inserted("afterPosition") == Position(2,5)
        assert self.inserted("deltaX") == 2

    def test_insert_newline_at_end_of_line(self):
        prefill = "1\n22\n3\n"
        text = "\n"
        expect = ['1\n', '22\n', '\n', '3\n']
        self.fillAndClear(prefill)
        self.buffer.insert(Position(2,3), text)
        assert self.buffer.lines == expect
        assert self.inserted("afterPosition") == Position(3,1)
        assert self.inserted("deltaX") == -2

    def test_insert_newline(self):
        prefill = "1\n22\n3\n"
        text = "\n"
        expect = ['1\n', '2\n', '2\n', '3\n']
        self.fillAndClear(prefill)
        self.buffer.insert(Position(2,2), text)
        assert self.buffer.lines == expect
        assert self.inserted("afterPosition") == Position(3,1)
        assert self.inserted("deltaX") == -1

    def test_insert_surrounding_newlines(self):
        prefill = "1\n22\n3\n"
        text = "\naa\n"
        expect = ['1\n', '2\n', 'aa\n', '2\n', '3\n']
        self.fillAndClear(prefill)
        self.buffer.insert(Position(2,2), text)
        assert self.buffer.lines == expect
        assert self.inserted("afterPosition") == Position(4,1)
        assert self.inserted("deltaX") == -1

    def test_insert_without_body(self):
        prefill = "1\n22\n3\n"
        text = "aa\nbb"
        expect = ['1\n', '2aa\n', 'bb2\n', '3\n']
        self.fillAndClear(prefill)
        self.buffer.insert(Position(2,2), text)
        assert self.buffer.lines == expect
        assert self.inserted("afterPosition") == Position(3,3)
        assert self.inserted("deltaX") == 1

    def test_insert_with_body(self):
        prefill = "1\n22\n3\n"
        text = "aa\nbb\ncc"
        expect = ['1\n', '2aa\n', 'bb\n', 'cc2\n', '3\n']
        self.fillAndClear(prefill)
        self.buffer.insert(Position(2,2), text)
        assert self.buffer.lines == expect
        assert self.inserted("afterPosition") == Position(4,3)
        assert self.inserted("deltaX") == 1


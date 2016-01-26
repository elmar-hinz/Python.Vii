from nose.tools import *
from vii.Range import *

class Range_Test:

    def test_line(self):
        range = Range(3)
        assert range == Range(3, 3)
        assert range.toLine() == 3
        assert range.toLines() == (3, 3)
        assert not range.isInverse()
        assert range.isLines()
        assert range.isOneLine()
        range.assertLines()
        range.assertOneLine()

    def test_lines(self):
        range = Range(1, 3)
        assert range == Range((1,3))
        assert range.toLines() == (1, 3)
        assert not range.isInverse()
        assert range.isLines()
        assert range.isTwoLines()
        range.assertLines()
        range.assertTwoLines()

    def test_position(self):
        range = Range(1, 3, isPosition = True)
        range2 = Range((1, 3), isPosition = True)
        range3 = Range((1, 3), (1, 3))
        assert range == range2
        assert range == range3
        assert range.toPosition() == (1, 3)
        assert range.toPositions() == ((1, 3), (1, 3))
        assert not range.isInverse()
        assert range.isPositions()
        assert range.isOnePosition()
        range.assertPositions()
        range.assertOnePosition()

    def test_postions(self):
        range = Range((1, 3), (2, 4))
        assert range.toPositions() == ((1, 3), (2, 4))
        assert not range.isInverse()
        assert range.isPositions()
        assert range.isTwoPositions()
        range.assertPositions()
        range.assertTwoPositions()

    def test_init_by_positions(self):
        pos1 = Position(1,1)
        pos2 = Range(2,2, isPosition = True)
        assert Range(pos1, pos2) == Range((1,1),(2,2))
        assert Range(pos2, pos1) == Range((2,2),(1,1))
        assert Range((1,1), pos2) == Range((1,1),(2,2))
        assert Range(pos1, (2,2)) == Range((1,1),(2,2))

    def test_isInverse(self):
        assert Range(3, 2).isInverse()
        assert Range((3, 1), (2, 1)).isInverse()
        assert Range((3, 3), (3, 2)).isInverse()

    def test_linewise(self):
        lines = Range((3, 1), (2, 1)).linewise()
        assert lines == Range(3, 2)

    def test_zero(self):
        assert Range(0) == Range((0,None), (0, None))
        assert Range(0).isLines()
        assert Position(0,0) == Range((0,0),(0,0))
        assert Position(0,0).isOnePosition()
        assert Position(0,0).toPosition() == (0,0)

    @raises(NotLinesRangeException)
    def test_NotLinesRangeException_1(self):
        range = Range((1, 3), (2, 4))
        range.assertLines()

    @raises(NotOneLineRangeException)
    def test_NotOneLineRangeException_1(self):
        range = Range(1, 3)
        range.assertOneLine()

    @raises(NotOneLineRangeException)
    def test_NotOneLineRangeException_2(self):
        range = Range((1, 3), (2, 4))
        range.assertOneLine()

    @raises(NotTwoLinesRangeException)
    def test_NotTwoLinesRangeException_1(self):
        range = Range(1)
        range.assertTwoLines()

    @raises(NotTwoLinesRangeException)
    def test_NotTwoLinesRangeException_2(self):
        range = Range((1, 3), (2, 4))
        range.assertTwoLines()

    @raises(NotPositionsRangeException)
    def test_NotPositionsRangeException_1(self):
        range = Range(1, 3)
        range.assertPositions()

    @raises(NotOnePositionRangeException)
    def test_NotOnePositionRangeException_1(self):
        range = Range(1, 3)
        range.assertOnePosition()

    @raises(NotOnePositionRangeException)
    def test_NotOnePositionRangeException_2(self):
        range = Range((1, 3), (2, 4))
        range.assertOnePosition()

    @raises(NotTwoPositionsRangeException)
    def test_NotTwoPositionsRangeException_1(self):
        range = Range(1, 3)
        range.assertTwoPositions()

    @raises(NotTwoPositionsRangeException)
    def test_NotTwoPositionsRangeException_2(self):
        range = Range((1, 3), (1, 3))
        range.assertTwoPositions()


from vii.Range import Range

class Range_Test:

    def test_lines(self):
        assert Range(1, 3) == Range((1,3))
        assert Range(1,3).isLines()
        assert Range(1,3).toLines() == (1, 3)

    def test_position(self):
        range1 = Range(1, 3, isPosition = True)
        range2 = Range((1, 3), isPosition = True)
        range3 = Range((1, 3), (1, 3))
        assert range1 == range2
        assert range1 == range3
        assert range1.isOnePositon()
        assert range1.toPosition() == (1, 3)

    def test_postions(self):
        range1 = Range((1, 3), (2, 4))
        assert not range1.isOnePositon()
        assert not range1.isLines()
        assert range1.toPositions() == ((1, 3), (2, 4))

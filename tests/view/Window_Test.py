from vii.view.Window import Window, WindowLines

class DummyBuffer:

    def lengthOfLine(self, nr):
        return 5

class DummyPort:

    def height(self):
        return 5

    def move(self, y, x):
        self.y = y
        self.x = x

    def draw(self, string):
        self.string = string

class DummyWindowLines:
    def mapPositionToWindowLines(self, y, x):
        if y == 1 and x == 1: return (1,1)
        if y == 3 and x == 5: return (5,1)
        if y == 4 and x == 5: return (6,1)

    def mapPositionFromWindowLines(self, y, x):
        print(y, x)
    #     if y == 4 and x == 5: return (6,1)

class Window_Test:

    def setup(self):
        self.port = DummyPort()
        self.lines = DummyWindowLines()
        self.buffer = DummyBuffer()
        self.fixture = Window()
        self.fixture.port = self.port
        self.fixture.buffer = self.buffer
        self.fixture.lines = self.lines

    def test__init__(self):
        assert self.fixture.port == self.port
        assert self.fixture.buffer == self.buffer
        assert self.fixture.lines == self.lines

    def test_lineIsAbovePort(self):
        self.fixture.firstLine = 5
        assert self.fixture.linesAbovePort(4) == 1
        assert self.fixture.linesAbovePort(5) == 0
        assert self.fixture.linesAbovePort(6) == -1

    def test_lineIsBelowPort(self):
        self.fixture.firstLine = 1
        # 3 maps to 5, 4 maps to 6 in the dummy
        # print(self.fixture.linesBelowPort(4))
        # assert not self.fixture.linesBelowPort(3)
        # assert self.fixture.linesBelowPort(4)

class WindowLines_Test:

    def setup(self):
        self.fixture = WindowLines()

    def test_splitLines(self):
        string = "1\n\n55555\n"
        width = 2
        expect = "1\n\n55\n55\n5\n"
        self.fixture.splitLines(string, width)
        assert str(self.fixture) == expect

    def test_mapPositionToWindowLines(self):
        string = "1\n\n55555\n"
        width = 2
        f = self.fixture
        f.splitLines(string, width)
        assert f.mapPositionToWindowLines(1,1) == (1,1)
        assert f.mapPositionToWindowLines(1,2) == (1,2)
        assert f.mapPositionToWindowLines(1,3) == (1,2)
        assert f.mapPositionToWindowLines(2,1) == (2,1)
        assert f.mapPositionToWindowLines(2,2) == (2,1)
        assert f.mapPositionToWindowLines(3,4) == (4,2)
        assert f.mapPositionToWindowLines(3,5) == (5,1)
        assert f.mapPositionToWindowLines(3,7) == (5,2)
        f.splitLines("", width)
        assert f.mapPositionToWindowLines(0,0) == (1,1)

    def test_mapPositionFromWindowLines(self):
        string = "1\n\n12345\n"
        width = 2
        f = self.fixture
        f.splitLines(string, width)
        assert f.mapPositionFromWindowLines(1,1) == (1,1)
        assert f.mapPositionFromWindowLines(1,2) == (1,2)
        assert f.mapPositionFromWindowLines(2,1) == (2,1)
        assert f.mapPositionFromWindowLines(2,1) == (2,1)
        assert f.mapPositionFromWindowLines(3, 1) == (3, 1)
        assert f.mapPositionFromWindowLines(3, 2) == (3, 2)
        assert f.mapPositionFromWindowLines(4, 2) == (3, 4)
        assert f.mapPositionFromWindowLines(10, 2) == None
        f.splitLines("", width)
        assert f.mapPositionFromWindowLines(1,1) == (0,0)


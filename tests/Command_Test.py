from vii.Command import Part, Command

class TestPart:

    def setup(self):
        self.fixture = Part()

    def test_setup(self):
        assert self.fixture.register == None
        assert self.fixture.numeral == ""
        assert self.fixture.count == None
        assert self.fixture.token == None

    def test_append_and_count(self):
        self.fixture.appendToNumeral("2")
        self.fixture.appendToNumeral("3")
        self.fixture.numeralToCount()
        assert self.fixture.count == 23

class TestCommand:

    def setup(self):
        self.fixture = Command()
        self.fixture.extend()

    def test_setup(self):
        assert len(self.fixture.parts) == 1
        assert self.fixture.position == 0

    def test_extend_and_last(self):
        self.fixture.extend()
        last = self.fixture.last()
        assert last == self.fixture.parts[-1]

    def test_next_rewind_getPart(self):
        self.fixture.extend()
        current = self.fixture.nextPart()
        assert current == self.fixture.getPart(0)
        current = self.fixture.nextPart()
        assert current == self.fixture.getPart(1)
        self.fixture.rewind()
        current = self.fixture.nextPart()
        assert current == self.fixture.getPart(0)

    def test_multiplyAll(self):
        self.fixture.last().count = 2
        self.fixture.extend()
        self.fixture.last().count = 3
        assert self.fixture.multiplyAll() == 6




from vii.Command import Part, Command

class TestPart:

    def setup(self):
        self.fixture = Part()

    def test_setup(self):
        assert self.fixture.numeral == ""
        assert self.fixture.operator == ""
        assert self.fixture.inserts == ""
        assert self.fixture.register == None
        assert self.fixture.count == None
        assert self.fixture.token == None
        assert self.fixture.ready == False

    def test_appendToNumeral_and_count(self):
        self.fixture.appendToNumeral("2")
        self.fixture.appendToNumeral("3")
        assert self.fixture.numeral == "23"
        self.fixture.numeralToCount()
        assert self.fixture.count == 23

    def test_appendToInserts(self):
        self.fixture.appendToInserts("a")
        self.fixture.appendToInserts("b")
        assert self.fixture.inserts == "ab"

class TestCommand:

    def setup(self):
        self.fixture = Command()
        self.fixture.extend()

    def test_setup(self):
        assert len(self.fixture.parts) == 1
        assert self.fixture.position == 0

    def test_extend_and_last(self):
        assert self.fixture.last() == self.fixture.part(0)
        self.fixture.extend()
        assert self.fixture.last() == self.fixture.part(1)

    def test_next_rewind_current(self):
        self.fixture.extend()
        assert self.fixture.current() == self.fixture.part(0)
        self.fixture.next()
        assert self.fixture.current() == self.fixture.part(1)
        self.fixture.rewind()
        assert self.fixture.current() == self.fixture.part(0)

    def test_multiplyAll(self):
        self.fixture.last().count = 2
        self.fixture.extend()
        self.fixture.last().count = 3
        assert self.fixture.multiplyAll() == 6

    def test_shortcuts_to_current_part(self):
        self.fixture.extend()
        self.fixture.next()
        assert not self.fixture.cpReady()
        self.fixture.part(1).ready = True
        assert self.fixture.cpReady()
        assert self.fixture.cpRegister() == None
        self.fixture.part(1).register = "R"
        assert self.fixture.cpRegister() == "R"
        assert self.fixture.cpOperator() == ""
        self.fixture.part(1).operator = "O"
        assert self.fixture.cpOperator() == "O"
        assert self.fixture.cpCount() == None
        self.fixture.part(1).count = 7
        assert self.fixture.cpCount() == 7
        assert self.fixture.cpInserts() == ""
        self.fixture.part(1).inserts = "ab"
        assert self.fixture.cpInserts() == "ab"
        assert self.fixture.cpToken() == None
        self.fixture.part(1).token = "T"
        assert self.fixture.cpToken() == "T"


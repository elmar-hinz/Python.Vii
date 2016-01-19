from vii.Command import Part, Command

class TestPart:

    def setup(self):
        self.fixture = Part()

    def test_setup(self):
        assert self.fixture.numeral == ""
        assert self.fixture.operator == ""
        assert self.fixture.inserts == []
        assert self.fixture.register == None
        assert self.fixture.count == None
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
        assert self.fixture.inserts == ["a", "b"]

    def test_insert(self):
        self.fixture.appendToInserts("a")
        self.fixture.appendToInserts("b")
        assert self.fixture.insert() == "b"

class TestCommand:

    def setup(self):
        self.fixture = Command()
        self.fixture.extend()

    def test_setup(self):
        assert len(self.fixture.parts) == 1

    def test_part_extend_previous_and_last(self):
        assert self.fixture.last() == self.fixture.part(0)
        self.fixture.extend()
        assert self.fixture.previous() == self.fixture.part(0)
        assert self.fixture.last() == self.fixture.part(1)

    def test_multiplyAll(self):
        self.fixture.last().count = 2
        self.fixture.extend()
        self.fixture.last().count = 3
        assert self.fixture.multiplyAll() == 6

    def test_shortcuts_to_lastPart(self):
        self.fixture.extend()
        assert not self.fixture.lpReady()
        self.fixture.part(1).ready = True
        assert self.fixture.lpReady()
        assert self.fixture.lpRegister() == None
        self.fixture.part(1).register = "R"
        assert self.fixture.lpRegister() == "R"
        assert self.fixture.lpOperator() == ""
        self.fixture.part(1).operator = "O"
        assert self.fixture.lpOperator() == "O"
        assert self.fixture.lpCount() == None
        self.fixture.part(1).count = 7
        assert self.fixture.lpCount() == 7
        assert self.fixture.lpInserts() == []
        self.fixture.part(1).inserts = ['a', 'b']
        assert self.fixture.lpInserts() == ['a', 'b']


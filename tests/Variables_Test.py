from vii.Variables import Variables

class Variables_Test:

    def setup(self):
        self.fixture = Variables()

    def test__init__(self):
        self.fixture.__class__ == Variables
        assert self.fixture.storage == dict()

    def test_set_get(self):
        self.fixture.set("seven", 7)
        assert self.fixture.get("seven") == 7

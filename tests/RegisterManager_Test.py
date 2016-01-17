from vii.RegisterManager import RegisterManager

class RegisterManager_Test:

    def setup(self):
        self.fixture = RegisterManager()

    def test_init(self):
        assert self.fixture.yankRegister == []

    def test_unshift_read(self):
        self.fixture.unshift("one")
        self.fixture.unshift("zero", True)
        assert self.fixture.read() == ("zero", True)
        assert self.fixture.read(1) == ("one", False)

    def test_limit_of_register(self):
        for i in range(11, -1, -1):
            self.fixture.unshift(str(i))
        assert self.fixture.read(0) == ("0", False)
        assert self.fixture.read(9) == ("9", False)
        assert self.fixture.read(10) == ("", False)



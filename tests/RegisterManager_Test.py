from vii.RegisterManager import RegisterManager

class RegisterManager_Test:

    def setup(self):
        self.fixture = RegisterManager()

    def test_init(self):
        assert (self.fixture.numbered ==
                10 * [tuple(["", False])])
        assert self.fixture.named == dict()
        assert self.fixture.unnamed == "0"

    def test_fetch_unknown_returns_empty_string(self):
        assert self.fixture.fetch("u") == ("", False)
        assert self.fixture.fetch("9") == ("", False)
        assert self.fixture.fetch("11") == ("", False)

    def test_store_fetch_replace(self):
        self.fixture.store("a", "alpha")
        assert self.fixture.fetch("a") == ("alpha", False)
        self.fixture.store("a", "ALPHA", True)
        assert self.fixture.fetch("a") == ("ALPHA", True)
        self.fixture.store("0", "zero")
        assert self.fixture.fetch("0") == ("zero", False)
        self.fixture.store("0", "ZERO", True)
        assert self.fixture.fetch("0") == ("ZERO", True)

    def test_limit_of_numbered(self):
        for i in range(11, 0, -1):
            self.fixture.shift(str(i))
        assert self.fixture.fetch(0) == ("", False)
        assert self.fixture.fetch(1) == ("1", False)
        assert self.fixture.fetch(9) == ("9", False)
        assert self.fixture.fetch(10) == ("", False)

    def test_storing_to_unnamed_register_stores_to_0(self):
        assert self.fixture.fetch('"') == ("", False)
        assert self.fixture.fetch(0) == ("", False)
        self.fixture.store('"', "uuu", True)
        assert self.fixture.fetch('"') == ("uuu", True)
        assert self.fixture.fetch(0) == ("uuu", True)

    def test_access_last_store_by_unnamed(self):
        assert self.fixture.fetch('"') == ("", False)
        assert self.fixture.fetch('a') == ("", False)
        self.fixture.store('a', "aaa", True)
        assert self.fixture.fetch('"') == ("aaa", True)
        assert self.fixture.fetch(0) == ("", False)

    def test_access_last_shift_by_unnamed(self):
        assert self.fixture.fetch('"') == ("", False)
        assert self.fixture.fetch(1) == ("", False)
        self.fixture.shift("aaa", True)
        assert self.fixture.fetch('"') == ("aaa", True)
        assert self.fixture.fetch(1) == ("aaa", True)


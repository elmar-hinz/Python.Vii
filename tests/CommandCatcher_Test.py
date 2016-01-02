from vii.CommandCatcher import CommandCatcher

class CommandCatcher_Test:

    commandMap = """
    a: alpha
    b: beta
    """

    def setup(self):
        self.catcher = CommandCatcher(self.commandMap)

    def test__init__(self):
        assert self.catcher.parts == None
        assert len(self.catcher.map) == 2

    def test_parseMap(self):
        map = self.catcher.parseMap(self.commandMap)
        assert map == {'a': 'alpha', 'b': 'beta'}

    def test_reset(self):
        self.catcher.parts = dict()
        self.catcher.reset()
        assert self.catcher.parts == None

    def test_ready_without_count(self):
        status = self.catcher.ready(ord('a'))
        assert status == True
        assert self.catcher.count() == 0
        assert self.catcher.action() ==  "alpha"
        assert self.catcher.operator() ==  "a"

    def test_ready_with_count(self):
        status = self.catcher.ready(ord('1'))
        status = self.catcher.ready(ord('2'))
        assert status == False
        status = self.catcher.ready(ord('b'))
        assert status == True
        assert self.catcher.count() == 12
        assert self.catcher.action() ==  "beta"
        assert self.catcher.operator() ==  "b"

    def test_ready_with_invalid_command(self):
        status = self.catcher.ready(ord('z'))
        assert self.catcher.action() == None
        assert self.catcher.operator() == 'z'


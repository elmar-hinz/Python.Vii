# from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.model.buffer import Buffer
from vii.model.line import Line

class TestBuffer:

    def setup(self):
        self.fixture = Buffer()

    def teardown(self):
        pass

    def testInit(self):
        assert self.fixture.__class__ == Buffer
        assert self.fixture.memberClass == Line
        assert self.fixture.length() == 1
        assert str(self.fixture) == ""
        assert 'cursor' in dir(self.fixture)

    def testInitWithText(self):
        content = "aa aa\nbb bb"
        buffer = Buffer(content)
        assert buffer.length() == 2
        assert str(buffer) == content

    def textCreateMember(self):
        assert(
            self.fixture.createMember().__class__ == Line)



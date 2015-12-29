# from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.model.line import Line

class TestLine:

    def setup(self):
        self.fixture = Line()

    def teardown(self):
        pass

    def testInit(self):
        assert self.fixture.__class__ == Line
        assert self.fixture.memberClass == str
        assert self.fixture.length() == 0

    def testInitWithText(self):
        assert str(Line("text")) == "text"
        assert Line("text").length() == 4

    def testToString(self):
        self.fixture.append('a')
        self.fixture.append('b')
        assert str(self.fixture) == "ab"

    def testCreateMember(self):
        assert self.fixture.createMember() == ' '

    def testCreateMemberWithText(self):
        assert self.fixture.createMember('a') == 'a'


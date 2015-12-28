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

    def testToString(self):
        self.fixture.append('a')
        self.fixture.append('b')
        assert str(self.fixture) == "ab"


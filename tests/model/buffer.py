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

    def testCreateElement(self):
        assert(
            self.fixture.createElement().__class__ == Line)


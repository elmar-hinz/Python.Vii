# from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.model.abstractlist import AbstractList

class TestList:

    def setup(self):
        self.fixture = AbstractList()

    def teardown(self):
        pass

    def assertContains(self, *numbers):
        assert(self.fixture.asList() == list(numbers))

    def testInit(self):
        assert self.fixture.__class__ == AbstractList

    def testLength(self):
        assert self.fixture.length() == 0
        self.fixture.append(1)
        self.fixture.append(1)
        assert self.fixture.length() == 2

    def testStr(self):
        self.fixture.append(1)
        self.fixture.append(2)
        assert str(self.fixture) == "1\n2"

    def testAppend(self):
        self.fixture.append(1)
        self.assertContains(1)
        self.fixture.append(2)
        self.assertContains(1,2)

    def testAppendMultiple(self):
        self.fixture.append(1)
        self.assertContains(1)
        self.fixture.append([2, 3])
        self.assertContains(1,2,3)

    def testDelete(self):
        self.fixture.append(1)
        self.fixture.append(2)
        self.fixture.append(3)
        self.fixture.delete(1)
        self.assertContains(1,3)

    def testDeleteMultiple(self):
        self.fixture.append(1)
        self.fixture.append(2)
        self.fixture.append(3)
        self.fixture.append(4)
        self.fixture.delete(1,2)
        self.assertContains(1,4)

    def testInsert(self):
        self.fixture.append(1)
        self.fixture.append(3)
        self.fixture.insert(1,2)
        self.assertContains(1,2,3)

    def testInsertMultiple(self):
        self.fixture.append(1)
        self.fixture.append(4)
        self.fixture.insert(1,[2,3])
        self.assertContains(1,2,3,4)

    def testRead(self):
        self.fixture.append(1)
        self.fixture.append(2)
        self.fixture.append(3)
        assert self.fixture.read(1) == 2

    def testReadMultiple(self):
        self.fixture.append(1)
        self.fixture.append(2)
        self.fixture.append(3)
        assert self.fixture.read(1, 2) == [2,3]

    def testReplace(self):
        self.fixture.append(1)
        self.fixture.append(4)
        self.fixture.append(3)
        self.fixture.replace(1,2)
        self.assertContains(1,2,3)

    def testReplaceMultiple(self):
        self.fixture.append(1)
        self.fixture.append(1)
        self.fixture.append(1)
        self.fixture.append(4)
        self.fixture.replace(1,[2,3])
        self.assertContains(1,2,3,4)





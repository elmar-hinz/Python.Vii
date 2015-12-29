# from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.controller.move import *


def testUp():
    assert up((1,1), 1) == (0,1)
    assert up((4,2), 2) == (2,2)

def testDown():
    assert down((0,1), 1) == (1,1)
    assert down((2,2), 2) == (4,2)

def testLeft():
    assert left((1,1), 1) == (1,0)
    assert left((2,4), 2) == (2,2)

def testRight():
    assert right((1,0), 1) == (1,1)
    assert right((2,2), 2) == (2,4)


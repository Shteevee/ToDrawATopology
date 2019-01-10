import unittest
import sys
sys.path.append("..")
from SketchCanvas import *
from SketchFeatures import *
from SketchShading import *

class SketchCanvasTest(unittest.TestCase):

    def test_a(self):
        self.assertEqual(True, True)

class SketchFeaturesTest(unittest.TestCase):

    def test_findMajorAnchors_tooFewPointsReturnsUnchanged(self):
        points = [[[1,1],
                   [1,1]]]
        points = findMajorAnchors(points)
        self.assertEqual(points, [[[1,1],
                                  [1,1]]])

    def test_findMajorAnchors_PointsReturnsReducedDiag(self):
        points = [[[5,5],
                   [10,10],
                   [15,15],
                   [20,20],
                   [25,25]]]
        points = findMajorAnchors(points)
        self.assertEqual(points, [[[5,5],
                                   [25,25]]])

    def test_findMajorAnchors_PointsReturnsReducedHoriz(self):
        points = [[[1,5],
                   [1,10],
                   [1,15],
                   [1,20],
                   [1,25]]]
        points = findMajorAnchors(points)
        self.assertEqual(points, [[[1,5],
                                   [1,25]]])

    def test_findMajorAnchors_PointsReturnsReducedVert(self):
        points = [[[5,1],
                   [10,1],
                   [15,1],
                   [20,1],
                   [25,1]]]
        points = findMajorAnchors(points)
        self.assertEqual(points, [[[5,1],
                                   [25,1]]])

    def test_findMajorAnchors_NoPointsReturnsUnchanged(self):
        points = [[]]
        points = findMajorAnchors(points)
        self.assertEqual(points, [[]])

class SketchShadingTest(unittest.TestCase):

    def test_a(self):
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()

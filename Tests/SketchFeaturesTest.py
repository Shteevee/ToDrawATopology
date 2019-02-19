import unittest
import sys
sys.path.append("..")
from SketchFeatures import *

class findMajorAnchorsTest(unittest.TestCase):

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

class getNeighboursTest(unittest.TestCase):

    def test_getNeighbours_EightPointsReturned(self):
        current_pixel = [13,7]
        centre_point = [20,20]

        neighbours = getNeighbours(current_pixel, centre_point)

        self.assertEqual(len(neighbours), 8)

    def test_getNeighbours_PointsReturnedCorrectOrder(self):
        current_pixel = [1,1]
        centre_point = [3,3]

        neighbours = getNeighbours(current_pixel, centre_point)

        target = np.array([[2,2],
                           [2,1],
                           [1,2],
                           [2,0],
                           [0,2],
                           [1,0],
                           [0,1],
                           [0,0]])
        self.assertTrue(np.array_equal(neighbours, target))

class getUnwalkedCoordsTest(unittest.TestCase):

    def test_getUnwalkedCoords_NoValuesReturned(self):
        image = np.zeros((3,3))

        coords = getUnwalkedCoords(image)

        target = np.empty((0,2))
        self.assertTrue(np.array_equal(coords, target))

    def test_getUnwalkedCoords_CorrectValuesReturned(self):
        image = np.zeros((3,3))
        image[[0,1],[1,1]] = 1

        coords = getUnwalkedCoords(image)

        target = np.array([[0,1],
                           [1,1]])
        self.assertTrue(np.array_equal(coords, target))

class checkColinearTest(unittest.TestCase):

    def test_checkColinear_ReturnsZeroForColinear(self):
        result = checkColinear([1,1], [2,2], [3,3])

        self.assertTrue(result)

    def test_checkColinear_ReturnsNonZeroForNotColinear(self):
        result = checkColinear([1,2], [2,2], [3,3])

        self.assertFalse(result)

class nextNeighbourTest(unittest.TestCase):

    def test_nextNeighbour_ReturnsNonValueWhenNoNeighbours(self):
        current_pixel = [0,0]
        thinned_image = np.zeros((3,3))
        centre_point = [2,2]

        coord = nextNeighbour(current_pixel, thinned_image, centre_point)

        target = np.array([-1,-1])
        self.assertTrue(np.array_equal(coord, target))

    def test_nextNeighbour_ReturnsNonValueWhenNoPixelsInRange(self):
        current_pixel = [0,0]
        thinned_image = np.zeros((3,3))
        thinned_image[[2,2]] = 1
        centre_point = [2,2]

        coord = nextNeighbour(current_pixel, thinned_image, centre_point)

        target = np.array([-1,-1])
        self.assertTrue(np.array_equal(coord, target))

    def test_nextNeighbour_ReturnsCoordWhenPixelInRange(self):
        current_pixel = [1,1]
        thinned_image = np.zeros((3,3))
        thinned_image[[2,2]] = 1
        centre_point = [2,2]

        coord = nextNeighbour(current_pixel, thinned_image, centre_point)

        target = np.array([2,2])
        self.assertTrue(np.array_equal(coord, target))

    def test_nextNeighbour_ReturnsCorrectCoordWhenPixelInRange(self):
        current_pixel = [1,2]
        thinned_image = np.zeros((3,3))
        thinned_image[1,1] = 1
        thinned_image[2,2] = 1
        centre_point = [1,1]

        coord = nextNeighbour(current_pixel, thinned_image, centre_point)

        target = np.array([1,1])
        self.assertTrue(np.array_equal(coord, target))

class walkNeighbourhoodTest(unittest.TestCase):

    def test_walkNeighbourhood_ReturnsNothingForEmptyImage(self):
        image = np.zeros((3,3))

        coords = walkNeighbourhood(image)

        target = []
        self.assertEqual(coords, target)

    def test_walkNeighbourhood_ReturnsPointsForSquareImage(self):
        image = np.zeros((5,5))
        image[1,1] = 255
        image[1,2] = 255
        image[1,3] = 255
        image[2,1] = 255
        image[2,3] = 255
        image[3,1] = 255
        image[3,2] = 255
        image[3,3] = 255

        coords = walkNeighbourhood(image)

        target = [[np.array([1,2]),
                  np.array([2,3]),
                  np.array([3,2]),
                  np.array([2,1])]]
        results = list(map(lambda x, y: np.array_equal(x,y), coords[0], target[0]))
        self.assertTrue(np.array_equal(coords, target))

if __name__=="__main__":
    unittest.main()

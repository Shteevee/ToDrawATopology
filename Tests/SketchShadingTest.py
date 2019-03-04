import unittest
import sys
sys.path.append("..")
from drawing_a_topology.drawing.sketch_shading import *
from drawing_a_topology.tests.MockPath import MockPath

class clean_paths_test(unittest.TestCase):

    def test_cleanPaths_emptyListReturnsEmpty(self):
         list = []

         result = clean_paths(list)

         self.assertEqual(result,[])

    def test_cleanPaths_spreadListReturnsUnchanged(self):
        list = [MockPath(np.array([[1,1], [2,2]]))]

        result = clean_paths(list)

        self.assertTrue(np.array_equal(result[0].vertices, np.array([[1,1], [2,2]])))

    def test_cleanPaths_closeVerticeReturnsEmptyList(self):
        list = [MockPath(np.array([[1,1],[1,1]]))]

        result = clean_paths(list)
        self.assertEqual(result, [])

    def test_cleanPaths_spreadListReturnsReduced(self):
        list = [MockPath(np.array([[1,1], [2,2]])), MockPath(np.array([[1,1], [1,1]]))]

        result = clean_paths(list)

        self.assertTrue(np.array_equal(result[0].vertices, np.array([[1,1], [2,2]])))

class stitch_paths_test(unittest.TestCase):

    def test_stitchPaths_EmptyListReturnEmpty(self):
        list = []

        result = stitch_paths(list)

        self.assertEqual(result,[])

def run_full_suite(classes):
    for test_class in classes:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
        unittest.TextTestRunner().run(suite)

if __name__=="__main__":
    run_full_suite([clean_paths_test, stitch_paths_test])

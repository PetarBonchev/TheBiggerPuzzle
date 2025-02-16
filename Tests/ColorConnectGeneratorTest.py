import unittest
from Utilities.ColorConnectGenerator import ColorTableGenerator

class TestFlask(unittest.TestCase):

    def setUp(self):
        self.table = ColorTableGenerator(10, 20, 6)

    def test_split_trail(self):
        trails = [[(0, 0), (0, 1)], [(1, 1), (1, 2), (2, 2), (2, 3)]]
        ColorTableGenerator._split_longest_trail(trails)
        self.assertEqual(len(trails), 3)
        self.assertEqual(trails[0], [(0, 0), (0, 1)])
        self.assertEqual(trails[1], [(1, 1), (1, 2)])
        self.assertEqual(trails[2], [(2, 2), (2, 3)])

    def test_merge_trails_1(self):
        trails = [[(0, 0), (0, 1)], [(1, 1), (1, 2), (2, 2), (2, 3)]]
        ColorTableGenerator._merge_multi_length_trail(trails, trails[0])
        self.assertEqual(len(trails), 1)
        self.assertEqual(trails[0][0], (0,0))

    def test_merge_trails_2(self):
        trails = [[(0, 1), ], [(1, 1), (1, 2), (2, 2), (2, 3)]]
        ColorTableGenerator._merge_one_length_trail(trails, 0)
        self.assertEqual(len(trails), 1)
        self.assertEqual(trails[0][0], (0, 1))

    def test_generate(self):
        trails = self.table.generate()
        self.assertEqual(len(trails), 6)
        for i in range(10):
            for j in range(20):
                self.assertFalse((i, j) in self.table._not_visited)

if __name__ == '__main__':
    unittest.main()
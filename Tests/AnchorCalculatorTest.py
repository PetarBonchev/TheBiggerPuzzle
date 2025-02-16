import unittest
import Utilities.AnchorCalculator
from Utilities.AnchorCalculator import Anchor

class TestAnchor(unittest.TestCase):

    def setUp(self):
        Utilities.AnchorCalculator.screen_width = 100
        Utilities.AnchorCalculator.screen_height = 50

    def test_proportions(self):
        width, height = Anchor.get_proportions(1/2, 1/2)
        self.assertEqual(width, 50)
        self.assertEqual(height, 25)

    def test_top_left(self):
        x, y = Anchor.top_left(10, 10)
        self.assertEqual(x, 10)
        self.assertEqual(y, 10)

    def test_center(self):
        x, y = Anchor.center(0, 0, 20, 10)
        self.assertEqual(x, (100 - 20) / 2)
        self.assertEqual(y, (50 - 10) / 2)

    def test_center_2(self):
        x, y = Anchor.center(10, 10, 20, 10)
        self.assertEqual(x, (100 - 20) / 2 + 10)
        self.assertEqual(y, (50 - 10) / 2 + 10)

    def test_bottom_right(self):
        x, y = Anchor.bottom_right(0, 0, 20, 10)
        self.assertEqual(x, 100 - 20)
        self.assertEqual(y, 50 - 10)


if __name__ == '__main__':
    unittest.main()
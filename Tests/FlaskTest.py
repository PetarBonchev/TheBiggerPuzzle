import unittest
from  UI_Elements.FlaskUI import Flask

class TestFlask(unittest.TestCase):

    def setUp(self):
        self.flask = Flask(5, 0, 0)

    def test_receive(self):
        self.flask.receive_top([1,1,1])
        self.assertEqual(self.flask.water_height, 3)

    def test_top_color(self):
        self.flask.receive_top([1,1])
        self.flask.receive_top([2,2])
        self.assertEqual(self.flask.top_color, 2)

    def test_complete(self):
        self.assertTrue(self.flask.complete)
        self.flask.receive_top([5,5,5,5,5])
        self.assertTrue(self.flask.complete)
        self.flask.content[1] = 1
        self.assertFalse(self.flask.complete)

    def test_top_count(self):
        self.assertEqual(self.flask._top_count, 0)
        self.flask.receive_top([1,1])
        self.assertEqual(self.flask._top_count, 2)
        self.flask.receive_top([2,2,2])
        self.assertEqual(self.flask._top_count, 3)

    def test_move_top(self):
        top_liquid = self.flask.move_top()
        self.assertFalse(top_liquid)
        self.flask.receive_top([1,1,2,2,2])
        top_liquid = self.flask.move_top()
        self.assertEqual(self.flask.water_height, 2)
        self.assertEqual(top_liquid, [2,2,2])

if __name__ == '__main__':
    unittest.main()
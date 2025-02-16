import unittest
from UI_Elements.Button import Button


class TestButton(unittest.TestCase):
    def setUp(self):
        self.button = Button(100, 100, 100, 100)
        self.x = 0

    def test_on_click_execution(self):
        def f():
            self.x = 5
        self.button.add_on_click(f)
        self.button._execute_on_click()
        self.assertEqual(self.x, 5)

    def test_on_click_sequence(self):
        def f():
            self.x = 5
        def g():
            self.x = 6
        self.button.add_on_click(f)
        self.button.add_on_click(g)
        self.button._execute_on_click()
        self.assertEqual(self.x, 6)

    def test_clear_on_click(self):
        def f():
            self.x = 5
        def g():
            self.x = 6
        self.button.add_on_click(f)
        self.button.add_on_click(g)
        self.button.clear_on_click()
        self.button._execute_on_click()
        self.assertEqual(self.x, 0)

    def test_on_click_with_args(self):
        def f(y):
            self.x = y
        self.button.add_on_click(f, 5)
        self.button._execute_on_click()
        self.assertEqual(self.x, 5)

    def test_on_click_with_kwargs(self):
        def f(y, z):
            self.x = y + z
        self.button.add_on_click(f, z=3, y=2)
        self.button._execute_on_click()
        self.assertEqual(self.x, 5)

if __name__ == '__main__':
    unittest.main()

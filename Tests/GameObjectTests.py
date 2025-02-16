import unittest
from UI_Elements.GameObject import GameObject


class TestGameObject(unittest.TestCase):
    def setUp(self):
        self.object1 = GameObject('obj1')
        self.object2 = GameObject('obj2')
        self.object3 = GameObject('obj3')
        self.object4 = GameObject('obj4')

    def test_creation(self):
        self.assertEqual(self.object2.name, 'obj2')

    def test_inheritance_1(self):
        self.object1.add_child(self.object2)
        self.assertTrue(self.object1.get_object_by_name('obj2'))

    def test_inheritance_2(self):
        self.object1.add_child(self.object2)
        self.object3.add_child(self.object4)
        self.object1.add_child(self.object3)
        self.assertTrue(self.object1.get_object_by_name('obj4'))

    def test_activeness_independence(self):
        self.object1.add_child(self.object2)
        self.object3.add_child(self.object4)
        self.object1.add_child(self.object3)
        self.object1.set_active(False)
        self.assertTrue(self.object1.get_object_by_name('obj4')._is_active)

if __name__ == '__main__':
    unittest.main()

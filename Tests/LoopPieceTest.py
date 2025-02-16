import unittest
from UI_Elements.LoopPieceUI import LoopPiece


class TestLoopPiece(unittest.TestCase):

    def setUp(self):
        self.loop_piece = LoopPiece([0,0,0,0],0,0)

    def test_rotate_1(self):
        self.loop_piece.rotate(1)
        self.assertEqual(self.loop_piece.up, 0)

    def test_rotate_2(self):
        self.loop_piece._connections = [1,0,0,0]
        self.loop_piece.rotate(1)
        self.assertEqual(self.loop_piece.up, 0)
        self.assertEqual(self.loop_piece.right, 1)

    def test_rotate_3(self):
        self.loop_piece._connections = [1, 0, 0, 0]
        self.loop_piece.rotate(2)
        self.assertEqual(self.loop_piece.up, 0)
        self.assertEqual(self.loop_piece.down, 1)

    def test_rotate_4(self):
        self.loop_piece._connections = [0, 1, 1, 1]
        self.loop_piece.rotate(1975)
        self.assertEqual(self.loop_piece.up, 1)
        self.assertEqual(self.loop_piece.left, 0)

if __name__ == '__main__':
    unittest.main()
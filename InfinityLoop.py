import random
import numpy as np
import Utils
from UIManager import LoopPiece


class Board:

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self._board = np.array([[0 for _ in range(width)] for _ in range(height)])
        self._piece_board = np.array([[None for _ in range(width)] for _ in range(height)])
        self._piece_length = 2 * LoopPiece.SIDE_HEIGHT - LoopPiece.SIDE_WIDTH
        self._top_left_x = (Utils.screen_width - width * self._piece_length) // 2 - LoopPiece.SIDE_WIDTH + LoopPiece.SIDE_HEIGHT
        self._top_left_y = (Utils.screen_height - height * self._piece_length) // 2 - LoopPiece.SIDE_WIDTH + LoopPiece.SIDE_HEIGHT

        self.generate()

    def draw(self, screen):
        for i in range(len(self._piece_board)):
            for j in range(len(self._piece_board[i])):
                if self._piece_board[i, j]:
                    self._piece_board[i, j].draw(screen)

    def check_click(self, mouse_x, mouse_y):
        for i in range(len(self._piece_board)):
            for j in range(len(self._piece_board[i])):
                if self._piece_board[i, j]:
                    self._piece_board[i, j].check_click(mouse_x, mouse_y)
        if self._is_solved():
            self.generate()

    def update(self):
        pass

    def generate(self):
        self._board = np.array([[0 for _ in range(self.width)] for _ in range(self.height)])
        self._piece_board = np.array([[None for _ in range(self.width)] for _ in range(self.height)])
        for i in range(self.height):
            for j in range(self.width):
                if random.random() > 0.5:
                    self._board[i, j] = 1

        for i in range(5):
            self._game_of_life()

        for x in range(self.height):
            for y in range(self.width):
                if self._board[x, y] == 1:
                    connections = [
                        (1 if self._board[x - 1, y] else 0) if x > 0 else 0,
                        (1 if self._board[x, y + 1] else 0) if y < self.width - 1 else 0,
                        (1 if self._board[x + 1, y] else 0) if x < self.height - 1 else 0,
                        (1 if self._board[x, y - 1] else 0) if y > 0 else 0
                    ]
                    piece = LoopPiece(connections, self._top_left_x + y * self._piece_length, self._top_left_y + x * self._piece_length)
                    piece.rotate(random.randint(0, 3))
                    self._board[x, y] = piece.state
                    self._piece_board[x, y] = piece

    def _is_solved(self):
        for i in range(len(self._piece_board)):
            for j in range(len(self._piece_board[i])):
                piece = self._piece_board[i, j]
                if piece:
                    if piece.up != (self._piece_board[i - 1, j].down if i > 0 and self._piece_board[i - 1, j] else 0):
                        return False
                    if piece.right != (
                    self._piece_board[i, j + 1].left if j < self.width - 1 and self._piece_board[i, j + 1] else 0):
                        return False
                    if piece.down != (
                    self._piece_board[i + 1, j].up if i < self.height - 1 and self._piece_board[i + 1, j] else 0):
                        return False
                    if piece.left != (
                    self._piece_board[i, j - 1].right if j > 0 and self._piece_board[i, j - 1] else 0):
                        return False
        return True

    def _game_of_life(self):
        new_board = np.copy(self._board)
        for x in range(self.height):
            for y in range(self.width):
                live_neighbours = sum([
                    self._board[x - 1, y - 1] if x > 0 and y > 0 else 0,
                    self._board[x - 1, y] if x > 0 else 0,
                    self._board[x - 1, y + 1] if x > 0 and y < self.width - 1 else 0,
                    self._board[x, y - 1] if y > 0 else 0,
                    self._board[x, y + 1] if y < self.width - 1 else 0,
                    self._board[x + 1, y - 1] if x < self.height - 1 and y > 0 else 0,
                    self._board[x + 1, y] if x < self.height - 1 else 0,
                    self._board[x + 1, y + 1] if x < self.height - 1 and y < self.width - 1 else 0
                ])

                if self._board[x, y] == 1:
                    if live_neighbours < 2 or live_neighbours > 6:
                        new_board[x, y] = 0
                else:
                    if live_neighbours < 3:
                        new_board[x, y] = 1

        self._board = new_board

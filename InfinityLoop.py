import random
import numpy as np
import Utils
from UIManager import LoopPiece


class Board:

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self._board = np.array([[0 for _ in range(width)] for _ in range(height)])
        self._piece_length = 2 * LoopPiece.SIDE_HEIGHT - LoopPiece.SIDE_WIDTH
        self._top_left_x = (Utils.screen_width - width * self._piece_length) // 2 - LoopPiece.SIDE_WIDTH + LoopPiece.SIDE_HEIGHT
        self._top_left_y = (Utils.screen_height - height * self._piece_length) // 2 - LoopPiece.SIDE_WIDTH + LoopPiece.SIDE_HEIGHT
        self._pieces = []

        self.generate()

    def draw(self, screen):
        for piece in self._pieces:
            piece.draw(screen)

    def check_click(self, mouse_x, mouse_y):
        for piece in self._pieces:
            piece.check_click(mouse_x, mouse_y)

    def update(self):
        pass

    def generate(self):
        self._board = np.array([[0 for _ in range(self.width)] for _ in range(self.height)])
        self._pieces.clear()
        placed = 0
        while placed < (4 * self.height * self.width) // 7:
            x, y = random.randint(0, self.height - 1), random.randint(0, self.width - 1)
            while random.random() < 0.8:
                self._board[x, y] = 1
                placed += 1
                for i in range(20):
                    direction = random.choice([(0, -1), (1, 0), (0, 1), (-1, 0)])
                    x, y = x + direction[1], y + direction[0]
                    if 0 <= x < self.height and 0 <= y < self.width and self._board[x][y] == 0:
                        break
                    x, y = x - direction[1], y - direction[0]

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
                    self._pieces.append(piece)
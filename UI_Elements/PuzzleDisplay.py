import random
import pygame
from UI_Elements.PuzzlePartUI import PuzzlePart


class PuzzleDisplay:

    def __init__(self, width, height, piece_size):
        self._width = width
        self._height = height
        self._piece_size = piece_size
        self._pieces = []
        self.choose_pieces()

    def choose_pieces(self):
        self._pieces = []
        rows = self._height // self._piece_size
        cols = self._width // self._piece_size
        board = [[None for _ in range(cols)] for _ in range(rows)]
        choice_options = [-1, 1]
        width_diff = self._width - self._piece_size * cols
        height_diff = self._height - self._piece_size * rows

        for i in range(rows):
            for j in range(cols):
                top = right = down = left = random.choice(choice_options)
                if i != 0:
                    top = -board[i - 1][j][2]
                if j != 0:
                    left = -board[i][j - 1][1]
                if i != rows - 1:
                    down = random.choice(choice_options)
                if j != cols - 1:
                    right = random.choice(choice_options)

                board[i][j] = (top, right, down, left)

        for i in range(rows):
            for j in range(cols):
                if random.randint(0, 3) == 1:
                    self._pieces.append((PuzzlePart.get_shape_points((j * self._piece_size + width_diff / 2, i * self._piece_size + height_diff / 2), self._piece_size, self._piece_size / 3, board[i][j]), pygame.Color('grey')))

    def draw(self, screen):
        for points, color in self._pieces:
            pygame.draw.polygon(screen, (183, 174, 209), points, 5)
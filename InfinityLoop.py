import random
import numpy as np
import Utils
from UIManager import LoopPiece


class InfinityLoop:

    SIDE_WIDTH = Utils.LOOP_PIECE_PART_WIDTH
    SIDE_HEIGHT = Utils.LOOP_PIECE_PART_HEIGHT

    def __init__(self, width, height):
        self._height = height
        self._width = width
        self._board = np.array([[0 for _ in range(width)] for _ in range(height)])
        self._piece_board = np.array([[None for _ in range(width)] for _ in range(height)])
        self._piece_length = 2 * InfinityLoop.SIDE_HEIGHT - InfinityLoop.SIDE_WIDTH
        self._top_left_x = (Utils.screen_width - width * self._piece_length) // 2 - InfinityLoop.SIDE_WIDTH + InfinityLoop.SIDE_HEIGHT
        self._top_left_y = (Utils.screen_height - height * self._piece_length) // 2 - InfinityLoop.SIDE_WIDTH + InfinityLoop.SIDE_HEIGHT

        self.new_game()

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
            self.new_game()

    def update(self):
        pass

    def new_game(self):
        self._board = np.array([[0 for _ in range(self._width)] for _ in range(self._height)])
        self._piece_board = np.array([[None for _ in range(self._width)] for _ in range(self._height)])
        for i in range(self._height):
            for j in range(self._width):
                if random.random() > Utils.GAME_OF_LIFE_INITIAL_SPAWN_CHANCE:
                    self._board[i, j] = 1

        for i in range(Utils.GAME_OF_LIFE_ITERATIONS):
            self._game_of_life()

        for x in range(self._height):
            for y in range(self._width):
                if self._board[x, y] == 1:
                    connections = [
                        (1 if self._board[x - 1, y] else 0) if x > 0 else 0,
                        (1 if self._board[x, y + 1] else 0) if y < self._width - 1 else 0,
                        (1 if self._board[x + 1, y] else 0) if x < self._height - 1 else 0,
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
                    self._piece_board[i, j + 1].left if j < self._width - 1 and self._piece_board[i, j + 1] else 0):
                        return False
                    if piece.down != (
                    self._piece_board[i + 1, j].up if i < self._height - 1 and self._piece_board[i + 1, j] else 0):
                        return False
                    if piece.left != (
                    self._piece_board[i, j - 1].right if j > 0 and self._piece_board[i, j - 1] else 0):
                        return False
        return True

    def _game_of_life(self):
        new_board = np.copy(self._board)
        for x in range(self._height):
            for y in range(self._width):
                live_neighbours = sum([
                    self._board[x - 1, y - 1] if x > 0 and y > 0 else 0,
                    self._board[x - 1, y] if x > 0 else 0,
                    self._board[x - 1, y + 1] if x > 0 and y < self._width - 1 else 0,
                    self._board[x, y - 1] if y > 0 else 0,
                    self._board[x, y + 1] if y < self._width - 1 else 0,
                    self._board[x + 1, y - 1] if x < self._height - 1 and y > 0 else 0,
                    self._board[x + 1, y] if x < self._height - 1 else 0,
                    self._board[x + 1, y + 1] if x < self._height - 1 and y < self._width - 1 else 0
                ])

                if self._board[x, y] == 1:
                    if (live_neighbours < Utils.GAME_OF_LIFE_LIVE_LOW_NEIGHBOUR_NUMBER
                            or live_neighbours > Utils.GAME_OF_LIFE_DIE_HIGH_NEIGHBOUR_NUMBER):
                        new_board[x, y] = 0
                else:
                    if live_neighbours < Utils.GAME_OF_LIFE_LIVE_LOW_NEIGHBOUR_NUMBER:
                        new_board[x, y] = 1

        self._board = new_board

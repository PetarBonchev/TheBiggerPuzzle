import random
import numpy as np

class Piece:

    SIDES = 4

    def __init__(self, connections):

        if type(connections) != list or len(connections) != Piece.SIDES:
            raise ValueError("Piece must take list with 4 elements")

        if any(item != 0 and item != 1 for item in connections):
            raise ValueError(f"List 'connections' in Piece initialization must contain only values 0 and 1: {connections}")

        self._connections = connections

    def __repr__(self):
        return f"Piece({self._connections})"

    @property
    def up(self):
        return self._connections[0]

    @property
    def right(self):
        return self._connections[1]

    @property
    def down(self):
        return self._connections[2]

    @property
    def left(self):
        return self._connections[3]

    @property
    def state(self):
        return (self.up << 3) | (self.right << 2) | (self.down << 1) | self.left

    def rotate(self, times=1):
        if times % 4 == 1:
            self._connections[0], self._connections[1], self._connections[2], self._connections[3] = (
                self.left, self.up, self.right, self.down)
        elif times % 4 == 2:
            self._connections[0], self._connections[2] = self.down, self.up
            self._connections[1], self._connections[3] = self.left, self.right
        elif times % 4 == 3:
            self._connections[0], self._connections[1], self._connections[2], self._connections[3] = (
                self.right, self.down, self.left, self.up)


class Board:

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self._board = np.array([[0 for _ in range(width)] for _ in range(height)])
        self._generate()

    def __getitem__(self, item):
        return self._board[item]

    def __repr__(self):
        board_repr = ""
        for row in self._board:
            row_repr = ""
            for cell in row:
                row_repr += str(cell) + " "
            board_repr += row_repr + "\n"
        return f"Board({self.width, self.height})\n" + board_repr

    def _generate(self):
        placed = 0
        while placed < (3 * self.height * self.width) // 4:
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
                        (1 if self._board[x - 1, y] else 0) if x > 0 else 0,  # Up
                        (1 if self._board[x, y + 1] else 0) if y < self.width - 1 else 0,  # Right
                        (1 if self._board[x + 1, y] else 0) if x < self.height - 1 else 0,  # Down
                        (1 if self._board[x, y - 1] else 0) if y > 0 else 0  # Left
                    ]
                    piece = Piece(connections)
                    piece.rotate(random.randint(0, 3))
                    self._board[x, y] = piece.state


board = Board(4, 5)
print(board)


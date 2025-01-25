import random
import pygame
import copy
import GlobalVariables
from AnchorCalculator import Anchor
from GameObject import GameObject
from LevelSystem import LevelSystem
from LoopPieceUI import LoopPiece
from Button import Button
from Text import Text


class InfinityLoop(GameObject):

    def __init__(self, width, height, game_data=None, name='infinity_loop'):
        super().__init__(name)
        self._height = height
        self._width = width
        self._part_width = GlobalVariables.IL_PIECE_WIDTH
        self._part_height = GlobalVariables.IL_PIECE_HEIGHT
        self._board = [[0 for _ in range(width)] for _ in range(height)]
        self._piece_board = [[None for _ in range(width)] for _ in range(height)]
        self._piece_length = 2 * self._part_height - self._part_width
        self._top_left_x, self._top_left_y = Anchor.center(self._part_height - self._part_width, self._part_height -
                                self._part_width, self._width * self._piece_length, self._height * self._piece_length)
        self._game_data = game_data
        self._set_game = False
        self._level_id = -1
        restart_button = Button(80, 50, *Anchor.top_left(70, 10), pygame.Color('orange'), text="Restart",
                                name='restart_button')
        restart_button.add_on_click(self.reset, game_data=self._game_data)
        message_text = Text(*Anchor.top_middle(0, 40, 0), '', pygame.Color('black'), 50, 'score_text')

        self.add_child(message_text)
        self.add_child(restart_button)
        self.new_game()

    def new_game(self):
        self._piece_board = [[None for _ in range(self._width)] for _ in range(self._height)]
        self.children = [self.get_object_by_name('restart_button'), self.get_object_by_name('score_text')]
        self.get_object_by_name('score_text').set_text('')

        if self._game_data:
            self._board = copy.deepcopy(self._game_data)
        else:
            self._board = [[0 for _ in range(self._width)] for _ in range(self._height)]
            for i in range(self._height):
                for j in range(self._width):
                    if random.random() > 0.5:
                        self._board[i][j] = 1

            for i in range(5):
                self._game_of_life()

        for x in range(self._height):
            for y in range(self._width):
                if self._board[x][y] == 1:
                    connections = [
                        (1 if self._board[x - 1][y] else 0) if x > 0 else 0,
                        (1 if self._board[x][y + 1] else 0) if y < self._width - 1 else 0,
                        (1 if self._board[x + 1][y] else 0) if x < self._height - 1 else 0,
                        (1 if self._board[x][y - 1] else 0) if y > 0 else 0
                    ]
                    piece = LoopPiece(connections, self._top_left_x + y * self._piece_length, self._top_left_y + x * self._piece_length)
                    piece.rotate(random.randint(0, 3))
                    self._board[x][y] = piece.state
                    self._piece_board[x][y] = piece
                    self.add_child(piece)

    def reset(self, width=-1, height=-1, game_data=None, level_number=-1):

        if not self._set_game:
            if width == height == -1:
                self._width = random.randint(3, 12)
                self._height = random.randint(4, 9)
            else:
                self._width = width
                self._height = height
            self._game_data = game_data
        else:
            if width != -1 and height != -1:
                self._width = width
                self._height = height
            if game_data:
                self._game_data = game_data

        self._level_id = level_number
        self._top_left_x, self._top_left_y = Anchor.center(self._part_height - self._part_width, self._part_height -
                                                           self._part_width, self._width * self._piece_length,
                                                           self._height * self._piece_length)

        self.new_game()


    def change_game_mode(self, is_set_game):
        self._set_game = is_set_game

    def _update(self):
        if self._is_solved():
            if self._set_game:
                self.get_object_by_name('score_text').set_text('You win!')
                LevelSystem.complete_level(GlobalVariables.INFINITY_LOOP_GAME_ID, self._level_id)
            else:
                self.reset()

    def _is_solved(self):
        for i in range(len(self._piece_board)):
            for j in range(len(self._piece_board[i])):
                piece = self._piece_board[i][j]
                if piece:
                    if piece.up != (self._piece_board[i - 1][j].down if i > 0 and self._piece_board[i - 1][j] else 0):
                        return False
                    if piece.right != (
                            self._piece_board[i][j + 1].left if j < self._width - 1 and self._piece_board[i][
                                j + 1] else 0):
                        return False
                    if piece.down != (
                            self._piece_board[i + 1][j].up if i < self._height - 1 and self._piece_board[i + 1][
                                j] else 0):
                        return False
                    if piece.left != (
                            self._piece_board[i][j - 1].right if j > 0 and self._piece_board[i][j - 1] else 0):
                        return False
        return True

    def _game_of_life(self):
        new_board = copy.deepcopy(self._board)
        for x in range(self._height):
            for y in range(self._width):
                live_neighbours = sum([
                    self._board[x - 1][y - 1] if x > 0 and y > 0 else 0,
                    self._board[x - 1][y] if x > 0 else 0,
                    self._board[x - 1][y + 1] if x > 0 and y < self._width - 1 else 0,
                    self._board[x][y - 1] if y > 0 else 0,
                    self._board[x][y + 1] if y < self._width - 1 else 0,
                    self._board[x + 1][y - 1] if x < self._height - 1 and y > 0 else 0,
                    self._board[x + 1][y] if x < self._height - 1 else 0,
                    self._board[x + 1][y + 1] if x < self._height - 1 and y < self._width - 1 else 0
                ])

                if self._board[x][y] == 1:
                    if (live_neighbours < 2
                            or live_neighbours > 6):
                        new_board[x][y] = 0
                else:
                    if live_neighbours < 3:
                        new_board[x][y] = 1

        self._board = new_board

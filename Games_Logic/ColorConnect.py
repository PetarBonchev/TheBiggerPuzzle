import random
import pygame
from Utilities import ColorConnectGenerator, GlobalVariables
from Utilities.AnchorCalculator import Anchor
from UI_Elements.GameObject import GameObject
from UI_Elements.LevelSystem import LevelSystem
from UI_Elements.PointConnectUi import PointConnect
from UI_Elements.LineConnectUI import LineConnect
from UI_Elements.Button import Button
from UI_Elements.Text import Text


class ColorConnect(GameObject):

    POINT_RADIUS = GlobalVariables.CC_TILE_SIZE * 3 / 7

    def __init__(self, width, height, color_count, game_data=None, name='color_connect'):
        super().__init__(name)
        self._width = width
        self._height = height
        self._color_count = color_count
        self._generator = ColorConnectGenerator.ColorTableGenerator(width, height, color_count)
        self._top_left_x, self._top_left_y = Anchor.center(0, 0,
                                                           self._width * GlobalVariables.CC_TILE_SIZE, self._height * GlobalVariables.CC_TILE_SIZE)
        self._board = [[None for _ in range(self._width)] for _ in range(self._height)]
        self._point_pairs = {}
        self._selected_item = None
        self._time_pressed = 0
        self._game_data = game_data
        self._set_game = False
        self._level_id = -1
        restart_button = Button(100, 50, *Anchor.top_left(70, 10), pygame.Color('orange'), text="Restart",
                                name='restart_button')
        restart_button.add_on_click(self.reset)
        message_text = Text(*Anchor.top_middle(0, 40, 0), '', pygame.Color('black'), 50, 'score_text')

        self.add_child(message_text)
        self.add_child(restart_button)
        self.reset()

    def _draw(self, screen):
        self._draw_grid(screen)

        for row in self._board:
            for item in row:
                if item:
                    item.draw(screen)

    def _check_click(self, mouse_x, mouse_y):
        for row in self._board:
            for item in row:
                if item:
                    if item.check_click(mouse_x, mouse_y):
                        self._selected_item = item

    def _update(self):
        if self._selected_item:
            if not pygame.mouse.get_pressed()[0]:
                if isinstance(self._selected_item, PointConnect):
                    if self._time_pressed < GlobalVariables.CLICK_HOLD_FRAMES_THRESHOLD:
                        self._remove_line(self._selected_item)
                        other_x, other_y = self._point_pairs[(self._selected_item.board_x, self._selected_item.board_y)]
                        self._remove_line(self._board[other_x][other_y])
                else:
                    if self._time_pressed < GlobalVariables.CLICK_HOLD_FRAMES_THRESHOLD:
                        self._remove_line(self._selected_item)
                    elif self._selected_item.next and self._selected_item.next.next:
                        self._remove_line(self._selected_item.next)
                self._selected_item = None
                self._time_pressed = 0
            else:
                self._time_pressed += 1
                mouse_pos = pygame.mouse.get_pos()
                board_y = (mouse_pos[0] - self._top_left_x) // GlobalVariables.CC_TILE_SIZE
                board_x = (mouse_pos[1] - self._top_left_y) // GlobalVariables.CC_TILE_SIZE
                if board_x < 0 or board_y < 0 or board_x >= self._height or board_y >= self._width:
                    pass
                elif ColorConnect._are_neighbours(board_x, board_y, self._selected_item.board_x,
                                                  self._selected_item.board_y):

                    if isinstance(self._selected_item, PointConnect):
                        other_x, other_y = self._point_pairs[
                            (self._selected_item.board_x, self._selected_item.board_y)]
                        self._remove_line(self._board[other_x][other_y])
                    if self._selected_item.next:
                        self._remove_line(self._selected_item.next)

                    if not self._board[board_x][board_y]:
                        new_line = self._create_line_connect(board_x, board_y, self._selected_item.color)
                        self._board[board_x][board_y] = new_line
                        new_line.prev = self._selected_item
                        self._selected_item.next = new_line
                        self._selected_item = new_line
                    else:
                        if self._board[board_x][board_y] is self._selected_item.prev:
                            self._remove_line(self._selected_item)
                            self._selected_item = self._board[board_x][board_y]
                        elif isinstance(self._board[board_x][board_y], PointConnect) and (
                                self._board[board_x][board_y].color == self._selected_item.color):
                            self._board[board_x][board_y].prev = self._selected_item
                            self._selected_item.next = self._board[board_x][board_y]
            if self._is_board_solved():
                if self._set_game:
                    self.get_object_by_name('score_text').set_text('You win!')
                    LevelSystem.complete_level(GlobalVariables.COLOR_CONNECT_GAME_ID, self._level_id)
                    GlobalVariables.window_system.get_object_by_name('bigger_puzzle').update_solved_puzzles()
                else:
                    self.reset()

    def new_game(self):
        self._board = [[None for _ in range(self._width)] for _ in range(self._height)]
        self._selected_item = None
        self._point_pairs = {}
        self._top_left_x, self._top_left_y = Anchor.center(0, 0,
                                                           self._width * GlobalVariables.CC_TILE_SIZE, self._height * GlobalVariables.CC_TILE_SIZE)
        self.get_object_by_name('score_text').set_text('')
        if self._game_data:
            trails = self._game_data
        else:
            self._generator = ColorConnectGenerator.ColorTableGenerator(self._width, self._height, self._color_count)
            trails = self._generator.generate()

        color_id = 0
        for trail in trails:
            point_1 = self._create_point_connect(trail[0][0], trail[0][1], GlobalVariables.COLORS[color_id % len(
                GlobalVariables.COLORS)])
            point_2 = self._create_point_connect(trail[-1][0], trail[-1][1], GlobalVariables.COLORS[color_id % len(
                GlobalVariables.COLORS)])

            self._board[trail[0][0]][trail[0][1]] = point_1
            self._board[trail[-1][0]][trail[-1][1]] = point_2

            self._point_pairs[(point_1.board_x, point_1.board_y)] = (point_2.board_x, point_2.board_y)
            self._point_pairs[(point_2.board_x, point_2.board_y)] = (point_1.board_x, point_1.board_y)

            color_id += 1

    def reset(self, width=-1, height=-1, color_count=-1, game_data=None, level_number=-1):
        if self._set_game:
            if game_data:
                self._width = width
                self._height = height
                self._color_count = color_count
                self._game_data = game_data
                self._level_id = level_number
            self.get_object_by_name('restart_button').set_text('Restart')
            self.new_game()
            return

        if width == height == -1:
            self._width = random.randint(4, 16)
            self._height = random.randint(4, 10)
            self._color_count = max(3, min(12, self._width * self._height // 9))
        else:
            self._width = width
            self._height = height
            self._color_count = color_count
        self.get_object_by_name('restart_button').set_text('New game')
        self._game_data = game_data
        self.new_game()

    def change_game_mode(self, is_set_game):
        self._set_game = is_set_game

    def _draw_grid(self, screen):
        for i in range(self._height + 1):
            pygame.draw.line(screen, pygame.Color('black'), (self._top_left_x, self._top_left_y +
                                                             i * GlobalVariables.CC_TILE_SIZE),
                             (self._top_left_x + self._width * GlobalVariables.CC_TILE_SIZE,
                              self._top_left_y + i * GlobalVariables.CC_TILE_SIZE))
        for i in range(self._width + 1):
            pygame.draw.line(screen, pygame.Color('black'), (self._top_left_x + i * GlobalVariables.CC_TILE_SIZE,
                                                             self._top_left_y),
                             (self._top_left_x + i * GlobalVariables.CC_TILE_SIZE,
                              self._top_left_y + self._height * GlobalVariables.CC_TILE_SIZE))

    def _create_point_connect(self, x, y, color):
        return PointConnect(self._top_left_x + y * GlobalVariables.CC_TILE_SIZE + GlobalVariables.CC_TILE_SIZE // 2,
                            self._top_left_y + x * GlobalVariables.CC_TILE_SIZE + GlobalVariables.CC_TILE_SIZE // 2,
                            ColorConnect.POINT_RADIUS, color, GlobalVariables.CC_TILE_SIZE, x, y)

    def _create_line_connect(self, x, y, color):
        return LineConnect(self._top_left_x + y * GlobalVariables.CC_TILE_SIZE + GlobalVariables.CC_TILE_SIZE // 2,
                           self._top_left_y + x * GlobalVariables.CC_TILE_SIZE + GlobalVariables.CC_TILE_SIZE // 2,
                           color, GlobalVariables.CC_TILE_SIZE, x, y)

    def _remove_line(self, line):
        if isinstance(line, PointConnect):
            line_to_go = line.next
            line.next = None
            line.prev = None
            line = line_to_go
        while line:
            if isinstance(line, PointConnect):
                line.prev = None
                break
            self._board[line.board_x][line.board_y] = None
            line = line.next

    def _is_board_solved(self):
        for coordinates in self._point_pairs.values():
            if not self._board[coordinates[0]][coordinates[1]].prev and not self._board[coordinates[0]][coordinates[1]].next:
                return False

        for row in self._board:
            for item in row:
                if not item:
                    return False

        return True

    @staticmethod
    def _are_neighbours(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2) == 1
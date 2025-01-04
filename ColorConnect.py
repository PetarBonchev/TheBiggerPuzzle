import pygame

import ColorConnectGenerator
import Utils
from UIManager import PointConnect, LineConnect


class ColorConnect:

    TILE_SIZE = 60
    POINT_RADIUS = 20

    def __init__(self, width, height, color_count):
        self._width = width
        self._height = height
        self._color_count = color_count
        self._generator = ColorConnectGenerator.TableGenerator(width, height, color_count)
        self._top_left_x = (Utils.screen_width - self._width * ColorConnect.TILE_SIZE) // 2
        self._top_left_y = (Utils.screen_height - self._height * ColorConnect.TILE_SIZE) // 2
        self._board = [[None for _ in range(self._width)] for _ in range(self._height)]
        self._point_pairs = {}
        self._selected_item = None

        self.generate()

    def draw(self, screen):
        self._draw_grid(screen)

        for row in self._board:
            for item in row:
                if item:
                    item.draw(screen)

    def check_click(self, mouse_x, mouse_y):
        for row in self._board:
            for item in row:
                if item:
                    if item.check_click(mouse_x, mouse_y):
                        self._selected_item = item

    def update(self):
        if self._selected_item:
            if not pygame.mouse.get_pressed()[0]:
                if isinstance(self._selected_item, PointConnect):
                    self._remove_line(self._selected_item)
                    other_x, other_y = self._point_pairs[(self._selected_item.board_x, self._selected_item.board_y)]
                    self._remove_line(self._board[other_x][other_y])
                else:
                    self._remove_line(self._selected_item.next)
                self._selected_item = None
            else:
                mouse_pos = pygame.mouse.get_pos()
                board_y = (mouse_pos[0] - self._top_left_x) // ColorConnect.TILE_SIZE
                board_x = (mouse_pos[1] - self._top_left_y) // ColorConnect.TILE_SIZE
                if board_x < 0 or board_y < 0 or board_x >= self._height or board_y >= self._width:
                    pass
                elif ColorConnect._are_neighbours(board_x, board_y, self._selected_item.board_x,
                                                  self._selected_item.board_y):
                    if not self._board[board_x][board_y]:
                        if self._selected_item.next:
                            self._remove_line(self._selected_item.next)
                        elif isinstance(self._selected_item, PointConnect):
                            other_x, other_y = self._point_pairs[
                                (self._selected_item.board_x, self._selected_item.board_y)]
                            self._remove_line(self._board[other_x][other_y])
                        new_line = self._create_line_connect(board_x, board_y, self._selected_item.color)
                        self._board[board_x][board_y] = new_line
                        new_line.prev = self._selected_item
                        self._selected_item.next = new_line
                        self._selected_item = new_line
                    else:
                        if self._board[board_x][board_y] is self._selected_item.prev:
                            self._remove_line(self._selected_item)
                            self._selected_item = self._board[board_x][board_y]
                        if isinstance(self._board[board_x][board_y], PointConnect) and (
                                self._board[board_x][board_y].color == self._selected_item.color):
                            self._board[board_x][board_y].prev = self._selected_item
                            self._selected_item.next = self._board[board_x][board_y]
            if self._is_board_solved():
                self.generate()

    def generate(self):
        self._board = [[None for _ in range(self._width)] for _ in range(self._height)]
        self._selected_item = None
        self._point_pairs = {}
        trails = self._generator.generate()

        color_id = 0
        for trail in trails:
            point_1 = self._create_point_connect(trail[0][0], trail[0][1], Utils.COLORS[color_id % len(Utils.COLORS)])
            point_2 =  self._create_point_connect(trail[-1][0], trail[-1][1], Utils.COLORS[color_id % len(Utils.COLORS)])

            self._board[trail[0][0]][trail[0][1]] = point_1
            self._board[trail[-1][0]][trail[-1][1]] = point_2

            self._point_pairs[(point_1.board_x, point_1.board_y)] = (point_2.board_x, point_2.board_y)
            self._point_pairs[(point_2.board_x, point_2.board_y)] = (point_1.board_x, point_1.board_y)

            color_id += 1

    def _draw_grid(self, screen):
        for i in range(self._height + 1):
            pygame.draw.line(screen, pygame.Color('black'), (self._top_left_x, self._top_left_y +
                                                             i * ColorConnect.TILE_SIZE),
                             (self._top_left_x + self._width * ColorConnect.TILE_SIZE,
                              self._top_left_y + i * ColorConnect.TILE_SIZE))
        for i in range(self._width + 1):
            pygame.draw.line(screen, pygame.Color('black'), (self._top_left_x + i * ColorConnect.TILE_SIZE,
                                                             self._top_left_y),
                             (self._top_left_x + i * ColorConnect.TILE_SIZE,
                              self._top_left_y + self._height * ColorConnect.TILE_SIZE))

    def _create_point_connect(self, x, y, color):
        return PointConnect(self._top_left_x + y * ColorConnect.TILE_SIZE + ColorConnect.TILE_SIZE // 2,
                            self._top_left_y + x * ColorConnect.TILE_SIZE + ColorConnect.TILE_SIZE // 2,
                            ColorConnect.POINT_RADIUS, color, ColorConnect.TILE_SIZE, x, y)

    def _create_line_connect(self, x, y, color):
        return LineConnect(self._top_left_x + y * ColorConnect.TILE_SIZE + ColorConnect.TILE_SIZE // 2,
                            self._top_left_y + x * ColorConnect.TILE_SIZE + ColorConnect.TILE_SIZE // 2,
                            color, ColorConnect.TILE_SIZE, x, y)

    def _remove_line(self, line):
        if isinstance(line, PointConnect):
            line_to_go = line.next
            line.next = None
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
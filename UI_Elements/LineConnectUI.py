import pygame
from UI_Elements.GameObject import GameObject


class LineConnect(GameObject):

    def __init__(self, center_x, center_y, color, side_size, board_x, board_y, name='line_connect'):
        super().__init__(name)
        self._side_size = side_size
        self.color = color
        self._center_y = center_y
        self._center_x = center_x
        self._line_width = self._side_size // 2
        self.board_x = board_x
        self.board_y = board_y
        self.prev = None
        self.next = None

    def draw(self, screen):

        if not self.next or self.prev.board_x == self.next.board_x or self.prev.board_y == self.next.board_y:
            if self.board_x == self.prev.board_x:
                pygame.draw.rect(screen, self.color, (self._center_x - self._side_size // 2, self._center_y -
                                            self._side_size // 4, self._side_size, self._line_width))
            else:
                pygame.draw.rect(screen, self.color, (self._center_x - self._side_size // 4, self._center_y -
                                            self._side_size // 2, self._line_width, self._side_size))
        else:
            self._draw_half_line_from_center(screen, self.prev)
            self._draw_half_line_from_center(screen, self.next)

    def check_click(self, mouse_x, mouse_y):
        return self._center_x - self._side_size // 2 <= mouse_x < self._center_x + self._side_size // 2 and (
                self._center_y - self._side_size // 2 <= mouse_y < self._center_y + self._side_size // 2)

    def _draw_half_line_from_center(self, screen, item_towards):
        if self.board_x < item_towards.board_x:
            pygame.draw.rect(screen, self.color, (self._center_x - self._side_size // 4,
                                                  self._center_y - self._side_size // 4,
                                                  self._line_width, 3 * self._side_size // 4))
        elif self.board_x > item_towards.board_x:
            pygame.draw.rect(screen, self.color, (self._center_x - self._side_size // 4,
                                                  self._center_y - self._side_size // 2,
                                                  self._line_width, 3 * self._side_size // 4))
        elif self.board_y < item_towards.board_y:
            pygame.draw.rect(screen, self.color, (self._center_x - self._side_size // 4,
                                                  self._center_y - self._side_size // 4,
                                                  3 * self._side_size // 4, self._line_width))
        elif self.board_y > item_towards.board_y:
            pygame.draw.rect(screen, self.color, (self._center_x - self._side_size // 2,
                                                  self._center_y - self._side_size // 4,
                                                  3 * self._side_size // 4, self._line_width))
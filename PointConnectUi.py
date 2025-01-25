import pygame
from GameObject import GameObject


class PointConnect(GameObject):

    def __init__(self, center_x, center_y, radius, color, click_box_size, board_x, board_y, name='point_connect'):
        super().__init__(name)
        self._radius = radius
        self._click_box_size = click_box_size
        self._line_width = click_box_size // 2
        self._center_y = center_y
        self._center_x = center_x
        self.board_x = board_x
        self.board_y = board_y
        self.color = color
        self.prev = None
        self.next = None

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self._center_x, self._center_y), self._radius)
        if self.prev:
            self._draw_half_line_from_center(screen, self.prev)
        elif self.next:
            self._draw_half_line_from_center(screen, self.next)

    def check_click(self, mouse_x, mouse_y):
        return self._center_x - self._click_box_size // 2 <= mouse_x < self._center_x + self._click_box_size // 2 and (
            self._center_y - self._click_box_size // 2 <= mouse_y < self._center_y + self._click_box_size // 2)

    def update(self):
        pass

    def _draw_half_line_from_center(self, screen, item_towards):
        if self.board_x < item_towards.board_x:
            pygame.draw.rect(screen, self.color, (self._center_x - self._click_box_size // 4,
                                                  self._center_y - self._click_box_size // 4,
                                                  self._line_width, 3 * self._click_box_size // 4))
        elif self.board_x > item_towards.board_x:
            pygame.draw.rect(screen, self.color, (self._center_x - self._click_box_size // 4,
                                                  self._center_y - self._click_box_size // 2,
                                                  self._line_width, 3 * self._click_box_size // 4))
        elif self.board_y < item_towards.board_y:
            pygame.draw.rect(screen, self.color, (self._center_x - self._click_box_size // 4,
                                                  self._center_y - self._click_box_size // 4,
                                                  3 * self._click_box_size // 4, self._line_width))
        elif self.board_y > item_towards.board_y:
            pygame.draw.rect(screen, self.color, (self._center_x - self._click_box_size // 2,
                                                  self._center_y - self._click_box_size // 4,
                                                  3 * self._click_box_size // 4, self._line_width))

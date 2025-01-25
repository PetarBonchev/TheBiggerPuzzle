import pygame
import GlobalVariables
from GameObject import GameObject


class Flask(GameObject):

    BOTTOM_CORNERS_RADIUS = 22
    BONUS_HEIGHT_WHEN_SELECTED = 20

    def __init__(self, height, bottom_left_x, bottom_left_y, name='flask'):
        super().__init__(name)
        self._bottom_left_x = bottom_left_x
        self._bottom_left_y = bottom_left_y
        self._height = height
        self.content = []

    def move_top(self):
        count_ = self._top_count
        top_elements = self.content[-count_:]
        self.content = self.content[:-count_]
        return top_elements

    def receive_top(self, color_stream):
        self.content.extend(color_stream)

    def select(self):
        self._bottom_left_y -= Flask.BONUS_HEIGHT_WHEN_SELECTED

    def deselect(self):
        self._bottom_left_y += Flask.BONUS_HEIGHT_WHEN_SELECTED

    def is_clicked(self, mouse_x, mouse_y):
        return self._bottom_left_x <= mouse_x <= self._bottom_left_x + GlobalVariables.WS_FLASK_WIDTH and (
                self._bottom_left_y - self._height * GlobalVariables.WS_FLASK_HEIGHT <= mouse_y <= self._bottom_left_y)

    @property
    def water_height(self):
        return len(self.content)

    @property
    def top_color(self):
        if self.content:
            return self.content[-1]
        return -1

    @property
    def complete(self):
        return len(self.content) == self._top_count == self._height or len(self.content) == 0

    @property
    def _top_count(self):
        if len(self.content) == 0:
            return 0
        i = len(self.content) - 1
        while i >= 0 and self.content[i] == self.content[-1]:
            i -= 1
        return len(self.content) - i - 1

    def _draw(self, screen):
        for i in range(self._height):
            color = pygame.Color('grey') if i >= len(self.content) \
                else GlobalVariables.COLORS[self.content[i] % len(GlobalVariables.COLORS)]
            if i == 0:
                rect = pygame.Rect(self._bottom_left_x, self._bottom_left_y - GlobalVariables.WS_FLASK_HEIGHT,
                                   GlobalVariables.WS_FLASK_WIDTH, GlobalVariables.WS_FLASK_HEIGHT)
                pygame.draw.rect(screen, color, rect, 0, 0, 0, 0,
                                 Flask.BOTTOM_CORNERS_RADIUS, Flask.BOTTOM_CORNERS_RADIUS)
                pygame.draw.rect(screen, pygame.Color('black'), rect, 2, 0, 0, 0,
                                 Flask.BOTTOM_CORNERS_RADIUS, Flask.BOTTOM_CORNERS_RADIUS)
            else:
                rect = pygame.Rect(self._bottom_left_x, self._bottom_left_y - (i + 1) * GlobalVariables.WS_FLASK_HEIGHT,
                                   GlobalVariables.WS_FLASK_WIDTH, GlobalVariables.WS_FLASK_HEIGHT)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, pygame.Color('black'), rect, 2)

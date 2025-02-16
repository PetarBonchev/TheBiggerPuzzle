from UI_Elements.Button import Button
from UI_Elements.Text import Text
from Utilities.PuzzlePointsCalculator import PuzzlePointsCalculator
import pygame


class PuzzlePart(Button):

    def __init__(self, top_left_x, top_left_y, sides, size=300, background_color=pygame.Color('orange'),
                 text=None, score_text=None, text_color=pygame.Color('black'), font_size=25, name='puzzle_part'):
        super().__init__(size, size, top_left_x, top_left_y, name=name, text=text, text_color=text_color,
                         font_size=font_size)
        self._top_left_x = top_left_x
        self._top_left_y = top_left_y
        self._sides = sides
        self._points = PuzzlePointsCalculator.get_shape_points((self._top_left_x, self._top_left_y), size, 2 * size / 7,
                                                    self._sides)
        self._background_color = background_color
        self._is_transparent = False

        if score_text:
            self.add_child(
                Text(self._top_left_x + size / 2, self._top_left_y + size / 2 + 25, '0/0', name='score_text'))

    def make_transparent(self):
        self._is_transparent = True

    def _draw(self, screen):
        text_obj = self.get_object_by_name('text')

        if self._is_hovered():
            text_obj.set_active(True)
            pygame.draw.polygon(screen, pygame.Color('white'), self._points)
        else:
            if self._is_transparent:
                text_obj.set_active(False)
            else:
                pygame.draw.polygon(screen, self._background_color, self._points)

        pygame.draw.polygon(screen, pygame.Color('black'), self._points, width=2)

    def _is_hovered(self):
        return PuzzlePointsCalculator.is_point_inside_polygon(pygame.mouse.get_pos(), self._points)
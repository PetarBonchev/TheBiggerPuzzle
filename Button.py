import pygame
from GameObject import GameObject
from Text import Text

class Button(GameObject):

    ROUND_CORNERS_RADIUS = 10

    def __init__(self, width, height, top_left_x, top_left_y, fill_color=pygame.Color('grey'),
                 outline_width=2, outline_color=pygame.Color('black'),
                 text=None, text_color=pygame.Color('black'), font_size=25, name='button'):
        super().__init__(name)

        self._width = width
        self._height = height
        self._top_left_x = top_left_x
        self._top_left_y = top_left_y
        self._fill_color = fill_color
        self._outline_width = outline_width
        self._outline_color = outline_color
        if text:
            text = Text(self._top_left_x + self._width // 2, self._top_left_y + self._height // 2, text, text_color,
                        font_size, name + '_text')
            self.add_child(text)
        self._on_click = []

    def add_on_click(self, func, *args, **kwargs):
        self._on_click.append((func, args, kwargs))

    def clear_on_click(self):
        self._on_click = []

    def _draw(self, screen):
        if self._is_hovered():
            pygame.draw.rect(screen, pygame.Color('white'), pygame.Rect(self._top_left_x, self._top_left_y,
                                    self._width, self._height), border_radius=Button.ROUND_CORNERS_RADIUS)
        else:
            pygame.draw.rect(screen, self._fill_color, pygame.Rect(self._top_left_x, self._top_left_y,
                                    self._width, self._height), border_radius=Button.ROUND_CORNERS_RADIUS)
        if self._outline_width:
            pygame.draw.rect(screen, self._outline_color, pygame.Rect(self._top_left_x, self._top_left_y,
                            self._width, self._height), self._outline_width, Button.ROUND_CORNERS_RADIUS)

    def _check_click(self, mouse_x, mouse_y):
        if self._is_hovered():
            for for_call in self._on_click:
                for_call[0](*for_call[1], **for_call[2])
            return True
        return False

    def _is_hovered(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self._top_left_x <= mouse_x <= self._top_left_x + self._width and \
            self._top_left_y <= mouse_y <= self._top_left_y + self._height

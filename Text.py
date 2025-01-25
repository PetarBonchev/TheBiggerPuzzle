import pygame
from GameObject import GameObject


class Text(GameObject):

    def __init__(self, center_x, center_y, text='', color=pygame.Color('black'), font_size=25, name='text'):
        super().__init__(name)

        self._center_x = center_x
        self._center_y = center_y
        self._color = color
        self._font = pygame.font.Font(None, font_size)
        self._rendered_text = None
        self._text_rect = None
        self.set_text(text)

    def set_text(self, text):
        self._rendered_text = self._font.render(text, True, self._color)
        self._text_rect = self._rendered_text.get_rect(center=(self._center_x, self._center_y))

    def _draw(self, screen):
        screen.blit(self._rendered_text, self._text_rect)
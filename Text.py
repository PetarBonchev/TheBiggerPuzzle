import pygame
import os
from GameObject import GameObject


class Text(GameObject):

    def __init__(self, center_x, center_y, text='', color=pygame.Color('black'),
                 font_size=25, name='text', font_path='Tasqib.otf'):
        super().__init__(name)

        self._center_x = center_x
        self._center_y = center_y
        self._color = color
        self._font_size = font_size
        self._font_path = font_path
        self._text = text
        self._rendered_text = None
        self._text_rect = None

        self._load_font()
        self.set_text(text)

    def _load_font(self):
        if self._font_path:
            if os.path.exists(self._font_path):
                self._font = pygame.font.Font(self._font_path, self._font_size)
        else:
            self._font = pygame.font.SysFont(None, self._font_size)

    def set_text(self, text):
        self._rendered_text = self._font.render(text, True, self._color)
        self._text_rect = self._rendered_text.get_rect(center=(self._center_x, self._center_y))

    def _draw(self, screen):
        screen.blit(self._rendered_text, self._text_rect)
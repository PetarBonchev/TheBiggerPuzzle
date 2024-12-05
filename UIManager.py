import pygame

class Button:

    def __init__(self, width, height, top_left_x, top_left_y, color, text = None, text_color = None,
                 text_size = None, outline_color = None, outline_width = None):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.width = width
        self.height = height

        self.color = color
        self.outline_width = outline_width
        self.outline_color = outline_color

        if text:
            font = pygame.font.Font(None, text_size)
            self.rendered_text = font.render(text, True, text_color)
            center_x = top_left_x + width // 2
            center_y = top_left_y + height // 2
            self.text_rect = self.rendered_text.get_rect(center=(center_x, center_y))
            self.text_rect.centery += self.rendered_text.get_height() // 10

        self.on_click = []

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.top_left_x, self.top_left_y,
                                                         self.width, self.height), max(self.width, self.height))
        if self.rendered_text:
            screen.blit(self.rendered_text, self.text_rect)
        if self.outline_color:
            pygame.draw.rect(screen, self.outline_color, pygame.Rect(self.top_left_x, self.top_left_y,
                                                         self.width, self.height), self.outline_width)
    def add_on_click(self, func, *args, **kwargs):
        self.on_click.append((func, args, kwargs))

    def check_click(self, mouse_x, mouse_y):
        if self.top_left_x <= mouse_x <= self.top_left_x + self.width and \
                self.top_left_y <= mouse_y <= self.top_left_y + self.height:
            for for_call in self.on_click:
                for_call[0](*for_call[1], **for_call[2])


import pygame
import math
import Utils


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

    def update(self):
        pass


class ColorWheel:

    EDGE_POINTS = 100
    CENTER_RATIO = 1 / 5
    OUTLINES_WIDTH = 5

    def __init__(self, color_count, center_x, center_y, radius):
        self._color_count = color_count
        self._center_x = center_x
        self._center_y = center_y
        self._radius = radius
        self._highlighted = set()

    def draw(self, screen):
        angle_step = 2 * math.pi / self._color_count
        for i in range(self._color_count):
            start_angle = i * angle_step
            end_angle = (i + 1) * angle_step
            color = Utils.COLORS[i % len(Utils.COLORS)]
            if i in self._highlighted:
                color = pygame.Color('White')

            points = [(self._center_x, self._center_y)]
            for j in range(ColorWheel.EDGE_POINTS):
                angle = start_angle + j * (end_angle - start_angle) / ColorWheel.EDGE_POINTS
                x = self._center_x + self._radius * math.cos(angle)
                y = self._center_y - self._radius * math.sin(angle)
                points.append((x, y))

            pygame.draw.polygon(screen, color, points)

        pygame.draw.circle(screen, pygame.Color('Black'), (self._center_x, self._center_y),
                           self._radius * ColorWheel.CENTER_RATIO, 0)

        for i in range(self._color_count):
            start_angle = i * angle_step
            pygame.draw.line(screen, pygame.Color('Black'), (self._center_x, self._center_y),
                             (self._center_x + self._radius * math.cos(start_angle),
                              self._center_y - self._radius * math.sin(start_angle)), ColorWheel.OUTLINES_WIDTH)

        pygame.draw.circle(screen, pygame.Color('Black'), (self._center_x, self._center_y),
                           self._radius + ColorWheel.OUTLINES_WIDTH, ColorWheel.OUTLINES_WIDTH)

    def check_click(self, mouse_x, mouse_y):
        if (math.hypot(mouse_x - self._center_x, mouse_y - self._center_y) <
                self._radius * ColorWheel.CENTER_RATIO):
            return -1

        angle_step = 2 * math.pi / self._color_count
        click_angle = math.atan2(self._center_y - mouse_y, mouse_x - self._center_x)
        if click_angle < 0:
            click_angle += 2 * math.pi

        distance_from_center = math.hypot(mouse_x - self._center_x, mouse_y - self._center_y)

        if distance_from_center > self._radius:
            return -1

        sector_id = int(click_angle // angle_step)
        return sector_id

    def update(self):
        pass

    def highlight_sector(self, sector_id):
        if sector_id in self._highlighted:
            self._highlighted.remove(sector_id)
        else:
            self._highlighted.add(sector_id)
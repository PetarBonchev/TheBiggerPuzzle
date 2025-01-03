import pygame
import math
import Utils


class Button:
    def __init__(self, width, height, top_left_x, top_left_y, color, text=None, text_color=None,
                 text_size=None, outline_color=None, outline_width=None):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.width = width
        self.height = height

        self.color = color
        self.outline_width = outline_width
        self.outline_color = outline_color

        self.rendered_text = None
        self.text_rect = None
        if text:
            self.text_color = text_color
            self.font = pygame.font.Font(None, text_size)
            self.set_text(text)

        self.on_click = []

    def set_text(self, text):
        self.rendered_text = self.font.render(text, True, self.text_color)
        center_x = self.top_left_x + self.width // 2
        center_y = self.top_left_y + self.height // 2
        self.text_rect = self.rendered_text.get_rect(center=(center_x, center_y))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.top_left_x, self.top_left_y,
                                                         self.width, self.height))
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
    CENTER_RATIO = 1 / 4
    OUTLINES_WIDTH = 5
    HIGHLIGHT_TIME = 30

    def __init__(self, color_count, center_x, center_y, radius):
        self._color_count = color_count
        self._center_x = center_x
        self._center_y = center_y
        self._radius = radius
        self._highlighted = {}

    def draw(self, screen):
        angle_step = 2 * math.pi / self._color_count
        for i in range(self._color_count):
            start_angle = i * angle_step
            end_angle = (i + 1) * angle_step
            color = Utils.COLORS[i % len(Utils.COLORS)]
            if i in self._highlighted:
                color = pygame.Color('White')
                self._highlighted[i] -= 1
                if self._highlighted[i] <= 0:
                    self._highlighted.pop(i)

            points = [(self._center_x, self._center_y)]
            for j in range(ColorWheel.EDGE_POINTS + 1):
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
        self._highlighted[sector_id] = ColorWheel.HIGHLIGHT_TIME // 3
        return sector_id

    def update(self):
        pass

    def highlight_sector(self, sector_id):
        self._highlighted[sector_id] = ColorWheel.HIGHLIGHT_TIME

    def stop_all_highlight(self):
        self._highlighted.clear()


class Flask:

    PART_WIDTH = 55
    PART_HEIGHT = 60
    BOTTOM_CORNERS_RADIUS = 22

    def __init__(self, height, bottom_left_x, bottom_left_y):
        self._bottom_left_x = bottom_left_x
        self._bottom_left_y = bottom_left_y
        self._height = height
        self.content = []

    @property
    def top_color(self):
        if self.content:
            return self.content[-1]
        return -1

    @property
    def top_count(self):
        if len(self.content) == 0:
            return 0
        i = len(self.content) - 1
        while i >= 0 and self.content[i] == self.content[-1]:
            i -= 1
        return len(self.content) - i - 1

    @property
    def water_height(self):
        return len(self.content)

    @property
    def complete(self):
        return len(self.content) == self.top_count == self._height or len(self.content) == 0

    def move_top(self):
        count_ = self.top_count
        top_elements = self.content[-count_:]
        self.content = self.content[:-count_]
        return top_elements

    def receive_top(self, color_stream):
        self.content.extend(color_stream)

    def select(self):
        self._bottom_left_y -= 20

    def deselect(self):
        self._bottom_left_y += 20

    def draw(self, screen):
        for i in range(self._height):
            color = pygame.Color('grey') if i >= len(self.content) \
                else Utils.COLORS[self.content[i] % len(Utils.COLORS)]
            if i == 0:
                rect = pygame.Rect(self._bottom_left_x, self._bottom_left_y - Flask.PART_HEIGHT,
                                   Flask.PART_WIDTH, Flask.PART_HEIGHT)
                pygame.draw.rect(screen, color, rect, 0, 0, 0, 0,
                                 Flask.BOTTOM_CORNERS_RADIUS, Flask.BOTTOM_CORNERS_RADIUS)
                pygame.draw.rect(screen, pygame.Color('black'), rect, 2, 0, 0, 0,
                                 Flask.BOTTOM_CORNERS_RADIUS, Flask.BOTTOM_CORNERS_RADIUS)
            else:
                rect = pygame.Rect(self._bottom_left_x, self._bottom_left_y - (i + 1) * Flask.PART_HEIGHT,
                                   Flask.PART_WIDTH, Flask.PART_HEIGHT)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, pygame.Color('black'), rect, 2)

    def update(self):
        pass

    def check_click(self, mouse_x, mouse_y):
        return self._bottom_left_x <= mouse_x <= self._bottom_left_x + Flask.PART_WIDTH and (
            self._bottom_left_y - self._height *Flask.PART_HEIGHT <= mouse_y <= self._bottom_left_y)

import pygame
import math
import Utils


class Button:
    def __init__(self, width, height, top_left_x, top_left_y, color, text=None, text_color=None,
                 text_size=None, outline_color=None, outline_width=None):
        self._top_left_x = top_left_x
        self._top_left_y = top_left_y
        self._width = width
        self._height = height
        self._color = color
        self._outline_width = outline_width
        self._outline_color = outline_color
        self._rendered_text = None
        self._text_rect = None
        if text:
            self._text_color = text_color
            self._font = pygame.font.Font(None, text_size)
            self.set_text(text)
        self._on_click = []

    def draw(self, screen):
        pygame.draw.rect(screen, self._color, pygame.Rect(self._top_left_x, self._top_left_y,
                                                          self._width, self._height))
        if self._rendered_text:
            screen.blit(self._rendered_text, self._text_rect)
        if self._outline_color:
            pygame.draw.rect(screen, self._outline_color, pygame.Rect(self._top_left_x, self._top_left_y,
                                                                      self._width, self._height), self._outline_width)

    def check_click(self, mouse_x, mouse_y):
        if self._top_left_x <= mouse_x <= self._top_left_x + self._width and \
                self._top_left_y <= mouse_y <= self._top_left_y + self._height:
            for for_call in self._on_click:
                for_call[0](*for_call[1], **for_call[2])
            return True
        return False

    def update(self):
        pass

    def add_on_click(self, func, *args, **kwargs):
        self._on_click.append((func, args, kwargs))

    def set_text(self, text):
        self._rendered_text = self._font.render(text, True, self._text_color)
        center_x = self._top_left_x + self._width // 2
        center_y = self._top_left_y + self._height // 2
        self._text_rect = self._rendered_text.get_rect(center=(center_x, center_y))


class ColorWheel:

    EDGE_POINTS = 100
    CENTER_RATIO = Utils.WHEEL_OF_COLORS_CENTER_RATIO
    OUTLINES_WIDTH = Utils.WHEEL_OF_COLORS_OUTLINE_WIDTH
    HIGHLIGHT_TIME = Utils.COLOR_DISPLAY_FRAMES

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
            return False

        angle_step = 2 * math.pi / self._color_count
        click_angle = math.atan2(self._center_y - mouse_y, mouse_x - self._center_x)
        if click_angle < 0:
            click_angle += 2 * math.pi

        distance_from_center = math.hypot(mouse_x - self._center_x, mouse_y - self._center_y)

        if distance_from_center > self._radius:
            return False

        sector_id = int(click_angle // angle_step)
        self._highlighted[sector_id] = Utils.CLICK_HIGHLIGHT_FRAMES
        return sector_id

    def update(self):
        pass

    def highlight_sector(self, sector_id):
        self._highlighted[sector_id] = ColorWheel.HIGHLIGHT_TIME

    def stop_all_highlights(self):
        self._highlighted.clear()


class Flask:

    PART_WIDTH = Utils.FLASK_PART_WIDTH
    PART_HEIGHT = Utils.FLASK_PART_HEIGHT
    BOTTOM_CORNERS_RADIUS = Utils.FLASK_BOTTOM_CORNERS_RADIUS
    BONUS_HEIGHT_WHEN_SELECTED = Utils.FLASK_BONUS_HEIGHT_WHEN_SELECTED

    def __init__(self, height, bottom_left_x, bottom_left_y):
        self._bottom_left_x = bottom_left_x
        self._bottom_left_y = bottom_left_y
        self._height = height
        self.content = []

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

    def check_click(self, mouse_x, mouse_y):
        return self._bottom_left_x <= mouse_x <= self._bottom_left_x + Flask.PART_WIDTH and (
            self._bottom_left_y - self._height *Flask.PART_HEIGHT <= mouse_y <= self._bottom_left_y)

    def update(self):
        pass

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


class LoopPiece:
    SIDE_WIDTH = Utils.LOOP_PIECE_PART_WIDTH
    SIDE_HEIGHT = Utils.LOOP_PIECE_PART_HEIGHT
    CIRCLE_RADIUS_TO_WIDTH_PROPORTION = Utils.CIRCLE_RADIUS_TO_WIDTH_PROPORTION

    def __init__(self, connections, top_left_x, top_left_y):
        self._connections = connections
        self._top_left_x = top_left_x
        self._top_left_y = top_left_y

    def draw(self, screen):
        if self.up:
            rect = pygame.Rect(self._top_left_x, self._top_left_y - LoopPiece.SIDE_HEIGHT + LoopPiece.SIDE_WIDTH,
                               LoopPiece.SIDE_WIDTH, LoopPiece.SIDE_HEIGHT)
            pygame.draw.rect(screen, pygame.Color('black'), rect)
        if self.right:
            rect = pygame.Rect(self._top_left_x, self._top_left_y,
                               LoopPiece.SIDE_HEIGHT, LoopPiece.SIDE_WIDTH)
            pygame.draw.rect(screen, pygame.Color('black'), rect)
        if self.down:
            rect = pygame.Rect(self._top_left_x, self._top_left_y,
                               LoopPiece.SIDE_WIDTH, LoopPiece.SIDE_HEIGHT)
            pygame.draw.rect(screen, pygame.Color('black'), rect)
        if self.left:
            rect = pygame.Rect(self._top_left_x - LoopPiece.SIDE_HEIGHT + LoopPiece.SIDE_WIDTH, self._top_left_y,
                               LoopPiece.SIDE_HEIGHT, LoopPiece.SIDE_WIDTH)
            pygame.draw.rect(screen, pygame.Color('black'), rect)
        if sum(self._connections) == 1:
            pygame.draw.circle(screen, pygame.Color('black'), (self._top_left_x + LoopPiece.SIDE_WIDTH // 2,
                                self._top_left_y + LoopPiece.SIDE_WIDTH // 2),
                                LoopPiece.CIRCLE_RADIUS_TO_WIDTH_PROPORTION * LoopPiece.SIDE_WIDTH)

    def check_click(self, mouse_x, mouse_y):
        if self._top_left_x - LoopPiece.SIDE_HEIGHT + LoopPiece.SIDE_WIDTH <= mouse_x < (
                self._top_left_x + LoopPiece.SIDE_HEIGHT) and (self._top_left_y - LoopPiece.SIDE_HEIGHT
                + LoopPiece.SIDE_WIDTH) <= mouse_y < self._top_left_y + LoopPiece.SIDE_HEIGHT:
            self.rotate()
            return True
        return False

    def update(self):
        pass

    def rotate(self, times=1):
        if times % 4 == 1:
            self._connections[0], self._connections[1], self._connections[2], self._connections[3] = (
                self.left, self.up, self.right, self.down)
        elif times % 4 == 2:
            self._connections[0], self._connections[2] = self.down, self.up
            self._connections[1], self._connections[3] = self.left, self.right
        elif times % 4 == 3:
            self._connections[0], self._connections[1], self._connections[2], self._connections[3] = (
                self.right, self.down, self.left, self.up)

    @property
    def state(self):
        return (self.up << 3) | (self.right << 2) | (self.down << 1) | self.left

    @property
    def up(self):
        return self._connections[0]

    @property
    def right(self):
        return self._connections[1]

    @property
    def down(self):
        return self._connections[2]

    @property
    def left(self):
        return self._connections[3]


class PointConnect:

    def __init__(self, center_x, center_y, radius, color, click_box_size, board_x, board_y):
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


class LineConnect:

    def __init__(self, center_x, center_y, color, side_size, board_x, board_y):
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

    def update(self):
        pass

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
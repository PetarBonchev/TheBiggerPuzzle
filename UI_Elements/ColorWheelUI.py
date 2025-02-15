import math
import pygame
from Utilities import GlobalVariables
from UI_Elements.GameObject import GameObject


class ColorWheel(GameObject):
    EDGE_POINTS = 100
    OUTLINES_WIDTH = 5

    def __init__(self, color_count, center_x, center_y, radius, name='color_wheel'):
        super().__init__(name)
        self._color_count = color_count
        self._center_x = center_x
        self._center_y = center_y
        self._radius = radius
        self._display_pattern = []
        self._display_color = None
        self._to_highlight = -1
        self._timer = 0

    def reset(self, color_count):
        self._color_count = color_count
        self.stop_all_highlights()

    def is_displaying(self):
        return bool(self._display_pattern) or self._timer

    def set_display_pattern(self, sectors, display_color):
        self.stop_all_highlights()
        self._display_pattern = sectors[1:]
        self._display_color = display_color
        self._to_highlight = sectors[0]
        self._timer = GlobalVariables.HIGHLIGHT_FRAME_DURATION

    def stop_all_highlights(self):
        self._to_highlight = -1
        self._timer = 0
        self._display_pattern = []

    def clicked_sector(self, mouse_x, mouse_y):
        if (math.hypot(mouse_x - self._center_x, mouse_y - self._center_y) <
                self._radius * GlobalVariables.WOC_CENTER_RADIUS_RATIO):
            return -1

        angle_step = 2 * math.pi / self._color_count
        click_angle = math.atan2(self._center_y - mouse_y, mouse_x - self._center_x)
        if click_angle < 0:
            click_angle += 2 * math.pi

        distance_from_center = math.hypot(mouse_x - self._center_x, mouse_y - self._center_y)

        if distance_from_center > self._radius:
            return -1

        return int(click_angle // angle_step)

    def _draw(self, screen):
        angle_step = 2 * math.pi / self._color_count
        for i in range(self._color_count):
            start_angle = i * angle_step
            end_angle = (i + 1) * angle_step
            color = GlobalVariables.COLORS[i % len(GlobalVariables.COLORS)]
            if i == self._to_highlight:
                color = self._display_color

            points = [(self._center_x, self._center_y)]
            for j in range(ColorWheel.EDGE_POINTS + 1):
                angle = start_angle + j * (end_angle - start_angle) / ColorWheel.EDGE_POINTS
                x = self._center_x + self._radius * math.cos(angle)
                y = self._center_y - self._radius * math.sin(angle)
                points.append((x, y))

            pygame.draw.polygon(screen, color, points)

        pygame.draw.circle(screen, pygame.Color('Black'), (self._center_x, self._center_y),
                           self._radius * GlobalVariables.WOC_CENTER_RADIUS_RATIO, 0)

        for i in range(self._color_count):
            start_angle = i * angle_step
            pygame.draw.line(screen, pygame.Color('Black'), (self._center_x, self._center_y),
                             (self._center_x + self._radius * math.cos(start_angle),
                              self._center_y - self._radius * math.sin(start_angle)), ColorWheel.OUTLINES_WIDTH)

        pygame.draw.circle(screen, pygame.Color('Black'), (self._center_x, self._center_y),
                           self._radius + ColorWheel.OUTLINES_WIDTH, ColorWheel.OUTLINES_WIDTH)

    def _update(self):
        if self._timer > 0:
            self._timer -= 1
        else:
            if self._display_pattern:
               if self._to_highlight == -1:
                   self._to_highlight = self._display_pattern.pop(0)
                   self._timer = GlobalVariables.HIGHLIGHT_FRAME_DURATION
               else:
                   self._to_highlight = -1
                   self._timer = GlobalVariables.FRAMES_BETWEEN_HIGHLIGHTS
            elif self._to_highlight != -1:
                self._to_highlight = -1
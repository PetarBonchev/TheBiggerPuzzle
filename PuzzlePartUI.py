from Button import Button
from Text import Text
import math
import pygame


class PuzzlePart(Button):
    POINTS_IN_CURVE = 20

    def __init__(self, top_left_x, top_left_y, sides, size=300, background_color=pygame.Color('orange'),
                 text=None, score_text=None, text_color=pygame.Color('black'), font_size=25, name='puzzle_part'):
        super().__init__(size, size, top_left_x, top_left_y, name=name, text=text, text_color=text_color,
                         font_size=font_size)
        self._top_left_x = top_left_x
        self._top_left_y = top_left_y
        self._sides = sides
        self._points = PuzzlePart.get_shape_points((self._top_left_x, self._top_left_y), size, 2 * size / 7,
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
        return PuzzlePart._is_point_inside_polygon(pygame.mouse.get_pos(), self._points)

    @staticmethod
    def _bezier_curve(p0, p1, p2, p3, t):
        x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
        return x, y

    @staticmethod
    def _head_curve(size, side, curve_points):
        start = (side / 2 - size / 2, 0)
        mid1 = (start[0] + size / 2, start[1] - size / 5)
        mid2 = (start[0] - size / 2, start[1] - 4 * size / 5)
        end = (start[0] + size / 2, start[1] - size)
        mirror_mid2 = (start[0] + 3 * size / 2, start[1] - 4 * size / 5)
        mirror_mid1 = mid1
        mirror_end = (start[0] + size, start[1])

        points = [start]
        for t in range(curve_points):
            points.append(PuzzlePart._bezier_curve(start, mid1, mid2, end, t / curve_points))
        points.append(end)
        for t in range(curve_points):
            points.append(PuzzlePart._bezier_curve(end, mirror_mid2, mirror_mid1, mirror_end, t / curve_points))
        points.append(mirror_end)

        return points

    @staticmethod
    def _rotate_points(points, angle, origin=(0, 0)):
        rotated_points = []
        for x, y in points:
            rotated_x = math.cos(angle) * (x - origin[0]) - math.sin(angle) * (y - origin[1]) + origin[0]
            rotated_y = math.sin(angle) * (x - origin[0]) + math.cos(angle) * (y - origin[1]) + origin[1]
            rotated_points.append((rotated_x, rotated_y))
        return rotated_points

    @staticmethod
    def _mirror_points(points, axis='x', origin=(0, 0)):
        mirrored_points = []
        for x, y in points:
            if axis == 'x':
                mirrored_points.append((x, 2 * origin[1] - y))
            elif axis == 'y':
                mirrored_points.append((2 * origin[0] - x, y))
        return mirrored_points

    @staticmethod
    def _edge_points(top_left, size, side_length, side, outwards=True):
        points = PuzzlePart._head_curve(size, side_length, PuzzlePart.POINTS_IN_CURVE)

        if not outwards:
            points = PuzzlePart._mirror_points(points, 'x', (side_length / 2, 0))

        match side:
            case 0:
                points = [(x + top_left[0], y + top_left[1]) for x, y in points]
            case 1:
                points = PuzzlePart._rotate_points(points, math.radians(90))
                points = [(x + top_left[0] + side_length, y + top_left[1]) for x, y in points]
            case 2:
                points = PuzzlePart._rotate_points(points, math.radians(180), (0, 0))
                points = [(x + top_left[0] + side_length, y + top_left[1] + side_length) for x, y in points]
            case 3:
                points = PuzzlePart._rotate_points(points, math.radians(-90), (0, 0))
                points = [(x + top_left[0], y + top_left[1] + side_length) for x, y in points]

        return points

    @staticmethod
    def _rounded_corner(center, radius, start_angle, end_angle, num_points=15):
        points = []
        for t in range(num_points + 1):
            angle = start_angle + t * (end_angle - start_angle) / num_points
            points.append((center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle)))
        return points

    @staticmethod
    def get_shape_points(top_left, size, head_size, sides, corner_radius=20):
        points = []
        corner_points = set()
        offsets = [(0, 0), (size, 0), (size, size), (0, size)]
        corner_positions = [(top_left[0] + corner_radius, top_left[1] + corner_radius),
            (top_left[0] + size - corner_radius, top_left[1] + corner_radius),
            (top_left[0] + size - corner_radius, top_left[1] + size - corner_radius),
            (top_left[0] + corner_radius, top_left[1] + size - corner_radius)]
        angles = [(180, 270), (270, 360), (0, 90), (90, 180)]

        for i in range(4):
            next_corner = (top_left[0] + offsets[i][0], top_left[1] + offsets[i][1])
            if sides[i - 1] == 0 and sides[i] == 0:
                points.extend(PuzzlePart._rounded_corner(corner_positions[i], corner_radius,
                    math.radians(angles[i][0]), math.radians(angles[i][1])))
                corner_points.add(next_corner)
            else:
                points.append(next_corner)
            if sides[i]:
                points.extend(PuzzlePart._edge_points(top_left, head_size, size, i, sides[i] == 1))

        return [point for point in points if point not in corner_points]

    @staticmethod
    def _is_point_inside_polygon(point, points_of_polygon):
        x, y = point
        n = len(points_of_polygon)
        inside = False
        j = n - 1

        for i in range(n):
            xi, yi = points_of_polygon[i]
            xj, yj = points_of_polygon[j]

            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i

        return inside
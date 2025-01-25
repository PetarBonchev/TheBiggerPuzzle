import random


class ColorTableGenerator:

    MIN_TRAIL_LENGTH = 2
    MAX_OPERATIONS = 100

    def __init__(self, width, height, color_count):
        self._colors = color_count
        self._height = height
        self._width = width
        self._not_visited = None
        self._max_trail_length = (width * height * 2) // color_count

    def generate(self):
        self._not_visited = set([(x, y) for x in range(self._height) for y in range(self._width)])
        trails = []

        while self._not_visited:
            new_trail = self._create_trail()
            trails.append(new_trail)

        operations_count = 0
        correct_trails = False
        while not correct_trails:
            correct_trails = True

            if operations_count > ColorTableGenerator.MAX_OPERATIONS:
                trails = self.generate()
                break
            operations_count += 1

            for i, trail in enumerate(trails):
                if len(trail) < self.MIN_TRAIL_LENGTH:
                    correct_trails = False
                    ColorTableGenerator._merge_one_length_trail(trails, i)
                    break
            else:
                if len(trails) > self._colors:
                    correct_trails = False
                    to_merge = min(trails, key=len)
                    ColorTableGenerator._merge_multi_length_trail(trails, to_merge)
                elif len(trails) < self._colors:
                    correct_trails = False
                    ColorTableGenerator._split_longest_trail(trails)

        coordinate_count = 0
        for trail in trails:
            coordinate_count += len(trail)
        if coordinate_count != self._width * self._height:
            trails = self.generate()
        return trails


    def _create_trail(self):
        x, y = random.choice(list(self._not_visited))
        self._not_visited.remove((x, y))

        trail = [(x, y)]
        desired_length = random.randint(self.MIN_TRAIL_LENGTH, self._max_trail_length)

        for _ in range(desired_length):
            neighbors = self._get_neighbors(x, y)
            if not neighbors:
                break

            x, y = random.choice(neighbors)
            trail.append((x, y))
            self._not_visited.remove((x, y))

        return trail

    def _get_neighbors(self, x, y):
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        return [(a, b) for (a, b) in neighbors if (a, b) in self._not_visited]

    @staticmethod
    def _merge_one_length_trail(trails, trail_id):
        x, y = trails.pop(trail_id)[0]

        for trail in trails:
            if ColorTableGenerator._are_neighbours(x, y, *trail[0]):
                trail.insert(0, (x, y))
                return
            if ColorTableGenerator._are_neighbours(x, y, *trail[-1]):
                trail.append((x, y))
                return

        for trail in trails:
            if len(trail) <= ColorTableGenerator.MIN_TRAIL_LENGTH + 1:
                continue

            for i in range(len(trail)):
                if ColorTableGenerator._are_neighbours(x, y, *trail[i]):
                    trail_1 = trail[:i]
                    trail_2 = trail[i:]
                    if len(trail_1) >= ColorTableGenerator.MIN_TRAIL_LENGTH and len(
                            trail_2) >= ColorTableGenerator.MIN_TRAIL_LENGTH:
                        if ColorTableGenerator._are_neighbours(x, y, *trail_1[-1]):
                            trail_1.append((x, y))
                        else:
                            trail_2.insert(0, (x, y))

                        trails.remove(trail)
                        trails.append(trail_1)
                        trails.append(trail_2)
                        return

        #може да стигне дотук, накрая ще бъде проверено дали дължината на всички пътища е _width * _height

    @staticmethod
    def _merge_multi_length_trail(trails, to_merge):
        trails.remove(to_merge)

        for trail in trails:
            if ColorTableGenerator._are_neighbours(*to_merge[-1], *trail[0]):
                to_merge.extend(trail)
                trails.remove(trail)
                trails.append(to_merge)
                return
            if ColorTableGenerator._are_neighbours(*to_merge[0], *trail[0]):
                to_merge = to_merge[::-1]
                to_merge.extend(trail)
                trails.remove(trail)
                trails.append(to_merge)
                return
            if ColorTableGenerator._are_neighbours(*to_merge[-1], *trail[-1]):
                to_merge =  to_merge[::-1]
                trail.extend(to_merge)
                return
            if ColorTableGenerator._are_neighbours(*to_merge[0], *trail[-1]):
                trail.extend(to_merge)
                return

        for trail in trails:
            for i in range(len(trail)):
                if ColorTableGenerator._are_neighbours(*to_merge[0], *trail[i]):
                    trail_1 = trail[:i + 1]
                    trail_2 = trail[i + 1:]
                    if len(trail_1) + len(to_merge) >= ColorTableGenerator.MIN_TRAIL_LENGTH and len(
                            trail_2) >= ColorTableGenerator.MIN_TRAIL_LENGTH:
                        trail_1.extend(to_merge)
                        trails.remove(trail)
                        trails.append(trail_1)
                        trails.append(trail_2)
                        return
                elif ColorTableGenerator._are_neighbours(*to_merge[-1], *trail[i]):
                    trail_1 = trail[:i + 1]
                    trail_2 = trail[i + 1:]
                    if len(trail_1) + len(to_merge) >= ColorTableGenerator.MIN_TRAIL_LENGTH and len(
                            trail_2) >= ColorTableGenerator.MIN_TRAIL_LENGTH:
                        to_merge = to_merge[::-1]
                        trail_1.extend(to_merge)
                        trails.remove(trail)
                        trails.append(trail_1)
                        trails.append(trail_2)
                        return

        # може да стигне дотук, накрая ще бъде проверено дали дължината на всички пътища е _width * _height

    @staticmethod
    def _split_longest_trail(trails):
        to_split = max(trails, key=len)
        split_point = random.randint(ColorTableGenerator.MIN_TRAIL_LENGTH, len(to_split) - ColorTableGenerator.MIN_TRAIL_LENGTH)
        trail_1 = to_split[:split_point]
        trail_2 = to_split[split_point:]
        trails.remove(to_split)
        trails.append(trail_1)
        trails.append(trail_2)

        #ако не са правилен размер (len(to_split) < 4), ще се merg-нат при другите случаи

    @staticmethod
    def _are_neighbours(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2) == 1
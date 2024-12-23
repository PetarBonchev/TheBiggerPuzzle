import random

class Flask:

    def __init__(self):
        self._content = []

    def __repr__(self):
        return str(self._content[::-1])

    @property
    def top_color(self):
        if self._content:
            return self._content[-1]
        return -1

    @property
    def top_count(self):
        if len(self._content) == 0:
            return 0
        i = len(self._content) - 1
        while i >= 0 and self._content[i] == self._content[-1]:
            i -= 1
        return len(self._content) - i - 1

    @property
    def water_height(self):
        return len(self._content)

    @property
    def complete(self):
        return len(self._content) == self.top_count

    def move_top(self):
        count_ = self.top_count
        top_elements = self._content[-count_:]
        self._content = self._content[:-count_]
        return top_elements

    def receive_top(self, color_stream):
        self._content.extend(color_stream)


class WaterSort:

    EMPTY_FLASKS = 2

    def __init__(self, height, flask_count):
        self.flask_count = flask_count
        self.height = height
        self.flasks = []
        for _ in range(flask_count):
            self.flasks.append(Flask())

    def complete(self):
        return all(flask.complete for flask in self.flasks)

    def move_liquid(self, from_id, to_id):
        if from_id < 0 or self.flask_count <= from_id or to_id < 0 or self.flask_count <= to_id:
            raise ValueError("Wrong flask number")
        if from_id == to_id or self.flasks[from_id].top_color == -1 or (self.flasks[to_id].top_color != -1 and self.flasks[from_id].top_color != self.flasks[to_id].top_color):
            return -1

        from_top = self.flasks[from_id].move_top()
        max_space = min(self.height - self.flasks[to_id].water_height, len(from_top))
        self.flasks[to_id].receive_top(from_top[:max_space])
        self.flasks[from_id].receive_top(from_top[max_space:])

    def random_fill(self):
        water_mix = [i for i in range(self.flask_count - WaterSort.EMPTY_FLASKS) for _ in range(self.height)]
        random.shuffle(water_mix)
        for i in range(self.flask_count - WaterSort.EMPTY_FLASKS):
            self.flasks[i].receive_top(water_mix[i * self.height: (i + 1) * self.height])

    def solvable(self):
        pass
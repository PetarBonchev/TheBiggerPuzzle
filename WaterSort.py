class Flask:

    def __init__(self):
        self._content = []

    def __repr__(self):
        return str(self._content[::-1])

    @property
    def top_color(self):
        if self._content:
            return self._content[-1]
        return None

    @property
    def top_count(self):
        if len(self._content) == 0:
            return 0
        i = len(self._content) - 1
        while i >= 0 and self._content[i] == self._content[-1]:
            i -= 1
        return len(self._content) - i - 1

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
        self.flasks = [Flask()] * flask_count

    def complete(self):
        return all(flask.complete for flask in self.flasks)

    def move_liquid(self, from_id, to_id):
        pass

    def random_fill(self):
        pass

    def solvable(self):
        pass

w = WaterSort(4, 6)
print(w.complete())
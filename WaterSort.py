import copy
import random
import WaterSortSolver
from UIManager import Flask
import Utils

class WaterSort:

    EMPTY_FLASKS = Utils.WATER_SORT_EMPTY_FLASKS
    SPACE_BETWEEN_FLASKS = Utils.WATER_SORT_SPACE_BETWEEN_FLASKS

    def __init__(self, height, flask_count):
        self._flask_count = flask_count
        self._height = height
        self._flasks = []
        self._initialize_flasks()
        self._game_state = 0
        self._selected_flask_id = -1
        self._actions = []

        self.new_game()

    def draw(self, screen):
        for flask in self._flasks:
            flask.draw(screen)

    def check_click(self, mouse_x, mouse_y):
        if self._game_state != 2:
            return
        pressed_flask = False
        for i, flask in enumerate(self._flasks):
            if flask.check_click(mouse_x, mouse_y):
                pressed_flask = True
                if self._selected_flask_id == -1:
                    self._selected_flask_id = i
                    flask.select()
                else:
                    moved = self._move_liquid(self._selected_flask_id, i)
                    self._flasks[self._selected_flask_id].deselect()
                    if moved:
                        self._selected_flask_id = -1
                    else:
                        self._selected_flask_id = i
                        self._flasks[i].select()
                    if self._complete():
                        self._game_state = 3
        if not pressed_flask and self._selected_flask_id != -1:
            self._flasks[self._selected_flask_id].deselect()
            self._selected_flask_id = -1

    def update(self):
        if self._game_state == 1:
            self._random_fill()
            solver = WaterSortSolver.WaterSortSolver([flask.content for flask in self._flasks], self._height)
            if solver.solve():
                self._game_state = 2
                self._actions.append(tuple(copy.deepcopy(flask.content) for flask in self._flasks))
        elif self._game_state == 2:
            pass
        elif self._game_state == 3:
            self.new_game()

    def new_game(self):
        self._game_state = 1
        self._actions.clear()

    def undo(self):
        if len(self._actions) > 1:
            state = self._actions[-2]
            self._actions.pop(-1)
            for i, content in enumerate(state):
                self._flasks[i].content = copy.deepcopy(content)

    def _complete(self):
        return all(flask.complete for flask in self._flasks)

    def _move_liquid(self, from_id, to_id):
        if from_id == to_id:
            return True
        if (self._flasks[from_id].top_color == -1 or (self._flasks[to_id].top_color != -1
            and self._flasks[from_id].top_color != self._flasks[to_id].top_color)
                or len(self._flasks[to_id].content) == self._height):
            return False

        from_top = self._flasks[from_id].move_top()
        max_space = min(self._height - self._flasks[to_id].water_height, len(from_top))
        self._flasks[to_id].receive_top(from_top[:max_space])
        self._flasks[from_id].receive_top(from_top[max_space:])
        self._actions.append(tuple(copy.deepcopy(flask.content) for flask in self._flasks))
        return True

    def _random_fill(self):
        self._flasks.clear()
        self._initialize_flasks()
        water_mix = [i for i in range(self._flask_count - WaterSort.EMPTY_FLASKS) for _ in range(self._height)]
        random.shuffle(water_mix)
        for i in range(self._flask_count - WaterSort.EMPTY_FLASKS):
            self._flasks[i].receive_top(water_mix[i * self._height: (i + 1) * self._height])

    def _initialize_flasks(self):
        total_flasks_width = Flask.PART_WIDTH * self._flask_count + (self._flask_count - 1) * WaterSort.SPACE_BETWEEN_FLASKS
        starting_x = (Utils.screen_width - total_flasks_width) // 2
        bottom_y = (Utils.screen_height + self._height * Flask.PART_HEIGHT) // 2

        for i in range(self._flask_count):
            bottom_left_x = starting_x + i * Flask.PART_WIDTH + i * WaterSort.SPACE_BETWEEN_FLASKS
            self._flasks.append(Flask(self._height, bottom_left_x, bottom_y))
import copy
import random
import pygame
from Utilities import WaterSortSolver, GlobalVariables
from UI_Elements.FlaskUI import Flask
from UI_Elements.GameObject import GameObject
from Utilities.AnchorCalculator import Anchor
from UI_Elements.Button import Button
from UI_Elements.LevelSystem import LevelSystem
from UI_Elements.Text import Text


class WaterSort(GameObject):

    SPACE_BETWEEN_FLASKS = 35

    def __init__(self, height, flask_count, game_data=None, name='water_sort'):
        super().__init__(name)
        self._flask_count = flask_count
        self._height = height
        self._flasks = []
        self._game_data = game_data
        self._set_game = False
        self._level_id = -1
        self._initialize_flasks()
        self._game_state = 'new_game'
        self._selected_flask_id = -1
        self._actions = []
        restart_button = Button(100, 50, *Anchor.top_left(70, 10), pygame.Color('orange'),
                                text="Restart", name='restart_button')
        restart_button.add_on_click(self.reset)
        undo_button = Button(80, 50, *Anchor.top_left(180, 10), pygame.Color('orange'),
                                text="Undo", name='undo_button')
        undo_button.add_on_click(self.undo)
        message_text = Text(*Anchor.top_middle(0, 40, 0), '', pygame.Color('black'), 50, 'score_text')

        self.add_child(message_text)
        self.add_child(restart_button)
        self.add_child(undo_button)

    def new_game(self, game_data=None):
        self._game_data = game_data
        self._game_state = 'playing'
        self._actions.clear()
        self._flasks.clear()
        self.children = [self.get_object_by_name('restart_button'),
                         self.get_object_by_name('score_text'),
                         self.get_object_by_name('undo_button')]
        self.get_object_by_name('score_text').set_text('')
        self._random_fill()
        self._record_action()
        if not self._set_game and (not self._find_solution() or self._is_game_complete()):
            self.reset()

    def reset(self, height=-1, flask_count=-1, game_data=None, level_number=-1):
        self._level_id = level_number
        if not self._set_game:
            self._height = random.randint(3, 6)
            self._flask_count = random.randint(4, 10)
            self.get_object_by_name('restart_button').set_text('New game')
            self.new_game()
        else:
            self.get_object_by_name('restart_button').set_text('Restart')
            if height != -1 and flask_count != -1:
                self._height = height
                self._flask_count = flask_count
            if game_data:
                self.new_game(game_data)
            else:
                self.new_game(self._game_data)

    def undo(self):
        if len(self._actions) > 1:
            state = self._actions[-2]
            self._actions.pop(-1)
            for i, content in enumerate(state):
                self._flasks[i].content = copy.deepcopy(content)

    def change_game_mode(self, is_set_game):
        self._set_game = is_set_game

    def _check_click(self, mouse_x, mouse_y):
        pressed_flask = False
        for i, flask in enumerate(self._flasks):
            if flask.is_clicked(mouse_x, mouse_y):
                pressed_flask = True
                self._click_flask(i)
                break

        if not pressed_flask and self._selected_flask_id != -1:
            self._deselect_flask()

    def _update(self):
        if self._game_state == 'new_game':
            self.reset()
        elif self._game_state == 'complete':
            if self._set_game:
                self.get_object_by_name('score_text').set_text('You win!')
                LevelSystem.instance.complete_level(GlobalVariables.WATER_SORT_GAME_ID, self._level_id)
            else:
                self.reset()

    def _click_flask(self, flask_id):
        if self._selected_flask_id == -1:
            self._select_flask(flask_id)
        else:
            if self._move_liquid(self._selected_flask_id, flask_id):
                self._deselect_flask()
                if self._is_game_complete():
                    self._game_state = 'complete'
            else:
                self._select_flask(flask_id)

    def _select_flask(self, flask_id):
        if self._selected_flask_id != -1:
            self._flasks[self._selected_flask_id].deselect()
        self._selected_flask_id = flask_id
        self._flasks[flask_id].select()

    def _deselect_flask(self):
        self._flasks[self._selected_flask_id].deselect()
        self._selected_flask_id = -1

    def _is_game_complete(self):
        return all(flask.complete for flask in self._flasks)

    def _move_liquid(self, from_id, to_id):
        if from_id == to_id:
            return True

        from_flask = self._flasks[from_id]
        to_flask = self._flasks[to_id]

        if (from_flask.top_color == -1 or
            (to_flask.top_color != -1 and from_flask.top_color != to_flask.top_color) or
                len(to_flask.content) == self._height):
            return False

        from_top = from_flask.move_top()
        max_space = min(self._height - to_flask.water_height, len(from_top))
        to_flask.receive_top(from_top[:max_space])
        from_flask.receive_top(from_top[max_space:])
        self._record_action()
        return True

    def _record_action(self):
        self._actions.append(tuple(copy.deepcopy(flask.content) for flask in self._flasks))

    def _random_fill(self):
        self._initialize_flasks()
        if self._game_data:
            water_mix = self._game_data
        else:
            water_mix = [
                i for i in range(self._flask_count - GlobalVariables.WS_EMPTY_FLASKS)
                for _ in range(self._height)
            ]
            random.shuffle(water_mix)

        for i in range(self._flask_count - GlobalVariables.WS_EMPTY_FLASKS):
            self._flasks[i].receive_top(water_mix[i * self._height: (i + 1) * self._height])

    def _initialize_flasks(self):
        total_flasks_width = (GlobalVariables.WS_FLASK_WIDTH * self._flask_count +
                              (self._flask_count - 1) * WaterSort.SPACE_BETWEEN_FLASKS)
        starting_x = (GlobalVariables.screen_width - total_flasks_width) // 2
        bottom_y = (GlobalVariables.screen_height + self._height * GlobalVariables.WS_FLASK_HEIGHT) // 2

        for i in range(self._flask_count):
            bottom_left_x = (starting_x + i * GlobalVariables.WS_FLASK_WIDTH +
                             i * WaterSort.SPACE_BETWEEN_FLASKS)
            flask = Flask(self._height, bottom_left_x, bottom_y)
            self._flasks.append(flask)
            self.add_child(flask)

    def _find_solution(self):
        if self._game_data:
            return True
        return WaterSortSolver.WaterSortSolver([flask.content for flask in self._flasks], self._height).solve()


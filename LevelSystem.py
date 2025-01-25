import pygame
import GlobalVariables
from AnchorCalculator import Anchor
from GameObject import GameObject
from Button import Button


class LevelSystem(GameObject):

    def __init__(self, window_system, name='level_system'):
        super().__init__(name)

        self._window_system = window_system

    def load(self, game_id):
        with open(GlobalVariables.GAME_DATA_FILES[game_id], 'r') as file:
            data = file.readlines()
            game_data = [line.strip() for line in data]
            self._window_system.get_object_by_name('endless_button').clear_on_click()
            self.children = []
            match game_id:
                case 0:
                    self._load_wheel_of_colors_levels(game_data)
                case 1:
                    self._load_infinity_loop_levels(game_data)
                case 2:
                    self._load_water_sort_levels(game_data)
                case 3:
                    self._load_color_connect_levels(game_data)

    def _load_wheel_of_colors_levels(self, data):
        endless_button = self._window_system.get_object_by_name('endless_button')
        endless_button.add_on_click(self._window_system.go_to_window, 'wheel_of_colors_window')
        endless_button.add_on_click(self._window_system.get_object_by_name('wheel_of_colors').reset)

        for i in range(len(data) // 2):
            game_data = [int(element) for element in data[2 * i + 1].split()]
            on_click = [(self._window_system.get_object_by_name('wheel_of_colors').reset, [int(data[2 * i]), game_data]),
                        (self._window_system.go_to_window, ['wheel_of_colors_window'])]
            self._spawn_level(on_click, i + 1)

    def _load_infinity_loop_levels(self, data):
        endless_button = self._window_system.get_object_by_name('endless_button')
        endless_button.add_on_click(self._window_system.go_to_window, 'infinity_loop_window')
        endless_button.add_on_click(self._window_system.get_object_by_name('infinity_loop').change_game_mode, False)
        endless_button.add_on_click(self._window_system.get_object_by_name('infinity_loop').reset)

        i = 0
        level_number = 1
        while i < len(data):
            width, height = [int(element) for element in data[i].split()]
            game_data = []
            for _ in range(height):
                i += 1
                game_row = [int(element) for element in data[i].split()]
                game_data.append(game_row)
            on_click = [(self._window_system.get_object_by_name('infinity_loop').reset, [width, height, game_data]),
                        (self._window_system.get_object_by_name('infinity_loop').change_game_mode, [True]),
                        (self._window_system.go_to_window, ['infinity_loop_window'])]
            self._spawn_level(on_click, level_number)
            i += 1
            level_number += 1

    def _load_water_sort_levels(self, data):
        endless_button = self._window_system.get_object_by_name('endless_button')
        endless_button.add_on_click(self._window_system.get_object_by_name('water_sort').change_game_mode, False)
        endless_button.add_on_click(self._window_system.get_object_by_name('water_sort').reset)
        endless_button.add_on_click(self._window_system.go_to_window, 'water_sort_window')

        for i in range(len(data) // 2):
            height, flask_count = [int(element) for element in data[2 * i].split()]
            game_data = [int(element) for element in data[2 * i + 1].split()]
            on_click = [
                (self._window_system.get_object_by_name('water_sort').change_game_mode, [True]),
                (self._window_system.get_object_by_name('water_sort').reset, [height, flask_count, game_data]),
                (self._window_system.go_to_window, ['water_sort_window'])]
            self._spawn_level(on_click, i + 1)

    def _load_color_connect_levels(self, data):
        endless_button = self._window_system.get_object_by_name('endless_button')
        endless_button.add_on_click(self._window_system.get_object_by_name('color_connect').change_game_mode, False)
        endless_button.add_on_click(self._window_system.get_object_by_name('color_connect').reset)
        endless_button.add_on_click(self._window_system.go_to_window, 'color_connect_window')

        i = 0
        level_number = 1
        while i < len(data):
            width, height, color_count = [int(element) for element in data[i].split()]
            game_data = []
            for _ in range(color_count):
                i += 1
                game_row = [int(element) for element in data[i].split()]
                if len(game_row) % 2 == 1 or len(game_row) == 0:
                    break
                game_row = list(zip(game_row[::2], game_row[1::2]))
                game_data.append(game_row)
            on_click = [
                (self._window_system.get_object_by_name('color_connect').change_game_mode, [True]),
                (self._window_system.get_object_by_name('color_connect').reset, [width, height, color_count, game_data]),
                (self._window_system.go_to_window, ['color_connect_window'])]
            self._spawn_level(on_click, level_number)
            i += 1
            level_number += 1

    def _spawn_level(self, on_click, level_number):
        size = GlobalVariables.screen_height * GlobalVariables.LEVEL_BUTTON_TO_HEIGHT
        level = Button(size, size, *Anchor.center((level_number - 1) % GlobalVariables.LEVEL_BUTTONS_IN_ROW * (size + 10),
                                                 (level_number - 1) // GlobalVariables.LEVEL_BUTTONS_IN_ROW * (size + 10),
                                                 GlobalVariables.LEVEL_BUTTONS_IN_ROW * (size + 10),
                                                 GlobalVariables.TOTAL_LEVELS_EACH_GAME // GlobalVariables.LEVEL_BUTTONS_IN_ROW * (size + 10)),
                       pygame.Color('orange'), text = str(level_number), name='level_'+str(level_number))
        for function_call in on_click:
            level.add_on_click(function_call[0], *function_call[1])
        self.add_child(level)
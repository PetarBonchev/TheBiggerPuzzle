import pygame

from ColorConnect import ColorConnect
from InfinityLoop import InfinityLoop
from UIManager import Button
from WaterSort import WaterSort
from WheelOfColors import WheelOfColors


class LevelSelector:

    def __init__(self, window_manager_ref):
        self._window_manager = window_manager_ref
        self._buttons = []

    def draw(self, screen):
        for button in self._buttons:
            button.draw(screen)

    def check_click(self, mouse_x, mouse_y):
        for button in self._buttons:
            button.check_click(mouse_x, mouse_y)

    def update(self):
        for button in self._buttons:
            button.update()

    def load_levels(self, filename):
        self._buttons = []
        with open(filename, 'r') as file:
            data = file.readlines()
            game_data = [line.strip() for line in data]
            match game_data[0]:
                case 'wheel':
                    self._load_wheel_of_colors_levels(game_data[1:])
                case 'infinity':
                    self._load_infinity_loop_levels(game_data[1:])
                case 'water':
                    self._load_water_sort_levels(game_data[1:])
                case 'color':
                    self._load_color_connect_levels(game_data[1:])

    def _load_wheel_of_colors_levels(self, data):
        self._window_manager.remove_object_from_window(WheelOfColors, 2)

        def load_level(color_count, game_data):
            wheel = WheelOfColors(color_count, game_data)
            self._window_manager.add_object_in_window(wheel, 2)

        for i in range(len(data) // 2):
            game_data = [int(element) for element in data[2 * i + 1].split()]
            self._spawn_level(load_level, [int(data[2 * i]), game_data], 2)

    def _load_infinity_loop_levels(self, data):
        self._window_manager.remove_object_from_window(InfinityLoop, 4)

        def load_level(width, height, game_data):
            loop = InfinityLoop(width, height, game_data)
            self._window_manager.add_object_in_window(loop, 4)

        i = 0
        while i < len(data):
            width, height = [int(element) for element in data[i].split()]
            game_data = []
            for _ in range(height):
                i += 1
                game_row = [int(element) for element in data[i].split()]
                game_data.append(game_row)
            self._spawn_level(load_level, [width, height, game_data], 4)
            i += 1

    def _load_water_sort_levels(self, data):
        self._window_manager.remove_object_from_window(WaterSort, 3)

        def load_level(height, flask_count, game_data):
            water_sort = WaterSort(height, flask_count, game_data)
            self._window_manager.add_object_in_window(water_sort, 3)

        for i in range(len(data) // 2):
            height, flask_count = [int(element) for element in data[2 * i].split()]
            game_data = [int(element) for element in data[2 * i + 1].split()]
            self._spawn_level(load_level, [height, flask_count, game_data], 3)

    def _load_color_connect_levels(self, data):
        self._window_manager.remove_object_from_window(ColorConnect, 5)

        def load_level(width, height, color_count, game_data):
            connect = ColorConnect(width, height, color_count, game_data)
            self._window_manager.add_object_in_window(connect, 5)

        i = 0
        while i < len(data):
            width, height, color_count = [int(element) for element in data[i].split()]
            game_data = []
            while i + 1 < len(data):
                i += 1
                game_row = [int(element) for element in data[i].split()]
                if len(game_row) % 2 == 1 or len(game_row) == 0:
                    break
                game_row = list(zip(game_row[::2], game_row[1::2]))
                game_data.append(game_row)
            self._spawn_level(load_level, [width, height, color_count, game_data], 5)
            i += 1

    def _spawn_level(self, on_click, args, window_number):
        button = Button(50, 50, 300 + len(self._buttons) * 60, 300, pygame.Color('orange'))
        button.add_on_click(on_click, *args)
        button.add_on_click(self._window_manager.go_to_window, window_number)
        self._buttons.append(button)
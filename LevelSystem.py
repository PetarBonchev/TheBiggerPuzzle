import os
from cryptography.fernet import Fernet
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
            completed_levels = LevelSystem._get_completed_levels(LevelSystem._read_completed_levels_data())
            match game_id:
                case 0:
                    self._load_wheel_of_colors_levels(game_data, completed_levels[0])
                case 1:
                    self._load_infinity_loop_levels(game_data, completed_levels[1])
                case 2:
                    self._load_water_sort_levels(game_data, completed_levels[2])
                case 3:
                    self._load_color_connect_levels(game_data, completed_levels[3])

    def _load_wheel_of_colors_levels(self, data, completed_levels):
        endless_button = self._window_system.get_object_by_name('endless_button')
        endless_button.add_on_click(self._window_system.go_to_window, 'wheel_of_colors_window')
        endless_button.add_on_click(self._window_system.get_object_by_name('wheel_of_colors').reset)

        for i in range(len(data) // 2):
            game_data = [int(element) for element in data[2 * i + 1].split()]
            on_click = [(self._window_system.get_object_by_name('wheel_of_colors').reset, [int(data[2 * i]), game_data, i + 1]),
                        (self._window_system.go_to_window, ['wheel_of_colors_window'])]
            self._spawn_level(on_click, i + 1, i + 1 in completed_levels)

    def _load_infinity_loop_levels(self, data, completed_levels):
        endless_button = self._window_system.get_object_by_name('endless_button')
        endless_button.add_on_click(self._window_system.get_object_by_name('infinity_loop').change_game_mode, False)
        endless_button.add_on_click(self._window_system.go_to_window, 'infinity_loop_window')
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
            on_click = [(self._window_system.get_object_by_name('infinity_loop').change_game_mode, [True]),
                        (self._window_system.get_object_by_name('infinity_loop').reset, [width, height, game_data, level_number]),
                        (self._window_system.go_to_window, ['infinity_loop_window'])]
            self._spawn_level(on_click, level_number, level_number in completed_levels)
            i += 1
            level_number += 1

    def _load_water_sort_levels(self, data, completed_levels):
        endless_button = self._window_system.get_object_by_name('endless_button')
        endless_button.add_on_click(self._window_system.get_object_by_name('water_sort').change_game_mode, False)
        endless_button.add_on_click(self._window_system.get_object_by_name('water_sort').reset)
        endless_button.add_on_click(self._window_system.go_to_window, 'water_sort_window')

        for i in range(len(data) // 2):
            height, flask_count = [int(element) for element in data[2 * i].split()]
            game_data = [int(element) for element in data[2 * i + 1].split()]
            on_click = [
                (self._window_system.get_object_by_name('water_sort').change_game_mode, [True]),
                (self._window_system.get_object_by_name('water_sort').reset, [height, flask_count, game_data, i + 1]),
                (self._window_system.go_to_window, ['water_sort_window'])]
            self._spawn_level(on_click, i + 1, i + 1 in completed_levels)

    def _load_color_connect_levels(self, data, completed_levels):
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
                (self._window_system.get_object_by_name('color_connect').reset, [width, height, color_count, game_data, level_number]),
                (self._window_system.go_to_window, ['color_connect_window'])]
            self._spawn_level(on_click, level_number, level_number in completed_levels)
            i += 1
            level_number += 1

    def _spawn_level(self, on_click, level_number, is_complete):
        size = GlobalVariables.screen_height * GlobalVariables.LEVEL_BUTTON_TO_HEIGHT
        button_color = (0, 200, 0) if is_complete else pygame.Color('orange')
        level = Button(size, size, *Anchor.center((level_number - 1) % GlobalVariables.LEVEL_BUTTONS_IN_ROW * (size + 10),
                                                 (level_number - 1) // GlobalVariables.LEVEL_BUTTONS_IN_ROW * (size + 10),
                                                 GlobalVariables.LEVEL_BUTTONS_IN_ROW * (size + 10),
                                                 GlobalVariables.TOTAL_LEVELS_EACH_GAME // GlobalVariables.LEVEL_BUTTONS_IN_ROW * (size + 10)),
                       button_color, text = str(level_number), name='level_'+str(level_number))
        for function_call in on_click:
            level.add_on_click(function_call[0], *function_call[1])
        self.add_child(level)

    _KEY_FILE = 'encryption_key.key'
    _DATA_FILE = 'completed_levels.enc'

    @staticmethod
    def get_completed_levels():
        return LevelSystem._get_completed_levels(LevelSystem._read_completed_levels_data())

    @staticmethod
    def _get_cipher():
        if not os.path.exists(LevelSystem._KEY_FILE):
            key = Fernet.generate_key()
            with open(LevelSystem._KEY_FILE, 'wb') as key_file:
                key_file.write(key)
        else:
            with open(LevelSystem._KEY_FILE, 'rb') as key_file:
                key = key_file.read()

        return Fernet(key)

    @staticmethod
    def complete_level(game_id, level_number):
        file_data = LevelSystem._read_completed_levels_data()
        if LevelSystem._is_level_completed(game_id, level_number, file_data):
            return

        while len(file_data) <= game_id:
            file_data.append('')
        file_data[game_id] += ' ' + str(level_number)

        cipher = LevelSystem._get_cipher()
        encrypted_data = cipher.encrypt('\n'.join(file_data).encode())
        with open(LevelSystem._DATA_FILE, 'wb') as file:
            file.write(encrypted_data)

    @staticmethod
    def _read_completed_levels_data():
        if not os.path.exists(LevelSystem._DATA_FILE):
            return []

        cipher = LevelSystem._get_cipher()
        with open(LevelSystem._DATA_FILE, 'rb') as file:
            encrypted_data = file.read()
            decrypted_data = cipher.decrypt(encrypted_data).decode()
            file_data = [row.strip() for row in decrypted_data.split('\n')]
        return file_data

    @staticmethod
    def _is_level_completed(game_id, level_number, file_data):
        if len(file_data) < game_id + 1:
            return False
        for level in file_data[game_id].split():
            if int(level) == level_number:
                return True
        return False

    @staticmethod
    def _get_completed_levels(file_data):
        levels = []
        for row in file_data:
            completed = set()
            for element in row.split():
                completed.add(int(element))
            levels.append(completed)
        while len(levels) < 4:
            levels.append(set())
        return levels
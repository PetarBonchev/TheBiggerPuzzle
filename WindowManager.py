import pygame
import Utils
from ColorConnect import ColorConnect
from InfinityLoop import InfinityLoop
from LevelSelector import LevelSelector
from UIManager import Button
from WaterSort import WaterSort
from WheelOfColors import WheelOfColors


class Window:

    def __init__(self, background_color):
        self._background_color = background_color
        self._game_objects = []

    def add_game_object(self, game_object):
        self._game_objects.append(game_object)

    def update(self):
        for game_object in self._game_objects:
            game_object.update()

    def draw(self, screen):
        screen.fill(self._background_color)
        for game_object in self._game_objects:
            game_object.draw(screen)

    def check_click(self, mouse_x, mouse_y):
        for game_object in self._game_objects:
            game_object.check_click(mouse_x, mouse_y)

    def find_by_class_type(self, class_type):
        for obj in self._game_objects:
            if isinstance(obj, class_type):
                return obj

    def remove_game_object(self, class_type):
        self._game_objects = [obj for obj in self._game_objects if not isinstance(obj, class_type)]


class WindowDefiner:

    @staticmethod
    def fill_window_manager():
        WindowManager.instance.add_window(WindowDefiner.define_level_window())
        WindowManager.instance.add_window(WindowDefiner.define_main_window())
        WindowManager.instance.add_window(WindowDefiner.define_wheel_of_colors_window())
        WindowManager.instance.add_window(WindowDefiner.define_water_sort_window())
        WindowManager.instance.add_window(WindowDefiner.define_infinity_loop_window())
        WindowManager.instance.add_window(WindowDefiner.define_color_connect_window())

    @staticmethod
    def define_main_window():
        window = Window(pygame.Color('blue'))

        title = Button(700, 150, Utils.screen_width / 2 - 350, 10,
                       pygame.Color('yellow'), "The Bigger Puzzle",
                        pygame.Color('red'), 100, pygame.Color('purple'), 5)

        level_ref = WindowManager.instance.find_object_by_class_type(LevelSelector)

        def stop_running():
            Utils.game_running = False
        quit_button = Button(50, 50, 10, 10, pygame.Color('red'),
                             "X", pygame.Color('black'), 50, pygame.Color('black'), 2)
        quit_button.add_on_click(stop_running)

        wheel_of_colors = Button(325, 325, Utils.screen_width / 2 - 325, 180,
                                 pygame.Color('green'), "Wheel of _colors", pygame.Color('black'), 25,
                                 pygame.Color('purple'), 10)
        wheel_of_colors.add_on_click(WindowManager.instance.go_to_window, 0)
        wheel_of_colors.add_on_click(level_ref.load_levels, 'wheel_of_colors_data.txt')

        flow_free = Button(325, 325, Utils.screen_width / 2 , 180,
                                 pygame.Color('green'), "Flow free", pygame.Color('black'), 25,
                                 pygame.Color('purple'), 10)
        flow_free.add_on_click(WindowManager.instance.go_to_window, 0)
        flow_free.add_on_click(level_ref.load_levels, 'color_connect_data.txt')

        infinity_loop = Button(325, 325, Utils.screen_width / 2 - 325, 505,
                                 pygame.Color('green'), "Infinity loop", pygame.Color('black'), 25,
                                 pygame.Color('purple'), 10)
        infinity_loop.add_on_click(WindowManager.instance.go_to_window, 0)
        infinity_loop.add_on_click(level_ref.load_levels, 'infinity_loop_data.txt')

        water_sort = Button(325, 325, Utils.screen_width / 2 , 505,
                                 pygame.Color('green'), "Water sort", pygame.Color('black'), 25,
                                 pygame.Color('purple'), 10)
        water_sort.add_on_click(WindowManager.instance.go_to_window, 0)
        water_sort.add_on_click(level_ref.load_levels, 'water_sort_data.txt')

        window.add_game_object(title)
        window.add_game_object(quit_button)
        window.add_game_object(wheel_of_colors)
        window.add_game_object(flow_free)
        window.add_game_object(infinity_loop)
        window.add_game_object(water_sort)

        return window

    @staticmethod
    def define_wheel_of_colors_window():
        window = Window(pygame.Color('grey'))

        wheel_game = WheelOfColors(4, [1,1])

        quit_button = Button(50, 50, 10, 10, pygame.Color('red'),
                             "X", pygame.Color('black'), 50, pygame.Color('black'), 2)
        quit_button.add_on_click(WindowManager.instance.go_to_window, 1)

        restart_button = Button(50, 50, 70, 10, pygame.Color('orange'),
                             "o", pygame.Color('black'), 50, pygame.Color('black'), 2)
        restart_button.add_on_click(wheel_game.new_game)

        window.add_game_object(quit_button)
        window.add_game_object(restart_button)
        window.add_game_object(wheel_game)

        return window

    @staticmethod
    def define_water_sort_window():
        window = Window(pygame.Color('grey'))

        water_sort = WaterSort(2,5,[1,2,1,2])

        quit_button = Button(50, 50, 10, 10, pygame.Color('red'),
                             "X", pygame.Color('black'), 50, pygame.Color('black'), 2)
        quit_button.add_on_click(WindowManager.instance.go_to_window, 1)

        restart_button = Button(50, 50, 70, 10, pygame.Color('orange'),
                                "o", pygame.Color('black'), 50, pygame.Color('black'), 2)
        restart_button.add_on_click(water_sort.new_game)

        undo_button = Button(50, 50, 130, 10, pygame.Color('orange'),
                                "<", pygame.Color('black'), 50, pygame.Color('black'), 2)
        undo_button.add_on_click(water_sort.undo)

        window.add_game_object(quit_button)
        window.add_game_object(restart_button)
        window.add_game_object(undo_button)
        window.add_game_object(water_sort)

        return window

    @staticmethod
    def define_infinity_loop_window():
        window = Window(pygame.Color('grey'))

        board = InfinityLoop(5, 8 )
        quit_button = Button(50, 50, 10, 10, pygame.Color('red'),
                             "X", pygame.Color('black'), 50, pygame.Color('black'), 2)
        quit_button.add_on_click(WindowManager.instance.go_to_window, 1)
        restart_button = Button(50, 50, 70, 10, pygame.Color('orange'),
                                "o", pygame.Color('black'), 50, pygame.Color('black'), 2)
        restart_button.add_on_click(board.new_game)

        window.add_game_object(quit_button)
        window.add_game_object(restart_button)
        window.add_game_object(board)

        return window

    @staticmethod
    def define_color_connect_window():
        window = Window(pygame.Color('grey'))

        grid = ColorConnect(6, 8, 6)
        quit_button = Button(50, 50, 10, 10, pygame.Color('red'),
                             "X", pygame.Color('black'), 50, pygame.Color('black'), 2)
        quit_button.add_on_click(WindowManager.instance.go_to_window, 1)
        restart_button = Button(50, 50, 70, 10, pygame.Color('orange'),
                                "o", pygame.Color('black'), 50, pygame.Color('black'), 2)
        restart_button.add_on_click(grid.new_game)

        window.add_game_object(quit_button)
        window.add_game_object(restart_button)
        window.add_game_object(grid)

        return window

    @staticmethod
    def define_level_window():
        window = Window(pygame.Color('grey'))

        levels = LevelSelector(WindowManager.instance)

        quit_button = Button(50, 50, 10, 10, pygame.Color('red'),
                             "X", pygame.Color('black'), 50, pygame.Color('black'), 2)
        quit_button.add_on_click(WindowManager.instance.go_to_window, 1)

        window.add_game_object(quit_button)
        window.add_game_object(levels)

        return window


class WindowManager:

    instance = None

    def __init__(self):
        if WindowManager.instance:
            return

        WindowManager.instance = self

        info = pygame.display.Info()
        Utils.screen_width = info.current_w
        Utils.screen_height = info.current_h
        self._screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN | pygame.SCALED)

        self._current_window = 1
        self._windows = []

        WindowDefiner.fill_window_manager()

    def add_window(self, window):
        self._windows.append(window)

    def go_to_window(self, window_number):
        self._current_window = window_number

    def update(self):
        if len(self._windows) <= self._current_window:
            return

        self._windows[self._current_window].update()

    def draw(self):
        if len(self._windows) <= self._current_window:
            return

        self._windows[self._current_window].draw(self._screen)

    def check_click(self, mouse_x, mouse_y):
        if len(self._windows) <= self._current_window:
            return

        self._windows[self._current_window].check_click(mouse_x, mouse_y)

    def find_object_by_class_type(self, class_type):
        for window in self._windows:
            obj = window.find_by_class_type(class_type)
            if obj:
                return obj

    def remove_object_from_window(self, class_type, window_number):
        self._windows[window_number].remove_game_object(class_type)

    def add_object_in_window(self, obj, window_number):
        self._windows[window_number].add_game_object(obj)
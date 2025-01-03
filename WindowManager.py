import pygame
import Utils
from UIManager import Button, Flask
from WaterSort import WaterSort
from WheelOfColors import WheelGame


class Window:

    def __init__(self, background_color):
        self.background_color = background_color
        self._game_objects = []

    def add_game_object(self, game_object):
        self._game_objects.append(game_object)

    def update(self):
        for game_object in self._game_objects:
            game_object.update()

    def draw(self, screen):
        screen.fill(self.background_color)
        for game_object in self._game_objects:
            game_object.draw(screen)

    def check_click(self, mouse_x, mouse_y):
        for game_object in self._game_objects:
            game_object.check_click(mouse_x, mouse_y)


class WindowDefiner:

    @staticmethod
    def fill_window_manager():
        WindowManager.instance.add_window(WindowDefiner.define_main_window())
        WindowManager.instance.add_window(WindowDefiner.define_wheel_of_colors_window())
        WindowManager.instance.add_window(WindowDefiner.define_water_sort_window())

    @staticmethod
    def define_main_window():
        window = Window(pygame.Color('blue'))

        title = Button(700, 150, Utils.screen_width / 2 - 350, 10,
                       pygame.Color('yellow'), "The Bigger Puzzle",
                        pygame.Color('red'), 100, pygame.Color('purple'), 5)

        def stop_running():
            Utils.running = False
        quit_button = Button(50, 50, 10, 10, pygame.Color('red'),
                             "X", pygame.Color('black'), 50, pygame.Color('black'), 2)
        quit_button.add_on_click(stop_running)

        wheel_of_colors = Button(325, 325, Utils.screen_width / 2 - 325, 180,
                                 pygame.Color('green'), "Wheel of colors", pygame.Color('black'), 25,
                                 pygame.Color('purple'), 10)
        wheel_of_colors.add_on_click(WindowManager.instance.go_to_window, 1)

        flow_free = Button(325, 325, Utils.screen_width / 2 , 180,
                                 pygame.Color('green'), "Flow free", pygame.Color('black'), 25,
                                 pygame.Color('purple'), 10)

        infinity_loop = Button(325, 325, Utils.screen_width / 2 - 325, 505,
                                 pygame.Color('green'), "Infinity loop", pygame.Color('black'), 25,
                                 pygame.Color('purple'), 10)

        water_sort = Button(325, 325, Utils.screen_width / 2 , 505,
                                 pygame.Color('green'), "Water sort", pygame.Color('black'), 25,
                                 pygame.Color('purple'), 10)
        water_sort.add_on_click(WindowManager.instance.go_to_window, 2)

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

        score_text = Button(600, 100, Utils.screen_width // 2 - 300, 10, pygame.Color('Green'),
                            'Score: 0', pygame.Color('black'), 50, pygame.Color('black'), 2)

        wheel_game = WheelGame(6, score_text)

        quit_button = Button(50, 50, 10, 10, pygame.Color('red'),
                             "X", pygame.Color('black'), 50, pygame.Color('black'), 2)
        quit_button.add_on_click(WindowManager.instance.go_to_window, 0)

        restart_button = Button(50, 50, 70, 10, pygame.Color('orange'),
                             "o", pygame.Color('black'), 50, pygame.Color('black'), 2)
        restart_button.add_on_click(wheel_game.restart)

        window.add_game_object(quit_button)
        window.add_game_object(restart_button)
        window.add_game_object(wheel_game)

        return window

    @staticmethod
    def define_water_sort_window():
        window = Window(pygame.Color('grey'))

        quit_button = Button(50, 50, 10, 10, pygame.Color('red'),
                             "X", pygame.Color('black'), 50, pygame.Color('black'), 2)
        quit_button.add_on_click(WindowManager.instance.go_to_window, 0)

        water_sort = WaterSort(4, 6)

        window.add_game_object(quit_button)
        window.add_game_object(water_sort)

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
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN | pygame.SCALED)

        self.current_window = 0
        self.windows = []
        WindowDefiner.fill_window_manager()

    def add_window(self, window):
        self.windows.append(window)

    def go_to_window(self, window_number):
        self.current_window = window_number

    def update(self):
        if len(self.windows) <= self.current_window:
            return

        self.windows[self.current_window].update()

    def draw(self):
        if len(self.windows) <= self.current_window:
            return

        self.windows[self.current_window].draw(self.screen)

    def check_click(self, mouse_x, mouse_y):
        if len(self.windows) <= self.current_window:
            return

        self.windows[self.current_window].check_click(mouse_x, mouse_y)
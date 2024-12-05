import pygame
import Utils
from UIManager import Button

class Window:

    def __init__(self, background_color):
        self.background_color = background_color
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def draw(self, screen):
        screen.fill(self.background_color)
        for button in self.buttons:
            button.draw(screen)

    def check_click(self, mouse_x, mouse_y):
        for button in self.buttons:
            button.check_click(mouse_x, mouse_y)

class WindowDefiner:

    screen_width = 0
    screen_height = 0

    @staticmethod
    def fill_window_manager():
        WindowManager.INSTANCE.add_window(WindowDefiner.define_main_window())

    @staticmethod
    def define_main_window():
        window = Window(pygame.Color('blue'))

        title = Button(700, 150, WindowDefiner.screen_width / 2 - 350, 10,
                       pygame.Color('yellow'), "The Bigger Puzzle",
                        pygame.Color('red'), 100, pygame.Color('purple'), 5)

        def stop_running():
            Utils.running = False
        quit_button = Button(50, 50, 10, 10, pygame.Color('red'),
                             "X", pygame.Color('black'), 50, pygame.Color('black'), 2)
        quit_button.add_on_click(stop_running)

        wheel_of_colors = Button(325, 325, WindowDefiner.screen_width / 2 - 325, 180,
                                 pygame.Color('green'), "Wheel of colors", pygame.Color('black'), 25,
                                 pygame.Color('purple'), 10)

        flow_free = Button(325, 325, WindowDefiner.screen_width / 2 , 180,
                                 pygame.Color('green'), "Flow free", pygame.Color('black'), 25,
                                 pygame.Color('purple'), 10)

        infinity_loop = Button(325, 325, WindowDefiner.screen_width / 2 - 325, 505,
                                 pygame.Color('green'), "Infinity loop", pygame.Color('black'), 25,
                                 pygame.Color('purple'), 10)

        water_sort = Button(325, 325, WindowDefiner.screen_width / 2 , 505,
                                 pygame.Color('green'), "Water sort", pygame.Color('black'), 25,
                                 pygame.Color('purple'), 10)

        window.add_button(title)
        window.add_button(quit_button)
        window.add_button(wheel_of_colors)
        window.add_button(flow_free)
        window.add_button(infinity_loop)
        window.add_button(water_sort)

        return window

class WindowManager:

    INSTANCE = None

    def __init__(self):
        if WindowManager.INSTANCE:
            return

        WindowManager.INSTANCE = self

        info = pygame.display.Info()
        WindowDefiner.screen_width = info.current_w
        WindowDefiner.screen_height = info.current_h
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN | pygame.SCALED)

        self.current_window = 0
        self.windows = []
        WindowDefiner.fill_window_manager()

    def add_window(self, window):
        self.windows.append(window)

    def go_to_window(self, window_number):
        self.current_window = window_number

    def draw(self):
        if len(self.windows) <= self.current_window:
            return

        self.windows[self.current_window].draw(self.screen)

    def check_click(self, mouse_x, mouse_y):
        if len(self.windows) <= self.current_window:
            return

        self.windows[self.current_window].check_click(mouse_x, mouse_y)
import pygame
import GlobalVariables
from Button import Button
from ColorConnect import ColorConnect
from InfinityLoop import InfinityLoop
from LevelSystem import LevelSystem
from WaterSort import WaterSort
from WheelOfColors import WheelOfColors
from Window import Window
from AnchorCalculator import Anchor


class WindowContentFiller:

    @staticmethod
    def define_window_manager_windows(window_system):
        WindowContentFiller._define_level_system_window(window_system)
        WindowContentFiller._define_main_menu(window_system)
        WindowContentFiller._define_wheel_of_colors_window(window_system)
        WindowContentFiller._define_infinity_loop_window(window_system)
        WindowContentFiller._define_water_sort_window(window_system)
        WindowContentFiller._define_color_connect_window(window_system)

        window_system.go_to_window('main_window')

    @staticmethod
    def _define_main_menu(window_system):
        window = Window(pygame.Color('grey'), 'main_window')

        title_width, title_height = Anchor.get_proportions(1/3, 1/10)
        title = Button(title_width,title_height, *Anchor.top_middle(0,10,title_width),
                       pygame.Color('orange'), text='THE BIGGER PUZZLE', font_size=60, name='title')

        game_button_width, game_button_height = Anchor.get_proportions(1/4, 1/4)

        wheel_of_colors_button = Button(game_button_width, game_button_height,
                                        *Anchor.center(-game_button_width // 2, -game_button_height // 2,
                                                       game_button_width, game_button_height),
                                        pygame.Color('green'), text='Wheel of colors', name='wheel_button')
        wheel_of_colors_button.add_on_click(window_system.go_to_window, 'level_select_window')
        wheel_of_colors_button.add_on_click(window_system.get_object_by_name('level_system').load,
                                            GlobalVariables.WHEEL_OF_COLORS_GAME_ID)

        infinity_loop_button = Button(game_button_width, game_button_height,
                                        *Anchor.center(game_button_width // 2, -game_button_height // 2,
                                                       game_button_width, game_button_height),
                                        pygame.Color('green'), text='Infinity loop', name='infinity_button')
        infinity_loop_button.add_on_click(window_system.go_to_window, 'level_select_window')
        infinity_loop_button.add_on_click(window_system.get_object_by_name('level_system').load,
                                            GlobalVariables.INFINITY_LOOP_GAME_ID)

        water_sort_button = Button(game_button_width, game_button_height,
                                        *Anchor.center(-game_button_width // 2, game_button_height // 2,
                                                       game_button_width, game_button_height),
                                        pygame.Color('green'), text='Water sort', name='water_button')
        water_sort_button.add_on_click(window_system.go_to_window, 'level_select_window')
        water_sort_button.add_on_click(window_system.get_object_by_name('level_system').load,
                                            GlobalVariables.WATER_SORT_GAME_ID)

        color_connect_button = Button(game_button_width, game_button_height,
                                        *Anchor.center(game_button_width // 2, game_button_height // 2,
                                                       game_button_width, game_button_height),
                                        pygame.Color('green'), text='Color connect', name='color_button')
        color_connect_button.add_on_click(window_system.go_to_window, 'level_select_window')
        color_connect_button.add_on_click(window_system.get_object_by_name('level_system').load,
                                            GlobalVariables.COLOR_CONNECT_GAME_ID)

        window.add_child(title)
        window.add_child(wheel_of_colors_button)
        window.add_child(infinity_loop_button)
        window.add_child(water_sort_button)
        window.add_child(color_connect_button)

        window_system.add_child(window)

    @staticmethod
    def _define_level_system_window(window_system):
        window = Window(pygame.Color('grey'), 'level_select_window')

        back_to_menu_button = Button(50, 50, *Anchor.top_left(10, 10),
                                     pygame.Color('orange'), text='back', name='back_button')
        back_to_menu_button.add_on_click(window_system.go_to_window, 'main_window')

        endless_mode_button = Button(100, 50, *Anchor.top_right(10, 10, 100),
                                     pygame.Color('green'), text='ENDLESS', name='endless_button')

        level_system = LevelSystem(window_system, 'level_system')

        window.add_child(back_to_menu_button)
        window.add_child(endless_mode_button)
        window.add_child(level_system)

        window_system.add_child(window)

    @staticmethod
    def _define_wheel_of_colors_window(window_system):
        window = Window(pygame.Color('grey'), 'wheel_of_colors_window')

        back_to_levels_button = Button(50, 50, *Anchor.top_left(10, 10),
                                       pygame.Color('orange'), text='back', name='back_button')
        back_to_levels_button.add_on_click(window_system.go_to_window, 'level_select_window')
        back_to_levels_button.add_on_click(window_system.get_object_by_name('level_system').load,
                                           GlobalVariables.WHEEL_OF_COLORS_GAME_ID)

        wheel_of_colors = WheelOfColors(4)

        window.add_child(back_to_levels_button)
        window.add_child(wheel_of_colors)

        window_system.add_child(window)

    @staticmethod
    def _define_infinity_loop_window(window_system):
        window = Window(pygame.Color('grey'), 'infinity_loop_window')

        back_to_levels_button = Button(50, 50, *Anchor.top_left(10, 10),
                                       pygame.Color('orange'), text='back', name='back_button')
        back_to_levels_button.add_on_click(window_system.go_to_window, 'level_select_window')
        back_to_levels_button.add_on_click(window_system.get_object_by_name('level_system').load,
                                           GlobalVariables.INFINITY_LOOP_GAME_ID)

        infinity_loop = InfinityLoop(10, 10)

        window.add_child(back_to_levels_button)
        window.add_child(infinity_loop)

        window_system.add_child(window)

    @staticmethod
    def _define_water_sort_window(window_system):
        window = Window(pygame.Color('grey'), 'water_sort_window')

        back_to_levels_button = Button(50, 50, *Anchor.top_left(10, 10),
                                       pygame.Color('orange'), text='back', name='back_button')
        back_to_levels_button.add_on_click(window_system.go_to_window, 'level_select_window')
        back_to_levels_button.add_on_click(window_system.get_object_by_name('level_system').load,
                                           GlobalVariables.WATER_SORT_GAME_ID)

        water_sort = WaterSort(5, 10)

        window.add_child(back_to_levels_button)
        window.add_child(water_sort)

        window_system.add_child(window)

    @staticmethod
    def _define_color_connect_window(window_system):
        window = Window(pygame.Color('grey'), 'color_connect_window')

        back_to_levels_button = Button(50, 50, *Anchor.top_left(10, 10),
                                       pygame.Color('orange'), text='back', name='back_button')
        back_to_levels_button.add_on_click(window_system.go_to_window, 'level_select_window')
        back_to_levels_button.add_on_click(window_system.get_object_by_name('level_system').load,
                                           GlobalVariables.COLOR_CONNECT_GAME_ID)

        color_connect = ColorConnect(10, 8, 9)

        window.add_child(back_to_levels_button)
        window.add_child(color_connect)

        window_system.add_child(window)
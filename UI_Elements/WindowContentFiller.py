import pygame
from Utilities import GlobalVariables
from Games_Logic.BiggerPuzzleGame import Puzzle
from UI_Elements.Button import Button
from UI_Elements.Text import Text
from Games_Logic.ColorConnect import ColorConnect
from Games_Logic.InfinityLoop import InfinityLoop
from UI_Elements.LevelSystem import LevelSystem
from Games_Logic.WaterSort import WaterSort
from Games_Logic.WheelOfColors import WheelOfColors
from UI_Elements.Window import Window
from Utilities.AnchorCalculator import Anchor


class WindowContentFiller:

    @staticmethod
    def define_window_manager_windows(window_system):
        WindowContentFiller._define_level_system_window(window_system)
        WindowContentFiller._define_main_menu(window_system)
        WindowContentFiller._define_wheel_of_colors_window(window_system)
        WindowContentFiller._define_infinity_loop_window(window_system)
        WindowContentFiller._define_water_sort_window(window_system)
        WindowContentFiller._define_color_connect_window(window_system)
        WindowContentFiller._define_quit_window(window_system)

        window_system.go_to_window('main_window')

    @staticmethod
    def _define_main_menu(window_system):
        window = Window(pygame.Color('grey'), 'main_window')

        title = Text(*Anchor.top_middle(0,100,0),'THE BIGGER PUZZLE',
                     color=pygame.Color('black'), font_size=80, name='title', font_path='Fonts/LuckiestGuy.ttf')

        on_click_data = []

        on_click_data.append(((window_system.go_to_window, 'level_select_window'),
                              (window_system.get_object_by_name('level_system').load, GlobalVariables.WHEEL_OF_COLORS_GAME_ID)))
        on_click_data.append(((window_system.go_to_window, 'level_select_window'), (window_system.get_object_by_name('level_system').load,
                                                                                    GlobalVariables.INFINITY_LOOP_GAME_ID)))
        on_click_data.append(((window_system.go_to_window, 'level_select_window'), (window_system.get_object_by_name('level_system').load,
                                                                                    GlobalVariables.WATER_SORT_GAME_ID)))
        on_click_data.append(((window_system.go_to_window, 'level_select_window'), (window_system.get_object_by_name('level_system').load,
                                                                                    GlobalVariables.COLOR_CONNECT_GAME_ID)))

        _, piece_size = Anchor.get_proportions(1, 1 / 3)
        bigger_puzzle = Puzzle(*Anchor.center(0, 50, 2 * piece_size, 2 * piece_size), on_click_data, piece_size, 'LevelData/output.png')

        window.add_child(title)
        window.add_child(bigger_puzzle)
        window_system.add_child(window)

    @staticmethod
    def _define_level_system_window(window_system):
        window = Window(pygame.Color('grey'), 'level_select_window')

        back_to_menu_button = Button(50, 50, *Anchor.top_left(10, 10),
                                     pygame.Color('orange'), text='back', name='back_button')
        back_to_menu_button.add_on_click(window_system.go_to_window, 'main_window')

        endless_mode_button = Button(100, 50, *Anchor.top_right(10, 10, 100),
                                     (0, 200, 0), text='ENDLESS', name='endless_button')

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

    @staticmethod
    def _define_quit_window(window_system):
        window = Window(pygame.Color('yellow'), 'quit_window')

        question_text = Text(*Anchor.center(0, -100, 0, 0), 'Do you want to quit?',
                             font_size=75, font_path='Fonts/LuckiestGuy.ttf')

        quit_button = Button(300, 150, *Anchor.center(-175, 50, 300, 150),
                             pygame.Color('red'), text='Quit', font_size=50)
        def quit_game():
            GlobalVariables.game_running = False
        quit_button.add_on_click(quit_game)

        stay_button = Button(300, 150, *Anchor.center(175, 50, 300, 150),
                             (0, 200, 0), text='Stay', font_size=50)
        stay_button.add_on_click(window_system.go_to_window, 'main_window')

        window.add_child(quit_button)
        window.add_child(stay_button)
        window.add_child(question_text)

        window_system.add_child(window)
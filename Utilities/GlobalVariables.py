#general
game_running = True
screen_width = 0
screen_height = 0

HIGHLIGHT_FRAME_DURATION = 15
FRAMES_BETWEEN_HIGHLIGHTS = 3
CLICK_HOLD_FRAMES_THRESHOLD = 10

#level system
TOTAL_LEVELS_EACH_GAME = 20
LEVEL_BUTTONS_IN_ROW = 10
LEVEL_BUTTON_TO_HEIGHT = 1 / 9

WHEEL_OF_COLORS_GAME_ID = 0
INFINITY_LOOP_GAME_ID = 1
WATER_SORT_GAME_ID = 2
COLOR_CONNECT_GAME_ID = 3

GAME_DATA_FILES = ['LevelData/wheel_of_colors_data.txt', 'LevelData/infinity_loop_data.txt',
                   'LevelData/water_sort_data.txt', 'LevelData/color_connect_data.txt']

#games
COLORS = [
    (255, 59, 48),
    (0, 71, 171),
    (255, 225, 25),
    (0, 100, 0),
    (255, 163, 0),
    (173, 216, 230),
    (255, 105, 180),
    (0, 128, 128),
    (147, 112, 219),
    (144, 238, 144),
    (255, 0, 144),
    (139, 69, 19)
]

#wheel of colors
WOC_RADIUS_TO_HEIGHT_RATIO = 1 / 3
WOC_CENTER_RADIUS_RATIO = 1 / 4

#infinity loop
IL_PIECE_WIDTH = 15
IL_PIECE_HEIGHT = 50

#water sort
WS_FLASK_WIDTH = 55
WS_FLASK_HEIGHT = 60
WS_EMPTY_FLASKS = 2
WS_SOLVER_TIME_LIMIT = 2

#color connect
CC_TILE_SIZE = 70
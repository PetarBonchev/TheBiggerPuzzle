import Utils
import pygame
from UIManager import ColorWheel, Button
from random import randint

class WheelOfColors:

    WHEEL_RADIUS = Utils.WHEEL_OF_COLORS_RADIUS
    COLOR_DISPLAY_TIME = Utils.COLOR_DISPLAY_FRAMES

    def __init__(self, color_count, game_data = None):
        self._color_count = color_count
        self._color_wheel = ColorWheel(color_count, Utils.screen_width // 2,
                                       Utils.screen_height // 2, WheelOfColors.WHEEL_RADIUS)
        self._score_text = Button(600, 100, Utils.screen_width // 2 - 300, 10, pygame.Color('Green'),
                            'Score: 0', pygame.Color('black'), 50, pygame.Color('black'), 2)
        self._pattern = []
        self._game_state = 1
        self._timer = 0
        self._displayed_color = 0
        self._color_to_receive = 0
        self._game_data = game_data

        self.new_game()

    def draw(self, screen):
        self._color_wheel.draw(screen)
        self._score_text.draw(screen)

    def check_click(self, mouse_x, mouse_y):
        if self._game_state != 4:
            return
        clicked_color = self._color_wheel.check_click(mouse_x, mouse_y)
        if 0 <= clicked_color < self._color_count:
            self._receive_color(clicked_color)

    def update(self):
        if self._game_state == 1:
            self._timer -= 1
            if self._timer <= 0:
                self._timer = 0
                self._pick_color()
                self._game_state = 2
        elif self._game_state == 2:
            state = self._display_color()
            self._game_state = state
        elif self._game_state == 3:
            self._timer -= 1
            if self._timer <= 0:
                self._displayed_color += 1
                self._game_state = 2
        elif self._game_state == 4:
            pass
        elif self._game_state == -1:
            self._color_wheel.stop_all_highlights()
            for i in range(self._color_count):
                self._color_wheel.highlight_sector(i)
            self._score_text.set_text(f"Game over! Final score: {len(self._pattern) - 1}")
            self._game_state = -2

    def new_game(self):
        self._pattern = []
        self._game_state = 1
        self._timer = 0
        self._color_to_receive = 0
        self._displayed_color = 0
        self._color_wheel.stop_all_highlights()
        self._score_text.set_text("Score: 0")

    def _pick_color(self):
        if self._game_data:
            self._pattern.append(self._game_data[len(self._pattern)])
        else:
            new_color = randint(0, self._color_count - 1)
            self._pattern.append(new_color)

    def _display_color(self):
        if self._displayed_color >= len(self._pattern):
            self._displayed_color = 0
            return 4
        self._color_wheel.highlight_sector(self._pattern[self._displayed_color])
        self._timer = WheelOfColors.COLOR_DISPLAY_TIME
        return 3

    def _receive_color(self, color_id):
        if self._game_state != 4:
            return
        if self._pattern[self._color_to_receive] == color_id:
            self._color_to_receive += 1
            if self._color_to_receive >= len(self._pattern):
                if self._game_data and len(self._game_data) == len(self._pattern):
                    self._score_text.set_text(f'You win!')
                    self._game_state = -2
                    return
                self._score_text.set_text(f'Score: {len(self._pattern)}')
                self._color_to_receive = 0
                self._game_state = 1
                self._timer = WheelOfColors.COLOR_DISPLAY_TIME
        else:
            self._game_state = -1

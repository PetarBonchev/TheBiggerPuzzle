import Utils
from UIManager import ColorWheel
from random import randint

class WheelGame:

    WHEEL_RADIUS = 350
    COLOR_DISPLAY_TIME = Utils.WOC_COLOR_DISPLAY_TIME

    def __init__(self, color_count, score_text):
        self._color_count = color_count
        self._color_wheel = ColorWheel(color_count, Utils.screen_width // 2,
                                       Utils.screen_height // 2, WheelGame.WHEEL_RADIUS)
        self._score_text = score_text
        self._pattern = []
        self._game_state = 1
        self._timer = 0
        self._displayed_color = 0
        self._color_to_receive = 0

    def draw(self, screen):
        self._color_wheel.draw(screen)
        self._score_text.draw(screen)

    def check_click(self, mouse_x, mouse_y):
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
            self._color_wheel.stop_all_highlight()
            for i in range(self._color_count):
                self._color_wheel.highlight_sector(i)
            self._score_text.set_text(f"Game over! Final score: {len(self._pattern) - 1}")
            self._game_state = -2

    def restart(self):
        self._pattern = []
        self._game_state = 1
        self._timer = 0
        self._color_to_receive = 0
        self._displayed_color = 0
        self._color_wheel.stop_all_highlight()
        self._score_text.set_text("Score: 0")

    def _pick_color(self):
        new_color = randint(0, self._color_count - 1)
        self._pattern.append(new_color)

    def _display_color(self):
        if self._displayed_color >= len(self._pattern):
            self._displayed_color = 0
            return 4
        self._color_wheel.highlight_sector(self._pattern[self._displayed_color])
        self._timer = WheelGame.COLOR_DISPLAY_TIME
        return 3

    def _receive_color(self, color_id):
        if self._game_state != 4:
            return
        if self._pattern[self._color_to_receive] == color_id:
            self._color_to_receive += 1
            if self._color_to_receive >= len(self._pattern):
                self._score_text.set_text(f'Score: {len(self._pattern)}')
                self._color_to_receive = 0
                self._game_state = 1
                self._timer = WheelGame.COLOR_DISPLAY_TIME
        else:
            self._game_state = -1

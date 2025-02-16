import pygame
from random import randint
from Utilities import GlobalVariables
from Utilities.AnchorCalculator import Anchor
from UI_Elements.GameObject import GameObject
from UI_Elements.ColorWheelUI import ColorWheel
from UI_Elements.LevelSystem import LevelSystem
from UI_Elements.Text import Text
from UI_Elements.Button import Button

class WheelOfColors(GameObject):
    def __init__(self, color_count, game_data=None, name='wheel_of_colors'):
        super().__init__(name)
        self._color_count = color_count
        self._game_data = game_data
        self._level_id = -1
        self._radius = GlobalVariables.screen_height * GlobalVariables.WOC_RADIUS_TO_HEIGHT_RATIO
        color_wheel = ColorWheel(self._color_count, *Anchor.center(0, 0, 0, 0), self._radius, name='color_wheel')
        score_text = Text(*Anchor.top_middle(0, 40, 0), 'Score: 0', pygame.Color('black'), 50, 'score_text')
        restart_button = Button(100, 50, *Anchor.top_left(70, 10), pygame.Color('orange'), text="Restart", name='restart_button')
        restart_button.add_on_click(self.new_game)

        self.add_child(color_wheel)
        self.add_child(score_text)
        self.add_child(restart_button)

        self._pattern = []
        self._game_state = None
        self._color_to_receive = 0
        self.new_game()

    def new_game(self):
        self._pattern = []
        self._game_state = 'pick_color'
        self._color_to_receive = 0
        self.get_object_by_name('color_wheel').stop_all_highlights()
        self.get_object_by_name('score_text').set_text("Score: 0")
        if self._game_data is None:
            self._color_count = randint(2, 10)
        self.get_object_by_name('color_wheel').reset(self._color_count)

    def reset(self, color_count=-1, game_data=None, level_id=-1):
        self._color_count = color_count
        self._game_data = game_data
        self._level_id = level_id
        if game_data:
            self.get_object_by_name('restart_button').set_text('Restart')
        else:
            self.get_object_by_name('restart_button').set_text('New game')
        self.new_game()

    def _check_click(self, mouse_x, mouse_y):
        if self._game_state != 'wait_for_input':
            return
        clicked_color = self.get_object_by_name('color_wheel').clicked_sector(mouse_x, mouse_y)
        if 0 <= clicked_color < self._color_count:
            self._receive_color(clicked_color)
            self.get_object_by_name('color_wheel').set_display_pattern([clicked_color], (0, 200, 0))

    def _update(self):
        match self._game_state:
            case 'pick_color':
                if self.get_object_by_name('color_wheel').is_displaying():
                    return
                self._pick_color()
                self._game_state = 'display_pattern'
                self.get_object_by_name('color_wheel').set_display_pattern(self._pattern, pygame.Color('white'))
            case 'display_pattern':
                if not self.get_object_by_name('color_wheel').is_displaying():
                    self._game_state = 'wait_for_input'
                    self.get_object_by_name('color_wheel').stop_all_highlights()
            case 'game_over':
                self.get_object_by_name('color_wheel').stop_all_highlights()
                self.get_object_by_name('score_text').set_text(f"Game over! Final score: {len(self._pattern) - 1}")
                self._game_state = 'game_ended'
            case _:
                pass

    def _pick_color(self):
        if self._game_data:
            self._pattern.append(self._game_data[len(self._pattern)])
        else:
            self._pattern.append(randint(0, self._color_count - 1))

    def _receive_color(self, color_id):
        if self._pattern[self._color_to_receive] == color_id:
            self._color_to_receive += 1
            if self._color_to_receive >= len(self._pattern):
                if self._game_data and len(self._game_data) == len(self._pattern):
                    self.get_object_by_name('score_text').set_text("You win!")
                    LevelSystem.instance.complete_level(GlobalVariables.WHEEL_OF_COLORS_GAME_ID, self._level_id)
                    self._game_state = 'game_ended'
                else:
                    self.get_object_by_name('score_text').set_text(f"Score: {len(self._pattern)}")
                    self._color_to_receive = 0
                    self._game_state = 'pick_color'
        else:
            self._game_state = 'game_over'

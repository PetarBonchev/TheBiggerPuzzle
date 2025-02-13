import GlobalVariables
from GameObject import GameObject
from PuzzleDisplay import PuzzleDisplay


class Window(GameObject):

    def __init__(self, background_color, name='window'):
        super().__init__(name)
        self._background_color = background_color
        self.puzzle_display = PuzzleDisplay(GlobalVariables.screen_width, GlobalVariables.screen_height, 50)

    def _draw(self, screen):
        screen.fill(self._background_color)
        self.puzzle_display.draw(screen)

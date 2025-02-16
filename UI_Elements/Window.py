from Utilities import GlobalVariables
from UI_Elements.GameObject import GameObject
from UI_Elements.PuzzleDisplay import PuzzleDisplay


class Window(GameObject):
    BACKGROUND_PIECE_SIZE = 50

    def __init__(self, background_color, name='window'):
        super().__init__(name)
        self._background_color = background_color
        puzzle_display = PuzzleDisplay(GlobalVariables.screen_width, GlobalVariables.screen_height, Window.BACKGROUND_PIECE_SIZE)
        self.add_child(puzzle_display)

    def set_active(self, active):
        if type(active) is not bool:
            return
        self._active_buffer = active
        if self._active_buffer:
            self.get_object_by_name('puzzle_display').choose_pieces()

    def _draw(self, screen):
        screen.fill(self._background_color)


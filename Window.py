from GameObject import GameObject


class Window(GameObject):

    def __init__(self, background_color, name='window'):
        super().__init__(name)
        self._background_color = background_color

    def _draw(self, screen):
        screen.fill(self._background_color)

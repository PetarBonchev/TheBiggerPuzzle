class GameObject:
    def __init__(self, name=''):
        self.name = name
        self.children = []
        self._is_active = True
        self._active_buffer = True

    def add_child(self, game_object):
        if not isinstance(game_object, GameObject):
            return
        self.children.append(game_object)

    def set_active(self, active):
        if type(active) is not bool:
            return
        self._active_buffer = active

    def draw(self, screen):
        if not self._is_active:
            return
        self._draw(screen)
        for child in self.children:
            child.draw(screen)

    def check_click(self, mouse_x, mouse_y):
        if not self._is_active:
            return
        self._check_click(mouse_x, mouse_y)
        for child in self.children:
            child.check_click(mouse_x, mouse_y)

    def update(self):
        self._is_active = self._active_buffer
        if not self._is_active:
            return
        self._update()
        for child in self.children:
            child.update()

    def get_object_by_name(self, name):
        if self.name == name:
            return self
        for child in self.children:
            result = child.get_object_by_name(name)
            if result:
                return result
        return None

    def _draw(self, screen):
        pass

    def _check_click(self, mouse_x, mouse_y):
        pass

    def _update(self):
        pass
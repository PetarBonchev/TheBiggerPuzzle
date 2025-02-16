from UI_Elements.GameObject import GameObject


class WindowManager(GameObject):

    def __init__(self):
        super().__init__('window_manager')
        self.current_window = ''

    def go_to_window(self, window_name):
        for child in self.children:
            if child.name == window_name:
                child.set_active(True)
                self.current_window = window_name
            else:
                child.set_active(False)

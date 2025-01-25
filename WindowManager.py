from GameObject import GameObject


class WindowManager(GameObject):

    def __init__(self):
        super().__init__('window_manager')

    def go_to_window(self, window_name):
        for child in self.children:
            if child.name == window_name:
                child.set_active(True)
            else:
                child.set_active(False)

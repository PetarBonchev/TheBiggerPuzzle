from Utilities import GlobalVariables

screen_width = GlobalVariables.screen_width
screen_height = GlobalVariables.screen_height

class Anchor:

    @staticmethod
    def top_left(margin_x, margin_y):
        return margin_x, margin_y

    @staticmethod
    def top_middle(margin_x, margin_y, rect_width):
        return screen_width // 2 + margin_x - rect_width // 2, margin_y

    @staticmethod
    def top_right(margin_x, margin_y, rect_width):
        return screen_width - margin_x - rect_width, margin_y

    @staticmethod
    def middle_left(margin_x, margin_y, rect_height):
        return margin_x, screen_height // 2 + margin_y - rect_height // 2

    @staticmethod
    def center(margin_x, margin_y, rect_width, rect_height):
        return screen_width // 2 + margin_x - rect_width // 2, screen_height // 2 + margin_y - rect_height // 2

    @staticmethod
    def middle_right(margin_x, margin_y, rect_width, rect_height):
        return screen_width - margin_x - rect_width, screen_height // 2 + margin_y - rect_height // 2

    @staticmethod
    def bottom_left(margin_x, margin_y, rect_height):
        return margin_x, screen_height - margin_y - rect_height

    @staticmethod
    def bottom_middle(margin_x, margin_y, rect_width, rect_height):
        return screen_width // 2 + margin_x - rect_width // 2, screen_height - margin_y - rect_height

    @staticmethod
    def bottom_right(margin_x, margin_y, rect_width, rect_height):
        return screen_width - margin_x - rect_width, screen_height - margin_y - rect_height

    @staticmethod
    def get_proportions(proportion_x, proportion_y):
        return screen_width * proportion_x, screen_height * proportion_y
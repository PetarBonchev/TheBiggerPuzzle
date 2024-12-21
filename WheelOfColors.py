import random
import time

class ColorWheel:

    def __init__(self, color_count):
        self.color_count = color_count
        self.sequence = []

    def __iter__(self):
        return iter(self.sequence)

    def add_random_color(self):
        self.sequence.append(random.randrange(0, self.color_count))


class WheelGame:

    def __init__(self, color_count):
        self._wheel = ColorWheel(color_count)

    def game_loop(self):
        while True:
            self._wheel.add_random_color()
            self._print_current_pattern()
            if not self._check_pattern():
                break
        print(f"Wrong! Score: {len(self._wheel.sequence) - 1}")

    def _print_current_pattern(self):
        for color in self._wheel:
            print(color)
            time.sleep(.5)

    def _check_pattern(self):
        for color in self._wheel:
            if int(input()) != color:
                return False
        return True

game = WheelGame(3)
game.game_loop()
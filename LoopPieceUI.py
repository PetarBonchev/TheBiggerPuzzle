import pygame
import GlobalVariables
from GameObject import GameObject


class LoopPiece(GameObject):

    def __init__(self, connections, top_left_x, top_left_y, name='loop_piece'):
        super().__init__(name)
        self._connections = connections
        self._top_left_x = top_left_x
        self._top_left_y = top_left_y

        self._width = GlobalVariables.IL_PIECE_WIDTH
        self._height = GlobalVariables.IL_PIECE_HEIGHT
        self._dot_radius = 4 / 3

    def _draw(self, screen):
        if self.up:
            rect = pygame.Rect(self._top_left_x, self._top_left_y - self._height + self._width,
                               self._width, self._height)
            pygame.draw.rect(screen, pygame.Color('black'), rect)
        if self.right:
            rect = pygame.Rect(self._top_left_x, self._top_left_y, self._height, self._width)
            pygame.draw.rect(screen, pygame.Color('black'), rect)
        if self.down:
            rect = pygame.Rect(self._top_left_x, self._top_left_y, self._width, self._height)
            pygame.draw.rect(screen, pygame.Color('black'), rect)
        if self.left:
            rect = pygame.Rect(self._top_left_x - self._height + self._width, self._top_left_y,
                               self._height, self._width)
            pygame.draw.rect(screen, pygame.Color('black'), rect)
        if sum(self._connections) == 1:
            pygame.draw.circle(screen, pygame.Color('black'), (self._top_left_x + self._width // 2,
                                self._top_left_y + self._width // 2),
                                self._dot_radius * self._width)

    def _check_click(self, mouse_x, mouse_y):
        if self._top_left_x - self._height + self._width <= mouse_x < (
                self._top_left_x + self._height) and (self._top_left_y - self._height
                + self._width) <= mouse_y < self._top_left_y + self._height:
            self.rotate()
            return True
        return False

    def rotate(self, times=1):
        if times % 4 == 1:
            self._connections[0], self._connections[1], self._connections[2], self._connections[3] = (
                self.left, self.up, self.right, self.down)
        elif times % 4 == 2:
            self._connections[0], self._connections[2] = self.down, self.up
            self._connections[1], self._connections[3] = self.left, self.right
        elif times % 4 == 3:
            self._connections[0], self._connections[1], self._connections[2], self._connections[3] = (
                self.right, self.down, self.left, self.up)

    @property
    def state(self):
        return (self.up << 3) | (self.right << 2) | (self.down << 1) | self.left

    @property
    def up(self):
        return self._connections[0]

    @property
    def right(self):
        return self._connections[1]

    @property
    def down(self):
        return self._connections[2]

    @property
    def left(self):
        return self._connections[3]
import pygame
from Utilities import GlobalVariables
from UI_Elements.LevelSystem import LevelSystem
from UI_Elements.GameObject import GameObject
from UI_Elements.PuzzlePartUI import PuzzlePart


class Puzzle(GameObject):

    def __init__(self, top_left_x, top_left_y, on_click_data, piece_size=300, background_image_file=None, name='bigger_puzzle'):
        super().__init__(name)
        self._top_left_x = top_left_x
        self._top_left_y = top_left_y
        self._piece_size = piece_size
        if background_image_file:
            self._image = pygame.image.load(background_image_file)

        self._create_puzzle_pieces(on_click_data)
        self.update_solved_puzzles()

    def update_solved_puzzles(self):
        completed_levels = LevelSystem.get_completed_levels()
        games = [('wheel_of_colors_piece', GlobalVariables.WHEEL_OF_COLORS_GAME_ID),
                 ('infinity_loop_piece', GlobalVariables.INFINITY_LOOP_GAME_ID),
                 ('water_sort_piece', GlobalVariables.WATER_SORT_GAME_ID),
                 ('color_connect_piece', GlobalVariables.COLOR_CONNECT_GAME_ID)]

        for piece_name, game_id in games:
            score_text = self.get_object_by_name(piece_name).get_object_by_name('score_text')
            if len(completed_levels[game_id]) == GlobalVariables.TOTAL_LEVELS_EACH_GAME:
                score_text.set_text('')
                self.get_object_by_name(piece_name).make_transparent()
            else:
                score_text.set_text(f'{len(completed_levels[game_id])} / {GlobalVariables.TOTAL_LEVELS_EACH_GAME}')

    def _draw(self, screen):
        if self._image:
            screen.blit(self._image, (self._top_left_x, self._top_left_y))

    def _create_puzzle_pieces(self, on_click_data):
        wheel_piece = PuzzlePart(self._top_left_x, self._top_left_y, (0, 1, 1, 0), self._piece_size,
                                 text='Wheel of colors', score_text='0/0', name='wheel_of_colors_piece')
        for on_click in on_click_data[0]:
            wheel_piece.add_on_click(*on_click)
        self.add_child(wheel_piece)

        infinity_loop_piece = PuzzlePart(self._top_left_x + self._piece_size, self._top_left_y, (0, 0, 1, -1), self._piece_size,
                                text='Infinity loop', score_text='0/0', name='infinity_loop_piece')
        for on_click in on_click_data[1]:
            infinity_loop_piece.add_on_click(*on_click)
        self.add_child(infinity_loop_piece)

        water_sort_piece = PuzzlePart(self._top_left_x, self._top_left_y + self._piece_size, (-1, -1, 0, 0), self._piece_size,
                                 text='Water sort', score_text='0/0', name='water_sort_piece')
        for on_click in on_click_data[2]:
            water_sort_piece.add_on_click(*on_click)
        self.add_child(water_sort_piece)

        color_connect_piece = PuzzlePart(self._top_left_x + self._piece_size, self._top_left_y + self._piece_size, (-1, 0, 0, 1), self._piece_size,
                                 text='Color connect', score_text='0/0', name='color_connect_piece')
        for on_click in on_click_data[3]:
            color_connect_piece.add_on_click(*on_click)
        self.add_child(color_connect_piece)
import pygame

from UI_Elements.WindowManager import WindowManager
from UI_Elements.WindowContentFiller import WindowContentFiller
from Utilities import AnchorCalculator, GlobalVariables

pygame.init()
clock = pygame.time.Clock()

info = pygame.display.Info()
GlobalVariables.screen_width = info.current_w
GlobalVariables.screen_height = info.current_h
AnchorCalculator.screen_width = info.current_w
AnchorCalculator.screen_height = info.current_h

screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN | pygame.SCALED)
window_system = WindowManager()
GlobalVariables.window_system = window_system
WindowContentFiller.define_window_manager_windows(window_system)

while GlobalVariables.game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GlobalVariables.game_running = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_ESCAPE and
                    GlobalVariables.current_window == 'main_window'):
                window_system.go_to_window('quit_window')
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                window_system.check_click(*event.pos)

    window_system.update()
    window_system.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
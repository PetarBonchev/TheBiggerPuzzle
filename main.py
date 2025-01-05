import pygame
from WindowManager import WindowManager
import Utils

pygame.init()
clock = pygame.time.Clock()

windows = WindowManager()

while Utils.game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Utils.game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Utils.game_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                windows.check_click(*event.pos)

    windows.update()
    windows.draw()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
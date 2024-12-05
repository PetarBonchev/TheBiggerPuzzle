import pygame
from UIManager import Button, Window

pygame.init()
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()
running = True

def not_run():
    globals()['running'] = False

button = Button(700, 150, screen_width / 2 - 350, 10, pygame.Color('yellow'),"The Bigger Puzzle",pygame.Color('red'),100,outline_color= pygame.Color('purple'),outline_width= 5)

quit_button = Button(50, 50, 10, 10, pygame.Color('red'), "X", pygame.Color('black'), 50, pygame.Color('black'), 2)
quit_button.add_on_click(not_run)

main_window = Window(pygame.Color('blue'))
main_window.add_button(button)
main_window.add_button(quit_button)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                main_window.check_click(*event.pos)

    main_window.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
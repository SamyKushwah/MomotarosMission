# Example file showing a circle moving on screen
import pygame
import sys

from scenes import main_menu
import game

# screen setup
pygame.init()
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()

# driver loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # run the main menu
    selection = main_menu.run_main_menu(screen, clock, 0)

    match selection:
        case "quit":
            pygame.quit()
            sys.exit()
        case "play":
            game.run_game(screen, clock)

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()

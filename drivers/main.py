import pygame
import sys
from scenes import start_screen, level_select, level_1_screen

# screen setup
pygame.init()
screen = pygame.display.set_mode((1024, 768), pygame.RESIZABLE)
clock = pygame.time.Clock()

"""
screen_w = 1024
screen_h = 768
screen = screen.Screen(screen_w, screen_h)
"""

# driver loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # run the main menu
    selection = start_screen.run_start_screen(screen)
    while True:
        match selection:
            case "quit":
                pygame.quit()
                sys.exit()
            case "play":
                # bring user to the level selection page
                selection = level_select.run_level_select_screen(screen)
            case "level_1":
                # bring the user to level 1
                selection = level_1_screen.run_level_1_screen(screen)
            case "level_2":
                # bring the user to level 2
                print("you made it to level 2!")
            case "level_3":
                # bring the user to level 3
                print("you made it to level 3!")
            case "credits":
                # bring the user to the credits page
                print("you made it to the credits!")
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000


pygame.quit()

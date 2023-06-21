import pygame
import sys
from scenes import start_screen, level_select, level_1_screen, pause_screen, win_screen, lose_screen

# screen setup
pygame.init()
# 1024, 768
screen = pygame.display.set_mode((1536, 1152), pygame.RESIZABLE)
clock = pygame.time.Clock()

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
            case "pause":
                # bring the user to the pause page
                selection = pause_screen.run_pause_screen(screen)
            case "resume":
                # resume current level - currently goes to win screen just for debugging
                selection = win_screen.run_win_screen(screen)
            case "restart":
                # restart current level
                selection = level_1_screen.run_level_1_screen(screen)
            case "home":
                # bring user back to level selection screen
                selection = level_select.run_level_select_screen(screen)
            case "next":
                # bring user to next level - currently goes to lose screen for debugging
                selection = lose_screen.run_lose_screen(screen)

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000


pygame.quit()
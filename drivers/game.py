import pygame
import sys


def run_game(screen, clock):
    # driver loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # fill the background
        screen.fill("brown4")

        # flip() the display to put your work on screen
        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            return "quit"

        dt = clock.tick(60) / 1000
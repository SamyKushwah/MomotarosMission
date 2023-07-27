import pygame
from momotaro.drivers import toolbox

def crossfade(screen1, screen2, window, clock, speed):
    curr_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen1 = pygame.transform.scale(screen1, curr_size)
    screen2 = pygame.transform.scale(screen2, curr_size)

    alpha = 0

    while alpha < 255:
        screen1.set_alpha(255 - alpha)
        screen2.set_alpha(alpha)

        window.blit(screen1, (0, 0))
        window.blit(screen2, (0, 0))

        pygame.display.update()

        alpha += speed
        clock.tick(60)

    # screen2.set_alpha(0)


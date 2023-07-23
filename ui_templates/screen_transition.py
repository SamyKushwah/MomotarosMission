import pygame
from drivers import toolbox

def crossfade(screen1, screen2, window, clock, speed):
    # pygame.transform.scale(screen1, window.get_size())
    curr_size = (pygame.display.Info().current_w - 10, pygame.display.Info().current_h - 50)
    scrren1 = pygame.transform.scale(screen1, curr_size)
    # pygame.transform.scale(screen2, window.get_size())
    screen2 = pygame.transform.scale(screen2, curr_size)

    alpha = 0
    fade_speed = 255 // speed

    while alpha < 255:
        screen1.set_alpha(255 - alpha)
        screen2.set_alpha(alpha)

        window.blit(screen1, (0, 0))
        window.blit(screen2, (0, 0))

        pygame.display.update()

        alpha += fade_speed
        clock.tick(60)
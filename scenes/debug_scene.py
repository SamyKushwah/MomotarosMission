import pygame


def create_scene(screen):
    # Load a ground platform
    ground_image = pygame.image.load("images/ground.png")
    ground_x = 0
    ground_y = 768 - 200

    screen.blit(ground_image, (ground_x, ground_y))

    return pygame.Rect(ground_x, ground_y, 1024, 200)

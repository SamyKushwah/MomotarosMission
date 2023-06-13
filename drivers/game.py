import pygame
import sys
from pygame.locals import *
from templates import controllable
from templates import borders
from scenes import debug_scene


def run_game(screen, clock):
    selected_level = 1
    player = controllable.Controllable()
    # driver loop
    running = True
    while running:

        if selected_level == 1:
            screen.fill((0, 0, 0))
            collidables = []
            collidables.append((load_debug_level(screen), "Floor"))
            collidables.append((load_platform(screen), "Floor"))
            collidables.append((load_wall(screen), "Wall"))

            player.poll_movement()
            player.check_collision(collidables)
            player.draw_sprite(screen)

        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_1:
                        selected_level = 1

        pygame.display.update()
        clock.tick(60)


def load_debug_level(screen):
    # Load a ground platform
    ground_image = pygame.image.load("images/ground.png")
    ground_x = 0
    ground_y = 768 - 200

    screen.blit(ground_image, (ground_x, ground_y))

    return pygame.Rect(ground_x, ground_y, 1024, 200)

def load_platform(screen):
    platform_image = pygame.image.load("images/platform.png")
    platform_x = 524
    platform_y = 768 - 380

    screen.blit(platform_image, (platform_x, platform_y))

    return pygame.Rect(platform_x, platform_y, 300, 50)

def load_wall(screen):
    wall_image = pygame.image.load("images/wall.png")
    wall_x = 1024-50
    wall_y = 0

    screen.blit(wall_image, (wall_x, wall_y))

    return pygame.Rect(wall_x, wall_y, 50, 568)
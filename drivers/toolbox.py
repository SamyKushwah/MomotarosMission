import pygame
import sys
import os


class Toolbox:
    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h),
                                              pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

    def draw_to_screen(self, image, location=(0, 0)):
        self.screen.blit(pygame.transform.scale(image, self.screen.get_size()), location)
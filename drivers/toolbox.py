import pygame
import sys
import os


class Toolbox:
    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode(
            (pygame.display.Info().current_w - 10, pygame.display.Info().current_h - 50),
            pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

    def draw_to_screen(self, image, location=(0, 0)):
        self.screen.blit(pygame.transform.scale(image, self.screen.get_size()), location)

    def adjusted_mouse_pos(self, mouse_loc):
        adjusted_x = (mouse_loc[0] / self.screen.get_width()) * 1920
        adjusted_y = (mouse_loc[1] / self.screen.get_height()) * 1080
        return adjusted_x, adjusted_y
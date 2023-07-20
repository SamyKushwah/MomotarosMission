import pygame
import sys
from momotaro.drivers import toolbox
import momotaro.drivers

pygame.font.init()


class TutorialText(pygame.sprite.Sprite):
    my_toolbox = toolbox.Toolbox()

    # loading the font
    font_path = "snapitc.ttf"
    #font_size = 135

    def __init__(self, location, x_min, x_max, dimensions = (100,100), font=font_path, lwd=None, text=None, font_size=30):
        pygame.sprite.Sprite.__init__(self)
        self.done = False

        self.location = location
        self.x_min = x_min
        self.x_max = x_max
        self.font = font
        self.lwd = lwd
        self.text = text
        self.dimensions = dimensions
        #self.rect = self.image.get_rect()
        self.font_size = font_size
        self.my_font = pygame.font.Font("drivers/" + self.font, self.font_size)
        '''self.text_surface = pygame.Surface(dimensions, pygame.SRCALPHA)
        self.text_surface.fill((0,0,0,0))
        self.text1_surface = self.my_font.render(self.text, False, (195, 52, 39))
        self.text_rect = self.text1_surface.get_rect()  # Set text_rect center
        self.text_rect.center = self.location'''

        self.text_surface = self.my_font.render(self.text, False, (195, 52, 39))  # red - 195, 52, 39
        self.text_rect = self.text_surface.get_rect()  # Set text_rect center
        self.text_rect.center = location

    def draw(self, surface, curr_x):
        # drawing button
        #self.rect.center = self.location
        #surface.blit(self.image, self.rect)

        # text_surface = None
        if self.font is not None and self.text is not None:
            # creating red text
            if curr_x > self.x_max:
                self.done = True
            if not self.done and self.x_min < curr_x < self.x_max:
                surface.blit(self.text_surface, self.text_rect)

# https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
# https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame